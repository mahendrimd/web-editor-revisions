# Reference Web Editor Track Changes Mapping Profile

Project status: Maintainer-reviewed

Profile identifier: `web-editor-revisions.reference-web-editor-track-changes`

Profile version: `1`

Core semantic model version: `1`

Canonical serialization profile: `json-jcs-1`

## 1. Purpose and conformance language

“Reference Web Editor” is a project-local neutral label for the publicly documented upstream implementation snapshot linked in Section 2. It is not an upstream product name and does not imply affiliation, approval, sponsorship, or endorsement.

This profile defines direction-specific mappings between the Web Editor Revisions core and that bounded editor-native track-changes model. It standardizes observable mappings, not upstream internals, UI, licensing, deployment, or a preferred integration API.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are interpreted as described in BCP 14 when they appear in all capitals. Sections 1 through 10 are normative. Section 11 is informative.

Conformance is separate for `reference-web-editor-to-core`, `core-to-reference-web-editor`, or both and also requires mapping-adapter conformance to the [Web Editor Revisions core](../standard.md).

## 2. Pinned upstream boundary

This profile is pinned to the upstream reference-editor release [`v48.3.1`](https://github.com/ckeditor/ckeditor5/releases/tag/v48.3.1), signed tag commit `ece36da`, released 14 July 2026. The upstream release applies one version across the core and premium-feature package families.

The documented product-model snapshot comprises the v48.3.1 behavior described by:

- [Track changes overview](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes.html);
- [Track changes integration](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-integration.html);
- [Track changes custom features](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-custom-features.html); and
- the v48.3.1 `Suggestion`, `TrackChanges`, and `TrackChangesData` APIs represented by the release tag.

The moving `/latest/` documentation URLs are citations to that verified snapshot, not permission to drift to a later product model. A claim for another Reference Web Editor version requires a new or explicitly compatible profile version.

The source boundary is one loaded Reference Web Editor model root using the paragraph and basic inline-style features plus Track Changes in standalone asynchronous integration. The observed input consists of both:

- editor data containing loadable suggestion markers or equivalent model markers; and
- complete suggestion records obtained through the pinned `TrackChanges` integration or adapter contract.

HTML alone, highlight-only preview output, comments, revision history, real-time collaboration transport, AI provenance, General HTML Support, multi-root relationships, tables, lists, widgets, objects, custom elements, block formats other than paragraph split/merge, and custom suggestion types are excluded. Comments may be retained separately but are not core proposal payloads.

## 3. Supported source subset and preconditions

A Reference Web Editor suggestion is supported only when:

- it is attached to the identified model root and has complete suggestion metadata;
- it has one stable suggestion `id`, one supported type, and one paragraph-local range or one exact adjacent-paragraph boundary effect;
- accepting and discarding it produce exact, reproducible projections;
- suggestions in the claimed pending set are non-overlapping, non-nested, independent, and do not target content introduced by another pending suggestion;
- it is not multi-range, chained, or automatically joined with an excluded object or nested suggestion;
- its text maps exactly to Unicode scalar text on valid UTF-16 boundaries; and
- its formatting values are effective Booleans for `bold`, `italic`, `underline`, and `strikethrough`.

The adapter MUST observe the model state, not infer semantics solely from serialized marker names. Marker prefixes such as `insertion`, `deletion`, and `attribute` help bind records to ranges but do not by themselves prove core proposal kind, atomicity, or projections.

Before mutation, an adapter MUST verify the editor version, loaded plugin configuration, marker/record attachment, proposal identities, ranges, both projections, and persistence boundary. Invalid records or markers are `invalid-input`; a record or value expected from the configured integration but not retrievable is `unavailable`.

## 4. Common state and identity mapping

### 4.1 Accepted state

For `reference-web-editor-to-core`, the core accepted state is the exact supported paragraph state obtained by discarding every pending supported suggestion. The adapter MAY obtain it through a temporary pinned editor using `TrackChangesData` or through another procedure that yields the same model result. It MUST NOT use `editor.getData()` with markers, suggestion-highlight preview output, or an accepted-all projection as the accepted state.

Paragraph order follows model order. Text is the exact model text in the discard-all projection. Model attributes are resolved to complete core formatting coverage; adjacent equal runs are coalesced as a permitted no-impact normalization.

For `core-to-reference-web-editor`, the core accepted state is loaded first, then pending suggestions are created so that discarding all suggestions reproduces it exactly.

### 4.2 Paragraph identity

Reference Web Editor model elements do not provide a required portable lineage identity under this profile. An importer MUST synthesize collision-free core paragraph identities from the bound document identity and stable model path and report `source-absent`, `synthesized`, and `impact: none`. The synthesis qualifies for equivalence only when it remains stable across the exact claimed load/save boundary.

For export, an implementation MAY use a separately declared, schema-registered Reference Web Editor model attribute or application sidecar to persist core paragraph identities. That carrier is an extension and MUST be identified and tested. Without it, loss of paragraph identity is `review-semantics-loss` and requires refusal or authorization.

### 4.3 Proposal identity, provenance, and lifecycle

Reference Web Editor `Suggestion.id` maps to `sourceProposalId` and MAY map directly to core `id` when it is unique in the portable lineage. Otherwise a core identity is synthesized while the source identifier is retained.

The suggestion author's stable user identifier maps to core `creator`. `authoredAt` maps to `createdAt` when available. Reference Web Editor's separate saving user and `createdAt` value MAY be preserved in an extension; they MUST NOT silently replace the change author and authored time. `originalSuggestionId`, chain links, and split/join history do not create a core replacement relation.

Reference Web Editor suggestions in content map to core `pending`. Accepting or discarding normally removes their marker attachment, so this profile does not infer a retained `accepted` or `rejected` terminal record from absence. A mapping that materializes pending state to an accepted or rejected projection MUST use the core `materialized` action and requires authorization.

Every pending proposal receives the discard-all accepted-state fingerprint as `baseFingerprint`.

## 5. Reference-Web-Editor-to-core mapping

| Reference Web Editor source behavior | Core result | Additional requirement |
| --- | --- | --- |
| One insertion suggestion on text in one paragraph | `insert` | Discard removes exactly the marked content; accept retains it; payload includes exact text and effective formatting. |
| One deletion suggestion on text in one paragraph | `delete` | Discard restores exactly the marked content; accept removes it; the exact payload is available. |
| One attribute suggestion for a core property | `format` | Suggestion data exposes one exact `oldValue` and `newValue`, uniform over the range, and both projections agree. |
| One format suggestion replaying a command | `format` | All command parameters are stored and the adapter independently resolves them to complete effective core before/after values; replay must not depend on later content state. |
| One suggestion whose projections differ only by a paragraph boundary insertion | `paragraph-split` | Discard yields one paragraph; accept yields exactly two with the prescribed left/right text. |
| One suggestion whose projections differ only by removal of an adjacent paragraph boundary | `paragraph-merge` | Discard yields exactly two paragraphs; accept concatenates them exactly. |

Multiple core property changes MAY form one `format` proposal only when Reference Web Editor exposes them as one suggestion with one atomic accept/discard action and the adapter proves all before/after values. Separate attribute suggestions remain separate proposals.

Reference Web Editor's documented replacement example uses separate insertion and deletion suggestions. Adjacency, common author, shared time, marker order, `originalSuggestionId`, chain membership, or a UI description does not establish one atomic core `replace`. The pair MAY map as independent proposals only when the core pending-set rules remain valid; otherwise it is unsupported.

Multi-range suggestions, chained suggestions that must resolve as one entity, automatically merged nested suggestions, unsupported attributes, and custom command suggestions whose exact projections cannot be computed are outside equivalent mapping.

For co-located insertions, the adapter MAY synthesize `samePointOrder` from the pinned model's deterministic marker/range order only when accepting the set reproduces the observed Reference Web Editor projection. The synthesis MUST be reported with no impact.

## 6. Core-to-Reference-Web-Editor mapping

| Core proposal | Reference Web Editor result | Equivalent export condition |
| --- | --- | --- |
| `insert` | One insertion suggestion attached to the exact model point | Text, formatting, order, identity, and both projections survive save/reload. |
| `delete` | One deletion suggestion retaining the exact content | Discard restores and accept removes the exact payload after reload. |
| `format` | One attribute or format suggestion | One Reference Web Editor accept/discard action atomically applies every core change and stored data yields exact before/after values. |
| `paragraph-split` | One tracked model change with exact boundary projections | The suggestion remains a single independently resolvable unit and paragraph identity is carried or reported. |
| `paragraph-merge` | One tracked model change with exact boundary projections | Discard restores both paragraphs; accept concatenates exactly; identity is carried or reported. |

The adapter MUST create suggestion records and their content markers as one logical operation. It MUST await all asynchronous adapter and `PendingActions` work before reporting success. The declared persistence boundary MUST include save and reload of both marker-bearing editor data and suggestion metadata.

Reference Web Editor v48.3.1 supplies no documented atomic replacement carrier in this profile. Export of `replace` MUST refuse without mutation or, with explicit authorization, emit separate insertion and deletion suggestions and report loss of `proposal.kind`, `proposal.relations`, `resolution.atomicity`, and affected projections. The result is never equivalent.

If the configured editor automatically merges, splits, nests, or chains suggestions so that a core proposal identity, atomic boundary, or selective resolution changes, the adapter MUST prevent that behavior for the operation or refuse/roll back. Increasing suggestion granularity is an implementation technique, not evidence that the resulting mapping is equivalent.

## 7. Permitted no-impact adaptations

The following are permitted when the accepted state, mandatory proposal semantics, and both projections remain unchanged:

- coalescing or splitting model attribute runs with identical effective core values;
- synthesizing stable paragraph or proposal identities for source-absent values;
- deriving same-point order from deterministic model order verified by projection;
- normalizing timestamps while preserving their instants;
- translating Reference Web Editor `null` or absent basic-style attribute values to effective core `false` when the configured model semantics prove that equivalence; and
- using marker-to-data conversion, an application adapter, or load/save integration interchangeably when the same complete observed input and persistence result are obtained.

Every represented synthesis or normalization MUST be declared. Auto-joined suggestions, lost `originalSuggestionId` semantics, command replay with omitted parameters, dropped markers, or missing suggestion records are not no-impact adaptations.

## 8. Loss, refusal, and report bindings

At minimum, adapters MUST apply these classifications:

| Condition | Required fields and impact | Required behavior |
| --- | --- | --- |
| Replacement atomicity unavailable | `proposal.kind`, `proposal.relations`, `resolution.atomicity`; `review-semantics-loss` | Refuse, or emit authorized lossy paired suggestions. |
| Suggestion is multi-range, nested, chained, or auto-merged across core boundaries | Narrowest target/relation/atomicity fields; `review-semantics-loss` | Refuse unless a later profile version defines the construct. |
| Formatting command data or effective values unavailable | `proposal.payload` and projections; `review-semantics-loss` | Refuse; do not replay against later state and guess. |
| Marker exists without record, or record without required marker | `proposal.identity`, `proposal.target`, `mapping.persistence`; normally `invalid-input` or `persistence-failure` | Refuse or roll back. |
| Available author or authored time omitted | `proposal.provenance`; `optional-information-loss` | Require omission authorization. |
| Paragraph identity lacks a stable configured carrier | `acceptedState.paragraphIdentity`; `review-semantics-loss` | Refuse or require omission authorization. |
| Pending suggestion is accepted/discarded instead of preserved | `proposal.reviewState` and the selected projection; `review-semantics-loss` | Require prior `materialized` authorization. |
| Asynchronous save/reload loses or changes marker or record data | `mapping.persistence` plus affected fields | Report `persistence-failure`; residual editor/database divergence is `transaction-integrity-failure`. |

Every report MUST use the profile identifier and version above. `direction` MUST be `reference-web-editor-to-core` or `core-to-reference-web-editor`. `boundary` MUST identify the editor version, root, integration mode, data store, and whether save/reload is included. `inputRef` and `outputRef` MUST jointly bind editor data, suggestion metadata, configuration relevant to semantics, and any core artifact.

Profile stages are `version-check`, `model-load`, `base-projection`, `target-mapping`, `proposal-mapping`, `adapter-save`, and `save-reload`.

## 9. Direction-specific conformance

A conforming `reference-web-editor-to-core` adapter MUST verify v48.3.1 and the supported plugin configuration, bind markers to complete suggestion records, compute the discard-all accepted state, emit a conforming core document, and compare exact accept/discard projections for each claimed suggestion.

A conforming `core-to-reference-web-editor` adapter MUST validate the complete core input, create one native independently resolvable unit per claimed core proposal, await asynchronous persistence, reload both editor data and suggestion records, and verify exact projections and identity behavior. It MUST prevent or detect automatic suggestion joining or splitting that changes core semantics.

Passing a live-editor operation without save/reload does not support a persistence claim. Passing standalone integration does not imply real-time-collaboration conformance. Passing one Reference Web Editor release does not imply another.

## 10. Minimum profile fixtures

A claim MUST declare its direction, proposal-kind capabilities, and whether a `reference-web-editor-to-core` claim additionally covers source persistence. Fixtures are activated by `always`, by a declared proposal-kind capability, or by `source-persistence`. Every activated fixture MUST pass; `not-run` or an inapplicability assertion does not satisfy it. An unclaimed capability is not supported by the claim.

The fixture identifiers below are mirrored by the evaluation catalog. The profile text is normative if the catalog differs.

### 10.1 `reference-web-editor-to-core`

<!-- profile-matrix:reference-web-editor-to-core:start -->
| Fixture identifier | Activated by | Required observation |
| --- | --- | --- |
| `bound-source-core-report` | `always` | Editor data, suggestion records, semantic configuration, core output, profile, direction, and boundary are bound by the final report. |
| `accepted-formatting-booleans` | `always` | The discard-all state yields exact effective values for all four core formatting properties. |
| `stable-suggestion-identity` | `always` | A usable suggestion identity remains stable and truthful. |
| `synthesized-paragraph-identity` | `always` | Source-absent paragraph identity is synthesized stably and reported. |
| `format-command-missing-refusal` | `always` | A command-shaped suggestion with missing parameters is refused rather than replayed against later state. |
| `separate-replacement-shape` | `always` | Separate insertion and deletion suggestions are not promoted to atomic replacement. |
| `multi-range-refusal` | `always` | A multi-range suggestion outside the subset is refused without mutation. |
| `chained-refusal` | `always` | A chained suggestion outside the subset is refused without mutation. |
| `nested-refusal` | `always` | A nested suggestion outside the subset is refused without mutation. |
| `auto-joined-refusal` | `always` | An auto-joined suggestion that changes the core boundary is refused without mutation. |
| `marker-record-mismatch` | `always` | Marker and suggestion-record mismatch is detected and refused. |
| `insertion-non-bmp` | `insert` | An insertion suggestion with non-BMP text maps at valid UTF-16 boundaries. |
| `colocated-insertions` | `insert` | Co-located insertions have a verified deterministic order. |
| `deletion-non-bmp` | `delete` | A deletion suggestion with non-BMP text retains the exact payload and projections. |
| `format-bold` | `format` | A bold attribute suggestion has exact before and after values. |
| `format-italic` | `format` | An italic attribute suggestion has exact before and after values. |
| `format-underline` | `format` | An underline attribute suggestion has exact before and after values. |
| `format-strikethrough` | `format` | A strikethrough attribute suggestion has exact before and after values. |
| `format-command-complete` | `format` | A command-based format suggestion with complete parameters yields exact stable projections. |
| `paragraph-split` | `paragraph-split` | A paragraph split preserves exact projections and identity behavior. |
| `paragraph-merge` | `paragraph-merge` | A paragraph merge preserves exact projections and identity behavior. |
| `source-async-save-reload-success` | `source-persistence` | Editor data and suggestion records survive the claimed source save/reload boundary. |
| `source-async-clean-failure` | `source-persistence` | Source persistence failure leaves the authoritative boundary unchanged. |
| `source-async-rollback` | `source-persistence` | A failed source-persistence attempt fully restores editor and suggestion data. |
| `source-async-partial-persistence` | `source-persistence` | Residual editor/database divergence is detected as transaction-integrity failure. |
<!-- profile-matrix:reference-web-editor-to-core:end -->

### 10.2 `core-to-reference-web-editor`

Asynchronous native save/reload, rollback, and partial-persistence detection are mandatory in this direction.

<!-- profile-matrix:core-to-reference-web-editor:start -->
| Fixture identifier | Activated by | Required observation |
| --- | --- | --- |
| `core-input-validation` | `always` | Invalid core input is rejected before editor or suggestion-data mutation. |
| `bound-core-native-report` | `always` | Core input, editor data, suggestion records, configuration, profile, direction, and save/reload boundary are bound by the final report. |
| `accepted-formatting-booleans` | `always` | Accepted-state text retains all four effective formatting Booleans after reload. |
| `stable-export-identity-policy` | `always` | Core identities are carried by a declared model attribute or sidecar, or refused or omitted only under the required reported policy. |
| `core-replacement-policy` | `always` | A core replacement is refused or emitted only as an authorized, reported non-equivalent suggestion pair. |
| `auto-joined-output-detection` | `always` | Automatic joining or splitting that changes a core proposal boundary is prevented or detected and rolled back. |
| `marker-record-persistence` | `always` | Every emitted marker remains bound to its complete suggestion record after reload. |
| `native-save-reload-success` | `always` | Asynchronous editor and suggestion-data save/reload preserves the complete output boundary. |
| `native-clean-failure` | `always` | A failed asynchronous write leaves no output mutation. |
| `native-rollback` | `always` | A failure after attempted mutation fully restores editor and suggestion data. |
| `native-partial-persistence` | `always` | Residual editor/database divergence is detected as transaction-integrity failure and cannot support a passing conformance result. |
| `insertion-non-bmp` | `insert` | A core insertion with non-BMP text remains one exact insertion suggestion after reload. |
| `colocated-insertions` | `insert` | Co-located core insertions retain their explicit order after reload. |
| `deletion-non-bmp` | `delete` | A core deletion with non-BMP text remains exactly restorable after reload. |
| `format-bold` | `format` | A bold proposal remains one exact atomic formatting suggestion. |
| `format-italic` | `format` | An italic proposal remains one exact atomic formatting suggestion. |
| `format-underline` | `format` | An underline proposal remains one exact atomic formatting suggestion. |
| `format-strikethrough` | `format` | A strikethrough proposal remains one exact atomic formatting suggestion. |
| `format-multi-property-atomic` | `format` | One multi-property core format proposal remains one independently resolvable native unit. |
| `paragraph-split` | `paragraph-split` | A core split remains one exact independently resolvable paragraph-boundary suggestion. |
| `paragraph-merge` | `paragraph-merge` | A core merge remains one exact independently resolvable paragraph-boundary suggestion. |
<!-- profile-matrix:core-to-reference-web-editor:end -->

## 11. Informative implementation notes

An implementation may use `TrackChanges#getSuggestions({ skipNotAttached: true, toJSON: true })`, an application adapter, `TrackChangesData`, or direct pinned model APIs. These are recipes rather than requirements. The integration should preserve `originalSuggestionId` when Reference Web Editor splits a suggestion so author data remains correct, but that source lineage still does not create core replacement atomicity.

A live-model planning trace can begin with the existing suggestion records, markers and live ranges, model operations, accept/discard commands, projection generation, and persistence integration. For each claimed proposal kind, the adapter maps the core content fragment and atomic review unit to the smallest native suggestion and marker combination that preserves the required observations. When proposal A resolves, native operations can transform the live marker for a remaining proposal B. The adapter can read B's resulting attachment, convert it to the successor core target and fingerprint, and compare both projections, association and same-point ordering, identity, mapping reports, and persistence after reload. A new general remapping call is useful only when a demonstrated gap remains.

Native transformation is not proof by itself. Marker collapse, incompatible stickiness, automatic suggestion joining, or a persistence mismatch can change version 1 attachment or atomicity. Configuration, sidecar data, refusal, or rollback can address such a mismatch; blindly trusting the marker update cannot support an equivalent claim.
