from typing import Dict, List
from core.schemas.hypothesis import Hypothesis


class Ranker:
    def rank(
        self,
        hypotheses: List[Hypothesis],
        scores: Dict[str, float],
    ) -> List[tuple]:

        ranked = sorted(
            hypotheses,
            key=lambda h: scores.get(h.hypothesis_id, 0),
            reverse=True,
        )

        return [
            (idx + 1, h, scores.get(h.hypothesis_id, 0))
            for idx, h in enumerate(ranked)
        ]
