"""Module 4: Comms Strings — text manipulation."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M04 = Module(
    id="m04_strings",
    title="Module 4 — Comms Strings",
    tagline="Text is data. Slice, search, format, transmit.",
    phase="Boot Camp",
    lessons=[
        Lesson(
            id="m04_l1",
            title="Lesson 4.1 — Strings, slicing, methods",
            body="""# Strings

A string is a sequence of characters. The mental model: a string is like a row of seats, each with an index starting at **0**.

```
 callsign = "Apollo 11"
 index:     0 1 2 3 4 5 6 7 8
            A p o l l o _ 1 1
```

You can grab one character or a *slice*:

```python
callsign = "Apollo 11"
callsign[0]      # 'A'
callsign[-1]     # '1'  (negatives count from the right)
callsign[0:6]    # 'Apollo'   start, stop (stop is exclusive)
callsign[7:]     # '11'        from 7 to end
callsign[:6]     # 'Apollo'    start to 6
```

Slicing never errors out for going past the end — it just gives you what's there.

## Concatenation and repetition

```python
"hello" + " " + "world"   # 'hello world'
"-" * 20                   # '--------------------'
```

## Useful string methods (you'll use these constantly)

```python
"apollo".upper()            # 'APOLLO'
"APOLLO".lower()            # 'apollo'
"  Apollo  ".strip()        # 'Apollo'  (trim whitespace)
"Apollo 11".replace("11", "13")  # 'Apollo 13'
"Apollo 11".split(" ")      # ['Apollo', '11']
"-".join(["a", "b", "c"])   # 'a-b-c'
"Apollo".startswith("Ap")   # True
"Apollo".endswith("lo")     # True
len("Apollo")               # 6
```

## f-string formatting tricks

You can format numbers inside f-strings:

```python
v = 7674.123456
print(f"{v:.2f} m/s")       # 7674.12 m/s   (.2f = 2 decimal places)
print(f"{v:,.0f} m/s")      # 7,674 m/s     (thousands separator)
print(f"{42:04d}")          # 0042          (pad to width 4 with zeros)
```

This shows up everywhere in mission readouts.

## input(): asking the user

```python
name = input("Your callsign: ")
print(f"Welcome aboard, {name}.")
```

`input(...)` always returns a **string**. If you want a number, convert: `age = int(input("Age: "))` or `mass = float(input("Mass kg: "))`.
""",
            exercises=[
                Exercise(
                    id="m04_l1_e1",
                    title="Build a callsign",
                    prompt=(
                        "Make a string callsign equal to 'NASA Artemis I' (use uppercase NASA).\n"
                        "Print it in lowercase."
                    ),
                    starter_code="callsign = \"\"\n",
                    checks=[StdoutEquals("nasa artemis i")],
                    hints=[
                        "callsign = \"NASA Artemis I\"",
                        "print(callsign.lower())",
                    ],
                    xp=15,
                ),
                Exercise(
                    id="m04_l1_e2",
                    title="Slice the rocket",
                    prompt=(
                        "Given rocket = 'SaturnV-stage1', print just the part 'stage1'.\n"
                        "Use slicing — don't hard-code 'stage1' as a literal."
                    ),
                    starter_code="rocket = \"SaturnV-stage1\"\n",
                    checks=[StdoutEquals("stage1")],
                    hints=[
                        "Find the position of '-' or just slice from index 8 to the end.",
                        "rocket[8:] gives you 'stage1'.",
                        "Or: rocket.split('-')[1]",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m04_l1_e3",
                    title="Velocity readout",
                    prompt=(
                        "Set v = 7674.987. Print it formatted to 2 decimal places, with a trailing ' m/s'.\n"
                        "Expected: 7674.99 m/s"
                    ),
                    starter_code="v = 7674.987\n",
                    checks=[StdoutEquals("7674.99 m/s")],
                    hints=[
                        "Use f\"{v:.2f} m/s\".",
                        ".2f rounds to 2 decimals.",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m04_l1_e4",
                    title="Mission patch line",
                    prompt=(
                        "Print a horizontal divider made of 30 equal signs ('='), then on the next line the words 'MISSION CONTROL', then another divider line.\n"
                        "Use string repetition for the dividers."
                    ),
                    starter_code="",
                    checks=[
                        StdoutContains("=" * 30),
                        StdoutContains("MISSION CONTROL"),
                    ],
                    hints=[
                        "'=' * 30 gives you 30 equal signs.",
                        "Three print() calls: divider, label, divider.",
                    ],
                    xp=20,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does 'rocket'[1:4] evaluate to?",
                    ["'roc'", "'ock'", "'ocke'", "'r'"],
                    1,
                    "Slice [1:4] is indices 1, 2, 3 = 'ock'.",
                ),
                QuizQuestion(
                    "input() returns a value of what type?",
                    ["int", "float", "str", "depends on the input"],
                    2,
                    "Always str. You convert it yourself if you need a number.",
                ),
                QuizQuestion(
                    "What does f\"{3.14159:.2f}\" produce?",
                    ["'3.14159'", "'3.14'", "'3.1'", "'3'"],
                    1,
                    ".2f rounds to 2 decimal places.",
                ),
            ]),
            resources=[
                Resource("Python docs: string methods", "https://docs.python.org/3/library/stdtypes.html#string-methods"),
                Resource("Python docs: format spec mini-language", "https://docs.python.org/3/library/string.html#format-specification-mini-language"),
            ],
            xp_on_complete=50,
        ),
    ],
)
