#!/usr/bin/env python3
"""Verify generated Pages routes, internal links, fragments, and artifacts."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


DEFAULT_BASE_URL = "/web-editor-revisions"


@dataclass
class Document:
    ids: set[str] = field(default_factory=set)
    links: list[str] = field(default_factory=list)
    main_count: int = 0
    h1_count: int = 0


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.document = Document()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.document.ids.add(attributes["id"] or "")
        if tag == "main":
            self.document.main_count += 1
        if tag == "h1":
            self.document.h1_count += 1
        if tag in {"a", "link"} and attributes.get("href"):
            self.document.links.append(attributes["href"] or "")
        if tag in {"script", "img"} and attributes.get("src"):
            self.document.links.append(attributes["src"] or "")


def normalize_base_url(value: str) -> str:
    if not value or value == "/":
        return ""
    return "/" + value.strip("/")


def public_url(path: Path, output: Path, base_url: str) -> str:
    relative = path.relative_to(output).as_posix()
    if relative == "index.html":
        return base_url + "/"
    if relative.endswith("/index.html"):
        return base_url + "/" + relative.removesuffix("index.html")
    return base_url + "/" + relative


def target_path(parsed_path: str, output: Path, base_url: str) -> Path | None:
    path = unquote(parsed_path)
    if base_url:
        if path.startswith(base_url + "/"):
            path = path[len(base_url) :]
        elif path == base_url:
            path = "/"
        elif path.startswith("/"):
            return None

    relative = path.lstrip("/")
    candidate = output / relative
    if path.endswith("/") or not Path(relative).suffix:
        directory_index = candidate / "index.html"
        if directory_index.exists():
            return directory_index
    return candidate


def verify(output: Path, base_url: str) -> None:
    errors: list[str] = []
    documents: dict[Path, Document] = {}

    html_files = sorted(output.rglob("*.html"))
    if not html_files:
        errors.append("No generated HTML files found")

    for path in html_files:
        parser = DocumentParser()
        parser.feed(path.read_text())
        document = parser.document
        documents[path] = document
        if document.main_count != 1:
            errors.append(f"{path.relative_to(output)} has {document.main_count} main elements")
        if document.h1_count != 1:
            errors.append(f"{path.relative_to(output)} has {document.h1_count} h1 elements")

    for source, document in documents.items():
        source_url = public_url(source, output, base_url)
        for href in document.links:
            parsed = urlparse(href)
            if parsed.scheme in {"http", "https", "mailto", "data"} or href.startswith("//"):
                continue
            absolute = urlparse(urljoin(source_url, href))
            target = target_path(absolute.path, output, base_url)
            if target is None:
                errors.append(f"{source.relative_to(output)} escapes the Pages base path: {href}")
                continue
            if not target.exists():
                errors.append(f"{source.relative_to(output)} links to missing target: {href}")
                continue
            if absolute.fragment and target.suffix == ".html":
                target_document = documents.get(target)
                if target_document is None:
                    parser = DocumentParser()
                    parser.feed(target.read_text())
                    target_document = parser.document
                    documents[target] = target_document
                if unquote(absolute.fragment) not in target_document.ids:
                    errors.append(
                        f"{source.relative_to(output)} links to missing fragment: {href}"
                    )

    expected = [
        "index.html",
        "v1/index.html",
        "v1/standard/index.html",
        "v1/schema/index.html",
        "v1/profiles/index.html",
        "v1/conformance/index.html",
        "v1/evidence/index.html",
        "v1/decisions/index.html",
        "v1/release/index.html",
        "v1/publication.json",
        "search-index.json",
        "llms.txt",
        "assets/style.css",
        "assets/site.js",
        "downloads/LICENSE.txt",
        "downloads/NOTICE.txt",
        "404.html",
    ]
    for relative in expected:
        if not (output / relative).is_file():
            errors.append(f"Missing required output: {relative}")

    json_files = [
        output / "v1/publication.json",
        output / "search-index.json",
        output / "v1/schema/web-editor-revisions-v1.schema.json",
        output / "v1/conformance/artifacts/profile-claim.schema.json",
        output / "v1/conformance/artifacts/profile-requirements.json",
        output / "v1/conformance/artifacts/fixtures/serialization-cases.json",
    ]
    for path in json_files:
        try:
            json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid or missing JSON {path.relative_to(output)}: {exc}")

    if list(output.rglob("*.md")):
        errors.append("Generated output unexpectedly contains Markdown source files")

    if errors:
        raise SystemExit("Site verification failed:\n- " + "\n- ".join(errors))

    print(f"Verified {len(html_files)} HTML pages and all internal links")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("_site"))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()
    verify(args.output.resolve(), normalize_base_url(args.base_url))


if __name__ == "__main__":
    main()
