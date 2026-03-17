"""Tests for emotion detection."""

from tonecheck.analyzer.emotion import EmotionDetector
from tonecheck.models import EmotionType


def test_joy_detected():
    scores = EmotionDetector().detect("I'm so happy and excited about this wonderful news!")
    emotions = {s.emotion: s.intensity for s in scores}
    assert EmotionType.JOY in emotions
    assert emotions[EmotionType.JOY] > 0.3


def test_anger_detected():
    scores = EmotionDetector().detect("This is unacceptable and ridiculous. I am furious and frustrated.")
    emotions = {s.emotion: s.intensity for s in scores}
    assert EmotionType.ANGER in emotions


def test_neutral_when_no_emotion():
    scores = EmotionDetector().detect("The report is attached.")
    emotions = {s.emotion for s in scores}
    assert EmotionType.NEUTRAL in emotions


def test_multiple_emotions():
    scores = EmotionDetector().detect("I'm worried but hopeful about the upcoming changes. I trust the team.")
    assert len(scores) >= 2
