"""Persistent progress: XP, completed lessons/exercises, achievements, settings."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


def save_path() -> Path:
    home = Path(os.path.expanduser("~"))
    folder = home / ".mission_python"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "save.json"


@dataclass
class Progress:
    xp: int = 0
    completed_lessons: set[str] = field(default_factory=set)
    completed_exercises: set[str] = field(default_factory=set)
    completed_projects: set[str] = field(default_factory=set)
    achievements: set[str] = field(default_factory=set)
    streak_days: int = 0
    last_active_date: str = ""    # YYYY-MM-DD
    api_key: str = ""
    counters: dict[str, int] = field(default_factory=dict)
    # Free-text notes you jot during projects, keyed by project_id
    project_notes: dict[str, str] = field(default_factory=dict)

    # ---- XP / level ------------------------------------------------------
    def add_xp(self, amount: int) -> int:
        self.xp += max(0, int(amount))
        return self.xp

    # ---- counters (for achievement triggers) -----------------------------
    def bump(self, key: str, by: int = 1) -> int:
        self.counters[key] = self.counters.get(key, 0) + by
        return self.counters[key]

    def get(self, key: str) -> int:
        return self.counters.get(key, 0)

    # ---- daily streak ----------------------------------------------------
    def touch_streak(self) -> None:
        today = time.strftime("%Y-%m-%d")
        if self.last_active_date == today:
            return
        if self.last_active_date:
            # crude consecutive-day check
            try:
                last = time.strptime(self.last_active_date, "%Y-%m-%d")
                last_day = int(time.mktime(last) // 86400)
                today_day = int(time.time() // 86400)
                if today_day - last_day == 1:
                    self.streak_days += 1
                elif today_day - last_day > 1:
                    self.streak_days = 1
            except ValueError:
                self.streak_days = 1
        else:
            self.streak_days = 1
        self.last_active_date = today

    # ---- (de)serialization ----------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["completed_lessons"] = sorted(self.completed_lessons)
        d["completed_exercises"] = sorted(self.completed_exercises)
        d["completed_projects"] = sorted(self.completed_projects)
        d["achievements"] = sorted(self.achievements)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Progress":
        return cls(
            xp=int(d.get("xp", 0)),
            completed_lessons=set(d.get("completed_lessons", [])),
            completed_exercises=set(d.get("completed_exercises", [])),
            completed_projects=set(d.get("completed_projects", [])),
            achievements=set(d.get("achievements", [])),
            streak_days=int(d.get("streak_days", 0)),
            last_active_date=str(d.get("last_active_date", "")),
            api_key=str(d.get("api_key", "")),
            counters=dict(d.get("counters", {})),
            project_notes=dict(d.get("project_notes", {})),
        )


def load() -> Progress:
    p = save_path()
    if not p.exists():
        return Progress()
    try:
        with p.open("r", encoding="utf-8") as f:
            return Progress.from_dict(json.load(f))
    except (OSError, ValueError, json.JSONDecodeError):
        backup = p.with_suffix(".broken.json")
        try:
            p.replace(backup)
        except OSError:
            pass
        return Progress()


def save(progress: Progress) -> None:
    p = save_path()
    tmp = p.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(progress.to_dict(), f, indent=2)
    tmp.replace(p)
