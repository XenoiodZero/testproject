"""Module 9: Star Catalogs (Dicts, Sets, Tuples)."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, CallFn
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M09 = Module(
    id="m09_dicts",
    title="Module 9 — Star Catalogs",
    tagline="Lookup tables, sets, and tuples — the workhorses.",
    phase="Flight School",
    lessons=[
        Lesson(
            id="m09_l1",
            title="Lesson 9.1 — Dictionaries",
            body="""# Dictionaries

A dict is a **lookup table**: keys -> values. Curly braces, colons:

```python
planet = {
    "name": "Mars",
    "radius_km": 3389.5,
    "gravity": 3.71,
    "moons": ["Phobos", "Deimos"],
}

planet["name"]      # 'Mars'
planet["gravity"]   # 3.71
```

Lists are positional. Dicts are by name. Use a dict whenever you'd otherwise have to remember "field 3 is gravity".

## Adding, updating, removing

```python
planet["mass_kg"] = 6.39e23     # add new key
planet["gravity"] = 3.711       # update existing
del planet["moons"]             # delete

planet.get("color", "unknown")  # safe lookup with default
"name" in planet                # True (membership test)
```

## Looping over a dict

```python
for key in planet:
    print(key)

for key, value in planet.items():
    print(f"{key} = {value}")
```

## Tuples — the immutable cousin

```python
position = (6378.0, 0.0, 0.0)   # x, y, z in km
position[0]                      # 6378.0
# position[0] = 7000           # ERROR — tuples can't be changed
x, y, z = position              # unpack into three variables
```

Use a tuple for fixed-shape records (like a 3D position). Use a list for collections that grow/shrink.

## Sets — uniqueness

```python
visited = set()
visited.add("Mars")
visited.add("Mars")
visited.add("Moon")
len(visited)            # 2
"Mars" in visited       # True
```

A set is like a dict with only keys. `set(some_list)` deduplicates.
""",
            exercises=[
                Exercise(
                    id="m09_l1_e1",
                    title="Build a planet record",
                    prompt=(
                        "Create a dict planet with keys 'name'='Mars', 'gravity'=3.71, 'radius_km'=3389.5.\n"
                        "Print exactly:\n"
                        "  Mars: g=3.71, r=3389.5"
                    ),
                    starter_code="planet = {}\n",
                    checks=[StdoutEquals("Mars: g=3.71, r=3389.5")],
                    hints=[
                        "planet = {'name': 'Mars', ...}",
                        "f-string with planet['name'], planet['gravity'], planet['radius_km'].",
                    ],
                    xp=25,
                ),
                Exercise(
                    id="m09_l1_e2",
                    title="Iterate over .items()",
                    prompt=(
                        "Given:\n"
                        "  body = {'gravity': 1.62, 'radius_km': 1737.4}\n"
                        "Loop over body.items() and print each as 'key=value'. Order matches insertion."
                    ),
                    starter_code="body = {'gravity': 1.62, 'radius_km': 1737.4}\n",
                    checks=[
                        StdoutContains("gravity=1.62"),
                        StdoutContains("radius_km=1737.4"),
                    ],
                    hints=[
                        "for k, v in body.items(): print(f\"{k}={v}\")",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=25,
                ),
                Exercise(
                    id="m09_l1_e3",
                    title="Catalog of planets",
                    prompt=(
                        "Build a dict planets where each value is itself a dict with 'gravity' and 'radius_km':\n"
                        "  Mercury -> g=3.7, r=2439.7\n"
                        "  Venus   -> g=8.87, r=6051.8\n"
                        "  Earth   -> g=9.81, r=6371.0\n"
                        "  Mars    -> g=3.71, r=3389.5\n"
                        "Then print Earth's gravity (just the number)."
                    ),
                    starter_code="planets = {}\n",
                    checks=[StdoutEquals("9.81")],
                    hints=[
                        "Nested dict: planets = { 'Earth': {'gravity': 9.81, ...}, ... }",
                        "print(planets['Earth']['gravity'])",
                    ],
                    xp=30,
                ),
                Exercise(
                    id="m09_l1_e4",
                    title="Tuples and unpacking",
                    prompt=(
                        "Given position = (6378.0, 0.0, 100.0), unpack into x, y, z and print:\n"
                        "x=6378.0 y=0.0 z=100.0"
                    ),
                    starter_code="position = (6378.0, 0.0, 100.0)\n",
                    checks=[StdoutEquals("x=6378.0 y=0.0 z=100.0")],
                    hints=[
                        "x, y, z = position",
                        "print(f\"x={x} y={y} z={z}\")",
                    ],
                    xp=25,
                ),
                Exercise(
                    id="m09_l1_e5",
                    title="Dedupe with set()",
                    prompt=(
                        "Given visits = ['Moon', 'Mars', 'Moon', 'Venus', 'Mars'], print the number of "
                        "*unique* destinations."
                    ),
                    starter_code="visits = ['Moon', 'Mars', 'Moon', 'Venus', 'Mars']\n",
                    checks=[StdoutEquals("3")],
                    hints=["len(set(visits))"],
                    xp=15,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What's the right way to look up the value at key 'name' in dict d?",
                    ["d.name", "d->name", "d['name']", "d(name)"],
                    2,
                ),
                QuizQuestion(
                    "Which is mutable (changeable)?",
                    ["tuple", "frozenset", "string", "list"],
                    3,
                ),
                QuizQuestion(
                    "set([1, 1, 2, 3, 3]) is:",
                    ["{1, 2, 3}", "{1, 1, 2, 3, 3}", "[1, 2, 3]", "Error"],
                    0,
                    "Sets discard duplicates.",
                ),
            ]),
            resources=[
                Resource("Python docs: dict", "https://docs.python.org/3/tutorial/datastructures.html#dictionaries"),
                Resource("NASA planetary fact sheets", "https://nssdc.gsfc.nasa.gov/planetary/factsheet/"),
            ],
            xp_on_complete=70,
        ),
    ],
)
