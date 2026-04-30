"""Lesson, exercise, project views — where the user reads, codes, runs, gets graded."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from . import theme, progress as progress_mod, ai_client
from .curriculum import get_lesson, get_module, get_project
from .grader import grade
from .runner import run_code
from .ui_widgets import CodeEditor, render_markdown


# --------------------------------------------------------------------------
# Module index page
# --------------------------------------------------------------------------
def build_module_view(parent: tk.Misc, app, module) -> None:
    frame = ttk.Frame(parent, style="Content.TFrame", padding=24)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=module.title, style="H1.TLabel").pack(anchor="w")
    ttk.Label(frame, text=module.tagline, style="Muted.TLabel").pack(anchor="w", pady=(0, 16))
    ttk.Label(frame, text=f"Phase: {module.phase}", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))

    for lesson in module.lessons:
        card = ttk.Frame(frame, style="Card.TFrame", padding=14)
        card.pack(fill="x", pady=4)
        card.columnconfigure(0, weight=1)
        done = lesson.id in app.progress.completed_lessons
        title = ("✓ " if done else "  ") + lesson.title
        ttk.Label(card, text=title, style="Gold.TLabel" if done else "CardH.TLabel").grid(
            row=0, column=0, sticky="w")
        n_ex = len(lesson.exercises)
        n_done = sum(1 for ex in lesson.exercises if ex.id in app.progress.completed_exercises)
        info = f"{n_done}/{n_ex} exercises"
        if lesson.quiz:
            info += f" · {len(lesson.quiz.questions)} quiz Qs"
        ttk.Label(card, text=info, style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 0))
        ttk.Button(card, text="Open ▸", style="Primary.TButton",
                   command=lambda lid=lesson.id, mid=module.id: app.show_lesson(lid, mid)
                   ).grid(row=0, column=1, rowspan=2, padx=8)

    if module.projects:
        ttk.Label(frame, text="Projects", style="H2.TLabel").pack(anchor="w", pady=(20, 6))
        for project in module.projects:
            card = ttk.Frame(frame, style="Card.TFrame", padding=14)
            card.pack(fill="x", pady=4)
            card.columnconfigure(0, weight=1)
            done = project.id in app.progress.completed_projects
            title = ("✓ " if done else "★ ") + project.title
            ttk.Label(card, text=title,
                      style="Gold.TLabel" if done else "CardH.TLabel").grid(row=0, column=0, sticky="w")
            ttk.Label(card, text=project.summary, style="Card.TLabel",
                      wraplength=900, justify="left").grid(row=1, column=0, sticky="w", pady=(4, 0))
            ttk.Label(card, text=f"+{project.xp} XP", style="Card.TLabel").grid(row=2, column=0, sticky="w")
            ttk.Button(card, text="Open ▸", style="Primary.TButton",
                       command=lambda pid=project.id, mid=module.id: app.show_project(pid, mid)
                       ).grid(row=0, column=1, rowspan=3, padx=8)


# --------------------------------------------------------------------------
# Lesson view (reading + scrolling list of exercises + quiz)
# --------------------------------------------------------------------------
def build_lesson_view(parent: tk.Misc, app, lesson_id: str, module_id: str) -> None:
    lesson = get_lesson(lesson_id)
    module = get_module(module_id)
    if lesson is None or module is None:
        ttk.Label(parent, text="Lesson not found.", style="H2.TLabel").pack(padx=20, pady=20)
        return

    paned = tk.PanedWindow(parent, orient="horizontal", bg=theme.BG, sashrelief="flat",
                           sashwidth=6, sashpad=0)
    paned.pack(fill="both", expand=True)

    # Left: reading
    left = ttk.Frame(paned, style="Content.TFrame", padding=16)
    paned.add(left, minsize=420, stretch="always")

    header = ttk.Frame(left, style="Content.TFrame")
    header.pack(fill="x")
    ttk.Button(header, text="← Back to module",
               command=lambda: app.show_module(module_id)).pack(side="left")
    ttk.Label(header, text=f"  {module.title}", style="Muted.TLabel").pack(side="left", padx=4)

    ttk.Label(left, text=lesson.title, style="H2.TLabel").pack(anchor="w", pady=(8, 8))

    body_frame = ttk.Frame(left, style="Content.TFrame")
    body_frame.pack(fill="both", expand=True)
    body_text = tk.Text(body_frame, wrap="word", borderwidth=0, highlightthickness=0,
                        bg=theme.BG, fg=theme.FG, font=theme.FONT_BODY,
                        padx=8, pady=8)
    body_scroll = ttk.Scrollbar(body_frame, command=body_text.yview)
    body_text.configure(yscrollcommand=body_scroll.set)
    body_text.pack(side="left", fill="both", expand=True)
    body_scroll.pack(side="right", fill="y")
    render_markdown(body_text, lesson.body)

    # Resources
    if lesson.resources:
        rframe = ttk.Frame(left, style="Content.TFrame")
        rframe.pack(fill="x", pady=(8, 4))
        ttk.Label(rframe, text="Field manual:", style="Muted.TLabel").pack(anchor="w")
        for r in lesson.resources:
            line = f"• {r.title} — {r.url}" + (f"  ({r.note})" if r.note else "")
            tk.Label(rframe, text=line, bg=theme.BG, fg=theme.ACCENT,
                     font=theme.FONT_SMALL, anchor="w", justify="left", wraplength=520
                     ).pack(anchor="w")

    # Right: exercises pane
    right_outer = ttk.Frame(paned, style="Content.TFrame")
    paned.add(right_outer, minsize=520, stretch="always")
    paned.paneconfig(right_outer, minsize=520)

    nb = ttk.Notebook(right_outer)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # one tab per exercise
    for i, ex in enumerate(lesson.exercises, 1):
        tab = ttk.Frame(nb, style="Content.TFrame")
        nb.add(tab, text=f"Ex {i}{'  ✓' if ex.id in app.progress.completed_exercises else ''}")
        _build_exercise_panel(tab, app, lesson, ex)

    # quiz tab
    if lesson.quiz:
        tab = ttk.Frame(nb, style="Content.TFrame")
        nb.add(tab, text="Quiz")
        _build_quiz_panel(tab, app, lesson)

    # mark-lesson-complete button
    bottom = ttk.Frame(right_outer, style="Content.TFrame", padding=8)
    bottom.pack(fill="x")
    ttk.Button(bottom, text="Mark lesson complete (+%d XP)" % lesson.xp_on_complete,
               style="Primary.TButton",
               command=lambda: _mark_lesson_complete(app, lesson)
               ).pack(side="right")


def _mark_lesson_complete(app, lesson) -> None:
    if lesson.id in app.progress.completed_lessons:
        app.toast.show("Already complete", "You've already crossed this one off.", color=theme.SUCCESS)
        return
    app.progress.completed_lessons.add(lesson.id)
    app.award_xp(lesson.xp_on_complete, f"Lesson complete: {lesson.title}")
    app.check_achievements()


# --------------------------------------------------------------------------
# Exercise panel
# --------------------------------------------------------------------------
def _build_exercise_panel(parent, app, lesson, exercise) -> None:
    parent.columnconfigure(0, weight=1)
    parent.rowconfigure(2, weight=1)

    # prompt
    ttk.Label(parent, text=exercise.title, style="H3.TLabel").grid(
        row=0, column=0, sticky="w", padx=8, pady=(8, 2))
    prompt = tk.Label(parent, text=exercise.prompt, bg=theme.BG, fg=theme.FG,
                      font=theme.FONT_BODY, anchor="w", justify="left", wraplength=720)
    prompt.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 4))

    # editor
    editor = CodeEditor(parent, height=14)
    editor.set_code(exercise.starter_code)
    editor.grid(row=2, column=0, sticky="nsew", padx=8, pady=4)

    # buttons
    btns = ttk.Frame(parent, style="Content.TFrame")
    btns.grid(row=3, column=0, sticky="ew", padx=8, pady=4)
    btn_run = ttk.Button(btns, text="▶ Run")
    btn_run.pack(side="left")
    btn_check = ttk.Button(btns, text="Check ✓", style="Primary.TButton")
    btn_check.pack(side="left", padx=6)
    btn_reset = ttk.Button(btns, text="Reset")
    btn_reset.pack(side="left")
    hint_state = {"index": 0}
    btn_hint = ttk.Button(btns, text="Hint")
    btn_hint.pack(side="left", padx=6)
    btn_ai = ttk.Button(btns, text="🛰 Ping Mission Control")
    btn_ai.pack(side="right")

    # output
    out_frame = ttk.Frame(parent, style="Content.TFrame")
    out_frame.grid(row=4, column=0, sticky="nsew", padx=8, pady=(4, 8))
    parent.rowconfigure(4, weight=1)
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

    # ---- run ---------------------------------------------------------
    def on_run():
        clear()
        append("Running...\n", "dim")
        code = editor.get_code()
        app.progress.bump("runs")

        def worker():
            res = run_code(code, stdin_text=exercise.stdin)
            def show():
                if res.stdout:
                    append(res.stdout)
                if res.stderr:
                    append(res.stderr, "err")
                    last_error["text"] = res.stderr
                else:
                    last_error["text"] = ""
                if res.timed_out:
                    append("\n⏱ Timed out (15s).\n", "warn")
                if not res.stdout and not res.stderr and not res.timed_out:
                    append("(no output)\n", "dim")
                progress_mod.save(app.progress)
                app.check_achievements()
            parent.after(0, show)

        threading.Thread(target=worker, daemon=True).start()

    btn_run.configure(command=on_run)

    # ---- check -------------------------------------------------------
    def on_check():
        clear()
        append("Checking against mission criteria...\n", "dim")
        code = editor.get_code()

        def worker():
            ok, results = grade(code, exercise.checks)
            def show():
                for r in results:
                    mark = "✓" if r.ok else "✗"
                    tag = "ok" if r.ok else "err"
                    append(f"{mark} {r.label}\n", tag)
                    if not r.ok and r.detail:
                        for line in r.detail.splitlines():
                            append("    " + line + "\n", "dim")
                if ok:
                    if exercise.id not in app.progress.completed_exercises:
                        app.progress.completed_exercises.add(exercise.id)
                        for k in exercise.counter_keys:
                            app.progress.bump(k)
                        app.award_xp(exercise.xp, f"Exercise: {exercise.title}")
                    else:
                        app.toast.show("Already passed", "You've already cleared this one.",
                                       color=theme.SUCCESS, duration_ms=2000)
                    append("\n🚀 PASS\n", "ok")
                    app.check_achievements()
                else:
                    append("\nNot quite — try again. Use Hint or Ping Mission Control.\n", "warn")
            parent.after(0, show)

        threading.Thread(target=worker, daemon=True).start()

    btn_check.configure(command=on_check)

    # ---- reset -------------------------------------------------------
    def on_reset():
        editor.set_code(exercise.starter_code)
        clear()
        append("Code reset to starter.\n", "dim")
        hint_state["index"] = 0

    btn_reset.configure(command=on_reset)

    # ---- hint --------------------------------------------------------
    def on_hint():
        if not exercise.hints:
            append("No hints available.\n", "dim")
            return
        i = hint_state["index"]
        if i >= len(exercise.hints):
            append("(no more hints)\n", "dim")
            return
        append(f"\nHint {i + 1}/{len(exercise.hints)}: {exercise.hints[i]}\n", "hint")
        hint_state["index"] = i + 1

    btn_hint.configure(command=on_hint)

    # ---- AI ----------------------------------------------------------
    def on_ai():
        api_key = app.progress.api_key
        if not ai_client.is_available(api_key):
            append(
                "\nAI helper not available. Set ANTHROPIC API key in Settings, "
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
            lesson_title=lesson.title,
            exercise_prompt=exercise.prompt,
            user_code=code,
            last_error=last_error["text"],
            on_chunk=on_chunk,
            on_done=on_done,
            on_error=on_error,
        )

    btn_ai.configure(command=on_ai)


# --------------------------------------------------------------------------
# Quiz panel
# --------------------------------------------------------------------------
def _build_quiz_panel(parent, app, lesson) -> None:
    parent.columnconfigure(0, weight=1)
    quiz = lesson.quiz
    ttk.Label(parent, text="Quick quiz", style="H3.TLabel").grid(
        row=0, column=0, sticky="w", padx=8, pady=(8, 4))

    state: dict[str, tk.IntVar] = {}
    for i, q in enumerate(quiz.questions):
        card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        card.grid(row=i + 1, column=0, sticky="ew", padx=8, pady=4)
        ttk.Label(card, text=f"Q{i + 1}. {q.prompt}", style="Card.TLabel",
                  wraplength=700, justify="left").pack(anchor="w")
        var = tk.IntVar(value=-1)
        state[f"q{i}"] = var
        for j, choice in enumerate(q.choices):
            tk.Radiobutton(card, text=choice, variable=var, value=j,
                           bg=theme.BG_PANEL, fg=theme.FG, selectcolor=theme.BG_INSET,
                           activebackground=theme.BG_PANEL, activeforeground=theme.FG,
                           font=theme.FONT_BODY, anchor="w", justify="left",
                           wraplength=620, pady=2).pack(anchor="w", padx=10)

    result_label = ttk.Label(parent, text="", style="H3.TLabel")
    result_label.grid(row=len(quiz.questions) + 2, column=0, sticky="w", padx=8, pady=8)

    def submit():
        correct = 0
        explanations = []
        for i, q in enumerate(quiz.questions):
            choice = state[f"q{i}"].get()
            if choice == q.correct_index:
                correct += 1
            else:
                explanations.append(f"Q{i + 1}: {q.explanation}")
        msg = f"You got {correct}/{len(quiz.questions)} correct."
        if explanations:
            msg += "\n\n" + "\n".join(explanations)
        result_label.configure(text=msg)
        if correct == len(quiz.questions):
            quiz_id = f"quiz:{lesson.id}"
            if quiz_id not in app.progress.completed_exercises:
                app.progress.completed_exercises.add(quiz_id)
                app.award_xp(quiz.xp_per_correct * correct, f"Quiz: {lesson.title}")
                app.check_achievements()

    ttk.Button(parent, text="Submit", style="Primary.TButton", command=submit
               ).grid(row=len(quiz.questions) + 3, column=0, sticky="w", padx=8, pady=8)


# --------------------------------------------------------------------------
# Project view
# --------------------------------------------------------------------------
def build_project_view(parent: tk.Misc, app, project_id: str, module_id: str) -> None:
    project = get_project(project_id)
    module = get_module(module_id)
    if project is None:
        ttk.Label(parent, text="Project not found.", style="H2.TLabel").pack(padx=20, pady=20)
        return

    paned = tk.PanedWindow(parent, orient="horizontal", bg=theme.BG, sashrelief="flat",
                           sashwidth=6, sashpad=0)
    paned.pack(fill="both", expand=True)

    # Left: brief
    left = ttk.Frame(paned, style="Content.TFrame", padding=16)
    paned.add(left, minsize=420, stretch="always")

    header = ttk.Frame(left, style="Content.TFrame")
    header.pack(fill="x")
    ttk.Button(header, text="← Back",
               command=lambda: app.show_module(module_id)).pack(side="left")

    done_mark = "✓ " if project.id in app.progress.completed_projects else "★ "
    ttk.Label(left, text=done_mark + project.title, style="H2.TLabel").pack(anchor="w", pady=(8, 4))
    ttk.Label(left, text=f"+{project.xp} XP", style="Muted.TLabel").pack(anchor="w")

    body_frame = ttk.Frame(left, style="Content.TFrame")
    body_frame.pack(fill="both", expand=True, pady=(8, 0))
    body_text = tk.Text(body_frame, wrap="word", bg=theme.BG, fg=theme.FG,
                        font=theme.FONT_BODY, borderwidth=0, highlightthickness=0,
                        padx=8, pady=8)
    body_scroll = ttk.Scrollbar(body_frame, command=body_text.yview)
    body_text.configure(yscrollcommand=body_scroll.set)
    body_text.pack(side="left", fill="both", expand=True)
    body_scroll.pack(side="right", fill="y")
    render_markdown(body_text, project.brief)

    if project.bonus_objectives:
        bframe = ttk.Frame(left, style="Content.TFrame")
        bframe.pack(fill="x", pady=(8, 0))
        ttk.Label(bframe, text="Bonus objectives:", style="Muted.TLabel").pack(anchor="w")
        for b in project.bonus_objectives:
            tk.Label(bframe, text=f"  · {b}", bg=theme.BG, fg=theme.GOLD,
                     font=theme.FONT_SMALL, anchor="w", justify="left",
                     wraplength=520).pack(anchor="w")

    if project.resources:
        rframe = ttk.Frame(left, style="Content.TFrame")
        rframe.pack(fill="x", pady=(8, 0))
        ttk.Label(rframe, text="Field manual:", style="Muted.TLabel").pack(anchor="w")
        for r in project.resources:
            line = f"• {r.title} — {r.url}"
            tk.Label(rframe, text=line, bg=theme.BG, fg=theme.ACCENT,
                     font=theme.FONT_SMALL, anchor="w", justify="left",
                     wraplength=520).pack(anchor="w")

    # Right: working area (reuse exercise panel pattern)
    right = ttk.Frame(paned, style="Content.TFrame", padding=10)
    paned.add(right, minsize=560, stretch="always")
    paned.paneconfig(right, minsize=560)

    # We treat a Project like a giant Exercise.
    from ._project_runner import build_project_workspace
    build_project_workspace(right, app, module_id, project)
