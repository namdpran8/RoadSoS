from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.request_models import TriageRequest

from app.services.triage_service import triage_stream


router = APIRouter()


@router.post("/triage")
async def triage(data: TriageRequest):

    async def event_stream():
        async for event in triage_stream(data.description, data.lat, data.lng):
            yield event

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )