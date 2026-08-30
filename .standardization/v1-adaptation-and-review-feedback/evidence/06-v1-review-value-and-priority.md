# V1 review value and capability priority

Research artifact for [Assess v1 review value and priority](../tickets/06-assess-v1-review-value-and-priority.md).

Observed and assessed: 2026-08-30

## Bounded question and method

This assessment asks whether the review interactions absent from Web Editor Revisions v1 make the standard provide little or no added value, and whether those interactions can be ranked by priority.

It reuses the released v1 baseline and the representative product and human-factors evidence already collected in [Document review-mode expectations and version 1 coverage](02-document-review-mode-expectations.md) and [Broad and compound proposal interaction in document review](05-broad-and-compound-review-interaction.md). It does not claim a population-level feature ranking: the available sources establish product convergence, semantic consequences, and review-safety concerns, but do not directly measure how many users prefer one grouping or partial-resolution policy.

Priority is therefore assigned using four bounded criteria:

1. **Review integrity:** can a reviewer understand and safely decide what accepting or rejecting changes?
2. **Scenario centrality:** does the interaction occur as ordinary editing behavior across representative document systems rather than as a specialist workflow?
3. **Interoperability consequence:** does omission cause silent ambiguity, forced materialization, splitting, refusal, or review-semantics loss across implementations?
4. **Layer fit:** is the need portable document-review semantics, an informative review-method expectation, or a product-specific UI/workflow choice?

## Priority scale

| Band | Meaning for this standard | Inclusion consequence |
| --- | --- | --- |
| **P0 — critical review integrity** | Without the capability, an implementation cannot truthfully expose a safe accept/reject decision or preserve the supported review state. | Must be normative for every claimed supported proposal, or the implementation must visibly refuse the claim. |
| **P1 — high-priority practical coverage** | The capability is common enough, and its loss consequential enough, that omission materially limits a claim to general-purpose document review. | May be absent from a deliberately bounded v1, but should be prominent in limitations and prioritized for a semantic extension or broader profile before making a general review-mode claim. |
| **P2 — useful review operation and triage** | The capability substantially improves comprehension or handling of many changes, but products legitimately vary and core interchange can still add value without standardizing one method. | Standardize an outcome only when evidence converges; otherwise use informative guidance or profiles. |
| **P3 — product workflow or presentation** | The capability belongs mainly to collaboration policy, discussion, access, or a particular surface. | Keep outside the portable core unless a separately scoped profile demonstrates interoperability need. |

The bands rank standardization urgency and claim impact. They are not a numerical user-preference survey and do not imply that every P1 interaction must be represented as one proposal.

## Ranked capability matrix

| Review capability | Evidence-backed reason | V1 coverage | Priority and consequence |
| --- | --- | --- | --- |
| Distinguish accepted content from pending changes in document context | Google Docs, Word, and LibreOffice all expose pending changes against a readable document | Semantic substrate covered; UI intentionally unspecified | **P0.** A review method using v1 must render or derive the distinction for supported proposals. |
| Explicitly accept or reject an independently reviewable proposal | Per-change accept/reject converges across all three representative document systems | Covered by proposal lifecycle and atomic resolution | **P0.** This is the defining review decision, not optional workflow polish. |
| Know the complete scope and atomic effect before deciding | Broad changes, hierarchy, auto-joining, and multi-range suggestions show that visible and actual action units can diverge | Exact target and payload cover supported proposals; no explicit review-method guidance | **P0.** Add informative clarification; unsupported scope must be qualified or refused rather than hidden. |
| Derive accepted and rejected readings | Google exposes alternate views; Word distinguishes hidden markup from actual resolution; human-factors evidence supports contextual before/after understanding | Covered normatively as acceptance and rejection projections | **P0.** V1 provides material value here even without prescribing a preview UI. |
| Preserve identity and attachment as accepted content changes, or surface failure | Stable decision identity and trustworthy attachment are prerequisites to acting on pending changes | Covered by immutable identity, deterministic successor remapping, preflight, and non-guessing failure | **P0.** A major interoperability contribution of v1. |
| Represent ordinary paragraph-local insert, delete, replace, and format proposals plus one paragraph split or merge | These are central document changes and establish a useful interoperable subset | Covered, subject to profile capabilities | **P0 for the declared subset.** This bounded subset is useful even though it is not complete editor coverage. |
| Represent one atomic multi-paragraph paste or structural insertion | Structural paste is ordinary authoring; Google suggestions span structural elements and editor models handle pasted structures | Not generally expressible | **P1.** Its absence does not erase v1 value, but prevents a credible unqualified general-purpose review-mode claim. |
| Represent one cross-paragraph or multi-range deletion | Word/LibreOffice expose broad deletions and CKEditor supports multi-range deletion; splitting may change atomic review intent | Not generally expressible | **P1.** Prioritize portable compound targeting or grouping semantics. |
| Preserve predictable grouping when later editing expands or reshapes a pending change | CKEditor can auto-join and expand suggestions; tracking sessions can instead freeze boundaries | Material change under one proposal identity is prohibited; overlapping/dependent replacements are excluded | **P1.** A future design must choose immutable groups, lineage, or another explicit policy; silent widening is unacceptable. |
| Represent proposal groups or hierarchy with an explicit parent/child resolution contract | LibreOffice exposes hierarchy; groups could preserve one authored intent while retaining inspectable pieces | Not defined | **P1 when needed to solve compound edits.** The exact group semantics remain a normative design question. |
| Navigate, filter, summarize, and batch-resolve a long review set | Common in Word and LibreOffice and helpful for scale | Individual and atomic set resolution are semantic; navigation/filter UI is unspecified | **P2.** Important usability guidance or profile work, but not necessary to prove core interchange value. |
| Preserve or expose attribution when available | Where/who/what awareness is useful; products differ in metadata guarantees | Core provenance is preserve-if-present | **P2.** Current treatment is defensible; do not invent missing attribution. |
| Partially accept arbitrary content inside one broad proposal | Could help reviewers isolate acceptable portions, but may violate authored atomic intent | Not defined; proposals are atomic | **P2 / unresolved.** Existing evidence does not justify making universal partial acceptance a P1 requirement. |
| Comments, discussion threads, reviewer permissions, approval gates, and prescribed visual layout | Common collaboration facilities but materially different across document and code review | Explicitly out of scope | **P3.** Their exclusion does not substantially reduce the value of the portable revision semantics. |

