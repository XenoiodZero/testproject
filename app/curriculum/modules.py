"""Module registry — ordered list of every Module in the curriculum, plus capstones."""
from __future__ import annotations

from ._types import Module, Lesson, Project, Exercise
from .m01_first_contact import M01
from .m02_variables import M02
from .m03_numbers import M03
from .m04_strings import M04
from .m05_conditionals import M05
from .m06_loops import M06
from .m07_functions import M07
from .m08_lists import M08
from .m09_dicts import M09
from .m10_files import M10
from .m11_oop import M11
from .m12_errors import M12
from .m13_numpy import M13
from .m14_plotting import M14
from .m15_orbits import M15
from .m16_rocket_eq import M16
from .m17_telemetry import M17
from .m18_lander import M18
from .final_projects_a import HOHMANN, MULTI_STAGE
from .final_projects_b import ISS_TRACKER, DASHBOARD, PROPAGATOR


CAPSTONE = Module(
    id="m_capstones",
    title="Capstone Missions",
    tagline="Five long boss-fight projects. Show what you've learned.",
    phase="Capstone",
    lessons=[],
    projects=[HOHMANN, MULTI_STAGE, ISS_TRACKER, DASHBOARD, PROPAGATOR],
)


ALL_MODULES: list[Module] = [
    M01, M02, M03, M04, M05, M06,
    M07, M08, M09, M10, M11, M12,
    M13, M14, M15, M16, M17, M18,
    CAPSTONE,
]


def get_module(module_id: str) -> Module | None:
    return next((m for m in ALL_MODULES if m.id == module_id), None)


def get_lesson(lesson_id: str) -> Lesson | None:
    for m in ALL_MODULES:
        for l in m.lessons:
            if l.id == lesson_id:
                return l
    return None


def get_exercise(exercise_id: str) -> Exercise | None:
    for m in ALL_MODULES:
        for l in m.lessons:
            for ex in l.exercises:
                if ex.id == exercise_id:
                    return ex
    return None


def get_project(project_id: str) -> Project | None:
    for m in ALL_MODULES:
        for p in m.projects:
            if p.id == project_id:
                return p
    return None


def total_xp_available() -> int:
    total = 0
    for m in ALL_MODULES:
        for l in m.lessons:
            total += l.xp_on_complete
            for ex in l.exercises:
                total += ex.xp
            if l.quiz:
                total += l.quiz.xp_per_correct * len(l.quiz.questions)
        for p in m.projects:
            total += p.xp
    return total
