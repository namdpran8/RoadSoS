from __future__ import annotations

from app.utils.validators import sanitize_description


FIRST_AID_GUIDES = {
    "CRITICAL_bleeding": {
        "title": "Severe Bleeding",
        "steps": [
            "Apply firm, direct pressure with any clean cloth",
            "Do not remove the cloth - add more on top if soaked",
            "Elevate the injured limb above heart level if possible",
            "Keep the person warm and still",
            "Talk to them - keep them conscious and calm",
        ],
        "warning": "Do not use a tourniquet unless trained",
    },
    "CRITICAL_unconscious": {
        "title": "Unconscious Person",
        "steps": [
            "Check if the scene is safe before approaching",
            "Call emergency services immediately",
            "Check breathing for 10 seconds without delaying help",
            "If breathing, place them on their side only if there is no spinal injury concern",
            "If not breathing, start CPR if you are trained and follow dispatcher instructions",
        ],
        "warning": "Do not give food, drink, or any medicine",
    },
    "CRITICAL_breathing": {
        "title": "Breathing Emergency",
        "steps": [
            "Keep the airway open and look for visible blockage",
            "If choking and conscious, encourage coughing",
            "If the person becomes unresponsive, call emergency services immediately",
            "Loosen tight clothing around the neck and chest",
            "Stay with the person and watch breathing continuously",
        ],
        "warning": "Do not put fingers into the mouth unless you can see and remove an object safely",
    },
    "SERIOUS_fracture": {
        "title": "Suspected Fracture",
        "steps": [
            "Keep the injured limb still in the position you found it",
            "Support the area with a splint or rolled cloth if available",
            "Apply a wrapped cold pack for swelling if it does not delay care",
            "Check for bleeding and cover any wounds with clean cloth",
            "Get medical help quickly, especially after a road crash",
        ],
        "warning": "Do not try to straighten the limb",
    },
    "SERIOUS_head": {
        "title": "Head or Neck Injury",
        "steps": [
            "Keep the head and neck as still as possible",
            "Call an ambulance and explain a possible head injury",
            "Watch for vomiting, drowsiness, seizures, or confusion",
            "If bleeding, apply gentle pressure around the wound without pressing hard on a suspected skull injury",
            "Keep the person lying flat unless breathing makes that unsafe",
        ],
        "warning": "Do not move the neck or let the person sit up suddenly",
    },
    "MINOR_general": {
        "title": "Minor Injuries",
        "steps": [
            "Move to a safe spot away from traffic",
            "Clean small cuts with clean water if available",
            "Cover wounds with a clean dressing or cloth",
            "Rest and monitor for increasing pain, swelling, or dizziness",
            "If symptoms worsen, seek medical review",
        ],
        "warning": "Do not ignore worsening pain or hidden head injury symptoms",
    },
}


INJURY_KEYWORDS = {
    "bleeding": ["blood", "bleeding", "cut", "wound", "खून"],
    "unconscious": ["unconscious", "fainted", "not responding", "बेहोश"],
    "breathing": ["not breathing", "breathless", "choking", "सांस"],
    "fracture": ["broken", "fracture", "bone", "टूट"],
    "head": ["head", "neck", "skull", "सिर"],
}


def detect_injury_type(description: str) -> str:
    text = sanitize_description(description)

    matches: list[tuple[str, int]] = []
    for injury_type, keywords in INJURY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score:
            matches.append((injury_type, score))

    if not matches:
        return "general"

    matches.sort(key=lambda item: (-item[1], item[0]))
    return matches[0][0]


def get_first_aid_guide(severity: str, injury_type: str) -> dict:
    normalized_severity = (severity or "CRITICAL").upper()
    normalized_injury = (injury_type or "general").lower()

    if normalized_severity == "CRITICAL" and normalized_injury in {"bleeding", "unconscious", "breathing"}:
        key = f"CRITICAL_{normalized_injury}"
    elif normalized_severity == "SERIOUS" and normalized_injury in {"fracture", "head"}:
        key = f"SERIOUS_{normalized_injury}"
    else:
        key = "MINOR_general"

    guide = FIRST_AID_GUIDES[key]
    return {
        "key": key,
        "title": guide["title"],
        "steps": guide["steps"],
        "warning": guide["warning"],
    }


def get_first_aid(text: str) -> list[str]:
    injury_type = detect_injury_type(text)
    if injury_type == "general":
        return FIRST_AID_GUIDES["MINOR_general"]["steps"]

    severity = "CRITICAL" if injury_type in {"bleeding", "unconscious", "breathing"} else "SERIOUS"
    return get_first_aid_guide(severity, injury_type)["steps"]
