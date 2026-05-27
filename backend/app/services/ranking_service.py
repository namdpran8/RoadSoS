from app.services.ranking import calculate_facility_score, get_nearby_facility, rank_facilities
import asyncio


def calculate_hospital_score(hospital):
    eta = hospital.get("eta", {})
    return calculate_facility_score(hospital, eta, hospital.get("severity", "CRITICAL"))


def rank_hospitals(hospitals, severity: str = "CRITICAL"):
    return rank_facilities(hospitals, user_severity=severity)


def get_ranked_facilities(severity: str = "CRITICAL"):
    return rank_facilities(user_severity=severity)


async def get_ranked_hospitals(latitude: float, longitude: float, severity: str = "critical"):
    await asyncio.sleep(0)
    ranked = rank_facilities(user_severity=severity.upper(), user_lat=latitude, user_lng=longitude)
    hospitals = []
    for facility in ranked:
        hospitals.append(
            {
                "name": facility.get("name"),
                "address": facility.get("address", ""),
                "distance_km": round(facility["eta"]["distance_meters"] / 1000, 2),
                "rating": facility.get("rating"),
                "trauma_capable": "trauma" in facility.get("name", "").lower() or "trauma" in facility.get("specialties", []),
            }
        )

    return {"severity": severity, "hospitals": hospitals}
