# Define content-change and resolution semantics

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 09, 10, 11
Decision status: active
Supersedes:
Superseded by:

## Question

What normative payload, grouping, ordering, and accept/reject behavior should v1 define for insertion, deletion, atomic replacement, bounded formatting, and paragraph split/merge, including selective resolution and remapping of proposals that remain pending?

## Resolution

### Decision

V1 resolves revision proposals against the accepted-state-plus-proposal-overlay model established by [Portable document state and targets](09-define-portable-document-state-and-targets.md). Accepted paragraph state includes the paragraph's stable identity, exact text, and normalized effective coverage of the four core inline-formatting properties established by [Bounded inline formatting](11-define-bounded-inline-formatting.md): italic, bold, underline, and strikethrough. Uncovered text has the effective value `false`. Paragraph order, identities, exact text, and core formatting coverage all contribute to the accepted-state fingerprint. This formatting coverage records actual accepted values; it is not a per-document list of permitted formatting kinds.

A content fragment consists of exact text plus normalized effective coverage of the four core properties over that text. Inserted and replacement content carries its formatting explicitly rather than inheriting from the target position or an editor's ambient state. Payload text is not silently Unicode-normalized, and every payload boundary obeys the UTF-16 and Unicode code-point-boundary rules of the target model.

Every operation has one immutable proposal identity and one exact, non-no-op payload:

- **Insertion** targets a text point and carries a non-empty content fragment. Acceptance splices the fragment at the point; rejection leaves accepted state unchanged.
- **Deletion** targets a non-empty text range and carries the exact content fragment covered by that range. The payload must match the base state's text and core formatting. Acceptance removes the range; rejection leaves it intact.
- **Replacement** is one atomic proposal, not independently resolvable insertion and deletion children. It targets a non-empty text range, carries the matching old fragment and a non-empty new fragment, and inserts the new fragment at the removed range's start. Acceptance performs the substitution as one outcome; rejection preserves the old fragment.
- **Formatting** targets a non-empty text range and carries a non-empty map of changed core properties. Each entry has one normalized effective before value matching the entire targeted range and one different after value. Every property in the map resolves atomically under the proposal's one identity.
- **Paragraph split** targets a valid text point, including offset `0` or the paragraph's text length, and reserves a collision-free identity for the new right paragraph. Acceptance keeps the original identity on the left paragraph and moves the suffix, with its formatting coverage, to the new right paragraph. Rejection preserves the original paragraph. Endpoint splits may therefore create an empty left or right paragraph.
- **Paragraph merge** targets an adjacent-paragraph boundary. Acceptance concatenates the right paragraph's exact text and formatting coverage onto the left paragraph, retains the left identity, and retires the right identity. Rejection preserves both paragraphs. Merging with an empty paragraph is valid.

Empty insertions or deletions, a replacement with an empty old or new fragment, unchanged formatting values, and empty formatting ranges are not alternative encodings of another operation; they are invalid no-ops. An empty replacement is represented as insertion or deletion as appropriate.

Same-position behavior is semantic rather than serialization-dependent. A target point or range boundary carries `before` or `after` association wherever accepting another insertion at that point would otherwise make successor attachment ambiguous. A range start defaults to `after` and a range end defaults to `before`, keeping a range attached to the original base content rather than automatically expanding it over an adjacent insertion. At an accepted split point, `before` maps to the end of the left paragraph and `after` maps to the start of the right paragraph.

Co-located insertions have an explicit immutable strict total order local to their base point and association. Their accepted fragments appear in that order. Portable semantics never infer this order from proposal identifiers, object enumeration, serialization order, timestamps, or provenance. An adapter that lacks source ordering must synthesize an order and report that transformation or report the relation as unavailable, as later conformance rules require.

A selective resolution request maps one or more pending proposal identities to `accepted` or `rejected`. It is evaluated as one atomic transaction against one verified accepted-state fingerprint. The selected proposals must be valid and mutually compatible. V1 excludes overlapping, nested, and dependent proposals; operations whose consumed text, formatting coverage, or paragraph boundaries intersect incompatibly cannot appear in the same conforming pending set or resolution transaction. Shared boundaries are permitted when association makes their outcomes unambiguous, and co-located insertions are permitted when their total order is explicit.

