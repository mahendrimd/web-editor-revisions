# Clarify bounded document review integrity

Type: decision
Phase: assessment
Status: resolved
Recorded by: project maintainer
Blocked by:
Decision status: active
Supersedes:
Superseded by:

## Question

Should the successor describe the user-important review integrity supplied by version 1, and how should it treat ordinary compound document changes that the model cannot represent as one atomic proposal?

## Resolution

### Decision

Add an informative explanation of the review-integrity outcomes supplied for supported proposals: accepted and pending content remain distinguishable; the complete target, payload, and atomic decision can be understood; both content projections can be inspected or derived; identity and attachment remain stable through other resolutions or fail visibly; and non-equivalent preservation is reported as refusal, materialization, or loss.

State plainly that version 1 is a meaningful paragraph-local and single-boundary interoperability core, not a complete general-purpose document review-mode contract. Do not prescribe a UI, navigation method, accessibility presentation, comments, permissions, approval workflow, or code-review process.

Defer atomic multi-paragraph paste, cross-paragraph or multi-range deletion, proposal grouping or hierarchy, and predictable reshaping of pending changes as a high-priority normative follow-up. Their provisional future impact is major until a compatible optional capability, extension, or independently versioned profile is demonstrated. Do not standardize arbitrary partial acceptance in this clarification because the evidence does not establish one universal policy and splitting authored atomic intent can create invalid intermediate outcomes.

The project maintainer accepted this direction on 2026-08-30. The current informative clarification is provisionally patch; the complete baseline-to-candidate diff controls the final classification.

### Rationale

Representative document systems converge on pending changes in document context, explicit accept/reject decisions, and comprehensible resulting readings. Version 1 already supplies exact targets and payloads, stable identity, accepted-state binding, atomic projections, successor remapping, and truthful mapping outcomes for its supported subset. Those are independently useful cross-vendor guarantees even without a prescribed review surface.

Ordinary structural paste, broad deletion, suggestion joining, and hierarchical change management can exceed that subset. Treating those gaps as merely UI exclusions would hide a material change to decision boundaries. The clarification therefore makes the value and the limitation visible while reserving unresolved grouping, targeting, lineage, and atomicity design for later normative work.

Document proposal resolution differs from code review: it changes the accepted or rejected in-document content projection, whereas code review ordinarily evaluates a branch, commit, or patch for integration and can include approvals, comments, CI, mergeability, and repository policy. The analogy does not import those workflow objects into the portable document core.

### Alternatives not selected

- Claiming complete general-purpose review-mode coverage would overstate the model.
- Expanding this patch to compound semantics would precede the needed compatibility and mapping design.
- Concluding that version 1 has little or no value would ignore its exact, testable guarantees for the supported subset.
- Requiring partial acceptance of every broad proposal could destroy one authored atomic intent.

### Evidence and publication effect

The representative product, human-factors, and compound-change evidence is summarized with its limits in the [evidence index](../evidence.md). The resulting interpretation appears in [Section 3.3](../standard.md#33-informative-review-method-interpretation), its exact subset boundary appears in [Section 18](../standard.md#18-limitations-and-reassessment-triggers), and the [evaluation guide](../evaluation/README.md#informative-review-method-inspection) gives supported and unsupported scenarios. No schema, semantic rule, profile capability, or fixture activation changes.
