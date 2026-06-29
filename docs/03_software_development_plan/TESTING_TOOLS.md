**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

# Guía maestra del stack de testing

Esta guía es la fuente única sobre **qué herramienta verifica qué**, **cuándo
corre** y **con qué comando** en {{PROJECT_NAME}}. El uso previsto del producto
es: {{INTENDED_USE}}. La clase SaMD {{SAMD_CLASS}} (IEC 62304 §5.7) exige
verificación demostrable: un test que solo "renderiza sin crashear" no es
verificación — exigimos aserciones sobre valores, llamadas y efectos
secundarios.

Stacks de referencia:

- Frontend: {{FRONTEND_STACK}}
- Backend: {{BACKEND_STACK}}
- Datos: {{DB_STACK}}
- Nube / CI: {{CLOUD_STACK}}

Idioma de trabajo del equipo: {{CHAT_LANG}}.

---

## 1. Tabla del stack

| Herramienta | Qué verifica | Cuándo corre | Comando |
|---|---|---|---|
| **Unit — frontend** (Vitest) | Lógica de componentes/hooks/servicios con aserciones específicas (no humo). | En cada cambio de frontend; gate de PR. | `npm test` |
| **Unit — backend** (pytest) | Routers, services, reglas de negocio, fail-safe; async en `asyncio_mode = auto`. | En cada cambio de backend; gate de PR. | `pytest -ra` |
| **Coverage — backend** (coverage.py) | Cobertura de líneas/ramas; gate ≥95% global (+ piso por capa datos/SQL). Reproducible, en paralelo. | Gate de PR backend; nightly. | `bash scripts/check_coverage.sh` |
| **Mutation — frontend** (Stryker) | Que los tests *maten* mutantes (no solo cubran líneas); gate `break ~90`. | Nightly/semanal incremental; full periódico. Nunca en paralelo con agentes que escriben tests. | `npx stryker run` |
| **Mutation — backend** (mutmut) | Igual que Stryker, en Python; gate de score por env var. | Nightly/semanal incremental. | `bash scripts/run_mutmut.sh` |
| **DB tier** (pytest @ Postgres + pgvector) | Comportamiento real del motor (asyncpg, pgvector, defaults SQL) que SQLite oculta. | Al tocar `app/models`/migraciones; cron 3×/sem; `workflow_dispatch`. | `bash scripts/run_pytest_postgres.sh` (o `.github/workflows/db-tier.yml`) |
| **SAST** (analizador estático de seguridad) | Vulnerabilidades en código Python+TS, secretos hardcodeados, patrones inseguros. | Nightly; gate de PR sobre archivos tocados. | `bash scripts/run_semgrep.sh` |
| **DAST** (escáner dinámico, OWASP ZAP) | Superficie HTTP en runtime: headers, auth, inyección, exposición. | Nightly contra entorno efímero. | `bash scripts/run_zap_dast.sh` |
| **Fuzz de API** (schemathesis contra OpenAPI) | Que cada endpoint respete su contrato OpenAPI bajo entradas adversariales. | Al cambiar el esquema/API; nightly. | `bash scripts/run_schemathesis.sh` |
| **SCA / deps** (escáner de CVEs) | CVEs en dependencias y capas de imagen Docker. | Nightly; gate de PR sobre lockfiles. | `bash scripts/run_trivy.sh` |
| **E2E** (navegador headless) | Flujos críticos de usuario de punta a punta en un navegador real. | Pre-release; nightly. | `<comando e2e>` |
| **Flaky check** (este kit) | Tests cuyo resultado verde↔rojo cambia entre corridas sin tocar código. | Cuando se sospecha inestabilidad; antes de cerrar una suite. | `FLAKY_RUNS=10 TEST_CMD="pytest -q" scripts/run_flaky_check.sh` |

> Rellená cada `<comando ...>` con el comando real del proyecto cuando
> conectes la herramienta. Los placeholders `<...>` marcan lo pendiente.

---

## 2. Reglas duras

Estas reglas no son negociables; son consecuencia directa de IEC 62304 §5.7.

1. **Mutation nunca en paralelo con agentes/tareas que escriben tests.** La
   herramienta de mutación congela la lista de tests en su *dry-run*; los
   tests nuevos creados en paralelo no entran y el score miente. Patrón
   correcto: primero los tests nuevos → suite unit verde → *entonces*
   mutación.
2. **Verificá la suite COMPLETA antes de cantar verde.** Un archivo de
   producción puede tener `*.test` y `*.mutation.test` (u otras) por
   separado; correr solo uno deja regresiones invisibles. Mocks globales con
   closure local se filtran entre tests: aislá el estado (`afterEach`
   robusto) y confirmá la corrida entera.
3. **Cobertura siempre reproducible.** No midas cobertura secuencialmente
   sobre una suite async+threaded: el tracer y el cambio de contexto
   (greenlet+thread) corrompen el data file y reportan misses fantasma. Corré
   en paralelo (`-n auto`), un data file por worker, luego `coverage combine`.
   Detalle en `.coveragerc` y `pytest.ini`.
4. **Tests rigurosos, no de humo.** Cada test asegura valores, llamadas y
   efectos concretos. "No crashea" no cuenta como verificación SaMD.
5. **Procesos pesados piden OK explícito** (mutación full, fuzz, DAST, suites
   completas, SCA de imagen): consumen mucho CPU; no se disparan implícitos.
6. **Umbrales como gate, no como adorno.** Mutación frontend `break ~90`
   (`frontend/stryker.conf.json`); mutación backend vía
   `scripts/check_mutmut_score.py` (umbral por env var, default 80);
   cobertura backend ≥95%. Si un módulo baja del umbral, se interviene antes
   de cerrar.

---

## 3. Archivos del paquete de testing en este kit

- `frontend/stryker.conf.json` — config de mutación frontend.
- `scripts/check_coverage.sh` — cobertura canónica con doble piso (global + capa datos/SQL).
- `scripts/run_mutmut.sh` + `scripts/check_mutmut_score.py` — mutación backend + gate de score.
- `scripts/run_pytest_postgres.sh` — suite contra Postgres real (self-contained, docker).
- `scripts/run_zap_dast.sh` — DAST (OWASP ZAP) contra la app corriendo.
- `scripts/check_translations.py` — auditor i18n (paridad de claves + "copiado sin traducir").
- `scripts/run_flaky_check.sh` — cazador de tests inestables.
- `scripts/run_act.sh` — corre los workflows de Actions localmente (nektos/act).
- `pytest.ini` — config de pytest + nota de cobertura reproducible.
- `.coveragerc` — config de cobertura en paralelo (greenlet+thread).
- `.github/workflows/db-tier.yml` — suite contra Postgres real + pgvector.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
