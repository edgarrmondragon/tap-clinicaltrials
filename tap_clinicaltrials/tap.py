"""ClinicalTrials.gov tap class."""

from __future__ import annotations

import typing as t

import requests
from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_clinicaltrials import streams
from tap_clinicaltrials.discover import metadata_to_json_schema


class TapClinicalTrials(Tap):
    """Singer tap for ClinicalTrials.gov."""

    name = "tap-clinicaltrials"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateType,
            description="Earliest date to get data from",
        ),
        th.Property(
            "condition",
            th.StringType,
            description="Conditions or disease query",
        ),
        th.Property(
            "sponsor",
            th.StringType,
            description="Sponsor query",
        ),
    ).to_dict()

    def get_studies_schema(self) -> dict[str, t.Any]:
        """Return a JSON Schema dict for the studies stream."""
        response = requests.get("https://clinicaltrials.gov/api/v2/studies/metadata", timeout=10)
        response.raise_for_status()

        upstream_schema = metadata_to_json_schema(response.json())
        upstream_schema["properties"].update(
            {
                "lastUpdateSubmitDate": upstream_schema["properties"]["protocolSection"]["properties"]["statusModule"]["properties"]["lastUpdateSubmitDate"],
                "nctId": upstream_schema["properties"]["protocolSection"]["properties"]["identificationModule"]["properties"]["nctId"],
            },
        )
        return upstream_schema

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of ClinicalTrials.gov streams.
        """
        return [streams.Studies(tap=self, schema=self.get_studies_schema())]
