# ODF Text Change Tracking Mapping Profile

Project status: Maintainer-reviewed

Profile identifier: `web-editor-revisions.odf-text-change-tracking`

Profile version: `1`

Core semantic model version: `1`

Canonical serialization profile: `json-jcs-1`

## 1. Purpose and conformance language

This profile defines direction-specific mappings between the Web Editor Revisions core and a bounded OpenDocument Text change-tracking subset. It deliberately does not claim coverage of all ODF text structures or application-specific tracked-change behavior.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are interpreted as described in BCP 14 when they appear in all capitals. Sections 1 through 10 are normative. Section 11 is informative.

Conformance is separate for `odf-text-to-core`, `core-to-odf-text`, or both and also requires mapping-adapter conformance to the [Web Editor Revisions core](../standard.md).

## 2. Pinned upstream boundary

This version is pinned to [Open Document Format for Office Applications (OpenDocument) Version 1.4, OASIS Standard, 6 October 2025](https://docs.oasis-open.org/office/OpenDocument/v1.4/os/part3-schema/OpenDocument-v1.4-os-part3-schema.html), specifically Part 3 Sections 5.5, 5.1.3, 6.1, and the referenced style and package rules required to determine effective text formatting. The authoritative ODF edition, not a moving implementation behavior, defines the source model.

The source boundary is one `office:text` body in a conforming ODF 1.4 text document. It covers ordered `text:p` paragraphs and the change-tracking constructs `text:tracked-changes`, `text:changed-region`, `text:insertion`, `text:deletion`, `text:format-change`, `office:change-info`, `text:change-start`, `text:change-end`, and `text:change`.

Headers, footers, sections with independent tracking scope, headings as a distinct structure, lists, tables, frames, notes, fields, indexes, drawing content, spreadsheet change tracking, and change marks outside the identified `office:text` scope are excluded. ODF 1.4 notes that historical change-tracking under-specification produced varying implementations; this profile therefore requires projection tests and does not infer interoperability from schema validity alone.

## 3. Supported source subset and preconditions

A source item is supported only when:

- its change region has one unique `xml:id` and exactly one insertion, deletion, or format-change record;
- every applicable change mark resolves unambiguously within the same `office:text` scope;
- its accepted and rejected projections can be reconstructed exactly under ODF 1.4;
- its affected content reduces to exact paragraph text and the four core effective formatting properties;
- pending changes are non-overlapping, non-nested, independent, and do not target content introduced by another pending change;
- paragraph-boundary behavior affects exactly two adjacent supported `text:p` elements; and
- every target endpoint is a valid UTF-16 code-point boundary.

The supported text subset consists of character data, `text:s`, `text:tab`, `text:line-break`, and `text:span` only when the adapter has a lossless scalar-text mapping and exact effective core formatting. `text:tab` maps to U+0009 and `text:line-break` maps to U+000A only when both remain paragraph-local and the target implementation preserves those scalar values exactly. Other inline elements are unsupported unless a later profile version defines them.

Effective values map as follows:

- `fo:font-weight` with the effective bold value maps to `bold`;
- `fo:font-style` with the effective italic value maps to `italic`;
- a single effective underline maps to `underline`; and
- a single effective line-through maps to `strikethrough`.

Named styles and inheritance MAY be used to compute the values, but the output always contains normalized Booleans. Theme-, locale-, or implementation-dependent values; multiple decoration styles; and unavailable style definitions are outside equivalent mapping.

An adapter MUST validate the ODF package and schema, tracking scope, identifiers, mark pairing, reconstructed projections, styles, and profile pending-set rules before mutation. Invalid source is `invalid-input`; a required but inaccessible value is `unavailable`.

## 4. Common state and identity mapping

### 4.1 Accepted state

For `odf-text-to-core`, the core accepted state is the exact state obtained by rejecting every supported pending ODF change. Inserted regions are absent, deleted content is reconstructed at its marks under Section 5.5.5, and format-change regions use their before values when those values are independently available. Paragraph order and boundaries are those of that rejection projection.

The adapter MUST NOT treat the current serialized ODF body, an application's display mode, or an accepted-all rendering as the accepted state without proving that it equals the rejection projection.

For `core-to-odf-text`, accepted paragraphs are emitted first, then pending change records and marks are added so that rejecting all pending changes yields those exact paragraphs.

Adjacent spans with identical effective core values MUST be coalesced into normalized core formatting coverage. This is a permitted no-impact normalization.

### 4.2 Paragraph identity

A unique, stable `xml:id` on a supported paragraph MAY be preserved as its core paragraph identity. If no such value exists, the adapter MUST synthesize a collision-free identity from the bound artifact and stable paragraph location and report `source-absent`, `synthesized`, and `impact: none`. The synthesis supports equivalence only across the exact boundary for which its stability is demonstrated.

On export, an adapter MAY emit collision-free `xml:id` values on supported paragraphs to carry core paragraph identities when permitted by the ODF schema and verified after reload. This is a declared no-impact adaptation. If it cannot carry them, omission affects `acceptedState.paragraphIdentity`, has `review-semantics-loss`, and requires authorization.

### 4.3 Proposal identity and provenance

The `text:changed-region/@xml:id` maps to `sourceProposalId`. It MAY map directly to the core `id` when it is unique in the portable lineage; otherwise a core identity is synthesized and the source value is retained.

`sourceSystem` identifies this profile and exact source artifact. `office:change-info/dc:creator` maps to `creator`, and `dc:date` maps to `createdAt` when valid. A timestamp spelling MAY be normalized while preserving the instant. Available comments are outside the core payload; they MAY be preserved through an optional extension, but silently dropping them cannot support an unqualified claim that all source information survived.

Every pending proposal receives the reconstructed accepted-state fingerprint as `baseFingerprint`.

## 5. ODF-Text-to-core mapping

The following mappings apply when Section 3 holds:

| ODF source construct | Core result | Additional requirement |
| --- | --- | --- |
| `text:insertion` with one marked paragraph-local region | `insert` | Target is the point in the rejection projection; content and formatting come from the inserted marked region. |
| `text:deletion` reconstructing one non-empty paragraph-local region | `delete` | Target covers the reconstructed source text; payload MUST match the deleted content and effective formatting exactly. |
| Deletion whose ODF reconstruction joins exactly two adjacent supported paragraphs | `paragraph-merge` | Reject preserves two paragraphs; accept produces their exact concatenation and the left identity survives. |
| Insertion whose two projections differ only by one new paragraph boundary | `paragraph-split` | Reject has one paragraph; accept has exactly two; the left identity survives and the right identity is reserved. |
| `text:format-change` with externally verifiable effective before/after values | `format` | Both values MUST be bound to the exact source artifact and uniform over one non-empty range. |

ODF 1.4 explicitly states that `text:format-change` does not contain the formatting changes that occurred. The element alone is therefore insufficient for a core `format` proposal. An adapter MAY use an authoritative application snapshot, retained prior style record, or extension only when that evidence is bound to the input and yields both exact projections. Otherwise it MUST refuse the proposal as unavailable or unsupported; it MUST NOT infer `before` from the current appearance.

Document order MAY synthesize `samePointOrder` for co-located insertions only when it yields the exact ODF projection. The synthesis MUST be reported with no impact.

Adjacent ODF insertion and deletion regions do not establish an atomic replacement. They MUST remain independent when the core pending-set rules allow it. If they overlap or depend on one another, they are unsupported. A `replace` requires a separately identified extension that proves one identity and atomic resolution.

## 6. Core-to-ODF-Text mapping

| Core proposal | ODF result | Equivalent export condition |
| --- | --- | --- |
| `insert` | One `text:changed-region/text:insertion` and matching change marks | Exact point, content, order, provenance, and both projections survive. |
| `delete` | One `text:changed-region/text:deletion` carrying reconstructible deleted content and a position mark | Reject reconstructs the exact payload; accept removes exactly the target. |
| `paragraph-split` | One insertion change whose marks and paragraph markup produce the two exact projections | ODF reconstruction and reload prove the split, including left/right text and identity behavior. |
| `paragraph-merge` | One deletion change whose stored content and marks reconstruct the removed boundary | ODF reconstruction and reload prove the merge and rejection restores both paragraphs. |

Core `format` has no equivalent ODF 1.4 text-change encoding because the native `text:format-change` record omits the prior formatting delta required for rejection. Export MUST refuse without mutation unless a separately identified extension profile carries the complete before/after values. Emitting a bare `text:format-change` is review-semantics loss and MUST NOT be labeled equivalent, even with authorization.

Core `replace` likewise has no native atomic relation. An adapter MUST refuse or, with explicit authorization, emit separate insertion and deletion regions and report loss of `proposal.kind`, `proposal.relations`, `resolution.atomicity`, and affected projections.

The adapter MUST allocate unique `xml:id` values, keep all change marks in the same identified scope, and serialize an ODF-conforming package. Unsupported concurrent structures MUST cause refusal or complete rollback rather than partial emission.

## 7. Permitted no-impact adaptations

The following are permitted when exact text, effective formatting, targets, identities after declared synthesis, and both projections remain unchanged:

- coalescing or splitting `text:span` boundaries with identical effective core formatting;
- synthesizing stable paragraph or proposal identities for source-absent values;
- adding schema-permitted `xml:id` values to carry core identity;
- deriving same-point order from deterministic change-mark document order;
- expanding ODF whitespace elements into their exact scalar values and serializing the same values back with any ODF-equivalent form; and
- normalizing a timestamp spelling while preserving its instant.

Each represented synthesis or normalization MUST be declared. Style approximation, deletion reconstruction that changes paragraph boundaries, comment loss, and any inferred formatting delta are not no-impact adaptations.

## 8. Loss, refusal, and report bindings

At minimum, adapters MUST apply these classifications:

| Condition | Required fields and impact | Required behavior |
| --- | --- | --- |
| `text:format-change` lacks verifiable before/after values | `proposal.payload`, acceptance and rejection projections; `review-semantics-loss` | Refuse. A bare native format-change never supports equivalence. |
| Atomic replacement relation absent | `proposal.kind`, `proposal.relations`, `resolution.atomicity`; `review-semantics-loss` | Refuse, or emit authorized lossy paired changes. |
| Change marks are unpaired, cross scope, nested, or ambiguous | `proposal.target` and affected relations; normally `invalid-input` or `review-semantics-loss` | Refuse without mutation. |
| Deleted content cannot be reconstructed exactly | `proposal.payload`, `resolution.rejectionProjection`; `review-semantics-loss` | Refuse; approximation requires authorization. |
| Available creator, date, or comment is omitted | `proposal.provenance` or a profile URI field; `optional-information-loss` | Require omission authorization before mutation. |
| Paragraph identity cannot survive export | `acceptedState.paragraphIdentity`; `review-semantics-loss` | Refuse or require omission authorization. |
| Save/reload changes marks, IDs, styles, or projections | `mapping.persistence` plus affected semantic fields | Report `persistence-failure`; residual mutation is a transaction-integrity failure. |

Every report MUST use the identifier and version at the top of this profile. `direction` MUST be `odf-text-to-core` or `core-to-odf-text`. `boundary` MUST name the exact ODF package, `office:text` scope, and any save/reload boundary. Input and output references MUST bind the complete observed artifacts and any authoritative auxiliary snapshot used for format mapping.

Profile stages are `source-parse`, `base-reconstruction`, `style-resolution`, `target-mapping`, `proposal-mapping`, `source-serialization`, and `save-reload`.

## 9. Direction-specific conformance

A conforming `odf-text-to-core` adapter MUST validate the pinned schema and profile subset, reconstruct the rejection projection, create a conforming core interchange document, bind any auxiliary evidence, and compare exact accept/reject projections for each claimed change.

A conforming `core-to-odf-text` adapter MUST validate the complete core input, emit a conforming ODF 1.4 package, independently reopen it, reconstruct both projections, and verify identities and provenance across the claimed boundary. It MUST refuse format and replacement proposals unless the required separately versioned extension is declared.

One direction, one `office:text` scope, or one proposal kind does not imply any other. Schema validity alone does not establish this profile's semantic conformance.

## 10. Minimum profile fixtures

A claim MUST declare its direction, proposal-kind capabilities, and whether an `odf-text-to-core` claim additionally covers source persistence. Fixtures are activated by `always`, by a declared proposal-kind capability, or by `source-persistence`. Every activated fixture MUST pass; `not-run` or an inapplicability assertion does not satisfy it. An unclaimed capability is not supported by the claim.

The fixture identifiers below are mirrored by the evaluation catalog. The profile text is normative if the catalog differs.

### 10.1 `odf-text-to-core`

<!-- profile-matrix:odf-text-to-core:start -->
| Fixture identifier | Activated by | Required observation |
| --- | --- | --- |
| `bound-source-core-report` | `always` | The complete ODF input, core output, auxiliary evidence, profile, direction, and measured boundary are bound by the final report. |
| `accepted-formatting-booleans` | `always` | Style inheritance yields exact effective values for all four core formatting properties. |
| `stable-xml-id` | `always` | A usable stable `xml:id` is preserved truthfully. |
| `source-absent-identity` | `always` | Missing paragraph or proposal identity is synthesized stably and reported. |
| `format-change-refusal` | `always` | A bare or otherwise unresolvable `text:format-change` is refused without mutation. |
| `paired-replacement-shape` | `always` | Paired insertion and deletion regions are not promoted to atomic replacement. |
| `ambiguous-marks-refusal` | `always` | Ambiguous change marks cause no mutation. |
| `nested-marks-refusal` | `always` | Nested marks outside the subset cause no mutation. |
| `cross-scope-marks-refusal` | `always` | Cross-scope marks cause no mutation. |
| `paragraph-insertion-non-bmp` | `insert` | A paragraph-local insertion with non-BMP text maps at valid UTF-16 boundaries. |
| `colocated-mark-order` | `insert` | Co-located insertions use deterministic mark order that reproduces the source projection. |
| `paragraph-deletion-non-bmp` | `delete` | A paragraph-local deletion with non-BMP text reconstructs exactly. |
| `deletion-formatting-reconstruction` | `delete` | Reconstructed deleted content retains exact effective formatting. |
| `format-change-authoritative-values` | `format` | Bound authoritative evidence supplies exact uniform before and after values and both projections. |
| `paragraph-split` | `paragraph-split` | Paragraph split follows the ODF reconstruction rules with exact identity behavior. |
| `paragraph-merge` | `paragraph-merge` | Paragraph merge follows the ODF reconstruction rules with exact identity behavior. |
| `source-package-save-reload` | `source-persistence` | The authoritative ODF source survives save/reload with marks, styles, identities, and projections intact. |
| `source-persistence-projections-identities` | `source-persistence` | Source persistence retains the complete bound projections and identity observations. |
<!-- profile-matrix:odf-text-to-core:end -->

### 10.2 `core-to-odf-text`

This base profile does not offer a `format` capability in this direction. Native save/reload, rollback, and partial-persistence detection are mandatory.

<!-- profile-matrix:core-to-odf-text:start -->
| Fixture identifier | Activated by | Required observation |
| --- | --- | --- |
| `core-input-validation` | `always` | Invalid core input is rejected before native mutation. |
| `bound-core-native-report` | `always` | The complete core input, ODF package output, profile, direction, and save/reload boundary are bound by the final report. |
| `accepted-formatting-booleans` | `always` | Accepted-state text retains all four effective formatting Booleans after ODF reload. |
| `stable-export-identity-policy` | `always` | Core identities are carried through schema-permitted values or refused or omitted only under the required reported policy. |
| `core-format-refusal` | `always` | A valid core format proposal is refused unless a separately versioned extension supplies complete semantics. |
| `core-replacement-policy` | `always` | A core replacement is refused or emitted only as an authorized, reported non-equivalent pair. |
| `native-save-reload-success` | `always` | A successful ODF package independently reopens with marks, styles, projections, and identity observations intact. |
| `native-clean-failure` | `always` | A failed native write leaves no output mutation. |
| `native-rollback` | `always` | A failure after attempted mutation fully restores the declared package boundary. |
| `native-partial-persistence` | `always` | Residual package mutation is detected as transaction-integrity failure and cannot support a passing conformance result. |
| `paragraph-insertion-non-bmp` | `insert` | A core insertion with non-BMP text emits exact ODF change markup. |
| `colocated-mark-order` | `insert` | Co-located core insertions retain their explicit order after reload. |
| `paragraph-deletion-non-bmp` | `delete` | A core deletion with non-BMP text remains exactly reconstructible. |
| `deletion-formatting-reconstruction` | `delete` | The ODF deletion record reconstructs the exact formatted payload. |
| `paragraph-split` | `paragraph-split` | A core split retains exact projections under ODF reconstruction and reload. |
| `paragraph-merge` | `paragraph-merge` | A core merge retains exact projections under ODF reconstruction and reload. |
<!-- profile-matrix:core-to-odf-text:end -->

## 11. Informative implementation notes

Implementations may use an ODF library, direct XML processing, or an office application's API. A robust importer can materialize reject-all and accept-one copies and compare their normalized supported paragraphs. Such a technique is informative; the required outcome is the normative state and projection equivalence in this profile.

A declarative-package planning trace can begin with `text:tracked-changes`, each typed `text:changed-region` record, the referenced change marks, accepted-content reconstruction, and the chosen library or application API. For each claimed proposal kind, the adapter maps the exact content fragment and review unit through those existing records and marks. Resolution can occur in core followed by package regeneration, or through mutation of change regions followed by reconstruction of the remaining marks and targets. Independently reopening the package and comparing both projections, identity observations, successor attachments, mapping reports, and persistence results completes the trace; no separate general remapping primitive is implied.

The native mechanism does not close every semantic gap. A bare `text:format-change` does not carry the exact prior formatting delta, and this profile does not establish an atomic native replacement relation. Those cases need an extension, reported loss, or refusal when exact equivalence cannot be shown. They are not reasons to duplicate every core operation inside an ODF model.
