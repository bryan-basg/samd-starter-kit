# Changelog

Todos los cambios notables de este proyecto se documentan acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el versionado sigue [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Added
- **13 Skills formales en `.claude/skills/*/SKILL.md`** (contraparte del punto anterior): el kit mantiene dos formatos por procedimiento — comando de barra (`.claude/commands/`) y Skill auto-descubrible (`.claude/skills/`), como ya mostraba `samd-trace`. Las 13 skills nuevas solo tenían el lado comando; se generó el lado Skill para las 13, con `description` enriquecida para auto-descubrimiento y sin `argument-hint`/`$ARGUMENTS` (exclusivos del formato comando). Verificado con `scripts/lint_agents.py` (27/27 artefactos en verde).
- **13 skills nuevas en `.claude/commands/`** portadas y generalizadas desde el proyecto de referencia que originó el kit: `anti-drift`, `captura-sin-login`, `cierre-bloque`, `ci-rojo`, `diagnostico-prod-no-se-ve`, `diagnostico-state-leak`, `matar-mutantes`, `mesa-ingenieros`, `ola-mutation` (metodología pura) + `arrancar-stack-local`, `diagnostico-cloud`, `rotar-secreto-prod`, `migracion-manual-db` (recetas técnicas, generalizadas de stack concreto a `{{CLOUD_STACK}}`/`{{DB_STACK}}`). Los agentes `backend`, `cloud-ops`, `docs-dhf`, `frontend`, `qa-mutation` y `security-samd` ganaron reglas nuevas destiladas de incidentes reales (generalizadas a su principio de ingeniería, sin nombres de producto/incidente). `CLAUDE.md` reestructurado: 3 bloques procedimentales condensados a regla corta + puntero a su skill.
- **Auto-auditoría del kit** (IEC 62304 §5.7 — el kit se verifica a sí mismo): `scripts/lint_agents.py` (valida que cada agente/comando/skill de `.claude/` tenga el frontmatter mínimo `name`/`description`/`tools`; sin deps — usa `pyyaml` si está, si no parsea a mano; exit 1 ante cualquier fallo), `.kit-version` (versión del kit en texto plano, fuente para `kit_upgrade`), `scripts/kit_upgrade.sh` (agrega el remote `kit-upstream`, hace fetch y muestra los cambios del kit que un proyecto derivado aún no tiene —excluyendo rutas personalizadas como `app/`, `frontend/src/`, `docs/`— sin aplicar nada; el dueño revisa antes de mergear), y los workflows `kit-quality.yml` (corre el lint de agentes + el link-checker cross-doc en cada push/PR) y `release.yml` (al pushear un tag `v*`, extrae las notas de la versión desde `CHANGELOG.md` y crea el GitHub Release).
- **Experiencia de desarrollo (DX)**: devcontainer reproducible, `docker-compose` para el stack local, `Makefile` con los atajos canónicos, guard de placeholders (evita commitear `{{...}}` sin resolver) y roadmap del kit.
- **Workflows extraídos** (generalizados, sin marca/secretos): `project-state-audit.yml` (foto semanal del estado → Issue, envuelve `audit_project_state.sh`), `openapi-contract.yml` (gate de drift del contrato, envuelve `verify_openapi_sync.py`; se saltea solo sin backend/contrato), `stale.yml` (cierra PRs abandonados), y `deploy.yml` (PLANTILLA de deploy SaMD: migrar-antes-de-publicar + abortar-si-falla + secretos desde el gestor; no-op hasta `DEPLOY_ENABLED=true`).
- **Scripts extraídos** (generalizados, parametrizados por env): `check_translations.py` (auditor i18n — paridad + "copiado sin traducir"; lo referencia el agente i18n y antes no existía), `check_coverage.sh` (cobertura canónica con doble piso global + capa datos/SQL), `run_pytest_postgres.sh` (suite contra Postgres real, self-contained con docker), `run_zap_dast.sh` (DAST OWASP ZAP), `run_mutmut.sh` (mutación backend + gate), `run_act.sh` (correr Actions localmente).
- **Esqueleto ejecutable** en `app/` (FastAPI) + `frontend/` (Vite + React + TS) + `tests/`: slice mínimo que cablea las reglas duras en código real — identidad solo del token (JWT), cifrado AES-256-GCM en reposo, aislamiento por dueño, fail-safe 503 + Retry-After, handler global sin traceback, UI plana/accesible con `prefers-reduced-motion`. Corre sin infra (store en memoria). Verificado: `pytest` 16/16 + mypy estricto + ruff; `vitest` 5/5 + build de producción. `requirements.txt` / `requirements-dev.txt` añadidos.
- **`GETTING_STARTED.md`**: guía de arranque guiada (primer día) con árbol de decisión de clase A/B/C en Mermaid, los 4 documentos base en orden, el ciclo diario con los agentes y un mapa "leé por clase" para no ahogarse en las 40+ plantillas.
- **`docs/04_user_documentation/`** (tapa el hueco de numeración 00–09): `USER_GUIDE.md` (manual de usuario final) y `RELEASE_NOTES_TEMPLATE.md`, enlazados en el índice del DHF — información de seguridad IEC 62366-1.
- Diagrama "cómo encajan las piezas" (Mermaid) en ambos READMEs + enlace prominente a la guía de arranque.
- Equipo de agentes ampliado a 10: `i18n-translations` (internacionalización) y `mobile-native` (capa nativa móvil).
- Capa de experiencia de ingeniería (`docs/09_engineering_experience/`): lecciones de producción, arquitectura de referencia y método multi-agente "Mesa de Ingenieros".
- Índice navegable del DHF (`docs/README.md`) con enlace a cada documento + pie de navegación en cada doc.
- Ejemplo trabajado (`examples/auralog/`): dispositivo Clase B ficticio con su DHF rellenado (Master Map, clasificación de seguridad, matriz de riesgo, trazabilidad).
- Diagramas de arquitectura en **Mermaid** (render nativo en GitHub) en Master Map, Architecture Overview y Reference Architecture.
- `dependabot.yml` (npm + pip + github-actions), `CODEOWNERS`, `.editorconfig`, `.gitattributes`.
- **Tooling de testing + gates**: `frontend/stryker.conf.json`, `scripts/check_mutmut_score.py` (gate de mutation), `scripts/run_flaky_check.sh`, `pytest.ini`, `.coveragerc`, workflow `db-tier.yml` (Postgres real), guía `TESTING_TOOLS.md`.
- **Stack de seguridad**: `scripts/generate_sbom.sh`, `scripts/run_gitleaks.sh` + `.gitleaks.toml`, workflows `sbom.yml` / `schemathesis.yml` / `dast.yml`, docs `SBOM_MANAGEMENT_PLAN.md` y `COMPLIANCE_CHECKLIST.md`.
- **Configs de calidad**: `.pre-commit-config.yaml`, `.mypy.ini`, `pyproject.toml` (ruff + vulture), `frontend/tsconfig.json`, `frontend/.eslintrc.cjs`, `scripts/audit_hallucinations.py`, `scripts/audit_smells.py`, `scripts/verify_openapi_sync.py`.
- **Docs regulatorios**: `RISK_CONTROL_TRACEABILITY.md`, `REGULATORY_VERSION_LOG.md`, `ISO_13485_READINESS_PLAN.md`, `CRITICAL_MODULES_INVENTORY.md`, `BREACH_NOTIFICATION_TEMPLATE.md`, `INCIDENT_POSTMORTEM_TEMPLATE.md`, `INCIDENT_RESPONSE_DRILL_REPORT.md`.
- Wrappers de comandos canónicos: `scripts/run_{stryker,trivy,semgrep,schemathesis}.sh`.
- `CHANGELOG.md`.

### Security
- **Fail-safe de secretos en el arranque** (ISO 14971 + IEC 62304 §5.4): el esqueleto ya NO degrada en silencio a una postura insegura. `app/core/config.py` expone `Settings.insecure_default_secrets()` y `app/main.py` corre un guard en el `lifespan` de FastAPI que **aborta el arranque** si la app intenta *servir* (uvicorn) fuera de `TESTING` con la `SECRET_KEY`/`ENCRYPTION_KEY` de dev públicas. El guard se dispara al servir, no al importar: tests, export de OpenAPI y tooling que solo importan la app quedan intactos.
- **Tokens de sesión con expiración** (`app/core/security.py`): `create_access_token` ahora emite `exp` + `iat`; un token sin `exp` que se filtra valía para siempre. TTL configurable vía `ACCESS_TOKEN_EXPIRE_MINUTES` (default 30). `jwt.decode` rechaza el `exp` vencido → 401 con mensaje empático. Nuevos tests: token vencido rechazado + guard fail-safe (aborta con defaults / pasa con secretos reales / se salta en TESTING).

### Fixed
- **Números de verificación desincronizados**: los READMEs, `GETTING_STARTED.md`, `CHANGELOG.md`, `app/README.md` y `tests/README.md` anunciaban `pytest 8/8` cuando la suite ya colectaba más tests. Corregido a `16/16` (real hoy). El propio kit predica "reportá números reales" — este era el contraejemplo.
- **`dast.yml` tiraba su evidencia a la basura**: el workflow subía el reporte desde `audit/…` pero `run_zap_dast.sh` lo escribe en `reports/dast/…`. Rutas alineadas → el artefacto DAST ahora sí se captura (trazabilidad SaMD §5.7).
- **Versión de `upload-artifact` contradictoria**: el mismo repo referenciaba la acción como `@v7` (nightly-mutation, db-tier) y como SHA pineado a `v4.4.0` (sbom, schemathesis, dast). Unificado al SHA pineado `v4.4.0` en los 5 usos (verificable + coherente con la postura de pineo por SHA).
- **`frontend/index.html`** declaraba `lang="en"` con la UI en español (viola WCAG 3.1.1). Corregido a `lang="es"`.
- **`requirements.txt`** usaba rangos `>=` sin techo → una instalación fresca de CI podía traer un major incompatible y romper la suite. Añadidos techos conservadores (`<` al próximo major) para reproducibilidad de build/SBOM en un contexto regulado.
- **Mutation testing del frontend — promesa oculta rota**: `stryker.conf.json` (gate `break: 90`) daba a entender que el ≥90% corría hoy, pero el motor no estaba instalado y `npx stryker` fallaría no-interactivo. Documentado como **opt-in explícito** en `frontend/README.md` (instalás el motor que matchee tu vitest y corrés `npx stryker run`). Deliberadamente NO se agrega Stryker al esqueleto desechable: hoy arrastra un CVE crítico en su árbol transitivo (v8) o fuerza un bump en cascada de vitest (v9) — deuda mayor que la que quita.

### Fixed (previo)
- **`.mypy.ini`** venía roto de fábrica: el placeholder `python_version = <3.12>` y comentarios en la misma línea que el valor (`clave = True   # …`) hacían que mypy no parseara la config. Corregido a `python_version = 3.12`, comentarios movidos a su propia línea y secciones de override de ejemplo comentadas (cero ruido). Ahora `mypy` pasa estricto out-of-the-box.

### Changed
- **Sync de reglas desde el proyecto de referencia (2026-07-05)**: (1) `CLAUDE.md` — Boy Scout pasa de obligatorio-por-archivo a oportunista (la versión obligatoria empujaba refactors de más en fixes puntuales); (2) `CLAUDE.md` + `COMPLETE_TESTING_STRATEGY.md` — el umbral de mutation score del frontend deja de ser un ≥90% GLOBAL y pasa a ≥90% solo en módulos clínicos/críticos con un piso de ≥75% en el resto (sostener 90% también en pantallas sin riesgo clínico costaba más de lo que protegía). Nuevo comando+skill `commit-selectivo-parcial` (generalizado de una skill de i18n del proyecto de referencia): des-mezclar un archivo compartido (locale, config generada, contrato) entreverado con una sesión paralela.
- **`docs/.../TESTING_TOOLS.md`**: rellenados los comandos `<...>` ahora que los scripts existen (DAST, SAST, fuzz, SCA, cobertura, mutación backend, Postgres tier) + inventario de scripts del paquete de testing actualizado.
- **`.gitignore`**: ignora `reports/`, `.coverage*` y `.secrets` (artefactos de DAST/cobertura y secretos locales de `act`).
- **`pytest.ini`**: ignore angosto para la deprecación de `httpx` que emite el `TestClient` de Starlette (ruido de terceros; `filterwarnings = error` la convertía en fallo).
- **`scripts/init_kit.sh`**: valida la clase de seguridad (A/B/C, normaliza mayúsculas; en `--yes` aborta si es inválida), muestra un ejemplo por campo en cada prompt e imprime los próximos pasos concretos según la clase elegida.
- Normalizada la convención de relleno en las plantillas: el "completar después" usa `<...>`; `{{...}}` queda reservado para los 9 marcadores que rellena `init_kit.sh`.
- READMEs sin emojis decorativos en los encabezados (look más sobrio para público regulatorio). Los marcadores de estado ✅/⚠️ del DHF se conservan.

## [1.0.0] - 2026-06-28

### Added
- **Equipo de 8 agentes** especializados (`backend`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `security-samd`, `samd-audit-trace`, `docs-dhf`).
- **Reglamento del agente** (`CLAUDE.md`): Regla 0 (SaMD prioridad absoluta), orquestación multi-agente, testing.
- **Comando + skill `samd-trace`**: análisis de impacto IEC 62304 §5.6.
- **Workflow multi-agente `samd-review`**: revisión por dimensiones de riesgo con verificación adversarial.
- **Protocolo de desarrollo** agnóstico al agente y estructura de memoria persistente.
- **Design History File**: 30+ plantillas regulatorias (ISO 14971, trazabilidad SaMD, IEC 62304 plan/clasificación/SOUP/mantenimiento, evaluación/validación clínica, post-market, IFU, privacidad, configuración, runbooks).
- **3 RFCs de ejemplo** rellenos (cifrado en reposo, identidad JWT-only, scheduler externo).
- **CI/CD funcional** sobre stack de referencia: `ci.yml`, `security-audit.yml` (Trivy+Semgrep), `nightly-mutation.yml` (Stryker).
- **Archivos de comunidad**: Contributing, Security policy, Code of Conduct, plantillas de issues/PR.
- README bilingüe (EN/ES) con badges, scaffolding (`frontend/`/`app/`/`tests/`) y scripts (`init_kit`, `check_doc_links`, `run_local_ci`, `sast`, `export_openapi`).

[Unreleased]: https://github.com/bryan-basg/samd-starter-kit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/bryan-basg/samd-starter-kit/releases/tag/v1.0.0
