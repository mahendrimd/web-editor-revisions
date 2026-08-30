# Mechanism-aware vendor adaptation in version 1

Research artifact for [Determine whether v1 guides mechanism-aware vendor adaptation](../tickets/01-determine-whether-v1-guides-mechanism-aware-vendor-adaptation.md).

Observed and accessed: 2026-08-30

## Bounded question and decision impact

Across the Web Editor Revisions v1 core, its three mapping profiles, their conformance fixtures, and primary documentation for the profiles' pinned native boundaries, what does an adapter actually need to implement for content fragments, proposal kinds, accept/reject resolution, and successor-target behavior? Which requirements are observable-equivalence obligations rather than requirements for new calls or storage primitives, and where is the implementation-planning guidance too weak to prevent an agent from prescribing redundant machinery?

The answer can change whether [Ground adaptation plans in existing vendor mechanisms](../changes/01-ground-adaptation-plans-in-existing-vendor-mechanisms.md) becomes a core clarification, profile or implementation guidance, an evaluation addition, or no release change. This artifact describes facts and implications; it does not choose the normative disposition.

## Scope, source classes, and stopping condition

The released baseline is the immutable `web-editor-revisions-v1` tag at commit `e6ac89287257646888a4eadf692d836eb8feb41b`. The primary baseline sources are Sections 1, 3, 9–11, 14–15, and 18 of [the core](../../../standards/v1/standard.md), the three [mapping profiles](../../../standards/v1/profiles/), and their direction-specific fixture matrices.

Primary upstream source classes are:

- ECMA-376 and Microsoft Open XML documentation for Strict WordprocessingML revision elements and programmatic revision acceptance;
- OASIS OpenDocument 1.4 for tracked-change regions, records, and marks; and
- CKEditor 5 v48.3.1 release provenance plus CKEditor documentation for suggestions, markers, live positions, commands, projection generation, and persistence integration. The v1 profile uses the neutral name “Reference Web Editor” for this pinned boundary.

The stopping condition is met. Each of the six profile directions has a representative native mechanism trace. The successor-remapping example is tested against a live model with an existing transformation base and against the two declarative file-format models. The remaining uncertainty concerns where to place planning guidance, not whether the existing mechanisms can be identified.

## Coverage matrix

| Representative and direction | Existing native base | Proposal/content adaptation | Resolution and successor behavior | What v1 requires | Principal limit |
| --- | --- | --- | --- | --- | --- |
| WordprocessingML → core | Strict package tree; `w:ins`, `w:del`, `w:rPrChange`, paragraph-mark revisions, run/style cascade | Reconstruct reject-all accepted paragraphs, exact changed content, effective formatting, and per-record identity; normalize runs only when effective values are unchanged | Import reads the result of native revision markup; no native “core remap” API is required | Exact projections, core target/payload validity, and truthful refusal for unsupported relations | No required carrier for portable paragraph identity; no native atomic replacement relation in the profile |
| Core → WordprocessingML | The same tracked-revision elements and package serializer; an Open XML SDK or XML library is optional | Emit the applicable native record around already serialized accepted content | A resolver may update core first and re-export remaining proposals, or a native API/tree transform may accept/reject markup; save/reload must prove the successor | Observable projections, identities where supportable, complete rollback, and persistence—not a named SDK call | Multiple independent proposals can be unrepresentable; run/tree mutation alone does not prove semantic attachment |
| ODF Text → core | `text:tracked-changes`, one typed child per `text:changed-region`, `xml:id`, and change marks | Reconstruct reject-all state from insertion/deletion/format records and their marks; map only exact supported text and effective values | Import derives targets from the current authoritative package; no live remapping service exists or is required | Exact reconstruction and refusal when values or marks are ambiguous | Bare `text:format-change` omits the formatting delta; replacement has no atomic native relation |
| Core → ODF Text | The same change regions and start/end/point marks in an ODF package | Emit native insertion/deletion and supported paragraph-boundary tracking; use declared `xml:id` adaptations | Resolve in core and regenerate the package, or mutate native regions and reconstruct the remaining marks; independently reopen and verify | Exact projections, mark/identity behavior, rollback, and persistence—not a new ODF remap primitive | Core format and atomic replace require refusal or a separately versioned extension |
| Reference Web Editor → core | Suggestion records, content markers/live ranges, model operations, track-changes commands, `TrackChangesData`, and a persistence adapter | Reconstruct the discard-all state, pair suggestion records with markers, and derive exact typed payloads/projections | Existing live ranges update as model operations change the document; import samples the resulting authoritative attachment | Bind editor data plus suggestion data, preserve exact projections/identity, detect automatic merge/split/chain changes | Native grouping and command replay may not match core atomicity or complete before/after values |
| Core → Reference Web Editor | Native track-changes commands, one suggestion plus marker range, live-position operation transforms, and adapter/save-reload integration | Load accepted content first, then create one native independently resolvable suggestion for each supported core proposal | Use native accept/discard and its operation/live-range transformation base; read back remaining markers into successor core targets and verify association/order | Resulting state and attachment must match v1; the standard does not require a separate `remapTargets()` call | Stickiness, automatic suggestion joining, persistence timing, and unsupported replacement may require configuration, sidecar data, or refusal |

