"""Dataclasses describing the curriculum."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Union

from ..grader import Check


@dataclass
class Resource:
    title: str
    url: str
    note: str = ""


@dataclass
class QuizQuestion:
    prompt: str
    choices: list[str]
    correct_index: int
    explanation: str = ""


@dataclass
class Quiz:
    questions: list[QuizQuestion]
    xp_per_correct: int = 5


@dataclass
class Exercise:
    id: str
    title: str
    prompt: str
    starter_code: str
    checks: list[Check]
    hints: list[str] = field(default_factory=list)
    xp: int = 25
    counter_keys: list[str] = field(default_factory=list)
    # Optional pre-supplied stdin if the exercise uses input()
    stdin: str = ""


@dataclass
class Lesson:
    id: str
    title: str
    body: str  # markdown-lite, rendered by ui_lesson
    exercises: list[Exercise] = field(default_factory=list)
    quiz: Quiz | None = None
    resources: list[Resource] = field(default_factory=list)
    xp_on_complete: int = 50


@dataclass
class Project:
    id: str
    title: str
    summary: str
    brief: str            # the long-form mission brief (markdown-lite)
    starter_code: str
    checks: list[Check]
    bonus_objectives: list[str] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)
    resources: list[Resource] = field(default_factory=list)
    xp: int = 500


@dataclass
class Module:
    id: str
    title: str
    tagline: str
    phase: str            # "Boot Camp" / "Flight School" / "Mission Specialist" / "Capstone"
    lessons: list[Lesson] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)


Item = Union[Lesson, Project]
