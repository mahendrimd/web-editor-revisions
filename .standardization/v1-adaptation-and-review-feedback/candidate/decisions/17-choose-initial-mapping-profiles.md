# Choose initial mapping profiles

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 12, 13, 15
Decision status: active
Supersedes:
Superseded by:

## Question

Which representative document formats or Web-editor models should receive the first mapping profiles, which profile clauses should be normative or informative, and what maintenance boundary keeps vendor change from destabilizing the core?

## Resolution

### Decision

The first mapping-profile set is a balanced trio:

1. WordprocessingML tracked revisions;
2. ODF Text change tracking; and
3. Reference Web Editor Track Changes.

Each is a normative semantic mapping profile limited to the accepted v1 subset. A profile normatively defines its pinned upstream source boundary, supported source subset, mapping direction, source-to-core and core-to-source mappings where feasible, required preconditions, permitted no-impact adaptations, lossy or unsupported cases, report bindings, and direction-specific conformance expectations. API recipes, code examples, product-integration instructions, explanatory examples, and treatment of capabilities outside the v1 subset are informative.

Profiles describe both import and export wherever the pinned source model makes a direction meaningful. Conformance claims are independent by profile, profile version, direction, and measured mapping or persistence boundary. An adapter may conform for import, export, or both and need not implement every initial profile. No profile may turn direction-specific evidence into a blanket format, product, or adapter-support claim.

Every profile has a version independent of the core semantic-model and canonical-serialization versions and pins an identifiable upstream specification edition or documented product-model snapshot. A published claim remains interpretable against that pin even after its upstream source changes. An upstream change updates or supersedes only the affected profile. It does not silently change the core, another profile, or an earlier conformance claim.

A profile cannot redefine core identity, targets, operations, projections, lifecycle, loss outcomes, canonical serialization, or other core semantics. Newly observed upstream behavior must map to existing core semantics, an explicit extension, a declared non-equivalent outcome, or refusal. A change that genuinely requires different core meaning follows the core model-version and decision process rather than entering through profile maintenance.

Google Docs suggestions are deferred from the initial set because the relevant mutation and suggestion-thread surfaces sampled by this effort are preview and server-managed. HTML edits, Quill Delta, and ProseMirror transformations remain useful evidence and possible future one-way or loss-boundary mappings, but their reviewed models do not independently provide the complete pending-review semantics required for an initial normative profile.

### Rationale

The trio tests the portable model across three materially different boundaries: a versioned package-based office vocabulary, an independently standardized open-document text-change vocabulary, and an explicit Web-editor review model. WordprocessingML and ODF expose important differences in tree structure, paragraph handling, formatting history, and reconstruction. Reference Web Editor tests whether the same core can map to an editor-native proposal system rather than only between document formats.

Normative semantic mappings make profile-scoped equivalence and loss claims testable. Keeping SDK calls and integration recipes informative prevents product APIs or preferred implementation techniques from becoming accidental requirements. Direction-specific claims preserve useful narrow adapters while preventing import success from implying export or round-trip equivalence.

Independent profile versions and upstream pins contain vendor and standards evolution. This preserves the settled vendor-neutral core while allowing a revised profile to track an upstream edition without invalidating older artifacts or claims.

### Rejected alternatives and trade-offs

- **WordprocessingML and Reference Web Editor only:** would reduce initial work but omit an independent open-document comparison point, especially ODF's reconstruction and formatting-change limitations.
- **WordprocessingML and ODF only:** would cover document interchange well but would not directly test the intended Web-editor adopter boundary.
- **Make Reference Web Editor informative only:** would reduce exposure to vendor change but would also prevent testable semantic conformance at the only initial editor-native boundary. Version pinning contains the volatility more precisely.
- **Make all mappings informative:** would offer implementation advice without supporting reproducible profile-scoped equivalence, loss, or conformance claims.
- **Make APIs and implementation recipes normative:** would overconstrain architecture and cause ordinary SDK evolution to change interoperability requirements.
- **Require every adapter to implement both directions or all profiles:** would exclude honest and useful import-only, export-only, or single-ecosystem adapters without improving the semantics of their actual claims.
- **Define import only:** would leave export loss and round-trip boundaries unspecified even where the source model supports export.
- **Let profiles evolve implicitly with upstream latest versions:** would make old conformance claims non-reproducible and allow upstream drift to change requirements without review.
- **Allow profiles to override core semantics:** would create three competing models under one name and prevent canonical cross-profile interchange.

### Supporting and contradictory evidence

[Normative revision-model evidence](../evidence.md) shows that WordprocessingML and ODF provide persistent but materially different change structures. WordprocessingML covers content, property, structural, and move revisions, while ODF Text uses changed regions and reconstruction and does not carry the actual formatting delta in `text:format-change`. These differences make both valuable profile boundaries while also requiring explicit unsupported or lossy outcomes outside v1.

[Web-editor revision-practice evidence](../evidence.md) identifies Reference Web Editor as an explicit pending-suggestion model with identity, attachment, persistence hooks, and accept/discard operations. It also shows that its marker representation, grouping, nesting, custom attributes, and persistence are product-specific, supporting a pinned semantic profile rather than core adoption of its internal architecture.

[Text-subset feasibility evidence](../evidence.md) supports mappings for the selected text-focused operations while documenting concrete gaps: atomic replacement may be represented as paired changes, formatting values may be unavailable or command-shaped, paragraph behavior differs, and some native systems admit nested or multi-range suggestions excluded from v1. The active [loss-reporting decision](13-define-loss-reporting-and-conformance-outcomes.md) already provides the outcome vocabulary needed to report those boundaries rather than disguise them as equivalence.

Contrary evidence limits the expected result. No current cross-vendor corpus demonstrates lossless round trips among all three sources, and the core deliberately excludes native features each source may support. Each source has an independently evolving boundary: Reference Web Editor documentation and APIs are release-specific; ODF change tracking has edition-specific limitations; and the reviewed Word behavior does not cover every structure permitted by WordprocessingML. The profiles are therefore versioned, direction-specific contracts for the accepted subset, not claims that the upstream ecosystems are natively uniform.

### Uncertainty, assumptions, and follow-ups

- Exact upstream edition, schema, product, and documentation pins are factual publication inputs to verify while drafting each profile; selecting a newer pin does not reopen this decision unless its semantics invalidate the chosen boundary.
- The permanent profile identifiers and publication authority remain unsettled. They must be stable before publication but do not change the independent-versioning rule.
- Profile synthesis must define precise normative source boundaries, both feasible directions, permitted adaptations, loss and refusal cases, report bindings, and conformance examples for each member of the trio.
- The executable conformance corpus must gain profile-scoped cases or adapters sufficient to test direction-specific claims without treating one profile's native representation as core semantics.
- Future profiles, including Google Docs or narrower HTML, Quill, and ProseMirror mappings, require their own evidence and versioned boundary. They do not alter the initial trio automatically.
- No prior decision is superseded, and no additional normative research is currently justified. Drafting may open bounded research only if an exact upstream pin exposes behavior capable of changing feasibility or core meaning.
