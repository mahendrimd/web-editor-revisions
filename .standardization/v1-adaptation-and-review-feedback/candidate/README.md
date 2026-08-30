# Web Editor Revisions publication

Project status: Maintainer-reviewed version 1.0.1
Publication set: `web-editor-revisions-v1.0.1`
Release tag: `web-editor-revisions-v1.0.1`
Predecessor publication: version `1`, tag `web-editor-revisions-v1`
Core semantic model: `1`
Canonical serialization profile: `json-jcs-1`

This directory is the self-contained version 1.0.1 publication for a vendor-neutral interchange model for pending revisions in text-focused Web editors. It defines a meaningful review-interoperability core for a deliberately bounded proposal subset, three direction-specific mapping profiles, and reproducible evaluation material. It does not claim to standardize a complete general-purpose review-mode editor, rich office documents, or every editor feature.

## Independence

This is an independent implementer project maintained by its repository owner. It is not an official standard and is not affiliated with, authorized, sponsored, endorsed, or approved by any referenced vendor, open-source project, or standards organization. Product and organization names are used only where needed to identify technical sources and interoperability boundaries; all such names and trademarks remain the property of their respective owners. “Reference Web Editor” is a project-local neutral label for the editor snapshot cited by URL in its mapping profile.

## Publication map

Normative material:

- [Web Editor Revisions](standard.md) — core semantics, canonical serialization, loss reporting, and role-specific conformance;
- [normative JSON Schema](schema/web-editor-revisions-v1.schema.json) — the structural contract used with the semantic requirements;
- [WordprocessingML Tracked Revisions Mapping Profile](profiles/wordprocessingml.md);
- [ODF Text Change Tracking Mapping Profile](profiles/odf-text.md); and
- [Reference Web Editor Track Changes Mapping Profile](profiles/reference-web-editor.md).

Supporting material:

- [Evaluation and claim packaging](evaluation/README.md) — executable core fixtures and the reproducible procedure for direction-specific profile claims;
- [Evidence index](evidence.md) — curated primary-source support, contrary evidence, and source limits; and
- [Decision provenance](provenance.md) and [authoritative decision records](decisions/) — the material design choices, full rationale, and their relationship to the publication; and
- [Release record](release.md) — complete change set, compatibility statement, validation and acceptance state, and propagation obligations.

Normative requirements are only those identified as normative by the core standard or a mapping profile. Evaluation instructions, provenance, rationale, and examples are informative unless a normative document explicitly incorporates them.

## Adoption path

1. Choose a claimed role: producer, consumer, resolver, or mapping adapter. A component may claim more than one.
2. Implement the core schema and semantic invariants before relying on a profile. Producers also emit JCS bytes; consumers validate before use; resolvers implement only the proposal kinds they explicitly claim.
3. Run the [published core suite](evaluation/README.md#core-evaluation). Passing supports only the roles and cases exercised by that suite.
4. For a native document or editor boundary, choose one profile, one direction, and one pinned upstream version. Declare either a safety-only claim with no proposal-kind capabilities or list every supported core proposal kind, and state whether a native-to-core claim additionally covers source persistence.
5. Execute the direction's universal fixture matrix plus the matrix for every declared capability and any activated source-persistence matrix. Core-to-native claims always include native save/reload, rollback, and partial-persistence checks. Preserve hashed native inputs, outputs, mapping reports, projections, persistence observations, and logs in a profile claim package.
6. Validate the claim manifest as described in [Profile evaluation](evaluation/README.md#profile-evaluation). A passing package is evidence for that exact implementation, version, profile, direction, and boundary—not for an entire product or format.

Start with a consumer claim when evaluating interoperability: strict validation and truthful refusal are useful before mutation is enabled. A safety-only adapter claim can likewise establish bounded refusal and transaction behavior, but it demonstrates no proposal-kind mapping support. Add proposal-mapping capabilities only after their exact projections are independently verified. Every core-to-native adapter claim includes the native save/reload and rollback boundary; native-to-core source persistence is optional and must be declared when claimed.

## Version and maintenance boundary

The core model, serialization profile, and each mapping profile version independently. Their compatibility rules are in [Section 19 of the core](standard.md#19-versioning-and-maintenance). A published version should carry matching document metadata and a Git tag. Claims should record the exact repository commit until a permanent publication authority and stable public identifiers are assigned.

Version 1.0.1 is a patch release with no normative, conformance, or migration effect. Its complete classification and compatibility record is in [the release manifest](release.md#compatibility-and-migration). The normative model and serialization selectors remain the literal version values above, and the schema deliberately has no provisional `$id`. Publication authority and long-term stewardship remain open; authority, registry, or stewardship changes must not silently alter the normative contents of a publication set.

## Known limits and reassessment

The model supports paragraph-local insertions, deletions, replacements, and formatting proposals—including a broad exact range within one paragraph—and one adjacent paragraph split or merge. It does not generally preserve one atomic multi-paragraph paste, one cross-paragraph or disjoint-range deletion, proposal groups or hierarchy, overlaps or dependencies, or material reshaping of a pending proposal under the same identity. Splitting a compound authored operation into independently resolvable proposals is not automatically equivalent.

Moves, general document trees, arbitrary formatting, comments, concurrent-editing semantics, undo/redo, permissions, and UI behavior also remain outside the core. The full limitations and concrete reassessment triggers are in [Section 18 of the core](standard.md#18-limitations-and-reassessment-triggers). The [evidence index](evidence.md) records the material counterexamples that prevent broader claims.
