# Define portable document state and targets

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 08, 18
Decision status: active
Supersedes:
Superseded by:

## Question

What canonical paragraph/text state and target-attachment model should v1 use so insertion, deletion, formatting, replacement, and paragraph split/merge proposals remain identifiable and produce deterministic projections without standardizing DOM shape, source run identity, or an editor's internal coordinate system?

## Resolution

### Decision

V1 uses an **accepted-state-plus-proposal-overlay** interchange model. The canonical semantic document state is an ordered sequence of accepted paragraph records. Each paragraph has a stable opaque identity local to the portable document and an exact text value. Revision proposals are separate records attached to that accepted state; proposal payloads and deleted content are not embedded into the accepted text.

Paragraph identities are portable targeting identities, not HTML `id` values, DOM-node identities, global resource identifiers, or requirements on an editor's native model. An adapter may synthesize a paragraph identity when its source has none. Source run, span, text-node, and DOM segmentation are not portable identities.

The minimal target vocabulary is:

- a **text point** identified by paragraph identity and zero-based text offset;
- a **text range** identified by one paragraph identity and half-open offsets `[start, end)`; and
- a **paragraph boundary** identified by the identities of its adjacent paragraphs.

Text offsets count UTF-16 code units in the paragraph's exact stored text. Every offset must be on a valid Unicode code-point boundary; an offset between the halves of a surrogate pair is invalid. The core does not silently normalize Unicode. An adapter that normalizes text must declare the transformation and recompute every affected target before claiming an equivalent result.

Points and range boundaries carry an explicit before/after association when accepting another insertion at the same position would otherwise make their successor attachment ambiguous. Per-operation defaults and ordering rules will be settled with content-change semantics.

Every v1 target is interpreted against a declared accepted document state. While proposals remain pending, they do not mutate that state, so their base-relative targets remain stable. After a proposal is resolved into a successor accepted state, every remaining proposal must have a deterministic semantically equivalent target in that successor state. The standard constrains that observable result, not the implementation strategy: an implementation may transform targets eagerly or lazily, use inline markers or a revision tree, retain transformation records, or use another algorithm. When no unambiguous equivalent exists, the implementation reports the target as conflicted or unmappable rather than guessing or performing fuzzy reattachment.

V1 proposals target accepted-state content only. One pending proposal cannot target content introduced by another pending proposal; that is a dependent-proposal feature already deferred from v1. Atomic replacement remains one explicitly related proposal, not a dependency inferred between independently resolvable proposals.

The interchange model does not constrain an editor's runtime representation or private persistence. An editor may use inline revision markup, markers, operations, an external metadata store, or the canonical shape internally. An implementation claiming portable interchange conformance must map its native state to and from the canonical model and report non-equivalent mappings; private storage need not itself use the canonical serialization.

### Rationale

The chosen separation makes accepted content, review identity, change payload, and attachment independently observable without prescribing a DOM, run tree, collaboration engine, or storage topology. It supports selective resolution and exact accepted/rejected projections while permitting existing inline or marker-based implementations to keep the representations that make their editors efficient.

Paragraph-local identities prevent an insertion or deletion elsewhere in the document from renumbering every target. Typed point, range, and boundary targets preserve the assessment decision that paragraph structure is semantic: a split or merge is not disguised as deletion or insertion of a newline in one flattened string. Half-open ranges compose cleanly and distinguish empty points from covered content.

The [text-subset evidence](../evidence.md) shows that source runs and spans are unstable representation details, paragraph boundaries affect resolution outcomes, and explicit review systems attach changes through materially different tree marks, IDs, ranges, or markers. The [Web-editor practice evidence](../evidence.md) likewise shows inline package markup, host-managed markers and metadata, server-managed suggestion IDs, and operation-based positions; the evidence does not support selecting any one native storage topology as a portable requirement.

The project requirements prioritize a Web-editor convention that is common and easy to implement. The bounded [Web text-coordinate research](../evidence.md) found UTF-16 code-unit positions across ECMAScript and DOM character operations, CodeMirror, and Google Docs, with Reference Web Editor reinforcing the need for structured offsets, Unicode-boundary validation, and position transformation after mutations. UTF-16 therefore minimizes adapter friction for the intended audience when paired with a mandatory code-point-boundary check.

The project requirements also keep the standard an interchange contract rather than a general Web editor architecture. Separating the canonical overlay from runtime and private storage preserves that boundary: a vendor may use an inline revision tree for performance and translate only at import/export.

