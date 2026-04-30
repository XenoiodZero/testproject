"""Entry point: launch the Tkinter app."""
from __future__ import annotations

import sys
import traceback


def main() -> int:
    try:
        from .ui_main import MainWindow
    except ImportError as exc:
        print(f"Import failed: {exc}\n", file=sys.stderr)
        print("If tkinter is missing, install Python from python.org (Tk is included by default).",
              file=sys.stderr)
        return 2

    try:
        app = MainWindow()
        app.mainloop()
    except Exception:
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
