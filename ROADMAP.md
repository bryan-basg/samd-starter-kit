<div align="center">

# Roadmap — SaMD Starter Kit

**English · [Español](#roadmap--español)**

</div>

> An honest, public roadmap for the kit. The kit is a **process scaffold**, not regulatory advice and not a guarantee of certification — see the [README](README.md) for what it is and isn't. Horizons are intentionally soft ("next", "exploring"); we don't commit to calendar dates for an open-source side project.
>
> Want to shape this? Open a [feature request](.github/ISSUE_TEMPLATE/feature_request.yml), grab a [good first issue](.github/ISSUE_TEMPLATE/good_first_issue.yml), or start a [Discussion](https://github.com/bryan-basg/samd-starter-kit/discussions).

## Done

What already ships in the kit today:

- **Team of 10 agents** (`.claude/agents/`) — per-layer specialists with the SaMD ruleset pre-loaded: `backend`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `security-samd`, `samd-audit-trace`, `docs-dhf`, `i18n-translations`, `mobile-native`.
- **Agent ruleset** (`CLAUDE.md`) — Rule 0 (SaMD is the absolute priority), backend/frontend standards, testing rules, and the multi-agent anti-drift protocol.
- **11 working CI/CD workflows** (`.github/workflows/`) — CI gates, security audit (Trivy + Semgrep), nightly mutation (Stryker), API contract fuzzing (schemathesis), DAST (OWASP ZAP), SBOM, Postgres tier, OpenAPI contract-drift, project-state audit, stale-PR triage, and a deploy template.
- **40+ document Design History File** (`docs/`) — ISO 14971 risk matrix, SaMD traceability matrix, IEC 62304 plan, safety classification, SOUP, clinical evaluation/validation, post-market surveillance, IFU, user docs, privacy, runbooks.
- **Runnable skeleton** (`app/` · `frontend/` · `tests/`) — a minimal FastAPI + React/TS example wiring the hard rules (token-only identity, AES-256-GCM at rest, fail-safe, flat accessible UI). Runs with zero infra.
- **Worked example** (`examples/auralog/`) — a fictional Class B device (AuraLog) with its DHF filled in, so you can see the kit in action.
- **Command, skill & review workflow** (`.claude/`) — `samd-trace` impact analysis (§5.6) and the `samd-review` adversarial diff review.
- **Bilingual onboarding** — `README` / `CONTRIBUTING` / `GETTING_STARTED` in English and Spanish, with a pre-certification clinical glossary so text never claims an uncertified medical-device function.

## In progress

The improvements this initiative is actively landing:

- **One-click developer experience** — smoother `init_kit.sh` flow and a faster path from clone to a green local CI run.
- **Broader regulatory coverage** — generalized references beyond the EU lens: U.S. FDA, EU MDR, and IMDRF guidance mapped to the existing DHF templates, so the kit reads cleanly in more markets.
- **Documentation site** — exploring a browsable docs site over `docs/` so the DHF and the agent method are easier to navigate than raw Markdown.
- **Public project signals** — roadmap, sponsorship template, good-first-issue path, and live CI status badges (this change).

## Planned

Ideas we're exploring; not committed, and open to community input:

- **More worked examples** — additional fictional devices across Class A/B/C to show how the DHF scales with safety classification.
- **More languages** — extending the bilingual baseline (EN/ES) to further locales across the README, contributor docs, and the i18n tooling.
- **Integrations** — optional adapters for other secret managers, cloud platforms, and CI providers beyond the reference stack (React + TS / Python + FastAPI).
- **Agent improvements** — sharpening the specialists as the underlying models evolve, without loosening the hard rules a better model must not override.

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

- **Equipo de 10 agentes** (`.claude/agents/`) — especialistas por capa con el reglamento SaMD precargado: `backend`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `security-samd`, `samd-audit-trace`, `docs-dhf`, `i18n-translations`, `mobile-native`.
- **Reglamento del agente** (`CLAUDE.md`) — Regla 0 (SaMD es prioridad absoluta), estándares de backend/frontend, reglas de testing y el protocolo anti-drift multi-agente.
- **15 workflows de CI/CD funcionales** (`.github/workflows/`) — 11 gates heredables por el proyecto derivado (CI, auditoría de seguridad con Trivy + Semgrep, mutación nocturna con Stryker, fuzz del contrato de API con schemathesis, DAST con OWASP ZAP, SBOM, tier Postgres, drift del contrato OpenAPI, auditoría del estado del proyecto, triage de PRs viejos y una plantilla de deploy) + 4 de mantenimiento del propio kit (docs, gates de calidad, guard de placeholders, release).
- **Design History File de 40+ documentos** (`docs/`) — matriz de riesgo ISO 14971, matriz de trazabilidad SaMD, plan IEC 62304, clasificación de seguridad, SOUP, evaluación/validación clínica, post-market, IFU, docs de usuario, privacidad, runbooks.
- **Esqueleto ejecutable** (`app/` · `frontend/` · `tests/`) — un ejemplo mínimo FastAPI + React/TS que cablea las reglas duras (identidad solo del token, AES-256-GCM en reposo, fail-safe, UI plana y accesible). Corre sin infra.
- **Ejemplo trabajado** (`examples/auralog/`) — un dispositivo Clase B ficticio (AuraLog) con su DHF rellenado, para ver el kit en acción.
- **Comando, skill y workflow de revisión** (`.claude/`) — el análisis de impacto `samd-trace` (§5.6) y la revisión adversarial de diff `samd-review`.
- **Onboarding bilingüe** — `README` / `CONTRIBUTING` / `GETTING_STARTED` en inglés y español, con un glosario clínico pre-certificación para que ningún texto afirme una función de dispositivo médico no certificada.

## En curso

Las mejoras que esta iniciativa está aterrizando ahora:

- **Experiencia de desarrollo de un clic** — un flujo `init_kit.sh` más suave y un camino más rápido del clone a un CI local en verde.
- **Cobertura regulatoria más amplia** — referencias generalizadas más allá del lente UE: FDA (EE. UU.), MDR (UE) y guías IMDRF mapeadas a las plantillas existentes del DHF, para que el kit lea bien en más mercados.
- **Sitio de documentación** — explorando un sitio navegable sobre `docs/` para que el DHF y el método de agentes sean más fáciles de recorrer que el Markdown crudo.
- **Señales de proyecto público** — roadmap, plantilla de sponsorship, camino de good-first-issue y badges de estado de CI en vivo (este cambio).

## Planeado

Ideas que estamos explorando; no comprometidas y abiertas a la comunidad:

- **Más ejemplos trabajados** — dispositivos ficticios adicionales en Clase A/B/C para mostrar cómo escala el DHF con la clasificación de seguridad.
- **Más idiomas** — extender la base bilingüe (EN/ES) a más locales en el README, las docs de contribución y el tooling de i18n.
- **Integraciones** — adaptadores opcionales para otros gestores de secretos, plataformas cloud y proveedores de CI más allá del stack de referencia (React + TS / Python + FastAPI).
- **Mejoras de agentes** — afilar a los especialistas a medida que evolucionan los modelos, sin aflojar las reglas duras que un modelo mejor no debe anular.
