# Choose the canonical serialization

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 14
Decision status: active
Supersedes:
Superseded by:

## Question

Which serialization family and versioning envelope should v1 require as its one canonical neutral interchange form, and which representation details are normative rather than implementation conveniences?

## Resolution

V1 uses JSON as its one canonical neutral interchange family, with JSON Schema Draft 2020-12 defining the structural contract and RFC 8785 JSON Canonicalization Scheme (JCS) defining canonical bytes. The envelope has separate mandatory `modelVersion` and `serializationProfile` members. V1 fixes them to the semantic-model version `1` and serialization profile `json-jcs-1`; a semantic incompatibility changes `modelVersion`, while a change that can alter schema interpretation or canonical bytes changes `serializationProfile`. An optional `$schema` member may assist tooling but does not determine interpretation. Unknown model versions or serialization profiles are unsupported rather than guessed.

The v1 JSON profile is intentionally narrower than generic JSON or JCS. Member names are unique. Identifiers, timestamps, and digests are strings. Numeric fields are non-negative safe integers where the model requires numbers; floating-point fields and implicit string/number coercion are forbidden. Strings satisfy the I-JSON interoperability constraints, and document text is preserved without Unicode normalization. A source containing text that the profile cannot represent, including isolated UTF-16 surrogates, is unsupported or produces an authorized, reported loss rather than silent repair. `null` is forbidden unless a field explicitly assigns it normative meaning; otherwise optionality is represented by absence.

The v1 schema fixes external field names, JSON types, required and conditionally required members, tagged operation forms, permitted values, and semantic ordering. Every operation has an explicit kind and the kind-specific required and forbidden members; operation type is never inferred from incidental field presence. JSON object member order is non-semantic. Arrays carry order only where the model says sequence is meaningful, including paragraph and formatted-fragment order. Proposal collection order does not define same-point ordering; that relation remains explicit. Collections without semantic order use identity-keyed objects or a specified canonical sort so equivalent instances do not acquire different canonical bytes accidentally.

Conforming canonical exporters emit the exact UTF-8 bytes produced by JCS after structural and semantic validation. Importers may accept noncanonical JSON as an implementation convenience, but they must validate and canonicalize it before treating or re-emitting it as canonical interchange. Pretty printing, input member order, parser and validator selection, internal object models, storage layout, transport, and noncanonical diagnostic views are not normative.

Each base-state fingerprint is SHA-256 over the JCS bytes of a versioned accepted-state projection, encoded as unpadded base64url. The projection includes the model/profile context and a domain discriminator, includes only the normative accepted document state, and excludes the fingerprint value itself, proposals, issue reports, provenance, and incidental metadata. The standard and fixtures must define the projection exactly so independent implementations produce the same digest.

Core schemas are closed except at explicit extension points. Extensions use stable URI identifiers and declare whether they are required. Unknown optional extensions must be preserved through the interchange path or produce a structured declared-loss outcome; an unknown required extension makes the input unsupported. Extensions cannot override core meaning.

### Rationale

JSON has the lowest implementation friction for the intended Web-editor and import/export audience, while JSON Schema and JCS provide a practical route to validation and repeatable bytes. Separating semantic and serialization versions prevents a canonicalization change from silently changing fingerprints without identifying a new profile. The strict wire contract standardizes only differences that can change interpretation, projections, canonical bytes, fingerprints, or interoperability; runtime architecture remains unconstrained.

The supporting comparison is [Canonical serialization candidates](../evidence.md). RFC 8259 establishes JSON's unordered objects and duplicate-name interoperability risk; I-JSON narrows Unicode, duplicate-name, number, and binary-representation hazards; RFC 8785 defines deterministic primitive serialization, recursive member sorting, preserved array order, and UTF-8 output; JSON Schema Draft 2020-12 supplies versioned structural vocabularies and controlled extension points.

### Rejected alternatives and trade-offs

- CBOR with CDDL was the standards-based generic binary alternative with the closest fit to the evaluation criteria and offers compact deterministic encoding, but requires additional browser codecs and more map, tag, and numeric-profile rules. It remains suitable as a future noncanonical mapping only if that mapping cannot claim canonical-v1 identity without conversion.
- XML with XSD and Canonical XML has established document tooling and rich schemas, but imposes heavier namespace, prefix, parser, and canonicalization policy than the selected Web-focused scope warrants.
- ASN.1 with DER provides strongly typed canonical binary encoding, but its compiler- and schema-centered tool boundary is disproportionate for the intended Web implementers.
- Protocol Buffers offers strong generated bindings and evolution support, but its own documentation does not provide portable canonical bytes as-is; a custom canonical layer would negate its main advantage here.
- MessagePack and YAML can carry the data but lack a stronger ready-made schema/canonicalization combination than the selected profile.
- Allowing multiple canonical families was rejected because it would move equivalence and fingerprinting back into pairwise conversion rules rather than establish one neutral form.
- Hashing the complete revision document was rejected because proposal metadata, issue reports, or provenance would then change a fingerprint intended to verify the accepted base state.

### Contradictory evidence, uncertainty, and assumptions

JCS is an Informational RFC rather than an IETF Standards Track specification, and JSON Schema validation alone cannot express all target-boundary, formatting-coverage, projection, and resolution constraints. V1 therefore adopts JCS normatively within this standard and requires semantic checks and cross-encoder fixtures in addition to schema validation. JSON is more verbose than the binary alternatives, and no performance or size benchmark was conducted; the decision prioritizes Web implementation friction, inspectability, and deterministic interoperability over wire compactness.

The eventual publication authority and permanent schema/extension URI locations remain unsettled. Stable literal version/profile values can be tested before those locations are chosen, but publication must assign durable schema identifiers without changing their normative contents. Media type and filename conventions are also deferred and do not determine document interpretation.

### Follow-ups

- [Build executable conformance fixtures](../evaluation/README.md#core-evaluation) must bind the semantic experiment to the v1 JSON schema and JCS profile, define the accepted-state fingerprint projection, and test cross-encoder canonicalization, duplicate names, member reordering, Unicode and surrogate boundaries, safe integers, all tagged operations, proposal ordering, extensions, declared loss, and invalid silent-loss cases.
- [Choose initial mapping profiles](17-choose-initial-mapping-profiles.md) must evaluate adapters against this canonical profile and use the settled mapping outcomes when a source cannot represent it exactly.
- No additional serialization-family research is justified unless a named candidate supplies materially stronger Web tooling or canonical/version-evolution evidence than the compared families.
