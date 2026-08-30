# Clarify mechanism-aware adaptation planning

Type: decision
Phase: assessment
Status: resolved
Recorded by: project maintainer
Blocked by:
Decision status: active
Supersedes:
Superseded by:

## Question

Should the successor clarify how an adapter plan relates portable content fragments, proposal kinds, resolution, and successor attachment to a vendor's existing mechanisms, and if so should that clarification prescribe an implementation architecture?

## Resolution

### Decision

Add an informative “inventory and leverage, then prove” planning method to the core and representative mechanism traces to the three mapping profiles. An adapter plan begins by inspecting the authoritative native model, maps each claimed semantic unit to the smallest existing mechanism that can preserve it, and adds configuration, sidecars, or adapter-local transforms only for demonstrated gaps. Observable projections, identity, successor attachment, reports, and persistence remain the proof boundary.

Do not require a named remapping API, a portable-model-shaped internal store, or any other private vendor architecture. Live markers and operations, package-tree transforms, core resolution followed by regeneration, and reconstruction are all potentially valid bases.

The project maintainer accepted this direction on 2026-08-30. Its provisional release classification is patch because it adds only informative planning guidance. The complete baseline-to-candidate diff controls the final classification.

### Rationale

The core and profiles already specify observable outcomes rather than internal calls or storage. The reviewed mechanisms include WordprocessingML tracked-revision trees, ODF change regions and marks, and Reference Web Editor suggestion records with markers and live positions. Their planning steps were distributed across architecture boundaries, mappings, loss rules, fixtures, and brief notes, which made it too easy to misread successor remapping as a demand for redundant machinery.

Native reuse is not sufficient evidence by itself. ODF formatting and replacement have semantic gaps, WordprocessingML lacks a profiled atomic replacement relation and portable paragraph-identity carrier, and live markers can collapse, join, or attach differently. The accepted sequence therefore couples reuse with explicit observation, truthful loss or refusal, and rollback.

### Alternatives not selected

- Leaving all planning guidance to adopters would preserve the baseline text but not address the recurring comprehension failure.
- A normative requirement to prefer existing mechanisms could constrain valid implementations when native behavior is absent, inaccessible, or incompatible.
- A required generic remapping service or internal portable model would contradict the architecture-neutral scope.

### Evidence and publication effect

The reviewed evidence is summarized in the [evidence index](../evidence.md). The resulting informative method appears in [Section 16.1](../standard.md#161-informative-adapter-planning-method), with concrete traces in each profile's informative implementation notes and a planning note in the [evaluation guide](../evaluation/README.md#profile-evaluation). No schema, semantic rule, profile capability, or fixture activation changes.
