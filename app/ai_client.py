"""Optional Claude API helper.

Used by the 'Ping Mission Control' button. If no API key is configured, the UI
should hide / disable the button. We intentionally lazy-import `anthropic` so
the rest of the app runs even without it installed.
"""
from __future__ import annotations

import threading
from typing import Callable


SYSTEM = (
    "You are Mission Control, an encouraging Python tutor inside a desktop "
    "learning app called Mission: Python. The student is a total beginner who "
    "loves gaming and wants to learn Python for aerospace / NASA / space "
    "applications. They will share the lesson context, an exercise prompt, "
    "and their current code. Your job:\n"
    "1) Give the smallest hint that unblocks them. Don't dump the full answer "
    "unless they explicitly ask after 2 hints.\n"
    "2) Be specific about *which line* or *which concept* is off.\n"
    "3) Use a friendly mission-control voice ('copy that, cadet'). Keep "
    "responses short — 4-8 sentences, code blocks only when needed.\n"
    "4) When you do show code, show only the minimum diff/snippet."
)


def is_available(api_key: str) -> bool:
    if not api_key.strip():
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return True


def ping(
    api_key: str,
    lesson_title: str,
    exercise_prompt: str,
    user_code: str,
    last_error: str = "",
    extra_question: str = "",
    on_chunk: Callable[[str], None] | None = None,
    on_done: Callable[[str], None] | None = None,
    on_error: Callable[[str], None] | None = None,
) -> threading.Thread:
    """Stream a hint from Claude on a background thread.

    Returns the thread; call .join() if you want to block.
    """
    def _run() -> None:
        try:
            import anthropic
        except ImportError:
            if on_error:
                on_error("The 'anthropic' package isn't installed. Run: pip install anthropic")
            return
        try:
            client = anthropic.Anthropic(api_key=api_key)
            user_block = (
                f"# Lesson\n{lesson_title}\n\n"
                f"# Exercise prompt\n{exercise_prompt}\n\n"
                f"# My current code\n```python\n{user_code}\n```\n"
            )
            if last_error.strip():
                user_block += f"\n# What happened when I ran it\n```\n{last_error.strip()}\n```\n"
            if extra_question.strip():
                user_block += f"\n# My question\n{extra_question.strip()}\n"
            else:
                user_block += "\n# My question\nI'm stuck — what's the smallest next step?\n"

            full: list[str] = []
            with client.messages.stream(
                model="claude-haiku-4-5-20251001",
                max_tokens=800,
                system=SYSTEM,
                messages=[{"role": "user", "content": user_block}],
            ) as stream:
                for text in stream.text_stream:
                    full.append(text)
                    if on_chunk:
                        on_chunk(text)
            if on_done:
                on_done("".join(full))
        except Exception as exc:  # pragma: no cover - UI surface
            if on_error:
                on_error(f"{type(exc).__name__}: {exc}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t
