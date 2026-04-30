"""Module 12: Error Recovery — exceptions, try/except, debugging."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M12 = Module(
    id="m12_errors",
    title="Module 12 — Error Recovery",
    tagline="When things go wrong (they will), don't crash. Recover.",
    phase="Flight School",
    lessons=[
        Lesson(
            id="m12_l1",
            title="Lesson 12.1 — try / except / raise",
            body="""# Errors aren't bugs — they're communication

Real flight software has to handle the unexpected: a sensor returns nonsense, a divide-by-zero from a corrupted reading, a file that's not there. Crashing is unacceptable. Python's tool for this is `try / except`.

```python
try:
    x = int("not a number")
except ValueError:
    print("That wasn't a number; defaulting to 0")
    x = 0
```

The flow:
- Python runs the `try` block.
- If something raises an exception **of the type listed**, control jumps to `except`.
- If nothing goes wrong, the `except` block is skipped.

## Common exception types you'll see

| Type              | Cause                                      |
|-------------------|--------------------------------------------|
| `ValueError`      | Right type, wrong value (`int("abc")`)     |
| `TypeError`       | Wrong type (`"abc" + 5`)                   |
| `ZeroDivisionError` | `1 / 0`                                  |
| `IndexError`      | List index out of range                    |
| `KeyError`        | Dict key not found                         |
| `FileNotFoundError` | File doesn't exist                       |

## Catching multiple things; getting the message

```python
try:
    risky()
except (ValueError, TypeError) as exc:
    print(f"Bad input: {exc}")
```

## else and finally

```python
try:
    f = open("telemetry.csv")
except FileNotFoundError:
    print("No telemetry file.")
else:
    print("Loaded:", f.read())
    f.close()
finally:
    print("Done.")
```

`else` runs only if no exception. `finally` runs no matter what (cleanup).

## Raising your own

```python
def set_throttle(pct):
    if not 0 <= pct <= 100:
        raise ValueError(f"throttle must be 0..100, got {pct}")
    print(f"Throttle: {pct}%")
```

## Debugging tips

When you get an error, **read the bottom of the traceback first** — that's the actual exception type and message. The stack above shows the call chain.

`print(...)` is a perfectly fine debugger. Drop prints to inspect values; remove when done.
""",
            exercises=[
                Exercise(
                    id="m12_l1_e1",
                    title="Catch a bad value",
                    prompt=(
                        "Try to convert 'abort' to an int. Catch ValueError and print 'caught: invalid'."
                    ),
                    starter_code=(
                        "raw = 'abort'\n"
                        "# try int(raw); on ValueError print 'caught: invalid'\n"
                    ),
                    checks=[StdoutEquals("caught: invalid")],
                    hints=[
                        "try: int(raw)",
                        "except ValueError: print('caught: invalid')",
                    ],
                    xp=25,
                ),
                Exercise(
                    id="m12_l1_e2",
                    title="Safe divide",
                    prompt=(
                        "Write safe_divide(a, b) that returns a/b but returns the string 'undefined' if b is 0.\n"
                        "Print safe_divide(10, 0) then safe_divide(10, 2)."
                    ),
                    starter_code="def safe_divide(a, b):\n    pass\n",
                    checks=[
                        StdoutContains("undefined"),
                        StdoutContains("5.0"),
                    ],
                    hints=[
                        "try: return a / b",
                        "except ZeroDivisionError: return 'undefined'",
                    ],
                    counter_keys=["functions_written"],
                    xp=30,
                ),
                Exercise(
                    id="m12_l1_e3",
                    title="Raise your own",
                    prompt=(
                        "Write set_throttle(pct) that raises ValueError if pct < 0 or > 100, else prints 'Throttle: {pct}%'.\n"
                        "Wrap a call to set_throttle(150) in try/except to print 'rejected: <message>'."
                    ),
                    starter_code="def set_throttle(pct):\n    pass\n",
                    checks=[StdoutContains("rejected:")],
                    hints=[
                        "raise ValueError(f'throttle must be 0..100, got {pct}')",
                        "try: set_throttle(150)\nexcept ValueError as e: print(f'rejected: {e}')",
                    ],
                    counter_keys=["functions_written"],
                    xp=30,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "Which exception is raised by int('abc')?",
                    ["TypeError", "ValueError", "SyntaxError", "NameError"],
                    1,
                    "Right type (a string), wrong value (not a number) -> ValueError.",
                ),
                QuizQuestion(
                    "What does `finally:` do?",
                    ["Run only on success", "Run only on failure", "Run no matter what", "Skip cleanup"],
                    2,
                ),
                QuizQuestion(
                    "When reading a traceback, which line is most useful?",
                    ["The first line", "The last line (the actual exception)", "The middle line", "The header"],
                    1,
                ),
            ]),
            resources=[
                Resource("Python docs: errors and exceptions", "https://docs.python.org/3/tutorial/errors.html"),
            ],
            xp_on_complete=70,
        ),
    ],
)
