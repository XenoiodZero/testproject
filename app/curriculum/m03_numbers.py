"""Module 3: Trajectory Math — numbers and the math module."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, CallFn
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M03 = Module(
    id="m03_numbers",
    title="Module 3 — Trajectory Math",
    tagline="Arithmetic, and your first whiff of orbital math.",
    phase="Boot Camp",
    lessons=[
        Lesson(
            id="m03_l1",
            title="Lesson 3.1 — Operators",
            body="""# Operators

Python is a fancy calculator. The basics:

```python
2 + 3       # 5     addition
10 - 4      # 6     subtraction
6 * 7       # 42    multiplication
20 / 4      # 5.0   division (always returns a float)
20 // 6     # 3     integer division (drops the remainder)
20 % 6      # 2     modulo (the remainder)
2 ** 10     # 1024  exponent (2 to the 10th)
```

`/` always gives you a float, even when the answer is whole. `//` gives you an int when both sides are ints.

## Order of operations

Same as math class: parentheses, exponents, multiply/divide, add/subtract.

```python
3 + 4 * 2       # 11   not 14
(3 + 4) * 2     # 14
```

When in doubt, add parentheses. Aerospace code is full of them — clarity > cleverness.

## The `math` module

Python ships with `math`, a library of physics-friendly tools. To use it, **import** it:

```python
import math

math.pi          # 3.141592653589793
math.sqrt(625)   # 25.0
math.sin(0)      # 0.0
math.cos(math.pi)  # -1.0
math.radians(180)  # 3.14159...  (degrees -> radians)
math.degrees(math.pi)  # 180.0
```

`math.sin` and `math.cos` use **radians**, not degrees — that trips up everyone once. Convert with `math.radians(...)`.

## Real-world: gravity at the surface of Earth

The acceleration due to gravity at Earth's surface is roughly **9.81 m/s²**. If you drop something for `t` seconds (and ignore air drag), it falls `0.5 * 9.81 * t**2` meters. You can compute that in Python directly. Try it.
""",
            exercises=[
                Exercise(
                    id="m03_l1_e1",
                    title="How far does it fall?",
                    prompt=(
                        "Compute the distance an object falls in 5 seconds at Earth gravity.\n"
                        "Formula: distance = 0.5 * 9.81 * t**2\n"
                        "Print exactly: 122.625"
                    ),
                    starter_code="t = 5\n# compute distance, then print(distance)\n",
                    checks=[StdoutEquals("122.625")],
                    hints=[
                        "Use 0.5 * 9.81 * t ** 2.",
                        "Just print(distance) — no formatting needed.",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m03_l1_e2",
                    title="Modulo: orbits per day",
                    prompt=(
                        "The ISS orbits Earth roughly every 92 minutes. There are 1440 minutes in a day.\n"
                        "Use integer division to compute how many full orbits per day, then modulo to compute leftover minutes.\n"
                        "Print exactly: 15 orbits, 60 leftover"
                    ),
                    starter_code="period = 92\nday = 1440\n",
                    checks=[StdoutEquals("15 orbits, 60 leftover")],
                    hints=[
                        "Use day // period for orbits, day % period for leftover.",
                        "f-string: print(f\"{orbits} orbits, {leftover} leftover\")",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=25,
                ),
                Exercise(
                    id="m03_l1_e3",
                    title="Use the math module",
                    prompt=(
                        "Import math. Print the value of math.sqrt(2 * 9.81 * 100).\n"
                        "(That's the speed in m/s an object hits after falling 100m — neat, right?)"
                    ),
                    starter_code="import math\n",
                    checks=[StdoutContains("44.29")],
                    hints=[
                        "print(math.sqrt(2 * 9.81 * 100))",
                        "It will print a long float; the check just looks for the leading 44.29.",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m03_l1_e4",
                    title="Degrees to radians",
                    prompt=(
                        "An antenna is pointed 45 degrees up. Convert that to radians and print it.\n"
                        "Use math.radians(45)."
                    ),
                    starter_code="import math\n",
                    checks=[StdoutContains("0.7853")],
                    hints=[
                        "print(math.radians(45)) — should print about 0.7853981...",
                    ],
                    xp=15,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does 7 // 2 evaluate to?",
                    ["3.5", "3", "4", "Error"],
                    1,
                    "// is integer division: drops the remainder. 7 // 2 = 3.",
                ),
                QuizQuestion(
                    "What does 2 ** 8 evaluate to?",
                    ["10", "16", "256", "64"],
                    2,
                    "** is exponentiation. 2 to the 8th = 256.",
                ),
                QuizQuestion(
                    "math.sin(...) expects its argument in:",
                    ["Degrees", "Radians", "Either, auto-detected", "Hours"],
                    1,
                    "All Python trig is in radians. Convert with math.radians(deg).",
                ),
                QuizQuestion(
                    "What does 17 % 5 evaluate to?",
                    ["3", "2", "3.4", "12"],
                    1,
                    "% is the remainder. 17 = 3*5 + 2, so 17 % 5 = 2.",
                ),
            ]),
            resources=[
                Resource("Python docs: math module", "https://docs.python.org/3/library/math.html"),
                Resource("NASA: Earth fact sheet (gravity, radius, etc.)", "https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html"),
            ],
            xp_on_complete=50,
        ),
    ],
)
