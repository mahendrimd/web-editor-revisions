# Define loss reporting and conformance outcomes

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 10, 12
Decision status: active
Supersedes:
Superseded by:

## Question

Which adapter outcomes, loss categories, affected semantic fields, severity or recoverability distinctions, and equivalence claims must v1 define so unsupported or partial mappings cannot be mistaken for preserved revision semantics?

## Resolution

### Decision

V1 separates the outcome of one mapping operation from conformance with the standard. A conforming adapter may accurately report a limited capability or a deliberately authorized lossy result; reporting loss never turns that result into semantic equivalence. Silent or misleading loss, an outcome inconsistent with the observable result, missing required reporting, an unauthorized lossy mutation, or a broken transaction guarantee is nonconforming.

Every mapping operation has exactly one of five closed overall outcomes, derived from its observable output and issue records rather than selected at the adapter's discretion:

- **`equivalent`** — the operation completed with valid output; all applicable v1 semantics and preserve-if-present information survived; and no reportable adaptation or loss occurred.
- **`equivalent-with-declared-adaptation`** — the operation completed with valid output; every change was a permitted and declared synthesis or normalization; every issue has `impact: none`; and all mandatory pending-state observations, identities after permitted synthesis, targets, payloads, relations, lifecycle states, and accept/reject projections remain semantically equivalent. The adaptation must remain stable across the exact boundary for which equivalence is claimed.
- **`lossy`** — the operation completed with valid usable output under an explicit caller policy, but source information or review semantics were omitted, approximated, materialized, or otherwise changed. Accurate reporting and authorization may make the operation conforming, but never equivalent.
- **`unsupported`** — no output mutation occurred because the adapter's declared capability or the caller's authorized policy was insufficient for the input semantics.
- **`failed`** — no valid result completed because the input was invalid, a safety precondition failed, execution failed, or the intended result did not survive the declared persistence boundary. A clean refusal or rollback can be a conforming failure. Residual mutation is a transaction-integrity failure and remains nonconforming even when accurately reported.

Overall outcomes aggregate deterministically. Any transaction-integrity failure produces `failed`. An operation that commits valid but non-equivalent output produces `lossy`; an operation that refuses without mutation produces `unsupported`. `Equivalent-with-declared-adaptation` is available only when every issue has no semantic impact, and `equivalent` only when there is neither adaptation nor loss. An adapter cannot use a successful result for one proposal, direction, fixture, or stage to mask another issue or claim blanket support.

Every reportable condition is a structured issue rather than one combined loss label. Each issue records its mapping stage, affected proposal identities when applicable, affected semantic fields, condition, adapter action, impact, recoverability, and any applicable extension identifier. It also records enough expected and observed disposition to reproduce the classification. The core condition values are:

- **`source-absent`** — the source model genuinely has no corresponding value or relation; this is not an access or read failure.
- **`unsupported`** — the adapter recognizes the semantic but cannot process or represent it within its declared capability.
- **`unavailable`** — the value should or may exist, but the adapter cannot retrieve, recover, or verify it.
- **`invalid-input`** — the input violates an applicable source, mapping-profile, or v1 invariant.
- **`precondition-failed`** — otherwise valid input cannot safely be applied to the verified current state, including a base-state mismatch or unresolved target precondition.
- **`persistence-failure`** — the intended result did not survive the declared save, reload, import/export, or other persistence boundary.
- **`other`** — a condition outside the core vocabulary, accompanied by a namespaced extension identifier and definition.

The core adapter-action values are:

- **`synthesized`** — the adapter created a portable value without asserting that the value came from the source. A synthesized identity, ordering relation, or other core value must satisfy its normal v1 invariants and declared stability boundary.
- **`normalized`** — the adapter changed only a representation detail explicitly permitted by v1 or the applicable mapping profile, without changing semantic observations or projections.
- **`approximated`** — the adapter substituted non-equivalent data or behavior.
- **`omitted`** — the adapter did not carry affected source information or semantics into the result.
- **`materialized`** — the adapter converted pending review state into a selected accepted or rejected document projection instead of preserving it as pending.
- **`refused`** — the adapter made no output mutation for the affected operation.
- **`rolled-back`** — the adapter attempted a mutation and fully reversed it, leaving the output boundary unchanged.
- **`partially-committed`** — an incomplete operation left residual mutation at the output boundary. This always has transaction-integrity impact.
- **`other`** — an action outside the core vocabulary, accompanied by a namespaced extension identifier and definition.

Impact is a closed objective classification, not a policy-relative `low`, `medium`, or `high` severity:

- **`none`** — no v1 semantic observation, projection, or preserve-if-present value changed; this is the only impact permitted by an equivalence-with-adaptation claim.
- **`optional-information-loss`** — a source value that v1 makes optional to originate but preserve-if-present was lost, such as available provenance, while mandatory review behavior remains intact.
- **`review-semantics-loss`** — a mandatory v1 field, relation, lifecycle fact, target, payload, identity guarantee, or possible accept/reject outcome changed or became unavailable.
- **`transaction-integrity-failure`** — the operation left partial, unverifiable, or otherwise non-atomic mutation across its declared boundary.

