# Assess document review-mode expectations and v1 coverage

Type: research
Phase: discovery
Status: resolved
Claimed by: /root/review_mode_research
Blocked by:

## Question

For users reviewing text-focused documents, which user-visible outcomes are consistently important across representative document-review systems; how do those outcomes differ materially from code-editor or pull-request review; and for each outcome does Web Editor Revisions v1 cover it, deliberately exclude it, or leave its relationship ambiguous? The result can change the standard's aim, limitations, examples, evaluation method, or the disposition of this report. Use the released baseline, primary documentation for representative document-review and code-review systems, and high-trust human-factors evidence where available. Preserve contradictions between systems rather than averaging them into one workflow. Stop when the evidence covers at least three materially different document-review systems and two code-review systems, every claimed user-important outcome has a source or is labeled an inference, and the v1 coverage matrix is stable enough to support an assessment decision.

## Resolution

Resolved by [Document review-mode expectations and version 1 coverage](../evidence/02-document-review-mode-expectations.md).

The evidence covers Google Docs Suggesting, Microsoft Word Track Changes, and LibreOffice Writer Track Changes as materially different document-review systems; GitHub pull-request review and GitLab merge-request review as code-review comparators; and high-trust human-factors research on accessible collaborative writing, annotation anchoring, and collaborative-writing practice.

Across the document systems, the strongest recurring user-visible outcomes are: distinguish pending content from the current accepted reading in context; inspect what changed and available attribution; explicitly accept or reject an individual change or compatible set; observe the resulting accepted/rejected reading; and keep a change attached to the intended content or surface an attachment failure. Navigation, filtering, grouping, comments, permissions, notifications, and accessibility presentation vary materially and are not a universal core workflow.

Version 1 covers the portable semantic substrate for these outcomes: accepted state, typed proposal payloads, stable identity, exact acceptance/rejection projections, deterministic successor remapping, and mapping/persistence reporting. It deliberately excludes the user-facing review UI, comments/discussion, permissions, workflow policy, and accessibility presentation; attribution is preserve-if-present rather than mandatory. The code-review comparison is useful only as a boundary: repository review adds patch/branch context, tests, mergeability, approval rules, and integration gates, so a code-review approval or suggestion is not equivalent to a document proposal resolution.

This research does not select the change item's disposition. It recommends a decision follow-up on whether to add a core-preserving informative review-mode boundary and projection/remapping evaluation guidance, a profile/implementation-guidance addition, or a separate UI/review-profile effort. A direct user study is justified only if the decision requires preference evidence rather than specification-scope evidence.
