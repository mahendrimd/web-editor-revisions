# Broad and compound proposal interaction in document review

Research artifact for [Assess review interaction for broad and compound proposals](../tickets/05-assess-review-interaction-for-broad-and-compound-proposals.md).

Observed and accessed: 2026-08-30

## Bounded question and decision impact

For multiline or multi-paragraph paste, broad deletion, and later editing that expands, shrinks, splits, or groups an already pending proposal, which user-visible review outcomes recur across representative document-review systems and human-factors evidence? How do those systems expose scope, granularity, grouping, preview, and accept/reject control, and which outcomes can Web Editor Revisions v1 represent?

This evidence can change whether [Clarify user-important document review mode](../changes/02-clarify-user-important-document-review-mode.md) needs only an informative boundary clarification, a semantic extension, a separate review-surface profile, or deferral for direct user research. It does not select that disposition.

## Scope and source classes

The released v1 baseline is inspected for paragraph state, targets, immutable proposal identity, proposal kinds, selective resolution, compatibility, and successor remapping. Representative product evidence covers:

- Google Docs' paragraph/index and suggestion model;
- Microsoft Word Track Changes review operations plus the released WordprocessingML profile;
- LibreOffice Writer recorded-change display and hierarchical change management; and
- the pinned Reference Web Editor boundary, supported by CKEditor 5 documentation for suggestion joining, tracking sessions, multi-range deletion, and accept/discard commands.

Human-factors evidence is the peer-reviewed accessible collaborative-writing study already curated for this effort and Microsoft Research's annotation-positioning studies. These sources support contextual comprehension and visible attachment failure but do not directly rank multiline paste or large deletion as requirements.

The stopping condition is met: all three named interaction classes have representative mechanism traces; user requirements below are distinguished as direct product facts or evidence-backed inferences; product contradictions in proposal grouping are preserved; and the v1 coverage boundary is stable enough to unblock the disposition decision.

## Compact coverage matrix

| Representative | Broad/compound mechanism | Scope and granularity exposed to reviewer | Contradiction or limit | V1 relationship |
| --- | --- | --- | --- | --- |
| Google Docs | Paragraphs end in newline characters; suggested insertion/deletion IDs attach to text and structural elements; nested suggested IDs can occur | Inline/accepted/rejected views expose alternative readings; suggestion identity can cover content represented across multiple elements | Current API details include Developer Preview behavior; user help does not document a universal split/partial-accept operation | Demonstrates broader structural suggestions than v1's paragraph-local independent proposals |
| Microsoft Word | Tracks insertions, deletions, formatting, and paragraph-mark changes; reviewers accept/reject one change, move sequentially, or act on all/all-shown changes | The selected change is contextualized by type; filters and next/previous support long review sets | UI-level “one change” need not equal one portable semantic record; technical markup can split a broad edit across run and paragraph-mark revisions | V1 maps only paragraph-local revisions and one adjacent paragraph boundary at a time; cross-paragraph inline revisions are refused |
| LibreOffice Writer | Deleted passages remain visible and crossed out; documentation explicitly gives an editor crossing out an entire paragraph; Manage Changes highlights the selected change and presents author-on-author edits hierarchically | Reviewer can inspect each change, navigate, filter a long list, expand hierarchy, and accept/reject the actionable level | The docs establish hierarchy and broad visible changes, not a universal atomic proposal definition | Supports transparent grouping and scope as a user concern; v1 has no proposal hierarchy or partial resolution within one proposal |
| Reference Web Editor / CKEditor | Adjacent suggestions by one user are automatically joined; editing next to a suggestion can expand it; tracking sessions prevent joining; custom features can create one multi-range deletion suggestion | Suggestion identity is the accept/discard unit; product offers per-suggestion, selected, and all-suggestion commands | Product granularity is configurable and may be multi-range or auto-joined; the v1 profile intentionally refuses those cases | Direct counterexample: ordinary native behavior can exceed v1's immutable, one-range, independent-proposal subset |
| HCI evidence | Contextual before/after presentation and where/what/who awareness; dense interleaved markup can overload readers | Supports seeing the whole decision effect in context and choosing a manageable presentation | Does not prove that every broad operation must remain one atomic proposal or that partial acceptance is mandatory | Supports outcome-level scope clarity and preview, not one serialization or UI method |

## Findings

### 1. What is important to the user

The evidence supports the following as **outcome-level review requirements**, not a prescribed widget or gesture.

1. **The full decision scope must be legible.** Before accepting or rejecting, the reviewer should be able to tell all content and boundaries affected by that decision. Word selects a contextual change and supports methodical next/previous review; LibreOffice highlights the selected change in the document and exposes hierarchy; Google provides alternate suggestion views; CKEditor binds accept/discard to suggestion identity. This is a strong inference from cross-product convergence.