Recoverability is recorded independently:

- **`not-applicable`** — no corrective action is required, normally because impact is `none`.
- **`retryable`** — the same authoritative request can be safely attempted again after the stated transient or environmental condition is corrected.
- **`requires-intervention`** — recovery needs additional source data, repair, policy authorization, user judgment, or an adapter or profile change.
- **`irrecoverable`** — exact affected semantics cannot be reconstructed within the declared boundary from the retained information.
- **`unknown`** — the implementation cannot establish whether or how recovery is possible.

Recoverability never upgrades the current operation's outcome. A later successful attempt receives its own report and outcome.

Affected fields use stable semantic model names, not JSON paths, XML paths, object layouts, or another serialization-specific syntax. The field vocabulary covers at least accepted paragraph order, paragraph identity, exact text, core formatting coverage, and accepted-state fingerprint; proposal identity, base reference, target, kind, payload, same-point order and other normative relations, review state, preserve-if-present provenance, and retained-terminal-record completeness; selective-resolution atomicity, accepted and rejected projections, and pending-target remapping; and mapping persistence and transaction integrity. An issue identifies the narrowest affected field or fields and proposal identities that reproduce its outcome. The canonical-serialization decision will define their lexical encoding without changing these semantic distinctions.

Lossy actions, including approximation, omission, and materialization, require matching caller authorization before output mutation. Authorization may be supplied by an API option, mapping profile, or configured policy; v1 does not require an interactive prompt or constrain UI. If the adapter discovers semantic loss not covered by the caller's policy, it refuses or fully rolls back. Permitted no-impact synthesis and normalization require declaration but not special loss authorization. For example, a stable portable proposal identifier synthesized for a source proposal that has no identity may be an equivalent declared adaptation; splitting one atomic replacement into independently resolvable deletion and insertion proposals is review-semantics loss even when declared.

Every operation produces a final machine-readable report bound unambiguously to the exact input and any output, mapping direction, operation stage or persistence boundary, and adapter and mapping-profile identity and version. The report contains the derived overall outcome and its structured issues. Input and output semantic fingerprints or equivalently strong references bind the report to the observed states; their lexical representation remains for the canonical serialization. Human-readable explanations may accompany but cannot replace the machine-readable report. A preflight prediction does not replace the final report because execution and persistence may introduce additional issues. An output without its required bound report cannot support an equivalence claim.

Equivalence claims are limited to the named operation, direction, profile and version, input and output, and measured mapping or persistence boundary. They are not generic claims that an adapter or format “supports the standard.” Overall and issue-level results coexist: one affected proposal or mandatory field downgrades the complete operation while the issue records preserve the unaffected detail.

The five overall outcomes and four impact classes are closed for v1 so independent implementations can derive comparable results. Condition and action extensions are allowed through namespaced identifiers, but every extension issue still supplies a core condition or `other`, a core action or `other`, affected semantic fields, a core impact, recoverability, and its effect on the overall outcome. An unknown extension cannot conceal loss or support `impact: none` unless v1 or the applicable mapping profile defines it as a permitted no-impact adaptation.

### Rationale

The standardization aim is not met if an adapter preserves visible text while silently discarding pending review state, atomic grouping, identity, or a rejection projection. Separating mapping outcome from conformance lets narrow adapters participate truthfully: refusing an unsupported structural proposal or producing an explicitly authorized accepted-content projection can be useful behavior without being mislabeled as preservation.

The provisional conformance experiment's combined labels mix causes, transformations, effects, and results. A source-absent identity that is synthesized stably has a different semantic consequence from source metadata that disappears during persistence, even though both involve a field not present at the final boundary. Structured dimensions make this distinction testable and allow one controlled vocabulary to cover identity synthesis, harmless run normalization, unavailable deleted payloads, lost replacement relations, unsupported paragraph structure, and partial native persistence.

Objective impact and recoverability are more portable than a severity scale. The importance of author provenance or an accepted-content fallback varies by adopter policy, but whether a mandatory projection changed and whether exact data can be recovered are observable. Binding each report to a precise direction and boundary also prevents an import success from implying export or round-trip equivalence.

Explicit authorization preserves valid projection workflows without making them accidental fallback. A caller that intentionally wants accepted content may authorize materialization. A caller seeking pending-review portability receives refusal rather than a document whose visible text survived while its review state silently vanished.

### Rejected alternatives and trade-offs

