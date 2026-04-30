"""Module 7: Mission Functions — def, parameters, return, scope."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, CallFn
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M07 = Module(
    id="m07_functions",
    title="Module 7 — Mission Functions",
    tagline="Package logic. Reuse it. Stage separation, in code.",
    phase="Flight School",
    lessons=[
        Lesson(
            id="m07_l1",
            title="Lesson 7.1 — def, parameters, return",
            body="""# Functions

A function is a named, reusable chunk of code. You define it once and call it as many times as you want.

```python
def greet(name):
    print(f"Welcome, {name}.")

greet("Buzz")     # Welcome, Buzz.
greet("Sally")    # Welcome, Sally.
```

The breakdown:
- `def` introduces a function definition.
- `greet` is the function's name.
- `(name)` is the **parameter** — a placeholder variable that takes whatever value the caller passes in.
- The indented block is the function **body**.
- `greet("Buzz")` is a **call** — it actually runs the function.

## return

`print` shows something. `return` *gives a value back* to the caller.

```python
def square(x):
    return x * x

result = square(4)     # result is now 16
print(result)
```

Without `return`, a function returns `None` (Python's word for "nothing").

A function can take multiple parameters:

```python
def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity ** 2

print(kinetic_energy(1000, 7700))    # 2.96e10 joules
```

## Default parameters

```python
def greet(name, greeting="Welcome"):
    print(f"{greeting}, {name}.")

greet("Buzz")                     # Welcome, Buzz.
greet("Buzz", "Howdy")            # Howdy, Buzz.
greet("Buzz", greeting="Hi")      # Hi, Buzz. (keyword argument)
```

## Why this matters

Once you have functions, your programs stop being a wall of code and start looking like English: `if launch_safe(weather, fuel, hatch): start_countdown()`. Aerospace code is enormous; functions are how it stays understandable.

## Docstrings

A string on the first line of a function body is its **docstring**. It's the docs.

```python
def kinetic_energy(mass, velocity):
    \"\"\"Return kinetic energy in joules. mass in kg, velocity in m/s.\"\"\"
    return 0.5 * mass * velocity ** 2
```
""",
            exercises=[
                Exercise(
                    id="m07_l1_e1",
                    title="Define `square`",
                    prompt=(
                        "Write a function `square(x)` that returns x * x.\n"
                        "Then print square(7)."
                    ),
                    starter_code="def square(x):\n    pass\n\nprint(square(7))\n",
                    checks=[StdoutEquals("49"), CallFn("square(9)", "81")],
                    hints=[
                        "Replace `pass` with `return x * x`.",
                        "Call square(7) and print the result.",
                    ],
                    counter_keys=["functions_written"],
                    xp=25,
                ),
                Exercise(
                    id="m07_l1_e2",
                    title="Kinetic energy",
                    prompt=(
                        "Write a function kinetic_energy(mass, velocity) that returns 0.5 * mass * velocity**2.\n"
                        "Print the result for mass=1000 kg, velocity=7700 m/s.\n"
                        "Expected output: 29645000000.0"
                    ),
                    starter_code="def kinetic_energy(mass, velocity):\n    pass\n\nprint(kinetic_energy(1000, 7700))\n",
                    checks=[StdoutEquals("29645000000.0")],
                    hints=[
                        "return 0.5 * mass * velocity ** 2",
                    ],
                    counter_keys=["functions_written"],
                    xp=30,
                ),
                Exercise(
                    id="m07_l1_e3",
                    title="Default parameter: gravity",
                    prompt=(
                        "Write weight(mass, g=9.81) that returns mass * g.\n"
                        "Print weight(70) (Earth) and weight(70, 3.71) (Mars)."
                    ),
                    starter_code="def weight(mass, g=9.81):\n    pass\n",
                    checks=[StdoutContains("686.7"), StdoutContains("259.7")],
                    hints=[
                        "Two print() calls after the def.",
                        "Default value goes in the def signature.",
                    ],
                    counter_keys=["functions_written"],
                    xp=25,
                ),
                Exercise(
                    id="m07_l1_e4",
                    title="Multiple returns / branching",
                    prompt=(
                        "Write classify(altitude_km) that returns:\n"
                        "  'suborbital' if < 100\n"
                        "  'LEO' if < 2000\n"
                        "  'MEO' if < 35786\n"
                        "  'GEO+' otherwise.\n"
                        "Print classify(408)."
                    ),
                    starter_code="def classify(altitude_km):\n    pass\n",
                    checks=[
                        StdoutEquals("LEO"),
                        CallFn("classify(50)", "'suborbital'"),
                        CallFn("classify(40000)", "'GEO+'"),
                    ],
                    hints=[
                        "Use if/elif/else with `return ...` in each branch.",
                        "After return, the function exits — no else needed.",
                    ],
                    counter_keys=["functions_written"],
                    xp=35,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does a function with no return statement return?",
                    ["0", "''", "None", "Error"],
                    2,
                    "Implicitly None.",
                ),
                QuizQuestion(
                    "How do you call a function named launch with argument 'Saturn V'?",
                    ["call launch 'Saturn V'", "launch['Saturn V']", "launch(\"Saturn V\")", "launch.run('Saturn V')"],
                    2,
                    "Parentheses, with the argument inside.",
                ),
                QuizQuestion(
                    "Which is the difference between print and return?",
                    ["No difference", "print shows output; return gives a value back to the caller", "print is faster", "return only works inside loops"],
                    1,
                    "print shows. return gives back a value.",
                ),
            ]),
            resources=[
                Resource("Python docs: defining functions", "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"),
            ],
            xp_on_complete=70,
        ),
    ],
)
