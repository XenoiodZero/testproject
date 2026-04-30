"""Module 15: Orbital Mechanics 101 — gravity, two-body, Kepler."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M15 = Module(
    id="m15_orbits",
    title="Module 15 — Orbital Mechanics 101",
    tagline="Why things fall sideways. Newton, Kepler, and circular orbits.",
    phase="Mission Specialist",
    lessons=[
        Lesson(
            id="m15_l1",
            title="Lesson 15.1 — Theory: Newton, gravity, escape, circular orbits",
            body="""# Why orbits work

A satellite isn't *resisting* gravity — it's **falling, but moving sideways fast enough that the Earth's surface curves away as fast as it falls**. That's it. That's an orbit.

## Newton's law of universal gravitation

Two masses M and m, distance r apart, attract each other with a force:

    F = G * M * m / r^2

`G` is the gravitational constant, **6.674e-11** N·m²/kg². For most spacecraft work we don't care about G directly; we care about **GM**, sometimes written **μ** ("mu"). For Earth:

    μ_earth = 3.986e14  m^3 / s^2

That's a magic number you'll see in every orbital-mechanics formula.

## Speed needed for a circular orbit

If you balance gravity (pulling you down) against centripetal acceleration (your sideways motion needing a turning force), you get:

    v_circ = sqrt(μ / r)

where `r` is **distance from the center of the Earth**, not altitude above the surface. Earth's radius is **6378 km**, so a satellite at 408 km altitude has `r = 6786 km = 6.786e6 m`, and:

    v = sqrt(3.986e14 / 6.786e6) ≈ 7660 m/s

The ISS orbits at about 7.66 km/s. (Roughly 17,000 mph. Nuts.)

## Escape velocity

The minimum speed to *never come back* (from radius r, ignoring atmosphere):

    v_escape = sqrt(2 * μ / r)

From Earth's surface: about 11.2 km/s.

## Orbital period (Kepler's third law)

For a circular orbit:

    T = 2*pi*sqrt(r^3 / μ)

For the ISS: about 5560 seconds = ~92.7 minutes. Real ISS: ~92.7 minutes. Math works.

## Useful constants (memorize these)

| Symbol  | Value                       | What                                |
|---------|-----------------------------|-------------------------------------|
| G       | 6.674e-11 N·m²/kg²          | Newton's gravitational constant     |
| μ_earth | 3.986e14 m³/s²              | GM for Earth                        |
| R_earth | 6.378e6 m (6378 km)         | Earth's radius                      |
| g       | 9.81 m/s²                   | surface gravity                     |
| AU      | 1.496e11 m                  | Earth-Sun distance (Astronomical Unit) |
| μ_sun   | 1.327e20 m³/s²              | GM for the Sun                      |

## Why the Sun? Because next module we go interplanetary.

In the next module we'll use exactly these formulas to plan a real Hohmann transfer to Mars.
""",
            exercises=[
                Exercise(
                    id="m15_l1_e1",
                    title="ISS orbital speed",
                    prompt=(
                        "Compute the circular-orbit speed (m/s) for an altitude of 408 km above Earth.\n"
                        "Use mu = 3.986e14, R_earth = 6378e3.\n"
                        "Formula: v = sqrt(mu / (R_earth + alt_m)).\n"
                        "Print v formatted to 1 decimal place, like:  v = 7669.5 m/s\n"
                        "(Yours might be 7669.X — anywhere in 7600-7700 is fine for the check.)"
                    ),
                    starter_code=(
                        "import math\n"
                        "mu = 3.986e14\n"
                        "R = 6378e3\n"
                        "alt = 408e3\n"
                    ),
                    checks=[StdoutContains("76")],
                    hints=[
                        "v = math.sqrt(mu / (R + alt))",
                        "print(f'v = {v:.1f} m/s')",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=35,
                ),
                Exercise(
                    id="m15_l1_e2",
                    title="Escape velocity from Earth's surface",
                    prompt=(
                        "Compute escape velocity from Earth's surface in m/s, formatted with 0 decimals.\n"
                        "Print: v_escape = 11186 m/s   (your number may be 11186 or 11185 — both pass)"
                    ),
                    starter_code="import math\nmu = 3.986e14\nR = 6378e3\n",
                    checks=[StdoutContains("v_escape = 1118")],
                    hints=[
                        "v = math.sqrt(2*mu/R)",
                        "print(f'v_escape = {v:.0f} m/s')",
                    ],
                    xp=30,
                ),
                Exercise(
                    id="m15_l1_e3",
                    title="ISS orbital period",
                    prompt=(
                        "Compute the orbital period in minutes for the ISS at 408 km altitude.\n"
                        "T_seconds = 2*pi*sqrt(r^3/mu), then divide by 60.\n"
                        "Print exactly:  T = 92.7 min\n"
                        "(Round to one decimal — 92.6 or 92.8 would also pass the substring check.)"
                    ),
                    starter_code="import math\nmu = 3.986e14\nR = 6378e3\nalt = 408e3\n",
                    checks=[StdoutContains("T = 92.")],
                    hints=[
                        "r = R + alt",
                        "T = 2*math.pi*math.sqrt(r**3/mu) / 60",
                        "print(f'T = {T:.1f} min')",
                    ],
                    xp=35,
                ),
                Exercise(
                    id="m15_l1_e4",
                    title="Geostationary radius",
                    prompt=(
                        "A geostationary satellite must orbit with a period of exactly 1 sidereal day "
                        "(86164 seconds) so it stays over a fixed point on Earth.\n"
                        "Use Kepler's third law backwards to find r: r = (mu * T^2 / (4*pi^2)) ** (1/3).\n"
                        "Print r in km to 0 decimals. Real answer is about 42164 km."
                    ),
                    starter_code="import math\nmu = 3.986e14\nT = 86164\n",
                    checks=[StdoutContains("4216")],
                    hints=[
                        "r_m = (mu * T**2 / (4*math.pi**2)) ** (1/3)",
                        "print(f'{r_m/1000:.0f} km')",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=40,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What is mu (gravitational parameter)?",
                    ["The mass of Earth", "G * M for a body", "Pi", "Escape velocity"],
                    1,
                ),
                QuizQuestion(
                    "At higher altitudes, circular orbital speed is:",
                    ["Higher", "Lower", "Same", "Always 7.8 km/s"],
                    1,
                    "v = sqrt(mu/r). Larger r -> smaller v.",
                ),
                QuizQuestion(
                    "Which of these is the right escape velocity formula?",
                    ["sqrt(mu/r)", "sqrt(2*mu/r)", "mu/r", "2*pi*r"],
                    1,
                ),
            ]),
            resources=[
                Resource("Curtis: Orbital Mechanics for Engineering Students", "https://www.elsevier.com/books/orbital-mechanics-for-engineering-students/curtis/978-0-08-102133-0", "The standard textbook."),
                Resource("NASA — basics of spaceflight", "https://solarsystem.nasa.gov/basics/"),
                Resource("Vallado: Fundamentals of Astrodynamics (advanced)", "https://www.smad.com/", ""),
            ],
            xp_on_complete=100,
        ),
    ],
)
