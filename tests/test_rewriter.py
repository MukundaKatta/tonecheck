"""Tests for rewriter and suggester."""

from tonecheck.models import Email, ToneType, ToneResult, ToneRisk, RiskLevel
from tonecheck.rewriter.suggester import ToneSuggester
from tonecheck.rewriter.rewriter import ToneRewriter


def test_suggester_finds_problematic_phrases():
    email = Email(body="As per my last email, you need to fix this.")
    result = ToneResult(dominant_tone=ToneType.PASSIVE_AGGRESSIVE, summary="test")
    risk = ToneRisk(level=RiskLevel.HIGH, issues=[], suggestions=[], flagged_phrases=["as per my last email"])
    suggestions = ToneSuggester().suggest(email, result, risk)
    assert len(suggestions) >= 2
    originals = [s.original.lower() for s in suggestions]
    assert any("as per my last email" in o for o in originals)


def test_rewriter_replaces_phrases():
    email = Email(body="You always forget to send the report.")
    result = ToneRewriter().rewrite(email)
    assert "you always" not in result.lower()


def test_rewriter_handles_clean_text():
    email = Email(body="Please review the attached document.")
    result = ToneRewriter().rewrite(email)
    assert result == email.body
