"""Grade user code against an exercise's checks.

An exercise defines `checks`: a list of Check objects. The grader runs the code
once per check (or once total if all checks share the same input), captures
stdout, and decides pass/fail.

Three check styles are supported:

1. StdoutContains(text):       user's stdout must contain `text`.
2. StdoutEquals(text):         user's stdout (stripped) must equal `text`.
3. StdinStdout(stdin, expect): feed stdin, expect stdout to contain `expect`.
4. CallFn(snippet, expect):    append `print(repr(<snippet>))` and check output.
5. PredicateOnStdout(fn):      fn(stdout) -> (ok, message)  -- escape hatch.

Each check runs the user's code in a fresh subprocess so they're independent.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .runner import run_code


@dataclass
class CheckResult:
    ok: bool
    label: str
    detail: str = ""


class Check:
    label: str = ""

    def run(self, user_code: str) -> CheckResult:
        raise NotImplementedError


@dataclass
class StdoutContains(Check):
    text: str
    label: str = ""
    case_sensitive: bool = False

    def __post_init__(self) -> None:
        if not self.label:
            self.label = f"Output contains {self.text!r}"

    def run(self, user_code: str) -> CheckResult:
        r = run_code(user_code)
        if r.timed_out:
            return CheckResult(False, self.label, "Code timed out (15s).")
        if r.returncode != 0:
            return CheckResult(False, self.label, f"Code crashed:\n{r.stderr.strip()[:500]}")
        haystack = r.stdout if self.case_sensitive else r.stdout.lower()
        needle = self.text if self.case_sensitive else self.text.lower()
        if needle in haystack:
            return CheckResult(True, self.label)
        return CheckResult(
            False, self.label,
            f"Expected output to contain {self.text!r}.\nGot:\n{r.stdout[:400]}"
        )


@dataclass
class StdoutEquals(Check):
    text: str
    label: str = ""
    strip: bool = True

    def __post_init__(self) -> None:
        if not self.label:
            self.label = f"Output equals {self.text!r}"

    def run(self, user_code: str) -> CheckResult:
        r = run_code(user_code)
        if r.timed_out:
            return CheckResult(False, self.label, "Code timed out (15s).")
        if r.returncode != 0:
            return CheckResult(False, self.label, f"Code crashed:\n{r.stderr.strip()[:500]}")
        actual = r.stdout.strip() if self.strip else r.stdout
        expected = self.text.strip() if self.strip else self.text
        if actual == expected:
            return CheckResult(True, self.label)
        return CheckResult(
            False, self.label,
            f"Expected:\n{expected}\n\nGot:\n{actual}"
        )


@dataclass
class StdinStdout(Check):
    stdin: str
    expect_contains: str
    label: str = ""

    def __post_init__(self) -> None:
        if not self.label:
            self.label = f"With input {self.stdin.strip()!r}, output contains {self.expect_contains!r}"

    def run(self, user_code: str) -> CheckResult:
        r = run_code(user_code, stdin_text=self.stdin)
        if r.timed_out:
            return CheckResult(False, self.label, "Code timed out.")
        if r.returncode != 0:
            return CheckResult(False, self.label, f"Code crashed:\n{r.stderr.strip()[:500]}")
        if self.expect_contains.lower() in r.stdout.lower():
            return CheckResult(True, self.label)
        return CheckResult(
            False, self.label,
            f"With input {self.stdin!r}, expected output to contain {self.expect_contains!r}.\nGot:\n{r.stdout[:400]}"
        )


@dataclass
class CallFn(Check):
    """Append a probe line that prints repr(<snippet>) then check the last line."""
    snippet: str
    expect_repr: str
    label: str = ""

    def __post_init__(self) -> None:
        if not self.label:
            self.label = f"`{self.snippet}` evaluates to {self.expect_repr}"

    def run(self, user_code: str) -> CheckResult:
        probe = f"\n\nprint('__MP_PROBE__', repr({self.snippet}))\n"
        r = run_code(user_code + probe)
        if r.timed_out:
            return CheckResult(False, self.label, "Code timed out.")
        if r.returncode != 0:
            return CheckResult(False, self.label, f"Code crashed:\n{r.stderr.strip()[:500]}")
        for line in r.stdout.splitlines():
            if line.startswith("__MP_PROBE__ "):
                got = line[len("__MP_PROBE__ "):]
                if got == self.expect_repr:
                    return CheckResult(True, self.label)
                return CheckResult(False, self.label, f"Expected {self.expect_repr}, got {got}")
        return CheckResult(False, self.label, "Probe didn't run — did your code raise an error?")


@dataclass
class PredicateOnStdout(Check):
    fn: Callable[[str], tuple[bool, str]]
    label: str = "Custom check"
    stdin: str = ""

    def run(self, user_code: str) -> CheckResult:
        r = run_code(user_code, stdin_text=self.stdin)
        if r.timed_out:
            return CheckResult(False, self.label, "Code timed out.")
        if r.returncode != 0:
            return CheckResult(False, self.label, f"Code crashed:\n{r.stderr.strip()[:500]}")
        ok, msg = self.fn(r.stdout)
        return CheckResult(ok, self.label, msg if not ok else "")


def grade(user_code: str, checks: list[Check]) -> tuple[bool, list[CheckResult]]:
    """Run all checks. Return (all_passed, results)."""
    results = [c.run(user_code) for c in checks]
    return all(r.ok for r in results), results
