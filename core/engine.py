from adapters.base import DatasetAdapter

from core.normalization.normalizer import EventNormalizer
from core.pattern_detection.temporal_basic import TemporalPatternDetector
from core.pattern_detection.correlation_basic import CorrelationPatternDetector

from core.hypothesis.generator import HypothesisGenerator
from core.scoring.evidence_builder import EvidenceBuilder
from core.scoring.weighted_scorer import WeightedScorer
from core.ranking.ranker import Ranker
from core.reasoning.explanation_reasoner import ExplanationReasoner
from core.memory.repository import MemoryRepository


class RCAEngine:
    """
    Core RCA Engine.

    Executes an end-to-end Root Cause Analysis pipeline:
    Adapter → Normalization → Pattern Detection → Hypotheses →
    Evidence → Scoring (with priors) → Ranking → Explanation
    """

    def __init__(self, adapter: DatasetAdapter):
        self.adapter = adapter

        # Core components
        self.normalizer = EventNormalizer()
        self.hypothesis_generator = HypothesisGenerator()
        self.evidence_builder = EvidenceBuilder()
        self.ranker = Ranker()
        self.reasoner = ExplanationReasoner()

        # Memory + learning (Phase 5)
        self.memory = MemoryRepository()
        self.scorer = WeightedScorer(memory_repo=self.memory)

        # Pattern detectors (initialized after graph load)
        self.pattern_detectors = []

    def run(self):
        """
        Run RCA for a single incident and persist results to memory.
        """

        # ------------------------------------------------------------
        # Load dataset
        # ------------------------------------------------------------
        events = self.adapter.load_events()
        dependency_graph = self.adapter.load_dependency_graph()
        incident_meta = self.adapter.load_incident_meta()

        # ------------------------------------------------------------
        # Initialize pattern detectors (graph-aware)
        # ------------------------------------------------------------
        self.pattern_detectors = [
            TemporalPatternDetector(),
            CorrelationPatternDetector(dependency_graph),
        ]

        # ------------------------------------------------------------
        # Normalize events
        # ------------------------------------------------------------
        normalized_events = self.normalizer.normalize(events)

        # ------------------------------------------------------------
        # Detect patterns (objective evidence)
        # ------------------------------------------------------------
        patterns = []
        for detector in self.pattern_detectors:
            patterns.extend(detector.detect(normalized_events))

        # ------------------------------------------------------------
        # Generate hypotheses
        # ------------------------------------------------------------
        hypotheses = self.hypothesis_generator.generate(patterns)

        # ------------------------------------------------------------
        # Evidence + scoring (with priors)
        # ------------------------------------------------------------
        evidences = self.evidence_builder.build(hypotheses, patterns)
        scores = self.scorer.score(evidences, hypotheses)

        # ------------------------------------------------------------
        # Ranking
        # ------------------------------------------------------------
        ranked_results = self.ranker.rank(hypotheses, scores)

        # ------------------------------------------------------------
        # Persist RCA run (Phase 5 memory)
        # ------------------------------------------------------------
        run_id = self.memory.start_run(incident_meta["incident_id"])

        for rank, hypothesis, score in ranked_results:
            self.memory.save_result(
                run_id=run_id,
                hypothesis_category=hypothesis.category,
                hypothesis_entity=hypothesis.description,
                rank=rank,
                score=score,
            )

        # ------------------------------------------------------------
        # Deterministic explanation (NO LLM API)
        # ------------------------------------------------------------
        explanation = self.reasoner.explain(ranked_results, evidences)

        return {
            "incident_id": incident_meta["incident_id"],
            "ranked_root_causes": ranked_results,
            "explanation": explanation,
        }
