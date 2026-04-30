# Mission: Python — Learn Python the Aerospace Way

A Windows-first desktop app that teaches you Python from absolute zero, all the way to writing real aerospace simulations: orbital mechanics, the rocket equation, multi-stage launchers, ISS tracking, and a Mars lander.

Gamer-flavored: XP, levels (Cadet → Mission Director), achievements / mission patches, streaks, boss-fight final projects.

Optional AI helper: every exercise has hand-written progressive hints. If you drop in an Anthropic API key, a "Ping Mission Control" button asks Claude for help on whatever you're stuck on.

---

## Quick start

```bash
# 1. Install Python 3.10+ from python.org (check "Add to PATH")
# 2. Open PowerShell or cmd in this folder
pip install -r requirements.txt
python run.py
```

That's it. Everything is local — your progress saves to `%USERPROFILE%\.mission_python\save.json`.

## Optional: turn on the AI helper

1. Get an API key from https://console.anthropic.com/
2. Open the app → Settings (bottom-left) → paste key → Save
3. Inside any exercise, click **Ping Mission Control** when stuck

The key is stored locally in your save file. No key ever leaves your machine except to Anthropic when you click the button.

## Optional: build a single-file .exe

```bash
pip install pyinstaller
python build_exe.py
```

Produces `dist/MissionPython.exe`. Distribute that file alone (~30–60 MB) — recipients don't need Python installed.

---

## What you'll learn

**Phase 1 — Boot Camp (modules 1–6):** print, variables, numbers, strings, if/else, loops.
**Phase 2 — Flight School (modules 7–12):** functions, lists, dicts, files, classes, error recovery.
**Phase 3 — Mission Specialist (modules 13–18):** NumPy, Matplotlib, orbital mechanics, the Tsiolkovsky rocket equation, telemetry parsing, Mars-lander simulation.
**Phase 4 — Capstone Missions:** five long final projects, each a "boss fight":

1. **Hohmann Transfer Calculator** — plan a fuel-optimal trip from Earth to Mars.
2. **Multi-Stage Rocket Simulator** — model a Saturn V-ish launcher with stage separation.
3. **ISS Live Tracker** — pull real position data from the Open Notify API and plot the ground track.
4. **Mission Control Dashboard** — a Tkinter app of your own, with live telemetry plots.
5. **Two-Body Orbital Propagator** — numerically integrate Newton's laws and watch a satellite orbit.

Every module has reading, runnable examples, graded exercises, a quiz, and a "field manual" link to deeper resources (real NASA / ESA / JPL pages).

## Architecture

```
app/
  main.py            — entry point
  theme.py           — space-cadet color/font theme
  progress.py        — XP, levels, save/load
  achievements.py    — mission patches and unlock logic
  runner.py          — runs your code in a sandboxed subprocess, captures stdout/err
  grader.py          — checks exercise solutions
  ai_client.py       — optional Claude API client
  ui_main.py         — main window + nav
  ui_dashboard.py    — Mission Control home screen
  ui_lesson.py       — reading + exercise + project view
  ui_panels.py       — achievements, settings, AI panel
  curriculum/        — all lessons, exercises, projects (pure data)
```

The curriculum is plain Python data — easy to extend. Add a module: drop a new file in `app/curriculum/`, register it in `modules.py`, done.

## Acknowledgements / further reading

This curriculum points you to the real, primary sources as you progress:

- NASA's general public site: https://www.nasa.gov/
- JPL Horizons (real ephemeris data): https://ssd.jpl.nasa.gov/horizons/
- ESA: https://www.esa.int/
- Open Notify ISS API: http://open-notify.org/
- Curtis, *Orbital Mechanics for Engineering Students* (textbook reference, Module 15)
- *Python for Astronomers* and *AstroPy*: https://www.astropy.org/

## License

MIT. Have fun. Build rockets.
