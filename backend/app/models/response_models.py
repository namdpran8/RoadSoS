from typing import Any, List

from pydantic import BaseModel, Field


class TriageResponse(BaseModel):
    severity: str
    confidence: float = Field(ge=0.0, le=1.0)
    priority_order: List[str]
    first_aid_steps: List[str]
    do_not_do: List[str] = Field(default_factory=list)
    call_now: str = "+911"
    reassurance_message: str
    estimated_risk: str


class TriageEnvelopeResponse(BaseModel):
    triage: TriageResponse
    nearby_facility: dict[str, Any]
    token_cost_estimate: dict[str, Any]


class RankingResponse(BaseModel):
    severity: str
    ranked_hospitals: List[dict]


class HealthResponse(BaseModel):
    status: str