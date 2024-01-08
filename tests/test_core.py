"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

import typing as t

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_clinicaltrials.discover import metadata_to_json_schema
from tap_clinicaltrials.tap import TapClinicalTrials

SAMPLE_CONFIG: dict[str, t.Any] = {
    "start_date": "2023-06-01",
    "condition": "COVID-19",
    "sponsor": "Pfizer",
}

TestTapClinicalTrials = get_tap_test_class(
    TapClinicalTrials,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        max_records_limit=1000,
    ),
)


def test_metadata_to_json_schema() -> None:
    """Test metadata_to_json_schema."""
    metadata: list[dict[str, t.Any]] = [
        {
            "name": "field_1",
            "sourceType": "STRUCT",
            "type": "Field1",
            "children": [
                {
                    "name": "field_1_1",
                    "sourceType": "TEXT",
                    "type": "text",
                },
            ],
        },
        {
            "name": "field_2",
            "sourceType": "TEXT",
            "type": "text[]",
            "rules": "Required",
        },
        {
            "name": "field_3",
            "sourceType": "TEXT",
            "type": "text",
        },
        {
            "name": "field_4",
            "sourceType": "NUMERIC",
            "type": "number",
        },
    ]

    result = metadata_to_json_schema(metadata)
    assert result == {
        "type": "object",
        "properties": {
            "field_1": {
                "type": ["object", "null"],
                "properties": {
                    "field_1_1": {
                        "type": ["string", "null"],
                    },
                },
            },
            "field_2": {
                "type": "array",
                "items": {
                    "type": "string",
                },
            },
            "field_3": {
                "type": ["string", "null"],
            },
            "field_4": {
                "type": ["number", "null"],
            },
        },
    }
