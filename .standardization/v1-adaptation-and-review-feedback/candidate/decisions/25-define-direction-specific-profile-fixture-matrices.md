# Define direction-specific profile fixture matrices

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by:
Decision status: active
Supersedes:
Superseded by:

## Question

How must each initial mapping profile divide its minimum fixtures between the native-to-core and core-to-native directions so a passing direction-scoped claim proves every applicable requirement without requiring source-only cases in the opposite direction or allowing inapplicable cases to pass untested?

## Resolution

### Decision

Publish six explicit minimum-fixture matrices: one for each native-to-core and core-to-native direction of the WordprocessingML, ODF Text, and Reference Web Editor profiles. Do not use one inherited profile-wide requirement set and do not permit a required fixture to pass as `not-applicable`.

Each direction-scoped claim declares the core proposal kinds for which it claims mapping capability. The fixtures required for a passing claim are the union of:

1. the direction's universal fixtures for validation, truthful refusal and loss classification, authorization, rollback, transaction integrity, identity and report binding, and other safety behavior that applies regardless of supported proposal kind;
2. the direction-specific fixtures for every declared proposal-kind capability; and
3. any fixtures activated by an additional persistence claim.

An unclaimed proposal kind is not advertised as supported and does not activate its capability fixtures. A required fixture must pass; `not-run`, failure, or an inapplicability label cannot satisfy it. A claim may declare no proposal-kind capability and demonstrate only the direction's universal safe-handling behavior, but it must clearly advertise zero mapping capability and must not be presented as semantic support for a proposal kind.

For every core-to-native claim, native save/reload, clean rollback, and residual partial-persistence detection are mandatory because the mapping creates native state whose survival is part of the direction's observable result. For a native-to-core claim, the mandatory boundary binds and verifies the complete native input and canonical core output; the adapter need not mutate or rewrite its native source merely to prove import. Native-source save/reload fixtures become mandatory only when the claim explicitly includes that additional source-persistence boundary.

The matrices use core proposal kinds as the portable capability vocabulary. Source-only invalid or excluded constructs remain universal native-to-core refusal fixtures where they test the profile boundary. The corresponding core-to-native matrix instead tests the valid core input, refusal, authorized-loss, emitted native representation, and persistence behavior defined for that direction. Exact fixture identifiers and catalog member names are synthesis details; they must implement these semantics without introducing a second conformance model.

### Rationale

The active profile decision and core conformance clauses make claims independent by profile, version, direction, capability, and measured boundary. Explicit per-direction matrices make that scope reviewable and prevent a native-source-only case from becoming a meaningless core-to-native requirement. Capability-conditioned fixtures preserve the existing rule that an adapter need not implement every proposal kind while ensuring a passing claim distinguishes implemented equivalence from truthful refusal.

Universal safety fixtures remain mandatory because limited capability does not excuse silent loss, misleading classification, unauthorized mutation, or partial commit. Asymmetric persistence requirements follow the operation boundary: export creates native state that must survive the profile's save/reload boundary, while import observes rather than rewrites its native source unless it makes an additional persistence claim.

The [version 1 publication validation report](https://github.com/mahendrimd/web-editor-revisions/blob/web-editor-revisions-v1/standards/v1/validation-report.md) demonstrates the defect in the shared catalog. WordprocessingML moved or nested native revisions, ODF `text:format-change` insufficiency, and Reference Web Editor marker/record or multi-range conditions are meaningful native-to-core inputs but cannot be supplied as conforming core-to-native inputs. The current catalog also cannot express partial proposal-kind capability even though the core permits it.

### Rejected alternatives and trade-offs

- **A shared baseline plus directional additions:** reduces textual duplication, but makes applicability depend on inheritance across documents and increases the risk that a source-shaped fixture silently reaches the opposite direction. Six explicit matrices are small enough to keep authority local and auditable.
- **One shared list with `not-applicable`:** is compact, but turns applicability into an adapter assertion and weakens the rule that every required fixture must pass.
- **Require every direction claim to support the complete profile subset:** produces simpler manifests but contradicts the active core rule that adapters need not implement every proposal kind and would exclude useful narrow implementations.
- **Let unsupported outcomes pass capability fixtures:** tests truthful refusal but does not prove the advertised semantic capability. Refusal belongs in universal or explicit loss-boundary fixtures, not as evidence that a proposal kind is supported.
- **Require native save/reload in both directions:** could gather extra evidence, but forces an importer to mutate its authoritative source for no semantic reason. Optional source-persistence claims preserve that evidence when it is actually in scope.
- **Disallow safety-only claims:** would make profile claims appear more substantial, but would also conflict with the core's recognition that truthful mutation-free unsupported behavior can conform. Such a claim remains valid only when its zero-capability limit is prominent.

### Supporting and contradictory evidence

Supporting evidence is the already accepted direction- and capability-scoped conformance model, the three profiles' distinct import and export clauses, and the validation finding that the shared catalog cannot model their asymmetric source conditions. The published claim schema already binds profile, direction, upstream version, scope, and persistence, so explicit capabilities and selected requirements extend an existing boundary rather than inventing a new claim type.

The chief trade-off is maintenance duplication: shared semantic cases such as insertion, deletion, and identity must appear in more than one explicit matrix. Catalog validation must therefore detect duplicate identifiers within a matrix, unknown capabilities, missing directional coverage, and drift between normative profile sections and executable requirements. No live native adapter corpus yet establishes whether the resulting minimum sets are optimally small; the matrices define reproducible evidence requirements, not adoption or universal round-trip success.

### Uncertainty and assumptions

- The exact fixture allocation, identifier spellings, catalog structure, and manifest field names remain synthesis work, constrained by this decision.
- A proposal-kind capability means the adapter claims the applicable profile mapping semantics for that kind across the declared direction and boundary; it does not broaden the source subset or imply support for excluded native structures.
- A source-persistence claim needs an explicit machine-readable declaration so the validator can activate its additional fixtures.
- Profiles or extension profiles that add atomic replacement or other capabilities require their own matrix entries and version boundary; the base profiles do not gain that support implicitly.
- Passing the matrices still requires independent inspection or rerun of native artifacts because hash and manifest validation cannot establish that an adapter's observed native behavior is truthful.

### Follow-up

[Implement direction- and capability-scoped profile matrices](../evaluation/README.md#profile-evaluation) must revise the normative profile fixture sections, requirements catalog, claim manifest schema, validator, evaluation guidance, and reproducibility checks. The interrupted publication-validation task resumes only after that synthesis is complete.
