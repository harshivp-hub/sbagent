import os
from typing import Dict
from schemas.output_schema import OptimizationResult
from agents.compute_agent import ComputeAgent
# future: from agents.storage_agent import StorageAgent

class Orchestrator:
    def __init__(self):
        self.compute_agent = ComputeAgent()
        # self.storage_agent = StorageAgent()

    def run(self, data: Dict) -> OptimizationResult:
        results = []

        # Run each agent
        comp_res = self.compute_agent.analyze(data)
        results.append(comp_res)

        # future: storage_res = self.storage_agent.analyze(data)
        # results.append(storage_res)

        # Merge results
        total = sum(r.total_savings for r in results)
        all_recs = []
        for r in results:
            all_recs.extend(r.recommendations)

        return OptimizationResult(total_savings=total, recommendations=all_recs)
