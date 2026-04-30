"""Final projects B: ISS tracker, mission control dashboard, two-body propagator."""
from __future__ import annotations

from ..grader import StdoutContains, PredicateOnStdout
from ._types import Project, Resource


def _has_iss_lat_lon(stdout: str) -> tuple[bool, str]:
    if "lat=" not in stdout.lower() or "lon=" not in stdout.lower():
        return False, "Expected output containing lat= and lon= for the ISS position."
    return True, ""


ISS_TRACKER = Project(
    id="fp_iss",
    title="Capstone 3 — Live ISS Tracker",
    summary="Pull live position data from the Open Notify API and plot the ISS ground track over time.",
    brief="""# Mission brief — track the ISS

The ISS broadcasts its current latitude and longitude through a free API. Your job:

1. Poll the API every ~5 seconds.
2. Save each (timestamp, lat, lon) reading to a list.
3. After ~60 seconds (or whenever you stop it), plot the points on a simple lat/lon map.
4. Save the plot as `iss_track.png`.

**API.** GET http://api.open-notify.org/iss-now.json (no key required).

**Required output line (at minimum):**

```
ISS now at lat=...  lon=...
```

You can print one of those each tick.

**Two important details:**

- The lat/lon come back as *strings*. Convert with float().
- The ISS moves fast. Even 5-second samples will produce a clearly curved track over a minute.

**Bonus.**

- Overlay a world-map outline (`cartopy` is the heavy-duty option, but you can also just draw the equator and prime meridian as reference lines).
- Store readings to a CSV (`iss_track.csv`) using Python's `csv` module — Module 10 was a primer.
- Compute the ISS's instantaneous ground speed in km/s using a great-circle distance formula between consecutive points and `dt`.

**If your environment can't reach the network**, swap in a recorded list of (lat, lon) pairs and treat the rest as a plotting/CSV exercise.

**Why this matters.** This is the *exact* shape of every ground-station-side telemetry consumer: poll endpoint, parse JSON, append to time series, visualize. Different domain, different field names, but identical bones.
""",
    starter_code='''"""Live ISS tracker.

Polls Open Notify every TICK_SECS and plots the ground track.
Stops after MAX_SECS (default 60). Save plot as iss_track.png.
"""
import time
import json
import csv
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

URL = "http://api.open-notify.org/iss-now.json"
TICK_SECS = 5
MAX_SECS = 60   # short by default so the smoke test finishes; bump to 600+ for real fun

readings = []  # list of (t, lat, lon)
start = time.time()

while time.time() - start < MAX_SECS:
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        t = data["timestamp"]
        readings.append((t, lat, lon))
        print(f"ISS now at lat={lat:.2f}  lon={lon:.2f}")
    except requests.RequestException as e:
        print(f"network error: {e}; backing off")
    time.sleep(TICK_SECS)

# Save CSV
with open("iss_track.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "lat", "lon"])
    w.writerows(readings)
print("saved: iss_track.csv")

# Plot
if readings:
    lats = [r[1] for r in readings]
    lons = [r[2] for r in readings]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(lons, lats, "-o", markersize=3, color="tab:cyan")
    ax.axhline(0, color="gray", linewidth=0.5); ax.axvline(0, color="gray", linewidth=0.5)
    ax.set_xlim(-180, 180); ax.set_ylim(-90, 90)
    ax.set_xlabel("longitude (deg)"); ax.set_ylabel("latitude (deg)")
    ax.set_title("ISS ground track")
    ax.grid(True, alpha=0.3)
    fig.savefig("iss_track.png")
    print("saved: iss_track.png")
''',
    checks=[
        PredicateOnStdout(_has_iss_lat_lon, label="Printed at least one lat/lon reading"),
    ],
    bonus_objectives=[
        "Add a CSV writer per the spec (already in starter — but try removing it and re-implementing).",
        "Compute ground speed between consecutive readings using haversine distance.",
        "Add a moving dot showing the *current* position with a different marker.",
    ],
    hints=[
        "If you have no internet, replace the `while` body with a list of fake (lat, lon) and the rest works.",
        "Module 17 covers the API call. Module 14 covers plotting. You're combining them.",
        "Set MAX_SECS lower while debugging; bump it back up once it works.",
    ],
    resources=[
        Resource("Open Notify ISS endpoint", "http://open-notify.org/Open-Notify-API/ISS-Location-Now/"),
        Resource("Cartopy (advanced map plotting)", "https://scitools.org.uk/cartopy/docs/latest/"),
    ],
    xp=600,
)


def _has_dashboard_loop(stdout: str) -> tuple[bool, str]:
    if "tick" not in stdout.lower() and "telemetry" not in stdout.lower():
        return False, "Expected periodic telemetry print lines (e.g. 'tick' or 'telemetry: ...')."
    return True, ""


