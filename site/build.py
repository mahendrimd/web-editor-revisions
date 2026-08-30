#!/usr/bin/env python3
"""Build the Web Editor Revisions static publication site."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

import markdown


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
GITHUB_REPOSITORY = os.environ.get(
    "GITHUB_REPOSITORY", "mahendrimd/web-editor-revisions"
)
GITHUB_OWNER = GITHUB_REPOSITORY.partition("/")[0]
REPOSITORY_URL = (
    f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com').rstrip('/')}"
    f"/{GITHUB_REPOSITORY}"
)
CANONICAL_ORIGIN = os.environ.get(
    "PAGES_ORIGIN", f"https://{GITHUB_OWNER}.github.io"
).rstrip("/")
DEFAULT_BASE_URL = "/web-editor-revisions"
PUBLICATION_ROOT = ROOT / "standards/v1.0.1"
PUBLICATION_VERSION = "1.0.1"
RELEASE_TAG = "web-editor-revisions-v1.0.1"


@dataclass(frozen=True)
class Page:
    source: Path | None
    route: str
    title: str
    description: str
    status: str
    nav_key: str


CORE_PAGES = [
    Page(
        PUBLICATION_ROOT / "README.md",
        "/v1/",
        "Version 1.0.1 publication",
        "Publication map, adoption path, version boundary, and known limits.",
        "Publication index",
        "publication",
    ),
    Page(
        PUBLICATION_ROOT / "standard.md",
        "/v1/standard/",
        "Web Editor Revisions",
        "Normative core semantics, serialization, loss reporting, and conformance requirements.",
        "Normative · Version 1.0.1",
        "standard",
    ),
    Page(
        None,
        "/v1/schema/",
        "Normative JSON Schema",
        "The structural contract for Web Editor Revisions version 1 interchange documents.",
        "Normative · Version 1.0.1",
        "schema",
    ),
    Page(
        None,
        "/v1/profiles/",
        "Mapping profiles",
        "Direction-specific mappings between the core model and selected document or editor formats.",
        "Normative profiles · Version 1.0.1",
        "profiles",
    ),
    Page(
        PUBLICATION_ROOT / "profiles/wordprocessingml.md",
        "/v1/profiles/wordprocessingml/",
        "WordprocessingML Tracked Revisions Mapping Profile",
        "Normative mapping profile for Strict WordprocessingML tracked revisions.",
        "Normative profile · Version 1.0.1",
        "profiles",
    ),
    Page(
        PUBLICATION_ROOT / "profiles/odf-text.md",
        "/v1/profiles/odf-text/",
        "ODF Text Change Tracking Mapping Profile",
        "Normative mapping profile for ODF Text 1.4 change tracking.",
        "Normative profile · Version 1.0.1",
        "profiles",
    ),
    Page(
        PUBLICATION_ROOT / "profiles/reference-web-editor.md",
        "/v1/profiles/reference-web-editor/",
        "Reference Web Editor Track Changes Mapping Profile",
        "Normative mapping profile for the pinned Reference Web Editor snapshot.",
        "Normative profile · Version 1.0.1",
        "profiles",
    ),
    Page(
        PUBLICATION_ROOT / "evaluation/README.md",
        "/v1/conformance/",
        "Evaluation and claim packaging",
        "Executable core evaluation and reproducible profile claim guidance.",
        "Informative · Evaluation procedure",
        "conformance",
    ),
    Page(
        PUBLICATION_ROOT / "evidence.md",
        "/v1/evidence/",
        "Evidence index",
        "Primary-source support, contrary evidence, uncertainty, and reassessment boundaries.",
        "Informative · Supporting material",
        "evidence",
    ),
    Page(
        PUBLICATION_ROOT / "provenance.md",
        "/v1/decisions/",
        "Decision provenance",
        "Material design choices, alternatives, retained tensions, and maintenance guidance.",
        "Informative · Decision records",
        "decisions",
    ),
    Page(
        PUBLICATION_ROOT / "release.md",
        "/v1/release/",
        "Version 1.0.1 release record",
        "Change set, compatibility, validation, acceptance, and propagation record.",
        "Informative · Release record",
        "release",
    ),
]


def normalize_base_url(value: str) -> str:
    value = value.strip()
    if not value or value == "/":
        return ""
    return "/" + value.strip("/")


def route_url(base_url: str, route: str) -> str:
    if not route.startswith("/"):
        route = "/" + route
    return f"{base_url}{route}"


def output_path(output_dir: Path, route: str) -> Path:
    route = route.strip("/")
    if not route:
        return output_dir / "index.html"
    return output_dir / route / "index.html"


def source_route_map(pages: list[Page]) -> dict[Path, str]:
    mapping = {page.source.resolve(): page.route for page in pages if page.source}
    for decision in (PUBLICATION_ROOT / "decisions").glob("*.md"):
        mapping[decision.resolve()] = f"/v1/decisions/{decision.stem}/"
    return mapping


def resolve_source_target(source: Path, target: str) -> Path:
    resolved = (source.parent / target).resolve()
    if resolved.is_dir():
        resolved = resolved / "README.md"
    return resolved


def public_artifact_route(path: Path) -> str | None:
    path = path.resolve()
    schema_root = (PUBLICATION_ROOT / "schema").resolve()
    evaluation_root = (PUBLICATION_ROOT / "evaluation").resolve()
    try:
        return "/v1/schema/" + path.relative_to(schema_root).as_posix()
    except ValueError:
        pass
    try:
        relative = path.relative_to(evaluation_root)
        if relative.name != "README.md" and "__pycache__" not in relative.parts:
            return "/v1/conformance/artifacts/" + relative.as_posix()
    except ValueError:
        pass
    return None


LINK_PATTERN = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")


def rewrite_markdown_links(
    text: str, source: Path, routes: dict[Path, str], base_url: str
) -> str:
    def replace(match: re.Match[str]) -> str:
        label, raw_target = match.groups()
        target = raw_target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        path_part, marker, fragment = target.partition("#")
        resolved = resolve_source_target(source, path_part)
        route = routes.get(resolved)
        if route is None:
            route = public_artifact_route(resolved)
        if route is None and resolved == (ROOT / "LICENSE").resolve():
            route = "/license/"
        if route is None and resolved == (ROOT / ".gitignore").resolve():
            href = f"{REPOSITORY_URL}/blob/main/.gitignore"
        elif route is None:
            href = f"{REPOSITORY_URL}/blob/main/{quote(resolved.relative_to(ROOT).as_posix())}"
        else:
            href = route_url(base_url, route)
        if marker:
            href += "#" + fragment
        return f"[{label}]({href})"

    return LINK_PATTERN.sub(replace, text)


def markdown_slug(value: str, separator: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\- ]", "", value.lower(), flags=re.UNICODE)
    value = re.sub(r"[\s\-]+", separator, value).strip(separator)
    return value


def render_markdown(
    source: Path, routes: dict[Path, str], base_url: str
) -> tuple[str, list[dict[str, object]]]:
    text = rewrite_markdown_links(source.read_text(), source, routes, base_url)
    renderer = markdown.Markdown(
        extensions=["fenced_code", "sane_lists", "tables", "toc"],
        extension_configs={
            "toc": {
                "anchorlink": False,
                "permalink": False,
                "slugify": markdown_slug,
                "toc_depth": "2-3",
            }
        },
        output_format="html5",
    )
    return renderer.convert(text), renderer.toc_tokens


def nested_toc(items: list[dict[str, object]]) -> str:
    if not items:
        return ""
    links: list[str] = ["<ol>"]
    for item in items:
        item_id = html.escape(str(item["id"]), quote=True)
        name = html.escape(str(item["name"]))
        links.append(f'<li><a href="#{item_id}">{name}</a>')
        children = item.get("children", [])
        if isinstance(children, list) and children:
            links.append(nested_toc(children))
        links.append("</li>")
    links.append("</ol>")
    return "".join(links)


def active_class(current: str, route: str, exact: bool = False) -> str:
    active = current == route if exact else current.startswith(route)
    return ' class="active" aria-current="page"' if active else ""


def sidebar(base_url: str, current: str) -> str:
    def link(label: str, route: str, exact: bool = False) -> str:
        return (
            f'<a{active_class(current, route, exact)} '
            f'href="{route_url(base_url, route)}">{html.escape(label)}</a>'
        )

    return f"""
      <nav class="side-nav" aria-label="Publication navigation">
        <p class="side-nav-label">Version 1.0.1</p>
        {link("Publication", "/v1/", True)}
        <p class="side-nav-label">Normative</p>
        {link("Core standard", "/v1/standard/")}
        {link("JSON Schema", "/v1/schema/")}
        {link("Mapping profiles", "/v1/profiles/")}
        <div class="side-nav-nested">
          {link("WordprocessingML", "/v1/profiles/wordprocessingml/")}
          {link("ODF Text", "/v1/profiles/odf-text/")}
          {link("Reference Web Editor", "/v1/profiles/reference-web-editor/")}
        </div>
        <p class="side-nav-label">Implementation</p>
        {link("Conformance", "/v1/conformance/")}
        <p class="side-nav-label">Supporting</p>
        {link("Evidence", "/v1/evidence/")}
        {link("Decision records", "/v1/decisions/")}
        {link("Release record", "/v1/release/")}
      </nav>
    """


def global_header(base_url: str, current: str) -> str:
    menu_button = (
        '<button class="menu-toggle" type="button" aria-expanded="false" '
        'aria-controls="site-sidebar">Menu</button>'
        if current != "/"
        else ""
    )
    return f"""
    <header class="site-header">
      <div class="header-inner">
        <a class="site-name" href="{route_url(base_url, '/')}">Web Editor Revisions</a>
        <span class="version-mark">v1.0.1</span>
        <nav class="global-nav" aria-label="Primary navigation">
          <a{active_class(current, "/v1/standard/")} href="{route_url(base_url, '/v1/standard/')}">Standard</a>
          <a{active_class(current, "/v1/profiles/")} href="{route_url(base_url, '/v1/profiles/')}">Profiles</a>
          <a{active_class(current, "/v1/conformance/")} href="{route_url(base_url, '/v1/conformance/')}">Conformance</a>
          <button class="search-open" type="button" aria-haspopup="dialog">Search</button>
          <a href="{REPOSITORY_URL}">GitHub</a>
        </nav>
        {menu_button}
      </div>
    </header>
    """


def search_dialog(base_url: str) -> str:
    return f"""
    <dialog class="search-dialog" aria-labelledby="search-title">
      <form method="dialog" class="search-heading">
        <label id="search-title" for="site-search">Search the publication</label>
        <button type="submit" class="search-close">Close</button>
      </form>
      <input id="site-search" type="search" autocomplete="off" placeholder="Standard, profile, requirement…">
      <p class="search-hint">Search titles, headings, and publication text.</p>
      <ol class="search-results" aria-live="polite"></ol>
    </dialog>
    <script src="{route_url(base_url, '/assets/site.js')}" defer></script>
    """


def source_url(source: Path | None) -> str | None:
    if source is None:
        return None
    return f"{REPOSITORY_URL}/blob/main/{source.relative_to(ROOT).as_posix()}"


def render_page(
    page: Page,
    content: str,
    toc: list[dict[str, object]],
    base_url: str,
    *,
    source_override: str | None = None,
) -> str:
    canonical = f"{CANONICAL_ORIGIN}{route_url(base_url, page.route)}"
    document_title = (
        page.title
        if page.title == "Web Editor Revisions"
        else f"{page.title} · Web Editor Revisions"
    )
    source = source_override or source_url(page.source)
    source_link = (
        f'<a href="{source}">View source</a>' if source else ""
    )
    toc_markup = nested_toc(toc)
    aside = (
        f'<aside class="page-toc" aria-label="On this page"><p>On this page</p>{toc_markup}</aside>'
        if toc_markup
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(document_title)}</title>
  <meta name="description" content="{html.escape(page.description, quote=True)}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="{route_url(base_url, '/assets/style.css')}">
  <meta name="color-scheme" content="light dark">
</head>
<body data-base-url="{html.escape(base_url, quote=True)}">
  <a class="skip-link" href="#main-content">Skip to content</a>
  {global_header(base_url, page.route)}
  <div class="docs-shell">
    <aside class="site-sidebar" id="site-sidebar">{sidebar(base_url, page.route)}</aside>
    <main id="main-content" class="document-main">
      <div class="document-status"><span>{html.escape(page.status)}</span>{source_link}</div>
      <article class="prose">{content}</article>
      <nav class="document-footer" aria-label="Document resources">
        {source_link}
        <a href="{route_url(base_url, '/v1/publication.json')}">Publication metadata</a>
      </nav>
    </main>
    {aside}
  </div>
  <footer class="site-footer">
    <p>Independent implementer specification. Apache-2.0 licensed.</p>
    <p><a href="{route_url(base_url, '/about/')}">About</a> · <a href="{route_url(base_url, '/license/')}">License</a> · <a href="{route_url(base_url, '/llms.txt')}">llms.txt</a></p>
  </footer>
  {search_dialog(base_url)}
</body>
</html>
"""


