# Choose the document review-mode disposition

Type: decision
Phase: assessment
Status: resolved
Claimed by: /root
Blocked by: 02, 05, 06
Decision status: active
Supersedes:
Superseded by:

## Question

Should this revision accept a core-preserving clarification that version 1 supplies the portable semantic substrate for document review but does not standardize a review-mode UI or workflow, open a broader normative review-surface effort, defer pending direct user-preference research, or reject the report because the existing purpose and exclusions are already sufficiently clear; and what provisional compatibility classification follows from that chosen depth?

## Resolution

### Decision

Accept [Clarify user-important document review mode](../changes/02-clarify-user-important-document-review-mode.md) for a core-preserving informative clarification, with provisional **patch** classification. The successor should explain the P0 review-integrity outcomes supplied by version 1 for supported proposals: a legible distinction between accepted and pending content, the complete scope and atomic effect of an accept/reject decision, derivable accepted and rejected readings, stable identity and attachment across resolution, and visible qualification or refusal when scope cannot be preserved. It should also state plainly that version 1 covers a deliberately bounded paragraph-local and single-boundary proposal subset rather than a complete general-purpose review-mode editor.

Record atomic multi-paragraph paste, cross-paragraph or multi-range deletion, proposal grouping or hierarchy, and predictable reshaping of pending changes as the separate high-priority normative follow-up [Extend portable review semantics for compound structural changes](../changes/03-extend-portable-review-semantics-for-compound-structural-changes.md). Defer that item from the current patch because its stable semantics and compatibility design are not yet resolved. Treat its future impact as provisionally **major** until a later effort proves that an optional capability, extension, or independently versioned profile preserves every previously conforming use.

Do not standardize arbitrary partial acceptance within every broad proposal in the current work. Existing evidence does not establish that as a universal user requirement, and splitting one authored atomic intent may itself create invalid intermediate outcomes.

The overall Assessment verdict is **standardize a subset**: proceed with the two stable informative clarifications and defer the compound semantic extension without dismissing its priority.

Accepted by the project maintainer on 2026-08-30.

### Rationale

[Document review-mode expectations and version 1 coverage](../evidence/02-document-review-mode-expectations.md) shows cross-product convergence on contextual pending-change visibility, explicit accept/reject decisions, and comprehensible resulting readings. [Broad and compound proposal interaction in document review](../evidence/05-broad-and-compound-review-interaction.md) shows that complete scope and atomicity are user-relevant safety concerns and that ordinary native behavior can exceed version 1's independent paragraph-local model. [V1 review value and capability priority](../evidence/06-v1-review-value-and-priority.md) distinguishes those concerns by standards priority.

Version 1 retains material value because it standardizes exact payloads and targets, stable proposal identity, accepted-state binding, atomic projections, deterministic successor remapping, compatibility checks, and truthful loss or refusal. These guarantees provide a cross-vendor review contract for the supported subset that a product's Track Changes UI does not supply by itself.

The missing compound interactions nevertheless prevent an unqualified claim that version 1 completely standardizes document review mode. Representative systems support structural suggestions, broad deletions, hierarchy, multi-range changes, or automatic suggestion joining. Treating these as merely UI-level exclusions would hide material semantic loss. Separating the patch clarification from a future normative extension preserves the stable v1 core while giving the most consequential coverage gaps explicit priority.

### Rejected alternatives and trade-offs

- **Make only an informative clarification and leave compound changes as undifferentiated out of scope:** would preserve a small patch, but would understate that ordinary editing behavior can require splitting, materialization, refusal, or review-semantics loss. The accepted decision instead records a named, high-priority normative follow-up.
- **Expand the current patch to define compound proposals immediately:** would address more scenarios sooner, but proposal grouping, parent/child atomicity, target representation, lineage, profile mappings, and compatibility have not been resolved. Adding them without that work would be premature and incompatible with patch classification.
- **Conclude that version 1 has little or no value:** correctly emphasizes practical coverage gaps, but ignores the independently useful and evaluable interoperability guarantees already provided for the supported subset.
- **Claim that version 1 already standardizes general-purpose review mode:** would overstate coverage and make ordinary compound edits appear conforming when adapters must actually refuse, materialize, or report loss.
- **Defer all review-mode clarification pending direct preference studies:** would avoid inferred priorities, but direct research is not needed to establish complete decision-scope visibility, explicit accept/reject outcomes, safe attachment, and truthful refusal as review-integrity requirements.
- **Import code-review approvals, comments, merge gates, or a prescribed UI into the core:** would conflate proposal resolution with branch integration and expand the standard into divergent product workflow and presentation concerns.
- **Require partial acceptance of every broad proposal:** could increase reviewer flexibility, but may destroy one authored atomic intent. The current evidence does not establish a universal policy.

### Supporting and contradictory evidence

Supporting evidence includes Google Docs' inline and alternate suggestion readings, Word's contextual per-change and batch review, LibreOffice's broad deletion and hierarchical change management, CKEditor's suggestion joining, tracking-session boundaries, and multi-range deletion, and human-factors evidence favoring contextual before/after comprehension and trustworthy attachment behavior. The released core already defines the P0 semantic basis for its supported subset.

Contradictory evidence constrains the decision. Products disagree on whether related edits auto-join, remain separate, form a hierarchy, or span multiple structural elements. Human-factors evidence does not establish one ideal grouping policy or universal partial acceptance. Dense markup can also increase cognitive load, so complete scope visibility must be an outcome rather than a prescribed presentation.

### Uncertainty and assumptions

- The priority scale ranks standardization urgency from product convergence, review safety, interoperability consequences, and layer fit; it is not a population-level user-preference survey.
- The exact compound model remains unresolved. A future effort must compare immutable proposal groups, multi-target proposals, lineage, and other designs against representative vendor mechanisms and atomic projections.
- The current patch classification assumes the candidate adds no normative recommendation or conformance obligation. Any such effect returns this item to Assessment and requires at least minor classification.
- The compound follow-up is provisionally major because it may change core parsing, validation, proposal compatibility, or resolution semantics. A later compatibility design may justify a lower classification under the configured version policy.

### Follow-up work now made expressible

- [Define mechanism-aware clarification content](07-define-mechanism-aware-clarification-content.md) will identify the minimum durable informative sequence and worked mechanism traces for the accepted adaptation item.
- [Define review-mode clarification content](08-define-review-mode-clarification-content.md) will identify the exact P0 claims, bounded-coverage statement, affected material, and compatibility effect for the accepted review item.
- The deferred compound change must begin a later linked revision or expansion assessment before candidate synthesis. That effort should settle compound targeting or grouping, atomic parent/child resolution, pending-edit evolution, mapping feasibility, and compatibility before drafting clauses.
