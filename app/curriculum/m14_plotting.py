"""Module 14: Plotting Trajectories with Matplotlib."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals, PredicateOnStdout
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


def _check_png_made(stdout: str) -> tuple[bool, str]:
    if "saved:" in stdout.lower() and ".png" in stdout.lower():
        return True, ""
    return False, "Expected a line like 'saved: free_fall.png' confirming the file was written."


M14 = Module(
    id="m14_plotting",
    title="Module 14 — Plotting Trajectories",
    tagline="Numbers are facts; plots are insight.",
    phase="Mission Specialist",
    lessons=[
        Lesson(
            id="m14_l1",
            title="Lesson 14.1 — Matplotlib basics",
            body="""# Matplotlib

Matplotlib is the standard plotting library. Its `pyplot` interface is what every aerospace tutorial uses.

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 200)
h = 0.5 * 9.81 * t**2

plt.figure(figsize=(8, 5))
plt.plot(t, h, label="free fall")
plt.xlabel("time (s)")
plt.ylabel("distance fallen (m)")
plt.title("Free fall, ignoring air drag")
plt.grid(True)
plt.legend()
plt.show()         # opens a window
```

That's the whole pattern, every time:
1. Build x and y arrays.
2. `plt.plot(x, y, label="...")` (call repeatedly to overlay multiple series).
3. Decorate: labels, title, grid, legend.
4. `plt.show()` to display, or `plt.savefig("name.png")` to write to disk.

In **this app**, exercises run in a subprocess that has no display, so we'll save to disk with `savefig` and *also* print a confirmation line that the grader can check.

```python
plt.savefig("free_fall.png")
print("saved: free_fall.png")
```

## Multiple curves; styling

```python
plt.plot(t, h_earth, label="Earth", color="tab:blue")
plt.plot(t, h_mars,  label="Mars",  color="tab:red", linestyle="--")
plt.legend()
```

Common styles: `'-'` solid, `'--'` dashed, `':'` dotted, `'o'` markers.

## Subplots

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(t, h)
ax1.set_title("altitude")
ax2.plot(t, v)
ax2.set_title("velocity")
fig.tight_layout()
fig.savefig("dual.png")
```

The "object-oriented" API (`fig, ax = plt.subplots(...)`) is preferred for anything beyond a one-shot plot.
""",
            exercises=[
                Exercise(
                    id="m14_l1_e1",
                    title="Plot free fall",
                    prompt=(
                        "Make t in [0, 10] with 200 samples, h = 0.5*9.81*t**2. Plot h vs. t with axis labels. "
                        "Save to 'free_fall.png' and print exactly 'saved: free_fall.png'."
                    ),
                    starter_code=(
                        "import numpy as np\n"
                        "import matplotlib\n"
                        "matplotlib.use('Agg')   # headless rendering\n"
                        "import matplotlib.pyplot as plt\n"
                        "\n"
                        "# build t, h, plot, savefig, print line\n"
                    ),
                    checks=[PredicateOnStdout(_check_png_made, label="Saved free_fall.png")],
                    hints=[
                        "plt.figure(); plt.plot(t, h); plt.xlabel('t (s)'); plt.ylabel('h (m)'); plt.savefig('free_fall.png')",
                        "Then print('saved: free_fall.png').",
                    ],
                    xp=35,
                ),
                Exercise(
                    id="m14_l1_e2",
                    title="Earth vs. Mars gravity",
                    prompt=(
                        "Plot two curves on one figure: free-fall distance on Earth (g=9.81) and Mars (g=3.71). "
                        "Use t = linspace(0, 30, 300). Add legend. Save as 'earth_vs_mars.png' and "
                        "print 'saved: earth_vs_mars.png'."
                    ),
                    starter_code=(
                        "import numpy as np\n"
                        "import matplotlib\n"
                        "matplotlib.use('Agg')\n"
                        "import matplotlib.pyplot as plt\n"
                    ),
                    checks=[PredicateOnStdout(_check_png_made, label="Saved earth_vs_mars.png")],
                    hints=[
                        "Compute h_earth = 0.5*9.81*t**2 and h_mars = 0.5*3.71*t**2.",
                        "Two plt.plot(...) calls with label=, then plt.legend().",
                        "savefig('earth_vs_mars.png') and print the line.",
                    ],
                    xp=40,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "Which line gives a dashed plot?",
                    ["plt.plot(x, y, dashed=True)", "plt.plot(x, y, '--')", "plt.dash(x, y)", "plt.plot(x, y, style='dash')"],
                    1,
                ),
                QuizQuestion(
                    "What does plt.savefig('orbit.png') do?",
                    ["Opens a window", "Saves the current figure to disk", "Prints to stdout", "Closes the figure"],
                    1,
                ),
                QuizQuestion(
                    "Why do we use matplotlib.use('Agg') in scripts?",
                    ["It's faster", "It picks a non-interactive backend (no window required)", "It activates 3D mode", "It's required by NumPy"],
                    1,
                ),
            ]),
            resources=[
                Resource("Matplotlib pyplot tutorial", "https://matplotlib.org/stable/tutorials/pyplot.html"),
                Resource("NASA image gallery (inspiration)", "https://images.nasa.gov/"),
            ],
            xp_on_complete=80,
        ),
    ],
)
