from typing import List

from pydantic import BaseModel, Field, field_validator


class TriageRequest(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("description cannot be empty")
        return value


class HospitalRankingRequest(BaseModel):
    hospitals: List[dict] = Field(default_factory=list)