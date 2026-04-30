"""Module 13: NumPy — vector math for space."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M13 = Module(
    id="m13_numpy",
    title="Module 13 — NumPy: Vector Math for Space",
    tagline="Arrays, dot products, broadcasting. The lingua franca of physics code.",
    phase="Mission Specialist",
    lessons=[
        Lesson(
            id="m13_l1",
            title="Lesson 13.1 — Arrays, vectors, broadcasting",
            body="""# NumPy

Pure Python loops are slow when you have thousands of data points. NumPy gives you **arrays** — chunks of numbers that operate as one. It's *the* standard for scientific Python: every aerospace, astronomy, and physics package builds on it.

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

a + b           # array([11, 22, 33])  — element-wise
a * 2           # array([2, 4, 6])     — broadcast scalar
np.dot(a, b)    # 140                  — scalar dot product
np.linalg.norm(a)   # 3.7416...        — vector magnitude
```

Things to notice:
1. Math operators on arrays work **element-wise** by default. No loop required.
2. A scalar (a single number) is **broadcast** to match the array's shape.
3. NumPy is *fast* — internally it's C, not Python.

## Vectors and 3D positions

A spacecraft's position is a 3-vector. With NumPy:

```python
r = np.array([6378.0, 0.0, 0.0])    # km, on the equator at sea level
v = np.array([0.0, 7.66, 0.0])      # km/s, eastward

speed = np.linalg.norm(v)            # 7.66
distance = np.linalg.norm(r)         # 6378.0
```

Need the unit vector? `r / np.linalg.norm(r)`.

## Generating ranges

```python
np.arange(0, 10, 2)         # array([0, 2, 4, 6, 8])
np.linspace(0, 1, 5)        # array([0.  , 0.25, 0.5 , 0.75, 1.  ]) — N evenly spaced points
np.zeros(5)                 # array([0., 0., 0., 0., 0.])
np.ones((2, 3))             # 2x3 matrix of ones
```

`linspace` is what you'll use to make a smooth time axis: `t = np.linspace(0, 60, 600)` (one minute, 600 samples).

## Indexing & slicing

Same rules as lists, plus 2D and boolean masking:

```python
a[0]            # first
a[-1]           # last
a[1:4]          # slice

mask = a > 10
a[mask]         # only elements where a > 10
```

## A real example: free fall

```python
import numpy as np
t = np.linspace(0, 10, 100)
h = 0.5 * 9.81 * t**2
print(h[-1])     # height after 10 seconds: 490.5 m
```

One line replaces a whole loop.
""",
            exercises=[
                Exercise(
                    id="m13_l1_e1",
                    title="Vector add",
                    prompt=(
                        "Make np arrays r = [6378, 0, 0] and v = [0, 7.66, 0]. Print r + v.\n"
                        "Expected: [6378.    7.66  0.  ]  (NumPy default formatting)"
                    ),
                    starter_code="import numpy as np\nr = np.array([6378.0, 0.0, 0.0])\nv = np.array([0.0, 7.66, 0.0])\n",
                    checks=[StdoutContains("6378"), StdoutContains("7.66")],
                    hints=["print(r + v)"],
                    xp=20,
                ),
                Exercise(
                    id="m13_l1_e2",
                    title="Magnitude",
                    prompt=(
                        "Compute the magnitude of v = [3, 4, 0] (Pythagoras in 3D). Print it.\n"
                        "Expected: 5.0"
                    ),
                    starter_code="import numpy as np\nv = np.array([3.0, 4.0, 0.0])\n",
                    checks=[StdoutEquals("5.0")],
                    hints=[
                        "Use np.linalg.norm(v).",
                    ],
                    xp=20,
                ),
                Exercise(
                    id="m13_l1_e3",
                    title="Free-fall column",
                    prompt=(
                        "Build t = np.linspace(0, 10, 11) (eleven points: 0, 1, 2, ..., 10).\n"
                        "Compute h = 0.5 * 9.81 * t**2.\n"
                        "Print h[-1] (height after 10s).\n"
                        "Expected: 490.5"
                    ),
                    starter_code="import numpy as np\n",
                    checks=[StdoutEquals("490.5")],
                    hints=[
                        "t = np.linspace(0, 10, 11)",
                        "h = 0.5 * 9.81 * t**2",
                        "print(h[-1])",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=30,
                ),
                Exercise(
                    id="m13_l1_e4",
                    title="Boolean mask: above 10 km",
                    prompt=(
                        "Given altitudes_km = np.array([0.5, 8, 12, 30, 100, 408]), use boolean masking "
                        "to print only the values >= 10. Expected: [ 12.  30. 100. 408.]"
                    ),
                    starter_code="import numpy as np\naltitudes_km = np.array([0.5, 8, 12, 30, 100, 408])\n",
                    checks=[
                        StdoutContains("12"),
                        StdoutContains("30"),
                        StdoutContains("408"),
                    ],
                    hints=[
                        "mask = altitudes_km >= 10",
                        "print(altitudes_km[mask])",
                    ],
                    xp=25,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does np.array([1,2,3]) * 2 give?",
                    ["array([2, 4, 6])", "array([1, 2, 3, 1, 2, 3])", "Error", "[2, 4, 6]"],
                    0,
                    "Element-wise multiplication.",
                ),
                QuizQuestion(
                    "What does np.linspace(0, 1, 5) produce?",
                    ["[0, 1, 2, 3, 4]", "5 evenly spaced points from 0 to 1 inclusive", "Random numbers", "[0.0, 0.25, 0.5, 0.75]"],
                    1,
                ),
                QuizQuestion(
                    "Which gives the magnitude of a 3-vector v?",
                    ["sum(v)", "np.linalg.norm(v)", "np.sqrt(v)", "len(v)"],
                    1,
                ),
            ]),
            resources=[
                Resource("NumPy quickstart", "https://numpy.org/doc/stable/user/quickstart.html"),
                Resource("NumPy for MATLAB users (if relevant)", "https://numpy.org/doc/stable/user/numpy-for-matlab-users.html"),
            ],
            xp_on_complete=80,
        ),
    ],
)
