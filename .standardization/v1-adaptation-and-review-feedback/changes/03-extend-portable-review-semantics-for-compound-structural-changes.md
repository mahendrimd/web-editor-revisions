# Extend portable review semantics for compound structural changes

Status: deferred
Classification: major
Grouping: single report
Grouping rationale: not applicable
Grouping confirmed by:
Grouping confirmed on:
Disposition confirmed by: project maintainer
Disposition confirmed on: 2026-08-30

## Source reports

- Direct user feedback, observed 2026-08-30, asking whether omission of interactions considered important in a review-mode editor would leave the standard with little or no added value and proposing a priority scale. Acceptance expectation: distinguish the bounded value already supplied by version 1 from missing capabilities that materially limit a general-purpose review-mode claim, and preserve high-priority missing semantics as real normative work.

## Problem

Version 1 cannot generally represent one atomic multi-paragraph paste, cross-paragraph or multi-range deletion, proposal group or hierarchy, or material expansion or shrinkage of a pending proposal while preserving one semantic identity. These interactions occur in representative document-review systems. An adapter may therefore have to split authored intent, materialize changes, refuse the mapping, or report review-semantics loss for ordinary editing behavior.

## Intended resolution

In a later linked revision or expansion assessment, define portable compound-review semantics that preserve complete decision scope, explicit atomicity, accepted and rejected projections, predictable pending-change evolution, deterministic successor attachment, and truthful vendor mapping. Compare immutable groups, multi-target proposals, lineage, or other designs before choosing a representation. Do not assume universal partial acceptance or silently mutable proposal identity.

## Affected material

- `standards/v1/standard.md`, especially accepted state and targets, proposal identity and lifecycle, proposal kinds, selective resolution, successor remapping, conformance, compatibility, and versioning.
- Canonical schema and serialization if new proposal or target forms affect parsing, validation, canonical bytes, or fingerprints.
- WordprocessingML, OpenDocument, and Reference Web Editor profile mappings and refusal cases.
- Projection fixtures, compatibility matrices, migration guidance, and review-method examples.

## Tickets

- [Assess review interaction for broad and compound proposals](../tickets/05-assess-review-interaction-for-broad-and-compound-proposals.md)
- [Assess v1 review value and priority](../tickets/06-assess-v1-review-value-and-priority.md)
- [Choose the document review-mode disposition](../tickets/04-choose-document-review-mode-disposition.md)

## Disposition

Deferred from the current patch revision and preserved as a high-priority normative follow-up. The stable need is established, but the representation, resolution contract, vendor feasibility, and compatibility boundary are not settled enough for synthesis.

The provisional future impact is major because the work may change core proposal, targeting, compatibility, resolution, parsing, or serialization semantics. A later effort may lower the classification only if it demonstrates a compatible optional capability, extension, or independently versioned profile that preserves every previously conforming use.
