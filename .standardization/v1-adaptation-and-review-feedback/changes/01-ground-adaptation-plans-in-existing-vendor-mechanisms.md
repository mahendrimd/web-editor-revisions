# Ground adaptation plans in existing vendor mechanisms

Status: resolved
Classification: patch
Grouping: single report
Grouping rationale: not applicable
Grouping confirmed by:
Grouping confirmed on:
Disposition confirmed by: project maintainer
Disposition confirmed on: 2026-08-30

## Source reports

- Direct user feedback, observed 2026-08-30, “adapt content fragments and proposal kinds into each vendor mechanism”: adaptation plans reportedly restate or prescribe portable operations without first checking whether the vendor's internal mechanism already provides the needed transformation base. Successor-target remapping after acceptance or rejection is the apparent example. Acceptance expectation: an agent should inspect and leverage the vendor mechanism that can produce the required observable successor attachment, adding machinery only when a demonstrated gap remains.

## Problem

The baseline defines vendor-neutral proposal semantics and successor outcomes, and permits different implementation algorithms, but an agent applying the standard may mistake those observable requirements for instructions to introduce a new vendor-side operation. That can produce invasive or redundant adaptation plans and obscure the actual mapping work for content fragments and proposal kinds.

## Intended resolution

Add a core-preserving informative clarification that tells adapter planners to inventory and leverage existing vendor mechanisms before adding machinery, then prove equivalent observable outcomes. Include representative live-model and declarative-package traces without prescribing private architecture. Patch classification remains provisional until the complete baseline-to-candidate diff confirms no normative or conformance effect.

## Affected material

- `standards/v1/standard.md`, especially Sections 1, 3, 9, 10, 11, 14, and 15.
- `standards/v1/profiles/wordprocessingml.md`, `odf-text.md`, and `reference-web-editor.md` in both mapping directions.
- Direction-specific profile fixtures and any informative implementation-planning guidance.

## Tickets

- [Determine whether v1 guides mechanism-aware vendor adaptation](../tickets/01-determine-whether-v1-guides-mechanism-aware-vendor-adaptation.md)
- [Choose the mechanism-aware adaptation disposition](../tickets/03-choose-mechanism-aware-adaptation-disposition.md)
- [Define mechanism-aware clarification content](../tickets/07-define-mechanism-aware-clarification-content.md)
- [Build the successor candidate from the accepted subset](../tickets/09-build-successor-candidate-from-accepted-subset.md)
- [Confirm the target version from the complete candidate diff](../tickets/10-confirm-target-version-from-complete-diff.md)

## Disposition

Accepted for work by the project maintainer on 2026-08-30 through [Choose the mechanism-aware adaptation disposition](../tickets/03-choose-mechanism-aware-adaptation-disposition.md). The item remains nonterminal until the accepted clarification is synthesized and validated.

[Define mechanism-aware clarification content](../tickets/07-define-mechanism-aware-clarification-content.md) fixed the actual candidate boundary: an informative shared planning method in core Section 16; native-mechanism traces in each profile's informative implementation notes; and a non-normative evidence note in the profile evaluation procedure. No schema, serialization, proposal semantics, mapping outcomes, capability matrix, or fixture activation changes were authorized. That boundary carried provisional patch classification into the complete-diff review.

The complete candidate and independent falsification reviews confirmed a final **patch** classification on 2026-08-30. The implemented text is informative, all protected artifacts and capability matrices are unchanged, and no previously conforming use or implementation algorithm is affected. The project maintainer confirmed target version `1.0.1`; materialization must remove or clearly label stale inherited supporting material without adding normative content.
