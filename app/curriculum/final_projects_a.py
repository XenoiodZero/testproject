"""Final projects A: Hohmann transfer, multi-stage rocket."""
from __future__ import annotations

from ..grader import StdoutContains, PredicateOnStdout
from ._types import Project, Resource


def _has_dv_total(stdout: str) -> tuple[bool, str]:
    """Check that the Hohmann project printed a total delta-v in 5500-6500 m/s range."""
    import re
    m = re.search(r"total\s*(?:delta[- ]?v|dv)\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", stdout, re.I)
    if not m:
        return False, "Expected a line like 'total delta-v: 5XXX m/s'."
    try:
        v = float(m.group(1))
    except ValueError:
        return False, "Couldn't read the delta-v number."
    if 5400 <= v <= 6700:
        return True, ""
    return False, f"Total delta-v should be ~5800-6000 m/s for an Earth->Mars Hohmann; got {v}."


HOHMANN = Project(
    id="fp_hohmann",
    title="Capstone 1 — Hohmann Transfer to Mars",
    summary="Compute the fuel-optimal two-burn transfer from Earth orbit to Mars orbit, by hand and in code.",
    brief="""# Mission brief — Hohmann to Mars

Your job: plan the most fuel-efficient ballistic transfer from Earth's orbit (around the Sun) to Mars's orbit (around the Sun).

**Background.** A Hohmann transfer is two burns:
1. From Earth's circular orbit, fire prograde to enter an elliptical orbit whose perihelion is Earth's orbit and aphelion is Mars's orbit.
2. When you arrive at Mars's orbit, fire prograde again to circularize.

The classic textbook problem in astrodynamics. Real missions (Mars Climate Orbiter, MAVEN, Perseverance) all use approximations of this, with corrections.

**Required output.**

```
Earth circular speed: ... m/s
Mars circular speed:  ... m/s
Transfer perihelion speed: ... m/s
Transfer aphelion speed:   ... m/s
Burn 1 (Earth departure): ... m/s
Burn 2 (Mars arrival):    ... m/s
total delta-v: ... m/s
Transfer half-period:     ... days
```

The total delta-v should land near **5800-6000 m/s**.

**Constants you'll need.**

```python
mu_sun  = 1.327e20      # m^3/s^2
r_earth = 1.496e11      # m  (1 AU)
r_mars  = 2.279e11      # m  (~1.524 AU)
```

**Math reminders.**

- Circular orbital speed at radius r around the Sun: v = sqrt(μ_sun / r).
- Semi-major axis of the transfer ellipse: a = (r_earth + r_mars) / 2.
- Speed at any point of an elliptical orbit (vis-viva equation): v = sqrt(μ_sun * (2/r - 1/a)).
- Burn 1 = v_perihelion (transfer) - v_circ(Earth).
- Burn 2 = v_circ(Mars) - v_aphelion (transfer).
- Half-period (one-way trip): π * sqrt(a³ / μ_sun) seconds.

**Bonus.** Plot the three orbits (Earth, Mars, transfer ellipse) on one figure with `matplotlib`. Save as `hohmann.png`.

**Why this matters.** Every interplanetary mission starts with a Hohmann (or near-Hohmann) baseline. NASA's "porkchop plots" — the 2D maps of departure date vs. arrival date with delta-v color-coded — are entirely built on top of this calculation.
""",
    starter_code='''"""Hohmann transfer to Mars."""
import math

mu_sun  = 1.327e20
r_earth = 1.496e11
r_mars  = 2.279e11

# 1. Circular speeds
v_earth = math.sqrt(mu_sun / r_earth)
v_mars  = math.sqrt(mu_sun / r_mars)

# 2. Transfer ellipse semi-major axis
a = (r_earth + r_mars) / 2

# 3. Transfer speeds at perihelion and aphelion (vis-viva)
v_peri = math.sqrt(mu_sun * (2 / r_earth - 1 / a))
v_apo  = math.sqrt(mu_sun * (2 / r_mars  - 1 / a))

# 4. Burns
burn1 = v_peri - v_earth
burn2 = v_mars - v_apo
total = burn1 + burn2

# 5. Trip time (half-period)
half_period_s = math.pi * math.sqrt(a**3 / mu_sun)
half_period_days = half_period_s / 86400

print(f"Earth circular speed: {v_earth:.0f} m/s")
print(f"Mars circular speed:  {v_mars:.0f} m/s")
print(f"Transfer perihelion speed: {v_peri:.0f} m/s")
print(f"Transfer aphelion speed:   {v_apo:.0f} m/s")
print(f"Burn 1 (Earth departure): {burn1:.0f} m/s")
print(f"Burn 2 (Mars arrival):    {burn2:.0f} m/s")
print(f"total delta-v: {total:.0f} m/s")
print(f"Transfer half-period:     {half_period_days:.0f} days")

# Bonus: uncomment to plot orbits.
# import numpy as np
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
#
# theta = np.linspace(0, 2*np.pi, 400)
# def ellipse(a, e):
#     b = a * math.sqrt(1 - e*e)
#     return a*np.cos(theta), b*np.sin(theta)
#
# # Earth & Mars are circular here
# fig, ax = plt.subplots(figsize=(7,7))
# ax.plot(r_earth*np.cos(theta), r_earth*np.sin(theta), label='Earth')
# ax.plot(r_mars *np.cos(theta), r_mars *np.sin(theta), label='Mars')
#
# # transfer: perihelion at +x = r_earth, aphelion at -x = -r_mars (shift origin to focus)
# e = (r_mars - r_earth) / (r_mars + r_earth)
# c = a * e   # focus offset
# bx, by = ellipse(a, e)
# ax.plot(bx - c, by, '--', label='Transfer')
# ax.plot([0],[0], 'y*', markersize=12)
# ax.set_aspect('equal'); ax.legend(); ax.set_title('Hohmann transfer Earth -> Mars')
# fig.savefig('hohmann.png'); print('saved: hohmann.png')
''',
    checks=[
        PredicateOnStdout(_has_dv_total, label="Total delta-v in expected range"),
        StdoutContains("Earth circular speed"),
        StdoutContains("Mars circular speed"),
        StdoutContains("Burn 1"),
        StdoutContains("Burn 2"),
    ],
    bonus_objectives=[
        "Plot all three orbits (Earth, Mars, transfer ellipse) and save as hohmann.png.",
        "Repeat the calculation for an Earth -> Venus transfer (r_venus = 1.082e11). What changes?",
        "Look up the actual delta-v of the Mars Climate Orbiter mission and compare.",
    ],
    hints=[
        "Read the lesson on orbital mechanics in module 15 again. Same formulas, just μ_sun instead of μ_earth.",
        "Vis-viva: v = sqrt(μ * (2/r − 1/a)). At perihelion r=r_earth; at aphelion r=r_mars.",
        "Burn magnitudes are *prograde*: positive numbers. Both burns add fuel cost.",
    ],
    resources=[
        Resource("NASA: Hohmann transfer overview", "https://www.jpl.nasa.gov/edu/learn/project/hohmann-transfer/"),
        Resource("Wikipedia: Hohmann transfer orbit", "https://en.wikipedia.org/wiki/Hohmann_transfer_orbit"),
        Resource("Vis-viva equation", "https://en.wikipedia.org/wiki/Vis-viva_equation"),
    ],
    xp=600,
)


