# Decision provenance

Status: Informative provenance for publication version 1.0.1, including applicable inherited version 1 decisions

This document records why the material design boundaries in the publication exist. It is not a second normative specification: when a summary here differs from the [core standard](standard.md), schema, or a profile, the normative artifact controls. Evidence links refer to the curated [evidence index](evidence.md) and to primary sources.

## Material decisions

| Decision | Accepted direction and rationale | Publication result |
| --- | --- | --- |
| [First standardization boundary](decisions/01-choose-first-standardization-boundary.md) | Define a text-focused semantic core and canonical interchange while separating source-specific mappings. Shared outcomes are portable; UI, runtime representation, collaboration architecture, and private storage are not stable common ground. | Core Sections 1–5 and the independent profiles |
| [Review terminology](decisions/04-reconcile-core-review-terminology.md) | Use **revision proposal** for the independently reviewable record and reserve operation, history, undo/redo, annotation, comment, and resolution for distinct layers. Vendor terms are aliases only when behavior matches. | Core Section 4 |
| [Assessment depth](decisions/08-accept-assessment-verdict.md) | Standardize a useful subset: common text, four effective Boolean formatting properties, atomic replacement, paragraph split/merge, observable projections, identity, serialization, and loss reporting. Defer moves, richer structure, overlap, dependencies, arbitrary formatting, and concurrency. | Core Sections 3 and 18 |
| [Accepted state and targets](decisions/09-define-portable-document-state-and-targets.md) | Use ordered paragraph records with stable paragraph identities, exact text, normalized effective formatting, and typed paragraph-local UTF-16 targets. Bind proposals to an accepted-state fingerprint and deterministically remap surviving targets after resolution. | Core Sections 6, 7, 11, and 12.3 |
| [Proposal identity and lifecycle](decisions/10-define-proposal-identity-metadata-and-lifecycle.md) | Require immutable, lineage-scoped proposal identity and a verifiable base-state reference. Preserve optional provenance when present. Keep processing conflict separate from the pending/accepted/rejected review lifecycle and permit either complete terminal records or none. | Core Section 8 |
| [Bounded formatting](decisions/11-define-bounded-inline-formatting.md) | Require `italic`, `bold`, `underline`, and `strikethrough` as complete effective before/after Boolean values. Source derivation may vary, but unavailable or outcome-changing mappings are reported rather than guessed. | Core Sections 6.3 and 9.4 |
| [Content changes and resolution](decisions/12-define-content-change-and-resolution-semantics.md) | Carry exact formatted payloads, preserve replacement and multi-property formatting atomically, keep the left paragraph identity across split/merge, order co-located insertions explicitly, and resolve selected compatible proposals all-or-nothing. | Core Sections 9–11 |
| [Loss and conformance](decisions/13-define-loss-reporting-and-conformance-outcomes.md) | Separate operation outcome from conformance. Bind structured issues to a profile, direction, boundary, input, and output; require authorization for semantic loss; reserve equivalence for exact results or declared no-impact adaptations. | Core Sections 14 and 15 |
| [Canonical serialization](decisions/15-choose-canonical-serialization.md) | Use JSON Schema Draft 2020-12 with the narrow `json-jcs-1` profile, strict interoperable values, JCS bytes, and a SHA-256 accepted-state fingerprint. Close core objects and use explicit URI-keyed extensions. | Core Sections 5, 12, and 13 plus the normative schema |
| [Initial mapping profiles](decisions/17-choose-initial-mapping-profiles.md) | Publish direction-specific, independently versioned profiles for Strict WordprocessingML, ODF Text 1.4, and Reference Web Editor v48.3.1. Pin upstream boundaries and isolate their evolution from the core. | Core Section 16 and `profiles/` |
| [Direction-specific profile evidence](decisions/25-define-direction-specific-profile-fixture-matrices.md) | Use six explicit fixture matrices. Every claim runs universal safety cases plus cases activated by its declared proposal-kind capabilities; core-to-native persistence is mandatory, while native-to-core source persistence is conditional. Safety-only claims advertise no mapping capability. | Profile Section 10 matrices and `evaluation/` claim packaging |
| [Mechanism-aware adaptation planning](decisions/26-clarify-mechanism-aware-adaptation-planning.md) | Clarify an informative “inventory and leverage, then prove” method and representative live-model and package traces without prescribing native reuse, a remapping API, an internal portable store, or another private architecture. | Core Section 16.1, profile Section 11 notes, and evaluation guidance |
| [Bounded document review integrity](decisions/27-clarify-bounded-document-review-integrity.md) | Explain the user-facing integrity outcomes already supplied for supported proposals, distinguish document projection decisions from code-review integration workflow, and state the paragraph-local and single-boundary limit. Defer compound structural proposals as high-priority normative work. | Core Sections 3.3 and 18, publication summary, and evaluation scenarios |

## Alternatives deliberately not selected

- A universal editor or office-document model was rejected because representative systems diverge on structures, grouping, replacement, prior formatting, identity, persistence, and concurrency.
- DOM paths, source run identities, fuzzy selectors, and grapheme indexes were not selected as core target coordinates. They remain adapter techniques or future-profile candidates.
- Inline change markup was not required as the portable representation because it couples the interchange contract to one document tree and complicates accepted-state fingerprinting and selective resolution.
- A delete-plus-insert convention was not treated as automatically equivalent to atomic replacement because independent resolution changes review semantics.
- Source timestamps, authors, and comments were not made mandatory because representative systems expose them unevenly; available provenance is preserve-if-present.
- Generic JSON, XML, CBOR, Protocol Buffers, or ASN.1 without a versioned application profile was rejected because syntax alone does not define canonical semantic bytes or revision outcomes.
- Lossless-or-fail as the only mapping policy was rejected because declared no-impact adaptation and explicitly authorized loss are useful and auditable. Silent or unauthorized loss remains nonconforming.

## Tensions intentionally retained

Version 1 keeps several constraints visible rather than resolving them through unsupported generalization:

- UTF-16 minimizes friction for representative Web implementations but is not a human grapheme unit and requires strict boundary validation.
- The four-property formatting subset is useful but cannot preserve theme-dependent, source-specific, or unavailable prior formatting.
- Atomic replacement is valuable in the neutral model even though the initial source profiles commonly need refusal or authorized degradation.
- Stable synthesized identities can be an equivalent declared adaptation, while native identity and provenance claims must remain truthful.
- A passing core suite establishes only the exercised neutral semantics. Native-format and editor claims require profile-specific fixtures across the exact persistence boundary.
- Existing vendor mechanisms can transform or reconstruct surviving changes, but their native results still require observation against the portable projections, attachment, identity, reporting, and persistence rules.
- Paragraph-local and one-boundary proposals provide useful review interoperability, while compound structural operations remain too consequential to hide and too unsettled to define through an informative patch.

## Maintenance use

Future changes should identify which row they alter. A behavior-changing revision should update the normative artifact and version metadata, refresh the relevant evidence, and record whether it supersedes the accepted direction. Purely editorial corrections should not silently broaden a conformance claim. The [evaluation package](evaluation/README.md) binds claims to exact versions and artifacts so later maintenance can compare evidence rather than relying on product names alone.