## Does v1 have little or no added value?

No—provided its claim remains bounded.

Version 1 standardizes guarantees that are independently valuable and difficult to recover after interchange: exact proposal payloads, accepted-state binding, stable identities, atomic acceptance/rejection projections, deterministic remapping of remaining proposals, compatibility checks, and explicit loss or refusal. These let two implementations agree on what a supported pending change means and what each decision produces. A product merely having a Track Changes UI does not create that cross-vendor contract.

The contrary conclusion becomes reasonable only if v1 is presented as a complete standard for a general-purpose review-mode editor. In that framing, ordinary multi-paragraph paste, broad cross-paragraph deletion, and continued editing around pending suggestions will frequently exceed the model. An implementation then has to split the user's intent, materialize it, refuse it, or report review-semantics loss. A standard that hid those limits would overstate its value.

The accurate value statement is therefore:

> V1 is a meaningful interoperability and review-integrity core for a deliberately bounded proposal subset. It is not yet a complete portable model for all ordinary document review-mode editing.

That is a narrower claim than “review mode is standardized,” but materially stronger than “v1 adds little or no value.”

## Disposition implications

The evidence supports a two-track disposition:

1. **Clarify v1 now:** describe the P0 outcome-level review contract—complete decision scope, explicit atomicity, accepted/rejected readings, stable attachment, and visible qualification or refusal—and state the bounded paragraph-local/single-boundary coverage plainly.
2. **Prioritize a separate semantic extension:** treat atomic multi-paragraph insertion, cross-paragraph or multi-range deletion, proposal groups/hierarchy, and pending-change reshaping as P1 design work. Do not smuggle these semantics into an informative patch.

This makes the current revision valuable without laundering known gaps. It also prevents lower-layer workflow features such as comments or approval gates from displacing the semantic P1 work that most affects portable review coverage.

## Contradictions and uncertainty

- Representative products establish that compound changes and grouping occur, but disagree on the unit: one suggestion may span structures, auto-join adjacent edits, expose hierarchy, or be split into technical revisions.
- A single large proposal may accurately preserve one authored intent; another equally large gesture may contain several independently reviewable intentions. Size alone cannot define atomicity.
- Direct user research would be needed to rank competing grouping interactions or to mandate partial acceptance. It is not needed to rank complete decision-scope visibility and safe failure as P0, or to identify compound structural proposals as a P1 coverage gap.
- Implementation feasibility and compatibility analysis are still required before selecting group, multi-target, or lineage semantics for a future version.

## Source basis

The detailed source register and limitations are preserved in [Document review-mode expectations and version 1 coverage](02-document-review-mode-expectations.md) and [Broad and compound proposal interaction in document review](05-broad-and-compound-review-interaction.md). The decisive baseline clauses are Sections 1, 3, 7–11, 14–16, and 18 of [Web Editor Revisions v1](../../../standards/v1/standard.md), especially the paragraph-local target model, immutable proposal identity, independent-proposal restriction, acceptance and rejection projections, deterministic pending-target remapping, profile-scoped claims, and explicit subset limitation.
