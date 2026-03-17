"""Rich console report for tone analysis."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tonecheck.models import (
    ToneResult, ToneRisk, RiskLevel, RewriteSuggestion, EmotionScore,
)

RISK_COLORS = {
    RiskLevel.LOW: "green",
    RiskLevel.MEDIUM: "yellow",
    RiskLevel.HIGH: "red",
    RiskLevel.CRITICAL: "bold red",
}


def print_report(
    tone_result: ToneResult,
    risk: ToneRisk,
    suggestions: list[RewriteSuggestion],
    console: Console | None = None,
) -> None:
    """Print a formatted tone analysis report to the console."""
    console = console or Console()

    # Header
    console.print(Panel("[bold]ToneCheck Analysis Report[/bold]", style="blue"))

    # Tone scores table
    tone_table = Table(title="Tone Analysis", show_lines=True)
    tone_table.add_column("Tone", style="cyan")
    tone_table.add_column("Score", justify="right")
    tone_table.add_column("Keywords Found")

    for ts in tone_result.tone_scores:
        bar_len = int(ts.score * 20)
        bar = "[green]" + "#" * bar_len + "[/green]" + "-" * (20 - bar_len)
        kw_str = ", ".join(ts.keywords_found[:5]) or "-"
        style = "bold" if ts.tone == tone_result.dominant_tone else ""
        tone_table.add_row(ts.tone.value, f"{ts.score:.2f} {bar}", kw_str, style=style)

    console.print(tone_table)
    console.print(f"\n[bold]Dominant tone:[/bold] {tone_result.dominant_tone.value}")
    console.print(f"[dim]{tone_result.summary}[/dim]\n")

    # Emotions
    if tone_result.emotions:
        emo_table = Table(title="Detected Emotions")
        emo_table.add_column("Emotion", style="magenta")
        emo_table.add_column("Intensity", justify="right")
        for e in tone_result.emotions[:5]:
            emo_table.add_row(e.emotion.value, f"{e.intensity:.2f}")
        console.print(emo_table)

    # Risk assessment
    color = RISK_COLORS.get(risk.level, "white")
    console.print(Panel(f"[{color}]Risk Level: {risk.level.value.upper()}[/{color}]", title="Risk Assessment"))

    if risk.issues:
        console.print("[bold]Issues:[/bold]")
        for issue in risk.issues:
            console.print(f"  [yellow]![/yellow] {issue}")

    if risk.flagged_phrases:
        console.print("\n[bold]Flagged Phrases:[/bold]")
        for phrase in risk.flagged_phrases:
            console.print(f'  [red]>[/red] "{phrase}"')

    # Suggestions
    if suggestions:
        console.print()
        sug_table = Table(title="Rewrite Suggestions", show_lines=True)
        sug_table.add_column("Original", style="red")
        sug_table.add_column("Suggested", style="green")
        sug_table.add_column("Reason")
        for s in suggestions:
            sug_table.add_row(s.original, s.suggested, s.reason)
        console.print(sug_table)

    if risk.suggestions:
        console.print("\n[bold]General Advice:[/bold]")
        for s in risk.suggestions:
            console.print(f"  [cyan]*[/cyan] {s}")
