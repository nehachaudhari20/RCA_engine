import json
from os import path
import yaml
import uuid
from datetime import datetime
from typing import List, Dict, Any

from adapters.base import DatasetAdapter
from core.schemas.event import Event


class MappingBasedAdapter(DatasetAdapter):
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def load_events(self) -> List[Event]:
        with open(self.config["raw_events_path"], "r") as f:
            rows = json.load(f)

        events = []
        for row in rows:
            for rule in self.config["event_mappings"]:
                if self._match_condition(row, rule["condition"]):
                    events.append(
                        Event(
                            event_id=str(uuid.uuid4()),
                            timestamp=self._parse_time(
                                row[self.config["timestamp_field"]]
                            ),
                            entity_id=row[self.config["entity_field"]],
                            event_type=rule["event_type"],
                            source=self.config["dataset_name"],
                            attributes=self._extract_attributes(row, rule),
                        )
                    )
        return events

    def load_dependency_graph(self) -> Dict[str, List[str]]:
        with open(self.config["dependency_graph_path"], "r") as f:
            return json.load(f)

    def load_incident_meta(self) -> dict:
        with open(self.config["incident_meta_path"], "r") as f:
            return json.load(f)

    def _match_condition(self, row: dict, condition: dict) -> bool:
        field_path = condition["field"]
        op = condition["op"]
        value = condition["value"]

        field_value = self._get_nested_value(row, field_path)

        if field_value is None:
            return False

        if op == ">":
            return field_value > value
        if op == "<":
            return field_value < value
        if op == "==":
            return field_value == value
        if op == "contains":
            return value in str(field_value)

        return False

    def _extract_attributes(self, row: dict, rule: dict) -> dict:
        attrs = {}
        for attr_key, field_path in rule.get("attributes", {}).items():
            attrs[attr_key] = self._get_nested_value(row, field_path)
        return attrs

    def _parse_time(self, ts: str) -> datetime:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    
    def _get_nested_value(self, data: dict, path: str):
        """
        Safely resolve dotted paths like 'attributes.latency_ms'
        from nested dictionaries.
        """
        current = data
        for part in path.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
            if current is None:
                return None
        return current
