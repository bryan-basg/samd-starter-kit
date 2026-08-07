# COMANDOS CORE

> Regla **transversal** del cerebro SaMD, en archivo aparte solo por legibilidad del core — **NO lleva `paths:`**, así que carga en cada sesión igual que `CLAUDE.md`. Mapa completo: `CLAUDE.md` §MAPA DE ESTE CEREBRO. Guía completa de la suite: `docs/04_user_documentation/TESTING_TOOLS.md`.
>
> **Adaptá los comandos a tu stack real** (`{{FRONTEND_STACK}}` / `{{BACKEND_STACK}}`).

```bash
# Tablero de salud rápido (~1 min — el semáforo diario: verde = sintaxis/tipos/estilo OK.
# La profundidad la dan los tests de abajo. No pide OK: es barato.)
mypy .                                     # tipos backend (con el entorno virtual activo)
ruff check app/                            # lint backend
cd frontend && npm run type-check          # tipos frontend
cd frontend && npm run lint                # lint frontend

# Frontend dev y test  ({{FRONTEND_STACK}})
cd frontend && npm run dev
cd frontend && npm run test

# Backend tests y cobertura  ({{BACKEND_STACK}})
# (activá el entorno virtual / toolchain correspondiente — sin él, el intérprete del
#  sistema da errores de módulo no encontrado que despistan)
pytest -q                                  # suite
pytest --cov=app --cov-report=term-missing # cobertura canónica

# CI local pre-push
bash scripts/run_local_ci.sh

# Stack SaMD-grade (lentos — correr con OK explícito del dueño)
bash scripts/run_stryker.sh      # mutation frontend
bash scripts/run_mutmut.sh       # mutation backend
bash scripts/run_schemathesis.sh # fuzz API contra el contrato OpenAPI
bash scripts/run_trivy.sh        # CVEs deps + Docker
bash scripts/run_semgrep.sh      # SAST
bash scripts/run_zap_dast.sh     # DAST
bash scripts/run_pytest_postgres.sh # tier de BD real con docker
```

* **Higiene de procesos dev locales**: tras levantar emuladores/servidor/frontend para una prueba, matalos y liberá los puertos que hayas ocupado. Los procesos pesados (tests, mutación, cobertura) corren en la máquina local; los agentes en la nube solo razonan.
* **Procesos pesados piden OK CADA vez** (ver `.claude/rules/orquestacion.md`, regla dura 2): un "vamos con todo" cubre el plan, **no** los subprocesos pesados implícitos.
* Para levantar el stack local completo con datos de prueba sembrados, ver la skill `/arrancar-stack-local`.
