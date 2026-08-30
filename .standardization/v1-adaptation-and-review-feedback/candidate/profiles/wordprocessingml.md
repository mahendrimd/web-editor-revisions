# WordprocessingML Tracked Revisions Mapping Profile

Project status: Maintainer-reviewed

Profile identifier: `web-editor-revisions.wordprocessingml-tracked-revisions`

Profile version: `1`

Core semantic model version: `1`

Canonical serialization profile: `json-jcs-1`

## 1. Purpose and conformance language

This profile defines direction-specific mappings between the Web Editor Revisions core and a narrow WordprocessingML tracked-revision subset. It does not claim that every WordprocessingML document, every Microsoft Word behavior, or every Open XML SDK operation maps to the core.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are interpreted as described in BCP 14 when they appear in all capitals. Sections 1 through 10 are normative. Section 11 is informative.

An implementation conforms separately for `wordprocessingml-to-core`, `core-to-wordprocessingml`, or both. It MUST also conform as a mapping adapter under the [Web Editor Revisions core](../standard.md).

## 2. Pinned upstream boundary

This version is pinned to [ECMA-376, fifth edition](https://ecma-international.org/publications-and-standards/standards/ecma-376/):

- Part 1, *Fundamentals and Markup Language Reference*, fifth edition, December 2016, for WordprocessingML vocabulary and semantics; and
- Part 2, *Open Packaging Conventions*, fifth edition, December 2021, for the package and Main Document part boundary.

The profile covers a conforming **Strict** WordprocessingML Main Document part rooted at `w:document/w:body`. It covers ordered `w:p` paragraphs whose supported text and tracked revisions are represented by `w:r`, `w:t`, `w:delText`, `w:ins`, `w:del`, `w:rPr`, `w:rPrChange`, and revision marks on paragraph marks. Revision metadata uses the applicable `w:id`, `w:author`, and `w:date` values.

The source subset excludes Transitional-only vocabulary; headers, footers, notes, comments, text boxes, glossary parts, and other stories; tables, lists as structures, fields, drawings, content controls, custom XML, math, bidirectional-control markup, and non-text objects; moves; and revision forms outside the version 1 core. A package containing excluded content is not globally invalid, but a conforming operation MUST limit its claim to an identified supported body range or report and refuse or lossily handle every excluded item that affects that boundary.

The [Microsoft Open XML revision example](https://learn.microsoft.com/en-us/office/open-xml/word/how-to-accept-all-revisions-in-a-word-processing-document) and ISO-derived Open XML SDK type pages are supporting explanations, not a second or floating normative edition.

## 3. Supported source subset and preconditions

A source item is in the supported subset only when all of the following hold:

- its accepted and rejected projections can be reconstructed exactly from the pinned markup;
- its content can be expressed as ordered paragraphs, exact Unicode text, and the four core formatting properties;
- its pending revisions are non-overlapping, non-nested, independent, and attached only to accepted-state content;
- every deletion retains the exact deleted text and effective core formatting;
- every formatting revision exposes one uniform effective `before` value and one effective `after` value for each mapped property;
- paragraph-boundary revisions affect exactly two adjacent supported paragraphs; and
- every target can be represented on valid UTF-16 code-point boundaries.

The source text subset uses `w:t` for ordinary text and `w:delText` for deleted text. Tabs, line breaks, field results, soft hyphens represented as markup, drawings, embedded objects, and other non-`w:t` text-like constructs are outside the supported subset unless a later profile version defines them.

Effective formatting MUST be computed after applying the WordprocessingML style cascade and run-property rules. This profile maps only:

- `w:b` to `bold`;
- `w:i` to `italic`;
- `w:u` with the single-underline value to `underline`; and
- `w:strike` to `strikethrough`.

Absent or explicitly false effective values map to `false`. Theme-dependent, complex-script-only, double-strike, non-single underline, or otherwise unresolved formatting is not silently collapsed into a core Boolean.

Before mutation or emission, an adapter MUST validate the package, supported source subset, revision identifiers, revision nesting, text reconstruction, effective formatting, and both projections. Failure of a source invariant is `invalid-input`; inability to obtain a value that the source should expose is `unavailable`.

## 4. Common state and identity mapping

### 4.1 Accepted state

For `wordprocessingml-to-core`, the core accepted state is the exact supported document state obtained by rejecting every supported pending WordprocessingML revision. Inserted content is absent; deleted content is restored; prior run properties are effective; an inserted paragraph mark is absent; and a deleted paragraph mark is restored. The adapter MUST NOT use a display view or accepted-all projection as the accepted state.

Paragraph order follows body order. Paragraph text is the concatenation of supported text nodes after rejection projection. Adjacent runs with identical effective core values MUST be coalesced into normalized core formatting coverage. This coalescing is a permitted no-impact normalization.

For `core-to-wordprocessingml`, the accepted state is serialized as untracked supported paragraphs before proposal marks are applied. Source run boundaries MAY differ from core formatting-run boundaries only when the four effective values and exact text remain identical.

### 4.2 Paragraph identity

An adapter MUST preserve a source paragraph identifier only when it can prove that the value is unique and stable across the claimed boundary. Otherwise it MUST synthesize a collision-free core paragraph identity from a stable artifact reference and stable paragraph location, and report `condition: source-absent`, `action: synthesized`, `impact: none`. The synthesis qualifies for `equivalent-with-declared-adaptation` only for a boundary across which the synthesized value remains stable.

Strict WordprocessingML in this profile has no required carrier for core paragraph identity on export. A `core-to-wordprocessingml` operation that omits it has `review-semantics-loss` on `acceptedState.paragraphIdentity` and requires authorization, unless a separately identified extension profile supplies a stable carrier.

### 4.3 Proposal identity and provenance

A usable `w:id` MUST be copied to `sourceProposalId`. It MAY become the core `id` only when it is unique in the portable lineage. Otherwise the adapter MUST synthesize a core `id`, retain the source value as `sourceProposalId`, and report the no-impact synthesis.

`sourceSystem` MUST identify this profile and the exact source artifact. Available `w:author` maps to `creator`; available `w:date` maps to `createdAt`. Normalizing a timestamp to a core-valid UTC spelling while preserving the instant is a permitted declared normalization. Missing provenance is `source-absent`; dropping available provenance is `optional-information-loss`.

Every pending proposal receives the fingerprint of the reconstructed accepted state as `baseFingerprint`.

## 5. WordprocessingML-to-core mapping

Each source revision maps as follows when the Section 3 preconditions hold:

| Source construct | Core result | Additional requirement |
| --- | --- | --- |
| Inline `w:ins` containing supported runs | `insert` | Target is the insertion point in the rejection projection; payload is the inserted exact text and effective formatting. |
| Inline `w:del` containing supported runs and `w:delText` | `delete` | Target covers the restored deleted content in the rejection projection; payload MUST match it exactly. |
| `w:rPrChange` on one non-empty paragraph-local range | `format` | Current effective values are `after`; the stored previous run properties yield `before`; only changed core properties are emitted and one record remains atomic. |
| Inserted paragraph mark affecting one supported paragraph | `paragraph-split` | Rejecting preserves one paragraph and accepting yields exactly two; the original identity remains left and a collision-free right identity is reserved. |
| Deleted paragraph mark between two adjacent supported paragraphs | `paragraph-merge` | Rejecting preserves two paragraphs and accepting yields their exact concatenation with the left identity retained. |

Source document order MAY be used to synthesize `samePointOrder` for co-located insertions when it defines the exact accepted projection. The adapter MUST report the synthesis with `impact: none`; it MUST NOT use proposal identity, author, timestamp, or an unordered collection.

Adjacent insertion and deletion revisions MUST NOT be inferred to be one replacement. They map as independent proposals only when the resulting pending set is valid. If their targets overlap or their outcomes depend on each other, the operation MUST refuse them as unsupported. An atomic `replace` is available only when a separately identified extension supplies a verifiable one-proposal relationship and both projections.

Moves, nested revisions, cross-paragraph inline revisions, property changes outside the four core values, and source structures with unsupported text or paragraph semantics are outside the equivalent mapping.

## 6. Core-to-WordprocessingML mapping

For a supported export, the adapter MUST emit conforming Strict WordprocessingML and MUST preserve the rejection and acceptance projections defined by the core:

| Core proposal | WordprocessingML result | Equivalent export condition |
| --- | --- | --- |
| `insert` | Inline `w:ins` around supported inserted runs | Exact point, payload text, formatting, order, identity, and provenance survive. |
| `delete` | Inline `w:del` with supported runs and `w:delText` | Exact deleted payload remains available for rejection. |
| `format` | Current run properties plus one `w:rPrChange` containing the complete prior run properties for the range | All changed core properties resolve together and both effective-value projections match. |
| `paragraph-split` | Tracked insertion of the applicable paragraph mark | Reject yields the original paragraph; accept yields the exact left/right paragraphs. |
| `paragraph-merge` | Tracked deletion of the boundary paragraph mark | Reject yields both paragraphs; accept concatenates exactly and retains the left paragraph semantically. |

The adapter MUST allocate conforming non-colliding revision identifiers. Source run segmentation, XML prefixes, attribute order, package compression, and equivalent run coalescing are nonsemantic and need no issue unless the adapter represents them as a declared adaptation.

Strict WordprocessingML does not provide a core atomic-replacement relation. Export of `replace` MUST therefore either refuse without mutation or, with caller authorization, emit separate deletion and insertion revisions and report loss of `proposal.kind`, `proposal.relations`, `resolution.atomicity`, and any affected projection. The paired output MUST NOT be described as equivalent.

When multiple core proposals cannot be represented as a valid independent WordprocessingML pending set, the operation MUST refuse or fully roll back. It MUST NOT partially emit the set.

## 7. Permitted no-impact adaptations

The following adaptations are permitted only when the observable core state and both projections are unchanged:

- coalescing or splitting source runs at identical effective core values;
- synthesizing stable core paragraph or proposal identities for a source-absent value across the declared boundary;
- deriving `samePointOrder` from a deterministic source document order that reproduces the source projection;
- normalizing an equivalent timestamp spelling while preserving its instant; and
- omitting WordprocessingML properties and package details outside the identified supported body range from the core output.

Each synthesis or normalization that changes a represented value MUST be declared in the mapping report. An excluded source feature that affects text, formatting, proposal identity, target, lifecycle, or a projection is not a no-impact adaptation.

## 8. Loss, refusal, and report bindings

At minimum, adapters MUST apply these classifications:

| Condition | Required fields and impact | Required behavior |
| --- | --- | --- |
| Atomic replacement relation unavailable | `proposal.kind`, `proposal.relations`, `resolution.atomicity`; `review-semantics-loss` | Refuse, or emit authorized lossy paired revisions. |
| Deleted payload or prior formatting unavailable | `proposal.payload` and affected projection; `review-semantics-loss` | Refuse; approximation requires authorization and cannot be equivalent. |
| Move, nested/dependent revision, unsupported structure, or cross-paragraph range | Narrowest affected target/kind/relation fields; `review-semantics-loss` | Refuse, or apply an explicitly authorized lossy policy. |
| Available author or date omitted | `proposal.provenance`; `optional-information-loss` | Require omission authorization before mutation. |
| Paragraph identity has no stable export carrier | `acceptedState.paragraphIdentity`; `review-semantics-loss` | Refuse or require omission authorization. |
| Save/reload loses revision markup or metadata | `mapping.persistence` plus affected fields | Report `persistence-failure`; residual mutation is `transaction-integrity-failure`. |

Every report MUST set `profile.id` and `profile.version` to the values at the top of this document. `direction` MUST be `wordprocessingml-to-core` or `core-to-wordprocessingml`. `boundary` MUST identify the exact package part or save/reload boundary. `inputRef` and `outputRef` MUST bind the complete observed package or core interchange artifact, not an unbound paragraph excerpt.

Profile stages are `source-parse`, `base-reconstruction`, `target-mapping`, `proposal-mapping`, `source-serialization`, and `save-reload`. An issue MUST use the narrowest applicable core affected fields.

## 9. Direction-specific conformance

A conforming `wordprocessingml-to-core` adapter MUST:

- validate the pinned source subset;
- reconstruct the rejection projection before creating targets;
- produce a conforming core interchange document and bound report;
- demonstrate exact acceptance and rejection projections for every claimed source construct; and
- refuse or truthfully classify every source item outside its declared capability.

A conforming `core-to-wordprocessingml` adapter MUST:

- validate the complete core input before mutation;
- emit conforming Strict WordprocessingML for every claimed proposal kind;
- reopen or independently parse the emitted package and verify both projections at the claimed persistence boundary;
- preserve or report identity and provenance; and
- roll back the complete output boundary on an unauthorized or failed mapping.

Passing one direction does not imply the other. Passing supported paragraph-local cases does not imply support for an entire `.docx` package or for Transitional WordprocessingML.

## 10. Minimum profile fixtures

A claim MUST declare its direction, proposal-kind capabilities, and whether a `wordprocessingml-to-core` claim additionally covers source persistence. A required fixture is activated by `always`, by a declared proposal-kind capability, or by the optional `source-persistence` boundary. Every activated fixture MUST pass. An unclaimed capability does not activate its fixtures and MUST NOT be advertised as supported. `not-run` or an inapplicability assertion does not satisfy a required fixture.

The fixture identifiers below are mirrored by the evaluation catalog. The profile text is normative if the catalog differs.

### 10.1 `wordprocessingml-to-core`

<!-- profile-matrix:wordprocessingml-to-core:start -->
| Fixture identifier | Activated by | Required observation |
| --- | --- | --- |
| `bound-source-core-report` | `always` | The complete Strict package input, core output, profile, direction, and measured boundary are bound by the final report. |
| `accepted-formatting-booleans` | `always` | Accepted-state style resolution yields exact bold, italic, single-underline, and strikethrough Booleans. |
| `stable-synthesized-identity` | `always` | Source-absent paragraph or proposal identity is synthesized stably and reported without claiming native identity. |
| `unavailable-deleted-payload` | `always` | A source deletion whose exact payload cannot be recovered is refused without mutation. |
| `unsupported-formatting` | `always` | Unsupported or unresolved formatting is refused or handled only by an authorized, reported non-equivalent policy. |
| `adjacent-replacement-shape` | `always` | Adjacent insertion and deletion revisions are not promoted to atomic replacement. |
| `nested-content-refusal` | `always` | Nested or dependent revision content outside the subset is refused without mutation. |
| `moved-content-refusal` | `always` | Moved content outside the subset is refused without mutation. |
| `insertion-non-bmp` | `insert` | A paragraph-local insertion with non-BMP text maps at valid UTF-16 boundaries with exact projections. |
| `colocated-insertions` | `insert` | Two co-located insertions receive deterministic order that reproduces the source projection. |
| `deletion-non-bmp` | `delete` | A paragraph-local deletion with non-BMP text retains the exact payload and projections. |
| `format-bold` | `format` | A bold change has exact effective before and after values. |
| `format-italic` | `format` | An italic change has exact effective before and after values. |
| `format-single-underline` | `format` | A single-underline change has exact effective before and after values. |
| `format-strikethrough` | `format` | A strikethrough change has exact effective before and after values. |
| `paragraph-split` | `paragraph-split` | A tracked paragraph-mark insertion produces exact split projections and identity behavior. |
| `paragraph-merge` | `paragraph-merge` | A tracked paragraph-mark deletion produces exact merge projections and identity behavior. |
| `source-package-save-reload` | `source-persistence` | The authoritative source package survives save/reload with the claimed revision boundary unchanged. |
| `source-persistence-identity-provenance-marks` | `source-persistence` | Identity, available provenance, and revision marks remain bound across the additional source-persistence boundary. |
<!-- profile-matrix:wordprocessingml-to-core:end -->

### 10.2 `core-to-wordprocessingml`

Native save/reload, rollback, and partial-persistence detection are mandatory in this direction.

<!-- profile-matrix:core-to-wordprocessingml:start -->
| Fixture identifier | Activated by | Required observation |
| --- | --- | --- |
| `core-input-validation` | `always` | Invalid core input is rejected before native mutation. |
| `bound-core-native-report` | `always` | The complete core input, Strict package output, profile, direction, and save/reload boundary are bound by the final report. |
| `accepted-formatting-booleans` | `always` | Accepted-state text retains all four exact effective formatting Booleans after native reload. |
| `stable-export-identity-policy` | `always` | Paragraph and proposal identities are carried where possible or refused or lossily omitted only with the required report and authorization. |
| `core-replacement-policy` | `always` | A core replacement is refused or exported only as an authorized, reported non-equivalent pair. |
| `native-save-reload-success` | `always` | A successful native package survives independent reopen with projections and revision state intact. |
| `native-clean-failure` | `always` | A failed native write leaves no output mutation. |
| `native-rollback` | `always` | A failure after attempted mutation fully restores the declared output boundary. |
| `native-partial-persistence` | `always` | Residual package mutation is detected as transaction-integrity failure and cannot support a passing conformance result. |
| `bound-identity-provenance-marks` | `always` | Identity, available provenance, and revision marks remain bound across package persistence. |
| `insertion-non-bmp` | `insert` | A core insertion with non-BMP text emits an exact supported tracked insertion. |
| `colocated-insertions` | `insert` | Co-located core insertions retain their explicit order after reload. |
| `deletion-non-bmp` | `delete` | A core deletion with non-BMP text retains exact restorable content. |
| `format-bold` | `format` | A bold proposal emits exact current and prior effective values. |
| `format-italic` | `format` | An italic proposal emits exact current and prior effective values. |
| `format-single-underline` | `format` | A single-underline proposal emits exact current and prior effective values. |
| `format-strikethrough` | `format` | A strikethrough proposal emits exact current and prior effective values. |
| `paragraph-split` | `paragraph-split` | A core split remains one tracked paragraph-boundary proposal with exact projections. |
| `paragraph-merge` | `paragraph-merge` | A core merge remains one tracked paragraph-boundary proposal with exact projections. |
<!-- profile-matrix:core-to-wordprocessingml:end -->

## 11. Informative implementation notes

An implementation may use the Open XML SDK, another XML library, or a native editor API. SDK class names and accept-all code are recipes, not requirements. A useful implementation strategy is to build and compare explicit reject-all and accept-one projections before emitting a core proposal; this does not replace the normative projection checks above.

A declarative-package planning trace can begin with the existing tracked-revision elements, document and run tree, effective-formatting cascade, and the selected XML library, SDK, or application API. For each claimed proposal kind, the adapter maps the exact content fragment and atomic review unit to the smallest applicable revision record and tree boundary. Resolution can occur in core followed by regeneration of the remaining native revisions, or through a package-tree or application transform followed by reconstruction of the surviving core targets. In either route, reopening the package and comparing both projections, identity observations, successor attachments, mapping reports, and persistence results is the proof boundary. The absence of a live coordinate service is not a reason to invent one.

Native revision markup still needs verification. The profile does not establish one native atomic replacement relation or a portable paragraph-identity carrier, and a tree mutation can leave surviving revisions attached differently even when the visible text looks plausible. Those gaps call for a reported adaptation, sidecar, refusal, or rollback as applicable, rather than an assumption that either native reuse or new machinery is automatically equivalent.
