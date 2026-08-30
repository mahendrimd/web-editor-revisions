# Define proposal identity, metadata, and lifecycle

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 08
Decision status: active
Supersedes:
Superseded by:

## Question

Which proposal identity, provenance, state, base-state or conflict precondition, and lifecycle fields must v1 preserve or synthesize so proposals remain independently resolvable across adapters while terminal-record retention remains optional?

## Resolution

### Decision

Every v1 revision proposal has a mandatory opaque portable identifier. It is unique within the portable document lineage, remains stable across adapter boundaries, persistence, target remapping, and any retained terminal record, and is never reused. The core does not require a UUID, URI, globally registered namespace, or a particular lexical form beyond constraints later imposed by the canonical serialization.

An adapter preserves a source identifier as the portable identifier when it is usable without collision. If the source has no identifier, or its identifier is incompatible or collides within the portable lineage, the adapter synthesizes a portable identifier and reports the synthesis. A distinct source-system identifier and source proposal identifier may be retained as optional provenance.

A proposal's semantic identity is immutable. Its base-state reference, target, change kind, and change payload cannot materially change while retaining the same portable identifier. A materially different proposed edit receives a new identifier. Optional nonsemantic metadata may be added or enriched without changing identity. V1 does not standardize the editing history by which an author composed or revised a proposal.

Every accepted semantic document state used as a proposal base has a deterministic verifiable fingerprint, and each pending proposal references the exact base-state fingerprint against which its target is interpreted. When resolution creates a successor accepted state, that state receives its own fingerprint and every remaining proposal is deterministically remapped to, and references, that successor. The fingerprint is an interchange and persistence precondition, not a required runtime representation: editors may internally use live markers, object references, version clocks, transformed positions, or any other architecture. The canonical serialization decision will fix the semantic encoding and digest algorithm. A source-system revision or version token may be retained as optional provenance but is not a substitute for the verifiable portable fingerprint.

Core provenance fields are optional but preserve-if-present: proposal creator, creation time, source system, and source proposal identifier. A retained terminal record may additionally carry an optional resolver and resolution time. A source or Web editor may introduce and use these fields even though their absence does not make a proposal invalid. An adapter does not invent source provenance silently; omission, redaction, normalization, or synthesis is reported when it affects a mapping claim.

The v1 review-state vocabulary is `pending`, `accepted`, and `rejected`. Resolution is one-way from `pending` to either terminal state. Stale-base, conflicted, unmappable, unsupported, or partially persisted conditions are processing or conformance outcomes, not review states. When the base fingerprint does not match or a target cannot be deterministically remapped, the proposal remains pending and unchanged while the condition is reported for an adapter or user to repair. The implementation must not infer acceptance or rejection, guess a target, or perform fuzzy relocation while claiming equivalent v1 behavior.

Terminal-record retention is optional. A conforming interchange may omit a terminal proposal after materializing its outcome. If it retains the terminal proposal, it retains the complete core semantic record: portable identity, original base-state reference, target, change kind and payload, terminal outcome, and every available core provenance field. Complete retention does not require bundling historical accepted-document snapshots; the fingerprint continues to identify the original base precondition. V1 does not define a compact identity-and-outcome tombstone as an equivalent retained proposal, though a future extension may define receipts separately.

### Rationale

Stable portable identity is what lets a consumer select one proposal for acceptance or rejection after adapters normalize run boundaries, remap targets, reorder serialization, or encounter multiple proposals at the same location. Native object references or positional order may serve the same purpose inside one editor session, but they do not survive an interchange boundary.

The accepted-state-plus-proposal-overlay decision makes numeric targets stable only relative to a known accepted state. A deterministic fingerprint turns that dependency into a verifiable precondition and prevents a detached or partially persisted proposal overlay from being silently applied to different text. Restricting the requirement to the portable boundary preserves the earlier decision not to standardize editor runtime or private storage architecture.

Optional-but-preserved provenance reflects the evidence rather than treating one product model as universal. Word, ODF, Reference Web Editor, Google Docs, and Web Annotation expose useful identity, creator, or time variants, while HTML, Input Events, Quill, and the sampled ProseMirror core do not provide one common review-provenance contract. Applications that need visible authorship or audit time can therefore carry it without excluding sources that lack it.

The narrow lifecycle preserves the semantic difference between a review decision and a technical failure. Keeping conflict outside review state allows an adapter or user to repair a bad precondition without fabricating a reviewer judgment. Complete-record-or-none terminal retention likewise gives implementations a clear choice between portable audit information and no portable review history, without presenting a partial tombstone as the original proposal.

### Rejected alternatives and trade-offs

