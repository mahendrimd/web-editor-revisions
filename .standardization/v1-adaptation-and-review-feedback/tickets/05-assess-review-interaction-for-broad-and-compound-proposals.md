# Assess review interaction for broad and compound proposals

Type: research
Phase: assessment
Status: resolved
Claimed by: /root
Blocked by:

## Question

For multiline or multi-paragraph paste, broad deletion, and user edits that expand, shrink, split, or otherwise reshape an already pending document proposal, which user-visible review outcomes are supported by representative document-review systems and human-factors evidence; how do those systems expose scope, granularity, grouping, preview, and accept/reject control; and which of those outcomes can Web Editor Revisions v1 represent, deliberately excludes, or cannot express? The result can change whether the review-mode report needs only an informative boundary clarification, a normative semantic extension, a separate review-surface profile, or deferral for direct user research. Use primary documentation for at least three materially different document-review systems, the released v1 baseline, and high-trust human-factors evidence where available. Stop when the three named interaction classes have representative mechanism traces, each claimed user requirement is directly sourced or labeled as inference, contradictions in grouping/granularity are preserved, and a stable v1 coverage matrix can unblock the disposition decision.

## Resolution

Resolved by [Broad and compound proposal interaction in document review](../evidence/05-broad-and-compound-review-interaction.md).

The evidence supports complete scope visibility, an explicit atomic decision unit, contextual accepted/rejected readings, predictable grouping as edits accumulate, and visible refusal when scope cannot be preserved as important user-facing review outcomes. It does not establish a universal requirement that multiline paste remain one proposal or that every wide deletion allow arbitrary partial acceptance.

Version 1 handles a large insertion or deletion within one paragraph, and one paragraph split or merge, but not general atomic multi-paragraph paste, cross-paragraph or multi-range deletion, proposal hierarchy, or material expansion/shrinkage of one pending proposal under the same identity. CKEditor directly demonstrates native auto-joining, suggestion expansion, tracking-session boundaries, and multi-range deletion; Google exposes suggestion identity across structural elements; LibreOffice exposes broad deleted passages and hierarchical edits; and Word exposes contextual per-change and batch review. These are ordinary review concerns, not hypothetical edge cases.

The research recommends distinguishing an informative review-method clarification from a semantic extension. Informative guidance can require that a reviewer understand the complete scope and atomic resolution effect. Portable support for multi-paragraph/multi-range proposals, groups/hierarchy, or mutable pending lineage would require a separate normative change item or future effort and additional feasibility and human-intent decisions.
