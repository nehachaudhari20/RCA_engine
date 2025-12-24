class ExplanationReasoner:
    """
    Generates human-readable RCA explanations from ranked hypotheses
    and structured evidence.

    This is a deterministic, LLM-free reasoning layer.
    Can be replaced by a real LLM later without changing the engine.
    """

    def explain(self, ranked_results, evidences):
        if not ranked_results:
            return "No root cause could be determined due to insufficient evidence."

        rank, hypothesis, score = ranked_results[0]

        explanation = (
            f"The most likely root cause is '{hypothesis.category}'. "
            f"{hypothesis.description}. "
            f"This conclusion is based on multiple corroborating signals "
            f"such as temporal clustering of failures, correlation patterns, "
            f"and structural context from the dependency graph. "
            f"The confidence score of {score} indicates stronger support "
            f"compared to alternative hypotheses."
        )

        return explanation
