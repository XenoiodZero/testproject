"""Space-cadet theme: colors, fonts, level titles."""
from __future__ import annotations

# Dark space palette
BG = "#0b1020"          # deep space
BG_PANEL = "#121a33"    # mission console
BG_INSET = "#0a1228"
FG = "#e6f0ff"          # starlight
FG_MUTED = "#7e8aa8"
ACCENT = "#5cb8ff"      # ion-engine blue
ACCENT_DIM = "#2c6da3"
SUCCESS = "#4ade80"
WARNING = "#fbbf24"
ERROR = "#f87171"
GOLD = "#facc15"        # achievements
PURPLE = "#a78bfa"      # XP / level
GRID = "#1f2a44"

FONT_BODY = ("Segoe UI", 11)
FONT_BODY_BOLD = ("Segoe UI", 11, "bold")
FONT_H1 = ("Segoe UI Semibold", 22)
FONT_H2 = ("Segoe UI Semibold", 16)
FONT_H3 = ("Segoe UI Semibold", 13)
FONT_SMALL = ("Segoe UI", 9)
FONT_CODE = ("Consolas", 11)
FONT_CODE_SMALL = ("Consolas", 10)


# Level ladder. (min_xp, title, callsign emoji-ish text badge)
LEVELS = [
    (0,      "Cadet",            "[CDT]"),
    (200,    "Pilot",            "[PLT]"),
    (600,    "Flight Engineer",  "[ENG]"),
    (1200,   "Mission Specialist","[SPC]"),
    (2000,   "Payload Commander","[PYC]"),
    (3000,   "Mission Commander","[CMD]"),
    (4500,   "Astronaut",        "[AST]"),
    (6500,   "Mission Director", "[DIR]"),
    (9000,   "Chief Engineer",   "[CHF]"),
    (12000,  "Flight Director",  "[FLT]"),
]


def level_for_xp(xp: int) -> tuple[int, str, str, int, int | None]:
    """Return (level_index, title, badge, xp_into_level, xp_to_next_or_None)."""
    idx = 0
    for i, (threshold, _, _) in enumerate(LEVELS):
        if xp >= threshold:
            idx = i
        else:
            break
    threshold, title, badge = LEVELS[idx]
    if idx + 1 < len(LEVELS):
        next_threshold = LEVELS[idx + 1][0]
        return idx, title, badge, xp - threshold, next_threshold - threshold
    return idx, title, badge, xp - threshold, None
