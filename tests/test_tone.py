"""Tests for tone analysis."""

from tonecheck.models import Email, ToneType
from tonecheck.analyzer.tone import ToneAnalyzer


def test_professional_tone_detected():
    email = Email(body="Please find attached the report for your review. I appreciate your feedback at your earliest convenience.")
    result = ToneAnalyzer().analyze(email)
    assert result.dominant_tone == ToneType.PROFESSIONAL


def test_urgent_tone_detected():
    email = Email(body="This is urgent! We need this ASAP. The deadline is today and it's critical we act immediately.")
    result = ToneAnalyzer().analyze(email)
    assert result.dominant_tone == ToneType.URGENT


def test_passive_aggressive_detected():
    email = Email(body="As per my last email, as I already explained, not sure if you saw my friendly reminder about this.")
    result = ToneAnalyzer().analyze(email)
    assert result.dominant_tone == ToneType.PASSIVE_AGGRESSIVE


def test_friendly_tone_detected():
    email = Email(body="Hope you're doing well! Thanks so much for the help. Sounds good, happy to help anytime. No worries at all!")
    result = ToneAnalyzer().analyze(email)
    assert result.dominant_tone == ToneType.FRIENDLY


def test_casual_tone_detected():
    email = Email(body="Hey, what's up? Gonna send that stuff over. Yeah, kinda busy but nope, not a problem. Cool cool.")
    result = ToneAnalyzer().analyze(email)
    assert result.dominant_tone == ToneType.CASUAL


def test_tone_scores_returned():
    email = Email(body="Please review this document.")
    result = ToneAnalyzer().analyze(email)
    assert len(result.tone_scores) == 8
    assert all(0.0 <= s.score <= 1.0 for s in result.tone_scores)


def test_summary_generated():
    email = Email(body="Please kindly review this at your earliest convenience.")
    result = ToneAnalyzer().analyze(email)
    assert result.summary
    assert "dominant tone" in result.summary.lower()