- **Optional identity or identity inferred from target, payload, or order:** is simpler for single-proposal sources but becomes ambiguous after remapping, normalization, reordering, or when two proposals share a target. It cannot reliably support selective resolution.
- **Mandatory global UUIDs or URIs:** simplify cross-document aggregation but impose generation and namespace requirements unsupported by the bounded document-lineage use case. Opaque lineage-scoped identifiers are sufficient for v1.
- **Mutable payload or target under one identifier:** can mirror products that grow or rewrite a live suggestion, but it lets an earlier resolution decision name materially different content and would require synchronization/version semantics outside this interchange scope.
- **An opaque producer revision token as the only base precondition:** may integrate easily with one source but cannot independently verify that portable paragraph identities and exact text match. It remains useful only as optional provenance.
- **Context matching or fuzzy reattachment:** can recover a plausible human location, but repeated text and structural changes make it non-deterministic. It may be an adapter repair aid, not an equivalent canonical mapping.
- **Mandatory author and timestamp:** improves attribution but makes valid proposals impossible for sources that do not expose review provenance and creates unnecessary privacy pressure. Preserve-if-present fields keep authorship available without inventing it.
- **Adding conflicted, stale, or unmappable to the review-state enum:** conflates processing failure with reviewer judgment and complicates later repair. A separate outcome report retains both facts.
- **Automatically rejecting a proposal whose precondition fails:** produces a review decision no user made and can silently lose intended content.
- **Mandatory terminal retention:** provides a uniform audit trail but conflicts with common resolution models that materialize the document and remove revision markers, and increases storage and privacy obligations.
- **Compact terminal receipts as complete proposal records:** preserve identity and outcome cheaply but omit what was reviewed. They may be standardized later as a distinct receipt concept rather than weakening retained-proposal semantics.
- **Mandatory historical accepted-state snapshots for terminal records:** would make old targets fully reconstructable but turns the v1 proposal model into document-version history, which is explicitly distinct and out of scope.

### Supporting and contradictory evidence

The [normative-model inventory](../evidence.md) shows persistent identifiers and creator/time metadata in WordprocessingML and ODF, portable identity and lifecycle metadata in Web Annotation, and the absence of a common proposal identity or review lifecycle in HTML and Input Events. Word resolution demonstrates that accepted changes may be materialized while their revision marks disappear, supporting optional terminal retention.

The [Web-editor practice comparison](../evidence.md) finds distinguishable proposal identities and accept/reject behavior in Reference Web Editor, Google Docs, and Word, but no native proposal state or provenance in Quill and the sampled ProseMirror core. It also documents materially different persistence topologies and notes that actor/time are useful rather than universal primitives.

The [text-subset feasibility evidence](../evidence.md) directly identifies source-absent identity and provenance, Google metadata/content partial persistence, and Reference Web Editor host-managed suggestion persistence as loss boundaries. The [coordinate research](../evidence.md) shows that numeric positions require a known state and deterministic transformation and that fuzzy position recovery cannot establish canonical equivalence. The [minimal conformance experiment](../evaluation/README.md) already depends on stable proposal identity for selective resolution and observes terminal outcomes only when terminal records remain.

Contradictory evidence limits the decision. Several reviewed sources have no proposal identifier, author, timestamp, or terminal record to preserve; adapters must synthesize or omit rather than claim native support. Existing standards use incompatible identifier scopes and do not share a deterministic semantic fingerprint. In the sampled Google Docs boundary, content and suggestion metadata can have different persistence outcomes, and native systems may merge or expand suggestions under source-specific identities. These differences support explicit synthesis and failure reporting but leave the exact cross-format success rate for later conformance fixtures.

### Uncertainty, assumptions, and follow-ups

- [Choose the canonical serialization](15-choose-canonical-serialization.md), informed by [Compare canonical serialization candidates](../evidence.md#serialization-alternatives-considered), must define deterministic semantic encoding, digest algorithm, identifier syntax, and timestamp encoding without turning the fingerprint into a runtime requirement.
- [Define content-change and resolution semantics](12-define-content-change-and-resolution-semantics.md) must specify how resolution produces successor fingerprints and remaps remaining targets while preserving proposal identity.
- [Define loss reporting and conformance outcomes](13-define-loss-reporting-and-conformance-outcomes.md) must classify synthesized or colliding identities, provenance omission or redaction, fingerprint mismatch, unmappable targets, partial persistence, and incomplete terminal records.
- [Build executable conformance fixtures](../evaluation/README.md#core-evaluation) must test identity through persistence and selective resolution, source-absent identity, stale-base rejection, repair without review-state mutation, and both permitted terminal-retention outcomes.
- The decision assumes the portable document lineage is available to detect identifier reuse and collisions. Cross-document global identity and aggregation remain outside v1.
- A retained terminal record identifies its historical base by fingerprint but does not guarantee that the complete historical accepted state remains available. Full document history remains outside v1.
- Proposal editing histories, compact resolution receipts, withdrawal or cancellation states, concurrency-native proposal versions, and organization-specific provenance requirements may be future profiles or extensions; none changes the v1 three-state review lifecycle.
