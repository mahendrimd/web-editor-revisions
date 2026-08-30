# Reconcile core review terminology

Type: decision
Phase: assessment
Status: resolved
Recorded by: project maintainer
Blocked by:
Decision status: active
Supersedes:
Superseded by:

## Question

Which normative terms and distinctions should the assessment use for a pending proposal, its change payload, the accepted document state, revision history, editing operations, undo/redo, annotations or comments, and accept/reject resolution so that evidence about different systems is compared without conflating unlike concepts?

## Resolution

### Decision

Use **revision proposal** as the canonical term for a lifecycle record representing a document change that is independently reviewable while pending. **Proposal** is its contextual shorthand. A retained revision proposal may have `pending`, `accepted`, or `rejected` state. The model permits implementations to remove terminal proposal records, so terminal-record retention is not required.

Use these distinct canonical terms:

- **change payload** — the implementation-independent semantic document mutation proposed by a revision proposal, excluding its identity, review state, provenance, target attachment, and comments;
- **accepted document state** — the currently authoritative document content against which pending revision proposals are interpreted;
- **acceptance projection** — the result or preview produced by accepting specified revision proposals;
- **rejection projection** — the result or preview produced by rejecting specified revision proposals;
- **proposal resolution** — the review decision that accepts or rejects a revision proposal and determines its document outcome;
- **edit operation** — a command or transformation applied by an editing system to change a document state;
- **revision history** — a chronological record of prior document versions or committed changes;
- **undo/redo history** — the editing-system record used to reverse or replay edit operations;
- **annotation** — a resource or record related to a document target that does not, by that relationship alone, define a document mutation or proposal-resolution behavior; and
- **comment** — human-readable discussion or explanation that does not itself define the proposed document mutation.

Use **accept** and **reject** as the canonical proposal-resolution actions. A vendor term such as *suggestion*, *tracked change*, *revision*, or *discard* is only a mapping alias where the vendor behavior matches the relevant canonical definition. The same spelling in different vendor systems does not establish semantic equivalence.

Terminal proposal retention and revision-history retention are separate concepts. The model must not infer that resolving a proposal stores it in document or version history, or that removing active revision markup erases every vendor-maintained history record.

### Rationale

The [normative-model comparison](../evidence.md) shows that “revision,” “change,” “history,” and “annotation” name materially different layers across OOXML, ODF, HTML, Input Events, and Web Annotation. Input Events history actions are transient editing intents, Web Annotation relates resources without defining document mutation or review resolution, and document formats use type-specific persistent revision structures.

The [Web-editor comparison](../evidence.md) shows the same distinction in the reviewed implementations. The cited Reference Web Editor, Google Docs, and Word models expose independently reviewable proposals with accept/reject behavior. The cited ProseMirror and Quill core models expose applied operations, collaboration, or undo/redo without native pending-proposal semantics. Similar visible outcomes therefore do not make proposal rejection, undo, operation refusal, or history restoration equivalent.

“Revision proposal” states the review purpose while avoiding the broadest overloads of “revision” and “change.” Separating authoritative content from acceptance and rejection projections prevents a current document state from being confused with a hypothetical resolved view. Allowing, but not requiring, terminal records accommodates materially different retention models without turning undocumented vendor history behavior into a common requirement.

### Rejected alternatives and trade-offs

- **Bare “revision” as the central term:** concise and familiar in office-document systems, but too easily confused with a saved version, history entry, edit operation, or vendor-specific tracked-change object.
- **“Suggestion” as the central term:** approachable and used by multiple products, but product-associated and liable to include non-mutating recommendations or discussion.
- **“Pending revision” as the lifecycle term:** accurately describes the unresolved state but becomes contradictory after a retained record is accepted or rejected.
- **“Tracked change” as the central term:** familiar to users, but can name a feature, a markup record, or any change captured by a vendor rather than the portable semantic record defined here.
- **“Baseline document state” instead of “accepted document state”:** avoids the word “accepted,” but can suggest an immutable historical snapshot rather than the authoritative content as review progresses.
- **Collapsing rejection into undo or operation refusal:** may resemble the same visible document result in a narrow case, but loses reviewer intent, proposal identity, and the distinction between review and synchronization or local editing history.
- **Requiring terminal proposal retention:** improves auditability but exceeds the common evidence and would exclude representations that materialize the result and remove active revision marks.

### Supporting and contradictory evidence

Supporting evidence includes three independently documented review systems with proposal identity and explicit resolution behavior, plus recurring distinctions between persistent proposal data, transient editing events, document history, comments or annotations, and accepted/rejected materializations.

Contradictory evidence prevents treating this vocabulary as universal native editor architecture. ProseMirror and Quill do not expose native review proposals in the sampled core models; vendor systems use overlapping terms with different behavior; Google exposes retained suggestion status while Word evidence shows acceptance removing revision marks. These differences support a neutral vocabulary and adapter aliases rather than assuming identical storage or lifecycle semantics.

### Uncertainty and assumptions

- The decision does not establish whether Google, Word, or any other vendor preserves a resolved or removed proposal in version history unless a mapping profile supplies direct evidence.
- The decision permits but does not require retention of terminal proposal records. Auditability and retention requirements remain available for later normative decision if the conformance model needs them.
- Exact proposal metadata, target attachment, change-payload kinds, grouping, nesting, and serialization remain unresolved.
- Vendor aliases are behavioral mappings, not global synonyms; profiles must document mismatches and loss.

### Follow-up work now made expressible

- Use the accepted vocabulary in the text-subset feasibility assessment and minimal conformance experiment.
- Test proposal identity and pending/accepted/rejected outcomes independently from revision-history or undo/redo preservation.
- Require future vendor mapping profiles to distinguish proposal retention from external version-history retention and to document terminology mismatches.

The accepted definitions and boundary scenarios are maintained in the [terminology ledger](../standard.md#4-terminology).