## Findings

### Direct baseline facts

1. **V1 standardizes portable observations, not vendor architecture.** The purpose says it standardizes portable data and observable outcomes and does not standardize UI, runtime data structures, collaboration algorithms, or private storage. Section 11 explicitly permits markers, operations, eager transformation, lazy transformation, or another algorithm when the resulting accepted state and pending targets are identical. This is direct evidence that “successor target remapping” is not a mandated new vendor call or subsystem.

2. **Content fragments and proposal kinds are mapping obligations, not instructions to reproduce the core object model inside a vendor.** Each profile maps exact content and supported proposal semantics to the vendor's existing constructs. WordprocessingML uses revision elements and run properties; ODF uses typed change regions and marks; Reference Web Editor uses suggestion records, markers, commands, and projections. The adapter may normalize, synthesize a stable value, or use a sidecar only within the declared adaptation and loss rules.

3. **The profiles already distinguish native support, bounded adaptation, and real gaps.** Examples include synthesizing identity or insertion order when the result is stable and projection-equivalent; refusing ODF formatting because its bare record lacks exact before/after values; and refusing or reporting loss for atomic replacement when the native system exposes only separate insertion and deletion records. This means an adaptation plan should not start from “implement every core kind natively.” It should start from the profile capability boundary.

4. **Conformance tests outcomes and boundaries, not implementation recipes.** Both native-to-core and core-to-native fixture matrices require exact projections, persistence, rollback, identity behavior, and explicit refusal or loss. The WordprocessingML and ODF informative notes say implementations may use a library, direct XML processing, or an application API. Microsoft documents Open XML SDK code for accepting WordprocessingML revisions, but the v1 profile correctly treats SDK class names and accept-all code as recipes rather than requirements ([Microsoft Open XML revision acceptance](https://learn.microsoft.com/en-us/office/open-xml/word/how-to-accept-all-revisions-in-a-word-processing-document)).

### Native mechanism traces

#### WordprocessingML

The v1 profile's source mapping reads supported `w:ins`, `w:del`, `w:rPrChange`, and paragraph-mark revisions into core insertion, deletion, formatting, split, and merge proposals. Its reverse mapping emits those same constructs around accepted content. Microsoft describes WordprocessingML as a document/body/paragraph/run/text tree and supplies an SDK implementation for accepting revision elements; this confirms that an implementation can leverage an XML tree or typed SDK rather than invent a portable-model-shaped native store ([Microsoft Open XML revision acceptance](https://learn.microsoft.com/en-us/office/open-xml/word/how-to-accept-all-revisions-in-a-word-processing-document)).

The native format does not supply the core's paragraph lineage identity or atomic replacement relation. Those are demonstrated gaps, so v1 requires a declared extension/sidecar, authorized loss, or refusal. That is materially different from adding a general remapping engine merely because Section 11 names a successor obligation.

#### ODF Text

ODF 1.4 defines each `text:changed-region` with one insertion, deletion, or format-change child and uses change marks referencing the region's `xml:id` to locate the changed content ([OASIS OpenDocument 1.4 Part 3](https://docs.oasis-open.org/office/OpenDocument/v1.4/os/part3-schema/OpenDocument-v1.4-os-part3-schema.html#element-text_changed-region)). The v1 profile reuses those constructs in both directions. An adapter reconstructs the reject-all state and derives core targets from the marks, or emits records and marks from core content.

This mechanism has real semantic holes: ODF states that a format-change record does not contain the change itself, so exact core before/after formatting cannot be recovered from that record alone; ODF also lacks the selected atomic replacement relation. V1's refusal/extension rules are therefore evidence-based additions at the boundary, not duplicated native machinery.

#### Reference Web Editor / CKEditor 5

CKEditor track changes already provides suggestions that users accept or discard, serialized suggestion boundary markup, commands, and accepted/discarded data projections ([track changes overview](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes.html), [projection generation](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-data.html)). Its integration guide provides load/save and adapter modes, asynchronous persistence, and `PendingActions`; it also warns that accepting or discarding a suggestion does not fire an adapter event because the change remains undoable during the session ([integration guide](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-integration.html)).

Most importantly for the reported example, CKEditor markers are live ranges whose ranges update automatically when the document changes. Operation-managed markers participate in undo and collaboration ([Marker API](https://ckeditor.com/docs/ckeditor5/latest/api/module_engine_model_markercollection-Marker.html)). Its `LivePosition` transforms through model operations and explicitly handles insertion, deletion, merge, and split effects ([LivePosition API](https://ckeditor.com/docs/ckeditor5/latest/api/module_engine_model_liveposition-LivePosition.html)). This is an existing transformation base for successor attachment. A mechanism-aware plan should first test whether suggestion markers and their stickiness/order reproduce v1's exact association and `samePointOrder` rules, then reuse them. It should add sidecar metadata or explicit transforms only for a proven mismatch.

### Successor-remapping example tested against the mechanisms

Consider pending proposal B attached after a point while proposal A at or before that point is accepted.

- **In the portable core**, Section 11 specifies the required successor observation: later offsets shift, same-point association and explicit order settle the boundary, identity remains stable, and an attachment swallowed by deletion is not guessed.
- **In Reference Web Editor**, accepting A executes existing model operations. The marker/live-range base transforms B's attachment as those operations apply. The adapter's job is to configure or interpret stickiness/order, read the resulting marker attachment, convert it back to the successor core target/fingerprint, and compare the observation with Section 11. A new “remap all pending proposals” call is justified only if the native transform cannot express a required boundary and no existing marker/sidecar composition can do so.
- **In WordprocessingML or ODF**, there is no persistent live-coordinate service to call. A resolver can update the portable accepted state and regenerate all remaining native revision records, or it can mutate the package tree using existing XML/application mechanisms and reconstruct the remaining marks against the successor. In either case, the v1 obligation is proven by reopened package projections and reconstructed targets. Asking the format for a nonexistent generic remap API misunderstands the mechanism boundary.

The counterexample matters: a live range is not automatically conforming. If a deletion causes the native marker to collapse or attach heuristically where v1 requires an unmappable outcome, or if automatic suggestion merging changes proposal identity/atomicity, the adapter must detect the mismatch and refuse, roll back, configure native behavior, or use a declared additional carrier. “Reuse first” is not “trust native behavior without verification.”

## Where version 1 is already sufficient

V1 already provides the semantic facts needed to reject the reported bad plan:

- the core is vendor-neutral and implementation-algorithm agnostic;
- mappings are profile- and direction-specific;
- all six profile directions identify native constructs or bounded refusal;
- successor target behavior is an observable invariant;
- projection and persistence checks are the proof boundary; and
- unsupported native concepts use extension, reported loss, or refusal rather than mandatory reinvention.

An agent that prescribes a new remapping call without inspecting markers, operations, package markup, tree transforms, or the selected adapter boundary is not following the baseline's architecture-neutral requirements.

## Where implementation-planning guidance is weak

The weakness is discoverability and planning method, not the semantic model. V1 distributes the relevant facts across the core's architecture disclaimer, Section 11's algorithm freedom, each profile's mapping tables, permitted adaptations, loss tables, fixture matrices, and short implementation notes. It never gives an adapter planner an explicit reuse-first sequence or asks a plan to name the existing host mechanism before proposing new machinery.

That omission can plausibly cause an AI agent to translate each capitalized outcome into a new implementation step—“call successor remapping,” “store a content fragment object,” or “implement replacement”—instead of asking which native construct already yields the observation. The baseline also lacks a worked trace showing how a live marker transform or package reserialization discharges Section 11.

## Evidence-backed planning sequence (informative implication)

The evidence supports evaluating, but does not by itself normatively select, this reusable planning sequence:

1. Identify the claimed profile, direction, version, source/output boundary, and persistence boundary.
2. Inventory the host's existing authoritative mechanisms: native change records, model operations, markers/live positions, projection APIs, serializers, save/reload integration, and sidecars.
3. Map each accepted-state fragment and claimed proposal kind to an existing native unit; record unsupported kinds rather than designing them away.
4. Identify which native operation performs accept/reject and which existing transform or reconstruction yields the successor attachment of every remaining pending proposal.
5. Compare the native result with the core's exact accepted/rejected projections, identity, association/order, and unmappable-target rules.
6. Add configuration, a sidecar, or adapter-local transformation only for the smallest demonstrated mismatch; otherwise reuse the native mechanism.
7. Reopen/reload the declared boundary and bind the observed output to the final mapping report. Refuse or roll back when equivalence cannot be proven.

This sequence would make “leverage the base already there” operational without standardizing private architecture.

## Supporting and contradictory evidence

Supporting evidence is strong: the core explicitly permits multiple algorithms; every profile maps to native constructs; the fixture model tests observations; CKEditor exposes an actual live transformation base; and the file-format profiles intentionally rely on reconstruction and reserialization rather than a live API.

Contradictory and qualifying evidence prevents a blanket “native mechanisms are enough” conclusion:

- WordprocessingML and ODF lack a native atomic replacement relation in the profiled subsets.
- ODF's format-change record lacks enough information for exact core formatting reversal.
- CKEditor may merge, split, nest, or chain suggestions in ways that change core identity or atomicity; command replay can be state-dependent unless all parameters are retained.
- A native marker can move deterministically yet still use the wrong association or collapse behavior for v1.
- Stable paragraph identity and portable `samePointOrder` may require a sidecar or declared synthesis even when content tracking is native.

The correct planning rule is therefore “inventory and leverage, then prove,” not “always reuse” and not “always build.”

## Uncertainty, omissions, and source limitations

- The repository contains normative profiles and fixtures, not live adapter implementations. This research establishes an implementation-planning boundary; it does not prove that a particular codebase already wires every native mechanism correctly.
- CKEditor documentation reviewed on 2026-08-30 describes the current v48.3.1 line and the official v48.3.1 release is identifiable, but hosted documentation is moving. The released v1 profile remains authoritative for the pinned claim; a live implementation should inspect the exact installed source and configuration.
- ECMA-376 and ODF define formats, not one required library or application behavior. A library may expose convenient transforms or only XML primitives.
- The example tests representative insertion/attachment behavior conceptually. Exact conformance still requires fixtures for every claimed kind, association, collision order, split, merge, deletion conflict, rollback, and save/reload boundary.

Evidence would change the implication if a selected vendor implementation had no stable authoritative change model to inspect, if its existing transformation base could not be observed or configured, or if a worked adapter showed that a new general remapping layer is consistently simpler and more reliable than native transform/reconstruction across the complete claimed boundary.

## Stopping rationale

The three profiles cover a declarative XML revision model with rich run markup, a second declarative model with known under-specification and semantic gaps, and a live editor model with native suggestions and automatic position transformation. Both directions are traced for each. The reported successor example has been examined where an existing transformation base is explicit and where no live base exists. Further vendor sampling would add mechanisms but is unlikely to change the disposition boundary: v1 semantics are already architecture-neutral, while explicit reuse-first planning guidance is missing.

## Newly visible questions and justified follow-up recommendations

No new ticket is created by this research task. The orchestrator should consider:

- **Decision follow-up:** decide whether to add a core-preserving informative adapter-planning rule, profile-specific worked traces, conformance-plan documentation, or no release change.
- **Task follow-up if guidance is accepted:** add a mechanism-inventory and reuse/proof checklist, plus one live-marker and one declarative-package remapping trace. Avoid naming a required method or internal subsystem.
- **Evaluation follow-up if behavior is uncertain:** add or sharpen fixtures that distinguish correct native transformation from silent marker collapse, auto-merged proposal identity, and guessed attachment after deletion.
- **Research follow-up only for a concrete adopter:** inspect the actual target codebase and installed vendor version to identify its authoritative markers/operations or package mutation pipeline before producing an adaptation plan.

## Source register

| Source | Observed/accessed | Evidence role | Principal limit |
| --- | --- | --- | --- |
| [Web Editor Revisions v1 core](../../../standards/v1/standard.md) | Released baseline; inspected 2026-08-30 | Architecture boundary, portable semantics, remapping freedom, conformance | Does not prescribe an implementation plan |
| [WordprocessingML profile](../../../standards/v1/profiles/wordprocessingml.md) | Released baseline; inspected 2026-08-30 | Direction-specific native mappings, adaptations, refusals, fixtures | Profile subset is narrower than all Word/ECMA behavior |
| [ODF Text profile](../../../standards/v1/profiles/odf-text.md) | Released baseline; inspected 2026-08-30 | Direction-specific native mappings, known format gaps, fixtures | Profile subset and exact ODF 1.4 boundary only |
| [Reference Web Editor profile](../../../standards/v1/profiles/reference-web-editor.md) | Released baseline; inspected 2026-08-30 | Direction-specific suggestion/marker mappings and persistence | Pinned vendor behavior is narrower than every CKEditor configuration |
| [OASIS OpenDocument 1.4 Part 3](https://docs.oasis-open.org/office/OpenDocument/v1.4/os/part3-schema/OpenDocument-v1.4-os-part3-schema.html) | OASIS Standard 2025-10-06; accessed 2026-08-30 | Authoritative ODF tracked-change records and marks | Format standard, not application implementation behavior |
| [ECMA-376](https://ecma-international.org/publications-and-standards/standards/ecma-376/) | Fifth edition baseline; accessed 2026-08-30 | Authoritative WordprocessingML vocabulary boundary | Large multipart standard; vendor application behavior is separate |
| [Microsoft Open XML revision acceptance](https://learn.microsoft.com/en-us/office/open-xml/word/how-to-accept-all-revisions-in-a-word-processing-document) | Updated 2025-05-12; accessed 2026-08-30 | Official example of leveraging SDK/tree mechanisms | Accept-all recipe; not selective-resolution or profile-conformance proof |
| [CKEditor track changes overview](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes.html) | Accessed 2026-08-30 | Suggestions, marks, commands, and preview boundary | Hosted latest documentation moves over time |
| [CKEditor track changes integration](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-integration.html) | Accessed 2026-08-30 | Adapter/save behavior, asynchronous persistence, accept/discard caveat | Application integration choices vary |
| [CKEditor accepted/discarded projection data](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-data.html) | Accessed 2026-08-30 | Existing projection mechanism | Temporary-editor method may require application configuration |
| [CKEditor Marker API](https://ckeditor.com/docs/ckeditor5/latest/api/module_engine_model_markercollection-Marker.html) | Accessed 2026-08-30 | Automatic live-range update and operation-managed markers | Generic model mechanism; exact suggestion configuration still must be inspected |
| [CKEditor LivePosition API](https://ckeditor.com/docs/ckeditor5/latest/api/module_engine_model_liveposition-LivePosition.html) | Accessed 2026-08-30 | Operation-based insert/delete/split/merge position transformation | Native transformation does not by itself prove v1 association semantics |
| [CKEditor 5 v48.3.1 release](https://github.com/ckeditor/ckeditor5/releases/tag/v48.3.1) | Released 2026-07-14; accessed 2026-08-30 | Pinned-version provenance | Release note is not detailed API documentation |
