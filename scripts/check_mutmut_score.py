#!/usr/bin/env python3
"""CI gate: fail the build when the backend mutation score drops below a threshold.

Part of the {{PROJECT_NAME}} SaMD {{SAMD_CLASS}} testing package
(backend stack: {{BACKEND_STACK}}).

SaMD Class B (IEC 62304 5.7) requires demonstrable verification. A passing
unit suite proves the code runs; a mutation score proves the tests actually
*assert* behavior. This script reads the result of a completed `mutmut run`
and exits non-zero if the surviving-mutant ratio pushes the score under the
configured floor, so CI blocks regressions in test rigor.

Mutation score = killed / (killed + survived + suspicious + timeout-as-killed)
We count killed + timeout as "caught" and survived + suspicious as "escaped".

Configuration (all via environment variables, with safe defaults):
    MUTMUT_SCORE_THRESHOLD   Minimum acceptable score, percent.   Default: 80.0
    MUTMUT_CACHE             Path to the mutmut cache db.         Default: .mutmut-cache
    MUTMUT_BIN               mutmut executable.                   Default: mutmut

Exit codes:
    0  score >= threshold
    1  score <  threshold  (gate failed)
    2  could not determine the score (mutmut missing / no results / parse error)

Usage:
    MUTMUT_SCORE_THRESHOLD=85 python scripts/check_mutmut_score.py
"""

from __future__ import annotations

import os
import subprocess  # noqa: S404 - invoking the project's own mutmut, fixed argv
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class MutationTotals:
    """Bucketed mutant counts parsed from `mutmut results`."""

    killed: int
    survived: int
    suspicious: int
    timeout: int
    skipped: int

    @property
    def caught(self) -> int:
        """Mutants the test suite detected (killed outright or via timeout)."""
        return self.killed + self.timeout

    @property
    def escaped(self) -> int:
        """Mutants that slipped past the suite (alive or ambiguous)."""
        return self.survived + self.suspicious

    @property
    def scored(self) -> int:
        """Total mutants that count toward the score (skipped excluded)."""
        return self.caught + self.escaped

    @property
    def score(self) -> float:
        """Mutation score as a percentage in [0, 100]; 100.0 when none scored."""
        if self.scored == 0:
            return 100.0
        return 100.0 * self.caught / self.scored


def _read_float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"::warning:: {name}={raw!r} is not a number; using default {default}")
        return default


def _run_mutmut_results(mutmut_bin: str, cache_path: str) -> str:
    """Return the raw text of `mutmut results`.

    Raises RuntimeError if mutmut cannot be invoked or has no cache.
    """
    if not os.path.exists(cache_path):
        raise RuntimeError(
            f"mutmut cache not found at {cache_path!r}; run `mutmut run` first"
        )
    try:
        completed = subprocess.run(  # noqa: S603 - argv is fixed, no shell
            [mutmut_bin, "results"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"mutmut executable {mutmut_bin!r} not found") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"`{mutmut_bin} results` failed (exit {exc.returncode}): {exc.stderr.strip()}"
        ) from exc
    return completed.stdout


def parse_totals(results_text: str) -> MutationTotals:
    """Parse the summary line block emitted by `mutmut results`.

    mutmut prints a header like:
        Killed 123  Survived 4  Suspicious 0  Timeout 2  Skipped 1
    Field order and casing vary across versions, so we scan token pairs.
    """
    buckets = {
        "killed": 0,
        "survived": 0,
        "suspicious": 0,
        "timeout": 0,
        "skipped": 0,
    }
    tokens = results_text.replace("\n", " ").split()
    for i in range(len(tokens) - 1):
        label = tokens[i].strip(":").lower()
        if label in buckets:
            candidate = tokens[i + 1].strip("()%,")
            if candidate.isdigit():
                buckets[label] = int(candidate)
    return MutationTotals(**buckets)


def main() -> int:
    threshold = _read_float_env("MUTMUT_SCORE_THRESHOLD", 80.0)
    cache_path = os.environ.get("MUTMUT_CACHE", ".mutmut-cache")
    mutmut_bin = os.environ.get("MUTMUT_BIN", "mutmut")

    try:
        results_text = _run_mutmut_results(mutmut_bin, cache_path)
    except RuntimeError as exc:
        print(f"::error:: cannot determine mutation score: {exc}")
        return 2

    totals = parse_totals(results_text)
    if totals.scored == 0:
        print("::error:: no scorable mutants found; was `mutmut run` executed?")
        return 2

    score = totals.score
    print(
        f"Mutation score: {score:.2f}%  "
        f"(caught {totals.caught} / {totals.scored}; "
        f"survived {totals.survived}, suspicious {totals.suspicious}, "
        f"timeout {totals.timeout}, skipped {totals.skipped})"
    )
    print(f"Threshold: {threshold:.2f}%")

    if score + 1e-9 < threshold:
        print(f"::error:: mutation score {score:.2f}% is below the {threshold:.2f}% gate")
        return 1

    print("Mutation gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
