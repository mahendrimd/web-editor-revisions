# Evaluation and claim packaging

Status: Informative evaluation procedure for publication version 1.0.1

This package provides two related paths:

- an executable oracle for the core model and serialization profile; and
- a reproducible evidence package for a mapping profile, direction, implementation version, and persistence boundary.

Passing either path supports only the roles, cases, versions, and boundaries actually exercised. It does not establish adoption, universal round-trip support, or conformance of an entire source format or product.

## Core evaluation

### Prerequisites

- Python 3.11 or later; and
- the `jsonschema` Python package with Draft 2020-12 support.

From the repository root, run:

```sh
python3 standards/v1.0.1/evaluation/run_conformance.py
```

The command reads the publication's [normative schema](../schema/web-editor-revisions-v1.schema.json), loads the literal serialization fixture with duplicate-member detection, and executes all 13 fixture groups. A nonzero exit status means at least one group failed. Use `--list` to list the groups without running them.

The runner covers strict JSON parsing, the narrow JCS profile, accepted-state fingerprints, all six proposal kinds, exact projections, selective resolution, target remapping, lifecycle and persistence observations, extensions, structured mapping outcomes, loss authorization, rollback, and safety outcomes. The fixture builders inside the runner are test authoring code, not another interchange representation.

The canonical serialization fixture is [`fixtures/serialization-cases.json`](fixtures/serialization-cases.json). It contains a schema-valid insertion document, its exact JCS bytes, its expected accepted-state fingerprint, and a differently ordered encoding that must produce the same bytes.

### Interpreting a core result

A passing run supports the exercised core document, producer/consumer, and resolver behavior. It does not exercise a native editor or document format. A truthful `lossy`, `unsupported`, or cleanly rolled-back `failed` mapping can conform; unauthorized loss, silent loss, misleading classification, or residual partial commit cannot.

Independent implementations should additionally compare canonical bytes and projections across encoders. A claim should record the exact publication commit, Python and `jsonschema` versions, operating environment, command, complete log, and hashes of the schema and fixture used.

### Informative review-method inspection

This inspection is informative and does not add a conformance claim. For a proposal in the supported subset, an evaluator can check whether a review method lets a reviewer distinguish accepted from pending content, identify the complete target and payload of the atomic decision, inspect both projections, and observe either stable successor attachment or a truthful incompatibility or unavailable-target result. The evaluator can also check that a refused, materialized, or lossy mapping is not presented as equivalent.

Two boundary scenarios make the distinction concrete:

- **Supported broad deletion:** one deletion covers a large exact range within one paragraph. The inspector can identify the complete range and payload, derive both projections, confirm one atomic accept/reject unit, and verify the attachment or truthful failure of remaining proposals.
- **Unsupported compound paste:** one authored operation atomically introduces content across multiple new paragraphs. If an adapter splits it, materializes it, or refuses it, the review method should disclose the changed decision boundary or mapping outcome rather than present the result as one equivalent version 1 proposal.

This inspection does not evaluate a prescribed inline design, navigation queue, filter, gesture, accessibility presentation, or discussion workflow. It also does not make arbitrary partial acceptance part of the model.

## Profile evaluation

Profile conformance needs a live or fixture-driven source adapter because the publication alone cannot establish authoritative native behavior for WordprocessingML, ODF Text, or Reference Web Editor. The procedure below makes that external run repeatable and reviewable.

Before designing adapter machinery, an implementation plan can name the authoritative native mechanism used for accepted content, pending changes, resolution, successor attachment, projections, and persistence. It can then identify any adapter-added configuration, sidecar, or transformation and the demonstrated native mismatch that requires it. This planning evidence is informative: conformance continues to depend on the activated fixture matrices and observed outcomes, not on using a preferred API or internal architecture.

For one profile direction:

1. Pin the adapter implementation, source-system version, configuration, supported subset, and exact persistence boundary. Declare `claimScope` as `safety-only` when no proposal-kind capability is claimed or `proposal-mapping` otherwise. List each supported core proposal kind in `profile.capabilities`.
2. Run the core suite above against the publication commit used by the adapter.
3. Select the required fixtures from the direction's explicit matrix in [`profile-requirements.json`](profile-requirements.json): every `alwaysRequired` fixture, every fixture for each declared capability, and—only when `boundary.sourcePersistenceClaimed` is true—the native-to-core `sourcePersistence` fixtures. Core-to-native matrices always include native save/reload, clean failure, rollback, and partial-persistence detection. The identifiers operationalize the normative profile matrices; the profile text controls if the catalog is defective.
4. For each fixture, preserve the native input, output when any, core interchange artifact when any, mapping report, acceptance and rejection observations when applicable, persistence observation when applicable, and a complete execution log. Demonstrate no mutation for refusal and rollback cases.
5. Hash every retained artifact with SHA-256 and describe the expected and observed outcomes without broadening the measured boundary.
6. Create a claim manifest conforming to [`profile-claim.schema.json`](profile-claim.schema.json). Artifact paths are relative to the manifest, cannot escape its directory, and must match their recorded hashes.
7. Validate the package:

   ```sh
   python3 standards/v1.0.1/evaluation/validate_profile_claim.py path/to/claim.json
   ```

The validator checks the manifest schema, pinned profile and direction, capability and claim-scope consistency, optional source-persistence activation, complete activated fixture identifiers, pass/fail consistency, core-suite result, local artifact containment, and artifact hashes. It rejects capabilities absent from the selected direction. It does not decide whether the preserved native artifacts are truthful; an independent verifier must rerun or inspect the adapter and projections.

### Claim result rules

A manifest may use `claimResult: "pass"` only when all 13 core groups passed and every activated profile fixture has `status: "passed"`. `failed`, `not-run`, and an assertion that a required case is inapplicable do not satisfy an activated fixture. A failed or incomplete experimental run remains useful evidence and uses `claimResult: "fail"`; it must not be presented as a conforming claim.

A passing `safety-only` claim has an empty `profile.capabilities` array. It proves only the selected direction's universal validation, reporting, refusal, loss, and transaction-safety behavior. It is not evidence of semantic mapping support for any proposal kind. A proposal-mapping claim activates and must pass the matrix for every listed capability. Unlisted kinds remain outside the claim even if experimental fixtures for them appear in the package.

Every claim is limited to its manifest's implementation, version, profile identifier and version, direction, claim scope, capabilities, source boundary, persistence boundary, optional source-persistence assertion, and publication commit. A bidirectional adapter therefore produces at least two claims. A profile update, capability change, persistence-boundary change, or upstream-version change requires a new claim.

## Profile requirements catalog maintenance

Validate the catalog and schemas without a claim package:

```sh
python3 standards/v1.0.1/evaluation/validate_profile_claim.py --check-catalog
```

The catalog is evaluation support, not an independent normative layer. The check verifies two explicit directions per profile, known and non-duplicated capabilities, unique fixture identifiers within each direction, mandatory core-to-native persistence cases, and exact fixture/activation agreement with the marked normative matrix in each profile document. When a normative profile changes its minimum fixture section, maintainers must update the corresponding catalog entry in the same change and rerun this check.

Run the packaged positive and negative manifest tests for all six directions:

```sh
python3 standards/v1.0.1/evaluation/validate_profile_claim.py --self-test
```

The self-test exercises full-capability and safety-only positive packages for every direction, a missing activated fixture in every direction, and rejection of scope/capability mismatch, `not-run` required evidence, invalid source-persistence scope, an unavailable direction capability, and catalog/profile drift.
