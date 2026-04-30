"""Module 6: Looping Through Space — for, while, range, break."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M06 = Module(
    id="m06_loops",
    title="Module 6 — Looping Through Space",
    tagline="Repeat until orbit. Or until something explodes.",
    phase="Boot Camp",
    lessons=[
        Lesson(
            id="m06_l1",
            title="Lesson 6.1 — for loops and range()",
            body="""# Loops

Most useful programs do something many times. Python has two loop forms.

## for

A `for` loop steps through a sequence:

```python
for i in [10, 9, 8, 7]:
    print(i)
```

Or, more commonly, with `range()`:

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):    # 1, 2, 3, 4, 5  (start, stop)
    print(i)

for i in range(10, 0, -1):   # 10, 9, ..., 1
    print(i)
```

`range(stop)` goes from 0 up to but **not including** stop. `range(start, stop)` is the same idea. `range(start, stop, step)` lets you skip or count down.

## A countdown

```python
for t in range(10, 0, -1):
    print(f"T-minus {t}")
print("LIFTOFF!")
```

## while

Use `while` when you don't know the number of iterations up front — keep going as long as a condition is true.

```python
fuel = 100
while fuel > 0:
    print(f"Fuel: {fuel}%")
    fuel -= 10        # short for fuel = fuel - 10
print("Empty.")
```

`fuel -= 10` is the same as `fuel = fuel - 10`. There's also `+=`, `*=`, `/=`, `//=`, `%=`.

## break and continue

- `break` exits the loop immediately.
- `continue` skips to the next iteration.

```python
for t in range(10, 0, -1):
    if t == 3:
        print("HOLD! Engineer paused countdown.")
        break
    print(f"T-minus {t}")
```

## Sum a sequence

A pattern you'll write a thousand times:

```python
total = 0
for x in [12.4, 9.1, 8.7, 11.0]:
    total += x
print(total)        # 41.2
```
""",
            exercises=[
                Exercise(
                    id="m06_l1_e1",
                    title="Countdown",
                    prompt=(
                        "Print T-minus 10 down to T-minus 1 (each on its own line, format 'T-minus 10' etc), "
                        "then print 'LIFTOFF!' on the last line."
                    ),
                    starter_code="# for loop with range(...)\n",
                    checks=[
                        StdoutContains("T-minus 10"),
                        StdoutContains("T-minus 1\n"),
                        StdoutContains("LIFTOFF!"),
                    ],
                    hints=[
                        "range(10, 0, -1) gives 10, 9, ..., 1.",
                        "Print LIFTOFF! after the loop ends.",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=25,
                ),
                Exercise(
                    id="m06_l1_e2",
                    title="Sum the burns",
                    prompt=(
                        "A series of engine burns produced these delta-v values (m/s):\n"
                        "  burns = [120.5, 88.0, 240.3, 67.7]\n"
                        "Use a for-loop to sum them. Print the total to 2 decimal places, like:\n"
                        "  total dv: 516.50 m/s"
                    ),
                    starter_code="burns = [120.5, 88.0, 240.3, 67.7]\ntotal = 0\n",
                    checks=[StdoutEquals("total dv: 516.50 m/s")],
                    hints=[
                        "for x in burns: total += x",
                        "f-string: f\"total dv: {total:.2f} m/s\"",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
                Exercise(
                    id="m06_l1_e3",
                    title="Drain the tank",
                    prompt=(
                        "Start with fuel = 100. In a while-loop, keep subtracting 15 until fuel <= 0. "
                        "Each iteration print 'Fuel: <amount>%'. Don't print fuel after it drops below zero. "
                        "After the loop, print 'Empty.'"
                    ),
                    starter_code="fuel = 100\n",
                    checks=[
                        StdoutContains("Fuel: 100%"),
                        StdoutContains("Empty."),
                    ],
                    hints=[
                        "while fuel > 0: print, then fuel -= 15.",
                        "Print Empty. after the loop.",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
                Exercise(
                    id="m06_l1_e4",
                    title="Find the first launch window",
                    prompt=(
                        "Given a list of weather scores per day (0=bad, 1=ok, 2=clear):\n"
                        "  weather = [0, 0, 1, 0, 2, 1, 0]\n"
                        "Use a for-loop with break to find the *first* day with score == 2 and "
                        "print 'launch on day <i>' (using the index)."
                    ),
                    starter_code="weather = [0, 0, 1, 0, 2, 1, 0]\n",
                    checks=[StdoutEquals("launch on day 4")],
                    hints=[
                        "Use enumerate(weather) to get index + value, or range(len(weather)).",
                        "if score == 2: print(...); break",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does range(5) produce?",
                    ["1, 2, 3, 4, 5", "0, 1, 2, 3, 4", "0, 1, 2, 3, 4, 5", "1 through 5 inclusive"],
                    1,
                    "range(stop) goes from 0 up to but NOT including stop.",
                ),
                QuizQuestion(
                    "x += 5 is shorthand for:",
                    ["x = 5", "x = x + 5", "x = x * 5", "Nothing"],
                    1,
                    "+= adds in place.",
                ),
                QuizQuestion(
                    "What does `break` do inside a loop?",
                    ["Exits the loop immediately", "Skips to the next iteration", "Pauses the program", "Restarts the loop"],
                    0,
                    "break ends the enclosing loop. continue skips to next iteration.",
                ),
                QuizQuestion(
                    "Which is best when you don't know how many iterations you need?",
                    ["for", "while", "range()", "break"],
                    1,
                    "while runs as long as a condition holds.",
                ),
            ]),
            resources=[
                Resource("Python docs: more on for/while", "https://docs.python.org/3/tutorial/controlflow.html#for-statements"),
                Resource("ISS orbital period", "https://spotthestation.nasa.gov/", "Real ISS pass times — every ~92 minutes."),
            ],
            xp_on_complete=60,
        ),
    ],
)
