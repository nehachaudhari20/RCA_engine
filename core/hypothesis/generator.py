import uuid
from typing import List
from core.schemas.pattern import Pattern
from core.schemas.hypothesis import Hypothesis


class HypothesisGenerator:
    def generate(self, patterns: List[Pattern]) -> List[Hypothesis]:
        hypotheses = []

        for p in patterns:
            # extract entity name from pattern description
            # example: "Multiple failures close in time for service-A"
            entity = p.description.split()[-1]

            if p.pattern_type == "temporal":
                hypotheses.append(
                    Hypothesis(
                        hypothesis_id=str(uuid.uuid4()),
                        category="service_degradation",
                        description=f"Service {entity} experienced internal degradation",
                        generated_by="rules",
                        related_pattern_ids=[p.pattern_id],
                    )
                )

            elif p.pattern_type == "correlation":
                hypotheses.append(
                    Hypothesis(
                        hypothesis_id=str(uuid.uuid4()),
                        category="external_dependency_failure",
                        description=f"Failures caused by dependency impacting {entity}",
                        generated_by="rules",
                        related_pattern_ids=[p.pattern_id],
                    )
                )

        return hypotheses
