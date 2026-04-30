"""Module 2: Mission Variables — names that hold values."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, CallFn
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M02 = Module(
    id="m02_variables",
    title="Module 2 — Mission Variables",
    tagline="Give your data a name. Use it later.",
    phase="Boot Camp",
    lessons=[
        Lesson(
            id="m02_l1",
            title="Lesson 2.1 — Variables and types",
            body="""# Variables: labels for stuff

A **variable** is a name you stick on a piece of data so you can refer to it later.

```python
spacecraft = "Orion"
crew_size = 4
fuel_pct = 87.5
launched = True
```

Read those out loud as: *"set spacecraft to 'Orion', set crew_size to 4..."*. The `=` is **assignment** — it points the name on the left at the value on the right. It is **not** a math equals sign.

## Four primitive types you'll use constantly

| Type    | Example          | What it is             |
|---------|------------------|------------------------|
| `str`   | `"Orion"`        | a string of characters |
| `int`   | `4`              | a whole number         |
| `float` | `87.5`           | a number with decimals |
| `bool`  | `True` / `False` | yes/no                 |

`type(x)` tells you what something is. Try `print(type(crew_size))` — Python will say `<class 'int'>`.

## Naming rules (and good habits)

- Use `lowercase_with_underscores` (this is called *snake_case*). Real aerospace teams do.
- Names can't start with a digit. `2nd_stage` is illegal; `stage_2` is fine.
- Don't reuse Python's reserved words like `print`, `for`, `if`, `True`, `class`.
- A good variable name reads like English: `delta_v`, not `dv` or `x`.

## Reassignment

Variables can be reassigned. The old value is just thrown away.

```python
fuel_pct = 87.5
fuel_pct = 86.9   # one second of burn later
```

## f-strings: print with variables

The cleanest way to print a sentence containing variables:

```python
spacecraft = "Orion"
crew_size = 4
print(f"{spacecraft} is carrying {crew_size} crew.")
# -> Orion is carrying 4 crew.
```

The `f` before the quotes makes it a **formatted string**. Anything inside `{ ... }` is evaluated as Python.
""",
            exercises=[
                Exercise(
                    id="m02_l1_e1",
                    title="Set up the manifest",
                    prompt=(
                        "Create three variables:\n"
                        "  mission_name = \"Artemis I\"\n"
                        "  crew = 0\n"
                        "  fuel_tons = 730.5\n"
                        "Then print exactly: Artemis I, crew=0, fuel=730.5t"
                    ),
                    starter_code='mission_name = ""\ncrew = 0\nfuel_tons = 0.0\n# print using an f-string\n',
                    checks=[StdoutEquals("Artemis I, crew=0, fuel=730.5t")],
                    hints=[
                        "Use an f-string: f\"... {mission_name} ... {crew} ... {fuel_tons}t\"",
                        "Don't forget the literal 't' at the end.",
                        "Solution body: print(f\"{mission_name}, crew={crew}, fuel={fuel_tons}t\")",
                    ],
                    xp=25,
                ),
                Exercise(
                    id="m02_l1_e2",
                    title="What type is it?",
                    prompt="Set altitude_km = 408 (the ISS orbit altitude). Then print the type of altitude_km.",
                    starter_code="altitude_km = 0\n# print(type(altitude_km))\n",
                    checks=[StdoutContains("int")],
                    hints=[
                        "type(x) returns a type object. print() it directly.",
                        "Output will look like <class 'int'>.",
                    ],
                    xp=15,
                ),
                Exercise(
                    id="m02_l1_e3",
                    title="Reassignment",
                    prompt=(
                        "Start with fuel_pct = 100. Then set fuel_pct = 87.\n"
                        "Print: fuel: 87"
                    ),
                    starter_code="fuel_pct = 100\n",
                    checks=[StdoutEquals("fuel: 87")],
                    hints=[
                        "Assigning a new value to a variable replaces the old.",
                        "f-string: print(f\"fuel: {fuel_pct}\")",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m02_l1_e4",
                    title="Booleans",
                    prompt=(
                        "Set hatch_closed = True and oxygen_ok = True.\n"
                        "Set ready = hatch_closed and oxygen_ok (this is a real boolean expression).\n"
                        "Print: ready=True"
                    ),
                    starter_code="hatch_closed = False\noxygen_ok = False\n",
                    checks=[StdoutEquals("ready=True")],
                    hints=[
                        "`and` returns True only if both sides are True.",
                        "Print with: print(f\"ready={ready}\")",
                    ],
                    xp=20,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "Which is the right way to assign 9.81 to a variable named 'g'?",
                    ["g == 9.81", "g := 9.81", "g = 9.81", "let g = 9.81"],
                    2,
                    "Single = is assignment in Python.",
                ),
                QuizQuestion(
                    "Which name is NOT a legal Python variable name?",
                    ["delta_v", "stage_2", "2nd_stage", "fuel_pct"],
                    2,
                    "Names can't start with a digit.",
                ),
                QuizQuestion(
                    "What does this print?\n\n  x = 5\n  x = 7\n  print(x)",
                    ["5", "7", "5 7", "Error"],
                    1,
                    "Reassignment overwrites. Final value of x is 7.",
                ),
                QuizQuestion(
                    "Inside an f-string, what do {curly braces} do?",
                    ["Comments", "Evaluate Python and insert the result", "Math", "Nothing"],
                    1,
                    "f-strings interpolate the value inside braces.",
                ),
            ]),
            resources=[
                Resource("Python docs: f-strings", "https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals"),
                Resource("PEP 8 naming conventions", "https://peps.python.org/pep-0008/#naming-conventions"),
            ],
            xp_on_complete=50,
        ),
    ],
)
