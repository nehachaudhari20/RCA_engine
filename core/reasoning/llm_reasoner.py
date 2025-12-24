class LLMReasoner:
    def explain(self, ranked_results):
        top = ranked_results[0]
        _, hypothesis, score = top

        explanation = (
            f"The most likely root cause is '{hypothesis.category}'. "
            f"This conclusion is based on multiple corroborating signals, "
            f"including temporal clustering, dependency-aware correlations, "
            f"and structural proximity within the service graph. "
            f"The confidence score of {score} reflects stronger evidence "
            f"compared to alternative hypotheses."
        )

        return explanation
