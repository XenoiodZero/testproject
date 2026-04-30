"""Mission patches: achievements that unlock based on progress.counters.

Each achievement has an id, title, description, and a `predicate(progress)`
that returns True when it should unlock.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .progress import Progress


@dataclass
class Achievement:
    id: str
    title: str
    description: str
    predicate: Callable[[Progress], bool]
    xp_bonus: int = 25


ACHIEVEMENTS: list[Achievement] = [
    Achievement(
        "hello_universe",
        "Hello, Universe",
        "Run your very first Python program.",
        lambda p: p.get("runs") >= 1,
        xp_bonus=10,
    ),
    Achievement(
        "first_blood",
        "First Light",
        "Pass your first graded exercise.",
        lambda p: len(p.completed_exercises) >= 1,
        xp_bonus=20,
    ),
    Achievement(
        "loop_until_leo",
        "Loop Until LEO",
        "Pass 10 exercises that involve loops or iteration.",
        lambda p: p.get("loop_exercises") >= 10,
        xp_bonus=50,
    ),
    Achievement(
        "stage_separation",
        "Stage Separation",
        "Define and call your first function.",
        lambda p: p.get("functions_written") >= 1,
        xp_bonus=25,
    ),
    Achievement(
        "data_pilot",
        "Data Pilot",
        "Complete the lists & dicts modules.",
        lambda p: "m08_lists" in p.completed_lessons and "m09_dicts" in p.completed_lessons,
        xp_bonus=50,
    ),
    Achievement(
        "telemetry_engineer",
        "Telemetry Engineer",
        "Read your first file and parse some data.",
        lambda p: "m10_files" in p.completed_lessons,
        xp_bonus=50,
    ),
    Achievement(
        "object_in_orbit",
        "Object in Orbit",
        "Build your first class.",
        lambda p: p.get("classes_written") >= 1,
        xp_bonus=50,
    ),
    Achievement(
        "numpy_navigator",
        "NumPy Navigator",
        "Finish the NumPy module.",
        lambda p: "m13_numpy" in p.completed_lessons,
        xp_bonus=75,
    ),
    Achievement(
        "first_orbit",
        "First Orbit",
        "Finish Orbital Mechanics 101.",
        lambda p: "m15_orbits" in p.completed_lessons,
        xp_bonus=100,
    ),
    Achievement(
        "delta_v",
        "Delta-V",
        "Solve your first rocket-equation exercise.",
        lambda p: p.get("rocket_eq_solved") >= 1,
        xp_bonus=75,
    ),
    Achievement(
        "mars_or_bust",
        "Mars or Bust",
        "Complete the Hohmann Transfer final project.",
        lambda p: "fp_hohmann" in p.completed_projects,
        xp_bonus=200,
    ),
    Achievement(
        "saturn_v",
        "Saturn V",
        "Complete the Multi-Stage Rocket project.",
        lambda p: "fp_rocket" in p.completed_projects,
        xp_bonus=200,
    ),
    Achievement(
        "mission_control",
        "Mission Control",
        "Build your own dashboard app.",
        lambda p: "fp_dashboard" in p.completed_projects,
        xp_bonus=200,
    ),
    Achievement(
        "the_right_stuff",
        "The Right Stuff",
        "Finish all five capstone missions.",
        lambda p: len(p.completed_projects) >= 5,
        xp_bonus=500,
    ),
    Achievement(
        "streak_3",
        "Three-Day Burn",
        "Practice 3 days in a row.",
        lambda p: p.streak_days >= 3,
        xp_bonus=30,
    ),
    Achievement(
        "streak_7",
        "Lunar Week",
        "Practice 7 days in a row.",
        lambda p: p.streak_days >= 7,
        xp_bonus=75,
    ),
    Achievement(
        "perfectionist",
        "Pad 39A",
        "Pass 25 exercises total.",
        lambda p: len(p.completed_exercises) >= 25,
        xp_bonus=100,
    ),
    Achievement(
        "debug_ace",
        "Debug Ace",
        "Run code 100 times — practice makes perfect.",
        lambda p: p.get("runs") >= 100,
        xp_bonus=50,
    ),
]


def check_unlocks(progress: Progress) -> list[Achievement]:
    """Return any newly-unlocked achievements (and mutate progress to record them)."""
    newly: list[Achievement] = []
    for a in ACHIEVEMENTS:
        if a.id in progress.achievements:
            continue
        try:
            if a.predicate(progress):
                progress.achievements.add(a.id)
                progress.add_xp(a.xp_bonus)
                newly.append(a)
        except Exception:
            continue
    return newly