2. **The visible action unit must match the actual resolution unit.** If one click accepts a whole paste, several ranges, or an entire paragraph deletion, the surface must not visually imply that only the currently visible line is affected. Conversely, if one authored operation has been split into several independently resolvable records, that split must not be hidden when it changes the outcomes a reviewer can choose.

3. **Broad destructive changes need contextual before/after understanding.** The accessible collaborative-writing study found contextual original/modified sentence presentation useful and found that dense announcements or markup can create cognitive overload. For a large deletion, this supports a preview or equivalent comprehension path showing both retained and removed readings, with enough surrounding structure to understand the effect. It does not prove one universal preview UI.

4. **Grouping and granularity must be predictable.** CKEditor documents automatic joining of adjacent suggestions, expansion when editing next to an existing suggestion, configurable tracking sessions that prevent joining, and native multi-range deletion. LibreOffice exposes author-on-author change hierarchy. These facts show that real systems group changes differently; reviewers need to know whether they are deciding one atomic proposal, a group, or several independent proposals.

5. **A reviewer must not accidentally widen a decision.** This is an evidence-backed safety inference: if later editing expands a pending deletion or insertion, the system should visibly preserve or re-identify the decision boundary. Silent expansion is risky because the accept/reject action now affects more content than the reviewer originally understood. The evidence supports visibility and predictable identity, but not one mandated policy of “always expand,” “always split,” or “always allocate a new proposal.”

6. **Unrepresentable or unstable scope should be surfaced, not guessed.** The annotation-positioning studies found that lost or wrongly repositioned annotations affect user trust and that visible orphaning can be preferable to plausible but incorrect placement. For content proposals, v1 already embodies the analogous rule: incompatible or unmappable targets are reported rather than fuzzily reattached.

### 2. Multiline paste

“Multiline” has two materially different meanings.

- **Soft line breaks or newline scalars inside one paragraph:** the core string rules do not prohibit U+000A, and a mapping profile may define a paragraph-local line-break mapping. Such an insertion can be one v1 `insert` only when it remains one paragraph's text and exact formatting coverage.
- **Hard paragraph breaks producing two or more paragraphs:** this is not one v1 insertion. V1 accepted state stores separate paragraphs; an insertion targets one point in one paragraph; one `paragraph-split` introduces exactly one boundary; pending proposals cannot target content introduced by another pending proposal; and dependent/overlapping proposals are excluded. An ordinary paste that atomically creates several paragraphs and inserts content on both sides of new boundaries generally cannot be represented as one equivalent v1 proposal or independent conforming set.

Representative systems do treat structural paste and multi-element suggestions as ordinary product behavior. Google Docs represents paragraphs as newline-terminated structural elements and exposes suggestion IDs on structural and inline elements. CKEditor track changes includes special handling for pasted table content and provides multi-range suggestion machinery. Product evidence therefore supports **multiline/structural paste as a real review scenario**, but not the normative claim that it must always be one proposal.

The user-important requirement is: the reviewer must see the full pasted structure and know whether accept/reject applies atomically to the whole paste, to separately reviewable pieces, or cannot be preserved. V1 currently cannot express the general atomic multi-paragraph case.

### 3. Broad pending deletion

- **Large deletion within one paragraph:** v1 can represent it. A `delete` range may span any non-empty amount of exact text inside one `paragraphId`; there is no length limit. The payload includes the entire deleted content and formatting, so rejection can restore it exactly.
- **Deletion of one paragraph boundary:** v1 can represent the boundary effect as one `paragraph-merge` proposal between two adjacent paragraphs.
- **Deletion spanning text across several paragraphs or several disjoint ranges:** v1 generally cannot represent it as one proposal. Range targets are paragraph-local, `paragraph-merge` handles one adjacent boundary, and multi-range/dependent proposal sets are excluded. The Reference Web Editor profile explicitly refuses native multi-range suggestions and cross-core-boundary auto-joining.

LibreOffice's example of crossing out an entire paragraph and Word's broad accept/reject controls show that large deletions are expected product operations. The evidence does not prove that a reviewer needs arbitrary partial acceptance inside every large deletion. It does support three requirements: expose the entire affected coverage, give a reliable before/after reading, and make the atomic decision boundary explicit.

### 4. Editing an already pending proposal

CKEditor provides the clearest direct mechanism trace: adjacent suggestions from the same user can be joined, typing next to an existing suggestion can expand it, and a new tracking session prevents later edits from joining the earlier suggestion. Its custom-feature API can also create one multi-range deletion suggestion.

