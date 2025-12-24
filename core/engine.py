from adapters.base import DatasetAdapter
from core.normalization.normalizer import EventNormalizer
from core.pattern_detection.temporal_basic import TemporalPatternDetector
from core.pattern_detection.correlation_basic import CorrelationPatternDetector
from core.hypothesis.generator import HypothesisGenerator
from core.scoring.evidence_builder import EvidenceBuilder
from core.scoring.weighted_scorer import WeightedScorer
from core.ranking.ranker import Ranker


class RCAEngine:
    def __init__(self, adapter: DatasetAdapter):
        self.adapter = adapter
        self.normalizer = EventNormalizer()
        self.pattern_detectors = [
            TemporalPatternDetector(),
            CorrelationPatternDetector(),
        ]
        self.hypothesis_generator = HypothesisGenerator()
        self.evidence_builder = EvidenceBuilder()
        self.scorer = WeightedScorer()
        self.ranker = Ranker()

    def run(self):
        events = self.adapter.load_events()
        incident_meta = self.adapter.load_incident_meta()

        normalized = self.normalizer.normalize(events)

        patterns = []
        for d in self.pattern_detectors:
            patterns.extend(d.detect(normalized))

        hypotheses = self.hypothesis_generator.generate(patterns)
        evidences = self.evidence_builder.build(hypotheses, patterns)
        scores = self.scorer.score(evidences)
        ranked = self.ranker.rank(hypotheses, scores)

        print(f"\nIncident: {incident_meta['incident_id']}")
        print("Ranked Root Causes:")
        for rank, h, score in ranked:
            print(f"{rank}. {h.category} | score={score}")

        return ranked