DASHBOARD = Project(
    id="fp_dashboard",
    title="Capstone 4 — Mission Control Dashboard",
    summary="Build YOUR OWN Tkinter app: a live mission-control dashboard with simulated rocket telemetry.",
    brief="""# Mission brief — Mission Control Dashboard

Time to build a Tkinter app from scratch. The goal: a small dashboard that shows simulated rocket telemetry — altitude, velocity, fuel — updating live.

**Required:**

1. A Tkinter window with three labels: Altitude, Velocity, Fuel.
2. A `Start` button that begins a simulated launch.
3. Internally, a "physics" loop running on a Tk `.after(...)` callback every 100ms. (Don't use `time.sleep` in the GUI thread — it freezes the window.)
4. Each tick: integrate altitude/velocity, decrement fuel, update the labels.
5. Print one line of telemetry per tick to stdout, e.g. `tick: t=0.1, alt=0, v=2.5, fuel=199.85`.
6. Stop the simulation when fuel runs out.

**Bonus:**

- Add a tiny matplotlib FigureCanvasTkAgg embedded in the window plotting altitude vs. time live.
- Add an `Abort` button.
- Add a "Mission Time" digital clock in the corner.

This is a long, hands-on capstone. Take your time; build piece by piece.

**Tkinter primer (very short):**

```python
import tkinter as tk
root = tk.Tk()
root.title("Mission Control")

label = tk.Label(root, text="Altitude: 0 m", font=("Consolas", 14))
label.pack()

def tick():
    label.configure(text="Altitude: 5 m")
    root.after(100, tick)   # schedule next tick in 100ms

root.after(100, tick)
root.mainloop()
```

For grading, the starter version runs *headless* (no `mainloop`) and just prints telemetry — that's enough. To actually use it interactively, run `python <file>.py` from your terminal outside the app.
""",
    starter_code='''"""Mission Control Dashboard (headless smoke version).

For the in-app grader we run a short headless simulation and print telemetry.
For the real interactive version, paste this into a .py file and uncomment
the Tkinter section at the bottom — then `python that_file.py`.
"""
import math

# --- Sim (headless) ---------------------------------------------------------
def simulate(steps: int = 30, dt: float = 0.1):
    g = 9.81
    thrust_accel = 30.0      # m/s^2 above gravity, while burning
    fuel = 200.0
    flow = 1.5               # kg/s, but here we just decrement fuel like a budget
    h = 0.0
    v = 0.0
    t = 0.0
    for _ in range(steps):
        a = (thrust_accel - g) if fuel > 0 else -g
        v += a * dt
        h = max(0.0, h + v * dt)
        if fuel > 0:
            fuel -= flow * dt
        t += dt
        print(f"tick: t={t:.1f}, alt={h:.1f}, v={v:.1f}, fuel={fuel:.1f}")
        if h <= 0 and v < 0:
            break

simulate()

# --- Tkinter UI (paste into a .py file outside the app to actually run it) -
INTERACTIVE = """
import tkinter as tk
import math

root = tk.Tk()
root.title("Mission Control")
root.configure(bg="#0b1020")

style = {"font": ("Consolas", 14), "bg": "#0b1020", "fg": "#5cb8ff"}

altitude_var = tk.StringVar(value="Altitude: 0.0 m")
velocity_var = tk.StringVar(value="Velocity: 0.0 m/s")
fuel_var     = tk.StringVar(value="Fuel:     200.0 kg")

tk.Label(root, textvariable=altitude_var, **style).pack(anchor="w", padx=20, pady=6)
tk.Label(root, textvariable=velocity_var, **style).pack(anchor="w", padx=20, pady=6)
tk.Label(root, textvariable=fuel_var,     **style).pack(anchor="w", padx=20, pady=6)

state = {"running": False, "h": 0.0, "v": 0.0, "fuel": 200.0, "t": 0.0}

def step():
    if not state["running"]:
        return
    g = 9.81
    thrust_accel = 30.0
    flow = 1.5
    dt = 0.1
    a = (thrust_accel - g) if state["fuel"] > 0 else -g
    state["v"] += a * dt
    state["h"]  = max(0.0, state["h"] + state["v"] * dt)
    if state["fuel"] > 0:
        state["fuel"] -= flow * dt
    state["t"] += dt
    altitude_var.set(f"Altitude: {state['h']:.1f} m")
    velocity_var.set(f"Velocity: {state['v']:.1f} m/s")
    fuel_var.set(f"Fuel:     {state['fuel']:.1f} kg")
    if state["h"] <= 0 and state["v"] < 0:
        state["running"] = False
        return
    root.after(100, step)

def start():
    state["running"] = True
    root.after(100, step)

tk.Button(root, text="Start", command=start, font=("Segoe UI", 12), bg="#2c6da3", fg="white").pack(pady=8)
root.mainloop()
"""
''',
    checks=[
        PredicateOnStdout(_has_dashboard_loop, label="Headless telemetry tick output"),
    ],
    bonus_objectives=[
        "Embed a live matplotlib chart with FigureCanvasTkAgg.",
        "Add an Abort button that cuts the engine.",
        "Add a hold-and-drop physics: hold = engines on, release = engines off.",
    ],
    hints=[
        "Tkinter's golden rule: NEVER block the main loop. Use root.after(ms, fn) to schedule work.",
        "The physics is just Module 18's Euler step.",
        "Build it bit by bit: get one label updating once, then make it tick, then add the rest.",
    ],
    resources=[
        Resource("Tkinter docs", "https://docs.python.org/3/library/tkinter.html"),
        Resource("FigureCanvasTkAgg example", "https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html"),
    ],
    xp=800,
)


