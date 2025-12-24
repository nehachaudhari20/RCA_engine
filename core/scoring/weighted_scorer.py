from typing import List, Dict
from core.schemas.evidence import Evidence


class WeightedScorer:
    def __init__(self, memory_repo=None, weights=None):
        self.memory_repo = memory_repo
        self.weights = weights or {
            "temporal": 0.4,
            "correlation": 0.3,
            "causal": 0.2,
            "signal": 0.1,
        }

    def score(self, evidences, hypotheses):
        scores = {}

        for e, h in zip(evidences, hypotheses):
            base_score = (
                self.weights["temporal"] * e.temporal_alignment
                + self.weights["correlation"] * e.correlation_strength
                + self.weights["causal"] * e.causal_proximity
                + self.weights["signal"] * e.signal_confidence
            )

            prior = (
                self.memory_repo.get_prior_weight(h.category, h.description)
                if self.memory_repo
                else 1.0
            )

            scores[h.hypothesis_id] = round(base_score * prior, 4)

        return scores
