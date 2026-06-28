# Changelog

Todos los cambios notables de este proyecto se documentan acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el versionado sigue [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Added
- Equipo de agentes ampliado a 10: `i18n-translations` (internacionalización) y `mobile-native` (capa nativa móvil).
- Capa de experiencia de ingeniería (`docs/09_engineering_experience/`): lecciones de producción, arquitectura de referencia y método multi-agente "Mesa de Ingenieros".
- Índice navegable del DHF (`docs/README.md`) con enlace a cada documento + pie de navegación en cada doc.
- Ejemplo trabajado (`examples/auralog/`): dispositivo Clase B ficticio con su DHF rellenado (Master Map, clasificación de seguridad, matriz de riesgo, trazabilidad).
- Diagramas de arquitectura en **Mermaid** (render nativo en GitHub) en Master Map, Architecture Overview y Reference Architecture.
- `dependabot.yml` (npm + pip + github-actions), `CODEOWNERS`, `.editorconfig`, `.gitattributes`.
- `CHANGELOG.md`.

### Changed
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
