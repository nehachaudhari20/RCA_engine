from collections import deque
from typing import Dict, List, Optional

class DependencyAnalyzer:
    def __init__(self, graph: Dict[str, List[str]]):
        self.graph = graph

    def distance(self, source: str, target: str) -> Optional[int]:
        if source == target:
            return 0

        visited = set()
        queue = deque([(source, 0)])

        while queue:
            node, dist = queue.popleft()
            if node == target:
                return dist

            for nxt in self.graph.get(node, []):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, dist + 1))

        return None

"""
Dependency proximity analyzer.

Computes the structural distance between services using a dependency graph.
This provides causal-context evidence by estimating how close a failing
component is to the impacted entity.

Dependency proximity is used as an evidence factor during hypothesis scoring,
not as a standalone root cause signal.
"""
