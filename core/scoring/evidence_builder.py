from typing import List, Dict
from core.schemas.hypothesis import Hypothesis
from core.schemas.pattern import Pattern
from core.schemas.evidence import Evidence


class EvidenceBuilder:
    def build(
        self,
        hypotheses: List[Hypothesis],
        patterns: List[Pattern],
        dependency_distances: Dict[str, int] | None = None,
    ) -> List[Evidence]:

        pattern_map = {p.pattern_id: p for p in patterns}
        evidences = []

        for h in hypotheses:
            related = [pattern_map[pid] for pid in h.related_pattern_ids]

            temporal = sum(
                p.confidence for p in related if p.pattern_type == "temporal"
            )
            correlation = sum(
                p.confidence for p in related if p.pattern_type == "correlation"
            )

            evidences.append(
                Evidence(
                    hypothesis_id=h.hypothesis_id,
                    temporal_alignment=min(1.0, temporal),
                    correlation_strength=min(1.0, correlation),
                    causal_proximity=0.5,  # placeholder (used later)
                    signal_confidence=min(1.0, temporal + correlation),
                    facts=[p.description for p in related],
                )
            )

        return evidences
