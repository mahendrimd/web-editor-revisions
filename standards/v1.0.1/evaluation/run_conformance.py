#!/usr/bin/env python3
"""Published executable fixtures for the Web Editor Revisions v1 subset."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT.parent / "schema" / "web-editor-revisions-v1.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "serialization-cases.json"
SAFE_INTEGER = 9_007_199_254_740_991
PROPERTIES = ("italic", "bold", "underline", "strikethrough")
FALSE_VALUES = {name: False for name in PROPERTIES}
LOSSY_ACTIONS = {"approximated", "omitted", "materialized"}
ISSUE_CONDITIONS = {
    "source-absent", "unsupported", "unavailable", "invalid-input",
    "precondition-failed", "persistence-failure", "other",
}
ISSUE_ACTIONS = {
    "synthesized", "normalized", "approximated", "omitted", "materialized",
    "refused", "rolled-back", "partially-committed", "other",
}
ISSUE_IMPACTS = {
    "none", "optional-information-loss", "review-semantics-loss",
    "transaction-integrity-failure",
}
RECOVERABILITY = {
    "not-applicable", "retryable", "requires-intervention", "irrecoverable", "unknown",
}
CORE_FIELDS = {
    "acceptedState.paragraphOrder", "acceptedState.paragraphIdentity", "acceptedState.text",
    "acceptedState.formatting", "acceptedState.fingerprint", "proposal.identity",
    "proposal.baseReference", "proposal.target", "proposal.kind", "proposal.payload",
    "proposal.samePointOrder", "proposal.relations", "proposal.reviewState",
    "proposal.provenance", "proposal.terminalCompleteness", "resolution.atomicity",
    "resolution.acceptanceProjection", "resolution.rejectionProjection",
    "resolution.pendingTargetRemapping", "mapping.persistence",
    "mapping.transactionIntegrity",
}
_SCHEMA: dict[str, Any] | None = None
_DOCUMENT_VALIDATOR: Draft202012Validator | None = None
_REPORT_VALIDATOR: Draft202012Validator | None = None


class ConformanceError(ValueError):
    pass


class DuplicateMemberError(ConformanceError):
    pass


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateMemberError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def parse_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=_object_without_duplicates,
        parse_float=lambda value: (_ for _ in ()).throw(ConformanceError(f"floating-point value forbidden: {value}")),
        parse_constant=lambda value: (_ for _ in ()).throw(ConformanceError(f"non-JSON number forbidden: {value}")),
    )


def _validators() -> tuple[Draft202012Validator, Draft202012Validator]:
    global _SCHEMA, _DOCUMENT_VALIDATOR, _REPORT_VALIDATOR
    if _SCHEMA is None:
        _SCHEMA = parse_json(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(_SCHEMA)
        _DOCUMENT_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())
        report_schema = {"$ref": "#/$defs/mappingReport", "$defs": _SCHEMA["$defs"]}
        _REPORT_VALIDATOR = Draft202012Validator(report_schema, format_checker=FormatChecker())
    assert _DOCUMENT_VALIDATOR is not None and _REPORT_VALIDATOR is not None
    return _DOCUMENT_VALIDATOR, _REPORT_VALIDATOR


def _raise_schema_errors(validator: Draft202012Validator, instance: Any, label: str) -> None:
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    if errors:
        path = "/".join(str(part) for part in errors[0].absolute_path)
        raise ConformanceError(f"{label} schema violation at {path or '<root>'}: {errors[0].message}")


def _utf16_sort_key(value: str) -> bytes:
    _assert_interoperable_string(value)
    return value.encode("utf-16-be")


def _assert_interoperable_string(value: str) -> None:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ConformanceError("isolated UTF-16 surrogate is forbidden") from error


def canonicalize(value: Any) -> bytes:
    """JCS for the deliberately narrow v1 value profile (no floats)."""

    def render(item: Any) -> str:
        if item is None:
            return "null"
        if item is True:
            return "true"
        if item is False:
            return "false"
        if isinstance(item, int):
            if abs(item) > SAFE_INTEGER:
                raise ConformanceError(f"integer outside interoperable safe range: {item}")
            return str(item)
        if isinstance(item, float):
            raise ConformanceError("floating-point values are forbidden by json-jcs-1")
        if isinstance(item, str):
            _assert_interoperable_string(item)
            return json.dumps(item, ensure_ascii=False, separators=(",", ":"))
        if isinstance(item, list):
            return "[" + ",".join(render(child) for child in item) + "]"
        if isinstance(item, dict):
            for key in item:
                if not isinstance(key, str):
                    raise ConformanceError("JSON object member names must be strings")
            members = sorted(item, key=_utf16_sort_key)
            return "{" + ",".join(render(key) + ":" + render(item[key]) for key in members) + "}"
        raise ConformanceError(f"unsupported JSON value type: {type(item).__name__}")

    return render(value).encode("utf-8")


def utf16_length(text: str) -> int:
    _assert_interoperable_string(text)
    return len(text.encode("utf-16-le")) // 2


def valid_utf16_boundaries(text: str) -> set[int]:
    result = {0}
    offset = 0
    for char in text:
        offset += 2 if ord(char) > 0xFFFF else 1
        result.add(offset)
    return result


def codepoint_index(text: str, offset: int) -> int:
    if offset not in valid_utf16_boundaries(text):
        raise ConformanceError(f"UTF-16 offset {offset} is not a Unicode code-point boundary")
    units = 0
    for index, char in enumerate(text):
        if units == offset:
            return index
        units += 2 if ord(char) > 0xFFFF else 1
    return len(text)


def false_values() -> dict[str, bool]:
    return dict(FALSE_VALUES)


def format_run(start: int, end: int, **values: bool) -> dict[str, Any]:
    effective = false_values()
    effective.update(values)
    return {"start": start, "end": end, "values": effective}


def plain_fragment(text: str, **values: bool) -> dict[str, Any]:
    length = utf16_length(text)
    return {
        "text": text,
        "formatting": [] if length == 0 else [format_run(0, length, **values)],
    }


def paragraph(identifier: str, text: str, **values: bool) -> dict[str, Any]:
    fragment = plain_fragment(text, **values)
    return {"id": identifier, **fragment}


def accepted_projection(accepted_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain": "web-editor-revisions.accepted-state",
        "modelVersion": "1",
        "serializationProfile": "json-jcs-1",
        "paragraphs": accepted_state["paragraphs"],
    }


def state_fingerprint(accepted_state: dict[str, Any]) -> str:
    digest = hashlib.sha256(canonicalize(accepted_projection(accepted_state))).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def make_document(paragraphs: list[dict[str, Any]], proposals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    state = {"fingerprint": "", "paragraphs": copy.deepcopy(paragraphs)}
    state["fingerprint"] = state_fingerprint(state)
    document = {
        "modelVersion": "1",
        "serializationProfile": "json-jcs-1",
        "acceptedState": state,
        "proposals": copy.deepcopy(proposals or []),
    }
    for proposal in document["proposals"]:
        if not proposal.get("baseFingerprint"):
            proposal["baseFingerprint"] = state["fingerprint"]
        proposal.setdefault("state", "pending")
    document["proposals"].sort(key=lambda proposal: _utf16_sort_key(proposal["id"]))
    return document


def point(paragraph_id: str, offset: int, association: str = "after") -> dict[str, Any]:
    return {"type": "point", "paragraphId": paragraph_id, "offset": offset, "association": association}


def range_target(
    paragraph_id: str,
    start: int,
    end: int,
    start_association: str = "after",
    end_association: str = "before",
) -> dict[str, Any]:
    return {
        "type": "range",
        "paragraphId": paragraph_id,
        "start": {"offset": start, "association": start_association},
        "end": {"offset": end, "association": end_association},
    }


def boundary(left: str, right: str) -> dict[str, Any]:
    return {"type": "paragraph-boundary", "leftParagraphId": left, "rightParagraphId": right}


def proposal(identifier: str, kind: str, **members: Any) -> dict[str, Any]:
    return {"id": identifier, "baseFingerprint": "", "state": "pending", "kind": kind, **members}


def _validate_formatting(text: str, runs: list[dict[str, Any]], context: str) -> None:
    length = utf16_length(text)
    boundaries = valid_utf16_boundaries(text)
    if length == 0:
        if runs:
            raise ConformanceError(f"{context}: empty text must have no formatting runs")
        return
    if not runs or runs[0]["start"] != 0 or runs[-1]["end"] != length:
        raise ConformanceError(f"{context}: formatting runs must partition the complete text")
    previous_end = 0
    previous_values = None
    for run in runs:
        start, end = run["start"], run["end"]
        if start != previous_end or end <= start or start not in boundaries or end not in boundaries:
            raise ConformanceError(f"{context}: formatting runs must be contiguous, non-empty, and boundary-valid")
        if run["values"] == previous_values:
            raise ConformanceError(f"{context}: adjacent identical formatting runs are not normalized")
        previous_end = end
        previous_values = run["values"]


def _paragraph_map(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in document["acceptedState"]["paragraphs"]}


def _extract_fragment(paragraph_value: dict[str, Any], start: int, end: int) -> dict[str, Any]:
    text = paragraph_value["text"]
    start_index, end_index = codepoint_index(text, start), codepoint_index(text, end)
    runs = []
    for run in paragraph_value["formatting"]:
        overlap_start = max(start, run["start"])
        overlap_end = min(end, run["end"])
        if overlap_start < overlap_end:
            runs.append({
                "start": overlap_start - start,
                "end": overlap_end - start,
                "values": copy.deepcopy(run["values"]),
            })
    return {"text": text[start_index:end_index], "formatting": runs}


def _format_values_at(paragraph_value: dict[str, Any], offset: int) -> dict[str, bool]:
    for run in paragraph_value["formatting"]:
        if run["start"] <= offset < run["end"]:
            return run["values"]
    raise ConformanceError(f"no formatting coverage at offset {offset}")


def validate_semantics(document: dict[str, Any], known_extensions: set[str] | None = None) -> None:
    document_validator, _ = _validators()
    _raise_schema_errors(document_validator, document, "document")
    known_extensions = known_extensions or set()
    if document["acceptedState"]["fingerprint"] != state_fingerprint(document["acceptedState"]):
        raise ConformanceError("accepted-state fingerprint mismatch")

    paragraph_ids: set[str] = set()
    for item in document["acceptedState"]["paragraphs"]:
        if item["id"] in paragraph_ids:
            raise ConformanceError(f"duplicate paragraph identity: {item['id']}")
        paragraph_ids.add(item["id"])
        _validate_formatting(item["text"], item["formatting"], f"paragraph {item['id']}")

    proposals = document["proposals"]
    expected_order = sorted(proposals, key=lambda item: _utf16_sort_key(item["id"]))
    if proposals != expected_order:
        raise ConformanceError("proposal array must use canonical UTF-16 identifier order")
    proposal_ids: set[str] = set()
    point_orders: set[tuple[str, int, str, int]] = set()
    paragraphs = _paragraph_map(document)
    for item in proposals:
        if item["id"] in proposal_ids:
            raise ConformanceError(f"duplicate proposal identity: {item['id']}")
        proposal_ids.add(item["id"])
        if item["state"] == "pending" and item["baseFingerprint"] != document["acceptedState"]["fingerprint"]:
            raise ConformanceError(f"proposal {item['id']}: stale base fingerprint")
        target = item["target"]
        kind = item["kind"]
        if target["type"] == "point":
            if target["paragraphId"] not in paragraphs:
                raise ConformanceError(f"proposal {item['id']}: unknown target paragraph")
            text = paragraphs[target["paragraphId"]]["text"]
            codepoint_index(text, target["offset"])
        elif target["type"] == "range":
            if target["paragraphId"] not in paragraphs:
                raise ConformanceError(f"proposal {item['id']}: unknown target paragraph")
            text = paragraphs[target["paragraphId"]]["text"]
            start, end = target["start"]["offset"], target["end"]["offset"]
            codepoint_index(text, start)
            codepoint_index(text, end)
            if end <= start:
                raise ConformanceError(f"proposal {item['id']}: range must be non-empty")
        else:
            ids = [value["id"] for value in document["acceptedState"]["paragraphs"]]
            left, right = target["leftParagraphId"], target["rightParagraphId"]
            if left not in ids or right not in ids or ids.index(right) != ids.index(left) + 1:
                raise ConformanceError(f"proposal {item['id']}: paragraph boundary is not adjacent")

        if kind == "insert":
            _validate_formatting(item["content"]["text"], item["content"]["formatting"], f"proposal {item['id']} content")
            if not item["content"]["text"]:
                raise ConformanceError(f"proposal {item['id']}: insertion is a no-op")
            key = (target["paragraphId"], target["offset"], target["association"], item["samePointOrder"])
            if key in point_orders:
                raise ConformanceError(f"proposal {item['id']}: duplicate same-point order")
            point_orders.add(key)
        elif kind == "delete":
            _validate_formatting(item["content"]["text"], item["content"]["formatting"], f"proposal {item['id']} content")
            actual = _extract_fragment(paragraphs[target["paragraphId"]], target["start"]["offset"], target["end"]["offset"])
            if actual != item["content"]:
                raise ConformanceError(f"proposal {item['id']}: deletion payload mismatch")
        elif kind == "replace":
            _validate_formatting(item["oldContent"]["text"], item["oldContent"]["formatting"], f"proposal {item['id']} oldContent")
            _validate_formatting(item["newContent"]["text"], item["newContent"]["formatting"], f"proposal {item['id']} newContent")
            if not item["oldContent"]["text"] or not item["newContent"]["text"]:
                raise ConformanceError(f"proposal {item['id']}: replacement payloads must be non-empty")
            actual = _extract_fragment(paragraphs[target["paragraphId"]], target["start"]["offset"], target["end"]["offset"])
            if actual != item["oldContent"]:
                raise ConformanceError(f"proposal {item['id']}: replacement old payload mismatch")
        elif kind == "format":
            paragraph_value = paragraphs[target["paragraphId"]]
            start, end = target["start"]["offset"], target["end"]["offset"]
            for property_name, change in item["changes"].items():
                if change["before"] == change["after"]:
                    raise ConformanceError(f"proposal {item['id']}: unchanged formatting value")
                cursor = start
                while cursor < end:
                    values = _format_values_at(paragraph_value, cursor)
                    if values[property_name] != change["before"]:
                        raise ConformanceError(f"proposal {item['id']}: formatting before value is not uniform")
                    run = next(run for run in paragraph_value["formatting"] if run["start"] <= cursor < run["end"])
                    cursor = min(end, run["end"])
        elif kind == "paragraph-split":
            if item["newRightParagraphId"] in paragraph_ids:
                raise ConformanceError(f"proposal {item['id']}: new right paragraph identity collides")

        _validate_extensions(item.get("extensions", {}), known_extensions)

    _validate_pending_compatibility(proposals)

    _validate_extensions(document.get("extensions", {}), known_extensions)
    for report in document.get("mappingReports", []):
        validate_mapping_report(report)


def _validate_pending_compatibility(proposals: list[dict[str, Any]]) -> None:
    pending = [item for item in proposals if item["state"] == "pending"]
    ranges: dict[str, list[tuple[int, int, str]]] = {}
    points: dict[str, list[tuple[int, str]]] = {}
    structural_ids: dict[str, str] = {}
    for item in pending:
        target = item["target"]
        if target["type"] == "range":
            ranges.setdefault(target["paragraphId"], []).append(
                (target["start"]["offset"], target["end"]["offset"], item["id"])
            )
        elif target["type"] == "point":
            points.setdefault(target["paragraphId"], []).append((target["offset"], item["id"]))
        if item["kind"] == "paragraph-split":
            affected = [target["paragraphId"], item["newRightParagraphId"]]
        elif item["kind"] == "paragraph-merge":
            affected = [target["leftParagraphId"], target["rightParagraphId"]]
        else:
            affected = []
        for paragraph_id in affected:
            if paragraph_id in structural_ids:
                raise ConformanceError(
                    f"proposals {structural_ids[paragraph_id]} and {item['id']}: incompatible structural targets"
                )
            structural_ids[paragraph_id] = item["id"]
    for paragraph_id, intervals in ranges.items():
        ordered = sorted(intervals)
        for (_, prior_end, prior_id), (start, _, item_id) in zip(ordered, ordered[1:]):
            if start < prior_end:
                raise ConformanceError(f"proposals {prior_id} and {item_id}: overlapping ranges are outside v1")
        for start, end, range_id in intervals:
            for offset, point_id in points.get(paragraph_id, []):
                if start < offset < end:
                    raise ConformanceError(
                        f"proposals {range_id} and {point_id}: dependent point inside consumed range is outside v1"
                    )


def _validate_extensions(extensions: dict[str, Any], known: set[str]) -> None:
    for identifier, entry in extensions.items():
        if entry["required"] and identifier not in known:
            raise ConformanceError(f"unknown required extension: {identifier}")


def _char_cells(fragment: dict[str, Any]) -> list[tuple[str, dict[str, bool]]]:
    cells = []
    offset = 0
    for char in fragment["text"]:
        values = _format_values_at(fragment, offset)
        cells.append((char, copy.deepcopy(values)))
        offset += 2 if ord(char) > 0xFFFF else 1
    return cells


def _fragment_from_cells(cells: list[tuple[str, dict[str, bool]]]) -> dict[str, Any]:
    text = "".join(char for char, _ in cells)
    if not cells:
        return {"text": "", "formatting": []}
    runs = []
    offset = 0
    run_start = 0
    current = cells[0][1]
    for index, (char, values) in enumerate(cells):
        if values != current:
            runs.append({"start": run_start, "end": offset, "values": copy.deepcopy(current)})
            run_start = offset
            current = values
        offset += 2 if ord(char) > 0xFFFF else 1
        if index == len(cells) - 1:
            runs.append({"start": run_start, "end": offset, "values": copy.deepcopy(current)})
    return {"text": text, "formatting": runs}


def _replace_fragment(paragraph_value: dict[str, Any], start: int, end: int, replacement: dict[str, Any]) -> None:
    cells = _char_cells(paragraph_value)
    start_index = codepoint_index(paragraph_value["text"], start)
    end_index = codepoint_index(paragraph_value["text"], end)
    result = _fragment_from_cells(cells[:start_index] + _char_cells(replacement) + cells[end_index:])
    paragraph_value.update(result)


def _apply_format(paragraph_value: dict[str, Any], start: int, end: int, changes: dict[str, Any]) -> None:
    cells = _char_cells(paragraph_value)
    start_index = codepoint_index(paragraph_value["text"], start)
    end_index = codepoint_index(paragraph_value["text"], end)
    for index in range(start_index, end_index):
        for property_name, change in changes.items():
            cells[index][1][property_name] = change["after"]
    paragraph_value.update(_fragment_from_cells(cells))


def _transform_offset(offset: int, association: str, operation: dict[str, Any]) -> int | None:
    target = operation["target"]
    if operation["kind"] == "insert":
        position = target["offset"]
        length = utf16_length(operation["content"]["text"])
        if offset > position or (offset == position and association == "after"):
            return offset + length
        return offset
    if operation["kind"] in {"delete", "replace"}:
        start, end = target["start"]["offset"], target["end"]["offset"]
        if start < offset < end:
            return None
        removed = end - start
        if offset >= end:
            offset -= removed
        elif offset == start:
            offset = start
        if operation["kind"] == "replace":
            inserted = utf16_length(operation["newContent"]["text"])
            if offset > start or (offset == start and association == "after"):
                offset += inserted
        return offset
    return offset


def _remap_target(target: dict[str, Any], operation: dict[str, Any], old_paragraphs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(target)
    kind = operation["kind"]
    op_target = operation["target"]
    if kind in {"insert", "delete", "replace"}:
        if target.get("paragraphId") != op_target["paragraphId"]:
            return result
        if target["type"] == "point":
            mapped = _transform_offset(target["offset"], target["association"], operation)
            if mapped is None:
                raise ConformanceError("pending point became unmappable")
            result["offset"] = mapped
        elif target["type"] == "range":
            for endpoint in ("start", "end"):
                source = target[endpoint]
                mapped = _transform_offset(source["offset"], source["association"], operation)
                if mapped is None:
                    raise ConformanceError("pending range became unmappable")
                result[endpoint]["offset"] = mapped
        return result
    if kind == "paragraph-split" and target.get("paragraphId") == op_target["paragraphId"]:
        split = op_target["offset"]

        def map_endpoint(endpoint: dict[str, Any]) -> tuple[str, int]:
            offset, association = endpoint["offset"], endpoint["association"]
            if offset < split or (offset == split and association == "before"):
                return op_target["paragraphId"], offset
            return operation["newRightParagraphId"], offset - split

        if target["type"] == "point":
            paragraph_id, offset = map_endpoint(target)
            result["paragraphId"], result["offset"] = paragraph_id, offset
        elif target["type"] == "range":
            start_id, start = map_endpoint(target["start"])
            end_id, end = map_endpoint(target["end"])
            if start_id != end_id:
                raise ConformanceError("pending range would cross a paragraph split")
            result["paragraphId"] = start_id
            result["start"]["offset"], result["end"]["offset"] = start, end
        return result
    if kind == "paragraph-merge":
        left = op_target["leftParagraphId"]
        right = op_target["rightParagraphId"]
        left_length = utf16_length(old_paragraphs[left]["text"])
        if target.get("paragraphId") == right:
            result["paragraphId"] = left
            if target["type"] == "point":
                result["offset"] += left_length
            elif target["type"] == "range":
                result["start"]["offset"] += left_length
                result["end"]["offset"] += left_length
        return result
    return result


def resolve(document: dict[str, Any], choices: dict[str, str], retain_terminal: bool = False) -> dict[str, Any]:
    original = copy.deepcopy(document)
    validate_semantics(original)
    by_id = {item["id"]: item for item in original["proposals"]}
    if not choices or any(identifier not in by_id for identifier in choices):
        raise ConformanceError("resolution request names an unknown or empty selection")
    if any(outcome not in {"accepted", "rejected"} for outcome in choices.values()):
        raise ConformanceError("resolution outcome must be accepted or rejected")
    if any(by_id[identifier]["state"] != "pending" for identifier in choices):
        raise ConformanceError("resolution can select only pending proposals")

    accepted = [by_id[identifier] for identifier, outcome in choices.items() if outcome == "accepted"]
    old_paragraphs = _paragraph_map(original)
    result = copy.deepcopy(original)
    paragraphs = result["acceptedState"]["paragraphs"]
    paragraph_by_id = {item["id"]: item for item in paragraphs}

    structural = [item for item in accepted if item["kind"] in {"paragraph-split", "paragraph-merge"}]
    if len(structural) > 1:
        raise ConformanceError("fixture harness rejects multiple structural operations in one transaction")

    edits_by_paragraph: dict[str, list[dict[str, Any]]] = {}
    for item in accepted:
        if item["kind"] in {"insert", "delete", "replace", "format"}:
            edits_by_paragraph.setdefault(item["target"]["paragraphId"], []).append(item)
    for paragraph_id, edits in edits_by_paragraph.items():
        def edit_key(item: dict[str, Any]) -> tuple[int, int]:
            target = item["target"]
            offset = target["offset"] if target["type"] == "point" else target["start"]["offset"]
            order = item.get("samePointOrder", 0)
            return offset, order

        for item in sorted(edits, key=edit_key, reverse=True):
            target = item["target"]
            paragraph_value = paragraph_by_id[paragraph_id]
            if item["kind"] == "insert":
                _replace_fragment(paragraph_value, target["offset"], target["offset"], item["content"])
            elif item["kind"] == "delete":
                _replace_fragment(paragraph_value, target["start"]["offset"], target["end"]["offset"], plain_fragment(""))
            elif item["kind"] == "replace":
                _replace_fragment(paragraph_value, target["start"]["offset"], target["end"]["offset"], item["newContent"])
            else:
                _apply_format(paragraph_value, target["start"]["offset"], target["end"]["offset"], item["changes"])

    if structural:
        item = structural[0]
        target = item["target"]
        if item["kind"] == "paragraph-split":
            source = paragraph_by_id[target["paragraphId"]]
            position = target["offset"]
            left = _extract_fragment(source, 0, position)
            right = _extract_fragment(source, position, utf16_length(source["text"]))
            source.update(left)
            new_paragraph = {"id": item["newRightParagraphId"], **right}
            index = paragraphs.index(source)
            paragraphs.insert(index + 1, new_paragraph)
        else:
            left = paragraph_by_id[target["leftParagraphId"]]
            right = paragraph_by_id[target["rightParagraphId"]]
            merged = _fragment_from_cells(_char_cells(left) + _char_cells(right))
            left.update(merged)
            paragraphs.remove(right)

    unresolved = []
    for item in result["proposals"]:
        if item["id"] in choices:
            if retain_terminal:
                item["state"] = choices[item["id"]]
                unresolved.append(item)
            continue
        if item["state"] == "pending":
            for applied in accepted:
                item["target"] = _remap_target(item["target"], applied, old_paragraphs)
            unresolved.append(item)
        else:
            unresolved.append(item)
    result["proposals"] = unresolved
    result["acceptedState"]["fingerprint"] = state_fingerprint(result["acceptedState"])
    for item in result["proposals"]:
        if item["state"] == "pending":
            item["baseFingerprint"] = result["acceptedState"]["fingerprint"]
    result["proposals"].sort(key=lambda item: _utf16_sort_key(item["id"]))
    validate_semantics(result)
    return result


def derive_mapping_outcome(report: dict[str, Any]) -> tuple[str, bool]:
    _, report_validator = _validators()
    _raise_schema_errors(report_validator, report, "mapping report")
    issues = report["issues"]
    mutation = report["outputMutation"]
    authorized = set(report["authorizedActions"])
    if any(issue["condition"] not in ISSUE_CONDITIONS for issue in issues):
        raise ConformanceError("unknown core condition")
    if any(issue["action"] not in ISSUE_ACTIONS for issue in issues):
        raise ConformanceError("unknown core action")
    if any(issue["impact"] not in ISSUE_IMPACTS for issue in issues):
        raise ConformanceError("unknown core impact")
    if any(issue["recoverability"] not in RECOVERABILITY for issue in issues):
        raise ConformanceError("unknown recoverability")
    if any(
        field not in CORE_FIELDS and not urlsplit(field).scheme
        for issue in issues
        for field in issue["fields"]
    ):
        raise ConformanceError("affected field must be a core identifier or absolute URI")
    if any((issue["condition"] == "other" or issue["action"] == "other") and not issue.get("extensionId") for issue in issues):
        raise ConformanceError("other condition or action requires an extension identifier")
    if any(issue["impact"] == "none" and issue["recoverability"] != "not-applicable" for issue in issues):
        raise ConformanceError("no-impact issue must use not-applicable recoverability")

    transaction_failure = mutation == "residual-invalid" or any(
        issue["impact"] == "transaction-integrity-failure" or issue["action"] == "partially-committed"
        for issue in issues
    )
    if transaction_failure:
        return "failed", False
    if mutation == "none":
        if not issues:
            raise ConformanceError("a no-mutation mapping needs an explanatory issue")
        if any(issue["condition"] in {"invalid-input", "precondition-failed", "persistence-failure"} for issue in issues):
            return "failed", True
        return "unsupported", True
    if not issues:
        return "equivalent", mutation == "valid-complete"
    if all(issue["impact"] == "none" and issue["action"] in {"synthesized", "normalized"} for issue in issues):
        return "equivalent-with-declared-adaptation", mutation == "valid-complete"
    if mutation not in {"valid-lossy", "valid-complete"}:
        return "failed", False
    used_lossy_actions = {issue["action"] for issue in issues if issue["action"] in LOSSY_ACTIONS}
    conforming = bool(used_lossy_actions) and used_lossy_actions <= authorized
    return "lossy", conforming


def validate_mapping_report(report: dict[str, Any]) -> None:
    outcome, _ = derive_mapping_outcome(report)
    if report["outcome"] != outcome:
        raise ConformanceError(f"mapping report claims {report['outcome']} but derives {outcome}")


def issue(
    condition: str,
    action: str,
    impact: str,
    recoverability: str,
    field: str = "proposal.identity",
    **extra: Any,
) -> dict[str, Any]:
    return {
        "stage": "round-trip",
        "fields": [field],
        "condition": condition,
        "action": action,
        "impact": impact,
        "recoverability": recoverability,
        "expected": "preserved",
        "observed": "fixture observation",
        **extra,
    }


def report(
    issues: list[dict[str, Any]],
    mutation: str,
    authorized: list[str] | None = None,
    claimed: str | None = None,
) -> dict[str, Any]:
    value = {
        "id": "report-1",
        "adapter": {"id": "fixture-adapter", "version": "1"},
        "profile": {"id": "fixture-profile", "version": "1"},
        "direction": "canonical-to-native-to-canonical",
        "boundary": "save-reload",
        "inputRef": "sha256:input",
        "outputRef": None if mutation == "none" else "sha256:output",
        "outputMutation": mutation,
        "authorizedActions": authorized or [],
        "outcome": "failed",
        "issues": issues,
    }
    derived, _ = derive_mapping_outcome(value)
    value["outcome"] = claimed or derived
    return value


@dataclass
class TestCase:
    name: str
    function: Callable[[], None]


TESTS: list[TestCase] = []


def fixture(name: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
    def register(function: Callable[[], None]) -> Callable[[], None]:
        TESTS.append(TestCase(name, function))
        return function
    return register


def expect_error(function: Callable[[], Any], contains: str | None = None) -> None:
    try:
        function()
    except (ConformanceError, DuplicateMemberError, json.JSONDecodeError) as error:
        if contains and contains not in str(error):
            raise AssertionError(f"expected error containing {contains!r}, got {error!r}") from error
        return
    raise AssertionError("expected conformance error")


def assert_texts(document: dict[str, Any], expected: list[tuple[str, str]]) -> None:
    actual = [(item["id"], item["text"]) for item in document["acceptedState"]["paragraphs"]]
    assert actual == expected, (actual, expected)


@fixture("schema and canonical insertion file")
def test_serialization_file() -> None:
    bundle = parse_json(FIXTURE_PATH.read_text(encoding="utf-8"))
    schema = parse_json(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    canonical_document = bundle["canonicalDocument"]
    errors = list(validator.iter_errors(canonical_document))
    assert not errors, errors
    validate_semantics(canonical_document)
    assert canonicalize(canonical_document).decode("utf-8") == bundle["canonicalBytes"]
    reordered = parse_json(bundle["reorderedJson"])
    assert canonicalize(reordered) == canonicalize(canonical_document)
    assert state_fingerprint(canonical_document["acceptedState"]) == bundle["acceptedStateFingerprint"]


@fixture("duplicate members, floats, unsafe integers, and isolated surrogates")
def test_strict_json_profile() -> None:
    expect_error(lambda: parse_json('{"a":1,"a":2}'), "duplicate")
    expect_error(lambda: parse_json('{"a":1.5}'), "floating")
    expect_error(lambda: canonicalize({"n": SAFE_INTEGER + 1}), "safe range")
    expect_error(lambda: canonicalize({"text": "\ud800"}), "surrogate")


@fixture("fingerprint projection excludes proposals and reports")
def test_fingerprint_projection() -> None:
    document = make_document([paragraph("p1", "A😀B")])
    baseline = document["acceptedState"]["fingerprint"]
    document["proposals"] = [proposal("x", "insert", target=point("p1", 1), content=plain_fragment("!"), samePointOrder=0)]
    document["proposals"][0]["baseFingerprint"] = baseline
    document["mappingReports"] = [report([], "valid-complete")]
    assert state_fingerprint(document["acceptedState"]) == baseline


@fixture("insertion, deletion, replacement, mixed resolution, and exact projections")
def test_text_operations() -> None:
    base = paragraph("p1", "The red fox waits.")
    document = make_document([base], [
        proposal("a-insert", "insert", target=point("p1", 8, "after"), content=plain_fragment("quick ", italic=True), samePointOrder=0),
        proposal("b-delete", "delete", target=range_target("p1", 4, 8), content=plain_fragment("red ")),
        proposal("c-replace", "replace", target=range_target("p1", 12, 17), oldContent=plain_fragment("waits"), newContent=plain_fragment("runs", bold=True)),
    ])
    validate_semantics(document)
    mixed = resolve(document, {"a-insert": "accepted", "b-delete": "rejected", "c-replace": "accepted"})
    assert_texts(mixed, [("p1", "The red quick fox runs.")])
    rejected = resolve(document, {item["id"]: "rejected" for item in document["proposals"]})
    assert_texts(rejected, [("p1", "The red fox waits.")])


@fixture("all core formatting properties, removal, and atomic multi-property formatting")
def test_formatting_operations() -> None:
    document = make_document([
        paragraph("p-bold", "bold"), paragraph("p-italic", "italic", italic=True),
        paragraph("p-under", "under"), paragraph("p-strike", "strike"),
        paragraph("p-multi", "multi"),
    ], [
        proposal("f-bold", "format", target=range_target("p-bold", 0, 4), changes={"bold": {"before": False, "after": True}}),
        proposal("f-italic-remove", "format", target=range_target("p-italic", 0, 6), changes={"italic": {"before": True, "after": False}}),
        proposal("f-multi", "format", target=range_target("p-multi", 0, 5), changes={"bold": {"before": False, "after": True}, "underline": {"before": False, "after": True}}),
        proposal("f-strike", "format", target=range_target("p-strike", 0, 6), changes={"strikethrough": {"before": False, "after": True}}),
        proposal("f-under", "format", target=range_target("p-under", 0, 5), changes={"underline": {"before": False, "after": True}}),
    ])
    result = resolve(document, {item["id"]: "accepted" for item in document["proposals"]})
    values = {item["id"]: item["formatting"][0]["values"] for item in result["acceptedState"]["paragraphs"]}
    assert values["p-bold"]["bold"] is True
    assert values["p-italic"]["italic"] is False
    assert values["p-under"]["underline"] is True
    assert values["p-strike"]["strikethrough"] is True
    assert values["p-multi"]["bold"] and values["p-multi"]["underline"]


@fixture("endpoint splits and empty-paragraph merges retain left identity")
def test_structural_operations() -> None:
    for offset, expected in [(0, [("p1", ""), ("right", "abc")]), (3, [("p1", "abc"), ("right", "")])]:
        document = make_document([paragraph("p1", "abc")], [
            proposal("split", "paragraph-split", target=point("p1", offset), newRightParagraphId="right")
        ])
        result = resolve(document, {"split": "accepted"})
        assert_texts(result, expected)
    merge = make_document([paragraph("left", ""), paragraph("right", "abc")], [
        proposal("merge", "paragraph-merge", target=boundary("left", "right"))
    ])
    assert_texts(resolve(merge, {"merge": "accepted"}), [("left", "abc")])


@fixture("same-point ordering and before/after successor attachment")
def test_same_point_order_and_association() -> None:
    document = make_document([paragraph("p1", "AB")], [
        proposal("a", "insert", target=point("p1", 1, "after"), content=plain_fragment("x"), samePointOrder=0),
        proposal("b", "insert", target=point("p1", 1, "after"), content=plain_fragment("y"), samePointOrder=1),
        proposal("pending-after", "insert", target=point("p1", 1, "after"), content=plain_fragment("z"), samePointOrder=2),
        proposal("pending-before", "insert", target=point("p1", 1, "before"), content=plain_fragment("w"), samePointOrder=0),
    ])
    result = resolve(document, {"a": "accepted", "b": "accepted"})
    assert_texts(result, [("p1", "AxyB")])
    remaining = {item["id"]: item for item in result["proposals"]}
    assert remaining["pending-after"]["target"]["offset"] == 3
    assert remaining["pending-before"]["target"]["offset"] == 1


@fixture("operation-specific pending-target remapping")
def test_remapping_rules() -> None:
    deletion = make_document([paragraph("p1", "abcdef")], [
        proposal("delete", "delete", target=range_target("p1", 1, 3), content=plain_fragment("bc")),
        proposal("pending", "insert", target=point("p1", 5), content=plain_fragment("!"), samePointOrder=0),
    ])
    after_delete = resolve(deletion, {"delete": "accepted"})
    assert next(item for item in after_delete["proposals"] if item["id"] == "pending")["target"]["offset"] == 3

    replacement = make_document([paragraph("p1", "abcdef")], [
        proposal("pending", "insert", target=point("p1", 6), content=plain_fragment("!"), samePointOrder=0),
        proposal("replace", "replace", target=range_target("p1", 1, 3), oldContent=plain_fragment("bc"), newContent=plain_fragment("WXYZ")),
    ])
    after_replace = resolve(replacement, {"replace": "accepted"})
    assert next(item for item in after_replace["proposals"] if item["id"] == "pending")["target"]["offset"] == 8

    split = make_document([paragraph("p1", "abcdef")], [
        proposal("pending", "insert", target=point("p1", 5), content=plain_fragment("!"), samePointOrder=0),
        proposal("split", "paragraph-split", target=point("p1", 3), newRightParagraphId="right"),
    ])
    after_split = resolve(split, {"split": "accepted"})
    pending = next(item for item in after_split["proposals"] if item["id"] == "pending")
    assert (pending["target"]["paragraphId"], pending["target"]["offset"]) == ("right", 2)

    merge = make_document([paragraph("left", "abc"), paragraph("right", "def")], [
        proposal("merge", "paragraph-merge", target=boundary("left", "right")),
        proposal("pending", "insert", target=point("right", 2), content=plain_fragment("!"), samePointOrder=0),
    ])
    after_merge = resolve(merge, {"merge": "accepted"})
    pending = next(item for item in after_merge["proposals"] if item["id"] == "pending")
    assert (pending["target"]["paragraphId"], pending["target"]["offset"]) == ("left", 5)

    formatting = make_document([paragraph("p1", "abcdef")], [
        proposal("format", "format", target=range_target("p1", 0, 2), changes={"italic": {"before": False, "after": True}}),
        proposal("pending", "insert", target=point("p1", 5), content=plain_fragment("!"), samePointOrder=0),
    ])
    after_format = resolve(formatting, {"format": "accepted"})
    pending = next(item for item in after_format["proposals"] if item["id"] == "pending")
    assert pending["target"]["offset"] == 5


@fixture("identity persists through canonical bytes and terminal retention is optional")
def test_identity_and_terminal_retention() -> None:
    document = make_document([paragraph("p1", "ab")], [
        proposal("stable-id", "insert", target=point("p1", 1), content=plain_fragment("X"), samePointOrder=0)
    ])
    reloaded = parse_json(canonicalize(document).decode("utf-8"))
    validate_semantics(reloaded)
    assert reloaded["proposals"][0]["id"] == "stable-id"
    omitted = resolve(reloaded, {"stable-id": "accepted"}, retain_terminal=False)
    retained = resolve(reloaded, {"stable-id": "accepted"}, retain_terminal=True)
    assert omitted["proposals"] == []
    assert retained["proposals"][0]["state"] == "accepted"
    assert retained["proposals"][0]["baseFingerprint"] == document["acceptedState"]["fingerprint"]


@fixture("stale base, payload mismatch, no-op, surrogate boundary, and unknown required extension")
def test_semantic_invalid_cases() -> None:
    stale = make_document([paragraph("p1", "abc")], [
        proposal("x", "insert", target=point("p1", 1), content=plain_fragment("!"), samePointOrder=0)
    ])
    stale["proposals"][0]["baseFingerprint"] = "A" * 43
    before = copy.deepcopy(stale)
    expect_error(lambda: validate_semantics(stale), "stale")
    expect_error(lambda: resolve(stale, {"x": "accepted"}), "stale")
    assert stale == before and stale["proposals"][0]["state"] == "pending"

    mismatch = make_document([paragraph("p1", "abc")], [
        proposal("x", "delete", target=range_target("p1", 0, 1), content=plain_fragment("z"))
    ])
    expect_error(lambda: validate_semantics(mismatch), "payload mismatch")

    no_op = make_document([paragraph("p1", "abc")], [
        proposal("x", "format", target=range_target("p1", 0, 1), changes={"bold": {"before": False, "after": False}})
    ])
    expect_error(lambda: validate_semantics(no_op), "unchanged")

    surrogate = make_document([paragraph("p1", "A😀B")], [
        proposal("x", "insert", target=point("p1", 2), content=plain_fragment("!"), samePointOrder=0)
    ])
    expect_error(lambda: validate_semantics(surrogate), "code-point boundary")

    extension = make_document([paragraph("p1", "abc")])
    extension["extensions"] = {"https://example.test/unknown": {"required": True, "value": {}}}
    expect_error(lambda: validate_semantics(extension), "unknown required")


@fixture("closed formatting vocabulary, coverage integrity, proposal order, compatibility, and optional extensions")
def test_closed_and_normalized_semantics() -> None:
    unsupported_property = make_document([paragraph("p1", "abc")], [
        proposal("x", "format", target=range_target("p1", 0, 1), changes={"color": {"before": False, "after": True}})
    ])
    expect_error(lambda: validate_semantics(unsupported_property), "schema violation")

    unavailable_before = make_document([paragraph("p1", "abc")], [
        proposal("x", "format", target=range_target("p1", 0, 1), changes={"bold": {"after": True}})
    ])
    expect_error(lambda: validate_semantics(unavailable_before), "schema violation")

    bad_coverage = make_document([paragraph("p1", "abc")])
    bad_coverage["acceptedState"]["paragraphs"][0]["formatting"] = [format_run(0, 2)]
    bad_coverage["acceptedState"]["fingerprint"] = state_fingerprint(bad_coverage["acceptedState"])
    expect_error(lambda: validate_semantics(bad_coverage), "partition")

    formatting_mismatch = make_document([paragraph("p1", "abc", bold=True)], [
        proposal("x", "delete", target=range_target("p1", 0, 1), content=plain_fragment("a"))
    ])
    expect_error(lambda: validate_semantics(formatting_mismatch), "payload mismatch")

    unsorted = make_document([paragraph("p1", "abc")], [
        proposal("a", "insert", target=point("p1", 0), content=plain_fragment("a"), samePointOrder=0),
        proposal("b", "insert", target=point("p1", 3), content=plain_fragment("b"), samePointOrder=0),
    ])
    unsorted["proposals"].reverse()
    expect_error(lambda: validate_semantics(unsorted), "canonical UTF-16")

    overlap = make_document([paragraph("p1", "abcdef")], [
        proposal("a", "delete", target=range_target("p1", 0, 3), content=plain_fragment("abc")),
        proposal("b", "format", target=range_target("p1", 2, 4), changes={"bold": {"before": False, "after": True}}),
    ])
    expect_error(lambda: validate_semantics(overlap), "overlapping")

    optional_extension = make_document([paragraph("p1", "abc")])
    optional_extension["extensions"] = {"https://example.test/optional": {"required": False, "value": {"opaque": "kept"}}}
    validate_semantics(optional_extension)
    round_trip = parse_json(canonicalize(optional_extension).decode("utf-8"))
    assert round_trip["extensions"] == optional_extension["extensions"]


@fixture("mapping outcomes are derived and every core vocabulary value is executable")
def test_mapping_outcomes_and_vocabularies() -> None:
    equivalent = report([], "valid-complete")
    assert derive_mapping_outcome(equivalent) == ("equivalent", True)

    synthesis = report([issue("source-absent", "synthesized", "none", "not-applicable")], "valid-complete")
    assert derive_mapping_outcome(synthesis) == ("equivalent-with-declared-adaptation", True)
    normalization = report([issue("source-absent", "normalized", "none", "not-applicable", field="acceptedState.formatting")], "valid-complete")
    assert derive_mapping_outcome(normalization) == ("equivalent-with-declared-adaptation", True)
    extension_field = report([issue("source-absent", "synthesized", "none", "not-applicable", field="urn:example:field")], "valid-complete")
    assert derive_mapping_outcome(extension_field) == ("equivalent-with-declared-adaptation", True)
    expect_error(
        lambda: report([issue("source-absent", "normalized", "none", "not-applicable", field="accepted.formatting")], "valid-complete"),
        "affected field",
    )

    optional_loss = report([issue("unavailable", "omitted", "optional-information-loss", "irrecoverable", field="proposal.provenance")], "valid-lossy", ["omitted"])
    assert derive_mapping_outcome(optional_loss) == ("lossy", True)
    replacement_loss = report([issue("unsupported", "approximated", "review-semantics-loss", "requires-intervention", field="proposal.relations")], "valid-lossy", ["approximated"])
    assert derive_mapping_outcome(replacement_loss) == ("lossy", True)
    materialized = report([issue("unsupported", "materialized", "review-semantics-loss", "irrecoverable", field="proposal.reviewState")], "valid-lossy", ["materialized"])
    assert derive_mapping_outcome(materialized) == ("lossy", True)

    refused = report([issue("unsupported", "refused", "review-semantics-loss", "requires-intervention")], "none")
    assert derive_mapping_outcome(refused) == ("unsupported", True)
    rollback = report([issue("precondition-failed", "rolled-back", "review-semantics-loss", "retryable")], "none")
    assert derive_mapping_outcome(rollback) == ("failed", True)
    partial = report([issue("persistence-failure", "partially-committed", "transaction-integrity-failure", "unknown", field="mapping.transactionIntegrity")], "residual-invalid")
    assert derive_mapping_outcome(partial) == ("failed", False)

    for condition in ISSUE_CONDITIONS:
        action = "other" if condition == "other" else "refused"
        extra = {"extensionId": "https://example.test/condition"} if condition == "other" else {}
        candidate = issue(condition, action, "review-semantics-loss", "requires-intervention", **extra)
        if action == "other":
            candidate["extensionId"] = "https://example.test/condition"
        derive_mapping_outcome(report([candidate], "none"))
    for action in ISSUE_ACTIONS:
        extra = {"extensionId": "https://example.test/action"} if action == "other" else {}
        impact = "transaction-integrity-failure" if action == "partially-committed" else "review-semantics-loss"
        mutation = "residual-invalid" if action == "partially-committed" else ("none" if action in {"refused", "rolled-back", "other"} else "valid-lossy")
        authorized = [action] if action in LOSSY_ACTIONS else []
        derive_mapping_outcome(report([issue("unsupported", action, impact, "unknown", **extra)], mutation, authorized))
    for recoverability in RECOVERABILITY - {"not-applicable"}:
        derive_mapping_outcome(report([issue("unsupported", "refused", "review-semantics-loss", recoverability)], "none"))


@fixture("unauthorized and silent loss cannot claim conformance")
def test_invalid_loss_reporting() -> None:
    unauthorized = report([issue("unavailable", "omitted", "review-semantics-loss", "irrecoverable")], "valid-lossy")
    assert derive_mapping_outcome(unauthorized) == ("lossy", False)
    silent = report([], "valid-lossy")
    assert derive_mapping_outcome(silent) == ("equivalent", False)
    misleading = report([issue("unavailable", "omitted", "review-semantics-loss", "irrecoverable")], "valid-lossy", ["omitted"], claimed="equivalent")
    expect_error(lambda: validate_mapping_report(misleading), "derives lossy")


def load_schema() -> dict[str, Any]:
    _validators()
    assert _SCHEMA is not None
    return _SCHEMA


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="list fixture checks")
    args = parser.parse_args()
    load_schema()
    if args.list:
        for case in TESTS:
            print(case.name)
        return 0
    failures = []
    for case in TESTS:
        try:
            case.function()
            print(f"PASS {case.name}")
        except Exception as error:  # fixture runner must continue to show the complete matrix
            failures.append((case.name, error))
            print(f"FAIL {case.name}: {error}", file=sys.stderr)
    print(f"\n{len(TESTS) - len(failures)}/{len(TESTS)} checks passed")
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
