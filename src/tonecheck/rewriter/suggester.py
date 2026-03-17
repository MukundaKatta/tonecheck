"""Tone adjustment suggestions."""

from __future__ import annotations

from tonecheck.models import (
    Email, ToneResult, ToneRisk, ToneType, RewriteSuggestion,
)


# Mapping of problematic phrases to better alternatives by target tone
PHRASE_ALTERNATIVES: dict[str, dict[ToneType, str]] = {
    "as per my last email": {
        ToneType.PROFESSIONAL: "To follow up on my previous message",
        ToneType.FRIENDLY: "Just circling back on this",
    },
    "per my previous email": {
        ToneType.PROFESSIONAL: "As I mentioned earlier",
        ToneType.FRIENDLY: "Going back to what we discussed",
    },
    "you need to": {
        ToneType.PROFESSIONAL: "Could you please",
        ToneType.FRIENDLY: "Would you mind",
    },
    "you must": {
        ToneType.PROFESSIONAL: "It would be necessary to",
        ToneType.FRIENDLY: "It would be great if you could",
    },
    "i demand": {
        ToneType.PROFESSIONAL: "I would appreciate",
        ToneType.FRIENDLY: "I'd really love it if",
    },
    "this is unacceptable": {
        ToneType.PROFESSIONAL: "I have concerns about this outcome",
        ToneType.FRIENDLY: "I think we can do better here",
    },
    "failure to comply": {
        ToneType.PROFESSIONAL: "If this is not addressed",
        ToneType.FRIENDLY: "If we can't get this sorted",
    },
    "do this now": {
        ToneType.PROFESSIONAL: "Could you prioritize this",
        ToneType.FRIENDLY: "Could you take a look at this when you get a chance",
    },
    "friendly reminder": {
        ToneType.PROFESSIONAL: "I wanted to follow up on",
        ToneType.FRIENDLY: "Just a quick note about",
    },
    "obviously": {
        ToneType.PROFESSIONAL: "As you may know",
        ToneType.FRIENDLY: "You probably already know this, but",
    },
    "with all due respect": {
        ToneType.PROFESSIONAL: "I see this differently",
        ToneType.FRIENDLY: "I have a slightly different take",
    },
}


class ToneSuggester:
    """Recommends tone adjustments for problematic phrases."""

    def suggest(
        self,
        email: Email,
        tone_result: ToneResult,
        risk: ToneRisk,
        target_tone: ToneType = ToneType.PROFESSIONAL,
    ) -> list[RewriteSuggestion]:
        """Generate suggestions to improve the email's tone."""
        suggestions: list[RewriteSuggestion] = []
        text_lower = email.full_text.lower()

        for phrase, alternatives in PHRASE_ALTERNATIVES.items():
            if phrase in text_lower:
                replacement = alternatives.get(target_tone) or next(iter(alternatives.values()))
                suggestions.append(
                    RewriteSuggestion(
                        original=phrase,
                        suggested=replacement,
                        reason=f"Softens language toward a more {target_tone.value} tone",
                        target_tone=target_tone,
                    )
                )

        # Add general suggestions based on dominant tone
        if tone_result.dominant_tone == ToneType.PASSIVE_AGGRESSIVE:
            suggestions.append(
                RewriteSuggestion(
                    original="(overall tone)",
                    suggested="State your needs directly and clearly",
                    reason="Direct communication is more effective than indirect hints",
                    target_tone=target_tone,
                )
            )
        if tone_result.dominant_tone == ToneType.DEMANDING:
            suggestions.append(
                RewriteSuggestion(
                    original="(overall tone)",
                    suggested="Frame requests as collaborative asks",
                    reason="Collaborative language fosters better working relationships",
                    target_tone=target_tone,
                )
            )

        return suggestions
