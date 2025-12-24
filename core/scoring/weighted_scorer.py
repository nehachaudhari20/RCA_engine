from typing import List, Dict
from core.schemas.evidence import Evidence


class WeightedScorer:
    def __init__(self, weights: Dict[str, float] | None = None):
        self.weights = weights or {
            "temporal": 0.4,
            "correlation": 0.3,
            "causal": 0.2,
            "signal": 0.1,
        }

    def score(self, evidences: List[Evidence]) -> Dict[str, float]:
        scores = {}

        for e in evidences:
            score = (
                self.weights["temporal"] * e.temporal_alignment
                + self.weights["correlation"] * e.correlation_strength
                + self.weights["causal"] * e.causal_proximity
                + self.weights["signal"] * e.signal_confidence
            )
            scores[e.hypothesis_id] = round(score, 4)

        return scores
