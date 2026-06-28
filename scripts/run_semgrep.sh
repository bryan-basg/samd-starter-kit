#!/usr/bin/env bash
# run_semgrep.sh — wrapper canónico (delega en sast.sh). Ver scripts/sast.sh.
exec bash "$(dirname "$0")/sast.sh" semgrep
