"""Emotion detection from text."""

from __future__ import annotations

from tonecheck.models import EmotionType, EmotionScore


EMOTION_KEYWORDS: dict[EmotionType, list[str]] = {
    EmotionType.JOY: [
        "happy", "glad", "excited", "delighted", "thrilled", "wonderful",
        "fantastic", "great", "love", "enjoy", "pleased", "grateful",
        "thankful", "awesome", "excellent", "amazing", "celebrate",
    ],
    EmotionType.ANGER: [
        "angry", "furious", "frustrated", "annoyed", "irritated",
        "unacceptable", "outraged", "disgusted", "livid", "fed up",
        "infuriating", "ridiculous", "absurd", "intolerable",
    ],
    EmotionType.FEAR: [
        "worried", "concerned", "anxious", "afraid", "scared",
        "nervous", "uneasy", "apprehensive", "dread", "alarming",
        "terrified", "panic", "risk", "threat", "danger",
    ],
    EmotionType.SADNESS: [
        "sad", "disappointed", "unfortunate", "regret", "sorry",
        "heartbroken", "miss", "loss", "painful", "unhappy",
        "devastated", "depressed", "hopeless", "grief",
    ],
    EmotionType.SURPRISE: [
        "surprised", "shocked", "unexpected", "astonished", "amazed",
        "stunned", "unbelievable", "incredible", "startled", "wow",
    ],
    EmotionType.TRUST: [
        "trust", "reliable", "confident", "depend", "count on",
        "faithful", "honest", "integrity", "committed", "loyal",
        "assure", "guarantee", "promise",
    ],
    EmotionType.ANTICIPATION: [
        "looking forward", "expect", "anticipate", "hope", "plan",
        "upcoming", "eager", "await", "soon", "prepare", "ready",
    ],
}


class EmotionDetector:
    """Maps email text to emotional dimensions."""

    def __init__(self) -> None:
        self._keywords = EMOTION_KEYWORDS

    def detect(self, text: str) -> list[EmotionScore]:
        """Detect emotions present in the text."""
        text_lower = text.lower()
        scores: list[EmotionScore] = []

        for emotion, keywords in self._keywords.items():
            found = sum(1 for kw in keywords if kw in text_lower)
            if found > 0:
                intensity = min(found / max(len(keywords) * 0.25, 1), 1.0)
                scores.append(EmotionScore(emotion=emotion, intensity=round(intensity, 3)))

        if not scores:
            scores.append(EmotionScore(emotion=EmotionType.NEUTRAL, intensity=1.0))

        scores.sort(key=lambda s: s.intensity, reverse=True)
        return scores
