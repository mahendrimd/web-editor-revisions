#!/usr/bin/env python3
"""Validate a reproducible Web Editor Revisions mapping-profile claim package."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "profile-claim.schema.json"
REQUIREMENTS_PATH = ROOT / "profile-requirements.json"
PUBLICATION_ROOT = ROOT.parent
CORE_CAPABILITIES = {
    "insert", "delete", "replace", "format", "paragraph-split", "paragraph-merge",
}
OUTPUT_PERSISTENCE_FIXTURES = {
    "native-save-reload-success",
    "native-clean-failure",
    "native-rollback",
    "native-partial-persistence",
}
MATRIX_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", re.MULTILINE)


class ClaimError(ValueError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ClaimError(f"cannot load {path}: {error}") from error


def validate_requirement_list(
    requirements: Any,
    label: str,
    activation: str,
    seen_ids: set[str],
    matrix: dict[str, str],
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(requirements, list) or (not requirements and not allow_empty):
        raise ClaimError(f"{label} must contain fixture requirements")
    for requirement in requirements:
        if not isinstance(requirement, dict) or set(requirement) != {"id", "description"}:
            raise ClaimError(f"{label} has a malformed requirement")
        fixture_id = requirement["id"]
        description = requirement["description"]
        if not isinstance(fixture_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fixture_id):
            raise ClaimError(f"{label} has an invalid fixture id")
        if fixture_id in seen_ids:
            raise ClaimError(f"duplicate fixture id in one direction: {fixture_id}")
        if not isinstance(description, str) or not description:
            raise ClaimError(f"catalog fixture {fixture_id} has no description")
        seen_ids.add(fixture_id)
        matrix[fixture_id] = activation


def validate_profile_matrix(profile: dict[str, Any], direction: dict[str, Any], expected: dict[str, str]) -> None:
    relative = Path(profile["document"])
    if relative.is_absolute():
        raise ClaimError(f"catalog profile document must be publication-relative: {relative}")
    document = (ROOT / relative).resolve()
    if not document.is_relative_to(PUBLICATION_ROOT) or not document.is_file():
        raise ClaimError(f"catalog profile document does not resolve inside the publication: {relative}")
    text = document.read_text(encoding="utf-8")
    direction_id = direction["id"]
    start_marker = f"<!-- profile-matrix:{direction_id}:start -->"
    end_marker = f"<!-- profile-matrix:{direction_id}:end -->"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise ClaimError(f"profile document has missing or duplicate matrix markers: {direction_id}")
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    observed: dict[str, str] = {}
    for fixture_id, activation in MATRIX_ROW.findall(text[start:end]):
        if fixture_id in observed:
            raise ClaimError(f"profile matrix repeats fixture {fixture_id}: {direction_id}")
        observed[fixture_id] = activation
    if observed != expected:
        missing = sorted(expected.keys() - observed.keys())
        extra = sorted(observed.keys() - expected.keys())
        changed = sorted(
            fixture_id
            for fixture_id in expected.keys() & observed.keys()
            if expected[fixture_id] != observed[fixture_id]
        )
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("extra " + ", ".join(extra))
        if changed:
            details.append("activation mismatch " + ", ".join(changed))
        raise ClaimError(f"catalog/profile matrix drift for {direction_id}: " + "; ".join(details))


def validate_catalog(catalog: dict[str, Any]) -> None:
    if catalog.get("catalogVersion") != "2":
        raise ClaimError("unsupported requirements catalog version")
    if not isinstance(catalog.get("coreChecks"), int) or catalog["coreChecks"] < 1:
        raise ClaimError("requirements catalog must declare a positive coreChecks value")

    profiles = catalog.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ClaimError("requirements catalog must contain profiles")

    seen_profiles: set[tuple[str, str]] = set()
    seen_directions: set[str] = set()
    for profile in profiles:
        if not isinstance(profile, dict):
            raise ClaimError("each catalog profile must be an object")
        if set(profile) != {"id", "version", "document", "directions"}:
            raise ClaimError("each catalog profile must have id, version, document, and directions")
        profile_key = (profile.get("id"), profile.get("version"))
        if not all(isinstance(value, str) and value for value in profile_key):
            raise ClaimError("each catalog profile needs a non-empty id and version")
        if profile_key in seen_profiles:
            raise ClaimError(f"duplicate catalog profile: {profile_key[0]} version {profile_key[1]}")
        seen_profiles.add(profile_key)

        if not isinstance(profile["document"], str) or not profile["document"]:
            raise ClaimError(f"catalog profile {profile_key[0]} has no profile document")
        directions = profile["directions"]
        if not isinstance(directions, list) or len(directions) != 2:
            raise ClaimError(f"catalog profile {profile_key[0]} must have two explicit directions")
        direction_kinds: set[str] = set()
        for direction in directions:
            if not isinstance(direction, dict) or set(direction) != {
                "id", "kind", "alwaysRequired", "capabilities", "sourcePersistence"
            }:
                raise ClaimError(f"catalog profile {profile_key[0]} has an invalid direction")
            direction_id = direction["id"]
            direction_kind = direction["kind"]
            if not isinstance(direction_id, str) or not direction_id:
                raise ClaimError(f"catalog profile {profile_key[0]} has an empty direction id")
            if direction_id in seen_directions:
                raise ClaimError(f"catalog direction is not unique: {direction_id}")
            seen_directions.add(direction_id)
            if direction_kind not in {"native-to-core", "core-to-native"}:
                raise ClaimError(f"catalog direction {direction_id} has an invalid kind")
            if direction_kind in direction_kinds:
                raise ClaimError(f"catalog profile {profile_key[0]} repeats direction kind {direction_kind}")
            direction_kinds.add(direction_kind)

            fixture_ids: set[str] = set()
            matrix: dict[str, str] = {}
            validate_requirement_list(
                direction["alwaysRequired"], direction_id, "always", fixture_ids, matrix
            )
            capabilities = direction["capabilities"]
            if not isinstance(capabilities, dict) or not capabilities:
                raise ClaimError(f"catalog direction {direction_id} has no capability matrices")
            unknown_capabilities = set(capabilities) - CORE_CAPABILITIES
            if unknown_capabilities:
                raise ClaimError(
                    f"catalog direction {direction_id} has unknown capabilities: "
                    + ", ".join(sorted(unknown_capabilities))
                )
            for capability, requirements in capabilities.items():
                validate_requirement_list(
                    requirements, f"{direction_id}/{capability}", capability, fixture_ids, matrix
                )
            validate_requirement_list(
                direction["sourcePersistence"],
                f"{direction_id}/source-persistence",
                "source-persistence",
                fixture_ids,
                matrix,
                allow_empty=True,
            )
            always_ids = {item["id"] for item in direction["alwaysRequired"]}
            if direction_kind == "core-to-native":
                if direction["sourcePersistence"]:
                    raise ClaimError(f"core-to-native direction {direction_id} cannot add source persistence")
                missing_persistence = OUTPUT_PERSISTENCE_FIXTURES - always_ids
                if missing_persistence:
                    raise ClaimError(
                        f"core-to-native direction {direction_id} omits mandatory persistence fixtures: "
                        + ", ".join(sorted(missing_persistence))
                    )
            elif not direction["sourcePersistence"]:
                raise ClaimError(f"native-to-core direction {direction_id} needs source-persistence fixtures")
            validate_profile_matrix(profile, direction, matrix)

        if direction_kinds != {"native-to-core", "core-to-native"}:
            raise ClaimError(f"catalog profile {profile_key[0]} lacks both direction kinds")


def required_fixture_ids(
    direction: dict[str, Any], capabilities: list[str], source_persistence_claimed: bool
) -> set[str]:
    required = {item["id"] for item in direction["alwaysRequired"]}
    for capability in capabilities:
        required.update(item["id"] for item in direction["capabilities"][capability])
    if source_persistence_claimed:
        required.update(item["id"] for item in direction["sourcePersistence"])
    return required


def parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ClaimError(f"invalid date-time: {value}") from error


def resolve_artifact(package_root: Path, artifact: dict[str, str]) -> Path:
    relative = Path(artifact["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ClaimError(f"artifact path must stay inside the claim package: {relative}")
    resolved = (package_root / relative).resolve()
    if not resolved.is_relative_to(package_root):
        raise ClaimError(f"artifact path escapes the claim package: {relative}")
    if not resolved.is_file():
        raise ClaimError(f"artifact does not exist: {relative}")
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    if digest != artifact["sha256"]:
        raise ClaimError(f"artifact hash mismatch: {relative}")
    return resolved


def validate_claim(claim_path: Path, schema: dict[str, Any], catalog: dict[str, Any]) -> None:
    claim = load_json(claim_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(claim), key=lambda error: list(error.absolute_path))
    if errors:
        path = "/".join(str(part) for part in errors[0].absolute_path) or "<root>"
        raise ClaimError(f"manifest schema violation at {path}: {errors[0].message}")

    started = parse_time(claim["run"]["startedAt"])
    finished = parse_time(claim["run"]["finishedAt"])
    if finished < started:
        raise ClaimError("run.finishedAt precedes run.startedAt")

    profile = next(
        (
            item
            for item in catalog["profiles"]
            if item["id"] == claim["profile"]["id"]
            and item["version"] == claim["profile"]["version"]
        ),
        None,
    )
    if profile is None:
        raise ClaimError("claim uses an unknown profile identifier or version")
    direction = next(
        (
            item
            for item in profile["directions"]
            if item["id"] == claim["profile"]["direction"]
        ),
        None,
    )
    if direction is None:
        raise ClaimError("claim direction is not defined by the selected profile")

    capabilities = claim["profile"]["capabilities"]
    unsupported_capabilities = sorted(set(capabilities) - direction["capabilities"].keys())
    if unsupported_capabilities:
        raise ClaimError(
            "claim uses capabilities not defined for the selected direction: "
            + ", ".join(unsupported_capabilities)
        )
    expected_scope = "proposal-mapping" if capabilities else "safety-only"
    if claim["profile"]["claimScope"] != expected_scope:
        raise ClaimError(
            f"claimScope must be {expected_scope} for the declared capabilities"
        )

    source_persistence_claimed = claim["boundary"]["sourcePersistenceClaimed"]
    if source_persistence_claimed and direction["kind"] != "native-to-core":
        raise ClaimError("source persistence can be claimed only for a native-to-core direction")
    if source_persistence_claimed and not direction["sourcePersistence"]:
        raise ClaimError("selected direction has no source-persistence fixture matrix")

    fixtures = claim["fixtures"]
    fixture_ids = [fixture["id"] for fixture in fixtures]
    if len(fixture_ids) != len(set(fixture_ids)):
        raise ClaimError("claim contains duplicate fixture identifiers")
    fixtures_by_id = {fixture["id"]: fixture for fixture in fixtures}
    required_ids = required_fixture_ids(
        direction, capabilities, source_persistence_claimed
    )
    missing = sorted(required_ids - fixtures_by_id.keys())
    if missing:
        raise ClaimError("claim omits required fixtures: " + ", ".join(missing))

    package_root = claim_path.resolve().parent
    artifacts = [claim["run"]["coreSuite"]["artifact"]]
    artifacts.extend(
        artifact
        for fixture in fixtures
        for artifact in fixture["artifacts"]
    )
    for artifact in artifacts:
        resolve_artifact(package_root, artifact)

    if claim["claimResult"] == "pass":
        core = claim["run"]["coreSuite"]
        expected_core_checks = catalog["coreChecks"]
        if core["total"] != expected_core_checks or core["passed"] != expected_core_checks:
            raise ClaimError(
                f"passing claim requires {expected_core_checks}/{expected_core_checks} core checks"
            )
        not_passed = sorted(
            fixture_id
            for fixture_id in required_ids
            if fixtures_by_id[fixture_id]["status"] != "passed"
        )
        if not_passed:
            raise ClaimError("passing claim has required fixtures not passed: " + ", ".join(not_passed))


def run_self_test(schema: dict[str, Any], catalog: dict[str, Any]) -> None:
    positive = 0
    negative = 0
    with tempfile.TemporaryDirectory() as directory_name:
        package_root = Path(directory_name)
        artifact_path = package_root / "observation.txt"
        artifact_path.write_text("profile claim self-test observation\n", encoding="utf-8")
        artifact = {
            "role": "log",
            "path": artifact_path.name,
            "sha256": hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
        }
        claim_path = package_root / "claim.json"

        def build_claim(
            profile: dict[str, Any],
            direction: dict[str, Any],
            capabilities: list[str],
            source_persistence_claimed: bool,
        ) -> dict[str, Any]:
            required_ids = sorted(
                required_fixture_ids(direction, capabilities, source_persistence_claimed)
            )
            return {
                "claimFormat": "web-editor-revisions-profile-claim-2",
                "publication": {
                    "commit": "0123456789abcdef",
                    "modelVersion": "1",
                    "serializationProfile": "json-jcs-1",
                },
                "profile": {
                    "id": profile["id"],
                    "version": profile["version"],
                    "direction": direction["id"],
                    "claimScope": "proposal-mapping" if capabilities else "safety-only",
                    "capabilities": capabilities,
                },
                "implementation": {"name": "claim-self-test", "version": "1"},
                "boundary": {
                    "upstreamVersion": "pinned-test-version",
                    "scope": "self-test boundary",
                    "persistence": "declared self-test persistence boundary",
                    "sourcePersistenceClaimed": source_persistence_claimed,
                },
                "run": {
                    "startedAt": "2026-08-18T00:00:00Z",
                    "finishedAt": "2026-08-18T00:00:01Z",
                    "environment": "validator self-test",
                    "coreSuite": {
                        "command": "published core suite",
                        "passed": catalog["coreChecks"],
                        "total": catalog["coreChecks"],
                        "artifact": artifact,
                    },
                },
                "fixtures": [
                    {
                        "id": fixture_id,
                        "status": "passed",
                        "expected": "activated profile requirement",
                        "observed": "self-test pass",
                        "artifacts": [artifact],
                    }
                    for fixture_id in required_ids
                ],
                "claimResult": "pass",
                "limitations": [],
            }

        def check(claim: dict[str, Any]) -> None:
            claim_path.write_text(json.dumps(claim), encoding="utf-8")
            validate_claim(claim_path, schema, catalog)

        def expect_error(claim: dict[str, Any], label: str) -> None:
            nonlocal negative
            try:
                check(claim)
            except ClaimError:
                negative += 1
                return
            raise ClaimError(f"self-test expected rejection: {label}")

        def expect_catalog_error(candidate: dict[str, Any], label: str) -> None:
            nonlocal negative
            try:
                validate_catalog(candidate)
            except ClaimError:
                negative += 1
                return
            raise ClaimError(f"self-test expected catalog rejection: {label}")

        native_example: tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None = None
        output_example: tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None = None
        odf_output: tuple[dict[str, Any], dict[str, Any]] | None = None
        for profile in catalog["profiles"]:
            for direction in profile["directions"]:
                capabilities = sorted(direction["capabilities"])
                source_persistence = direction["kind"] == "native-to-core"
                full_claim = build_claim(profile, direction, capabilities, source_persistence)
                check(full_claim)
                positive += 1

                safety_claim = build_claim(profile, direction, [], False)
                check(safety_claim)
                positive += 1

                missing = copy.deepcopy(full_claim)
                missing["fixtures"].pop()
                expect_error(missing, f"missing activated fixture for {direction['id']}")

                if native_example is None and direction["kind"] == "native-to-core":
                    native_example = (profile, direction, full_claim)
                if output_example is None and direction["kind"] == "core-to-native":
                    output_example = (profile, direction, full_claim)
                if direction["id"] == "core-to-odf-text":
                    odf_output = (profile, direction)

        assert native_example is not None and output_example is not None and odf_output is not None

        misleading_scope = build_claim(native_example[0], native_example[1], [], False)
        misleading_scope["profile"]["claimScope"] = "proposal-mapping"
        expect_error(misleading_scope, "misleading zero-capability scope")

        not_run = copy.deepcopy(native_example[2])
        not_run["fixtures"][0]["status"] = "not-run"
        expect_error(not_run, "not-run activated fixture in a passing claim")

        output_source_persistence = copy.deepcopy(output_example[2])
        output_source_persistence["boundary"]["sourcePersistenceClaimed"] = True
        expect_error(output_source_persistence, "source persistence on core-to-native direction")

        unknown_capability = build_claim(odf_output[0], odf_output[1], [], False)
        unknown_capability["profile"]["claimScope"] = "proposal-mapping"
        unknown_capability["profile"]["capabilities"] = ["format"]
        expect_error(unknown_capability, "capability absent from selected direction")

        drifted_catalog = copy.deepcopy(catalog)
        drifted_catalog["profiles"][0]["directions"][0]["alwaysRequired"][0]["id"] += "-drift"
        expect_catalog_error(drifted_catalog, "catalog/profile matrix drift")

    print(f"OK: profile claim self-test ({positive} positive, {negative} negative packages)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("claim", nargs="?", type=Path, help="path to a profile claim manifest")
    parser.add_argument(
        "--check-catalog",
        action="store_true",
        help="validate the published claim schema and requirements catalog only",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run positive and negative package tests for every profile direction",
    )
    args = parser.parse_args()

    try:
        schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        catalog = load_json(REQUIREMENTS_PATH)
        validate_catalog(catalog)
        if args.check_catalog and args.self_test:
            parser.error("--check-catalog and --self-test are mutually exclusive")
        if args.claim is not None and (args.check_catalog or args.self_test):
            parser.error("a claim path cannot be combined with --check-catalog or --self-test")
        if args.check_catalog:
            print("OK: profile claim schema and requirements catalog")
            return 0
        if args.self_test:
            run_self_test(schema, catalog)
            return 0
        if args.claim is None:
            parser.error("claim is required unless --check-catalog is used")
        validate_claim(args.claim.resolve(), schema, catalog)
        print(f"OK: {args.claim}")
        return 0
    except (ClaimError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
