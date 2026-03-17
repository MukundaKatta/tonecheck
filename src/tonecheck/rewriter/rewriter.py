"""Tone rewriting - generates alternative phrasings."""

from __future__ import annotations

import re

from tonecheck.models import Email, ToneType, RewriteSuggestion


TONE_TEMPLATES: dict[ToneType, dict[str, str]] = {
    ToneType.PROFESSIONAL: {
        "greeting": "I hope this message finds you well.",
        "request": "Could you please {action}?",
        "closing": "Thank you for your time and attention to this matter.",
        "followup": "I wanted to follow up regarding {topic}.",
        "deadline": "It would be appreciated if this could be completed by {date}.",
    },
    ToneType.FRIENDLY: {
        "greeting": "Hope you're having a great day!",
        "request": "Would you mind {action}? That would be awesome!",
        "closing": "Thanks so much! Let me know if you need anything.",
        "followup": "Just checking in on {topic} - no rush!",
        "deadline": "If possible, it would be great to have this by {date}.",
    },
    ToneType.FORMAL: {
        "greeting": "Dear {recipient},",
        "request": "I respectfully request that you {action}.",
        "closing": "Yours sincerely,",
        "followup": "I am writing to inquire about the status of {topic}.",
        "deadline": "The deadline for this matter is {date}.",
    },
}

# Direct phrase replacements to soften or shift tone
REWRITE_RULES: list[tuple[str, str, str]] = [
    (r"\byou always\b", "it seems like this happens often", "Avoids accusatory generalization"),
    (r"\byou never\b", "I've noticed this hasn't happened yet", "Avoids accusatory generalization"),
    (r"\bwhy didn't you\b", "I was wondering about", "Reframes as curiosity rather than blame"),
    (r"\byou forgot to\b", "it looks like we still need to", "Uses 'we' to share responsibility"),
    (r"\bthat's wrong\b", "I see this differently", "Softens disagreement"),
    (r"\byou failed to\b", "this still needs to be", "Removes personal blame"),
    (r"\bI told you\b", "as we discussed", "Removes condescending phrasing"),
    (r"\bwhat's the problem\b", "could you help me understand the situation", "More collaborative framing"),
]


class ToneRewriter:
    """Generates alternative phrasings for email text."""

    def rewrite(self, email: Email, target_tone: ToneType = ToneType.PROFESSIONAL) -> str:
        """Rewrite the email body with improved tone."""
        text = email.body

        # Apply pattern-based rewrites
        for pattern, replacement, _reason in REWRITE_RULES:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    def rewrite_phrase(self, phrase: str, target_tone: ToneType = ToneType.PROFESSIONAL) -> list[RewriteSuggestion]:
        """Generate alternative phrasings for a single phrase."""
        suggestions: list[RewriteSuggestion] = []
        phrase_lower = phrase.lower()

        for pattern, replacement, reason in REWRITE_RULES:
            if re.search(pattern, phrase_lower):
                rewritten = re.sub(pattern, replacement, phrase_lower, flags=re.IGNORECASE)
                suggestions.append(
                    RewriteSuggestion(
                        original=phrase,
                        suggested=rewritten,
                        reason=reason,
                        target_tone=target_tone,
                    )
                )

        return suggestions
