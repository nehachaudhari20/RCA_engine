from adapters.base import DatasetAdapter

from core.normalization.normalizer import EventNormalizer
from core.pattern_detection.temporal_basic import TemporalPatternDetector
from core.pattern_detection.correlation_basic import CorrelationPatternDetector

from core.hypothesis.generator import HypothesisGenerator
from core.scoring.evidence_builder import EvidenceBuilder
from core.scoring.weighted_scorer import WeightedScorer
from core.ranking.ranker import Ranker
from core.reasoning.explanation_reasoner import ExplanationReasoner


class RCAEngine:
    """
    Core RCA Engine.

    This class orchestrates the full Root Cause Analysis pipeline:
    DatasetAdapter
        → Event Normalization
        → Pattern Detection (temporal, correlation)
        → Hypothesis Generation
        → Evidence Assembly
        → Scoring
        → Ranking
        → Explanation

    The engine is dataset-agnostic and does not depend on any
    external LLM APIs or infrastructure.
    """

    def __init__(self, adapter: DatasetAdapter):
        self.adapter = adapter

        # Core components
        self.normalizer = EventNormalizer()
        self.hypothesis_generator = HypothesisGenerator()
        self.evidence_builder = EvidenceBuilder()
        self.scorer = WeightedScorer()
        self.ranker = Ranker()
        self.reasoner = ExplanationReasoner()

        # Pattern detectors (initialized later once graph is loaded)
        self.pattern_detectors = []

    def run(self):
        """
        Execute the full RCA pipeline for a single incident.
        """

        # ------------------------------------------------------------------
        # Load dataset inputs
        # ------------------------------------------------------------------
        events = self.adapter.load_events()
        dependency_graph = self.adapter.load_dependency_graph()
        incident_meta = self.adapter.load_incident_meta()

        print(f"[Engine] Loaded events: {len(events)}")
        for e in events:
            print(f"[Engine] Event type={e.event_type}, entity={e.entity_id}")

        # ------------------------------------------------------------------
        # Initialize pattern detectors (graph-aware)
        # ------------------------------------------------------------------
        self.pattern_detectors = [
            TemporalPatternDetector(),
            CorrelationPatternDetector(dependency_graph),
        ]

        # ------------------------------------------------------------------
        # Normalize events into canonical failure semantics
        # ------------------------------------------------------------------
        normalized_events = self.normalizer.normalize(events)

        # ------------------------------------------------------------------
        # Pattern detection (objective evidence)
        # ------------------------------------------------------------------
        patterns = []
        for detector in self.pattern_detectors:
            patterns.extend(detector.detect(normalized_events))

        print(f"\nPatterns detected: {len(patterns)}")
        for p in patterns:
            print(f"- Pattern type: {p.pattern_type}, desc: {p.description}")

        # ------------------------------------------------------------------
        # Hypothesis generation (explanations, not decisions)
        # ------------------------------------------------------------------
        hypotheses = self.hypothesis_generator.generate(patterns)

        print(f"\nHypotheses generated: {len(hypotheses)}")
        for h in hypotheses:
            print(f"- Hypothesis: {h.category} | {h.description}")

        # ------------------------------------------------------------------
        # Evidence assembly and scoring
        # ------------------------------------------------------------------
        evidences = self.evidence_builder.build(hypotheses, patterns)
        scores = self.scorer.score(evidences)

        # ------------------------------------------------------------------
        # Ranking
        # ------------------------------------------------------------------
        ranked_results = self.ranker.rank(hypotheses, scores)

        print(f"\nIncident: {incident_meta['incident_id']}")
        print("Ranked Root Causes:")
        for rank, hypothesis, score in ranked_results:
            print(f"{rank}. {hypothesis.category} | score={score}")

        # ------------------------------------------------------------------
        # Deterministic explanation (NO LLM API)
        # ------------------------------------------------------------------
        explanation = self.reasoner.explain(ranked_results, evidences)

        print("\nExplanation:")
        print(explanation)

        return {
            "incident_id": incident_meta["incident_id"],
            "ranked_root_causes": ranked_results,
            "explanation": explanation,
        }
