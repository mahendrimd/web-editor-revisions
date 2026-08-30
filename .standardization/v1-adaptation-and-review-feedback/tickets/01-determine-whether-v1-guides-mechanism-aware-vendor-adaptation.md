# Determine whether v1 guides mechanism-aware vendor adaptation

Type: research
Phase: discovery
Status: resolved
Claimed by: /root
Blocked by:

## Question

Across the v1 core, its three mapping profiles, their conformance fixtures, and the documented native mechanisms at those pinned vendor boundaries, what does an adapter actually need to implement for content fragments, proposal kinds, accept/reject resolution, and successor-target behavior; which requirements are observable equivalence obligations rather than required new calls or storage primitives; and where, if anywhere, is the implementation-planning guidance too weak to prevent an agent from prescribing redundant mechanisms? The result can change whether the report becomes a core clarification, profile guidance, evaluation addition, or no release change. Use the released baseline and primary upstream specifications or vendor documentation for the pinned boundaries. Stop when each profile direction has at least one representative mechanism trace, the successor-remapping example is explicitly tested against existing native transformation bases, and remaining uncertainty could not change that disposition choice.

## Resolution

Resolved by [Mechanism-aware vendor adaptation in version 1](../evidence/01-mechanism-aware-vendor-adaptation.md).

Version 1 already treats content fragments, proposal kinds, resolution, and successor-target behavior as portable observations, not required vendor-side method names or storage primitives. Its six profile directions map those observations into existing WordprocessingML revision elements, ODF change regions and marks, or Reference Web Editor suggestion records, commands, markers/live ranges, and persistence integration. The core explicitly permits markers, operations, eager or lazy transformation, or another algorithm when the resulting state and targets agree.

The reported successor-remapping example exposes an existing base particularly clearly: Reference Web Editor markers use live ranges that update through model operations, and live positions transform across insert, delete, split, and merge. A conforming plan should test and reuse that behavior, read back the successor attachment, and add configuration, sidecar data, or adapter-local transformation only for a demonstrated mismatch. WordprocessingML and ODF have no generic live remapping API; the adapter instead leverages XML/application transforms or resolves in core and regenerates remaining change records, then proves the result by reconstruction and reopen.

The research also preserves real counterexamples. ODF formatting, atomic replacement, portable paragraph identity, same-point order, native marker collapse, and automatic suggestion merging can require extension, reported loss, or refusal. The supported planning principle is therefore “inventory and leverage, then prove,” not unconditional reuse.

The remaining gap is guidance discoverability: v1 distributes these facts across architecture disclaimers, profile tables, adaptation rules, loss tables, fixtures, and short implementation notes, but provides no explicit mechanism-inventory/reuse-first planning sequence or worked remapping trace. The evidence recommends a decision on core-preserving informative guidance, profile-specific worked traces, evaluation clarification, or no release change; it does not select that normative disposition.
