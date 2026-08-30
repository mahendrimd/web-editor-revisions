# Define review-mode clarification content

Type: task
Phase: resolution
Status: resolved
Claimed by: /root
Blocked by: 04

## Completion criterion

Identify the exact baseline sections, P0 review-integrity claims, bounded paragraph-local and single-boundary coverage statement, document-versus-code-review boundary, candidate evaluation checks, and confirmed patch compatibility effect for [Clarify user-important document review mode](../changes/02-clarify-user-important-document-review-mode.md), while keeping compound semantics deferred and avoiding a prescribed UI or workflow.

## Resolution

### Exact candidate placement

The candidate should make only informative or supporting-material changes in these locations:

1. **`standard.md`, Section 3, Scope:** add an explicitly labeled informative subsection after Section 3.2. It should explain the document review-method outcomes that the released semantics support, distinguish that semantic contract from a prescribed review UI, and state the document-versus-code-review boundary.
2. **`standard.md`, Section 18, Limitations and reassessment triggers:** expand the existing subset limitation with the exact paragraph-local and single-boundary coverage statement and the high-priority compound cases that version 1 cannot represent generally.
3. **`README.md`, publication summary and Known limits:** position the publication as a meaningful review-interoperability core for a bounded proposal subset, not a complete general-purpose review-mode editor contract.
4. **`evaluation/README.md`, after Interpreting a core result:** add an explicitly informative review-method inspection checklist and one supported/one unsupported scenario. Passing these human-facing checks must not become a new conformance claim.
5. **`evidence.md`:** update the evidence snapshot date and add a concise evidence-to-publication row covering document-review outcomes, the code-review distinction, and the limits of product-convergence evidence.

No normative schema, serialization, target, proposal kind, resolution, remapping, mapping-outcome, profile capability, or fixture activation should change. No profile text is required for this item: existing direction-specific matrices already determine whether a native proposal is equivalent, lossy, unsupported, or failed. The generated site should reflect the accepted successor publication; no separate site-only semantic wording is authorized.

### P0 review-integrity claims

The informative scope subsection should state that a document review method using version 1's supported subset has enough portable semantics to help a reviewer:

1. distinguish the accepted document state from pending proposed changes in document context;
2. identify the complete target, payload, and atomic decision unit affected by accepting or rejecting a supported proposal;
3. inspect or derive the acceptance and rejection projections rather than confusing hidden markup with resolved content;
4. keep proposal identity and semantic attachment stable as other proposals resolve, or surface an incompatibility or unavailable target instead of guessing; and
5. understand when an operation cannot be preserved as equivalent and has instead been refused, materialized, or reported as lossy.

These are user-facing interpretations of existing Sections 5 and 7 through 15. They do not require a particular inline rendering, preview control, navigation queue, filter, accessibility presentation, or gesture. Attribution remains preserve-if-present and useful rather than a new P0 mandatory field.

The text should not claim a statistical ranking of user preferences. It may describe these outcomes as recurring across representative document-review systems and necessary to understand a supported accept/reject decision, while leaving presentation variation explicit.

### Bounded coverage statement

The candidate must say plainly:

- Version 1's point and range targets apply within one accepted paragraph; its paragraph-boundary target covers one adjacent boundary.
- It can represent paragraph-local insertion, deletion, replacement, and formatting proposals, including a large range within one paragraph, plus one paragraph split or merge, subject to the selected profile's capability claim.
- It does not generally represent one atomic paste that creates or spans several paragraphs, one deletion covering several paragraphs or disjoint ranges, proposal groups or hierarchy, overlapping or dependent proposals, or material expansion or shrinkage of a pending proposal under the same identity.
- Splitting one compound authored operation into independent proposals is not automatically equivalent because it can create independently resolvable outcomes that the source did not permit.
- Arbitrary partial acceptance within one proposal is not defined; one version 1 proposal is the atomic review unit.
- These limits do not erase the value of the exact identity, projection, remapping, persistence, and loss guarantees for the supported subset. They do prevent an unqualified claim that version 1 completely standardizes general-purpose document review mode.

The wording should distinguish hard paragraph structure from a line-break scalar that a profile may map within one paragraph. It must not incorrectly state that every string containing a newline is necessarily a compound proposal.

### Document-versus-code-review boundary

The informative scope subsection should distinguish the semantic objects:

- **Document proposal resolution** decides whether a pending in-document content mutation becomes part of the accepted document and defines the resulting accepted or rejected projection.
- **Code review** ordinarily evaluates a branch, commit, or patch for integration and may include review-level approval, request-changes status, comments, CI results, mergeability, repository policy, and later commits.

Contextual comparison, targeted discussion, and re-review are useful analogies, but a code-review approval is not acceptance of each document proposal, and a resolved comment is not a content projection. The candidate must not import merge gates, approvals, comments, or repository workflow into the portable document core.

### Informative evaluation scenarios and checks

The evaluation guide should include two compact scenarios:

- **Supported broad deletion:** one deletion covers a large exact range within one paragraph. An inspector can identify the complete range and payload, derive both projections, confirm one atomic accept/reject unit, and verify the attachment or truthful failure of remaining proposals.
- **Unsupported compound paste:** one authored operation atomically introduces content across multiple new paragraphs. An implementation must not present a split, materialized, or refused result as an equivalent single version 1 proposal; the review method should disclose the changed decision boundary or mapping outcome.

Candidate validation must additionally confirm:

1. The new core subsection and evaluation checklist are explicitly informative and contain no new RFC 2119/8174 keyword or equivalent obligation.
2. Every P0 claim traces to an existing target, identity, lifecycle, projection, remapping, mapping-outcome, or conformance rule.
3. The supported and unsupported examples match the exact paragraph-local, one-boundary, independent-proposal model; they do not imply compound semantics or universal partial acceptance.
4. No passage claims that v1 conformance proves a usable review UI, accessibility presentation, user preference, market adoption, or complete round-trip support for an upstream product.
5. The document-versus-code comparison remains a boundary explanation and does not redefine `proposal`, `resolution`, `annotation`, `comment`, or `reviewState`.
6. The schema, serialization fixtures, `profile-requirements.json`, marked profile matrices, and profile-claim schema remain byte-for-byte unchanged unless the item returns to Assessment.
7. The existing core suite, profile catalog check, and profile self-test pass unchanged.
8. Site generation and verification present the same bounded claim as the canonical candidate and do not shorten it into an unqualified “review mode standardized” message.

### Compatibility effect

The confirmed provisional classification remains **patch**. The candidate will clarify the purpose, human-facing interpretation, and known limits of already released semantics. It will not alter valid documents, semantic observations, resolution results, mapping classifications, conformance roles, or previously conforming behavior.

If synthesis adds a normative review-surface recommendation, changes a conformance or profile claim, or attempts to define compound targets, grouping, hierarchy, mutable pending identity, or partial acceptance, [Clarify user-important document review mode](../changes/02-clarify-user-important-document-review-mode.md) must return to Assessment. A normative review recommendation requires at least minor classification; incompatible compound semantics may require major classification.
