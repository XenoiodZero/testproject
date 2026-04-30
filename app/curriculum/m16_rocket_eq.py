"""Module 16: The Rocket Equation."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M16 = Module(
    id="m16_rocket_eq",
    title="Module 16 — The Rocket Equation",
    tagline="Tsiolkovsky's tyranny: why staging exists.",
    phase="Mission Specialist",
    lessons=[
        Lesson(
            id="m16_l1",
            title="Lesson 16.1 — Delta-v, Isp, and Tsiolkovsky",
            body="""# The Tsiolkovsky rocket equation

Konstantin Tsiolkovsky figured out, in 1903, the equation that *every rocket ever built* obeys:

    Δv = v_e * ln(m0 / mf)

- **Δv** ("delta-v") is the change in velocity the rocket can produce. Hard limit. To go from Earth's surface to LEO is roughly 9,400 m/s of Δv. To leave LEO for Mars on a Hohmann transfer: another ~3,800 m/s.
- **v_e** is the exhaust velocity — how fast the engine throws mass out the back. Equivalent to specific impulse: `v_e = Isp * g0`, where `g0 = 9.81 m/s²`. Modern liquid-hydrogen engines have Isp ~450s, so v_e ~ 4400 m/s.
- **m0** is the wet mass (full of fuel). **mf** is the dry mass (after the burn).
- **ln** is the natural log (`math.log` in Python).

## The tyranny

Notice the **ln**. To double your delta-v, you don't double the fuel — you square the mass ratio. To get from 4 km/s to 12 km/s of delta-v with the same engine, you need a mass ratio of e^3 ≈ 20:1 (95% of your rocket is fuel and tank).

This is why rockets are mostly fuel. And why **staging** matters: drop empty tanks so you don't have to keep accelerating them.

## Specific impulse cheat sheet

| Engine                        | Isp (s) | v_e (m/s) |
|-------------------------------|---------|-----------|
| Solid booster (Shuttle SRB)   | ~250    | ~2450     |
| RP-1/LOX (Falcon 9 Merlin)    | ~310    | ~3040     |
| H2/LOX (Saturn V J-2)         | ~420    | ~4120     |
| Hall-effect thruster (electric)| ~1500   | ~14700    |
| Ion drive (Dawn)              | ~3000   | ~29400    |

## Worked example

A booster has m0 = 100 t, mf = 20 t, Isp = 300 s. How much delta-v does it produce?

```python
import math
g0 = 9.81
Isp = 300
v_e = Isp * g0          # 2943 m/s
delta_v = v_e * math.log(100 / 20)
print(f"{delta_v:.0f} m/s")
# 4736 m/s
```

Earth-to-LEO is ~9400 m/s. One stage gets you halfway. That's why you need stages.
""",
            exercises=[
                Exercise(
                    id="m16_l1_e1",
                    title="Tsiolkovsky as a function",
                    prompt=(
                        "Write delta_v(m0, mf, isp) that returns the delta-v from Tsiolkovsky.\n"
                        "Use g0 = 9.81. Print delta_v(100, 20, 300) to 0 decimals.\n"
                        "Expected: 4737"
                    ),
                    starter_code=(
                        "import math\n"
                        "g0 = 9.81\n"
                        "\n"
                        "def delta_v(m0, mf, isp):\n"
                        "    pass\n"
                    ),
                    checks=[StdoutContains("473")],
                    hints=[
                        "v_e = isp * g0",
                        "return v_e * math.log(m0/mf)",
                        "print(f'{delta_v(100,20,300):.0f}')",
                    ],
                    counter_keys=["functions_written", "rocket_eq_solved"],
                    xp=40,
                ),
                Exercise(
                    id="m16_l1_e2",
                    title="Mass ratio for a target Δv",
                    prompt=(
                        "Solve Tsiolkovsky backwards. Given a target delta-v of 9400 m/s and Isp 350s, "
                        "find the required mass ratio m0/mf. Print to 2 decimals.\n"
                        "Formula: ratio = exp(dv / v_e). Expected: 15.51 (or close)."
                    ),
                    starter_code="import math\ng0 = 9.81\ndv = 9400\nisp = 350\n",
                    checks=[StdoutContains("15.5")],
                    hints=[
                        "v_e = isp*g0; ratio = math.exp(dv/v_e); print(f'{ratio:.2f}')",
                    ],
                    counter_keys=["rocket_eq_solved"],
                    xp=40,
                ),
                Exercise(
                    id="m16_l1_e3",
                    title="Two-stage stack",
                    prompt=(
                        "Two stages, both Isp=300s. Stage 1: m0=100, mf=20. Stage 2 (which sits on top of stage 1's "
                        "dry mass before separation? — for this exercise treat them independently): m0=15, mf=3.\n"
                        "Compute total delta_v as the sum of each stage's delta_v. Print to 0 decimals.\n"
                        "Expected: 9476 (give or take 1)"
                    ),
                    starter_code=(
                        "import math\n"
                        "g0 = 9.81\n"
                        "\n"
                        "def delta_v(m0, mf, isp):\n"
                        "    return isp*g0*math.log(m0/mf)\n"
                    ),
                    checks=[StdoutContains("947")],
                    hints=[
                        "total = delta_v(100,20,300) + delta_v(15,3,300)",
                        "print(f'{total:.0f}')",
                    ],
                    counter_keys=["rocket_eq_solved"],
                    xp=50,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "Doubling Isp and keeping mass ratio constant:",
                    ["doubles delta-v", "squares delta-v", "halves delta-v", "no change"],
                    0,
                    "Δv = v_e * ln(m0/mf). Double v_e -> double Δv.",
                ),
                QuizQuestion(
                    "Why are real rockets staged?",
                    ["Looks cool", "To shed empty tank mass and improve effective mass ratio", "Required by law", "Heat dissipation"],
                    1,
                ),
                QuizQuestion(
                    "Tsiolkovsky uses which logarithm?",
                    ["log10", "ln (natural)", "log2", "It depends on the units"],
                    1,
                ),
            ]),
            resources=[
                Resource("NASA: rocket equation", "https://www.grc.nasa.gov/www/k-12/airplane/rktpow.html"),
                Resource("Wikipedia: Tsiolkovsky rocket equation", "https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation"),
            ],
            xp_on_complete=100,
        ),
    ],
)