V1 takes a different position. Proposal semantic identity is immutable: target, kind, and payload cannot materially change under the same identifier. A materially different edit needs a new identifier. But a new proposal that overlaps, nests, depends on, or targets content introduced by the earlier pending proposal is invalid in v1. Consequently, a native “keep deleting and expand the pending deletion” behavior often cannot map equivalently unless the adapter freezes native grouping, resolves/materializes first under authorization, or refuses the case.

This is not merely UI polish. It is a semantic coverage gap between a common native editing behavior and v1. Whether v2 should support mutable drafting lineage, compound proposal groups, or multi-range proposals is a normative question requiring more than an informative review-mode sentence.

## V1 coverage matrix

| Interaction outcome | V1 status | Consequence |
| --- | --- | --- |
| See exact content of a large one-paragraph insertion/deletion | Covered semantically by exact fragments and range payloads | UI presentation remains implementation-defined |
| Preview accepted and rejected reading for one supported proposal | Covered | Strong basis for review surfaces and evaluation |
| One hard paragraph insertion or deletion | Covered as split or merge | Exactly one adjacent boundary per proposal |
| Atomic multi-paragraph paste | Not generally expressible | Requires loss/refusal, materialization, or a future semantic extension |
| Atomic deletion spanning several paragraphs or disjoint ranges | Not expressible in the general case | Reference profile explicitly refuses multi-range/cross-boundary cases |
| Expand or shrink a pending proposal under the same identity | Prohibited when target/payload changes materially | Common native auto-joining can become non-equivalent |
| Proposal hierarchy or group with atomic parent and inspectable children | Not defined | LibreOffice/native grouping cannot be represented as portable review semantics |
| Partial accept/reject within one proposal | Not defined; proposal is atomic | Evidence does not yet establish this as a universal user requirement |
| Clearly expose scope, atomicity, and resulting reading | Supported by v1 semantics for in-scope proposals; UI unspecified | Strong candidate for informative review guidance or a review-surface profile |
| Surface incompatible/unmappable attachment instead of guessing | Covered | Aligns with user-trust evidence from annotation positioning |

## Direct answer to the expected-user-requirement question

Yes, **broad and compound change interaction is an expected review concern**, but the supported user requirement is not “multiline paste must be stored as one proposal” or “every large delete must allow partial acceptance.” The stronger evidence-backed requirement is:

> A review method should make the complete scope and atomic decision unit of a pending change understandable in document context, show or derive the accepted and rejected readings, keep grouping predictable as the proposal is edited, and visibly refuse or qualify cases whose scope cannot be preserved.

For multiline paste and wide deletion, users need to know exactly what one accept/reject action will affect. Whether the product groups the operation as one proposal, a visible proposal group, or several independent proposals legitimately varies. V1 handles the single-paragraph and single-boundary subset but does not handle general multi-paragraph, multi-range, hierarchical, or mutable-pending cases.

## Supporting and contradictory evidence

Supporting evidence includes convergence on contextual per-change decisions, alternate readings, navigation, hierarchy/filtering for large review sets, automatic/native grouping behavior, and HCI findings favoring before/after context. CKEditor provides direct evidence that expanding and multi-range suggestions are real mechanisms, not hypothetical edge cases.

Contradictory evidence is equally important:

- Systems disagree on grouping. CKEditor auto-joins by default but provides sessions to prevent joining; LibreOffice exposes hierarchy; Word presents contextual changes and batch actions; Google can associate suggestion IDs with multiple structural elements.
- Human-factors research supports comprehension, context, and manageable presentation but does not establish mandatory partial acceptance or one ideal granularity.
- A very large proposal may be easiest to understand as a unit when it expresses one intent, while the same visual size may conceal several unrelated intents. Size alone cannot define proposal boundaries.
- Splitting one authored atomic change can give reviewers flexibility but can also create invalid half-outcomes. Atomicity must come from declared intent and representable semantics, not a UI heuristic.

## Uncertainty, omissions, and source limitations

- Product documentation establishes current affordances and mechanisms, not a universal ranking of user preferences.
- No direct user study found in this bounded pass asks whether reviewers prefer one atomic multi-paragraph paste, automatically split proposals, or arbitrary partial acceptance of a large deletion.
- Google suggestion API details observed in 2026 include Developer Preview portions. They demonstrate representational breadth but are not a stable normative model.
- Microsoft and LibreOffice user documentation does not precisely define how one broad authored gesture is divided into internal revision identities.
- The accessible-writing study focuses on screen-reader users and sentence-level presentation; its overload finding should inform, not dictate, all review surfaces.

Direct interviews or usability tests would be required before standardizing a preferred grouping UI. They are not required to conclude that scope visibility, predictable atomicity, before/after comprehension, and safe refusal are important outcomes.

