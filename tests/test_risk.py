"""Tests for risk assessment."""

from tonecheck.models import Email, ToneType, ToneResult, RiskLevel
from tonecheck.analyzer.risk import ToneRiskAssessor


def _make_result(tone: ToneType = ToneType.PROFESSIONAL) -> ToneResult:
    return ToneResult(dominant_tone=tone, summary="Test")


def test_low_risk_for_clean_email():
    email = Email(body="Thank you for your time. I look forward to hearing from you.")
    risk = ToneRiskAssessor().assess(email, _make_result())
    assert risk.level == RiskLevel.LOW


def test_flags_passive_aggressive_phrases():
    email = Email(body="As per my last email, I already mentioned this. Friendly reminder to check.")
    risk = ToneRiskAssessor().assess(email, _make_result())
    assert risk.level in (RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL)
    assert len(risk.flagged_phrases) >= 2


def test_flags_demanding_tone():
    risk = ToneRiskAssessor().assess(
        Email(body="Do this."),
        _make_result(ToneType.DEMANDING),
    )
    assert any("demanding" in i.lower() for i in risk.issues)


def test_flags_all_caps():
    email = Email(body="Please COMPLETE THIS IMMEDIATELY")
    risk = ToneRiskAssessor().assess(email, _make_result())
    assert any("caps" in i.lower() for i in risk.issues)
