#!/usr/bin/env bash
#
# run_flaky_check.sh — flakiness hunter for the {{PROJECT_NAME}} test suite.
#
# SaMD {{SAMD_CLASS}} (IEC 62304 5.7): a non-deterministic test is not
# verification, it is noise that hides regressions. This script runs the same
# suite N times and flags any test command whose pass/fail result is not
# stable across runs.
#
# A test is "flaky" here at the *suite* granularity: if the suite passes on
# some runs and fails on others without any code change, the run set is flaky.
# Point TEST_CMD at a single test/file/marker to bisect down to the culprit.
#
# Configuration (env vars):
#   FLAKY_RUNS   Number of times to run the suite.          Default: 10
#   TEST_CMD     The test command to execute each run.       Default: see below
#   FLAKY_LOG_DIR  Where per-run logs are written.           Default: .flaky-logs
#
# Examples:
#   # Backend ({{BACKEND_STACK}}), 20 runs:
#   FLAKY_RUNS=20 TEST_CMD="pytest -q tests/clinical" scripts/run_flaky_check.sh
#
#   # Frontend ({{FRONTEND_STACK}}):
#   TEST_CMD="npm test --silent" scripts/run_flaky_check.sh
#
# Exit codes:
#   0  every run produced the same result (stable)
#   1  results diverged across runs (flaky) OR every run failed identically
#      -> see note below; a uniformly-failing suite is a real failure, not flake
#   2  bad configuration

set -u -o pipefail

FLAKY_RUNS="${FLAKY_RUNS:-10}"
TEST_CMD="${TEST_CMD:-pytest -q}"
FLAKY_LOG_DIR="${FLAKY_LOG_DIR:-.flaky-logs}"

if ! [[ "${FLAKY_RUNS}" =~ ^[0-9]+$ ]] || [[ "${FLAKY_RUNS}" -lt 2 ]]; then
  echo "ERROR: FLAKY_RUNS must be an integer >= 2 (got '${FLAKY_RUNS}')." >&2
  exit 2
fi

mkdir -p "${FLAKY_LOG_DIR}"

echo "Flaky check: running '${TEST_CMD}' ${FLAKY_RUNS} times."
echo "Per-run logs -> ${FLAKY_LOG_DIR}/run_<n>.log"
echo

pass_count=0
fail_count=0
declare -a results=()

for ((n = 1; n <= FLAKY_RUNS; n++)); do
  log_file="${FLAKY_LOG_DIR}/run_${n}.log"
  printf 'Run %2d/%d ... ' "${n}" "${FLAKY_RUNS}"

  # Run the suite; capture combined output and the exit status.
  if bash -c "${TEST_CMD}" >"${log_file}" 2>&1; then
    results[n]="PASS"
    pass_count=$((pass_count + 1))
    echo "PASS"
  else
    results[n]="FAIL"
    fail_count=$((fail_count + 1))
    echo "FAIL (log: ${log_file})"
  fi
done

echo
echo "----------------------------------------"
echo "Summary: ${pass_count} pass / ${fail_count} fail  out of ${FLAKY_RUNS} runs"

# Stable: all runs agree.
if [[ "${fail_count}" -eq 0 ]]; then
  echo "STABLE: every run passed."
  exit 0
fi

if [[ "${pass_count}" -eq 0 ]]; then
  # Not flaky in the verde<->rojo sense; it is a consistent, real failure.
  echo "NOT FLAKY but FAILING: every run failed. Fix the failing test(s)."
  exit 1
fi

# Mixed results => flaky.
echo "FLAKY: results changed between runs (green<->red without code changes)."
echo "Run indices and their outcomes:"
for ((n = 1; n <= FLAKY_RUNS; n++)); do
  printf '  run %2d: %s\n' "${n}" "${results[n]}"
done
echo
echo "Compare a passing log against a failing one to find the unstable test, e.g.:"
echo "  diff ${FLAKY_LOG_DIR}/run_1.log ${FLAKY_LOG_DIR}/run_2.log"
exit 1
