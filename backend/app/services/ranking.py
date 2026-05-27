from __future__ import annotations

import math
from copy import deepcopy


DEFAULT_FACILITIES: list[dict] = [
    {
        "name": "City Trauma Centre",
        "facility_type": "hospital",
        "specialties": ["trauma", "emergency"],
        "is_247": True,
        "is_open": True,
        "eta": {"duration_seconds": 540, "distance_meters": 1800},
        "location": {"lat": 28.6139, "lng": 77.2090},
    },
    {
        "name": "District General Hospital",
        "facility_type": "hospital",
        "specialties": ["general medicine"],
        "is_247": True,
        "is_open": True,
        "eta": {"duration_seconds": 720, "distance_meters": 3200},
        "location": {"lat": 28.6200, "lng": 77.2200},
    },
    {
        "name": "Metro Clinic",
        "facility_type": "clinic",
        "specialties": ["primary care"],
        "is_247": False,
        "is_open": True,
        "eta": {"duration_seconds": 360, "distance_meters": 1100},
        "location": {"lat": 28.6100, "lng": 77.2000},
    },
]


def calculate_facility_score(facility: dict, eta: dict, user_severity: str = "CRITICAL") -> float:
    """
    Lower score = higher priority (rank ascending).
    """
    time_min = eta.get("duration_seconds", 9999) / 60
    dist_km = eta.get("distance_meters", 99999) / 1000

    time_weight = 0.55
    dist_weight = 0.35
    bonus_weight = 0.10

    base_score = (time_weight * time_min) + (dist_weight * dist_km)

    bonus = 0
    name_lower = facility.get("name", "").lower()
    specialties = facility.get("specialties", [])

    if "trauma" in name_lower or "trauma" in specialties:
        bonus -= 3
    if "aiims" in name_lower or "government" in name_lower:
        bonus -= 1
    if facility.get("is_247"):
        bonus -= 1
    if not facility.get("is_open", True):
        bonus += 8

    type_bonus = 0
    if user_severity == "CRITICAL" and facility["facility_type"] == "hospital":
        type_bonus = -2
    elif user_severity == "MINOR" and facility["facility_type"] == "clinic":
        type_bonus = -1

    return base_score + (bonus_weight * bonus) + type_bonus


def _normalise_severity(user_severity: str) -> str:
    severity = (user_severity or "CRITICAL").upper()
    return severity if severity in {"CRITICAL", "SERIOUS", "MINOR"} else "CRITICAL"


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius_km = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return 2 * radius_km * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _build_eta(user_lat: float, user_lng: float, facility: dict) -> dict:
    location = facility.get("location", {})
    facility_lat = float(location.get("lat", user_lat))
    facility_lng = float(location.get("lng", user_lng))
    distance_km = max(0.1, _haversine_km(user_lat, user_lng, facility_lat, facility_lng))
    duration_seconds = int(distance_km * 180)

    return {
        "duration_seconds": duration_seconds,
        "distance_meters": int(distance_km * 1000),
    }


def rank_facilities(
    facilities: list[dict] | None = None,
    *,
    user_severity: str = "CRITICAL",
    user_lat: float = 28.6139,
    user_lng: float = 77.2090,
) -> list[dict]:
    severity = _normalise_severity(user_severity)
    source = facilities if facilities else DEFAULT_FACILITIES

    ranked: list[dict] = []
    for facility in deepcopy(source):
        eta = facility.get("eta") or _build_eta(user_lat, user_lng, facility)
        score = calculate_facility_score(facility, eta, severity)
        ranked.append({
            **facility,
            "eta": eta,
            "score": round(score, 3),
        })

    ranked.sort(key=lambda item: item["score"])
    return ranked


def get_nearby_facility(
    *,
    user_severity: str = "CRITICAL",
    user_lat: float = 28.6139,
    user_lng: float = 77.2090,
) -> dict:
    ranked = rank_facilities(
        user_severity=user_severity,
        user_lat=user_lat,
        user_lng=user_lng,
    )
    return ranked[0] if ranked else {}
