# Choose the first standardization boundary

Type: decision
Phase: discovery
Status: resolved
Recorded by: project maintainer
Blocked by: 02, 03
Decision status: active
Supersedes:
Superseded by:

## Question

What shared expectation should this effort target first, which adopters should it serve, and which concrete interoperability or provenance benefit should justify it: a common vocabulary and conceptual model, an implementable interchange data model with resolution semantics, a Web-platform serialization or API, or a deliberately staged combination?

## Resolution

### Decision

Create an independent open implementer specification for portable pending revisions in text-focused Web editors. The authoritative core will define a vendor-neutral semantic model, one canonical neutral serialization, observable accept/reject outcomes, revision identity preservation, and explicit reporting when an implementation cannot preserve a standardized concept.

The first maintained content subset is text runs, paragraph boundaries, and inline formatting. Common review operations such as insertion, deletion, and replacement are candidates for later normative definition. Lists, tables, embeds, spreadsheets, presentations, specialist desktop-publishing semantics, and other structural revisions are deferred until evidence shows a concrete portability need.

The primary adopters are Web-editor and document import/export or integration implementers. The intended benefit is that clients and end users can migrate between vendors without silent loss of supported pending revisions or dependence on one vendor ecosystem.

The core will define vendor-neutral mapping and conformance requirements. Mappings for named formats, APIs, or vendors will live in separate profiles and may become normative when sufficiently stable; a vendor change must not destabilize the core. The specification will standardize portable data and observable semantic outcomes, not user interfaces, storage topology, permissions, collaboration architecture, or internal editor design.

### Rationale

The [normative-model comparison](../evidence.md) found no existing source that spans persistent revision data, portable metadata, edit intent, and accept/reject semantics. OOXML and ODF demonstrate rich persistent models but also format- and content-family-specific behavior. The [Web-editor comparison](../evidence.md) found independent proposal systems with identity and accept/reject outcomes, alongside operation/history systems that do not natively model pending proposals. Together they support a small, layered proposal model and contradict a universal internal editor architecture.

A canonical serialization is included to demonstrate practical interchange rather than stopping at vocabulary. Keeping its semantic model authoritative and named-vendor mappings separate protects neutrality. A maintained subset with explicit loss reporting is better supported than a claim of lossless coverage for rich office-document behavior that the first adopters do not need.

### Rejected alternatives and trade-offs

- **Terminology-only guidance:** easier to publish, but would not demonstrate migration or give implementers an interoperable artifact.
- **Immediate HTML, JavaScript, or browser API standardization:** could improve platform integration, but current evidence does not establish browser-engine requirements and would prematurely bind the model to one runtime surface.
- **A universal editor-operation, undo, or collaboration model:** would conflict with the documented ProseMirror and Quill counterexamples and unnecessarily constrain OT, CRDT, and application architectures.
- **Complete lossless OOXML/ODF abstraction:** would pull moves, dependencies, rich structure, and format-specific semantics into the initial core and undermine maintainability.
- **Named vendor behavior in the core:** would make vendor changes a source of instability. Separate profiles retain practical mappings without transferring vendor ownership into the core.
- **Data interchange without behavioral conformance:** would allow implementations to serialize the same record while producing incompatible accept/reject outcomes.

### Contradictory evidence and limitations

Pending review is not universal among Web editors; some widely used frameworks model applied operations or history instead. Existing review systems disagree about storage, anchoring, structural changes, provenance requirements, nesting, grouping, and whether replacement is atomic. No current evidence establishes adoption demand across vendors or proves that the proposed subset can round-trip without loss. The motivating use case is plain and formatted text; urgency for richer structures is unknown.

### Uncertainty and assumptions

- The canonical serialization technology remains undecided.
- The exact required metadata, anchoring rules, operation vocabulary, formatting representation, and terminal-state retention remain undecided.
- “Explicit loss reporting” requires later conformance semantics and test fixtures.
- Named mapping profiles are expected, but which formats or APIs receive the first profiles depends on feasibility and adopter value.
- Formal standards-body submission is not an initial goal; it may be reconsidered after implementer evidence exists.

### Follow-up work now made expressible

- Reconcile the normative vocabulary for proposal, revision, tracked change, history, operation, and resolution.
- Assess whether the selected text-focused subset and one canonical serialization are technically feasible and worth standardizing now.
- Identify the smallest conformance experiment that can test semantic preservation, accept/reject outcomes, and explicit loss reporting across representative adapters.
