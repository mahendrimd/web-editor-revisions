# Web Editor Revisions 1.0.1

Standard identity: web-editor-revisions
Version: 1.0.1
Status: released
Release date: 2026-08-30
Predecessor version: 1
Predecessor tag: web-editor-revisions-v1
History locator: web-editor-revisions-v1.0.1
Release tag: web-editor-revisions-v1.0.1
Version policy: standard-versioning
Minimum classification: patch
Confirmed increment: patch
Publication directory: standards/v1.0.1
Acceptance status: accepted
Propagation status: complete

## Summary

This patch release adds two informative clarifications to version 1. It explains how adapter plans can inventory and leverage existing vendor mechanisms before adding machinery, while proving the same portable observations. It also explains the user-facing document-review integrity supplied by the supported subset and states the paragraph-local and single-boundary limits that prevent an unqualified general-purpose review-mode claim. Compound structural proposal semantics remain a named, high-priority deferred change.

The semantic model, canonical serialization, schema, proposal kinds and resolution rules, mapping outcomes, profile capability matrices, and fixture activation are unchanged.

## Change items

### C01 — Ground adaptation plans in existing vendor mechanisms

Disposition: resolved
Disposition confirmation: not applicable
Source reports: Direct project-maintainer feedback observed 2026-08-30
Classification: patch
Affected material: Core Section 16.1; Section 11 of the WordprocessingML, ODF Text, and Reference Web Editor profiles; profile evaluation guidance; evidence; decision provenance
Resolution: Add an explicitly informative “inventory and leverage, then prove” planning sequence and three mechanism traces. The guidance requires no named API, internal portable store, or private architecture; existing live transformation, package-tree mutation, regeneration, and reconstruction remain valid when their observable outcomes pass the existing requirements.
Decision record: [Mechanism-aware adaptation planning](decisions/26-clarify-mechanism-aware-adaptation-planning.md)

### C02 — Clarify user-important document review mode

Disposition: resolved
Disposition confirmation: not applicable
Source reports: Direct project-maintainer feedback observed 2026-08-30
Classification: patch
Affected material: Core Sections 3.3 and 18; publication summary and known limits; informative review-method evaluation; evidence; decision provenance
Resolution: Explain the review-integrity outcomes supplied for supported proposals, distinguish document proposal resolution from code-review integration workflow, and describe version 1 as a useful bounded core rather than a complete general-purpose review-mode contract. The clarification prescribes no UI, workflow, accessibility presentation, comments, permissions, or approval system.
Decision record: [Bounded document review integrity](decisions/27-clarify-bounded-document-review-integrity.md)

### C03 — Extend portable review semantics for compound structural changes

Disposition: deferred
Disposition confirmation: project maintainer, 2026-08-30
Source reports: Direct project-maintainer feedback observed 2026-08-30 during assessment of broad paste, deletion, and pending-change interaction
Classification: major
Affected material: No normative release material; limitations, evidence, and future reassessment scope only
Resolution: Preserve atomic multi-paragraph paste, cross-paragraph or multi-range deletion, proposal groups or hierarchy, and predictable pending-change reshaping as a high-priority normative follow-up. The exact grouping, targeting, lineage, resolution, mapping, and compatibility design remains unresolved. Arbitrary partial acceptance is not adopted as a universal requirement.
Decision record: [Bounded document review integrity](decisions/27-clarify-bounded-document-review-integrity.md)

## Compatibility and migration

The two resolved items are informative and have no normative, conformance, serialization, or migration effect. Every document, behavior, profile claim, and implementation algorithm conforming to version 1 remains conforming to version 1.0.1. The deferred major item does not affect this release's increment. No adopter action is required to migrate from version 1.

## Current decisions and evidence

