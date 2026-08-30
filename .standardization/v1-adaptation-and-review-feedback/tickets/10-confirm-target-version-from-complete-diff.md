# Confirm the target version from the complete candidate diff

Type: decision
Phase: validation
Status: resolved
Claimed by: /root
Blocked by: 09
Decision status: active
Supersedes:
Superseded by:

## Question

After reviewing every baseline-to-candidate difference, protected-file comparison, normative and conformance effect, and an independent attempt to falsify the working classification, should the successor use the minimum patch increment `1.0.1`, or does the complete diff require a higher increment under the configured standard-versioning policy; and what maintainer rationale confirms that target version?

## Resolution

### Decision

Confirm target publication version **`1.0.1`**, the configured patch successor to baseline version `1`. Resolve the publication directory as `standards/v1.0.1` and the planned immutable release tag as `web-editor-revisions-v1.0.1`.

The project maintainer explicitly confirmed `1.0.1` on 2026-08-30 and required the materialized bundle to contain no avoidable bloat, stale wording or metadata, or harmful duplication.

### Working-agent review

The complete baseline-to-candidate diff changes eleven paths: six concise publication/supporting documents, three profile files only in their informative Section 11 notes, two new durable decision records, and the required new `release.md`. Of 252 added lines, 85 are the two retained decision records and 78 are the release manifest; the remaining additions are the bounded core, profile, evaluation, evidence, provenance, and publication-summary clarifications.

Core Sections 3.3 and 16.1 explicitly state that they are informative and add no conformance requirement or prescribed architecture. Section 18 makes existing paragraph-local targets, one-boundary targets, independent atomic proposals, and excluded overlap/dependency consequences visible without changing them. Profile additions are confined to Section 11, which each profile already declares informative. The schema, serialization fixture, profile requirements catalog, profile-claim schema, core runner, and profile validator are byte-identical to version 1, and profile diffs leave all six capability matrices unchanged.

The duplicate scan found no exact duplicate long-form addition. Its only repeated long lines are inherited BCP 14 and fixture boilerplate shared intentionally by the three standalone profiles. Layer-specific summaries in the publication index, core limitation, evaluation guide, evidence, provenance, decision record, and release manifest serve distinct navigation, interpretation, test, rationale, and release-record purposes.

No previously conforming document, producer, consumer, resolver, adapter, profile claim, fixture result, or implementation algorithm becomes nonconforming. No migration or deprecation action is introduced. Under the configured standard-versioning policy, the final classification is therefore **patch**.

### Independent falsification review

An independent agent reviewed the full diff without editing it and attempted to prove that a minor or major increment was required. It found no normative, conformance, compatibility, migration, schema, capability, fixture, or algorithm effect and agreed that patch remains defensible. It independently confirmed the protected-file identity and passing core and profile evaluations.

The independent review did identify materialization cleanup rather than classification blockers:

- `validation-report.md` is an inherited version 1 report whose date, input path, decision count, reproduction commands, and closeout statement would be stale if presented as the current 1.0.1 validation record;
- the evaluation guide still labels itself as the accepted version 1 publication and uses `standards/v1` command paths;
- inherited decisions link to the old validation report and need repaired history links if that report is renamed or replaced;
- provisional candidate labels and fields must become exact 1.0.1 release metadata;
- site generation and verification remain hard-coded to the v1 source and route; and
- a candidate-stage `.gitignore` link resolves only after relocation, so links must be checked in the materialized publication location.

These findings do not raise the release classification. They are mandatory hygiene checks for [Materialize and verify the version-confirmed candidate](11-materialize-and-verify-versioned-candidate.md).

### Rejected alternatives and trade-offs

- **Minor `1.1`:** would be justified by a new compatible normative recommendation, capability, or conformance interpretation. The diff contains none; using a higher increment would overstate adopter impact without a supporting policy rationale.
- **Major `2`:** would require a previously conforming use to become nonconforming or an incompatible semantic interpretation. The deferred compound proposal work could have that future impact, but it is not implemented in this candidate.
- **No release change:** is unavailable because the successor intentionally changes released explanatory, profile, evaluation, evidence, and provenance content and adds the durable release record.
- **Patch without hygiene cleanup:** would preserve semantic compatibility but publish stale or ambiguous supporting material. The confirmed version is conditional on completing the explicit materialization audit before exact-bundle acceptance.

### Supporting and contradictory evidence

Supporting evidence is the complete diff, byte-identical protected artifacts, unchanged capability matrices, passing 13-group core suite, passing catalog check, passing 12-positive/11-negative profile self-test, explicit informative labels, traceability to the two resolved change items, and the independent falsification result.

The strongest contrary consideration is that Section 18 now says more plainly which compound operations cannot generally be represented. That wording could influence an adopter's claim, but it derives directly from the unchanged one-paragraph range target, one-adjacent-boundary target, immutable proposal identity, independent-proposal restriction, and atomic resolution semantics. It exposes an existing limit rather than narrowing a previously valid use.

### Uncertainty and follow-up

Patch classification assumes ticket 11 performs only mechanical version materialization, removal or explicit historical labeling of stale material, deduplication, link repair, and site-preview work. Any new normative recommendation, profile claim, schema change, capability activation, or semantic rewrite reopens this decision and requires a new complete-diff review.
