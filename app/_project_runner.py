"""Project workspace: a beefier exercise panel for capstones."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from . import theme, progress as progress_mod, ai_client
from .grader import grade
from .runner import run_code
from .ui_widgets import CodeEditor


def build_project_workspace(parent, app, module_id, project) -> None:
    parent.columnconfigure(0, weight=1)
    parent.rowconfigure(1, weight=2)
    parent.rowconfigure(3, weight=1)

    ttk.Label(parent, text=project.summary, style="H3.TLabel",
              wraplength=720).grid(row=0, column=0, sticky="w", padx=4, pady=(0, 6))

    editor = CodeEditor(parent, height=22)
    editor.set_code(project.starter_code)
    editor.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)

    btns = ttk.Frame(parent, style="Content.TFrame")
    btns.grid(row=2, column=0, sticky="ew", padx=4, pady=4)
    btn_run = ttk.Button(btns, text="▶ Run")
    btn_run.pack(side="left")
    btn_check = ttk.Button(btns, text="Submit Mission ✓", style="Primary.TButton")
    btn_check.pack(side="left", padx=6)
    btn_reset = ttk.Button(btns, text="Reset to brief")
    btn_reset.pack(side="left")
    hint_state = {"index": 0}
    btn_hint = ttk.Button(btns, text="Hint")
    btn_hint.pack(side="left", padx=6)
    btn_ai = ttk.Button(btns, text="🛰 Ping Mission Control")
    btn_ai.pack(side="right")

    out_frame = ttk.Frame(parent, style="Content.TFrame")
    out_frame.grid(row=3, column=0, sticky="nsew", padx=4, pady=(4, 4))
    out = tk.Text(out_frame, height=10, wrap="word", bg=theme.BG_INSET, fg=theme.FG,
                  font=theme.FONT_CODE_SMALL, borderwidth=0, highlightthickness=1,
                  highlightbackground=theme.GRID)
    out_scroll = ttk.Scrollbar(out_frame, command=out.yview)
    out.configure(yscrollcommand=out_scroll.set)
    out.pack(side="left", fill="both", expand=True)
    out_scroll.pack(side="right", fill="y")
    out.tag_configure("ok", foreground=theme.SUCCESS)
    out.tag_configure("err", foreground=theme.ERROR)
    out.tag_configure("dim", foreground=theme.FG_MUTED)
    out.tag_configure("warn", foreground=theme.WARNING)
    out.tag_configure("hint", foreground=theme.GOLD)
    out.tag_configure("ai", foreground=theme.PURPLE)
    out.configure(state="disabled")

    last_error = {"text": ""}

    def append(s, tag=None):
        out.configure(state="normal")
        out.insert("end", s, tag) if tag else out.insert("end", s)
        out.see("end")
        out.configure(state="disabled")

    def clear():
        out.configure(state="normal")
        out.delete("1.0", "end")
        out.configure(state="disabled")

    def on_run():
        clear()
        append("Running mission code...\n", "dim")
        code = editor.get_code()
        app.progress.bump("runs")

        def worker():
            res = run_code(code, timeout=120.0)
            def show():
                if res.stdout:
                    append(res.stdout)
                if res.stderr:
                    append(res.stderr, "err")
                    last_error["text"] = res.stderr
                else:
                    last_error["text"] = ""
                if res.timed_out:
                    append("\n⏱ Timed out (2 min).\n", "warn")
                progress_mod.save(app.progress)
                app.check_achievements()
            parent.after(0, show)

        threading.Thread(target=worker, daemon=True).start()

    btn_run.configure(command=on_run)

    def on_check():
        clear()
        append("Submitting for mission review...\n", "dim")
        code = editor.get_code()

        def worker():
            ok, results = grade(code, project.checks)
            def show():
                for r in results:
                    mark = "✓" if r.ok else "✗"
                    tag = "ok" if r.ok else "err"
                    append(f"{mark} {r.label}\n", tag)
                    if not r.ok and r.detail:
                        for line in r.detail.splitlines():
                            append("    " + line + "\n", "dim")
                if ok:
                    if project.id not in app.progress.completed_projects:
                        app.progress.completed_projects.add(project.id)
                        app.award_xp(project.xp, f"Capstone: {project.title}")
                    else:
                        app.toast.show("Already complete", "Already cleared this capstone!",
                                       color=theme.SUCCESS, duration_ms=2000)
                    append("\n🚀🚀🚀 MISSION COMPLETE 🚀🚀🚀\n", "ok")
                    app.check_achievements()
                else:
                    append("\nSome objectives still unmet — keep going.\n", "warn")
            parent.after(0, show)

        threading.Thread(target=worker, daemon=True).start()

    btn_check.configure(command=on_check)

    def on_reset():
        editor.set_code(project.starter_code)
        clear()
        append("Reset to mission brief starter.\n", "dim")
        hint_state["index"] = 0

    btn_reset.configure(command=on_reset)

    def on_hint():
        if not project.hints:
            append("No hints for this capstone — read the brief carefully.\n", "dim")
            return
        i = hint_state["index"]
        if i >= len(project.hints):
            append("(no more hints)\n", "dim")
            return
        append(f"\nHint {i + 1}/{len(project.hints)}: {project.hints[i]}\n", "hint")
        hint_state["index"] = i + 1

    btn_hint.configure(command=on_hint)

    def on_ai():
        api_key = app.progress.api_key
        if not ai_client.is_available(api_key):
            append(
                "\nAI helper not available. Set your Anthropic API key in Settings, "
                "and run: pip install anthropic\n",
                "warn",
            )
            return
        append("\n🛰 Pinging Mission Control...\n", "ai")
        code = editor.get_code()

        def on_chunk(s: str):
            parent.after(0, lambda: append(s, "ai"))

        def on_done(_full: str):
            parent.after(0, lambda: append("\n", None))

        def on_error(msg: str):
            parent.after(0, lambda: append(f"\nAI error: {msg}\n", "err"))

        ai_client.ping(
            api_key=api_key,
            lesson_title=f"Capstone: {project.title}",
            exercise_prompt=project.brief,
            user_code=code,
            last_error=last_error["text"],
            on_chunk=on_chunk,
            on_done=on_done,
            on_error=on_error,
        )

    btn_ai.configure(command=on_ai)