- **Treat every lossy or unsupported result as nonconforming:** makes conformance synonymous with universal feature support and excludes honest limited adapters. Conformance instead requires correct behavior and truthful classification for the declared capability.
- **Treat explicit reporting as sufficient for equivalence:** erases the distinction the effort exists to protect. Reporting makes loss visible; it never repairs changed review semantics.
- **Use only the provisional flat labels such as `relation-lost`, `structural-loss`, and `partial-persistence`:** is compact but conflates why an issue arose, what the adapter did, which field changed, and whether recovery is possible. Structured axes retain those facts compositionally.
- **Use subjective severity levels:** allows the same loss to be rated differently by products and cannot drive deterministic fixtures. Objective impact and separate recoverability allow adopters to apply their own severity policy afterward.
- **Classify every synthesis as loss:** would mark a source-absent identity as non-equivalent even when the synthesized identity is stable and all review outcomes are preserved. Permitted declared synthesis is a no-impact adaptation.
- **Allow any declared transformation under equivalence:** would let a report legitimize lost atomicity, target changes, or altered projections. Only transformations explicitly permitted by v1 or a profile and proven to have no semantic impact qualify.
- **Let adapters self-select an overall label:** encourages optimistic classification and prevents reproducible tests. The overall outcome is derived from mutation, issue impact, and transaction completion.
- **Permit lossy mutation by default:** supports convenient fallback but recreates the documented risk that pending revisions become ordinary content without the caller asking. Lossy actions require prior policy authorization.
- **Require an interactive confirmation UI:** would constrain editor and batch-tool architecture. Authorization is semantic and may be supplied programmatically or by policy.
- **Allow a human-readable warning without a bound machine report:** is hard to preserve, aggregate, or test and can become detached from an artifact. Human text remains supplementary.
- **Make every vocabulary permanently closed:** would prevent profiles from describing new adapter mechanisms. Extension details are permitted while closed outcomes and impacts preserve interoperability.
- **Use serialization-specific affected paths:** couples the semantic decision to a technology not yet selected and makes equivalent encodings report different fields. Stable semantic field names keep the report independent of JSON, XML, or binary layout.

### Supporting and contradictory evidence

The [minimal conformance experiment](../evaluation/README.md) already distinguishes equivalent, equivalent with permitted normalization, lossy, unsupported, and invalid results; binds loss to fixtures, proposals, stages, and semantic aspects; and treats silent loss as invalid. Its boundary fixtures demonstrate source-absent identity, unavailable deleted payload, lost replacement grouping, bounded-formatting loss, structural loss, harmless run normalization, and partial persistence. This decision retains those observations while separating condition, action, impact, recoverability, operation outcome, and conformance.

[Proposal identity, metadata, and lifecycle](10-define-proposal-identity-metadata-and-lifecycle.md) requires reporting synthesized or colliding identity, provenance omission or redaction, fingerprint mismatch, unmappable targets, partial persistence, and incomplete terminal records. It also establishes that source-absent identity may be synthesized and that processing failures are not review states. [Content-change and resolution semantics](12-define-content-change-and-resolution-semantics.md) requires transaction-wide preflight and rollback on mismatched payloads, absent ordering, ambiguity, or failed pending-target remapping. Those decisions supply the affected fields and make transaction-integrity failure materially different from ordinary semantic loss.

The [portability need and timeliness evidence](../evidence.md) documents the central risk: visible content may survive while suggestions, author mapping, or pending review state do not. It also shows that accepted-content projections are legitimate when deliberately requested, supporting authorized materialization rather than a universal prohibition. The [text-subset feasibility evidence](../evidence.md) identifies unavailable deletion payloads, source-absent identity and provenance, unsupported atomic replacement, structural mismatch, and partial persistence as concrete mapping boundaries.

Contradictory evidence prevents the report from assuming that every difference is loss. Native run segmentation, source identity availability, provenance, persistence topology, and proposal representation vary widely, and several reviewed sources do not originate all portable fields. Existing adapters and accepted-content tools can satisfy workflows that do not require pending review state. No sampled standard or implementation supplies the complete structured outcome vocabulary adopted here, and no current cross-vendor fixture corpus establishes how frequently each outcome occurs. The vocabulary is therefore a vendor-neutral conformance contract to be tested, not a claim that existing products already emit equivalent reports.

### Uncertainty, assumptions, and follow-ups

- [Compare canonical serialization candidates](../evidence.md#serialization-alternatives-considered) and [Choose the canonical serialization](15-choose-canonical-serialization.md) must encode overall outcomes, issue records, semantic field identifiers, extension identifiers, adapter/profile versioning, and input/output bindings deterministically.
- [Build executable conformance fixtures](../evaluation/README.md#core-evaluation) must derive outcomes rather than trust adapter labels and cover each core condition, action, impact, and recoverability value; stable synthesized identity; permitted normalization; optional provenance loss; unavailable payload; lost replacement atomicity; authorized materialization; refusal without mutation; rollback; and partial commit.
- [Choose initial mapping profiles](17-choose-initial-mapping-profiles.md) must define profile-specific permitted no-impact adaptations, capability and direction claims, authorization-relevant lossy actions, and which native boundaries are measured.
- The standard may define a registry or maintenance policy for semantic field names and extension identifiers during synthesis without reopening these distinctions. Unknown extension details remain unable to conceal their core impact.
- The decision assumes a mapping operation can identify its authoritative input and declared output boundary. A failure that prevents any report is observable nonconformance, not a sixth outcome.
- The decision does not assign adopter-specific business severity, mandate a UI, require universal format support, or promise recovery merely because an issue is marked retryable or requires intervention.
- No new ticket is required: the existing serialization, fixture, and profile tickets cover the newly expressible follow-up work. No prior decision is superseded.
