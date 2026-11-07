"""Guardián del aviso de `main` en rojo (IEC 62304 §5.7 — un gate que no avisa no es un gate).

`.github/workflows/main-en-rojo.yml` abre un Issue cuando un workflow termina en rojo en
`main`. Tiene un límite que ninguna prueba puede saltarse: `workflow_run` solo dispara
desde la versión del archivo que vive en la rama por defecto, así que **el disparo real
no se puede probar hasta que esto esté mergeado**. Lo que sí se puede — y este archivo
hace — es verificar todo lo demás:

* la ESTRUCTURA del YAML (a quién escucha, a quién ignora, permisos, concurrencia), y
* la LÓGICA del script (crear / comentar / cerrar / no hacer nada), ejecutándolo con
  `node` contra un cliente de GitHub simulado.

Lo segundo es lo que distingue una prueba de una foto del texto: cambiar `ROJO` o borrar
un `if` del script hace rojear un caso de comportamiento, no solo un `assert "x" in texto`.

Dos defensas contra el verde vacío:
* los casos de «no hizo nada» exigen haber visto la consulta de Issues abiertos
  (`paginate`): sin eso, un script vacío o que revienta pasaría todos los «no hace nada»;
* si no hay `node`, el test FALLA (no se salta): un salto aprobaría sin haber mirado.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "main-en-rojo.yml"

NOMBRE = "Main en rojo — aviso"
ETIQUETA = "main-en-rojo"

# Cliente de GitHub simulado: registra cada llamada que el script hace.
_ARNES_JS = r"""
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const llamadas = [];
const abiertos = JSON.parse(process.env.ABIERTOS_JSON);
const github = {
  paginate: async (fn, args) => { llamadas.push(['paginate', args]); return abiertos; },
  rest: { issues: {
    listForRepo: 'listForRepo',
    create: async (a) => { llamadas.push(['create', a]); return { data: { number: 99 } }; },
    createComment: async (a) => { llamadas.push(['comment', a]); },
    update: async (a) => { llamadas.push(['update', a]); },
  } },
};
const context = { repo: { owner: 'dueno', repo: 'proyecto' } };
const core = { info: () => {} };
const f = new AsyncFunction('github', 'context', 'core', process.env.SCRIPT_SRC);
f(github, context, core).then(
  () => console.log(JSON.stringify(llamadas)),
  (e) => { console.error(String(e)); process.exit(2); },
);
"""


def _workflow() -> dict[Any, Any]:
    cargado = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(cargado, dict)
    return cargado


def _disparador(wf: dict[Any, Any]) -> dict[str, Any]:
    # PyYAML (YAML 1.1) lee la clave `on` como el booleano True.
    valor = wf["on"] if "on" in wf else wf[True]
    assert isinstance(valor, dict)
    return valor


def _job() -> dict[str, Any]:
    job = _workflow()["jobs"]["avisar"]
    assert isinstance(job, dict)
    return job


def _paso() -> dict[str, Any]:
    pasos = _job()["steps"]
    assert len(pasos) == 1, "el aviso es UN paso; si crece, revisá este guardián"
    assert isinstance(pasos[0], dict)
    return pasos[0]


def _script() -> str:
    codigo = _paso()["with"]["script"]
    assert isinstance(codigo, str) and codigo.strip(), "el script del aviso está vacío"
    return codigo


def _condicion() -> list[str]:
    """Las cláusulas del `if:` del job, normalizadas (separadas por `&&`)."""
    crudo = _job()["if"]
    assert isinstance(crudo, str)
    return [" ".join(c.split()) for c in crudo.split("&&")]


# ───────────────────────── Estructura del YAML ─────────────────────────


def test_escucha_a_todos_los_workflows_al_terminar():
    """`workflows: ["*"]`: un workflow nuevo entra en la vigilancia por existir."""
    on = _disparador(_workflow())
    assert set(on) == {"workflow_run"}, "solo debe dispararse por workflow_run"
    assert on["workflow_run"]["workflows"] == ["*"]
    assert on["workflow_run"]["types"] == ["completed"]


def test_solo_mira_main_del_propio_repo():
    clausulas = _condicion()
    assert "github.event.workflow_run.head_branch == 'main'" in clausulas
    # Sin esto, un PR desde un fork cuya rama se llame `main` abriría Issues falsos.
    assert (
        "github.event.workflow_run.head_repository.full_name == github.repository"
        in clausulas
    )


def test_no_se_vigila_a_si_mismo_y_el_nombre_coincide():
    """Si este aviso fallara y se vigilara, se dispararía en bucle.

    El nombre aparece DOS veces (`name:` y el `if:`): si alguien renombra una y olvida
    la otra, la autoexclusión deja de funcionar en silencio.
    """
    wf = _workflow()
    assert wf["name"] == NOMBRE
    assert f"github.event.workflow_run.name != '{wf['name']}'" in _condicion()


def test_deja_fuera_al_robot_de_dependabot():
    assert (
        "github.event.workflow_run.path != 'dynamic/dependabot/dependabot-updates'"
        in _condicion()
    )


def test_no_quedo_ninguna_referencia_a_master():
    texto = WORKFLOW.read_text(encoding="utf-8")
    # La cabecera menciona `master` solo para explicar cómo adaptarlo.
    codigo = "\n".join(
        linea for linea in texto.splitlines() if not linea.lstrip().startswith("#")
    )
    assert "master" not in codigo.lower()


def test_concurrencia_por_workflow_id_y_nunca_por_nombre():
    """El grupo se evalúa ANTES que el `if`: un nombre largo tumba el arranque (0 jobs)."""
    conc = _workflow()["concurrency"]
    assert conc["group"] == (
        "main-en-rojo-${{ github.event.workflow_run.workflow_id }}"
    )
    # Cada aviso es la única muestra de su corrida: no se cancela a medias.
    assert conc["cancel-in-progress"] is False


def test_corre_en_runner_gestionado_con_reloj_duro():
    job = _job()
    assert job["runs-on"] == "ubuntu-latest", "un avisador no vive en la máquina que vigila"
    assert isinstance(job["timeout-minutes"], int) and job["timeout-minutes"] <= 10


def test_permisos_minimos():
    assert _workflow()["permissions"] == {"contents": "read", "issues": "write"}


def test_valores_del_evento_viajan_por_env_y_no_dentro_del_script():
    """Inyección: el nombre de un workflow es texto controlable (D-CI-…-INJECTION)."""
    paso = _paso()
    assert "${{" not in _script(), "interpolación cruda dentro de script:"
    assert paso["env"], "los valores del evento deben entrar por env:"
    assert all(re.fullmatch(r"WF_[A-Z]+", k) for k in paso["env"])
    for clave in paso["env"]:
        assert f"process.env.{clave}" in _script(), f"{clave} se declara y no se usa"


def test_usa_github_script():
    # El pineo por SHA completo lo vigila tests/test_workflows_pineados_a_sha.py.
    assert _paso()["uses"].startswith("actions/github-script@")


def test_las_conclusiones_rojas_son_exactamente_tres():
    """`timed_out` y `startup_failure` cuentan; `cancelled` NO (ruido diario)."""
    encontrado = re.search(r"const ROJO = \[([^\]]*)\]", _script())
    assert encontrado, "no se encontró la lista ROJO en el script"
    rojas = set(re.findall(r"'([a-z_]+)'", encontrado.group(1)))
    assert rojas == {"failure", "timed_out", "startup_failure"}


# ───────────────────── Lógica del script (ejecutada con node) ─────────────────────


def _ejecutar(
    conclusion: str,
    abiertos: list[dict[str, Any]],
    nombre: str = "CI",
) -> list[list[Any]]:
    node = shutil.which("node")
    assert node, (
        "Hace falta `node` para ejecutar la lógica del aviso. Sin él este guardián NO se "
        "salta: aprobaría sin haber mirado (los runners de GitHub ya lo traen)."
    )
    resultado = subprocess.run(
        [node, "-e", _ARNES_JS],
        env={
            "PATH": "/usr/bin:/bin",
            "SCRIPT_SRC": _script(),
            "ABIERTOS_JSON": json.dumps(abiertos),
            "WF_NAME": nombre,
            "WF_CONCLUSION": conclusion,
            "WF_URL": "https://example.test/run/1",
            "WF_SHA": "0123456789abcdef0123456789abcdef01234567",
            "WF_ACTOR": "alguien",
        },
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert resultado.returncode == 0, resultado.stderr
    llamadas = json.loads(resultado.stdout)
    assert isinstance(llamadas, list)
    # Guarda anti-vacío: el script TIENE que haber consultado los Issues abiertos.
    assert llamadas and llamadas[0][0] == "paginate", "el script no llegó a ejecutarse"
    return llamadas[1:]  # solo lo que hizo DESPUÉS de consultar


def _tipos(llamadas: list[list[Any]]) -> list[str]:
    return [str(c[0]) for c in llamadas]


def _previo(titulo: str, numero: int = 7) -> dict[str, Any]:
    return {"number": numero, "title": titulo}


@pytest.mark.parametrize("conclusion", ["failure", "timed_out", "startup_failure"])
def test_rojo_sin_aviso_previo_crea_el_issue(conclusion: str):
    llamadas = _ejecutar(conclusion, [])
    assert _tipos(llamadas) == ["create"]
    creado = llamadas[0][1]
    assert creado["title"] == "🔴 main en rojo — CI"
    assert creado["labels"] == [ETIQUETA]
    assert conclusion in creado["body"]


@pytest.mark.parametrize("conclusion", ["failure", "timed_out", "startup_failure"])
def test_rojo_con_aviso_previo_comenta_y_no_duplica(conclusion: str):
    llamadas = _ejecutar(conclusion, [_previo("🔴 main en rojo — CI")])
    assert _tipos(llamadas) == ["comment"], "tres rojos seguidos no son tres Issues"
    assert llamadas[0][1]["issue_number"] == 7


def test_verde_con_aviso_previo_comenta_y_cierra():
    llamadas = _ejecutar("success", [_previo("🔴 main en rojo — CI")])
    assert _tipos(llamadas) == ["comment", "update"]
    assert llamadas[1][1] == {
        "owner": "dueno",
        "repo": "proyecto",
        "issue_number": 7,
        "state": "closed",
    }


def test_verde_sin_aviso_previo_no_hace_nada():
    assert _ejecutar("success", []) == []


@pytest.mark.parametrize("conclusion", ["cancelled", "skipped", "neutral", "action_required"])
@pytest.mark.parametrize("hay_previo", [False, True])
def test_conclusiones_no_rojas_ni_verdes_no_tocan_nada(conclusion: str, hay_previo: bool):
    """`cancelled` no avisa (ruido diario) y TAMPOCO cierra un aviso abierto."""
    abiertos = [_previo("🔴 main en rojo — CI")] if hay_previo else []
    assert _ejecutar(conclusion, abiertos) == []


def test_un_aviso_de_otro_workflow_no_se_reutiliza_ni_se_cierra():
    otro = _previo("🔴 main en rojo — Backend CI")
    assert _tipos(_ejecutar("failure", [otro], nombre="CI")) == ["create"]
    assert _ejecutar("success", [otro], nombre="CI") == []


def test_consulta_y_creacion_usan_la_misma_etiqueta():
    """Si difieren, el aviso nunca se encuentra y cada rojo crea un Issue nuevo."""
    node = shutil.which("node")
    assert node
    resultado = subprocess.run(
        [node, "-e", _ARNES_JS],
        env={
            "PATH": "/usr/bin:/bin",
            "SCRIPT_SRC": _script(),
            "ABIERTOS_JSON": "[]",
            "WF_CONCLUSION": "failure",
        },
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert resultado.returncode == 0, resultado.stderr
    llamadas = json.loads(resultado.stdout)
    consulta = llamadas[0][1]
    creacion = next(c[1] for c in llamadas if c[0] == "create")
    assert consulta["labels"] == ETIQUETA
    assert creacion["labels"] == [ETIQUETA]
    assert consulta["state"] == "open"


def test_un_nombre_hostil_viaja_como_texto_y_no_se_ejecuta():
    """El nombre de un workflow es texto controlable: nunca debe correr como código."""
    hostil = "x`; process.exit(7); //${{ secrets.TOKEN }}"
    llamadas = _ejecutar("failure", [], nombre=hostil)
    assert _tipos(llamadas) == ["create"]
    assert hostil in llamadas[0][1]["title"]
