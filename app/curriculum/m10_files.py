"""Module 10: Telemetry Files — reading and writing files, CSV, JSON."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, PredicateOnStdout
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M10 = Module(
    id="m10_files",
    title="Module 10 — Telemetry Files",
    tagline="Read it, parse it, save it. Real data starts here.",
    phase="Flight School",
    lessons=[
        Lesson(
            id="m10_l1",
            title="Lesson 10.1 — Reading and writing files, CSV, JSON",
            body="""# Files

Real telemetry doesn't live in your code — it lives in files. Python opens them with `open(path, mode)`. The mode is `'r'` (read), `'w'` (write, overwrite), or `'a'` (append).

The idiomatic pattern uses `with`, which automatically closes the file when the block ends:

```python
with open("log.txt", "w") as f:
    f.write("Mission start\\n")
    f.write("Engines nominal\\n")

with open("log.txt", "r") as f:
    text = f.read()           # whole file as one string
    print(text)
```

To read line-by-line:

```python
with open("log.txt", "r") as f:
    for line in f:
        print(line.strip())   # strip removes the trailing newline
```

## CSV — comma-separated values

Most telemetry exports look like this:

```
time_s,altitude_m,velocity_ms
0.0,0,0
1.0,4.9,9.81
2.0,19.6,19.6
```

Python ships with a `csv` module:

```python
import csv

with open("flight.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # each row is a dict: {'time_s': '0.0', 'altitude_m': '0', ...}
        t = float(row["time_s"])
        alt = float(row["altitude_m"])
        print(f"t={t}s, alt={alt}m")
```

`DictReader` uses the first row as headers. Values are always strings; you convert.

## JSON — structured data

JSON is what most space-related APIs (including NASA's) return.

```python
import json

planet = {"name": "Mars", "moons": ["Phobos", "Deimos"]}

# write
with open("mars.json", "w") as f:
    json.dump(planet, f, indent=2)

# read
with open("mars.json", "r") as f:
    data = json.load(f)
print(data["moons"])
```

In the exercises below, the app pre-creates a small file in your working directory; you read it.

(The runner runs your code in a fresh subprocess in the OS's temp folder, so for the exercises that need a file we'll *write the file from your code* first, then read it — that way it's reproducible.)
""",
            exercises=[
                Exercise(
                    id="m10_l1_e1",
                    title="Write then read",
                    prompt=(
                        "Write a file 'log.txt' with two lines:\n"
                        "  Engines nominal\n"
                        "  Stage 1 ignition\n"
                        "Then read it back and print its contents (preserving the newline)."
                    ),
                    starter_code=(
                        "with open('log.txt', 'w') as f:\n"
                        "    f.write('Engines nominal\\n')\n"
                        "    f.write('Stage 1 ignition\\n')\n"
                        "\n"
                        "# now open in read mode and print the contents\n"
                    ),
                    checks=[
                        StdoutContains("Engines nominal"),
                        StdoutContains("Stage 1 ignition"),
                    ],
                    hints=[
                        "with open('log.txt', 'r') as f: print(f.read())",
                    ],
                    xp=25,
                ),
                Exercise(
                    id="m10_l1_e2",
                    title="Parse a small CSV",
                    prompt=(
                        "Build flight.csv with the rows shown in starter code, then use csv.DictReader "
                        "to compute and print the maximum altitude in meters from the 'altitude_m' column.\n"
                        "Expected: max alt: 19.6"
                    ),
                    starter_code=(
                        "import csv\n"
                        "with open('flight.csv', 'w') as f:\n"
                        "    f.write('time_s,altitude_m\\n0.0,0\\n1.0,4.9\\n2.0,19.6\\n')\n"
                        "\n"
                        "max_alt = 0.0\n"
                        "with open('flight.csv', 'r') as f:\n"
                        "    reader = csv.DictReader(f)\n"
                        "    # loop over rows, update max_alt\n"
                        "    pass\n"
                        "\n"
                        "print(f'max alt: {max_alt}')\n"
                    ),
                    checks=[StdoutContains("max alt: 19.6")],
                    hints=[
                        "Replace `pass` with: for row in reader: alt = float(row['altitude_m']); if alt > max_alt: max_alt = alt",
                        "Or: use a list comprehension and max().",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=35,
                ),
                Exercise(
                    id="m10_l1_e3",
                    title="JSON round-trip",
                    prompt=(
                        "Save the planet dict to 'mars.json', then read it back into a different variable, "
                        "and print read_back['name'].\n"
                        "Expected: Mars"
                    ),
                    starter_code=(
                        "import json\n"
                        "planet = {'name': 'Mars', 'gravity': 3.71}\n"
                        "# json.dump to mars.json, then json.load back into read_back\n"
                    ),
                    checks=[StdoutContains("Mars")],
                    hints=[
                        "json.dump(planet, open('mars.json','w'))  # or with-block",
                        "read_back = json.load(open('mars.json'))",
                        "print(read_back['name'])",
                    ],
                    xp=30,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does `with open(path) as f:` give you over plain `f = open(path)`?",
                    ["Faster speed", "Auto-closes the file when the block ends", "Encrypts the file", "Nothing"],
                    1,
                ),
                QuizQuestion(
                    "csv.DictReader values are of what type by default?",
                    ["int", "float", "str", "auto-detected"],
                    2,
                    "Always strings. Convert as needed.",
                ),
                QuizQuestion(
                    "Which mode opens a file for writing, creating or overwriting it?",
                    ["'r'", "'w'", "'a'", "'x'"],
                    1,
                ),
            ]),
            resources=[
                Resource("Python docs: input/output", "https://docs.python.org/3/tutorial/inputoutput.html"),
                Resource("NASA Open Data Portal", "https://data.nasa.gov/", "Tons of real CSV/JSON datasets."),
            ],
            xp_on_complete=70,
        ),
    ],
)