## Stopping rationale

The sample covers a cloud structural suggestion model, a mainstream tracked-revision workflow, an open-source hierarchical change manager, and the v1 live-editor profile's configurable joining/multi-range behavior. Each named case—structural paste, broad deletion, and pending-proposal reshaping—has a mechanism trace and a stable v1 coverage result. Further product sampling is unlikely to change the core distinction between outcome-level scope clarity and unresolved normative granularity policy.

## Implications and newly visible questions

The research supports separating two possible maintenance depths:

- A **core-preserving informative clarification** can state the outcome-level review requirements: complete scope visibility, explicit atomic decision unit, accepted/rejected reading, predictable grouping, and visible refusal.
- Support for **atomic multi-paragraph/multi-range proposals, proposal groups/hierarchy, or mutable pending proposal lineage** is a semantic extension, not merely review-mode guidance. It should be a separate accepted change item or future effort with direct feasibility and user-intent decisions.

The disposition decision should now choose whether this effort accepts only the informative boundary, expands scope to semantic proposal grouping, or defers the richer interaction pending direct user research.

## Source register

| Source | Observed/accessed | Evidence role | Principal limit |
| --- | --- | --- | --- |
| [Web Editor Revisions v1](../../../standards/v1/standard.md) | Released baseline; inspected 2026-08-30 | Exact core coverage and exclusions | No review UI or compound proposal model |
| [Reference Web Editor profile](../../../standards/v1/profiles/reference-web-editor.md) | Released baseline; inspected 2026-08-30 | Explicit multi-range, auto-join, and cross-boundary refusal | Narrow pinned subset |
| [WordprocessingML profile](../../../standards/v1/profiles/wordprocessingml.md) | Released baseline; inspected 2026-08-30 | Paragraph-local and one-boundary mapping limits | Not the complete Word product model |
| [Google Docs document structure](https://developers.google.com/workspace/docs/api/concepts/structure) | Accessed 2026-08-30 | Newline-terminated paragraphs and indexed structural model | API structure, not user-preference evidence |
| [Google Docs resource model](https://developers.google.com/workspace/docs/api/reference/rest/v1/documents) | Accessed 2026-08-30 | Suggested IDs on inline and structural elements, including nested suggestions | Some current features are Developer Preview |
| [Google Docs suggestion views](https://developers.google.com/workspace/docs/api/how-tos/suggestions) | Accessed 2026-08-30 | Inline/accepted/rejected readings | Programmatic boundary, not universal UI |
| [Microsoft Word accept/reject](https://support.microsoft.com/en-us/word/accept-or-reject-tracked-changes-in-word) | Accessed 2026-08-30 | Contextual per-change, next/previous, all/all-shown actions | Does not define internal grouping identity |
| [LibreOffice recording changes](https://help.libreoffice.org/latest/en-US/text/shared/guide/redlining.html) | Accessed 2026-08-30 | Entire-paragraph deletion example and final per-change review | Product help, not a controlled user study |
| [LibreOffice accepting/rejecting changes](https://help.libreoffice.org/latest/en-GB/text/shared/guide/redlining_accept.html) | Accessed 2026-08-30 | Highlighted selection, long-list filtering, and hierarchy | Does not define universal atomicity |
| [CKEditor suggestion granularity](https://ckeditor.com/docs/ckeditor5/latest/features/collaboration/track-changes/track-changes-granular-suggestions.html) | Accessed 2026-08-30 | Auto-joining, expansion, and tracking sessions | Hosted latest docs; exact integration is configurable |
| [CKEditor TrackChanges API](https://ckeditor.com/docs/ckeditor5/latest/api/module_track-changes_trackchanges-TrackChanges.html) | Accessed 2026-08-30 | Per-suggestion, selected, and all-suggestion commands | Product mechanism, not user preference |
| [CKEditor TrackChangesEditing API](https://ckeditor.com/docs/ckeditor5/latest/api/module_track-changes_trackchangesediting-TrackChangesEditing.html) | Accessed 2026-08-30 | Native multi-range deletion and joining behavior | Custom-feature API; outside v1 profile subset |
| [Das, Piper, and Gergle, accessible collaborative writing](https://doi.org/10.1145/3480169) | Published 2022; accessed 2026-08-30 | Contextual before/after comprehension and overload trade-off | Focused on 48 screen-reader users |
| [Brush et al., robust annotation positioning](https://www.microsoft.com/en-us/research/publication/robust-annotation-positioning-in-digital-documents/) | Published 2000; accessed 2026-08-30 | User expectations around lost/wrong attachment | Annotation evidence, not proposal granularity |
