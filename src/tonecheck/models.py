"""Data models for ToneCheck."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ToneType(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    URGENT = "urgent"
    PASSIVE_AGGRESSIVE = "passive_aggressive"
    APOLOGETIC = "apologetic"
    DEMANDING = "demanding"
    CASUAL = "casual"
    FORMAL = "formal"


class EmotionType(str, Enum):
    JOY = "joy"
    ANGER = "anger"
    FEAR = "fear"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    NEUTRAL = "neutral"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Email(BaseModel):
    """Represents an email to be analyzed."""

    subject: str = ""
    body: str
    recipient: str = ""
    sender: str = ""

    @property
    def full_text(self) -> str:
        parts = []
        if self.subject:
            parts.append(self.subject)
        parts.append(self.body)
        return " ".join(parts)


class ToneScore(BaseModel):
    """Score for a single tone dimension."""

    tone: ToneType
    score: float = Field(ge=0.0, le=1.0)
    keywords_found: list[str] = Field(default_factory=list)


class EmotionScore(BaseModel):
    """Score for a detected emotion."""

    emotion: EmotionType
    intensity: float = Field(ge=0.0, le=1.0)


class ToneResult(BaseModel):
    """Complete tone analysis result."""

    dominant_tone: ToneType
    tone_scores: list[ToneScore] = Field(default_factory=list)
    emotions: list[EmotionScore] = Field(default_factory=list)
    summary: str = ""


class ToneRisk(BaseModel):
    """Risk assessment for an email's tone."""

    level: RiskLevel
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    flagged_phrases: list[str] = Field(default_factory=list)


class RewriteSuggestion(BaseModel):
    """A suggested rewrite for a phrase or sentence."""

    original: str
    suggested: str
    reason: str
    target_tone: Optional[ToneType] = None