def _check_propagator(stdout: str) -> tuple[bool, str]:
    if "orbit complete" not in stdout.lower():
        return False, "Expected an 'orbit complete' line at the end of the simulation."
    return True, ""


PROPAGATOR = Project(
    id="fp_propagator",
    title="Capstone 5 — Two-Body Orbital Propagator",
    summary="Numerically integrate Newton's law of gravity in 2D and watch a satellite trace an orbit.",
    brief="""# Mission brief — propagate an orbit

Your task: given a satellite's initial position and velocity around Earth, integrate Newton's gravity equations forward in time and trace the resulting orbit.

**Physics.**

```
r_vec  = position vector from Earth's center      (m)
r_mag  = |r_vec|                                  (m)
a_vec  = -mu * r_vec / r_mag^3                    (m/s^2)
v_vec += a_vec * dt
r_vec += v_vec * dt
```

This is just F = ma where F is gravity. In 2D, vectors are (x, y).

**Required:**

1. Start the satellite at (R_earth + 408 km, 0) moving "up" at 7.66 km/s — that's a circular ISS orbit.
2. Integrate forward for one full period (~5560 s) using dt = 1 s.
3. Plot the trajectory; it should look like a circle. Save as `orbit.png`.
4. Print "orbit complete" at the end.

**Why Euler is good enough here (barely):** Pure Euler accumulates energy errors. For one orbit it'll be visually fine. For 100 orbits it'll spiral. Welcome to numerical methods.

**Bonus.**

- Use `scipy.integrate.solve_ivp` with RK45 instead of Euler. Compare.
- Try elliptical initial conditions: same position, but velocity = 9 km/s. Watch what happens.
- Try escape: velocity = 12 km/s. Now you need a much longer t_max.
- Add a second body (a moon) and see what 3-body chaos looks like.

**Why this matters.** Everything above this — Hohmann calculations, ISS tracking, lander descent — assumes idealized two-body gravity. Real spacecraft software propagates positions exactly like this, with stiffer integrators, J2 perturbations, atmospheric drag, third-body gravity, solar radiation pressure...
""",
    starter_code='''"""Two-body propagator: a satellite around Earth, in 2D, with simple Euler."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

mu = 3.986e14
R_earth = 6378e3
alt = 408e3

# Initial state: at +x edge, moving in +y at circular speed
r0 = np.array([R_earth + alt, 0.0])
v0 = np.array([0.0, math.sqrt(mu / np.linalg.norm(r0))])

dt = 1.0          # seconds
T_total = 5560    # one ISS orbital period
steps = int(T_total / dt)

xs = np.zeros(steps)
ys = np.zeros(steps)
r = r0.copy()
v = v0.copy()

for i in range(steps):
    rmag = np.linalg.norm(r)
    a = -mu * r / rmag**3
    v = v + a * dt
    r = r + v * dt
    xs[i] = r[0]
    ys[i] = r[1]

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(xs/1e3, ys/1e3, "-", color="tab:cyan", linewidth=1)
# Earth
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(R_earth/1e3 * np.cos(theta), R_earth/1e3 * np.sin(theta), color="tab:blue")
ax.fill(R_earth/1e3 * np.cos(theta), R_earth/1e3 * np.sin(theta), alpha=0.15, color="tab:blue")
ax.set_aspect("equal")
ax.set_xlabel("x (km)"); ax.set_ylabel("y (km)")
ax.set_title("Two-body propagated orbit (one period)")
ax.grid(alpha=0.3)
fig.savefig("orbit.png")
print("saved: orbit.png")
print("orbit complete")
''',
    checks=[
        PredicateOnStdout(_check_propagator, label="One-orbit propagation completes"),
    ],
    bonus_objectives=[
        "Replace Euler with scipy.integrate.solve_ivp (RK45). Compare orbital drift after 50 orbits.",
        "Try elliptical initial conditions and overlay both orbits.",
        "Add a perturbation (e.g., +1% gravity to fake a J2 effect) and see how the orbit changes.",
    ],
    hints=[
        "Use NumPy arrays for r and v — saves you from writing component-wise math.",
        "Don't forget r is a vector; rmag is its magnitude (np.linalg.norm).",
        "Reduce dt if your orbit doesn't close. dt=1s is on the edge for 1 orbit.",
    ],
    resources=[
        Resource("scipy.integrate.solve_ivp docs", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html"),
        Resource("Numerical Recipes (classic)", "https://numerical.recipes/"),
        Resource("JPL Horizons (cross-check with real ephemeris)", "https://ssd.jpl.nasa.gov/horizons/"),
    ],
    xp=900,
)


CAPSTONES_B = [ISS_TRACKER, DASHBOARD, PROPAGATOR]
