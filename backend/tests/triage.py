import pytest
from app.services.triage_service import classify_severity, get_call_order, generate_triage_response


# ── classify_severity ────────────────────────────────────────────────────────

class TestClassifySeverity:

    def test_critical_keyword(self):
        result = classify_severity("Person is unconscious and not breathing")
        assert result.level == "critical"
        assert result.confidence > 0
        assert len(result.matched_keywords) >= 1

    def test_serious_keyword(self):
        result = classify_severity("Victim has a fracture and heavy bleeding")
        assert result.level == "serious"

    def test_minor_keyword(self):
        result = classify_severity("Driver has a bruise and minor scratch")
        assert result.level == "minor"

    def test_no_keyword_defaults_to_serious(self):
        result = classify_severity("There was an accident nearby")
        assert result.level == "serious"
        assert result.confidence == 0.10

    def test_empty_text_defaults_to_serious(self):
        result = classify_severity("")
        assert result.level == "serious"

    def test_no_partial_match(self):
        # 'uncritical' should NOT trigger critical
        result = classify_severity("The situation seems uncritical")
        assert result.level != "critical"

    def test_confidence_scales_with_matches(self):
        result = classify_severity("unconscious, cardiac arrest, no pulse, crushed")
        assert result.confidence >= 0.9


# ── get_call_order ───────────────────────────────────────────────────────────

class TestGetCallOrder:

    def test_critical_order(self):
        assert get_call_order("critical") == ["ambulance", "hospital", "police"]

    def test_serious_order(self):
        assert get_call_order("serious") == ["hospital", "ambulance"]

    def test_minor_order(self):
        assert get_call_order("minor") == ["clinic"]

    def test_unknown_falls_back_to_serious(self):
        assert get_call_order("unknown_level") == ["hospital", "ambulance"]


# ── generate_triage_response ─────────────────────────────────────────────────

class TestGenerateTriageResponse:

    def test_returns_all_keys(self):
        result = generate_triage_response("Person is unconscious after crash")
        assert "severity" in result
        assert "confidence" in result
        assert "matched_keywords" in result
        assert "call_order" in result
        assert "first_aid_steps" in result
        assert "ai_analysis" in result

    def test_empty_input_returns_safe_default(self):
        result = generate_triage_response("")
        assert result["severity"] == "serious"
        assert result["ai_analysis"] == "No input provided"

    def test_whitespace_input_returns_safe_default(self):
        result = generate_triage_response("   ")
        assert result["severity"] == "serious"