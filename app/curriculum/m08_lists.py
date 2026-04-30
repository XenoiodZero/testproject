"""Module 8: Payload Lists."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, CallFn
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M08 = Module(
    id="m08_lists",
    title="Module 8 — Payload Lists",
    tagline="Stack things in order. Index, slice, append, comprehend.",
    phase="Flight School",
    lessons=[
        Lesson(
            id="m08_l1",
            title="Lesson 8.1 — Lists in depth",
            body="""# Lists

A list is an ordered, mutable collection. Square brackets, commas:

```python
crew = ["Armstrong", "Aldrin", "Collins"]
altitudes = [0, 100, 408, 2200, 35786]
mixed = [1, "two", 3.0, True]      # lists can hold mixed types (but usually shouldn't)
```

## Indexing & slicing — same rules as strings

```python
crew[0]      # 'Armstrong'
crew[-1]     # 'Collins'
crew[0:2]    # ['Armstrong', 'Aldrin']
len(crew)    # 3
```

## Adding, removing, mutating

```python
crew.append("Glenn")        # add to end
crew.insert(0, "Shepard")   # insert at index
crew.remove("Aldrin")       # remove by value
last = crew.pop()           # remove and return last
crew[0] = "Yeager"          # replace by index
```

## Looping over a list

```python
for name in crew:
    print(name)

for i, name in enumerate(crew):
    print(f"{i}: {name}")
```

## Useful built-ins

```python
sum([1, 2, 3])         # 6
min([5, 2, 9])         # 2
max([5, 2, 9])         # 9
sorted([3, 1, 2])      # [1, 2, 3]   (returns a new list)
[3, 1, 2].sort()       # in-place
"Apollo 11".split(" ") # ['Apollo', '11']  (strings -> list)
", ".join(crew)        # 'Yeager, Collins, Glenn'
```

## List comprehensions — Python's superpower

A list comprehension builds a new list from another sequence in one line:

```python
squares = [x*x for x in range(1, 6)]
# [1, 4, 9, 16, 25]

altitudes_m = [km * 1000 for km in altitudes]

heavy_burns = [b for b in burns if b > 100]
```

Pattern: `[expression for var in iterable if condition]`. The `if` is optional.

This will save you hundreds of lines over the rest of the curriculum.
""",
            exercises=[
                Exercise(
                    id="m08_l1_e1",
                    title="Crew manifest",
                    prompt=(
                        "Start with crew = ['Armstrong', 'Aldrin', 'Collins'].\n"
                        "Append 'Glenn'. Then print the crew list."
                    ),
                    starter_code="crew = ['Armstrong', 'Aldrin', 'Collins']\n",
                    checks=[StdoutContains("'Armstrong'"), StdoutContains("'Glenn'")],
                    hints=[
                        "crew.append('Glenn')",
                        "print(crew)",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m08_l1_e2",
                    title="Sum and average",
                    prompt=(
                        "Given burns = [120.5, 88.0, 240.3, 67.7], compute and print:\n"
                        "  total = ... (use sum)\n"
                        "  avg = ...\n"
                        "Print exactly:\n"
                        "  total: 516.50\n"
                        "  avg: 129.13"
                    ),
                    starter_code="burns = [120.5, 88.0, 240.3, 67.7]\n",
                    checks=[
                        StdoutContains("total: 516.50"),
                        StdoutContains("avg: 129.13"),
                    ],
                    hints=[
                        "total = sum(burns); avg = total / len(burns)",
                        "f-string with .2f format.",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
                Exercise(
                    id="m08_l1_e3",
                    title="Comprehension: km to m",
                    prompt=(
                        "Given altitudes_km = [0, 100, 408, 2200, 35786], use a list comprehension to "
                        "build altitudes_m where each value is multiplied by 1000.\n"
                        "Print the result."
                    ),
                    starter_code="altitudes_km = [0, 100, 408, 2200, 35786]\n",
                    checks=[
                        CallFn("altitudes_m", "[0, 100000, 408000, 2200000, 35786000]"),
                    ],
                    hints=[
                        "altitudes_m = [km * 1000 for km in altitudes_km]",
                        "Then print(altitudes_m).",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
                Exercise(
                    id="m08_l1_e4",
                    title="Filter heavy burns",
                    prompt=(
                        "Given burns = [120.5, 88.0, 240.3, 67.7, 305.1], use a comprehension with a filter "
                        "to make heavy = list of burns > 100. Print heavy.\n"
                        "Expected: [120.5, 240.3, 305.1]"
                    ),
                    starter_code="burns = [120.5, 88.0, 240.3, 67.7, 305.1]\n",
                    checks=[CallFn("heavy", "[120.5, 240.3, 305.1]")],
                    hints=[
                        "heavy = [b for b in burns if b > 100]",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
                Exercise(
                    id="m08_l1_e5",
                    title="Find the max altitude",
                    prompt=(
                        "Given altitudes = [220, 408, 35786, 380, 1200, 18000], print the largest value.\n"
                        "Use max()."
                    ),
                    starter_code="altitudes = [220, 408, 35786, 380, 1200, 18000]\n",
                    checks=[StdoutEquals("35786")],
                    hints=["print(max(altitudes))"],
                    xp=15,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does crew.append('X') do?",
                    ["Replaces the list", "Adds 'X' to the end", "Adds 'X' to the start", "Removes 'X'"],
                    1,
                ),
                QuizQuestion(
                    "What does [x*2 for x in range(3)] produce?",
                    ["[0, 2, 4]", "[2, 4, 6]", "[1, 2, 4]", "Error"],
                    0,
                    "range(3) is 0,1,2; doubled is 0,2,4.",
                ),
                QuizQuestion(
                    "How do you get the second-to-last element?",
                    ["lst[-1]", "lst[-2]", "lst[len-1]", "lst[2]"],
                    1,
                ),
            ]),
            resources=[
                Resource("Python docs: list", "https://docs.python.org/3/tutorial/datastructures.html"),
            ],
            xp_on_complete=70,
        ),
    ],
)
