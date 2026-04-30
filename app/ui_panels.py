"""Achievements and settings panels."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from . import theme, progress as progress_mod, ai_client
from .achievements import ACHIEVEMENTS


def build_achievements(parent: tk.Misc, app) -> None:
    frame = ttk.Frame(parent, style="Content.TFrame", padding=24)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Mission Patches", style="H1.TLabel").pack(anchor="w")
    earned = len(app.progress.achievements)
    total = len(ACHIEVEMENTS)
    ttk.Label(frame, text=f"{earned}/{total} unlocked", style="Muted.TLabel").pack(anchor="w", pady=(0, 12))

    canvas = tk.Canvas(frame, bg=theme.BG, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    sb = ttk.Scrollbar(frame, command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=sb.set)

    inner = ttk.Frame(canvas, style="Content.TFrame")
    canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure("all", width=e.width))

    inner.columnconfigure(0, weight=1)
    inner.columnconfigure(1, weight=1)

    for i, a in enumerate(ACHIEVEMENTS):
        row, col = divmod(i, 2)
        unlocked = a.id in app.progress.achievements
        card = ttk.Frame(inner, style="Card.TFrame", padding=12)
        card.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        head = ttk.Frame(card, style="Card.TFrame")
        head.pack(fill="x")
        emoji = "★" if unlocked else "☆"
        color = theme.GOLD if unlocked else theme.FG_MUTED
        tk.Label(head, text=emoji, bg=theme.BG_PANEL, fg=color, font=("Segoe UI", 18)
                 ).pack(side="left", padx=(0, 8))
        tk.Label(head, text=a.title, bg=theme.BG_PANEL, fg=color, font=theme.FONT_H3,
                 anchor="w").pack(side="left")
        tk.Label(head, text=f"+{a.xp_bonus} XP", bg=theme.BG_PANEL, fg=theme.PURPLE,
                 font=theme.FONT_SMALL).pack(side="right")
        tk.Label(card, text=a.description, bg=theme.BG_PANEL,
                 fg=theme.FG if unlocked else theme.FG_MUTED,
                 font=theme.FONT_BODY, anchor="w", justify="left",
                 wraplength=460).pack(anchor="w", pady=(4, 0))


def build_settings(parent: tk.Misc, app) -> None:
    frame = ttk.Frame(parent, style="Content.TFrame", padding=24)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Settings", style="H1.TLabel").pack(anchor="w")
    ttk.Label(frame,
              text="Local-only. Nothing leaves your machine except API requests you trigger explicitly.",
              style="Muted.TLabel").pack(anchor="w", pady=(0, 16))

    # ---- API key card ------------------------------------------------
    card = ttk.Frame(frame, style="Card.TFrame", padding=16)
    card.pack(fill="x", pady=(0, 12))
    ttk.Label(card, text="🛰 Mission Control AI helper", style="CardH.TLabel").pack(anchor="w")
    ttk.Label(card,
              text=("Optional. Add an Anthropic API key to enable the 'Ping Mission Control' button. "
                    "Your key is saved locally in ~/.mission_python/save.json. The 'anthropic' Python package "
                    "must be installed (it is, if you used the included requirements.txt)."),
              style="Card.TLabel", wraplength=900, justify="left").pack(anchor="w", pady=(4, 8))

    api_var = tk.StringVar(value=app.progress.api_key)
    show_var = tk.BooleanVar(value=False)
    entry = ttk.Entry(card, textvariable=api_var, font=theme.FONT_CODE, width=72, show="•")
    entry.pack(fill="x", pady=(2, 4))

    def toggle_show():
        entry.configure(show="" if show_var.get() else "•")

    tk.Checkbutton(card, text="Show key", variable=show_var, command=toggle_show,
                   bg=theme.BG_PANEL, fg=theme.FG, selectcolor=theme.BG_INSET,
                   activebackground=theme.BG_PANEL, activeforeground=theme.FG,
                   font=theme.FONT_SMALL).pack(anchor="w")

    status_label = ttk.Label(card, text=_status_text(app), style="Card.TLabel")
    status_label.pack(anchor="w", pady=(4, 0))

    btn_row = ttk.Frame(card, style="Card.TFrame")
    btn_row.pack(anchor="w", pady=(8, 0))

    def save():
        app.progress.api_key = api_var.get().strip()
        progress_mod.save(app.progress)
        status_label.configure(text=_status_text(app))
        app.toast.show("Saved", "API key stored locally.", color=theme.SUCCESS)

    def clear():
        api_var.set("")
        app.progress.api_key = ""
        progress_mod.save(app.progress)
        status_label.configure(text=_status_text(app))

    ttk.Button(btn_row, text="Save", style="Primary.TButton", command=save).pack(side="left")
    ttk.Button(btn_row, text="Clear", command=clear).pack(side="left", padx=6)
    tk.Label(btn_row,
             text="Get a key at console.anthropic.com",
             bg=theme.BG_PANEL, fg=theme.ACCENT, font=theme.FONT_SMALL).pack(side="left", padx=10)

    # ---- save card ---------------------------------------------------
    card2 = ttk.Frame(frame, style="Card.TFrame", padding=16)
    card2.pack(fill="x", pady=(0, 12))
    ttk.Label(card2, text="Save file", style="CardH.TLabel").pack(anchor="w")
    save_path = progress_mod.save_path()
    tk.Label(card2, text=str(save_path), bg=theme.BG_PANEL, fg=theme.FG,
             font=theme.FONT_CODE_SMALL, anchor="w", justify="left",
             wraplength=900).pack(anchor="w", pady=(4, 4))
    tk.Label(card2,
             text=("Backup or share this file to move your progress between machines. "
                   "Delete it to start over."),
             bg=theme.BG_PANEL, fg=theme.FG_MUTED, font=theme.FONT_SMALL,
             wraplength=900, justify="left").pack(anchor="w")

    # ---- about -------------------------------------------------------
    card3 = ttk.Frame(frame, style="Card.TFrame", padding=16)
    card3.pack(fill="x")
    ttk.Label(card3, text="About", style="CardH.TLabel").pack(anchor="w")
    tk.Label(card3,
             text=("Mission: Python is a hands-on Python course aimed at total beginners "
                   "with a love of space. 18 modules + 5 capstones, all local. "
                   "Source: edit anything in app/curriculum/ to add your own lessons."),
             bg=theme.BG_PANEL, fg=theme.FG, font=theme.FONT_BODY,
             wraplength=900, justify="left").pack(anchor="w", pady=(4, 0))


def _status_text(app) -> str:
    if not app.progress.api_key.strip():
        return "Status: no key set — AI helper disabled."
    if not ai_client.is_available(app.progress.api_key):
        return "Status: key set, but `anthropic` package not installed.  Run: pip install anthropic"
    return "Status: key set ✓ — Ping Mission Control is live."
