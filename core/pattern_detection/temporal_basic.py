import uuid
from collections import defaultdict
from typing import List

from core.schemas.pattern import Pattern
from core.schemas.normalized_event import NormalizedEvent
from core.pattern_detection.base import PatternDetector

class TemporalPatternDetector(PatternDetector):
    def detect(self, events: List[NormalizedEvent]) -> List[Pattern]:
        patterns = []
        by_entity = defaultdict(list)

        for e in events:
            by_entity[e.entity].append(e)

        for entity, evs in by_entity.items():
            if len(evs) >= 2:
                patterns.append(
                    Pattern(
                        pattern_id=str(uuid.uuid4()),
                        pattern_type="temporal",
                        description=f"Multiple failures close in time for {entity}",
                        confidence=min(1.0, 0.3 * len(evs)),
                        supporting_event_ids=[e.normalized_event_id for e in evs],
                    )
                )

        return patterns


"""
Temporal pattern detector.

Detects clusters of normalized failure events occurring close together in time.
This serves as evidence that a component is experiencing abnormal behavior
within a short time window.

Temporal patterns are treated as objective signals and later combined
with other evidence types (correlation, dependency) during hypothesis scoring.
"""
