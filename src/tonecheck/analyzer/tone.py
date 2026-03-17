"""Tone analysis using keyword matching."""

from __future__ import annotations

import re

from tonecheck.models import Email, ToneType, ToneScore, ToneResult


# Keyword dictionaries for each tone
TONE_KEYWORDS: dict[ToneType, list[str]] = {
    ToneType.PROFESSIONAL: [
        "please", "kindly", "regarding", "per our discussion", "as discussed",
        "i would like to", "for your review", "at your earliest convenience",
        "thank you for", "i appreciate", "looking forward", "please advise",
        "as per", "in accordance", "with respect to", "pursuant to",
        "i wanted to follow up", "for your consideration", "please find attached",
        "i hope this email finds you well",
    ],
    ToneType.FRIENDLY: [
        "hope you're doing well", "great to hear", "thanks so much",
        "awesome", "sounds good", "happy to help", "no worries",
        "feel free", "let me know", "cheers", "hope that helps",
        "excited", "wonderful", "looking forward to", "glad",
        "appreciate it", "that's great", "love it", "nice work",
        "well done",
    ],
    ToneType.URGENT: [
        "asap", "urgent", "immediately", "right away", "critical",
        "time-sensitive", "deadline", "overdue", "must", "emergency",
        "as soon as possible", "by end of day", "cannot wait",
        "high priority", "escalate", "pressing", "without delay",
        "act now", "respond immediately", "don't delay",
    ],
    ToneType.PASSIVE_AGGRESSIVE: [
        "as per my last email", "per my previous", "as i mentioned",
        "i'm confused why", "just to clarify", "correct me if i'm wrong",
        "going forward", "as previously stated", "not sure if you saw",
        "friendly reminder", "just a gentle reminder", "as you should know",
        "i would have thought", "with all due respect", "no offense but",
        "i was under the impression", "surely you", "obviously",
        "as i already explained", "once again",
    ],
    ToneType.APOLOGETIC: [
        "sorry", "apologies", "i apologize", "my mistake", "my fault",
        "i regret", "unfortunately", "i'm afraid", "forgive me",
        "pardon", "excuse me", "i didn't mean to", "oversight",
        "i take responsibility", "my apologies", "regrettably",
        "i should have", "i wish i had", "i feel bad", "mea culpa",
    ],
    ToneType.DEMANDING: [
        "you must", "you need to", "i expect", "i demand", "do this now",
        "make sure", "ensure that", "it is imperative", "non-negotiable",
        "required", "mandatory", "you are responsible", "i insist",
        "no excuses", "failure to", "be advised", "you will",
        "this is not optional", "comply", "immediately address",
    ],
    ToneType.CASUAL: [
        "hey", "hi there", "what's up", "lol", "haha", "btw",
        "gonna", "wanna", "gotta", "cool", "yeah", "nope", "yep",
        "stuff", "things", "kinda", "sorta", "fyi", "tbh", "imo",
    ],
    ToneType.FORMAL: [
        "dear", "sincerely", "respectfully", "hereby", "furthermore",
        "moreover", "nevertheless", "notwithstanding", "aforementioned",
        "henceforth", "therein", "whereas", "accordingly", "thus",
        "therefore", "consequently", "in light of", "to whom it may concern",
        "yours faithfully", "with regards",
    ],
}


class ToneAnalyzer:
    """Analyzes email text to detect the dominant tone using keyword analysis."""

    def __init__(self) -> None:
        self._keywords = TONE_KEYWORDS

    def analyze(self, email: Email) -> ToneResult:
        """Analyze the tone of an email and return scored results."""
        text = email.full_text.lower()
        scores = self._score_all_tones(text)
        scores.sort(key=lambda s: s.score, reverse=True)
        dominant = scores[0].tone if scores and scores[0].score > 0 else ToneType.PROFESSIONAL
        return ToneResult(
            dominant_tone=dominant,
            tone_scores=scores,
            summary=self._build_summary(dominant, scores),
        )

    def _score_all_tones(self, text: str) -> list[ToneScore]:
        """Score text against all tone keyword lists."""
        results: list[ToneScore] = []
        for tone, keywords in self._keywords.items():
            found = [kw for kw in keywords if kw in text]
            score = min(len(found) / max(len(keywords) * 0.3, 1), 1.0)
            results.append(ToneScore(tone=tone, score=round(score, 3), keywords_found=found))
        return results

    def _build_summary(self, dominant: ToneType, scores: list[ToneScore]) -> str:
        """Build a human-readable summary."""
        strong = [s for s in scores if s.score >= 0.3 and s.tone != dominant]
        summary = f"The dominant tone is {dominant.value}."
        if strong:
            others = ", ".join(s.tone.value for s in strong[:3])
            summary += f" Secondary tones detected: {others}."
        return summary
