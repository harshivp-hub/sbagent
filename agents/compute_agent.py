import os
import json
from typing import Dict, Any
from pydantic import ValidationError

from schemas.input_schema import InfrastructureData
from schemas.output_schema import OptimizationResult, Recommendation
from .base_agent import BaseAgent

class ComputeAgent(BaseAgent):
    TEMPLATE = """
You are a Compute Optimization Agent. Given the following instances data, identify:
 - Over-provisioned VMs (low avg CPU/memory)
 - Under-provisioned VMs (high avg CPU/memory > 80%)
Return JSON matching this schema:
{{
  "total_savings": float,
  "recommendations": [
    {{
      "type": "downsize_instance"|"upsize_instance"|"optimize_storage",
      "resource": str,
      "action": str,
      "savings": float,
      "reason": str,
      "confidence": float
    }}
  ]
}}
Input Instances:
{instances_json}
"""

    def __init__(self):
        model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        super().__init__(model=model)
        self.threshold_high = 80.0
        self.threshold_low = 30.0

    def build_prompt(self, infra: InfrastructureData) -> str:
        instances = [inst.model_dump() for inst in infra.instances]
        return self.TEMPLATE.format(
            instances_json=json.dumps(instances, indent=2)
        )

    def analyze(self, data: Dict[str, Any]) -> OptimizationResult:
        infra = InfrastructureData(**data)
        prompt = self.build_prompt(infra)
        raw = self.call_llm(prompt)

        try:
            parsed = json.loads(raw)
            result = OptimizationResult(**parsed)
        except (json.JSONDecodeError, ValidationError):
            result = self.fallback(infra)

        return result

    def fallback(self, infra: InfrastructureData) -> OptimizationResult:
        recs = []
        total = 0.0

        # Downsize under-utilized
        for inst in infra.instances:
            if inst.cpu_utilization < self.threshold_low:
                new_type = inst.type.replace("xlarge", "large")
                savings = inst.monthly_cost * 0.5
                recs.append(Recommendation(
                    type="downsize_instance",
                    resource=inst.id,
                    action=f"Change to {new_type}",
                    savings=savings,
                    reason="Low CPU utilization",
                    confidence=0.5
                ))
                total += savings

        # Upsize over-utilized
        for inst in infra.instances:
            if inst.cpu_utilization > self.threshold_high:
                # naive mapping: small→medium, medium→large, large→xlarge, xlarge→2xlarge
                size_map = {"nano":"micro","micro":"small","small":"medium","medium":"large","large":"xlarge","xlarge":"2xlarge"}
                base, size = inst.type.split(".")
                new_suffix = size_map.get(size, size)
                new_type = f"{base}.{new_suffix}"
                extra_cost = inst.monthly_cost * 0.5
                recs.append(Recommendation(
                    type="upsize_instance",
                    resource=inst.id,
                    action=f"Change to {new_type}",
                    savings=-extra_cost,
                    reason="High CPU utilization",
                    confidence=0.5
                ))
                total -= extra_cost

        return OptimizationResult(total_savings=total, recommendations=recs)
