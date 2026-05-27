from fastapi import FastAPI

from app.api.triage import router as triage_router
from app.api.ranking import router as ranking_router
from app.api.health import router as health_router

from app.core.constants import (
    APP_NAME,
    VERSION,
    DESCRIPTION,
    API_PREFIX
)

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description=DESCRIPTION
)

# Register API routes
app.include_router(triage_router, prefix=API_PREFIX)
app.include_router(ranking_router, prefix=API_PREFIX)
app.include_router(health_router, prefix=API_PREFIX)


# Root endpoint
@app.get("/")
def root():

    return {
        "message": "RoadSoS AI Backend Running"
    }