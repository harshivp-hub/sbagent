from pydantic import BaseModel, Field
from typing import List

class Instance(BaseModel):
    id: str
    type: str
    cpu_utilization: float = Field(ge=0, le=100)
    memory_utilization: float = Field(ge=0, le=100)
    monthly_cost: float

class Storage(BaseModel):
    type: str
    size_gb: int
    utilization: float = Field(ge=0, le=100)
    monthly_cost: float

class AccountInfo(BaseModel):
    cloud_provider: str
    monthly_spend: float

class InfrastructureData(BaseModel):
    account_info: AccountInfo
    instances: List[Instance]
    storage: List[Storage]
