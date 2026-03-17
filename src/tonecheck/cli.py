"""CLI interface for ToneCheck."""

from __future__ import annotations

import sys

import click
from rich.console import Console

from tonecheck.models import Email, ToneType
from tonecheck.analyzer.tone import ToneAnalyzer
from tonecheck.analyzer.emotion import EmotionDetector
from tonecheck.analyzer.risk import ToneRiskAssessor
from tonecheck.rewriter.suggester import ToneSuggester
from tonecheck.rewriter.rewriter import ToneRewriter
from tonecheck.report import print_report


@click.group()
def main() -> None:
    """ToneCheck - Email Tone Detector and Improver."""


@main.command()
@click.option("--subject", "-s", default="", help="Email subject line.")
@click.option("--body", "-b", default=None, help="Email body text. Reads from stdin if not provided.")
@click.option("--target-tone", "-t", type=click.Choice([t.value for t in ToneType]), default="professional")
def analyze(subject: str, body: str | None, target_tone: str) -> None:
    """Analyze the tone of an email."""
    if body is None:
        if sys.stdin.isatty():
            click.echo("Enter email body (Ctrl+D to finish):")
        body = sys.stdin.read()

    email = Email(subject=subject, body=body)
    target = ToneType(target_tone)

    analyzer = ToneAnalyzer()
    emotion_detector = EmotionDetector()
    risk_assessor = ToneRiskAssessor()
    suggester = ToneSuggester()

    tone_result = analyzer.analyze(email)
    tone_result.emotions = emotion_detector.detect(email.full_text)
    risk = risk_assessor.assess(email, tone_result)
    suggestions = suggester.suggest(email, tone_result, risk, target)

    print_report(tone_result, risk, suggestions)


@main.command()
@click.option("--body", "-b", required=True, help="Email body text to rewrite.")
@click.option("--target-tone", "-t", type=click.Choice([t.value for t in ToneType]), default="professional")
def rewrite(body: str, target_tone: str) -> None:
    """Rewrite an email with improved tone."""
    email = Email(body=body)
    target = ToneType(target_tone)
    rewriter = ToneRewriter()
    result = rewriter.rewrite(email, target)
    console = Console()
    console.print("[bold]Rewritten email:[/bold]\n")
    console.print(result)


if __name__ == "__main__":
    main()
