"""Module 17: Telemetry & Real Data — APIs and parsing."""
from __future__ import annotations

from ..grader import StdoutContains, StdoutEquals
from ._types import Exercise, Lesson, Module, Quiz, QuizQuestion, Resource


M17 = Module(
    id="m17_telemetry",
    title="Module 17 — Telemetry & Real Data",
    tagline="Pull live data from NASA / Open Notify. Parse it. Plot it.",
    phase="Mission Specialist",
    lessons=[
        Lesson(
            id="m17_l1",
            title="Lesson 17.1 — HTTP, JSON APIs, and the ISS",
            body="""# Talking to the internet

Real telemetry lives behind APIs. The simplest aerospace API on the planet is **Open Notify** — it tells you where the ISS is *right now*.

```python
import requests

resp = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
resp.raise_for_status()         # raise if HTTP 4xx/5xx
data = resp.json()              # parse JSON into a Python dict

print(data)
# {'iss_position': {'latitude': '12.34', 'longitude': '-56.78'},
#  'message': 'success',
#  'timestamp': 1700000000}
```

Three things to internalize:

1. `requests.get(url)` does an HTTP GET.
2. `.raise_for_status()` is your friend — it converts an HTTP error into a Python exception you can catch.
3. `.json()` parses the response body as JSON into a Python dict (or list).

## Handling failure

The internet is hostile. Wrap network calls:

```python
try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
except requests.RequestException as e:
    print(f"Network error: {e}")
    data = None
```

## Other public space APIs you'll meet

- **Open Notify ISS**: http://api.open-notify.org/iss-now.json
- **NASA APOD** (picture of the day, free demo key): https://api.nasa.gov/
- **NASA SPK / Horizons** (real ephemeris): https://ssd-api.jpl.nasa.gov/doc/horizons.html

---

**Note for exercises in this module:** the in-app subprocess may or may not have network access. So we'll use a *recorded* JSON sample for the graded exercise — same shape as the real API.
""",
            exercises=[
                Exercise(
                    id="m17_l1_e1",
                    title="Parse a recorded ISS payload",
                    prompt=(
                        "Given the JSON string below (already in starter_code), parse it with json.loads and "
                        "print exactly:\n"
                        "  ISS at lat=12.34, lon=-56.78"
                    ),
                    starter_code=(
                        "import json\n"
                        "raw = '''{\"iss_position\": {\"latitude\": \"12.34\", \"longitude\": \"-56.78\"}, \"message\": \"success\", \"timestamp\": 1700000000}'''\n"
                        "data = json.loads(raw)\n"
                        "# extract latitude and longitude (they're strings — convert if you want; here just print)\n"
                    ),
                    checks=[StdoutEquals("ISS at lat=12.34, lon=-56.78")],
                    hints=[
                        "lat = data['iss_position']['latitude']",
                        "lon = data['iss_position']['longitude']",
                        "print(f'ISS at lat={lat}, lon={lon}')",
                    ],
                    xp=30,
                ),
                Exercise(
                    id="m17_l1_e2",
                    title="Find the brightest pass",
                    prompt=(
                        "Given a list of dicts representing ISS pass times with 'duration' (s) and 'risetime' (epoch),\n"
                        "  passes = [\n"
                        "    {'duration': 322, 'risetime': 1700000000},\n"
                        "    {'duration': 612, 'risetime': 1700004000},\n"
                        "    {'duration': 158, 'risetime': 1700008000},\n"
                        "  ]\n"
                        "Find and print the duration of the longest pass. Expected: 612"
                    ),
                    starter_code=(
                        "passes = [\n"
                        "  {'duration': 322, 'risetime': 1700000000},\n"
                        "  {'duration': 612, 'risetime': 1700004000},\n"
                        "  {'duration': 158, 'risetime': 1700008000},\n"
                        "]\n"
                    ),
                    checks=[StdoutEquals("612")],
                    hints=[
                        "Try max(passes, key=lambda p: p['duration'])['duration']",
                        "Or a loop tracking best so far.",
                    ],
                    counter_keys=["loop_exercises"],
                    xp=35,
                ),
            ],
            quiz=Quiz(questions=[
                QuizQuestion(
                    "What does resp.json() do?",
                    ["Save to disk", "Parse the response body as JSON into Python types", "Print the JSON", "Convert to CSV"],
                    1,
                ),
                QuizQuestion(
                    "Why use timeout= on requests.get?",
                    ["Required syntax", "Otherwise a slow server can hang your program forever", "It's faster", "It compresses the request"],
                    1,
                ),
                QuizQuestion(
                    "Which exception type covers most network errors in `requests`?",
                    ["ValueError", "OSError", "requests.RequestException", "ConnectionError only"],
                    2,
                    "RequestException is the parent of HTTPError, ConnectionError, Timeout, etc.",
                ),
            ]),
            resources=[
                Resource("Open Notify (free, no key)", "http://open-notify.org/"),
                Resource("NASA APIs (some free with demo key)", "https://api.nasa.gov/"),
                Resource("requests docs", "https://requests.readthedocs.io/"),
            ],
            xp_on_complete=80,
        ),
    ],
)
