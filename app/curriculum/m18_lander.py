"""Module 18: Mars Lander Sim — pulling it all together."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M18 = Module(
    id="m18_lander",
    title="Module 18 — Simulating a Mars Lander",
    tagline="Numerical integration. Discrete time steps. Touchdown.",
    phase="Mission Specialist",
    lessons=[
        Lesson(
            id="m18_l1",
            title="Lesson 18.1 — Euler integration and a 1D lander",
            body="""# A 1D Mars lander

We're going to simulate a powered descent. 1D for now: just altitude, vertical velocity, vertical thrust. We'll go 2D in the final projects.

## Physics in tiny steps (Euler integration)

Continuous physics:

    dv/dt = (T_thrust - m*g) / m
    dh/dt = v

You can't solve the integral by hand for a real lander (thrust changes, mass changes as fuel burns). But you can **step time forward in tiny chunks `dt`** and update each variable a little:

```python
v += (thrust/mass - g_mars) * dt
h += v * dt
mass -= fuel_flow_rate * dt
t += dt
```

That's **Euler's method**. It's not the most accurate (real software uses Runge-Kutta or symplectic integrators), but it's perfectly fine for this — and it's easy to reason about.

## The simulation loop

```python
import math

g_mars = 3.71
mass = 600.0          # kg, dry+fuel
fuel = 200.0          # kg, included in mass
thrust = 3000.0       # N (constant for this demo)
flow = 1.5            # kg/s of fuel

h = 1000.0            # start 1 km up
v = -80.0             # falling at 80 m/s
t = 0.0
dt = 0.1

while h > 0:
    # gravity always
    a = -g_mars
    # if there's fuel, fire engine (upward thrust)
    if fuel > 0:
        a += thrust / mass
        mass -= flow * dt
        fuel -= flow * dt
    v += a * dt
    h += v * dt
    t += dt
    if t > 200:        # safety bailout
        break

print(f"touchdown at t={t:.1f}s, v={v:.2f} m/s")
```

What you're seeing here is the same skeleton SpaceX, NASA, and ESA use for descent simulation. Real ones add 6 degrees of freedom, throttle profiles, sensor noise, terrain, and Mars's atmosphere. But the core loop is the same.

## Survivable landing speed

Curiosity touched down at about **0.6 m/s**. Anything under ~3 m/s is generally survivable for a sturdy probe. Above that — bent legs at best, scrap metal at worst.

## In the exercise

You'll write a `simulate(initial_v, fuel_kg, thrust_n)` function. Try different inputs. Get a feel for what works.
""",
            exercises=[
                Exercise(
                    id="m18_l1_e1",
                    title="One-step Euler",
                    prompt=(
                        "A craft is at h=100m, v=-10 (falling), with no thrust on Mars (g=3.71). After dt=0.5 seconds, "
                        "what's the new (h, v)?\n"
                        "Compute and print as: h=94.54 v=-11.86 (your numbers should match those exactly)."
                    ),
                    starter_code=(
                        "g = 3.71\n"
                        "h, v = 100.0, -10.0\n"
                        "dt = 0.5\n"
                        "# Euler: v_new = v + (-g)*dt; h_new = h + v_old*dt   (use OLD v for h update)\n"
                    ),
                    checks=[StdoutEquals("h=94.54 v=-11.86")],
                    hints=[
                        "Compute v_new with -g*dt.",
                        "For h_new use the OLD v: h + v*dt.",
                        "Format both: f'h={h_new:.2f} v={v_new:.2f}'",
                    ],
                    xp=35,
                ),
                Exercise(
                    id="m18_l1_e2",
                    title="Powered descent loop",
                    prompt=(
                        "Write the descent loop from the lesson. Start with h=1000, v=-80, mass=600, fuel=200, "
                        "thrust=3000, flow=1.5, dt=0.1, g_mars=3.71. Loop until h <= 0 or t > 200.\n"
                        "Print the final touchdown line:  touchdown at t=XX.Xs, v=YY.YY m/s\n"
                        "We just check it contains 'touchdown at t=' and 'm/s'."
                    ),
                    starter_code=(
                        "g = 3.71\n"
                        "mass = 600.0\nfuel = 200.0\nthrust = 3000.0\nflow = 1.5\n"
                        "h = 1000.0\nv = -80.0\nt = 0.0\ndt = 0.1\n"
                    ),
                    checks=[
                        StdoutContains("touchdown at t="),
                        StdoutContains("m/s"),
                    ],
                    hints=[
                        "while h > 0: compute a, update v then h, decrement fuel/mass if fuel > 0.",
                        "Increment t by dt each iteration.",
                        "After the loop: print(f'touchdown at t={t:.1f}s, v={v:.2f} m/s')",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=60,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "Euler integration is:",
                    ["Solving the integral analytically", "Stepping forward in tiny dt and updating each variable", "Random sampling", "An IDE"],
                    1,
                ),
                QuizQuestion(
                    "Why does mass decrease during the burn?",
                    ["The lander shrinks", "Fuel is being expelled out the engine", "Gravity changes mass", "It doesn't"],
                    1,
                ),
                QuizQuestion(
                    "A smaller dt:",
                    ["Makes the simulation more accurate but slower", "Makes it faster", "Has no effect", "Is forbidden"],
                    0,
                ),
            ]),
            resources=[
                Resource("Wikipedia: Euler method", "https://en.wikipedia.org/wiki/Euler_method"),
                Resource("Curiosity landing animation", "https://mars.nasa.gov/msl/timeline/landing/"),
            ],
            xp_on_complete=120,
        ),
    ],
)
