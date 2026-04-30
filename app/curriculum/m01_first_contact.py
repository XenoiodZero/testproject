"""Module 1: First Contact — print, comments, running Python."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M01 = Module(
    id="m01_first_contact",
    title="Module 1 — First Contact",
    tagline="Power on the console. Make Python say something.",
    phase="Boot Camp",
    lessons=[
        Lesson(
            id="m01_l1",
            title="Lesson 1.1 — Hello, Universe",
            body="""# Hello, Universe

Welcome aboard, Cadet.

Every astronaut starts the day with a comms check. In Python, the comms check is one line:

```python
print("Hello, Universe!")
```

`print(...)` is a **function**: a tool you call by writing its name and putting stuff in parentheses. Whatever you put inside, Python sends out to the console (the black-text window where output appears).

The thing in quotes — `"Hello, Universe!"` — is a **string**. A string is just text. You can use double quotes (`"like this"`) or single quotes (`'like this'`), Python doesn't care. Pick one and be consistent.

## Comments

Lines that start with `#` are **comments**. Python ignores them. They're notes for humans (including future-you):

```python
# This is mission log entry 001.
print("T-minus 10")  # countdown begins
```

You can put a comment on its own line, or after some code on the same line.

## Why aerospace cares

When you're flying anything that costs $300M, every line of code is documented. NASA's own Python style guide leans heavily on comments and docstrings. The habit starts now.

## Try it

In the box on the right, hit **Run**. The starter code is already a `print` — change the message and run it again. Nothing breaks. You can run code as many times as you want.
""",
            exercises=[
                Exercise(
                    id="m01_l1_e1",
                    title="Send the launch greeting",
                    prompt="Print exactly:  Liftoff!",
                    starter_code='# Replace this comment with a print statement.\n',
                    checks=[StdoutEquals("Liftoff!")],
                    hints=[
                        "Use print(...) with the text in quotes.",
                        "The quotes are part of the syntax, not part of the output.",
                        "Solution: print(\"Liftoff!\")",
                    ],
                    xp=15,
                ),
                Exercise(
                    id="m01_l1_e2",
                    title="Two-line transmission",
                    prompt="Print two lines: first 'Mission Control, do you copy?' then 'Apollo here, we hear you.'",
                    starter_code="# Two print() calls do two lines.\n",
                    checks=[
                        StdoutContains("Mission Control, do you copy?"),
                        StdoutContains("Apollo here, we hear you."),
                    ],
                    hints=[
                        "Each print() ends its output with a newline automatically.",
                        "Two separate print() calls give you two lines.",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m01_l1_e3",
                    title="Comment + print",
                    prompt="Add a comment on the first line that says: # mission log 001\nThen print: All systems nominal.",
                    starter_code="",
                    checks=[StdoutEquals("All systems nominal.")],
                    hints=[
                        "A comment line starts with #.",
                        "The comment doesn't affect output. Just print the message.",
                    ],
                    xp=15,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "Which line prints 'Go for launch'?",
                    [
                        'echo "Go for launch"',
                        'print(Go for launch)',
                        'print("Go for launch")',
                        'PRINT("Go for launch")',
                    ],
                    2,
                    "Python uses print(...), lowercase, with quotes around text.",
                ),
                QuizQuestion(
                    "What does Python do with a line that starts with #?",
                    ["Errors out", "Prints it", "Ignores it (it's a comment)", "Saves it as a variable"],
                    2,
                    "# starts a comment. Python skips the rest of that line.",
                ),
                QuizQuestion(
                    "Which is a valid string in Python?",
                    ["Hello", '"Hello"', "[Hello]", "<Hello>"],
                    1,
                    "Strings need matching quotes.",
                ),
            ]),
            resources=[
                Resource("Python docs: print()", "https://docs.python.org/3/library/functions.html#print"),
                Resource("NASA Python style notes (general)", "https://www.python.org/dev/peps/pep-0008/", "PEP 8 — the closest thing Python has to an aerospace style guide."),
            ],
            xp_on_complete=40,
        ),
    ],
)