def render_home(base_url: str) -> str:
    standard = route_url(base_url, "/v1/standard/")
    conformance = route_url(base_url, "/v1/conformance/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Web Editor Revisions</title>
  <meta name="description" content="A portable model for pending revisions in text-focused Web editors.">
  <link rel="canonical" href="{CANONICAL_ORIGIN}{route_url(base_url, '/')}">
  <link rel="stylesheet" href="{route_url(base_url, '/assets/style.css')}">
  <meta name="color-scheme" content="light dark">
</head>
<body data-base-url="{html.escape(base_url, quote=True)}">
  <a class="skip-link" href="#main-content">Skip to content</a>
  {global_header(base_url, '/')}
  <main id="main-content" class="home-main">
    <section class="home-intro" aria-labelledby="home-title">
      <p class="eyebrow">Independent implementer specification</p>
      <h1 id="home-title">Portable pending revisions for Web editors.</h1>
      <p class="home-summary">A vendor-neutral interchange model for preserving, resolving, and truthfully reporting pending changes in text-focused editors.</p>
      <p class="publication-state"><span>Maintainer-reviewed</span><span>Version 1.0.1</span><span>Released</span></p>
      <div class="primary-actions">
        <a class="primary-button" href="{standard}">Read the standard</a>
        <a href="{conformance}">Implement and evaluate</a>
      </div>
    </section>

    <section class="home-section" aria-labelledby="start-title">
      <h2 id="start-title">Start with your task</h2>
      <div class="task-list">
        <a href="{standard}"><strong>Understand the model</strong><span>Core terminology, semantics, and resolution behavior</span></a>
        <a href="{conformance}"><strong>Implement the standard</strong><span>Roles, schema, evaluation, and claim packaging</span></a>
        <a href="{route_url(base_url, '/v1/profiles/')}"><strong>Build an adapter</strong><span>Direction-specific format and editor mapping profiles</span></a>
      </div>
    </section>

    <section class="home-grid" aria-label="Version 1.0.1 publication">
      <div>
        <p class="eyebrow">Normative publication</p>
        <h2>Version 1.0.1</h2>
        <p>The bounded core covers insertion, deletion, replacement, four inline-formatting properties, paragraph split and merge, selective resolution, canonical JSON, and explicit loss reporting.</p>
        <ul class="plain-links">
          <li><a href="{standard}">Core standard</a></li>
          <li><a href="{route_url(base_url, '/v1/schema/')}">Normative JSON Schema</a></li>
          <li><a href="{route_url(base_url, '/v1/profiles/')}">Mapping profiles</a></li>
        </ul>
      </div>
      <div>
        <p class="eyebrow">Supporting material</p>
        <h2>Trace and verify</h2>
        <p>Evaluation procedures, curated evidence, decision records, and the durable release record remain separate from normative requirements.</p>
        <ul class="plain-links">
          <li><a href="{conformance}">Evaluation and claim packaging</a></li>
          <li><a href="{route_url(base_url, '/v1/evidence/')}">Evidence index</a></li>
          <li><a href="{route_url(base_url, '/v1/decisions/')}">Decision records</a></li>
          <li><a href="{route_url(base_url, '/v1/release/')}">Release record</a></li>
        </ul>
      </div>
    </section>

    <aside class="independence-note">
      <strong>Independent project.</strong> This publication is not affiliated with, authorized, sponsored, endorsed, or approved by any referenced vendor, open-source project, or standards organization.
    </aside>
  </main>
  <footer class="site-footer home-footer">
    <p>Copyright 2026 Mahendri Dwicahyo.</p>
    <p><a href="{route_url(base_url, '/about/')}">About</a> · <a href="{route_url(base_url, '/license/')}">Apache 2.0</a> · <a href="{REPOSITORY_URL}">GitHub</a> · <a href="{route_url(base_url, '/llms.txt')}">llms.txt</a></p>
  </footer>
  {search_dialog(base_url)}
</body>
</html>
"""


def render_profiles_index(base_url: str) -> str:
    items = [
        ("WordprocessingML", "Strict WordprocessingML tracked revisions", "/v1/profiles/wordprocessingml/"),
        ("ODF Text", "ODF Text 1.4 change tracking", "/v1/profiles/odf-text/"),
        ("Reference Web Editor", "Pinned Web editor track-changes behavior", "/v1/profiles/reference-web-editor/"),
    ]
    cards = "".join(
        f'<li><a href="{route_url(base_url, route)}"><strong>{name}</strong><span>{description}</span></a></li>'
        for name, description, route in items
    )
    return f"""
<h1>Mapping profiles</h1>
<p>Profiles define direction-specific mappings between the version 1 core and a pinned native document or editor boundary. Each profile versions independently from the core.</p>
<ul class="profile-list">{cards}</ul>
<h2 id="claim-boundary">Claim boundary</h2>
<p>A conformance claim selects one profile, one direction, a pinned upstream version, declared capabilities, and a measured persistence boundary. A profile does not claim universal support for its source format or product.</p>
<p><a href="{route_url(base_url, '/v1/conformance/')}">Continue to evaluation and claim packaging.</a></p>
"""


def render_schema_page(base_url: str) -> str:
    schema_path = PUBLICATION_ROOT / "schema/web-editor-revisions-v1.schema.json"
    schema = html.escape(schema_path.read_text())
    raw_url = route_url(base_url, "/v1/schema/web-editor-revisions-v1.schema.json")
    return f"""
<h1>Normative JSON Schema</h1>
<p>The schema defines the structural contract for version 1 interchange documents. It applies together with the semantic requirements in the <a href="{route_url(base_url, '/v1/standard/')}">core standard</a>.</p>
<p class="artifact-actions"><a class="primary-button" href="{raw_url}" download>Download schema</a><a href="{REPOSITORY_URL}/blob/main/standards/v1.0.1/schema/web-editor-revisions-v1.schema.json">View source</a></p>
<h2 id="schema-source">Schema source</h2>
<pre class="schema-view"><code>{schema}</code></pre>
"""


def render_decisions_index(base_url: str) -> str:
    rows = []
    for path in sorted((PUBLICATION_ROOT / "decisions").glob("*.md")):
        text = path.read_text()
        title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
        phase_match = re.search(r"^Phase: (.+)$", text, re.MULTILINE)
        title = title_match.group(1) if title_match else path.stem
        phase = phase_match.group(1) if phase_match else "—"
        route = f"/v1/decisions/{path.stem}/"
        number = path.name.split("-", 1)[0]
        rows.append(
            f'<tr><td>{number}</td><td><a href="{route_url(base_url, route)}">{html.escape(title)}</a></td><td>{html.escape(phase.title())}</td><td>Active</td></tr>'
        )
    return f"""
<h1>Decision provenance</h1>
<p>This index records why the material boundaries in the publication exist. Decision records are informative maintenance inputs; normative documents control if a summary differs.</p>
<div class="table-scroll"><table><thead><tr><th>Record</th><th>Decision</th><th>Phase</th><th>Status</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<h2 id="maintenance-use">Maintenance use</h2>
<p>Future changes should identify the decision they alter, preserve contrary evidence, and update the corresponding normative material and evaluation coverage together.</p>
"""


def render_about(base_url: str) -> str:
    return f"""
<h1>About this publication</h1>
<p>Web Editor Revisions is an independent implementer specification for portable pending revisions in text-focused Web editors. It is maintained by the repository owner and published as a versioned, reproducible set.</p>
<h2 id="independence">Independence</h2>
<p>The project is not an official standard and is not affiliated with, authorized, sponsored, endorsed, or approved by any referenced vendor, open-source project, or standards organization. Product and organization names identify technical sources and interoperability boundaries only.</p>
<h2 id="publication-boundary">Publication boundary</h2>
<p>Version 1.0.1 is identified by the release tag <code>web-editor-revisions-v1.0.1</code>. The core, serialization profile, and mapping profiles version independently. Claims should remain pinned to the exact publication commit and measured implementation boundary.</p>
<h2 id="source-and-license">Source and license</h2>
<p>The complete source is available on <a href="{REPOSITORY_URL}">GitHub</a>. Original specification text, schemas, evaluation code, fixtures, and supporting material are licensed under the <a href="{route_url(base_url, '/license/')}">Apache License 2.0</a>.</p>
"""


def render_license(base_url: str) -> str:
    license_text = html.escape((ROOT / "LICENSE").read_text())
    notice_text = html.escape((ROOT / "NOTICE").read_text())
    return f"""
<h1>License and notice</h1>
<p>The original specification text, schemas, evaluation code, fixtures, and supporting material are licensed under the Apache License 2.0. External specifications, documentation, products, and projects remain subject to their owners’ terms.</p>
<p class="artifact-actions"><a href="{route_url(base_url, '/downloads/LICENSE.txt')}" download>Download LICENSE</a><a href="{route_url(base_url, '/downloads/NOTICE.txt')}" download>Download NOTICE</a></p>
<h2 id="apache-license">Apache License 2.0</h2>
<pre class="license-view">{license_text}</pre>
<h2 id="notice">Notice</h2>
<pre class="license-view">{notice_text}</pre>
"""


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


def plain_text(markup: str) -> str:
    parser = TextExtractor()
    parser.feed(markup)
    return parser.text()


def write_page(output_dir: Path, route: str, markup: str) -> None:
    path = output_path(output_dir, route)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markup)


def copy_artifacts(output_dir: Path) -> None:
    schema_source = PUBLICATION_ROOT / "schema/web-editor-revisions-v1.schema.json"
    schema_target = output_dir / "v1/schema/web-editor-revisions-v1.schema.json"
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(schema_source, schema_target)

    evaluation_source = PUBLICATION_ROOT / "evaluation"
    evaluation_target = output_dir / "v1/conformance/artifacts"
    for source in evaluation_source.rglob("*"):
        relative = source.relative_to(evaluation_source)
        if source.is_dir() or source.name == "README.md" or "__pycache__" in relative.parts:
            continue
        target = evaluation_target / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    downloads = output_dir / "downloads"
    downloads.mkdir()
    shutil.copy2(ROOT / "LICENSE", downloads / "LICENSE.txt")
    shutil.copy2(ROOT / "NOTICE", downloads / "NOTICE.txt")


def publication_metadata(base_url: str, decision_pages: list[Page]) -> dict[str, object]:
    def entry(page: Page) -> dict[str, str]:
        result = {
            "title": page.title,
            "url": f"{CANONICAL_ORIGIN}{route_url(base_url, page.route)}",
            "status": page.status,
        }
        if page.source:
            result["source"] = source_url(page.source) or ""
        return result

    return {
        "publication": "Web Editor Revisions",
        "publicationSet": f"web-editor-revisions-v{PUBLICATION_VERSION}",
        "releaseTag": RELEASE_TAG,
        "status": "maintainer-reviewed",
        "coreModelVersion": "1",
        "serializationProfile": "json-jcs-1",
        "canonicalUrl": f"{CANONICAL_ORIGIN}{route_url(base_url, '/v1/')}",
        "repository": REPOSITORY_URL,
        "normative": [entry(page) for page in CORE_PAGES if page.status.startswith("Normative")],
        "informative": [entry(page) for page in CORE_PAGES if page.status.startswith("Informative")],
        "decisions": [entry(page) for page in decision_pages],
        "artifacts": {
            "schema": f"{CANONICAL_ORIGIN}{route_url(base_url, '/v1/schema/web-editor-revisions-v1.schema.json')}",
            "evaluation": f"{CANONICAL_ORIGIN}{route_url(base_url, '/v1/conformance/artifacts/')}",
        },
    }


def write_support_files(
    output_dir: Path,
    base_url: str,
    rendered: list[tuple[Page, str]],
    decision_pages: list[Page],
) -> None:
    metadata = publication_metadata(base_url, decision_pages)
    publication_path = output_dir / "v1/publication.json"
    publication_path.parent.mkdir(parents=True, exist_ok=True)
    publication_path.write_text(json.dumps(metadata, indent=2) + "\n")

    search_entries = []
    for page, markup in rendered:
        search_entries.append(
            {
                "title": page.title,
                "description": page.description,
                "url": route_url(base_url, page.route),
                "text": plain_text(markup),
            }
        )
    (output_dir / "search-index.json").write_text(json.dumps(search_entries, separators=(",", ":")))

    llms = f"""# Web Editor Revisions

> Independent implementer specification for portable pending revisions in text-focused Web editors.

Status: Maintainer-reviewed version 1.0.1
Publication set: web-editor-revisions-v1.0.1
Core model: 1
Serialization profile: json-jcs-1
Canonical publication: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/')}
Repository: {REPOSITORY_URL}

## Normative documents

- Core standard: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/standard/')}
- JSON Schema: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/schema/web-editor-revisions-v1.schema.json')}
- Mapping profiles: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/profiles/')}

## Implementation and evaluation

- Evaluation and claim packaging: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/conformance/')}
- Evaluation artifacts: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/conformance/artifacts/')}

## Informative supporting material

- Evidence index: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/evidence/')}
- Decision records: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/decisions/')}
- Release record: {CANONICAL_ORIGIN}{route_url(base_url, '/v1/release/')}

Normative requirements are only those identified as normative by the core standard or a mapping profile. Evaluation instructions, provenance, rationale, and examples are informative unless a normative document explicitly incorporates them.
"""
    (output_dir / "llms.txt").write_text(llms)

    urls = [f"{CANONICAL_ORIGIN}{route_url(base_url, page.route)}" for page, _ in rendered]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{html.escape(url)}</loc></url>\n" for url in urls)
    sitemap += "</urlset>\n"
    (output_dir / "sitemap.xml").write_text(sitemap)
    (output_dir / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {CANONICAL_ORIGIN}{route_url(base_url, '/sitemap.xml')}\n"
    )
    (output_dir / ".nojekyll").write_text("")


def build(output_dir: Path, base_url: str) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    decision_pages = []
    for path in sorted((PUBLICATION_ROOT / "decisions").glob("*.md")):
        match = re.search(r"^# (.+)$", path.read_text(), re.MULTILINE)
        title = match.group(1) if match else path.stem
        decision_pages.append(
            Page(
                path,
                f"/v1/decisions/{path.stem}/",
                title,
                "Authoritative project decision record supporting the version 1.0.1 publication.",
                "Informative · Active decision record",
                "decisions",
            )
        )

    all_source_pages = CORE_PAGES + decision_pages
    routes = source_route_map(all_source_pages)
    rendered: list[tuple[Page, str]] = []

    home_page = Page(None, "/", "Web Editor Revisions", "A portable model for pending revisions in text-focused Web editors.", "", "home")
    home = render_home(base_url)
    write_page(output_dir, "/", home)
    rendered.append((home_page, home))

    for page in all_source_pages:
        if page.route == "/v1/profiles/":
            content = render_profiles_index(base_url)
            toc = [{"id": "claim-boundary", "name": "Claim boundary", "children": []}]
            source_override = f"{REPOSITORY_URL}/tree/main/standards/v1.0.1/profiles"
        elif page.route == "/v1/schema/":
            content = render_schema_page(base_url)
            toc = [{"id": "schema-source", "name": "Schema source", "children": []}]
            source_override = f"{REPOSITORY_URL}/blob/main/standards/v1.0.1/schema/web-editor-revisions-v1.schema.json"
        elif page.route == "/v1/decisions/":
            content = render_decisions_index(base_url)
            toc = [{"id": "maintenance-use", "name": "Maintenance use", "children": []}]
            source_override = source_url(page.source)
        else:
            if page.source is None:
                raise RuntimeError(f"No source for {page.route}")
            content, toc = render_markdown(page.source, routes, base_url)
            source_override = None
        page_markup = render_page(page, content, toc, base_url, source_override=source_override)
        write_page(output_dir, page.route, page_markup)
        rendered.append((page, page_markup))

    about_page = Page(None, "/about/", "About this publication", "Project purpose, independence, publication boundary, source, and license.", "Project information", "about")
    about_content = render_about(base_url)
    about_markup = render_page(about_page, about_content, [], base_url, source_override=f"{REPOSITORY_URL}/blob/main/README.md")
    write_page(output_dir, about_page.route, about_markup)
    rendered.append((about_page, about_markup))

    license_page = Page(None, "/license/", "License and notice", "Apache License 2.0 and project notice.", "Legal", "license")
    license_content = render_license(base_url)
    license_markup = render_page(license_page, license_content, [], base_url, source_override=f"{REPOSITORY_URL}/blob/main/LICENSE")
    write_page(output_dir, license_page.route, license_markup)
    rendered.append((license_page, license_markup))

    error_page = Page(None, "/404.html", "Page not found", "The requested page was not found.", "", "")
    error_content = f"""<h1>Page not found</h1><p>The requested page does not exist. Return to the <a href="{route_url(base_url, '/')}">publication index</a> or use search.</p>"""
    error_markup = render_page(error_page, error_content, [], base_url)
    (output_dir / "404.html").write_text(error_markup)

    assets = output_dir / "assets"
    assets.mkdir()
    shutil.copy2(SITE_DIR / "style.css", assets / "style.css")
    shutil.copy2(SITE_DIR / "site.js", assets / "site.js")
    copy_artifacts(output_dir)
    write_support_files(output_dir, base_url, rendered, decision_pages)

    print(f"Built {len(rendered)} pages in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()
    build(args.output.resolve(), normalize_base_url(args.base_url))


if __name__ == "__main__":
    main()
