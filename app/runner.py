"""Run user-submitted Python code in a separate subprocess and capture output.

We use subprocess (not exec inside this process) so a runaway loop or a SystemExit
in user code can't take down the app. Output is streamed line by line via a queue
so the UI can show it live.
"""
from __future__ import annotations

import os
import queue
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass


@dataclass
class RunResult:
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool


class CodeRunner:
    """Runs user code in a subprocess. Use start() then poll output_queue, then wait()."""

    def __init__(self, code: str, stdin_text: str = "", timeout: float = 15.0):
        self.code = code
        self.stdin_text = stdin_text
        self.timeout = timeout
        self.output_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.proc: subprocess.Popen | None = None
        self._tmpfile: str | None = None
        self._stdout_buf: list[str] = []
        self._stderr_buf: list[str] = []
        self._timed_out = False
        self._reader_threads: list[threading.Thread] = []

    def start(self) -> None:
        fd, path = tempfile.mkstemp(prefix="mp_user_", suffix=".py")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(self.code)
        self._tmpfile = path

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"

        creationflags = 0
        if sys.platform == "win32":
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        self.proc = subprocess.Popen(
            [sys.executable, "-u", path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            creationflags=creationflags,
        )
        if self.stdin_text and self.proc.stdin:
            try:
                self.proc.stdin.write(self.stdin_text)
                self.proc.stdin.close()
            except (BrokenPipeError, OSError):
                pass

        for stream_name in ("stdout", "stderr"):
            t = threading.Thread(
                target=self._read_stream, args=(stream_name,), daemon=True
            )
            t.start()
            self._reader_threads.append(t)

        threading.Thread(target=self._watchdog, daemon=True).start()

    def _read_stream(self, name: str) -> None:
        assert self.proc is not None
        stream = getattr(self.proc, name)
        if stream is None:
            return
        try:
            for line in iter(stream.readline, ""):
                if not line:
                    break
                if name == "stdout":
                    self._stdout_buf.append(line)
                else:
                    self._stderr_buf.append(line)
                self.output_queue.put((name, line))
        except (ValueError, OSError):
            pass

    def _watchdog(self) -> None:
        if self.proc is None:
            return
        try:
            self.proc.wait(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            self._timed_out = True
            try:
                self.proc.kill()
            except OSError:
                pass

    def wait(self) -> RunResult:
        if self.proc is None:
            raise RuntimeError("CodeRunner.start() not called")
        try:
            self.proc.wait(timeout=self.timeout + 1)
        except subprocess.TimeoutExpired:
            self._timed_out = True
            self.proc.kill()
            self.proc.wait()
        for t in self._reader_threads:
            t.join(timeout=2.0)
        if self._tmpfile and os.path.exists(self._tmpfile):
            try:
                os.unlink(self._tmpfile)
            except OSError:
                pass
        return RunResult(
            stdout="".join(self._stdout_buf),
            stderr="".join(self._stderr_buf),
            returncode=self.proc.returncode if self.proc.returncode is not None else -1,
            timed_out=self._timed_out,
        )

    def kill(self) -> None:
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.kill()
            except OSError:
                pass


def run_code(code: str, stdin_text: str = "", timeout: float = 15.0) -> RunResult:
    """Convenience: run code and block until done."""
    r = CodeRunner(code, stdin_text=stdin_text, timeout=timeout)
    r.start()
    return r.wait()
