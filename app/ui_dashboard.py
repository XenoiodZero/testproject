"""Mission Control dashboard: progress overview + Continue button."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from . import theme
from .achievements import ACHIEVEMENTS
from .curriculum import ALL_MODULES


def build_dashboard(parent: tk.Misc, app) -> None:
    """Lay out the dashboard inside `parent` (the content frame)."""
    progress = app.progress

    container = ttk.Frame(parent, style="Content.TFrame", padding=24)
    container.pack(fill="both", expand=True)

    # Top: greeting + summary
    ttk.Label(container, text="Mission Control", style="H1.TLabel").pack(anchor="w")
    idx, title, badge, into, span = theme.level_for_xp(progress.xp)
    ttk.Label(
        container,
        text=f"Welcome back, {title}.  ({progress.xp} XP / {app.total_xp_available} possible)",
        style="Muted.TLabel",
    ).pack(anchor="w", pady=(0, 16))

    # Stats cards row
    stats_row = ttk.Frame(container, style="Content.TFrame")
    stats_row.pack(fill="x", pady=(0, 16))
    for col in range(4):
        stats_row.columnconfigure(col, weight=1, uniform="stat")
    _stat_card(stats_row, 0, "LESSONS",  f"{len(progress.completed_lessons)}",
               f"of {sum(len(m.lessons) for m in ALL_MODULES)}")
    _stat_card(stats_row, 1, "EXERCISES", f"{len(progress.completed_exercises)}", "passed")
    _stat_card(stats_row, 2, "PROJECTS", f"{len(progress.completed_projects)}", "of 5 capstones")
    _stat_card(stats_row, 3, "PATCHES",  f"{len(progress.achievements)}",
               f"of {len(ACHIEVEMENTS)} unlocked")

    # Continue / next-up
    next_lesson, next_module = _find_next_lesson(progress)
    next_card = ttk.Frame(container, style="Card.TFrame", padding=20)
    next_card.pack(fill="x", pady=(0, 16))
    ttk.Label(next_card, text="UP NEXT", style="CardH.TLabel").pack(anchor="w")
    if next_lesson is None:
        ttk.Label(next_card, text="All lessons complete. Move on to the Capstone Missions!",
                  style="Card.TLabel", wraplength=900).pack(anchor="w", pady=(6, 10))
        btn = ttk.Button(next_card, text="View Capstones",
                         style="Primary.TButton",
                         command=lambda: app.show_module("m_capstones"))
        btn.pack(anchor="w")
    else:
        ttk.Label(next_card, text=next_lesson.title, style="Gold.TLabel").pack(anchor="w", pady=(4, 2))
        first_para = next_lesson.body.strip().split("\n\n")[0].replace("# ", "")
        ttk.Label(next_card, text=first_para[:240] + ("..." if len(first_para) > 240 else ""),
                  style="Card.TLabel", wraplength=1000, justify="left").pack(anchor="w", pady=(0, 12))
        btn = ttk.Button(next_card, text="Resume mission",
                         style="Primary.TButton",
                         command=lambda l=next_lesson, m=next_module: app.show_lesson(l.id, m.id))
        btn.pack(anchor="w")

    # Module grid
    grid_label = ttk.Label(container, text="Curriculum overview", style="H2.TLabel")
    grid_label.pack(anchor="w", pady=(8, 8))

    canvas = tk.Canvas(container, bg=theme.BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True, side="left")
    sb = ttk.Scrollbar(container, command=canvas.yview)
    sb.pack(fill="y", side="right")
    canvas.configure(yscrollcommand=sb.set)

    inner = ttk.Frame(canvas, style="Content.TFrame")
    canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure("all", width=e.width))

    last_phase = None
    for m in ALL_MODULES:
        if m.phase != last_phase:
            ttk.Label(inner, text=m.phase.upper(), style="Muted.TLabel").pack(anchor="w", pady=(12, 4))
            last_phase = m.phase
        _module_row(inner, m, app)


def _stat_card(parent: tk.Misc, col: int, label: str, big: str, sub: str) -> None:
    card = ttk.Frame(parent, style="Card.TFrame", padding=14)
    card.grid(row=0, column=col, sticky="nsew", padx=4)
    ttk.Label(card, text=label, style="CardH.TLabel").pack(anchor="w")
    tk.Label(card, text=big, bg=theme.BG_PANEL, fg=theme.FG, font=("Segoe UI Semibold", 28)).pack(anchor="w")
    ttk.Label(card, text=sub, style="Card.TLabel").pack(anchor="w")


def _module_row(parent: tk.Misc, m, app) -> None:
    row = ttk.Frame(parent, style="Card.TFrame", padding=10)
    row.pack(fill="x", padx=2, pady=3)
    row.columnconfigure(1, weight=1)

    # status dot
    done_count = sum(1 for l in m.lessons if l.id in app.progress.completed_lessons)
    total = len(m.lessons) + len(m.projects)
    done_total = done_count + sum(1 for p in m.projects if p.id in app.progress.completed_projects)
    if total > 0 and done_total == total:
        dot_color = theme.SUCCESS
        dot = "●"
    elif done_total > 0:
        dot_color = theme.GOLD
        dot = "◐"
    else:
        dot_color = theme.FG_MUTED
        dot = "○"
    tk.Label(row, text=dot, bg=theme.BG_PANEL, fg=dot_color,
             font=("Segoe UI", 14)).grid(row=0, column=0, padx=(4, 12))

    info = ttk.Frame(row, style="Card.TFrame")
    info.grid(row=0, column=1, sticky="ew")
    ttk.Label(info, text=m.title, style="CardH.TLabel").pack(anchor="w")
    ttk.Label(info, text=m.tagline, style="Card.TLabel").pack(anchor="w")
    if total:
        ttk.Label(info, text=f"{done_total}/{total} complete", style="Card.TLabel").pack(anchor="w")

    btn = ttk.Button(row, text="Open ▸", command=lambda mid=m.id: app.show_module(mid))
    btn.grid(row=0, column=2, padx=8)


def _find_next_lesson(progress):
    """Return the first incomplete (lesson, module) pair, or (None, None)."""
    for m in ALL_MODULES:
        for l in m.lessons:
            if l.id not in progress.completed_lessons:
                return l, m
    return None, None
