"""Utilities for converting the studies data models fields to JSON schema."""

from __future__ import annotations

import typing as t


def _metadata_type_to_json_schema_type(metadata_type: str) -> dict[str, t.Any]:  # noqa: PLR0911
    """Convert a metadata type to a json schema type."""
    if metadata_type == "text":
        return {"type": "string"}
    if metadata_type == "integer":
        return {"type": "integer"}
    if metadata_type in "number":
        return {"type": "number"}
    if metadata_type == "long":
        return {"type": "integer"}
    if metadata_type == "boolean":
        return {"type": "boolean"}
    if metadata_type == "NormalizedDate":
        return {"type": "string", "format": "date"}
    if metadata_type == "DateTimeMinutes":
        return {"type": "string", "format": "date-time"}
    if metadata_type == "GeoPoint":
        return {"type": "object", "properties": {"lat": {"type": "number"}, "lon": {"type": "number"}}}

    return {"type": "string"}


def _metadata_item_to_json_schema(item: dict[str, t.Any]) -> dict[str, t.Any]:
    data_type = item["type"]
    rules = item.get("rules")

    if data_type.endswith("[]"):
        result = {
            "type": "array" if rules == "Required" else ["array", "null"],
            "items": _metadata_item_to_json_schema({**item, "type": data_type[:-2]}),
        }
        if "title" in item:
            result["title"] = item["title"]

        if "definition" in item:
            result["description"] = item["definition"]

        return result

    if item["sourceType"] == "STRUCT":
        return {
            "type": "object" if rules == "Required" else ["object", "null"],
            "properties": {child["name"]: _metadata_item_to_json_schema(child) for child in item["children"]},
        }

    result = _metadata_type_to_json_schema_type(data_type)
    if "title" in item:
        result["title"] = item["title"]

    if "definition" in item:
        result["description"] = item["definition"]

    if rules != "Required":
        result["type"] = [result["type"], "null"]  # type: ignore[list-item]

    return result


def metadata_to_json_schema(metadata: list[dict[str, t.Any]]) -> dict[str, t.Any]:
    """Convert a metadata response to a JSON schema."""
    return {
        "type": "object",
        "properties": {item["name"]: _metadata_item_to_json_schema(item) for item in metadata},
    }