Accepted members of a compatible transaction materialize simultaneously from the common base-relative observation. Rejected members do not alter accepted content. A transaction containing no accepted member leaves the accepted-state fingerprint unchanged. Otherwise the complete successor state receives a new fingerprint. Terminal proposal records may be retained or omitted according to [Proposal identity, metadata, and lifecycle](10-define-proposal-identity-metadata-and-lifecycle.md).

Every proposal left pending must preserve its identity and semantic attachment while being deterministically remapped to the successor state and updated to reference the successor fingerprint. Observable remapping follows these rules:

- an insertion shifts later offsets by its inserted UTF-16 length, with same-point association and explicit insertion order deciding attachment;
- a deletion shifts later offsets left by the deleted length, while a target inside removed content is incompatible or unmappable rather than guessed;
- a replacement applies the deletion and insertion transformation atomically, using its new-fragment length and the same boundary rules;
- a formatting acceptance changes effective coverage but does not move text coordinates;
- a split maps suffix targets to the new right identity with offsets relative to the split, while association settles targets exactly at the split point; and
- a merge maps targets from the retired right identity to the retained left identity by adding the left paragraph's pre-merge UTF-16 length.

The same transformations split, shift, concatenate, or preserve accepted formatting coverage along with the affected text. An implementation may realize them eagerly, lazily, with markers, operations, or another algorithm; only the resulting state, projections, identities, and targets are normative.

The implementation preflights the whole transaction. A fingerprint mismatch, invalid or non-matching payload, incompatible proposals, absent same-point order, ambiguous result, or inability to remap any proposal that would remain pending fails the transaction without partial content, lifecycle, fingerprint, or target mutation. The condition is reported separately from review state; it never implies acceptance or rejection.

### Rationale

Exact content fragments make both accepted and rejected projections independently testable and let a retained terminal record remain meaningful without requiring historical accepted-state snapshots. Carrying explicit formatting on inserted and replacement text is necessary because dependent proposals are outside v1: otherwise a content-significant italic insertion, for example, could not be represented without ambient editor behavior or a second proposal.

One proposal per user-reviewable atomic outcome preserves the identity and lifecycle decisions already accepted. It prevents a consumer from accepting half a replacement or only some properties of one formatting proposal. The evidence does not show a universal native replacement primitive, but the assessment decision explicitly chose producer-declared replacement intent; sources that expose separate revisions must either establish and preserve that relation or report loss.

Stable left-paragraph identity for split and merge minimizes identity churn and gives adapters a simple deterministic transformation for paragraph-local targets. Allowing endpoint splits covers ordinary creation of an empty adjacent paragraph without inventing another structural operation.

Base-relative simultaneous resolution, explicit same-point order, and transaction-wide preflight prevent storage order or API call order from changing the accepted result. Requiring every remaining proposal to reach the successor state also preserves the invariant that a pending proposal is interpreted against its declared fingerprint rather than leaving a partly transformed overlay behind.

### Rejected alternatives and trade-offs