### Rejected alternatives and trade-offs

- **Canonical inline revision tree:** can make markers move naturally in a native tree and resembles OOXML, ODF, HTML edit markup, or Reference Web Editor data. The sampled trees differ materially, however, and selecting one would standardize source segmentation and storage shape rather than portable meaning.
- **Before/after document snapshots:** makes whole-document acceptance or rejection simple but obscures independent proposal identity and requires diff inference or combinatorial snapshots for selective resolution.
- **One flattened document string and global range:** reduces the number of target types but hides paragraph split/merge semantics in separator characters and causes unrelated paragraph edits to shift later targets.
- **Operation-specific unrelated target schemas:** can optimize each operation but multiplies attachment rules and weakens common validation and remapping.
- **Paragraph ordinals instead of identities:** are compact but make insertions, deletions, splits, or merges before a target renumber unrelated attachments.
- **Unicode scalar, grapheme-cluster, or byte offsets:** can be more encoding-neutral or closer to cursor behavior, but would require conversion at several representative Web adapter boundaries. Grapheme segmentation is versioned and may be tailored; byte offsets depend on an encoding. UTF-16's surrogate-boundary hazard is handled explicitly instead.
- **Implicit Unicode normalization:** can simplify some comparisons but changes exact text and offset counts. Silent normalization could attach a proposal between a base character and combining mark or make a stored target invalid.
- **Permanent raw offsets without transformation:** become stale after resolution changes accepted text. The standard instead requires a logically remapped successor attachment without mandating eager recomputation.
- **Fuzzy quote or context reattachment:** may recover a human-plausible location after unrelated edits but can select the wrong repeated text and makes projections non-deterministic. Such recovery may be an adapter diagnostic, not canonical equivalence.
- **Mandating canonical runtime or private storage:** could simplify inspection but would exclude efficient native marker, tree, and operation models without improving the interchange observation.
- **Targets into other pending proposals:** enable nested or dependent review but contradict the accepted v1 deferral and require ordering, dependency, and conflict semantics not supported by the current subset.

### Supporting and contradictory evidence

Supporting evidence includes paragraph-aware revision outcomes in Word and ODF; distinct accepted, inline, accepted-preview, and rejected-preview observations in Google Docs; marker/range attachment in Reference Web Editor; transformation of positions in DOM, CodeMirror, Reference Web Editor, and ProseMirror-style systems; and the direct UTF-16 conventions in the Web platform, CodeMirror, and Google Docs.

Contradictory evidence qualifies the choice. Several reviewed systems place revision marks or suggestion IDs directly on content, showing that an inline or attached native model can be efficient. UTF-16 indices do not correspond one-to-one with supplementary Unicode scalars or grapheme clusters and can express an invalid boundary inside a surrogate pair. Numeric text positions are brittle without a known source state, as Web Annotation notes. These facts support adapter freedom, mandatory boundary validation, base-state preconditions, and deterministic remapping rather than a claim that raw overlay offsets solve anchoring by themselves.

### Uncertainty, assumptions, and follow-ups

- [Define proposal identity, metadata, and lifecycle](10-define-proposal-identity-metadata-and-lifecycle.md) must define the accepted base-state or conflict precondition against which targets are valid, plus the lifecycle outcome for a conflicted or unmappable target.
- [Define bounded inline formatting](11-define-bounded-inline-formatting.md) must define which effective values occupy text-range coverage without turning source runs into identities.
- [Define content-change and resolution semantics](12-define-content-change-and-resolution-semantics.md) must define per-operation boundary association, ordering, target transformation, and stable paragraph-identity behavior for split and merge.
- [Define loss reporting and conformance outcomes](13-define-loss-reporting-and-conformance-outcomes.md) must classify synthesized paragraph identity, declared Unicode normalization, stale or unmappable targets, and non-equivalent native mappings.
- The decision assumes well-formed Unicode interchange text. Whether the selected serialization enforces that structurally remains open until canonical serialization is chosen.
- Multiple proposals at one point, proposals adjacent to a resolved range, and structural remapping remain permitted only where later rules produce an unambiguous result; overlapping and dependent proposals stay outside v1.
- Concurrent external edits and CRDT/OT-relative positions remain outside v1. A future concurrency profile could add different native anchoring while still mapping to the portable observation.
