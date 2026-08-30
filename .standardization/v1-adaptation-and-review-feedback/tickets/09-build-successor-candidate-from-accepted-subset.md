# Build the successor candidate from the accepted subset

Type: task
Phase: synthesis
Status: resolved
Claimed by: /root
Blocked by: 07, 08

## Completion criterion

Create an unversioned successor candidate by seeding the complete version 1 publication bundle and applying only the two resolved informative clarifications: the mechanism-aware planning method and vendor traces defined by [Define mechanism-aware clarification content](07-define-mechanism-aware-clarification-content.md), and the bounded review-integrity interpretation defined by [Define review-mode clarification content](08-define-review-mode-clarification-content.md). Add a provisional `release.md`; retain applicable decisions and curated evidence, including the deferred compound-semantic change; keep schema, serialization, normative proposal semantics, profile capability matrices, and fixture activation unchanged; run the core and profile evaluation commands plus structural candidate validation; and leave the target version pending until complete-diff classification review and user confirmation.

## Resolution

Created the complete unversioned [successor candidate](../candidate/README.md) by seeding the accepted version 1 publication bundle and applying only the two accepted informative clarifications.

The mechanism-aware change appears in core Section 16.1, the three profile Section 11 implementation notes, profile evaluation guidance, curated evidence, and [Mechanism-aware adaptation planning](../candidate/decisions/26-clarify-mechanism-aware-adaptation-planning.md). The review-integrity change appears in core Sections 3.3 and 18, the publication summary and limits, informative evaluation scenarios, curated evidence, and [Bounded document review integrity](../candidate/decisions/27-clarify-bounded-document-review-integrity.md). The [provisional release record](../candidate/release.md) retains both resolved outcomes and the deferred compound-semantic item.

The candidate adds no compound target, group, hierarchy, pending-edit lineage, or partial-acceptance semantics. The normative schema, serialization fixture, profile requirements catalog, profile-claim schema, core runner, and profile validator are byte-identical to version 1. Profile diffs are confined to the informative Section 11 notes, so their marked capability matrices and fixture activation are unchanged.

Checks run on 2026-08-30:

- core evaluation: 13 of 13 groups passed;
- profile requirements catalog and claim schema: passed;
- profile self-test: 12 positive and 11 negative packages passed;
- structural release-candidate validation: passed; and
- baseline comparison: only the authorized prose, evidence, decision, provenance, candidate metadata, and release-record files differ.

The candidate remains `drafting`. Its publication version, directory, date, release tag, and target version remain pending the complete-diff classification review, independent challenge, and project-maintainer confirmation required in Validation.
