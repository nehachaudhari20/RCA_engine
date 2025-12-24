import uuid
from collections import Counter
from typing import List

from core.schemas.pattern import Pattern
from core.schemas.normalized_event import NormalizedEvent
from core.pattern_detection.base import PatternDetector

class CorrelationPatternDetector(PatternDetector):
    def detect(self, events: List[NormalizedEvent]) -> List[Pattern]:
        patterns = []

        dependency_counts = Counter(
            e.dimensions.get("dependency")
            for e in events
            if "dependency" in e.dimensions
        )

        for dep, count in dependency_counts.items():
            if count >= 2:
                patterns.append(
                    Pattern(
                        pattern_id=str(uuid.uuid4()),
                        pattern_type="correlation",
                        description=f"Failures correlated with dependency {dep}",
                        confidence=min(1.0, 0.4 * count),
                        supporting_event_ids=[
                            e.normalized_event_id
                            for e in events
                            if e.dimensions.get("dependency") == dep
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
