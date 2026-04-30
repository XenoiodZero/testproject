"""Module 5: Decision Systems — booleans and if/elif/else."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, StdinStdout
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M05 = Module(
    id="m05_conditionals",
    title="Module 5 — Decision Systems",
    tagline="If A, do B. Else, scrub the launch.",
    phase="Boot Camp",
    lessons=[
        Lesson(
            id="m05_l1",
            title="Lesson 5.1 — Booleans, comparisons, if/elif/else",
            body="""# Decisions

A spacecraft asks "is it safe to launch?" 10,000 times a second. In code, that's an `if` statement.

## Comparisons

These all return `True` or `False`:

```python
5 == 5      # True   (== is equality, NOT =)
5 != 4      # True   (not equal)
5 > 4       # True
5 >= 5      # True
"abc" == "abc"  # True
```

The single `=` is **assignment**. The double `==` is **comparison**. Mixing them up is one of the most common bugs in any language.

## Logical operators

```python
True and True     # True
True and False    # False
True or False     # True
not True          # False
```

Plain English. `and` requires both, `or` requires at least one, `not` flips it.

## if / elif / else

```python
fuel_pct = 35

if fuel_pct < 5:
    print("CRITICAL: scrub launch")
elif fuel_pct < 20:
    print("WARN: low fuel")
else:
    print("Fuel nominal")
```

A few rules that catch beginners:

1. The colon `:` at the end of `if`, `elif`, `else` is **mandatory**.
2. The lines underneath must be **indented** — Python uses indentation to group code (most languages use `{ }` braces; Python uses whitespace). Standard is 4 spaces.
3. `elif` is short for "else if". You can have zero, one, or many. `else` is optional.

## A real launch checklist

```python
fueled = True
hatch_closed = True
weather_ok = False

if fueled and hatch_closed and weather_ok:
    print("GO for launch")
else:
    print("HOLD")
```

Reads like English.
""",
            exercises=[
                Exercise(
                    id="m05_l1_e1",
                    title="Launch readiness check",
                    prompt=(
                        "Set fuel_pct = 92, hatch_closed = True, weather_ok = True.\n"
                        "If fuel_pct >= 90 AND hatch_closed AND weather_ok, print 'GO'.\n"
                        "Otherwise print 'HOLD'."
                    ),
                    starter_code="fuel_pct = 92\nhatch_closed = True\nweather_ok = True\n",
                    checks=[StdoutEquals("GO")],
                    hints=[
                        "Use one if + one else.",
                        "Combine with `and`.",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m05_l1_e2",
                    title="Tiered alert",
                    prompt=(
                        "Read fuel level via input() (it'll be a string — convert to int).\n"
                        "If <5: print 'CRITICAL'\n"
                        "Elif <20: print 'WARN'\n"
                        "Else: print 'OK'"
                    ),
                    starter_code="fuel = int(input())\n",
                    checks=[
                        StdinStdout("3\n", "CRITICAL"),
                        StdinStdout("15\n", "WARN"),
                        StdinStdout("80\n", "OK"),
                    ],
                    hints=[
                        "Order matters: check the most extreme case first.",
                        "Use elif, not three separate ifs.",
                    ],
                    xp=30,
                    counter_keys=["loop_exercises"],
                ),
                Exercise(
                    id="m05_l1_e3",
                    title="Altitude category",
                    prompt=(
                        "Given altitude_km (set it to 408), print:\n"
                        "  'suborbital' if altitude_km < 100\n"
                        "  'LEO' if 100 <= altitude_km < 2000\n"
                        "  'MEO' if 2000 <= altitude_km < 35786\n"
                        "  'GEO+' otherwise\n"
                        "(LEO = Low Earth Orbit. The ISS sits at about 408 km, so you should print 'LEO'.)"
                    ),
                    starter_code="altitude_km = 408\n",
                    checks=[StdoutEquals("LEO")],
                    hints=[
                        "Python lets you chain comparisons: 100 <= altitude_km < 2000 is legal.",
                        "Three elifs and an else.",
                    ],
                    xp=25,
                ),
                Exercise(
                    id="m05_l1_e4",
                    title="not, and, or",
                    prompt=(
                        "Given engine_on = True and abort_pressed = False, print 'FIRING' if "
                        "engine_on AND NOT abort_pressed, else print 'SAFE'."
                    ),
                    starter_code="engine_on = True\nabort_pressed = False\n",
                    checks=[StdoutEquals("FIRING")],
                    hints=[
                        "if engine_on and not abort_pressed:",
                    ],
                    xp=20,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What's the difference between = and ==?",
                    ["No difference", "= compares, == assigns", "= assigns, == compares", "Both compare"],
                    2,
                    "= sets a variable. == checks equality.",
                ),
                QuizQuestion(
                    "What does Python use to group the body of an if statement?",
                    ["Curly braces { }", "Indentation", "Parentheses ( )", "The 'end' keyword"],
                    1,
                    "Indentation. Standard is 4 spaces.",
                ),
                QuizQuestion(
                    "What does (True and False) or True evaluate to?",
                    ["True", "False", "Error", "None"],
                    0,
                    "(True and False) is False. False or True is True.",
                ),
                QuizQuestion(
                    "Which line is correctly written?",
                    ["if x > 5", "if (x > 5):", "if x > 5:", "if {x > 5}:"],
                    2,
                    "Parentheses are optional in Python. The colon is required.",
                ),
            ]),
            resources=[
                Resource("Python docs: control flow", "https://docs.python.org/3/tutorial/controlflow.html"),
            ],
            xp_on_complete=60,
        ),
    ],
)
