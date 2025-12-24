import uuid
from typing import List
from core.schemas.pattern import Pattern
from core.schemas.normalized_event import NormalizedEvent
from core.pattern_detection.base import PatternDetector


class CorrelationPatternDetector(PatternDetector):
    def __init__(self, dependency_graph: dict):
        self.graph = dependency_graph

    def detect(self, events: List[NormalizedEvent]) -> List[Pattern]:
        patterns = []

        for e in events:
            upstreams = self.graph.get(e.entity, [])
            for u in upstreams:
                for other in events:
                    if other.entity == u:
                        patterns.append(
                            Pattern(
                                pattern_id=str(uuid.uuid4()),
                                pattern_type="correlation",
                                description=(
                                    f"Failure propagated from {e.entity} "
                                    f"to upstream service {u}"
                                ),
                                confidence=0.6,
                                supporting_event_ids=[
                                    e.normalized_event_id,
                                    other.normalized_event_id,
                                ],
                            )
                        )
        return patterns


"""
Correlation pattern detector.

Identifies failure events that share common attributes such as dependencies
or dimensions. Correlated failures provide evidence that multiple anomalies
may be related to the same underlying factor.

Correlation patterns are later combined with temporal and structural evidence
to assess root cause likelihood.
"""
