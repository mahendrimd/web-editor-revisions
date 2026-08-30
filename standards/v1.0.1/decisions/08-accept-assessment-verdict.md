# Accept the assessment verdict

Type: decision
Phase: assessment
Status: resolved
Recorded by: project maintainer
Blocked by: 04, 05, 06, 07
Decision status: active
Supersedes:
Superseded by:

## Question

Considering shared purpose, material benefit, stable-core feasibility, evaluability, timeliness, contradictory evidence, and risks, should the effort standardize, standardize a subset, defer, or decline, and at what depth?

## Resolution

### Decision

**Standardize a subset.** Proceed to Resolution with a useful first-version scope for portable pending revisions in text-focused Web editors.

The mandatory v1 semantic scope is:

- paragraph-local text insertion and deletion;
- replacement as an explicitly linked, atomically resolved deletion-and-insertion proposal rather than an inferred textual diff;
- a bounded set of common inline-formatting changes represented by portable before/after effective values;
- paragraph split and merge as explicit structural operations rather than character-only newline edits;
- proposal identity, pending state, selective proposal resolution, and deterministic acceptance and rejection projections;
- one canonical neutral serialization selected during Resolution; and
- explicit reporting of unsupported, unavailable, synthesized, normalized, relation-lost, structural-loss, and partial-persistence outcomes, with final terminology to be settled during Resolution.

Formatting is content-bearing for the intended use. Motivating use cases require italic styling used for taxonomic names and language-specific conventions for foreign words to survive review interchange. The model will preserve the formatting outcome without inferring whether italic means a foreign word, taxonomic name, emphasis, or another semantic role unless the source supplies that role separately.

For a portable formatting proposal, the core will record normalized effective values before and after the proposal. Mapping profiles may additionally preserve whether a value was explicit, inherited, style-derived, or theme-derived. An adapter that cannot determine or reproduce either projection must report the limitation rather than claim equivalence.

A producer records whether a change is an insertion or an atomic replacement. The standard will not infer replacement merely because a deletion and insertion are adjacent. Thus adding `u` to `color` may remain an insertion, while replacing `color` with `colour` may be one linked replacement when the authoring system records that intent.

Moves, overlapping or nested proposals, dependent proposals, arbitrary or theme-dependent formatting, lists, tables, embeds, concurrent-editing semantics, and standardization of undo/redo or vendor history are deferred from v1. Moves may be mapped to deletion and insertion only with explicit reporting that their source/destination relationship was lost.

### Rationale

The five assessment tests support this bounded verdict:

- **Shared purpose:** the reviewed Word, ODF, Reference Web Editor, and Google Docs models independently represent pending review changes and resolution outcomes, while the accepted terminology distinguishes those proposals from editing operations, history, annotations, and comments.
- **Material benefit:** the [portability evidence](../evidence.md) documents recurring skipped pending state, semantic divergence, feature-gated mappings, and repeated adapter work. The economic magnitude and breadth of demand remain unquantified, so the result supports an optional implementer standard rather than universal adoption claims.
- **Stable core:** the [text-subset evidence](../evidence.md) supports paragraph-local insertion and deletion most strongly. It also shows a feasible conceptual basis for bounded formatting through before/after values, replacement through explicit grouping, and paragraph changes through structural operations, provided Resolution defines their contracts and loss boundaries.
- **Evaluability:** the [minimal conformance experiment](../evaluation/README.md) already defines adapter-neutral pending, projection, identity, persistence, and loss observations. Resolution can extend its boundary fixtures into mandatory formatting, replacement, and paragraph fixtures.
- **Timeliness:** current review products and conversion tooling make the portability problem present rather than hypothetical, while a bounded, profile-based core avoids freezing unrelated editor architecture or experimental collaboration models.

The assessment found that an insertion/deletion-only core would omit content-significant formatting from realistic review documents. Including a bounded formatting vocabulary and linked replacement makes v1 useful without claiming portability for every source property or compound edit. Paragraph split/merge is included because it is a common text-editing operation and the evidence shows that silently flattening it to character deletion produces non-equivalent document structure.

### Rejected alternatives and trade-offs

- **Standardize the full intended domain now:** would include moves, arbitrary formatting, rich structures, overlap, dependencies, and concurrency before cross-model semantics or adopter evidence are stable. This maximizes apparent coverage but risks a vendor-shaped or untestable standard.
- **Insertion/deletion-only v1:** has the most direct evidence and simplest tests, but does not cover the identified content-bearing formatting requirements and would make common replacement and paragraph edits lossy by design.
- **Defer until the conformance experiment is executed:** would reduce implementation risk, but the evidence is already sufficient to settle a bounded semantic direction. The experiment is better used during Resolution and Validation to refine or invalidate specific requirements.
- **Decline standardization:** avoids maintenance and adoption risk, but leaves documented portability loss and repeated source-specific adapter work without a neutral target.
- **Infer replacement from adjacent edits:** could improve presentation, but would overwrite authoring intent and could merge independent proposals. Replacement must be explicit.
- **Include moves as delete-plus-insert:** produces similar accepted text in simple cases but loses one-operation identity, paired source/destination semantics, and interactions with nested content.

### Supporting and contradictory evidence

Supporting evidence includes persistent revision models in OOXML and ODF, explicit proposal and resolution behavior in the reviewed Word, Reference Web Editor, and Google Docs models, recurring insertion/deletion semantics across the sample, formatting-change concepts in multiple independent systems, and observable migration or conversion loss. The conformance design demonstrates that the core can be evaluated without choosing an editor architecture.

Contradictory evidence limits the verdict. In the reviewed boundaries, ODF text format changes may omit the actual formatting delta; Word, Google, and Reference Web Editor use materially different property, mask, and command representations; replacement atomicity is not shared; HTML and Input Events lack persistent proposal semantics; the sampled Quill Delta model requires external state to reverse deletion; and the sampled ProseMirror collaboration model does not represent reviewer acceptance or rejection. Existing pairwise converters also preserve enough accepted content for some workflows, so the standard's value is greatest when pending review state matters.

### Uncertainty, assumptions, and reassessment triggers

- The exact formatting-property vocabulary, representation of inherited or unset values, proposal metadata, target model, serialization technology, and loss-report schema remain Resolution decisions.
- The current verdict assumes adapters can normalize common effective formatting values while reporting loss of source-specific inheritance or style structure.
- The replacement contract assumes a producer can explicitly record grouping; absent grouping will not be invented by an adapter.
- No organization or implementer community has yet committed to adoption or maintenance.
- Reassess the depth if independent adapters cannot reproduce the required projections, if common formatting cannot be mapped without systematic semantic loss, if paragraph operations require a broader document tree than the bounded model can support, or if implementer feedback shows a materially different minimum useful scope.

### Follow-up work now made expressible

- Define the portable paragraph/text state and attachment model.
- Settle proposal identity, metadata, lifecycle, and conflict preconditions.
- Define the bounded formatting vocabulary and before/after value semantics.
- Define insertion, deletion, atomic replacement, formatting, and paragraph split/merge resolution behavior.
- Define loss reporting and conformance outcomes.
- Compare and select a canonical serialization after the semantic requirements stabilize.
- Turn the assessment experiment into executable conformance fixtures and choose initial mapping profiles.