- **Text-only accepted state:** would keep the paragraph model smaller but could neither materialize nor fingerprint accepted formatting outcomes. Core effective formatting is therefore part of accepted semantic state.
- **Ambient or inherited formatting for inserted content:** resembles some editor typing behavior but makes the portable outcome depend on target context and source cascade. Inserted content carries explicit effective values instead.
- **Derive deleted content only from the current base:** removes redundant payload data but weakens self-validation and retained terminal records. The exact deletion payload is required and checked against the base.
- **Replacement as two independently resolvable proposals:** matches HTML, OOXML, ODF, and some Reference Web Editor representations more directly, but permits intermediate and terminal outcomes that contradict producer-declared atomic replacement intent.
- **One proposal per formatting property:** allows finer reviewer choices but splits one authored formatting change into outcomes the producer did not declare. A multi-property formatting payload resolves atomically.
- **Keep the right identity or allocate two fresh identities on structural change:** is deterministic but causes more target and provenance churn than retaining the left/original continuity rule.
- **Disallow endpoint splits or empty paragraphs:** narrows fixtures but excludes common paragraph creation and removal behavior without reducing target-model complexity materially.
- **Use proposal ID, timestamp, enumeration, or serialization order for co-located insertions:** avoids an order field but can silently reorder author intent and makes semantics depend on incidental metadata.
- **Sequential best-effort batch resolution:** is easy to expose through imperative APIs but makes results depend on application order and can leave content, proposal state, and fingerprints partially updated.
- **Permit overlapping or dependent proposals when one execution order happens to work:** increases coverage but requires conflict, dependency, and nested-resolution semantics explicitly deferred from v1.
- **Guess or fuzzily relocate an unmappable remaining target:** may appear helpful, but repeated text and structural edits make the result non-deterministic. Repair may be offered outside an equivalent v1 transaction.

### Supporting and contradictory evidence

The [text-subset feasibility evidence](../evidence.md) supports exact accepted/rejected outcomes for paragraph-local insertion and deletion, requires deleted content for rejection, identifies explicit replacement grouping as the first compound semantic, and shows why paragraph boundaries cannot be flattened into character-only edits. Word and ODF provide insertion, deletion, formatting, and paragraph-aware structures; Reference Web Editor and Google Docs provide independent proposal identity and accept/reject behavior.

The same evidence supports normalized effective formatting rather than source runs: Word retains property history, Google uses field masks, Reference Web Editor replays commands, and ODF format changes may omit the actual formatting delta. These differences support explicit effective before/after values and loss reporting rather than a source-shaped portable payload. The [minimal conformance experiment](../evaluation/README.md) independently requires exact projections, stable identity, selective resolution, and no silent loss.

Contradictory evidence limits claims of native uniformity. The checked WordprocessingML and ODF vocabularies do not share an atomic replacement record; HTML and Reference Web Editor examples can represent replacement as adjacent deletion and insertion; HTML edit elements do not change paragraphing; Quill deletions are not reversible without external state; and Google and Reference Web Editor can expose partial or host-managed persistence. No sampled system establishes the selected transaction, same-position ordering, or paragraph-identity rules as a universal native model. Those rules are the vendor-neutral interchange contract adapters map into, not a claim about existing storage architecture.

### Uncertainty, assumptions, and follow-ups

- The lexical form of the co-located insertion-order value, content fragments, property coverage, and operation payloads remains for [Choose the canonical serialization](15-choose-canonical-serialization.md). The semantic requirement is only a stable strict total order at each affected point.
- The exact state-fingerprint encoding and digest algorithm remain with the canonical-serialization decision; they must cover accepted core formatting as well as paragraph identities, order, and text.
- [Define loss reporting and conformance outcomes](13-define-loss-reporting-and-conformance-outcomes.md) must classify non-matching payloads, synthesized or unavailable insertion order, unsupported atomic grouping, conflicting or unmappable targets, failed transaction preconditions, and partial native persistence.
- [Build executable conformance fixtures](../evaluation/README.md#core-evaluation) must test formatted insertion and replacement payloads, atomic multi-property formatting, no-op rejection, endpoint splits, empty-paragraph merges, both same-point associations, explicit co-located ordering, mixed accept/reject transactions, rollback on preflight failure, and every operation-specific remapping rule.
- [Choose initial mapping profiles](17-choose-initial-mapping-profiles.md) must state when a source's paired revisions, formatting commands, paragraph marks, or native ordering can establish equivalent portable semantics and when transformation or loss is reported.
- Overlapping, nested, dependent, move, concurrent-editing, arbitrary-formatting, and richer document-tree interactions remain deferred. A future extension may define compatibility and transformation rules without changing v1 outcomes.
- The decision assumes the four core properties can be represented as effective per-text coverage. Sources unable to recover those values remain valid mapping inputs only with the non-equivalent outcome defined by the later loss decision.
- No prior decision is superseded. This record extends the accepted paragraph state with the formatting coverage already required by the active formatting decision.
