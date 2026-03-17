"""Tone risk assessment for emails."""

from __future__ import annotations

import re

from tonecheck.models import Email, ToneResult, ToneRisk, RiskLevel, ToneType


RISKY_PHRASES: dict[str, str] = {
    "as per my last email": "May come across as passive-aggressive",
    "per my previous email": "May come across as passive-aggressive",
    "as i already mentioned": "Can sound condescending",
    "i'm not sure why you": "Can sound accusatory",
    "you should have": "Can sound blaming",
    "you always": "Generalizing can feel accusatory",
    "you never": "Generalizing can feel accusatory",
    "obviously": "Can sound condescending",
    "clearly": "Can sound dismissive when pointing out errors",
    "with all due respect": "Often precedes something disrespectful",
    "no offense": "Often precedes something offensive",
    "just to be clear": "Can sound passive-aggressive in context",
    "i would have expected": "Can sound disappointed/judgmental",
    "correct me if i'm wrong": "Often used passive-aggressively",
    "not sure if you noticed": "Can sound sarcastic",
    "as you should know": "Can sound condescending",
    "friendly reminder": "Often perceived as passive-aggressive",
    "please advise why": "Can sound demanding",
    "failure to comply": "Sounds threatening",
    "this is unacceptable": "Very strong language for email",
}

PROBLEMATIC_PATTERNS: list[tuple[str, str]] = [
    (r"!{2,}", "Multiple exclamation marks may seem aggressive or unprofessional"),
    (r"\b[A-Z]{4,}\b", "ALL CAPS words can seem like shouting"),
    (r"\?\?+", "Multiple question marks can seem aggressive"),
    (r"\.\.\.", "Ellipsis can seem passive-aggressive or trailing off"),
]


class ToneRiskAssessor:
    """Flags potentially problematic tones before sending."""

    def assess(self, email: Email, tone_result: ToneResult) -> ToneRisk:
        """Assess risk of the email's tone causing miscommunication."""
        issues: list[str] = []
        flagged: list[str] = []
        suggestions: list[str] = []
        text_lower = email.full_text.lower()

        # Check risky phrases
        for phrase, reason in RISKY_PHRASES.items():
            if phrase in text_lower:
                flagged.append(phrase)
                issues.append(f'"{phrase}" - {reason}')

        # Check problematic patterns
        for pattern, reason in PROBLEMATIC_PATTERNS:
            if re.search(pattern, email.full_text):
                issues.append(reason)

        # Check tone-based risks
        if tone_result.dominant_tone == ToneType.PASSIVE_AGGRESSIVE:
            issues.append("Overall tone reads as passive-aggressive")
            suggestions.append("Consider being more direct about your concerns")

        if tone_result.dominant_tone == ToneType.DEMANDING:
            issues.append("Overall tone reads as demanding")
            suggestions.append("Consider softening requests with 'could you' or 'would you mind'")

        if tone_result.dominant_tone == ToneType.URGENT:
            suggestions.append("If urgency is warranted, ensure recipient understands why")

        # Determine risk level
        level = self._calculate_level(issues, flagged)

        if not suggestions and issues:
            suggestions.append("Review flagged phrases and consider rephrasing")

        return ToneRisk(
            level=level,
            issues=issues,
            suggestions=suggestions,
            flagged_phrases=flagged,
        )

    def _calculate_level(self, issues: list[str], flagged: list[str]) -> RiskLevel:
        """Calculate overall risk level."""
        count = len(issues)
        if count == 0:
            return RiskLevel.LOW
        elif count <= 2:
            return RiskLevel.MEDIUM
        elif count <= 4:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
