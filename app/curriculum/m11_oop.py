"""Module 11: Spacecraft Classes — OOP."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, CallFn
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M11 = Module(
    id="m11_oop",
    title="Module 11 — Spacecraft Classes",
    tagline="Bundle data + behavior. Build your own types.",
    phase="Flight School",
    lessons=[
        Lesson(
            id="m11_l1",
            title="Lesson 11.1 — Classes, instances, methods",
            body="""# Classes

A class is a blueprint for a custom type. You define what data each instance carries (its **attributes**) and what it can do (its **methods**).

```python
class Spacecraft:
    def __init__(self, name, fuel_tons):
        self.name = name
        self.fuel_tons = fuel_tons

    def burn(self, tons):
        self.fuel_tons -= tons
        print(f"{self.name}: {self.fuel_tons:.1f}t fuel remaining")

orion = Spacecraft("Orion", 10.0)
orion.burn(2.5)
orion.burn(3.0)
print(orion.fuel_tons)    # 4.5
```

Walk through that:
- `class Spacecraft:` defines a new type.
- `__init__` (two underscores each side) is the **constructor** — it runs every time you make a new instance with `Spacecraft(...)`.
- `self` is the instance itself. The first parameter of every method is `self`. You don't pass it explicitly when calling — Python does it.
- `self.name = name` saves the argument as an attribute on the instance.
- `orion = Spacecraft("Orion", 10.0)` creates an instance.
- `orion.burn(2.5)` calls the method, with `self` automatically bound to `orion`.

## Why bother?

For aerospace specifically: a spacecraft has a state (mass, fuel, velocity, attitude...) and a set of operations (burn, deploy, separate, dock). A class keeps state and behavior together so a function 50 lines later doesn't have to take 9 parameters.

## __repr__ — friendlier print

If you `print(orion)` you'll get something ugly like `<Spacecraft object at 0x...>`. Define `__repr__` to fix that:

```python
class Spacecraft:
    def __init__(self, name, fuel_tons):
        self.name = name
        self.fuel_tons = fuel_tons

    def __repr__(self):
        return f"Spacecraft(name={self.name!r}, fuel_tons={self.fuel_tons})"
```

## Inheritance (briefly)

```python
class Capsule(Spacecraft):
    def __init__(self, name, fuel_tons, crew_size):
        super().__init__(name, fuel_tons)
        self.crew_size = crew_size

dragon = Capsule("Dragon", 1.5, 4)
dragon.burn(0.2)   # inherited from Spacecraft
print(dragon.crew_size)
```

`super().__init__(...)` calls the parent class's constructor.

You won't need deep inheritance trees here — Python culture favors simpler designs — but knowing the basics is enough.
""",
            exercises=[
                Exercise(
                    id="m11_l1_e1",
                    title="Define a Spacecraft",
                    prompt=(
                        "Write class Spacecraft with __init__(self, name, fuel_tons) and a method burn(self, tons) "
                        "that subtracts tons from fuel.\n"
                        "Make orion = Spacecraft('Orion', 10.0), call orion.burn(2.5), then print orion.fuel_tons.\n"
                        "Expected: 7.5"
                    ),
                    starter_code=(
                        "class Spacecraft:\n"
                        "    def __init__(self, name, fuel_tons):\n"
                        "        pass\n"
                        "\n"
                        "    def burn(self, tons):\n"
                        "        pass\n"
                        "\n"
                        "orion = Spacecraft('Orion', 10.0)\n"
                        "orion.burn(2.5)\n"
                        "print(orion.fuel_tons)\n"
                    ),
                    checks=[StdoutEquals("7.5")],
                    hints=[
                        "Inside __init__: self.name = name; self.fuel_tons = fuel_tons.",
                        "Inside burn: self.fuel_tons -= tons.",
                    ],
                    counter_keys=["classes_written"],
                    xp=35,
                ),
                Exercise(
                    id="m11_l1_e2",
                    title="Add __repr__",
                    prompt=(
                        "Extend the Spacecraft class with __repr__ that returns:\n"
                        "  Spacecraft(name='Orion', fuel=7.5t)\n"
                        "Then construct one with fuel 7.5 and print it."
                    ),
                    starter_code=(
                        "class Spacecraft:\n"
                        "    def __init__(self, name, fuel_tons):\n"
                        "        self.name = name\n"
                        "        self.fuel_tons = fuel_tons\n"
                        "\n"
                        "    def __repr__(self):\n"
                        "        return ''\n"
                        "\n"
                        "orion = Spacecraft('Orion', 7.5)\n"
                        "print(orion)\n"
                    ),
                    checks=[StdoutEquals("Spacecraft(name='Orion', fuel=7.5t)")],
                    hints=[
                        "f\"Spacecraft(name={self.name!r}, fuel={self.fuel_tons}t)\"",
                        "!r calls repr() on the value (gives quoted strings).",
                    ],
                    counter_keys=["classes_written"],
                    xp=30,
                ),
                Exercise(
                    id="m11_l1_e3",
                    title="Subclass: Capsule",
                    prompt=(
                        "Make Capsule(Spacecraft) that adds a crew_size attribute.\n"
                        "Constructor signature: __init__(self, name, fuel_tons, crew_size).\n"
                        "Use super().__init__ for the parent fields.\n"
                        "Construct dragon = Capsule('Dragon', 1.5, 4); print dragon.crew_size, dragon.name."
                    ),
                    starter_code=(
                        "class Spacecraft:\n"
                        "    def __init__(self, name, fuel_tons):\n"
                        "        self.name = name\n"
                        "        self.fuel_tons = fuel_tons\n"
                        "\n"
                        "class Capsule(Spacecraft):\n"
                        "    def __init__(self, name, fuel_tons, crew_size):\n"
                        "        pass\n"
                        "\n"
                        "dragon = Capsule('Dragon', 1.5, 4)\n"
                        "print(dragon.crew_size, dragon.name)\n"
                    ),
                    checks=[StdoutEquals("4 Dragon")],
                    hints=[
                        "super().__init__(name, fuel_tons); self.crew_size = crew_size",
                    ],
                    counter_keys=["classes_written"],
                    xp=35,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What is `self` in a method?",
                    ["A keyword to define a class", "The instance the method was called on", "The class itself", "Optional — you don't need it"],
                    1,
                ),
                QuizQuestion(
                    "Which method runs when you call MyClass(...)?",
                    ["__call__", "__new__", "__init__", "create"],
                    2,
                ),
                QuizQuestion(
                    "What does super().__init__(...) do?",
                    ["Calls a global init", "Calls the parent class's __init__", "Resets the object", "Errors out"],
                    1,
                ),
            ]),
            resources=[
                Resource("Python docs: classes", "https://docs.python.org/3/tutorial/classes.html"),
            ],
            xp_on_complete=70,
        ),
    ],
)
