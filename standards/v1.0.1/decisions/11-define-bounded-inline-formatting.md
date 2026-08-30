# Define bounded inline formatting

Type: decision
Phase: resolution
Status: resolved
Recorded by: project maintainer
Blocked by: 09
Decision status: active
Supersedes:
Superseded by:

## Question

Which inline formatting properties and before/after value states belong to the mandatory v1 vocabulary, how should effective, unset, inherited, style-derived, and normalized values be distinguished, and which source representation differences require explicit loss reporting?

## Resolution

### Decision

The mandatory v1 inline-formatting vocabulary is limited to four independently observable properties: **italic**, **bold**, **underline**, and **strikethrough**. Each property has a concrete normalized effective value representing whether that formatting is present or absent over the targeted text range. A portable formatting proposal records the before and after effective value for every property it changes.

The core preserves the formatting outcome visible to a user, not the source mechanism that produced it. Direct formatting, an inherited value, an unset or removed local declaration, a named style, a theme, a command, or another source representation may map to the same effective core value. Source derivation may be preserved as optional mapping-profile metadata, but it is not an alternative to the required before and after effective values.

Normalization is a mapping transformation, not a value state. Source forms that produce the same effective property value and cover the same text may normalize to one portable value without semantic loss. Source syntax, declaration order, redundant declarations, run splitting or merging, and equivalent internal structure are not portable.

A mapping must report a limitation when it cannot determine a required before or after effective value, cannot reproduce both acceptance and rejection outcomes, changes the covered text, drops an unsupported formatting change, or changes the user-visible formatting or meaning. A source-origin difference is reportable as loss only when a mapping profile promises to preserve that origin. The exact loss-report vocabulary and conformance outcome are deferred to [Define loss reporting and conformance outcomes](13-define-loss-reporting-and-conformance-outcomes.md).

Properties outside the mandatory vocabulary—including colors, highlighting, font family, font size, subscript, superscript, arbitrary CSS or document-format properties, and theme-dependent formatting—may be represented by future extensions or mapping profiles. They are not silently treated as one of the four core properties.

### Rationale

The four-property vocabulary covers common, directly observable inline-formatting outcomes while keeping the mandatory adapter contract narrow. It makes the first version more useful than an insertion/deletion-only standard without requiring arbitrary or source-specific styling.

Requiring effective before and after values makes acceptance and rejection independently testable across representation models. It avoids mistaking an implementation detail such as an HTML element, CSS declaration, document style, source run, editor command, or inheritance path for the portable outcome. Optional profile metadata still permits higher-fidelity round trips where both endpoints understand the same derivation model.

This boundary follows the assessment decision to standardize normalized effective formatting values and report limitations instead of claiming equivalence. It also fits the accepted target model: formatting attaches to a paragraph-local text range without making source runs or spans portable identities.

### Rejected alternatives and trade-offs

- **Require a broader mandatory vocabulary:** colors, highlighting, fonts, sizes, baseline shifts, arbitrary properties, and theme-dependent values would improve coverage for some documents, but the available evidence does not establish a stable cross-model value or inheritance contract for them. They remain possible extensions rather than silent loss.
- **Require only italic:** would satisfy the motivating example but create an unnecessarily special-purpose core when bold, underline, and strikethrough can use the same bounded binary contract.
- **Preserve source declarations instead of effective values:** could improve source-format round trips, but would make equivalent user outcomes depend on incompatible cascade, named-style, theme, command, and property systems.
- **Make unset, inherited, style-derived, or theme-derived core values:** conflates how a result was obtained with the result itself. The same derivation label can produce different outcomes in different contexts, while different derivations can produce the same outcome.
- **Require exact source segmentation and syntax:** would preserve incidental representation details at the cost of treating harmless run normalization, equivalent declarations, or editor-specific storage as semantic loss.
- **Ignore all representation changes:** would hide cases where normalization changes visible formatting, range coverage, or accept/reject behavior. Equivalent representation changes are permitted; outcome-changing transformations are reported.

### Supporting and contradictory evidence

The [text-subset feasibility research](../evidence.md) found a stable conceptual shape in effective style ranges with before and after values, while showing materially different native forms: OOXML retains prior property sets, ODF text format changes omit the changed formatting, Reference Web Editor replays stored commands and parameters, Google uses changed-field masks, and Quill uses attributes including explicit removal. It also found that Word runs, ODF spans, Google text runs, Reference Web Editor markers, HTML elements, and Quill operations segment equivalent text differently.

The [normative-model research](../evidence.md) supports persistent property-change concepts in OOXML but contradicts any claim of a shared lossless source representation: ODF text format-change does not carry the actual delta, and HTML and Input Events do not define persistent formatting-proposal resolution. The [Web-editor practice research](../evidence.md) likewise supports formatting as a real revision category while showing that tree marks, server fields, command replay, and operation attributes are not interchangeable storage models.

The evidence does not prove that every source can recover both effective values. In particular, a bare ODF text format-change may lack the information required for an equivalent portable proposal. That contradiction is handled through unavailable or unsupported outcomes rather than weakening the core value requirement.

### Uncertainty, assumptions, and follow-ups

- The decision assumes adapters can determine concrete effective values for a useful subset of native formatting proposals. An adapter that cannot do so reports the limitation.
- The core values are deliberately outcome-oriented and do not preserve source markup distinctions.
- The serialization names and representation of the four properties remain open until [Choose the canonical serialization](15-choose-canonical-serialization.md).
- Whether one proposal may change several formatting properties atomically, and how its boundary association and target transformation behave, will be settled by [Define content-change and resolution semantics](12-define-content-change-and-resolution-semantics.md).
- [Define loss reporting and conformance outcomes](13-define-loss-reporting-and-conformance-outcomes.md) must name unavailable values, unsupported properties, outcome-changing normalization, coverage changes, profile-promised origin loss, and projection failures.
- [Build executable conformance fixtures](../evaluation/README.md#core-evaluation) must include application and removal cases for all four properties, equivalent source normalization, unavailable before/after values, unsupported properties, and range-coverage changes.
