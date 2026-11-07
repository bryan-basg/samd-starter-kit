#!/usr/bin/env python3
"""CI gate: fail the build when the backend mutation score drops below a threshold.

Part of the {{PROJECT_NAME}} SaMD {{SAMD_CLASS}} testing package
(backend stack: {{BACKEND_STACK}}).

SaMD Class B (IEC 62304 5.7) requires demonstrable verification. A passing
unit suite proves the code runs; a mutation score proves the tests actually
*assert* behavior. This script reads the result of a completed `mutmut run`
and exits non-zero if the surviving-mutant ratio pushes the score under the
configured floor, so CI blocks regressions in test rigor.

Source of truth: the SQLite cache (`.mutmut-cache`) that mutmut 2.x leaves
behind, table `Mutant`, column `status`. We do NOT parse the human text of
`mutmut results`: in 2.5.1 that text lists only survived / suspicious /
timed-out / untested mutants and never the killed ones, so a text parser sees
`killed = 0` and reports a score near 0% on a healthy suite (and "no scorable
mutants" on a perfect one) -- a gate that can never go green.

Mutant.status values (mutmut 2.x):
    ok_killed      detected by the suite                      -> caught
    bad_timeout    detected by timeout                        -> caught
    bad_survived   NOT detected                               -> escaped
    ok_suspicious  slowed the suite down, not reliably caught -> escaped
    skipped        excluded from the score
    untested       not run yet; excluded from the score
    (anything else is counted as escaped: the conservative reading)

Mutation score = caught / (caught + escaped)

Configuration (all via environment variables, with safe defaults):
    MUTMUT_SCORE_THRESHOLD   Minimum acceptable score, percent.   Default: 80.0
    MUTMUT_CACHE             Path to the mutmut cache db.         Default: .mutmut-cache

Exit codes:
    0  score >= threshold
    1  score <  threshold  (gate failed)
    2  could not determine the score (no cache / unreadable / no scorable mutants)

Usage:
    MUTMUT_SCORE_THRESHOLD=85 python scripts/check_mutmut_score.py
"""

from __future__ import annotations

import os
import sqlite3
import sys
from contextlib import closing
from dataclasses import dataclass

_CAUGHT_STATUSES = {"ok_killed", "bad_timeout"}
_ESCAPED_STATUSES = {"bad_survived", "ok_suspicious"}
_EXCLUDED_STATUSES = {"skipped", "untested"}


@dataclass(frozen=True)
class MutationTotals:
    """Bucketed mutant counts read from the mutmut cache."""

    killed: int
    survived: int
    suspicious: int
    timeout: int
    skipped: int  # skipped + untested: excluded from the score
    unknown: int = 0  # statuses this script does not know: counted as escaped

    @property
    def caught(self) -> int:
        """Mutants the test suite detected (killed outright or via timeout)."""
        return self.killed + self.timeout

    @property
    def escaped(self) -> int:
        """Mutants that slipped past the suite (alive, ambiguous or unknown)."""
        return self.survived + self.suspicious + self.unknown

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


def read_totals(cache_path: str) -> MutationTotals:
    """Count mutants by status straight from the mutmut SQLite cache.

    Raises RuntimeError if the cache is missing or cannot be read.
    """
    if not os.path.exists(cache_path):
        raise RuntimeError(
            f"mutmut cache not found at {cache_path!r}; run `mutmut run` first"
        )
    try:
        with closing(sqlite3.connect(cache_path)) as con:
            rows = con.execute(
                "SELECT status, COUNT(*) FROM Mutant GROUP BY status"
            ).fetchall()
    except sqlite3.Error as exc:
        raise RuntimeError(f"cannot read table Mutant from {cache_path!r}: {exc}") from exc

    counts = {str(status): int(n) for status, n in rows}
    known = _CAUGHT_STATUSES | _ESCAPED_STATUSES | _EXCLUDED_STATUSES
    unknown = {s: n for s, n in counts.items() if s not in known}
    if unknown:
        print(f"::warning:: unknown mutmut statuses (counted as escaped): {unknown}")
    return MutationTotals(
        killed=counts.get("ok_killed", 0),
        survived=counts.get("bad_survived", 0),
        suspicious=counts.get("ok_suspicious", 0),
        timeout=counts.get("bad_timeout", 0),
        skipped=sum(counts.get(s, 0) for s in _EXCLUDED_STATUSES),
        unknown=sum(unknown.values()),
    )


def main() -> int:
    threshold = _read_float_env("MUTMUT_SCORE_THRESHOLD", 80.0)
    cache_path = os.environ.get("MUTMUT_CACHE", ".mutmut-cache")

    try:
        totals = read_totals(cache_path)
    except RuntimeError as exc:
        print(f"::error:: cannot determine mutation score: {exc}")
        return 2

    if totals.scored == 0:
        print(
            "::error:: no scorable mutants found (empty cache, or all skipped/untested); "
            "was `mutmut run` executed and did the runner actually run the tests?"
        )
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
