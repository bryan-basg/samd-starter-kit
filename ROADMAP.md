<div align="center">

# Roadmap — SaMD Starter Kit

**English · [Español](#roadmap--español)**

</div>

> An honest, public roadmap for the kit. The kit is a **process scaffold**, not regulatory advice and not a guarantee of certification — see the [README](README.md) for what it is and isn't. Horizons are intentionally soft ("next", "exploring"); we don't commit to calendar dates for an open-source side project.
>
> Want to shape this? Open a [feature request](.github/ISSUE_TEMPLATE/feature_request.yml), grab a [good first issue](.github/ISSUE_TEMPLATE/good_first_issue.yml), or start a [Discussion](https://github.com/bryan-basg/samd-starter-kit/discussions).

## Done

What already ships in the kit today:

- **Team of 12 agents** (`.claude/agents/`) — per-layer specialists with the SaMD ruleset pre-loaded: `backend`, `clinical-algorithms`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `e2e-integration`, `security-samd`, `samd-audit-trace`, `docs-dhf`, `i18n-translations`, `mobile-native`.
- **Agent ruleset** (`CLAUDE.md` + `.claude/rules/`) — a **core** holding Rule 0 (SaMD is the absolute priority), owner preferences, tutor mode, impact analysis and block closure; plus eight rules under `.claude/rules/`: four **path-scoped** (backend, clinical UX, testing, CI) that load only when that layer is touched, and four cross-cutting (orchestration, agents, commands, parallel sessions).
- **15 working CI/CD workflows** (`.github/workflows/`) — 11 gates the derived project inherits (CI, security audit with Trivy + Semgrep, nightly mutation, API contract fuzzing, DAST, SBOM, Postgres tier, OpenAPI contract-drift, project-state audit, stale-PR triage, and a deploy template) + 4 that maintain the kit itself (docs, quality gates, placeholder guard, release).
- **A CI that actually verifies** — the CI runs the skeleton's real checks on every push: dead imports, strict type-check and backend tests, frontend lint/types/tests, and OpenAPI contract-drift, with path filters so only the affected layers run. A green badge that never ran a test is worse than no badge.
- **One-click developer experience** — devcontainer, `docker-compose`, `Makefile`, a guided `init_kit.sh` and a placeholder guard, for a fast path from clone to a green local run.
- **Cross-framework regulatory coverage** — U.S. FDA, EU MDR, IMDRF, ISO 27001 / SOC 2 mapped to the existing DHF templates, so the kit reads cleanly beyond the EU lens.
- **Documentation site** — a browsable MkDocs Material site over `docs/`, published on GitHub Pages.
- **Public project signals** — roadmap, sponsorship template, good-first-issue path, and live CI status badges.
- **40+ document Design History File** (`docs/`) — ISO 14971 risk matrix, SaMD traceability matrix, IEC 62304 plan, safety classification, SOUP, clinical evaluation/validation, post-market surveillance, IFU, user docs, privacy, runbooks.
- **Runnable skeleton** (`app/` · `frontend/` · `tests/`) — a minimal FastAPI + React/TS example wiring the hard rules (token-only identity, AES-256-GCM at rest, fail-safe, flat accessible UI). Runs with zero infra.
- **Worked example** (`examples/auralog/`) — a fictional Class B device (AuraLog) with its DHF filled in, so you can see the kit in action.
- **Command, skill & review workflow** (`.claude/`) — `samd-trace` impact analysis (§5.6) and the `samd-review` adversarial diff review.
- **Bilingual onboarding** — `README` / `CONTRIBUTING` / `GETTING_STARTED` in English and Spanish, with a pre-certification clinical glossary so text never claims an uncertified medical-device function.

## In progress

- **Continuous distillation from the source project.** The kit was extracted from a real Class B SaMD that keeps shipping, so it drifts behind on its own — mostly in *governance* (rules, agents, skills), which is exactly what the kit sells. The ongoing work is periodically diffing that project's ruleset against this one and porting what generalizes, discarding what is stack-specific. The per-layer rule split, the clinical and E2E agents, and the parallel-session rules all came from that pass.

## Planned

Ideas we're exploring; not committed, and open to community input:

- **More worked examples** — additional fictional devices across Class A/B/C to show how the DHF scales with safety classification.
- **More languages** — extending the bilingual baseline (EN/ES) to further locales across the README, contributor docs, and the i18n tooling.
- **Integrations** — optional adapters for other secret managers, cloud platforms, and CI providers beyond the reference stack (React + TS / Python + FastAPI).
- **Agent improvements** — sharpening the specialists as the underlying models evolve, without loosening the hard rules a better model must not override.
- **Waking the dormant security gates.** Security audit, contract fuzzing and DAST ship with their triggers commented on purpose: they need a deployed app/API that the base kit doesn't have, and a gate that scans a nonexistent target passes without looking at anything. Turning them on means giving them a real target to hit — not just uncommenting a trigger.

---

<div align="center">

# Roadmap — Español

**[English](#roadmap--samd-starter-kit) · Español**

</div>

> Un roadmap público y honesto del kit. El kit es un **andamiaje de proceso**, no asesoría regulatoria ni garantía de certificación — ver el [README](README.es.md) para qué es y qué no. Los horizontes son deliberadamente blandos ("próximo", "explorando"); no comprometemos fechas de calendario para un proyecto open-source.
>
> ¿Querés influir en esto? Abrí un [feature request](.github/ISSUE_TEMPLATE/feature_request.yml), tomá un [good first issue](.github/ISSUE_TEMPLATE/good_first_issue.yml) o iniciá una [Discusión](https://github.com/bryan-basg/samd-starter-kit/discussions).

## Hecho

Lo que el kit ya trae hoy:

- **Equipo de 12 agentes** (`.claude/agents/`) — especialistas por capa con el reglamento SaMD precargado: `backend`, `clinical-algorithms`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `e2e-integration`, `security-samd`, `samd-audit-trace`, `docs-dhf`, `i18n-translations`, `mobile-native`.
- **Reglamento del agente** (`CLAUDE.md` + `.claude/rules/`) — un **core** con la Regla 0 (SaMD es prioridad absoluta), las preferencias del dueño, el modo tutor, el análisis de impacto y el cierre de bloque; más ocho reglas en `.claude/rules/`: cuatro **path-scoped** (backend, UX clínica, testing, CI) que cargan solas al tocar esa capa y cuatro transversales (orquestación, agentes, comandos, sesiones paralelas).
- **15 workflows de CI/CD funcionales** (`.github/workflows/`) — 11 gates heredables por el proyecto derivado (CI, auditoría de seguridad con Trivy + Semgrep, mutación nocturna con Stryker, fuzz del contrato de API con schemathesis, DAST con OWASP ZAP, SBOM, tier Postgres, drift del contrato OpenAPI, auditoría del estado del proyecto, triage de PRs viejos y una plantilla de deploy) + 4 de mantenimiento del propio kit (docs, gates de calidad, guard de placeholders, release).
- **Un CI que verifica de verdad** — en cada push corre los chequeos reales del esqueleto: imports muertos, type-check estricto y tests de backend, lint/tipos/tests de frontend, y drift del contrato OpenAPI, con filtros por rutas para que solo corran las capas afectadas. Un badge verde que nunca corrió un test es peor que no tener badge.
- **Experiencia de desarrollo de un clic** — devcontainer, `docker-compose`, `Makefile`, un `init_kit.sh` guiado y el guard de placeholders, para ir del clone a una corrida local en verde sin fricción.
- **Cobertura regulatoria cross-framework** — FDA (EE. UU.), MDR (UE), IMDRF e ISO 27001 / SOC 2 mapeados a las plantillas existentes del DHF, para que el kit lea bien más allá del lente europeo.
- **Sitio de documentación** — un sitio navegable MkDocs Material sobre `docs/`, publicado en GitHub Pages.
- **Señales de proyecto público** — roadmap, plantilla de sponsorship, camino de good-first-issue y badges de estado de CI en vivo.
- **Design History File de 40+ documentos** (`docs/`) — matriz de riesgo ISO 14971, matriz de trazabilidad SaMD, plan IEC 62304, clasificación de seguridad, SOUP, evaluación/validación clínica, post-market, IFU, docs de usuario, privacidad, runbooks.
- **Esqueleto ejecutable** (`app/` · `frontend/` · `tests/`) — un ejemplo mínimo FastAPI + React/TS que cablea las reglas duras (identidad solo del token, AES-256-GCM en reposo, fail-safe, UI plana y accesible). Corre sin infra.
- **Ejemplo trabajado** (`examples/auralog/`) — un dispositivo Clase B ficticio (AuraLog) con su DHF rellenado, para ver el kit en acción.
- **Comando, skill y workflow de revisión** (`.claude/`) — el análisis de impacto `samd-trace` (§5.6) y la revisión adversarial de diff `samd-review`.
- **Onboarding bilingüe** — `README` / `CONTRIBUTING` / `GETTING_STARTED` en inglés y español, con un glosario clínico pre-certificación para que ningún texto afirme una función de dispositivo médico no certificada.

## En curso

- **Destilación continua desde el proyecto de origen.** El kit se extrajo de un SaMD Clase B real que sigue en desarrollo, así que se queda atrás solo — sobre todo en *gobernanza* (reglas, agentes, skills), que es justo lo que el kit vende. El trabajo vivo es comparar cada tanto el reglamento de ese proyecto contra este y portar lo que generaliza, descartando lo que es específico de su stack. De esa pasada salieron el reparto de reglas por capa, los agentes clínico y de E2E, y las reglas de sesiones paralelas.

## Planeado

Ideas que estamos explorando; no comprometidas y abiertas a la comunidad:

- **Más ejemplos trabajados** — dispositivos ficticios adicionales en Clase A/B/C para mostrar cómo escala el DHF con la clasificación de seguridad.
- **Más idiomas** — extender la base bilingüe (EN/ES) a más locales en el README, las docs de contribución y el tooling de i18n.
- **Integraciones** — adaptadores opcionales para otros gestores de secretos, plataformas cloud y proveedores de CI más allá del stack de referencia (React + TS / Python + FastAPI).
- **Mejoras de agentes** — afilar a los especialistas a medida que evolucionan los modelos, sin aflojar las reglas duras que un modelo mejor no debe anular.
- **Despertar los gates de seguridad dormidos.** La auditoría de seguridad, el fuzz del contrato y el DAST vienen con sus disparadores comentados a propósito: necesitan una app/API desplegada que el kit base no tiene, y un gate que escanea un objetivo inexistente pasa sin haber mirado nada. Encenderlos significa darles un objetivo real, no solo descomentar una línea.
