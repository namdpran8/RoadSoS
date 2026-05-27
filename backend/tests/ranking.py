import pytest
import asyncio
from app.services.ranking_service import get_ranked_hospitals


class TestGetRankedHospitals:

    def test_returns_hospitals_list(self):
        result = asyncio.get_event_loop().run_until_complete(
            get_ranked_hospitals(23.2599, 77.4126, "serious")
        )
        assert "hospitals" in result
        assert isinstance(result["hospitals"], list)
        assert len(result["hospitals"]) > 0

    def test_critical_trauma_capable_first(self):
        result = asyncio.get_event_loop().run_until_complete(
            get_ranked_hospitals(23.2599, 77.4126, "critical")
        )
        hospitals = result["hospitals"]
        # First hospital should be trauma capable for critical severity
        assert hospitals[0]["trauma_capable"] is True

    def test_severity_echoed_in_response(self):
        result = asyncio.get_event_loop().run_until_complete(
            get_ranked_hospitals(23.2599, 77.4126, "minor")
        )
        assert result["severity"] == "minor"