def _check_rocket_orbit(stdout: str) -> tuple[bool, str]:
    if "total delta-v:" not in stdout.lower():
        return False, "Expected a 'total delta-v:' line summarizing all stages."
    if "stage 1" not in stdout.lower() or "stage 2" not in stdout.lower():
        return False, "Expected per-stage breakdown (Stage 1, Stage 2 ...)."
    return True, ""


MULTI_STAGE = Project(
    id="fp_rocket",
    title="Capstone 2 — Multi-Stage Rocket Simulator",
    summary="Model a 3-stage launcher (Saturn V-ish), compute total delta-v, and check whether it gets to LEO.",
    brief="""# Mission brief — multi-stage launcher

Build a 3-stage rocket simulator. For each stage you'll know the wet mass, dry mass, and Isp. Compute:
1. Each stage's contribution to delta-v.
2. The cumulative delta-v after each stage.
3. Whether the total delta-v exceeds **9400 m/s** (the rough threshold to reach low Earth orbit, including gravity & drag losses).

**Required output (something like):**

```
Stage 1: m0=2300t, mf=300t, Isp=263s -> dv=5246 m/s | cumulative=5246 m/s
Stage 2: m0=480t, mf=40t, Isp=421s   -> dv=10260 m/s | cumulative=15506 m/s
Stage 3: m0=120t, mf=15t, Isp=421s   -> dv=8579 m/s  | cumulative=24085 m/s
total delta-v: 24085 m/s
LEO threshold (9400 m/s): EXCEEDED
```

Wire it as a function `simulate(stages)` that takes a list of dicts and returns the per-stage and cumulative numbers.

**Bonus.** The "rocket equation" assumes you keep all the dropped stages with you. In reality, when stage 1 burns out you separate, so stage 2 carries only m0_stage2 (which already includes stages 3+ and payload). Make sure your stages account for "everything still attached."

**Bigger bonus.** Plot velocity vs. time, integrating with thrust and drag. (Skip atmosphere if you want — focus on Δv.)
""",
    starter_code='''"""Multi-stage rocket Δv calculator."""
import math

g0 = 9.81

def stage_dv(m0, mf, isp):
    """Tsiolkovsky rocket equation. Returns delta-v in m/s."""
    return isp * g0 * math.log(m0 / mf)


# Saturn V-ish (rough numbers in tonnes; mass ratios are what matter)
stages = [
    {"name": "Stage 1 (S-IC)", "m0": 2300, "mf": 300, "isp": 263},
    {"name": "Stage 2 (S-II)", "m0": 480,  "mf": 40,  "isp": 421},
    {"name": "Stage 3 (S-IVB)","m0": 120,  "mf": 15,  "isp": 421},
]

cumulative = 0
for s in stages:
    dv = stage_dv(s["m0"], s["mf"], s["isp"])
    cumulative += dv
    print(f"{s['name']}: m0={s['m0']}t, mf={s['mf']}t, Isp={s['isp']}s -> dv={dv:.0f} m/s | cumulative={cumulative:.0f} m/s")

print(f"total delta-v: {cumulative:.0f} m/s")
print(f"LEO threshold (9400 m/s): {'EXCEEDED' if cumulative >= 9400 else 'NOT REACHED'}")
''',
    checks=[
        PredicateOnStdout(_check_rocket_orbit, label="Per-stage and total Δv printed"),
        StdoutContains("LEO threshold"),
    ],
    bonus_objectives=[
        "Add a 4th stage and re-run.",
        "Try replacing each stage's Isp with a Hall-effect thruster (Isp=1500). What happens to delta-v? What happens to *time*?",
        "Plot cumulative delta-v as a bar chart, save as `rocket_dv.png`.",
    ],
    hints=[
        "Module 16 has the formula. dv = Isp * g0 * ln(m0/mf).",
        "Don't forget: each subsequent stage's m0 already includes the upper stages — that's why staging works.",
        "Use a for loop accumulating into `cumulative`.",
    ],
    resources=[
        Resource("Saturn V tech reference", "https://history.nasa.gov/saturnv.html"),
        Resource("Falcon 9 user guide (real numbers)", "https://www.spacex.com/media/falcon-users-guide-2021-09.pdf"),
    ],
    xp=700,
)
