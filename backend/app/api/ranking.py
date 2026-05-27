from fastapi import APIRouter, Query

from app.models.request_models import HospitalRankingRequest

from app.services.ranking import rank_facilities


router = APIRouter()


@router.post("/rank-hospitals")
@router.post("/ranking")
def ranking(data: HospitalRankingRequest, severity: str = Query(default="CRITICAL")):

    ranked = rank_facilities(data.hospitals, user_severity=severity)

    return {
        "severity": severity.upper(),
        "ranked_hospitals": ranked
    }