Applicable inherited version 1 design decisions remain in [the decision directory](decisions/) and are indexed in [decision provenance](provenance.md). Version 1's release-specific maintainer-review decision and validation report remain reconstructable from immutable tag `web-editor-revisions-v1`; they are not duplicated here. The two decisions reviewed for this revision are [Mechanism-aware adaptation planning](decisions/26-clarify-mechanism-aware-adaptation-planning.md) and [Bounded document review integrity](decisions/27-clarify-bounded-document-review-integrity.md).

The [evidence index](evidence.md) retains the version 1 source basis and identifies evidence reviewed through 2026-08-30 for native mechanism reuse, document review outcomes, the code-review boundary, and compound structural limitations. The product evidence establishes mechanisms and recurring review outcomes, not adoption prevalence or a population-level preference ranking.

## Validation and acceptance

Synthesis checks passed on 2026-08-30: structural release validation; all 13 existing core evaluation groups; the profile requirements catalog and claim schema check; and the profile self-test with 12 positive and 11 negative packages. The normative schema, serialization fixture, profile requirements catalog, profile-claim schema, core runner, and profile validator are byte-identical to version 1. Profile diffs are confined to Section 11 informative notes, leaving all six marked capability matrices unchanged.

Complete baseline-to-candidate traceability and classification review found no normative or conformance effect. An independent falsification review reached the same patch conclusion, and the project maintainer confirmed version 1.0.1 on 2026-08-30. Materialization removed the stale v1 validation report and release-specific v1 maintainer decision from this bundle, repaired the remaining historical link, updated versioned commands and metadata, and found no harmful duplicate new guidance.

The exact materialized layout at `standards/v1.0.1` was reproduced in a temporary tree and passed relative-link and heading-anchor checks across all 22 Markdown files, structural release validation, all 13 core groups, the profile catalog check, and the profile self-test with 12 positive and 11 negative packages. Protected schemas, fixtures, catalog, and evaluators remain byte-identical to version 1; profile diffs remain confined to informative Section 11 notes.

On 2026-08-30, the project maintainer accepted the exact 28-file materialized bundle identified before the acceptance-record update by SHA-256 manifest digest `2cffdc201006780a049a1675f1128f57153d6619f2a82dbf373a42c69a227115`. No normative content revision was requested. The maintainer authorized the scoped release commit, immutable `web-editor-revisions-v1.0.1` tag, configured deployment, and a subsequent operational storage correction from side-by-side retention to single-current tagged history. That correction changes only release-storage and propagation wording; immutable tag `web-editor-revisions-v1` preserves the predecessor.

## Publication and propagation

The canonical release directory is `standards/v1.0.1`. Under single-current tagged history, cutover removes `standards/v1` from the active tree only after verifying immutable tag `web-editor-revisions-v1`; that tag preserves the complete predecessor. Version 1 remains authoritative until cutover.

The current GitHub Pages surface is generated by `site/build.py` and verified by `site/verify.py`. The repository-resident cutover maps every current-page source and artifact root to `standards/v1.0.1`, labels the publication 1.0.1, retains the `/v1/` current-route namespace, and publishes this durable release record in place of the removed v1 validation report. Before the release commit, a fresh temporary build produced 27 publication pages and verification passed across all 28 generated HTML pages, internal links, fragments, JSON artifacts, and 1.0.1 source links.

[GitHub Pages workflow run 33294205531](https://github.com/mahendrimd/web-editor-revisions/actions/runs/33294205531) successfully built and deployed release commit `781a21f9ef33b21f73a7f7d20d394d30454d54f4` on 2026-08-30. Observable checks at 2026-08-30T12:14:55+07:00 returned HTTP 200 for the [current publication](https://mahendrimd.github.io/web-editor-revisions/), [release record](https://mahendrimd.github.io/web-editor-revisions/v1/release/), and [publication metadata](https://mahendrimd.github.io/web-editor-revisions/v1/publication.json); the outputs identify publication set and tag `web-editor-revisions-v1.0.1`. Required propagation is complete.

## Notifications

No notification targets are configured.
