"""Guardián del gate de mutación del backend (SaMD §5.7 — verificación fiable).

Un gate que nunca puede ponerse verde, o que da verde sin haber medido, es peor que no
tenerlo. Esto ancla tres piezas que fallaron EN SILENCIO antes de existir este archivo:

1. `check_mutmut_score.py` leía el TEXTO de `mutmut results`, que en 2.5.1 no lista los
   mutantes matados: veía `killed = 0` y daba ~0 % en una suite sana. Ahora lee el cache.
2. `mutmut_pytest_runner.py`: mutmut solo da por muerto un mutante si pytest sale con 1;
   un import roto (4) o una lista vacía (5) contaban como superviviente.
3. El enchufe: `run_mutmut.sh` tiene que usar ese runner, el flag `--CI` y la MISMA
   versión que fija `requirements-dev.txt` (mutmut 3 eliminó la CLI que el script usa).
"""

import importlib.util
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load_gate(monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "check_mutmut_score", SCRIPTS / "check_mutmut_score.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # @dataclass + `from __future__ import annotations` busca el módulo en sys.modules.
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def _make_cache(path: Path, statuses: dict[str, int]) -> Path:
    """Cache mínimo con la tabla `Mutant(status)` que lee el gate."""
    with closing(sqlite3.connect(path)) as con:
        con.execute("CREATE TABLE Mutant (id INTEGER PRIMARY KEY, status TEXT)")
        for status, n in statuses.items():
            con.executemany(
                "INSERT INTO Mutant (status) VALUES (?)", [(status,)] * n
            )
        con.commit()
    return path


def _run_gate(monkeypatch, cache: Path, threshold: str = "80") -> int:
    monkeypatch.setenv("MUTMUT_CACHE", str(cache))
    monkeypatch.setenv("MUTMUT_SCORE_THRESHOLD", threshold)
    return _load_gate(monkeypatch).main()


# ── 1. El gate cuenta los MATADOS (el bug del parser de texto) ──────────────────


def test_gate_counts_killed_mutants_not_only_survivors(tmp_path, monkeypatch, capsys):
    # 2 matados + 5 sobrevivientes = 28,57 %. El parser de texto veía killed=0 → 0 %.
    cache = _make_cache(tmp_path / "c.db", {"ok_killed": 2, "bad_survived": 5})
    assert _run_gate(monkeypatch, cache) == 1
    out = capsys.readouterr().out
    assert "caught 2 / 7" in out
    assert "28.57%" in out


def test_gate_passes_when_every_mutant_is_killed(tmp_path, monkeypatch):
    # El parser de texto devolvía exit 2 («no scorable mutants») justo en el caso perfecto.
    cache = _make_cache(tmp_path / "c.db", {"ok_killed": 6})
    assert _run_gate(monkeypatch, cache) == 0


def test_gate_threshold_boundary_is_inclusive(tmp_path, monkeypatch):
    # 8 matados + 2 sobrevivientes = exactamente 80 %.
    cache = _make_cache(tmp_path / "c.db", {"ok_killed": 8, "bad_survived": 2})
    assert _run_gate(monkeypatch, cache, threshold="80") == 0
    assert _run_gate(monkeypatch, cache, threshold="80.5") == 1


def test_timeout_counts_as_caught_and_suspicious_as_escaped(tmp_path, monkeypatch):
    # 7 matados + 1 timeout = 8 atrapados; 1 sobreviviente + 1 sospechoso = 2 escapados.
    cache = _make_cache(
        tmp_path / "c.db",
        {"ok_killed": 7, "bad_timeout": 1, "bad_survived": 1, "ok_suspicious": 1},
    )
    assert _run_gate(monkeypatch, cache, threshold="80") == 0  # 8/10 = 80 %
    assert _run_gate(monkeypatch, cache, threshold="81") == 1


def test_skipped_and_untested_are_excluded_from_the_denominator(tmp_path, monkeypatch):
    cache = _make_cache(
        tmp_path / "c.db", {"ok_killed": 9, "bad_survived": 1, "skipped": 50, "untested": 50}
    )
    assert _run_gate(monkeypatch, cache, threshold="90") == 0  # 9/10, no 9/110


def test_unknown_status_counts_as_escaped_not_as_a_pass(tmp_path, monkeypatch, capsys):
    # Una versión futura de mutmut con un estado nuevo no puede inflar el score.
    cache = _make_cache(tmp_path / "c.db", {"ok_killed": 9, "estado_nuevo": 1})
    assert _run_gate(monkeypatch, cache, threshold="95") == 1
    assert "estado_nuevo" in capsys.readouterr().out


# ── 2. «No pude medir» es exit 2, nunca un verde por vacío ──────────────────────


def test_missing_cache_is_unmeasurable_not_green(tmp_path, monkeypatch):
    assert _run_gate(monkeypatch, tmp_path / "no-existe.db") == 2


def test_cache_with_only_untested_mutants_is_unmeasurable(tmp_path, monkeypatch):
    cache = _make_cache(tmp_path / "c.db", {"untested": 4, "skipped": 2})
    assert _run_gate(monkeypatch, cache) == 2


def test_unreadable_cache_is_unmeasurable(tmp_path, monkeypatch):
    garbage = tmp_path / "c.db"
    garbage.write_text("esto no es una base sqlite")
    assert _run_gate(monkeypatch, garbage) == 2


# ── 3. El runner convierte CUALQUIER fallo de pytest en «mutante muerto» ────────


def _run_runner(tmp_path: Path) -> int:
    return subprocess.run(  # noqa: S603 - argv fijo, sin shell
        [sys.executable, str(SCRIPTS / "mutmut_pytest_runner.py"), "-q", "-p", "no:cacheprovider", "."],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
    ).returncode


def test_runner_exit_0_when_the_suite_passes(tmp_path):
    (tmp_path / "test_ok.py").write_text("def test_ok():\n    assert True\n")
    assert _run_runner(tmp_path) == 0


def test_runner_exit_1_when_a_test_fails(tmp_path):
    (tmp_path / "test_ko.py").write_text("def test_ko():\n    assert False\n")
    assert _run_runner(tmp_path) == 1


def test_runner_maps_an_import_error_to_1_not_to_pytest_raw_exit(tmp_path):
    # Un mutante que rompe el import deja a pytest en exit 2/4: mutmut lo contaba vivo.
    (tmp_path / "test_boom.py").write_text("import modulo_que_no_existe\n")
    assert _run_runner(tmp_path) == 1


def test_runner_maps_an_empty_test_list_to_1(tmp_path):
    # pytest sale con 5 cuando no junta tests; sin el runner, mutmut lo contaba vivo.
    assert _run_runner(tmp_path) == 1


# ── 4. El ENCHUFE: run_mutmut.sh usa el runner, --CI y la versión fijada ────────


def _pinned_version_in_requirements() -> str:
    for line in (ROOT / "requirements-dev.txt").read_text().splitlines():
        if line.strip().startswith("mutmut=="):
            return line.split("==", 1)[1].split("#")[0].strip()
    pytest.fail("requirements-dev.txt no fija `mutmut==<versión>`")


def test_run_mutmut_sh_is_wired_to_runner_ci_flag_and_the_same_pin():
    script = (SCRIPTS / "run_mutmut.sh").read_text()
    code = "\n".join(
        line for line in script.splitlines() if not line.lstrip().startswith("#")
    )
    assert "scripts/mutmut_pytest_runner.py" in code, "run_mutmut.sh no usa el runner propio"
    assert "--runner" in code
    assert "--CI" in code, "sin --CI un error fatal queda mezclado con 'hay sobrevivientes'"
    assert "|| true" not in code, "un `|| true` se come el error fatal de mutmut"
    assert f'MUTMUT_PIN="{_pinned_version_in_requirements()}"' in script, (
        "la versión de mutmut en run_mutmut.sh y en requirements-dev.txt divergieron"
    )
    assert (SCRIPTS / "mutmut_pytest_runner.py").is_file()
    assert (SCRIPTS / "check_mutmut_score.py").is_file()
