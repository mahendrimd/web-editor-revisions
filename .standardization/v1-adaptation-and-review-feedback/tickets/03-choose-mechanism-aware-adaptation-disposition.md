# Choose the mechanism-aware adaptation disposition

Type: decision
Phase: assessment
Status: resolved
Claimed by: /root
Blocked by: 01
Decision status: active
Supersedes:
Superseded by:

## Question

Should this revision accept the reported adaptation-planning problem for a core-preserving informative clarification that requires plans to inventory and leverage existing vendor mechanisms before adding machinery, defer it to implementation-specific adopter work, or reject it because version 1's architecture-neutral clauses and mapping profiles are already sufficient; and what provisional compatibility classification follows from that chosen depth?

## Resolution

### Decision

Accept [Ground adaptation plans in existing vendor mechanisms](../changes/01-ground-adaptation-plans-in-existing-vendor-mechanisms.md) for a core-preserving informative clarification. The successor should give adapter planners an explicit “inventory and leverage, then prove” sequence and representative worked traces for a live-marker model and a declarative package model. It must not require a vendor to add a named remapping call, portable-model-shaped internal store, or other private architecture.

The provisional standard-version classification is **patch** because the accepted direction clarifies how to apply existing architecture-neutral requirements without changing normative semantics or conformance. If synthesis introduces a new normative recommendation, capability, or conformance obligation, the item must return to Assessment and be reclassified at least minor as the complete diff requires.

Accepted by the project maintainer on 2026-08-30.

### Rationale

[Mechanism-aware vendor adaptation in version 1](../evidence/01-mechanism-aware-vendor-adaptation.md) found that the core and all six profile directions already define observable outcomes and native mapping boundaries rather than required internal methods. Reference Web Editor markers and live positions provide an existing transformation base; WordprocessingML and ODF adapters can use existing package/tree transforms or resolve in core and regenerate remaining native records. The observed agent failure is therefore a documentation and planning-method problem: relevant instructions are distributed across the architecture disclaimer, mapping tables, permitted adaptations, loss rules, fixtures, and short implementation notes.

An explicit reuse-first planning sequence addresses the demonstrated comprehension problem while preserving the foundational decision not to standardize private runtime architecture. Patch classification is appropriate only while the clarification remains informative and conformance-neutral.

### Rejected alternatives and trade-offs

- **Defer entirely to adopter-specific documentation:** would keep the release unchanged, but would leave a recurring standards-application failure unaddressed even though the reusable planning boundary is now evidence-backed across three materially different mechanisms.
- **Reject because v1 is already semantically sufficient:** correctly observes that conforming outcomes are already defined, but ignores that agents can still misread those outcomes as required new machinery because no explicit mechanism-inventory sequence or worked trace exists.
- **Add a normative reuse requirement:** would make the instruction more forceful, but “existing mechanism” is implementation-dependent and may be absent, inaccessible, or nonconforming. A normative preference could constrain valid adapter designs and would require at least minor classification and additional conformance analysis.
- **Require a named remapping API or portable internal model:** would directly contradict v1's architecture-neutral boundary and exclude valid marker-, operation-, reconstruction-, and regeneration-based implementations.

### Supporting and contradictory evidence

Supporting evidence includes the core's explicit permission for markers, operations, eager or lazy transformation, or another algorithm; direction-specific native mapping tables; outcome-based fixture matrices; CKEditor live ranges that transform with model operations; and file-format profiles that rely on reconstruction, XML/application transforms, and save/reload verification.

Contradictory evidence prevents an unconditional native-reuse rule. ODF formatting and atomic replacement have documented semantic gaps; WordprocessingML lacks a profiled atomic replacement relation and portable paragraph-identity carrier; and native live markers can merge, collapse, or attach differently from v1. The clarification must therefore say “leverage, then prove,” with extension, sidecar data, refusal, or rollback for demonstrated mismatches.

### Uncertainty and assumptions

- The exact placement and wording remain synthesis work; this decision authorizes the bounded clarification, not draft clauses.
- Patch classification assumes no new normative or conformance effect. The final baseline-to-candidate diff controls classification.
- Worked traces should illustrate mechanism selection and observation boundaries without making CKEditor, an XML library, or an application API the required implementation.
- Concrete adopter plans still require inspection of the installed vendor version and target codebase.

### Follow-up work now made expressible

- In Resolution, decide the minimum durable content of the informative planning sequence and worked traces if their detailed boundary could change conformance interpretation.
- In Synthesis, add the accepted mechanism inventory, smallest-gap adaptation rule, projection/attachment proof step, and live-model/declarative-package examples.
- In Validation, verify that the resulting text never implies a required private architecture and that every new statement traces to existing requirements or is clearly informative.
