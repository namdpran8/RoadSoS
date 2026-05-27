from __future__ import annotations


DEMO_SCENARIOS = [
    {
        "name": "Highway Collision",
        "description": "Multi-vehicle highway crash. One person is unconscious and another is trapped in the car.",
        "expected_severity": "CRITICAL",
        "expected_priority_order": ["ambulance", "hospital", "police"],
        "wow_factor": "Use a red severity badge, auto-streamed first-aid steps, and the nearest trauma center as the highlighted facility.",
    },
    {
        "name": "Two-Wheeler Leg Injury",
        "description": "Two-wheeler accident. The rider is conscious but cannot move one leg after the impact.",
        "expected_severity": "SERIOUS",
        "expected_priority_order": ["hospital", "ambulance", "police"],
        "wow_factor": "Show an amber severity badge with a fracture-focused first-aid card and hospital-first call order.",
    },
    {
        "name": "Minor Fender-Bender",
        "description": "Minor fender-bender. No injuries, but both cars are blocking the road and causing traffic.",
        "expected_severity": "MINOR",
        "expected_priority_order": ["clinic", "hospital", "police"],
        "wow_factor": "Use a green severity badge to demonstrate calm handling and a low-risk preview panel.",
    },
    {
        "name": "Truck Rollover",
        "description": "Truck rollover. The driver is trapped inside and smoke is visible near the cabin.",
        "expected_severity": "CRITICAL",
        "expected_priority_order": ["ambulance", "hospital", "police"],
        "wow_factor": "Highlight the fire-risk warning and the immediate emergency call button for maximum drama.",
    },
    {
        "name": "Pedestrian Head Bleeding",
        "description": "Pedestrian hit by a vehicle. An elderly person is bleeding from the head and is confused.",
        "expected_severity": "CRITICAL",
        "expected_priority_order": ["ambulance", "hospital", "police"],
        "wow_factor": "Show a head-injury guide with strong visual hierarchy and a rapidly updating triage stream.",
    },
    {
        "name": "Hindi Demo",
        "description": "मेरी गाड़ी पलट गई, एक आदमी बेहोश है",
        "expected_severity": "CRITICAL",
        "expected_priority_order": ["ambulance", "hospital", "police"],
        "wow_factor": "Demonstrates Hindi support, instant severe-case fallback handling, and bilingual emergency readiness.",
    },
]


def get_demo_scenarios() -> list[dict]:
    return list(DEMO_SCENARIOS)
