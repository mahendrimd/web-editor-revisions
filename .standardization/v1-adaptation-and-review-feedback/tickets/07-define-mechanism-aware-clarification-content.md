# Define mechanism-aware clarification content

Type: task
Phase: resolution
Status: resolved
Claimed by: /root
Blocked by: 03

## Completion criterion

Identify the exact baseline sections, minimum informative “inventory and leverage, then prove” sequence, live-model and declarative-package traces, candidate evaluation checks, and confirmed patch compatibility effect for [Ground adaptation plans in existing vendor mechanisms](../changes/01-ground-adaptation-plans-in-existing-vendor-mechanisms.md), without drafting a required private architecture or new conformance obligation.

## Resolution

### Exact candidate placement

The candidate should make only informative changes in these locations:

1. **`standard.md`, Section 16, Mapping profiles:** add an explicitly informative adapter-planning subsection after the profile boundary and before or immediately after the initial profile list. This is the shared “inventory and leverage, then prove” method.
2. **`profiles/wordprocessingml.md`, Section 11, Informative implementation notes:** extend the existing library/API note with one declarative-package trace using revision elements and package/tree reconstruction.
3. **`profiles/odf-text.md`, Section 11, Informative implementation notes:** extend the existing library/API note with one declarative-package trace using change regions, marks, reconstruction, and explicit native semantic gaps.
4. **`profiles/reference-web-editor.md`, Section 11, Informative implementation notes:** extend the existing pinned-model note with one live-model trace using suggestion records, markers/live ranges, model operations, accept/discard commands, and persistence readback.
5. **`evaluation/README.md`, Profile evaluation:** add an informative planning/evidence note explaining that a claim package should name the authoritative native mechanism and any demonstrated adapter-added mechanism, while conformance remains determined by the existing activated fixtures and observed outcomes.

No schema, canonical serialization, proposal kind, mapping-outcome vocabulary, profile capability matrix, or fixture activation should change for this item.

### Minimum shared informative sequence

The shared method must preserve this order:

1. Identify the exact profile, direction, pinned upstream version, source/output boundary, persistence boundary, and claimed proposal kinds.
2. Inventory the host's existing authoritative mechanisms for accepted content, native changes, resolution, coordinate transformation or reconstruction, projection generation, serialization, persistence, and any established sidecars.
3. Map each core content fragment and claimed proposal kind to the smallest existing native unit that can preserve its semantic observation; record unsupported kinds and relations rather than assuming a new implementation.
4. Identify the existing native operation, tree transform, regeneration step, or reconstruction that yields accept/reject outcomes and the successor attachment of every remaining pending proposal.
5. Compare the observed accepted state, acceptance and rejection projections, proposal identity, association and same-point ordering, unmappable-target behavior, and persistence result with the existing core and profile requirements.
6. Add configuration, sidecar data, or adapter-local transformation only for a demonstrated mismatch, and document why the existing mechanism is insufficient. Reuse alone is not proof.
7. Reopen or reload the declared persistence boundary, bind observations and any declared adaptation or loss to the mapping report, and refuse or roll back when the claimed equivalence cannot be established.

The text must say that this is a planning method, not a required implementation architecture or preference for native APIs over another valid implementation.

### Required worked mechanism traces

- **Reference Web Editor live model:** accepted content and suggestions already live in the pinned editor model. An adapter should inspect suggestion records, markers/live ranges, model operations, accept/discard commands, projection generation, and persistence integration. When proposal A resolves, native operations transform the marker for remaining proposal B. The adapter reads B's resulting attachment, converts it to the successor core target and fingerprint, and verifies v1 association, ordering, identity, and unmappable-target rules. A new general remapping call is added only for a proven gap; marker collapse, auto-joining, or incompatible stickiness requires configuration, sidecar data, refusal, or rollback rather than blind trust.
- **WordprocessingML declarative package:** the adapter should inspect tracked-revision elements, the document/run tree, effective formatting, and the selected XML library, SDK, or application API. It may resolve in core and regenerate remaining native revisions, or mutate the package tree and reconstruct remaining targets. Reopening the package and comparing projections, identity observations, and remaining attachments is the proof boundary. Absence of a live coordinate service is not a requirement to invent one.
- **ODF Text declarative package:** the adapter should inspect `text:tracked-changes`, typed `text:changed-region` records, referenced change marks, accepted-content reconstruction, and the chosen library or application API. It may resolve in core and regenerate the package, or mutate regions and reconstruct marks, then independently reopen and verify. Missing exact format deltas and atomic replacement relations are demonstrated gaps requiring extension, reported loss, or refusal—not reasons to duplicate every core operation inside the ODF model.

Each trace must map content fragments and proposal kinds through existing native constructs and end at observable projections, successor attachment, mapping report, and persistence. Product or library method names remain examples only.

### Candidate evaluation checks

1. Every added passage is labeled informative and introduces no new RFC 2119/8174 keyword or equivalent conformance obligation.
2. A terminology review confirms that “mechanism,” “operation,” “proposal,” “mapping,” “remapping,” and “projection” retain their released meanings; no native edit operation is presented as a portable revision proposal merely because it produces similar content.
3. Each profile trace identifies the existing authoritative mechanism before any adapter-added mechanism and includes a concrete counterexample showing why native behavior still requires verification.
4. No passage requires a named SDK, library, API call, internal portable-model store, general `remapTargets` service, or private vendor architecture.
5. The core schema, serialization fixtures, `profile-requirements.json`, marked profile matrices, and profile-claim schema remain byte-for-byte unchanged unless the item is returned to Assessment.
6. Run the existing core suite, profile catalog check, and profile self-test. Results must remain unchanged because the item adds no conformance case.
7. Review the complete baseline-to-candidate diff and confirm that every new statement either restates an existing outcome requirement or is clearly described as non-normative planning advice.

### Compatibility effect

The confirmed provisional classification remains **patch**. The defined candidate content changes discoverability, examples, and planning order only. It does not change a conforming interchange document, resolver, adapter, mapping outcome, profile capability, fixture obligation, or previously valid implementation algorithm.

If synthesis adds any normative recommendation, requires reuse of a native mechanism, changes a profile claim package requirement, or activates new fixture evidence, [Ground adaptation plans in existing vendor mechanisms](../changes/01-ground-adaptation-plans-in-existing-vendor-mechanisms.md) must return to Assessment and be reclassified at least minor.
