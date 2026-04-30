"""Build a single-file Windows executable with PyInstaller.

Usage:
    pip install pyinstaller
    python build_exe.py

Output:  dist/MissionPython.exe
"""
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is not installed. Run:  pip install pyinstaller")
        return 1

    root = Path(__file__).parent
    for d in ("build", "dist"):
        p = root / d
        if p.exists():
            shutil.rmtree(p)
    for spec in root.glob("*.spec"):
        spec.unlink()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "MissionPython",
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--collect-all", "app",
        "run.py",
    ]
    print("Building:", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
