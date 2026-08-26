"""AI Skill: Summarizer and Translator."""

from ai.skills.base import Skill, string_parameters
from ai.providers import Tool


def _run_summarize(kernel, text: str, max_points: str = "5") -> str:
    try:
        n = int(max_points)
    except ValueError:
        n = 5

    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]

    if len(sentences) <= n:
        points = sentences
    else:
        step = len(sentences) / n
        points = [sentences[int(i * step)] for i in range(n)]

    summary = "\n".join(f"• {p}." for p in points)
    return (
        f"📋 Summary ({len(sentences)} sentences → {len(points)} points):\n\n"
        f"{summary}\n\n"
        f"💡 Tip: Use me to summarize notes, articles, or any text!"
    )


def _run_translate(kernel, text: str, target_language: str = "spanish") -> str:
    return (
        f"🌐 Translation → {target_language.title()}:\n\n"
        f"Original: {text}\n\n"
        f"For accurate translations, ask Nova AI (click ◈ Nova) "
        f"which has access to translation models.\n\n"
        f"💡 Tip: I can also help with code, notes, and system commands!"
    )


SKILLS = (
    Skill(
        tool=Tool(
            name="summarize",
            description="Summarize text into key points",
            parameters=string_parameters(
                text="The text to summarize",
                max_points="Maximum number of summary points (default: 5)"
            ),
        ),
        run=_run_summarize,
    ),
    Skill(
        tool=Tool(
            name="translate_text",
            description="Translate text to another language",
            parameters=string_parameters(
                text="The text to translate",
                target_language="Target language (e.g., spanish, french, german)"
            ),
        ),
        run=_run_translate,
    ),
)
