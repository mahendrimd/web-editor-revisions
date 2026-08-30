# Web Editor Revisions

Project status: Maintainer-reviewed

Publication version: `1.0.1`

Release date: 2026-08-30

Release tag: `web-editor-revisions-v1.0.1`

Predecessor publication: version `1`, tag `web-editor-revisions-v1`

Semantic model version: `1`

Canonical serialization profile: `json-jcs-1`

## 1. Purpose

Web Editor Revisions defines a vendor-neutral interchange model for pending revisions in text-focused Web editors. It enables an editor, import/export adapter, or integration to preserve independently reviewable changes, resolve them predictably, and report when a mapping cannot preserve their meaning.

The model addresses a gap between editor-specific suggestion systems and document-format-specific tracked-change models. It standardizes portable data and observable outcomes. It does not standardize an editor's user interface, runtime data structures, collaboration algorithm, or private storage.

The intended adopters are:

- Web-editor implementers that import, export, or persist pending revisions;
- document import/export and integration implementers;
- conformance-tool authors; and
- systems that generate reviewable proposals, including automated editing systems.

The intended user benefit is migration between implementations without silent loss of the supported review state.

## 2. Conventions and normative references

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14) when, and only when, they appear in all capitals.

This version normatively uses:

- [RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html);
- [RFC 7493, The I-JSON Message Format](https://www.rfc-editor.org/rfc/rfc7493.html);
- [RFC 8785, JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html);
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12); and
- SHA-256 as specified by [FIPS PUB 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

Requirements in this document and in the [normative JSON Schema](schema/web-editor-revisions-v1.schema.json) apply together. The schema defines the structural contract. This document defines semantic constraints, resolution behavior, canonicalization, mapping outcomes, and conformance requirements that JSON Schema cannot fully express. If an apparent conflict is found, an implementation MUST NOT guess; it MUST report the specification defect to the maintainers and MUST NOT claim conformance for the affected case until the conflict is resolved.

Examples and rationale are informative unless explicitly identified as normative.

## 3. Scope

### 3.1 Included in version 1

Version 1 defines:

- an accepted document state consisting of ordered paragraphs, exact text, and effective inline-formatting coverage;
- revision proposals stored separately from accepted content;
- paragraph-local UTF-16 targets and paragraph-boundary targets;
- insertion, deletion, atomic replacement, formatting, paragraph split, and paragraph merge proposals;
- stable proposal and paragraph identity;
- proposal acceptance and rejection, including selective atomic resolution;
- deterministic target remapping after resolution;
- one canonical JSON/JCS serialization and accepted-state fingerprint;
- URI-keyed extensions;
- structured mapping outcomes, loss reporting, and bounded equivalence claims; and
- role-based conformance requirements.

The mandatory inline-formatting properties are `italic`, `bold`, `underline`, and `strikethrough`.

### 3.2 Excluded from version 1

Version 1 does not define:

- moves;
- overlapping, nested, or dependent proposals;
- lists, tables, embeds, or a general document tree;
- formatting beyond the four core properties;
- comments or discussion threads;
- proposal withdrawal or cancellation;
- concurrent-editing, OT, or CRDT semantics;
- undo/redo or document-version history;
- reviewer permissions, workflow policy, or access control;
- editor UI, DOM shape, source-run identity, or source markup;
- transport, database layout, or private persistence architecture; or
- a browser API.

An implementation MAY support excluded features outside this model. It MUST NOT describe them as core version 1 semantics unless a versioned extension or mapping profile defines their relationship to the core.

### 3.3 Informative review-method interpretation

This subsection is informative. It explains the user-facing review integrity that the normative model can support; it does not add a conformance requirement or prescribe a review interface.

For a proposal inside version 1's supported subset, the model gives a document review method enough portable information to help a reviewer:

- distinguish accepted document content from pending proposed changes in document context;
- identify the complete target, payload, and atomic decision unit affected by accepting or rejecting the proposal;
- inspect or derive both the acceptance and rejection projections instead of treating hidden markup as resolved content;
- keep proposal identity and semantic attachment stable as other proposals resolve, or surface an incompatibility or unavailable target instead of guessing; and
- understand when an operation was refused, materialized, or reported as lossy rather than preserved as an equivalent proposal.

These outcomes concern the meaning and integrity of a supported decision, not its presentation. An implementation can choose its inline rendering, previews, navigation, filters, gestures, accessibility presentation, and discussion workflow. Creator and time information is useful when present and is preserved under Section 8.4, but version 1 does not make attribution a mandatory review-surface field.

Document proposal resolution and code review also operate on different semantic objects. Document resolution decides whether a pending in-document content mutation becomes accepted content and defines the corresponding accepted or rejected projection. Code review ordinarily evaluates a branch, commit, or patch for integration and can include review-level approval, requested changes, comments, continuous-integration results, mergeability, repository policy, and later commits. Contextual comparison and re-review are useful analogies, but a code-review approval is not acceptance of each document proposal, and a resolved comment is not a content projection.

## 4. Terminology

**Accepted document state** is the currently authoritative document content against which pending revision proposals are interpreted.

**Acceptance projection** is the document state produced or previewed by accepting a specified proposal or compatible set of proposals.

**Rejection projection** is the document state produced or previewed by rejecting a specified proposal or compatible set of proposals.

**Revision proposal**, or **proposal** in context, is a lifecycle record representing a document change that is independently reviewable while pending. A retained proposal can also record an accepted or rejected outcome.

**Change payload** is the implementation-independent document mutation proposed by a proposal. It excludes proposal identity, review state, provenance, target attachment, and comments.

**Proposal resolution** is a review decision that accepts or rejects a proposal and determines the corresponding document outcome.

**Edit operation** is a command or transformation applied by an editing system. An edit operation is not a revision proposal unless it has the independently reviewable lifecycle required here.

**Revision history** is a chronological record of prior document versions or committed changes. **Undo/redo history** records reversible editor operations. Neither is a set of pending proposals merely because it contains changes.

**Annotation** relates a body or resource to a document target without, by that relationship alone, defining a mutation and resolution behavior. A **comment** is human-readable discussion or explanation and is not a change payload.

Vendor terms such as *suggestion*, *tracked change*, *revision*, and *discard* are mapping aliases only when their behavior matches the applicable definition above.

## 5. Interchange document

An interchange document MUST contain:

- `modelVersion` with the value `"1"`;
- `serializationProfile` with the value `"json-jcs-1"`;
- one `acceptedState`; and
- a `proposals` array.

It MAY contain `mappingReports`, `extensions`, and a tooling-oriented `$schema` URI. `$schema` does not select the model or serialization profile.

An implementation MUST treat an unknown `modelVersion` or `serializationProfile` as unsupported. It MUST NOT guess compatibility from field similarity.

The proposal array MUST be sorted by proposal `id` using lexicographic UTF-16 code-unit order before canonical interchange. This sorting has no proposal-resolution meaning. In particular, proposal order, member order, identifiers, timestamps, and provenance MUST NOT determine the order of co-located insertions.

## 6. Accepted document state

### 6.1 Paragraphs

The accepted state contains a non-empty ordered `paragraphs` array. Each paragraph contains:

- an opaque, non-empty `id` unique in the portable document lineage;
- an exact `text` string; and
- normalized `formatting` coverage.

A paragraph identity is a portable targeting identity. It is not an HTML `id`, DOM node identity, global resource identifier, source-run identity, or requirement on an editor's native model. An adapter MAY synthesize it under the reporting requirements in Section 14.

Paragraph order, paragraph identities, exact text, and core formatting coverage are semantic and contribute to the accepted-state fingerprint.

### 6.2 Text and offsets

Text MUST satisfy the I-JSON string constraints and MUST NOT contain isolated UTF-16 surrogates. Text MUST be preserved exactly and MUST NOT be silently Unicode-normalized.

Every offset in the model counts UTF-16 code units. An offset MUST be between zero and the UTF-16 length of the applicable string, inclusive, and MUST fall on a Unicode code-point boundary. An offset between the two code units of a surrogate pair is invalid.

An adapter that normalizes text MUST declare the normalization, recompute all affected targets, and classify the result under Section 14. It MUST NOT claim equivalence if the normalization changes any version 1 semantic observation or projection.

### 6.3 Formatting coverage

Each formatting run has a half-open interval `[start, end)` and a complete `values` object containing Boolean values for `italic`, `bold`, `underline`, and `strikethrough`.

For non-empty text, formatting runs MUST:

- form a complete partition from offset zero through the text length;
- be ordered, contiguous, and non-empty;
- begin and end on valid code-point boundaries; and
- not contain adjacent runs with identical `values`.

Empty text MUST have an empty formatting array. Uncovered text is not a permitted alternate encoding; effective false values MUST be represented in the complete coverage.

The model preserves the effective visible value, not whether that value came from direct formatting, inheritance, a named style, a theme, a command, or source markup. A mapping profile MAY preserve source derivation as optional metadata. Such metadata does not replace the required effective values.

## 7. Targets

Version 1 has three target types.

A **point target** identifies `paragraphId`, `offset`, and `association`. It is used by insertions and paragraph splits.

A **range target** identifies one `paragraphId` and half-open `start` and `end` endpoints. Each endpoint contains an offset and association. A range MUST satisfy `start.offset < end.offset` for deletion, replacement, and formatting proposals.

A **paragraph-boundary target** identifies adjacent `leftParagraphId` and `rightParagraphId` values in that order. It is used by paragraph merge.

An association is either `before` or `after`. It determines successor attachment when another insertion is accepted at the same offset. Range starts SHOULD use `after`, and range ends SHOULD use `before`; these are the canonical defaults, but the serialized endpoints always carry their association explicitly.

Every pending proposal target is interpreted against the accepted state named by its `baseFingerprint`. Pending proposals target accepted-state content only. A proposal MUST NOT target content introduced by another pending proposal.

Targets MUST be validated against paragraph existence, adjacency, text length, Unicode boundaries, payload preconditions, and compatibility with the pending set. Fuzzy or context-based reattachment MAY be offered as an application repair operation, but its result is not an equivalent version 1 mapping unless it independently establishes the exact required attachment.

## 8. Proposal identity, provenance, and lifecycle

### 8.1 Identity

Every proposal has a non-empty opaque `id` that:

- is unique within the portable document lineage;
- remains stable through adapter boundaries, persistence, target remapping, and any retained terminal record; and
- is never reused within that lineage.

A proposal's semantic identity is immutable. Its base reference, target, kind, and payload MUST NOT materially change while retaining the same identifier. A materially different proposed edit receives a new identifier. Optional nonsemantic metadata MAY be enriched without changing identity.

An adapter SHOULD preserve a usable non-colliding source identifier. If it cannot, it MAY synthesize an identifier that satisfies the normal invariants and MUST report that synthesis.

### 8.2 Base reference

Each proposal has a `baseFingerprint`. A pending proposal's value MUST equal the fingerprint of the accepted state against which its target and payload are interpreted.

After a successful resolution changes the accepted state, every proposal that remains pending MUST be deterministically remapped and updated to the successor fingerprint without changing proposal identity.

### 8.3 Lifecycle

The closed review-state vocabulary is `pending`, `accepted`, and `rejected`. Resolution is one-way from `pending` to one terminal state.

Stale bases, conflicts, unavailable targets, unsupported input, and persistence failures are processing or mapping outcomes. They are not review states. Such a condition MUST leave an unresolved proposal pending and MUST NOT fabricate acceptance or rejection.

Terminal proposal retention is optional. After resolution an implementation MAY:

- omit the terminal proposal after materializing its outcome; or
- retain the complete core record.

A retained terminal record MUST preserve the proposal identity, original base fingerprint, original target, kind and payload, terminal state, and every available core provenance field. It does not require the historical accepted-state snapshot. An identity-and-outcome tombstone is not a complete terminal proposal in version 1.

### 8.4 Provenance

The optional core provenance fields are:

- `creator` and `createdAt`;
- `sourceSystem` and `sourceProposalId`; and
- for a retained terminal record, `resolver` and `resolvedAt`.

These fields are preserve-if-present. An adapter MUST NOT invent source provenance silently. Omission, redaction, normalization, or synthesis that affects a mapping claim is reportable. Date-time strings MUST satisfy the JSON Schema `date-time` format and SHOULD use UTC when a source offset need not be preserved.

## 9. Content fragments and proposal kinds

A content fragment consists of exact non-empty `text` and normalized formatting coverage under Section 6. Payload text obeys the same string, UTF-16, and boundary rules as paragraph text. Inserted and replacement content carries explicit effective formatting and does not inherit ambient formatting from its target.

Every proposal MUST have exactly one of the following tagged kinds and MUST satisfy the corresponding requirements.

### 9.1 Insertion

An `insert` proposal targets a point, carries a non-empty `content` fragment, and carries a non-negative `samePointOrder` safe integer.

Acceptance splices the content at the point. Rejection leaves accepted state unchanged.

All insertions with the same base point and association MUST have distinct `samePointOrder` values. Their accepted fragments appear in ascending order. An adapter MUST NOT derive this order from proposal identity, array order, timestamps, or provenance.

### 9.2 Deletion

A `delete` proposal targets a non-empty range and carries the exact `content` fragment covered by that range in the base state, including formatting. The payload MUST match before resolution.

Acceptance removes the range. Rejection leaves it intact.

### 9.3 Replacement

A `replace` proposal targets a non-empty range, carries matching non-empty `oldContent`, and carries non-empty `newContent`.

Acceptance atomically removes the old range and inserts the new content at its start. Rejection preserves the old content. Replacement is one proposal and MUST NOT be independently resolved as insertion and deletion children.

An adapter MUST NOT infer replacement merely because a deletion and insertion are adjacent. If a source cannot establish atomic replacement intent, it must preserve separate proposals where valid or report loss of the relation.

### 9.4 Formatting

A `format` proposal targets a non-empty range and carries a non-empty `changes` map. Each named core property contains a Boolean `before` value and a different Boolean `after` value. The `before` value MUST match the entire targeted range in the base state.

All properties in one formatting proposal resolve atomically. Acceptance applies all `after` values over the range. Rejection preserves all `before` values.

### 9.5 Paragraph split

A `paragraph-split` proposal targets a valid point and reserves a collision-free `newRightParagraphId`.

Acceptance retains the original paragraph identity on the left, creates the new identity on the right, and moves the suffix text and formatting coverage to the right. A split at offset zero or at the paragraph length is valid and creates an empty left or right paragraph respectively. Rejection preserves the original paragraph.

### 9.6 Paragraph merge

A `paragraph-merge` proposal targets an adjacent paragraph boundary.

Acceptance appends the right paragraph's exact text and formatting coverage to the left paragraph, retains the left identity, and retires the right identity. Merging an empty paragraph is valid. Rejection preserves both paragraphs.

### 9.7 Invalid no-ops

Empty insertion or deletion payloads, replacement with empty old or new content, empty formatting ranges, empty formatting maps, and unchanged formatting values are invalid. A pure insertion or deletion MUST use its corresponding kind rather than an empty-sided replacement.

## 10. Selective resolution

A resolution request maps one or more pending proposal identifiers to `accepted` or `rejected`. It is one atomic transaction against one verified accepted-state fingerprint.

Before mutation, the resolver MUST validate:

- the current accepted-state fingerprint;
- proposal identity and pending state;
- all targets and payload matches;
- same-point ordering;
- proposal-set compatibility;
- the requested actions; and
- deterministic remapping of every unselected proposal that would remain pending.

Version 1 pending sets and resolution transactions MUST NOT contain overlapping, nested, or dependent proposals. Operations whose consumed text, formatting coverage, or paragraph boundaries intersect incompatibly are invalid together. Shared boundaries are allowed when associations make their outcomes unambiguous. Co-located insertions are allowed when their total order is explicit.

Accepted members of a compatible transaction materialize simultaneously from the common base-relative observation. Rejected members do not mutate accepted content. A transaction with no accepted member leaves the accepted-state fingerprint unchanged. Otherwise, the complete successor accepted state receives a new fingerprint.

If any preflight check fails, the resolver MUST leave content, proposal lifecycle, fingerprint, and targets unchanged. It MUST report the condition separately from review state. Partial commit is nonconforming.

## 11. Successor target remapping

Every proposal left pending after successful resolution MUST preserve its identifier and semantic attachment while being remapped to the successor state.

The observable remapping rules are:

- accepted insertion shifts later offsets by the inserted UTF-16 length; same-point association and explicit insertion order determine attachment at the point;
- accepted deletion shifts later offsets left by the deleted length; a target inside removed content is incompatible or unmappable rather than guessed;
- accepted replacement applies deletion and insertion transformation atomically using the new fragment length;
- accepted formatting changes coverage without moving text coordinates;
- accepted split maps suffix targets to the new right identity with offsets relative to the split; at the split point, `before` maps to the end of the left paragraph and `after` to the start of the right paragraph; and
- accepted merge maps a target from the retired right identity to the retained left identity by adding the left paragraph's pre-merge UTF-16 length.

Text-associated formatting coverage MUST be split, shifted, concatenated, or preserved with the affected text. Implementations MAY use markers, operations, eager transformation, lazy transformation, or another algorithm, provided the resulting accepted state and pending targets are identical to these requirements.

## 12. Canonical JSON serialization

### 12.1 Narrow JSON profile

Canonical interchange is a JSON value conforming to the normative schema and all semantic requirements in this document.

In addition:

- object member names MUST be unique;
- strings MUST satisfy I-JSON and MUST be preserved without Unicode normalization;
- numbers MUST be non-negative integers no greater than `9007199254740991` where the schema permits numbers;
- floating-point values, non-finite values, and implicit string/number coercion are forbidden;
- `null` is forbidden except where the schema explicitly assigns it meaning;
- JSON object member order has no meaning; and
- arrays have meaning only where this document defines sequence, including paragraph order and formatting-run order.

Identifiers, timestamps, and digests are strings.

### 12.2 Canonical bytes

A canonical exporter MUST structurally and semantically validate the interchange document and then emit exactly the UTF-8 bytes produced by RFC 8785 JCS.

An importer MAY accept noncanonical JSON as a convenience. Before treating it as canonical interchange or re-emitting it as canonical, the importer MUST reject duplicate member names, validate it, apply the required proposal sort, and canonicalize it.

Pretty printing, source member order, parser selection, validator selection, transport, and internal object layout are not normative.

### 12.3 Accepted-state fingerprint

The accepted-state fingerprint input is exactly this JSON value, where `paragraphs` is the validated `acceptedState.paragraphs` value unchanged:

```json
{
  "domain": "web-editor-revisions.accepted-state",
  "modelVersion": "1",
  "serializationProfile": "json-jcs-1",
  "paragraphs": []
}
```

The producer MUST:

1. validate the accepted state and normalized formatting coverage;
2. replace the example empty array above with the actual `paragraphs` value;
3. produce the RFC 8785 JCS UTF-8 bytes of that projection;
4. compute SHA-256 over those bytes; and
5. encode the 32-byte digest as unpadded base64url.

The result is a 43-character `acceptedState.fingerprint` string. The projection excludes the fingerprint itself, proposals, mapping reports, provenance, extensions, and incidental metadata.

## 13. Extensions

Extensions are stored at explicit `extensions` objects keyed by stable absolute URI identifiers. Each entry contains:

- `required`, a Boolean; and
- `value`, the extension-defined JSON value.

An extension MUST NOT override or conceal core meaning.

An implementation that does not understand an extension with `required: true` MUST classify the input as unsupported and MUST NOT mutate output. An unknown optional extension MUST be preserved opaquely across an interchange path or reported as declared loss. Preserving an extension means preserving its JSON value semantically; a canonical re-encoding MAY change only nonsemantic source representation such as object member order or whitespace.

Version 1 permits condition and action extensions in mapping issues through `extensionId`. An extension issue still supplies all core issue dimensions and cannot introduce a sixth overall outcome or a fifth impact class.

## 14. Mapping outcomes and loss reporting

### 14.1 Mapping operation and conformance

A mapping operation is observed at a declared import, export, save/reload, persistence, or other adapter boundary. Its outcome is distinct from whether the adapter conforms. A conforming adapter can truthfully refuse unsupported input or produce caller-authorized lossy output. Reporting loss does not make the result equivalent.

Every operation produces one final machine-readable `mappingReport` bound to:

- the exact input and any output through `inputRef` and `outputRef`;
- the adapter identity and version;
- the mapping profile identity and version;
- the direction;
- the measured boundary; and
- the observed mutation, outcome, and issues.

The references MUST be semantic fingerprints, artifact identifiers, or equivalently strong references sufficient to identify the exact observed input and output. A preflight prediction or human-readable warning does not replace the final report.

`outputRef` is `null` exactly when the operation produced no output artifact or state at the declared boundary; this is the only core use of JSON `null`. `outputMutation` records the observed boundary state:

- `none`: the boundary is unchanged;
- `valid-complete`: valid output was committed without semantic loss;
- `valid-lossy`: valid usable but non-equivalent output was committed; or
- `residual-invalid`: partial, unverifiable, or invalid mutation remains.

`authorizedActions` lists the lossy actions the caller authorized before mutation. Its presence does not establish that those actions occurred or that their results are equivalent.

### 14.2 Overall outcomes

Exactly one derived overall outcome applies:

- `equivalent`: valid output; all applicable version 1 semantics and preserve-if-present information survived; no reportable adaptation or loss;
- `equivalent-with-declared-adaptation`: valid output; every issue is a permitted, declared synthesis or normalization with `impact: none`; mandatory semantics and projections remain equivalent across the measured boundary;
- `lossy`: valid usable output was committed under explicit caller authorization, but information or review semantics changed;
- `unsupported`: no output mutation occurred because declared capability or authorized policy was insufficient; or
- `failed`: no valid result completed because input was invalid, a safety precondition or execution failed, persistence failed, or residual invalid mutation occurred.

Outcome aggregation is deterministic:

- any transaction-integrity failure yields `failed`;
- a valid non-equivalent committed result yields `lossy`;
- a clean refusal for insufficient capability or policy yields `unsupported`;
- `equivalent-with-declared-adaptation` requires at least one declared issue and every issue to have `impact: none`; and
- `equivalent` requires no adaptation or loss issue.

An adapter MUST NOT self-select a more favorable label than the observations derive.

### 14.3 Structured issues

Each issue records:

- `stage`;
- applicable `proposalIds`;
- the narrowest affected semantic `fields`;
- `condition`;
- adapter `action`;
- semantic `impact`;
- `recoverability`;
- reproducible `expected` and `observed` dispositions;
- an `extensionId` when required; and
- an optional human-readable `explanation`.

Core condition values mean:

- `source-absent`: the source model genuinely has no corresponding value or relation;
- `unsupported`: the adapter recognizes the semantic but cannot process it within its declared capability;
- `unavailable`: a value should or may exist, but the adapter cannot retrieve, recover, or verify it;
- `invalid-input`: input violates an applicable source, profile, or version 1 invariant;
- `precondition-failed`: otherwise valid input cannot safely be applied to the verified current state;
- `persistence-failure`: the intended result did not survive the declared persistence boundary; and
- `other`: a condition defined by the accompanying namespaced `extensionId`.

Core action values mean:

- `synthesized`: the adapter created a portable value without claiming it came from the source;
- `normalized`: the adapter changed only a representation detail that the core or profile permits without semantic impact;
- `approximated`: the adapter substituted non-equivalent data or behavior;
- `omitted`: the adapter did not carry affected information or semantics into the result;
- `materialized`: the adapter converted pending review state into an accepted or rejected projection;
- `refused`: the adapter made no output mutation;
- `rolled-back`: the adapter attempted mutation and fully restored the declared boundary;
- `partially-committed`: an incomplete operation left residual mutation; and
- `other`: an action defined by the accompanying namespaced `extensionId`.

Core impact values are:

- `none` for no change to a version 1 observation, projection, or preserve-if-present value;
- `optional-information-loss` for loss of a source value that version 1 makes optional to originate but preserve-if-present;
- `review-semantics-loss` for change or loss of a mandatory field, relation, lifecycle fact, target, payload, identity guarantee, or possible projection; and
- `transaction-integrity-failure` for partial, unverifiable, or non-atomic mutation across the declared boundary.

Core recoverability values mean:

- `not-applicable`: no corrective action is required;
- `retryable`: the same authoritative request can be safely attempted after the stated transient or environmental condition is corrected;
- `requires-intervention`: recovery requires additional data, repair, policy authorization, user judgment, or an adapter/profile change;
- `irrecoverable`: the exact affected semantics cannot be reconstructed within the declared boundary from retained information; and
- `unknown`: the implementation cannot establish whether or how recovery is possible.

Recoverability does not upgrade the current operation's outcome. A later successful attempt has a separate report.

Core affected-field identifiers are:

- `acceptedState.paragraphOrder`, `acceptedState.paragraphIdentity`, `acceptedState.text`, `acceptedState.formatting`, and `acceptedState.fingerprint`;
- `proposal.identity`, `proposal.baseReference`, `proposal.target`, `proposal.kind`, `proposal.payload`, `proposal.samePointOrder`, `proposal.relations`, `proposal.reviewState`, `proposal.provenance`, and `proposal.terminalCompleteness`;
- `resolution.atomicity`, `resolution.acceptanceProjection`, `resolution.rejectionProjection`, and `resolution.pendingTargetRemapping`; and
- `mapping.persistence` and `mapping.transactionIntegrity`.

A future profile or extension MAY define additional stable URI-named affected fields. It MUST use the closest core impact class and MUST NOT conceal impact behind an unknown identifier.

### 14.4 Authorization and equivalence claims

Lossy actions—`approximated`, `omitted`, and `materialized`—require matching caller authorization before output mutation. Authorization MAY be supplied by an API option, mapping profile, or configured policy. It need not be interactive.

If newly discovered loss is not authorized, the adapter MUST refuse or fully roll back. A `partially-committed` result always has transaction-integrity impact and is nonconforming.

No-impact synthesis and normalization require declaration but do not require loss authorization. Stable synthesis of a portable identity for a source that has none can be an equivalent declared adaptation. Splitting one atomic replacement into independently resolvable proposals is review-semantics loss even when declared.

An equivalence claim is limited to the named operation, direction, profile and version, input and output, and measured boundary. It MUST NOT be generalized into an unqualified claim that an adapter, product, or format supports the entire standard.

## 15. Conformance

Conformance is role- and boundary-specific. An implementation MAY claim one or more roles and is evaluated only for the behaviors it claims.

### 15.1 Core interchange document

A core interchange document conforms when it:

- validates against the normative schema;
- satisfies every applicable semantic invariant in this document;
- has the required version values and proposal ordering;
- has the correct accepted-state fingerprint; and
- contains no unsupported required extension for the consumer making the claim.

### 15.2 Producer

A conforming producer MUST emit conforming interchange documents and canonical JCS bytes. It MUST NOT silently normalize text, invent provenance, infer atomic replacement, or claim native identity for a synthesized identity.

### 15.3 Consumer

A conforming consumer MUST validate structure and semantics before relying on a document. It MUST reject unknown versions, unsupported required extensions, invalid fingerprints, invalid targets or payloads, and nonconforming pending sets. A consumer MAY accept noncanonical source JSON but MUST canonicalize it before canonical re-emission.

### 15.4 Resolver

A conforming resolver MUST implement Sections 9 through 11 for every proposal kind it claims, including exact projections, atomic transaction preflight, deterministic successor fingerprints, and pending-target remapping. It MUST either retain complete terminal records or omit them.

### 15.5 Mapping adapter

A conforming adapter MUST declare the profile, profile version, direction, capability, and measured boundary of its claim. It MUST produce bound reports, derive outcomes correctly, require authorization for lossy mutation, preserve optional extensions or report their loss, and prevent partial commit.

A profile-scoped claim MUST distinguish safety-only behavior from proposal-mapping support and MUST list every core proposal kind it claims. The applicable profile defines universal, capability-activated, and persistence-activated evidence requirements independently for each direction. A safety-only claim with no proposal kinds MUST NOT be presented as semantic mapping support.

An adapter is not required to implement every proposal kind, mapping profile, or direction. A truthful, mutation-free `unsupported` outcome can conform. Silent loss, misleading classification, missing reporting, unauthorized lossy mutation, or residual partial commit cannot conform.

### 15.6 Evaluation

Conformance evaluation SHOULD include:

- strict parsing with duplicate-member detection;
- schema and semantic validation;
- cross-encoder JCS byte comparison;
- accepted-state fingerprint comparison;
- acceptance and rejection projections for every claimed proposal kind;
- selective mixed resolution and rollback cases;
- same-point ordering and every remapping rule;
- persistence across the exact claimed boundary;
- extension preservation and required-extension refusal; and
- all claimed mapping outcome, authorization, and report behaviors.

The publication's [executable fixture suite](evaluation/README.md#core-evaluation) is the initial test oracle for model version 1. Passing it supports only the roles and cases exercised. Native-format and editor-profile claims require their separate profile fixtures and the direction-specific evidence procedure in the evaluation package.

## 16. Mapping profiles

Named source systems are mapped through independently versioned profiles. A profile defines its pinned upstream specification or product-model snapshot, supported subset, direction, preconditions, source-to-core and core-to-source mappings, permitted no-impact adaptations, loss and refusal cases, report bindings, and direction-specific conformance tests.

A profile MUST NOT redefine core identity, targets, proposal kinds, projections, lifecycle, loss outcomes, canonical serialization, or other core semantics. An upstream change updates or supersedes the affected profile; it does not silently change this core or an earlier claim.

### 16.1 Informative adapter-planning method

This subsection is informative. It is a planning method for applying the outcome requirements in the core and a selected profile. It is not a required implementation architecture, and it does not prefer a native API over another implementation that produces the required observations.

An adapter plan can proceed in this order:

1. Identify the exact profile, direction, pinned upstream version, source and output boundaries, persistence boundary, and claimed proposal kinds.
2. Inventory the host's authoritative existing mechanisms for accepted content, native changes, resolution, coordinate transformation or reconstruction, projection generation, serialization, persistence, and established sidecars.
3. Map each core content fragment and claimed proposal kind to the smallest existing native unit that can preserve its semantic observations. Record unsupported kinds and relations instead of assuming that a new implementation is needed.
4. Identify the native operation, tree transform, regeneration step, or reconstruction that yields accept and reject outcomes and the successor attachment of every remaining pending proposal.
5. Compare accepted state, both projections, proposal identity, association and same-point ordering, unavailable-target behavior, and the persistence result with the existing core and profile requirements.
6. Add configuration, sidecar data, or adapter-local transformation only for a demonstrated mismatch, documenting why the existing mechanism is insufficient. Reuse alone is not proof of equivalence.
7. Reopen or reload the declared persistence boundary, bind observations and any declared adaptation or loss to the mapping report, and refuse or roll back when the claimed equivalence cannot be established.

This sequence avoids treating an observable successor-target requirement as an instruction to invent a general remapping service. Markers, live ranges, model operations, package-tree transformations, regeneration, and reconstruction can all be valid implementation bases. Their validity depends on the resulting projections, identities, attachments, reports, and persistence observations.

The initial independently versioned profiles are:

- [WordprocessingML Tracked Revisions Mapping Profile](profiles/wordprocessingml.md);
- [ODF Text Change Tracking Mapping Profile](profiles/odf-text.md); and
- [Reference Web Editor Track Changes Mapping Profile](profiles/reference-web-editor.md).

Implementations are not required to support all three. A profile's inclusion in this publication does not broaden the core subset or imply that its entire upstream format or product conforms.

The informative [profile evaluation procedure](evaluation/README.md#profile-evaluation) defines how an implementation can package reproducible evidence for one profile, version, direction, and persistence boundary without broadening the profile's normative claim.

## 17. Security, privacy, and integrity

Proposal provenance and retained terminal records can contain personal or audit-sensitive information. Implementations SHOULD apply data minimization, access control, retention, and disclosure policies appropriate to their use. Redaction at a claimed mapping boundary is reportable when it removes preserve-if-present information.

Consumers MUST treat proposal text, provenance, extension values, and human-readable explanations as untrusted data. This standard does not authorize rendering markup as active content or executing extension values.

Base fingerprints provide integrity binding to an accepted state; they do not authenticate the source, signer, reviewer, or transport. Applications requiring authenticity or non-repudiation need an external signature and trust model.

Implementations SHOULD bound input sizes, nesting, proposal counts, and resolution work to resist denial of service. Such limits are capabilities and MUST yield truthful unsupported or failed reports rather than partial mutation.

## 18. Limitations and reassessment triggers

This version deliberately standardizes a subset. It does not claim lossless coverage of rich office documents or every Web editor. Existing implementations differ in replacement grouping, formatting derivation, paragraph semantics, identity, provenance, nesting, and persistence. Some accepted-content workflows do not need pending revision portability at all.

More precisely, point and range targets apply within one accepted paragraph, while a paragraph-boundary target identifies one adjacent paragraph pair. Subject to a selected profile's capability claim, this supports paragraph-local insertion, deletion, replacement, and formatting—including a large exact range within one paragraph—and one paragraph split or merge. A line-break scalar that a profile maps inside one paragraph is not necessarily a structural paragraph break.

Version 1 does not generally represent one atomic paste that creates or spans several paragraphs, one deletion across several paragraphs or disjoint ranges, proposal groups or hierarchy, overlapping or dependent proposals, or material expansion or shrinkage of a pending proposal under the same identity. Splitting one authored compound operation into several independent proposals is not automatically equivalent: it can create intermediate, independently resolvable outcomes that the source operation did not permit. Version 1 also does not define arbitrary partial acceptance within a proposal; one proposal is the atomic review unit.

These limits do not erase the value of exact identity, projections, successor remapping, persistence checks, and truthful loss or refusal for the supported subset. They do prevent an unqualified claim that version 1 completely standardizes a general-purpose document review mode. Compound structural proposals and predictable evolution of pending changes are high-priority reassessment areas, but their grouping, targeting, lineage, and atomic resolution semantics remain unresolved.

The model should be reassessed if:

- independent adapters cannot reproduce the required acceptance and rejection projections;
- common source systems systematically cannot provide the mandatory formatting or deletion payloads;
- paragraph split/merge requires a broader portable tree for useful interoperability;
- implementer feedback identifies a materially different minimum useful subset;
- repeated extensions show stable demand for moves, richer structure, or dependencies; or
- the chosen serialization or fingerprint profile causes material cross-implementation failure.

Until cross-vendor profile fixtures and implementation reports exist, conformance to this core demonstrates adherence to the neutral contract, not adoption prevalence or universal round-trip success.

## 19. Versioning and maintenance

`modelVersion` identifies semantic compatibility. A change that makes an existing conforming semantic instance or outcome incompatible requires a new model version.

`serializationProfile` identifies schema interpretation and canonical bytes. A change that can alter parsing, validation, canonical encoding, accepted-state projection bytes, or fingerprints requires a new serialization profile.

Mapping profiles have independent versions and pin their upstream source boundary. Updating one profile does not change the core model, another profile, or an earlier profile-scoped conformance claim.

Additive corrections that do not change normative meaning MAY update prose or tests without changing version values. Errata that change normative behavior MUST identify their compatibility impact and follow the version rules above. Published versions SHOULD be preserved with explicit document metadata and matching Git tags.

This document is publication version `1.0.1`, identified by release tag `web-editor-revisions-v1.0.1`, and succeeds version `1` at tag `web-editor-revisions-v1`. It keeps model version `1`, serialization profile `json-jcs-1`, the schema, proposal semantics, and profile capability claims unchanged. The [release record](release.md) documents its patch classification, complete change set, validation, acceptance, and propagation state.

A permanent publication authority, schema URI, extension registry authority, and long-term maintenance community have not yet been assigned. A future publication authority MUST assign stable identifiers without silently changing the normative schema contents. Until then, the repository path, release tag, and Git history identify a released version; claims SHOULD include the exact commit identifier.

The publication's [evidence index](evidence.md) and [decision provenance](provenance.md) are informative maintenance inputs. They preserve the supporting and contradictory evidence and the rationale for the current boundaries without adding requirements. The [publication index](README.md) identifies the complete accepted set and adoption path.
