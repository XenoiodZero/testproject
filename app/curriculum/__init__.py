"""Curriculum content. Modules are pure data — easy to extend."""
from ._types import Lesson, Exercise, Project, Module, Quiz, QuizQuestion, Resource
from .modules import ALL_MODULES, get_module, get_lesson, get_exercise, get_project

__all__ = [
    "Lesson", "Exercise", "Project", "Module", "Quiz", "QuizQuestion", "Resource",
    "ALL_MODULES", "get_module", "get_lesson", "get_exercise", "get_project",
]
