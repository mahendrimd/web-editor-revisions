# Materialize and verify the version-confirmed candidate

Type: task
Phase: validation
Status: resolved
Claimed by: /root
Blocked by: 10

## Completion criterion

Using the maintainer-confirmed target version, resolve the configured publication directory and release tag; materialize consistent candidate metadata, release date, history locator, planned released status, and pending acceptance record throughout the bundle; replace provisional command paths and publication-version claims while preserving semantic model and independently versioned profile identifiers; replace, rename as explicitly historical, or remove the inherited v1 validation report and repair every affected decision and publication link; audit and eliminate avoidable bloat, stale text, and harmful duplication while retaining required layer-specific summaries and durable rationale; update the release validation and compatibility summary; build and verify a bounded current-site candidate preview or record the exact pre-cutover verification plan; run all structural, core, profile, link, anchor, metadata, and baseline-to-candidate traceability checks against the materialized location; and leave `Acceptance status: pending` while preserving the exact bytes for maintainer review.

## Resolution

Materialized the exact [version 1.0.1 candidate](../candidate/README.md) for future canonical directory `standards/v1.0.1`, release date `2026-08-30`, release tag and history locator `web-editor-revisions-v1.0.1`, planned release status `released`, patch increment, and pending acceptance and propagation states. The [release record](../candidate/release.md), [core standard](../candidate/standard.md), publication index, evaluation guide, evidence, and provenance now use consistent final-ready publication metadata while retaining semantic model version `1`, serialization profile `json-jcs-1`, and profile version `1`.

### Hygiene and curation

- Removed the inherited `validation-report.md`, whose v1 date, source paths, decision counts, commands, and closeout claims were stale for 1.0.1. Current validation is consolidated in `release.md`; the original remains recoverable in `standards/v1` and tag `web-editor-revisions-v1`.
- Removed release-specific decision `23-record-maintainer-review.md` from the successor bundle. It designated only the v1 release and remains preserved with that predecessor. Applicable semantic and conformance decisions remain.
- Repaired the retained direction-specific fixture decision's validation link to the immutable v1-tagged historical report.
- Replaced every provisional publication version, directory, date, tag, history, increment, and command path with its exact 1.0.1 value. The only release fields still pending are acceptance and propagation, as required by the lifecycle.
- Scanned exact long-line duplication across the bundle. No new guidance is duplicated verbatim. Repeats are limited to inherited standalone-profile BCP 14 and fixture-authority boilerplate plus two independently scoped persistence rows; they remain intentional.
- Retained the short layer-specific review-limit summaries because the core, publication index, evaluation guide, evidence, provenance, decision record, and release manifest each serve a distinct normative-boundary, navigation, inspection, source, rationale, or release-history purpose.

### Verification

The 28-file candidate was copied unchanged into a temporary `standards/v1.0.1` layout and tested from that future location:

- all 22 Markdown files passed relative-target and heading-anchor validation;
- structural release-candidate validation passed;
- all 13 core evaluation groups passed;
- profile requirements catalog and claim schema validation passed;
- profile self-test passed all 12 positive and 11 negative packages;
- the normative schema, serialization fixture, profile requirements catalog, profile-claim schema, core runner, and profile validator remain byte-identical to version 1;
- profile diffs remain confined to informative Section 11 notes, leaving all six capability matrices unchanged;
- no stale `standards/v1` reproduction command remains; the sole `standards/v1/` occurrence is an intentional immutable historical URL; and
- the accepted-bundle validator fails only on `Acceptance status: pending`, proving that no other release field or placeholder blocks maintainer acceptance.

The current exact candidate file-manifest digest is `2cffdc201006780a049a1675f1128f57153d6619f2a82dbf373a42c69a227115`, computed as SHA-256 over the sorted per-file SHA-256 manifest in the candidate path. This digest must be recomputed before the exact-bundle decision because any later byte change invalidates it.

### Publication-surface plan

Because the canonical `standards/v1.0.1` directory does not exist before acceptance and promotion, the [release record](../candidate/release.md#publication-and-propagation) now contains a bounded pre-cutover site plan rather than a misleading preview. It specifies the exact source-root change in `site/build.py`, retains `/v1/` as the configured current route, updates labels and generated metadata to 1.0.1, names the temporary build and verification commands, and requires rendered-to-canonical comparison before release commit and deployment.

The candidate remains `drafting` solely because exact-bundle maintainer acceptance is still pending.
