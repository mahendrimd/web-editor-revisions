# Clarify user-important document review mode

Status: resolved
Classification: patch
Grouping: single report
Grouping rationale: not applicable
Grouping confirmed by:
Grouping confirmed on:
Disposition confirmed by: project maintainer
Disposition confirmed on: 2026-08-30

## Source reports

- Direct user feedback, observed 2026-08-30, “what is expected of review mode in a document”: the user asks which outcomes are important in document review mode, whether version 1 already answers that question, and whether document review mode differs materially from code-editor review mode. Acceptance expectation: establish a user-centered boundary grounded in representative evidence, then state which important outcomes version 1 covers, excludes, or leaves ambiguous.

## Problem

Version 1 defines portable pending revision semantics and explicitly excludes editor UI, comments, permissions, and workflow policy. It is not yet established whether that boundary covers the review-mode outcomes users care about most, or whether analogy to code review is causing omitted document-specific expectations or misleading implementation plans.

## Intended resolution

Identify the important user-visible outcomes of review mode in text-focused documents, compare them with code-review workflows only where the comparison clarifies scope, and assess version 1 coverage without silently expanding “review mode” into all collaboration features.

## Affected material

- `standards/v1/standard.md`, especially Purpose, Scope, Terminology, proposal lifecycle, selective resolution, projections, and excluded workflow/UI features.
- Mapping-profile claims where native review behavior affects preservation or materialization.
- Potential user-centered examples, limitations, or evaluation criteria.

## Tickets

- [Assess document review-mode expectations and v1 coverage](../tickets/02-assess-document-review-mode-expectations-and-v1-coverage.md)
- [Assess review interaction for broad and compound proposals](../tickets/05-assess-review-interaction-for-broad-and-compound-proposals.md)
- [Assess v1 review value and priority](../tickets/06-assess-v1-review-value-and-priority.md)
- [Choose the document review-mode disposition](../tickets/04-choose-document-review-mode-disposition.md)
- [Define review-mode clarification content](../tickets/08-define-review-mode-clarification-content.md)
- [Build the successor candidate from the accepted subset](../tickets/09-build-successor-candidate-from-accepted-subset.md)
- [Confirm the target version from the complete candidate diff](../tickets/10-confirm-target-version-from-complete-diff.md)

## Disposition

Accepted for a core-preserving informative clarification. The candidate should describe the P0 review-integrity outcomes already supplied by version 1 for its supported proposals and state the paragraph-local and single-boundary coverage limit without claiming a complete review-mode UI or general-purpose editor model.

Atomic multi-paragraph paste, cross-paragraph or multi-range deletion, proposal groups or hierarchy, and material reshaping of pending changes are not folded into this patch. They are recorded as a separate, high-priority normative change item. Arbitrary partial acceptance within every broad proposal remains unresolved rather than assumed.

Classification is provisionally patch because the accepted change clarifies existing semantics and limitations without changing conformance. If synthesis adds a normative recommendation or obligation, return the item to Assessment and classify it at least minor.

[Define review-mode clarification content](../tickets/08-define-review-mode-clarification-content.md) fixed the actual candidate boundary: an informative scope subsection containing the P0 review-integrity interpretation and document-versus-code-review distinction; an exact bounded-coverage statement in the core limitations; aligned publication and evaluation guidance; and curated evidence provenance. It authorized no schema, proposal-semantic, profile-capability, or fixture change. That boundary carried provisional patch classification into the complete-diff review.

The complete candidate and independent falsification reviews confirmed a final **patch** classification on 2026-08-30. The added interpretation and limitations only expose outcomes and boundaries already fixed by the unchanged normative model; they add no review-surface or conformance obligation. The project maintainer confirmed target version `1.0.1`; exact materialization must keep the clarification concise and remove stale or duplicative supporting content before acceptance.
