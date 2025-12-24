import uuid
from datetime import timedelta
from typing import List

from core.schemas.event import Event
from core.schemas.normalized_event import NormalizedEvent

class EventNormalizer:
    def normalize(self, events: List[Event]) -> List[NormalizedEvent]:
        normalized = []

        for event in events:
            failure_type = self._map_failure_type(event)
            if not failure_type:
                continue  # ignore non-failure signals

            normalized.append(
                NormalizedEvent(
                    normalized_event_id=str(uuid.uuid4()),
                    entity=event.entity_id,
                    failure_type=failure_type,
                    severity=self._map_severity(event),
                    time_window_start=event.timestamp - timedelta(seconds=30),
                    time_window_end=event.timestamp + timedelta(seconds=30),
                    dimensions=self._extract_dimensions(event),
                    raw_event_ids=[event.event_id],
                )
            )
            print(f"[Normalizer] Raw event_type = {event.event_type}")


        return normalized

    def _map_failure_type(self, event: Event) -> str | None:
        mapping = {
            # latency
            "latency_spike": "latency_degradation",

        # dependency
            "dependency_timeout": "external_dependency_timeout",
            "external_call_timeout": "external_dependency_timeout",

        # errors
            "request_failure": "error_rate_increase",
            "error_rate_spike": "error_rate_increase",

        # resources
            "cpu_high": "resource_pressure",
            "memory_high": "resource_pressure",
        }
        return mapping.get(event.event_type)


    def _map_severity(self, event: Event) -> str:
        if event.event_type in ["dependency_timeout", "error_rate_spike"]:
            return "high"
        if event.event_type == "latency_spike":
            return "medium"
        return "low"

    def _extract_dimensions(self, event: Event) -> dict:
        dims = {}
        if "dependency" in event.attributes:
            dims["dependency"] = event.attributes["dependency"]
        return dims
