from pydantic import BaseModel
from typing import List, Literal

class Recommendation(BaseModel):
    type: Literal["downsize_instance", "upsize_instance", "optimize_storage"]
    resource: str
    action: str
    savings: float      # positive = money saved, negative = extra cost
    reason: str
    confidence: float = 1.0

class OptimizationResult(BaseModel):
    total_savings: float
    recommendations: List[Recommendation]

    def json(self, *args, **kwargs) -> str:
        # Delegate to Pydantic v2's model_dump_json to support indent, etc.
        return self.model_dump_json(*args, **kwargs)
