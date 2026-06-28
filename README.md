# SaMD Starter Kit

> **Kit de arranque para construir un dispositivo software médico (Software as a Medical Device) con un equipo de agentes de IA.**
> Destila la experiencia de un proyecto SaMD Clase B real: el equipo de agentes especializados, el reglamento de cumplimiento, los workflows multi-agente, la estructura de memoria y el Design History File (DHF) regulatorio completo — todo generalizado en plantillas listas para adaptar.

Este repositorio NO es una aplicación. Es el **andamiaje y la metodología** para que vos (y tu agente de IA, como Claude Code) arranquen un SaMD de cero sin reinventar el proceso de cumplimiento, testing y trazabilidad que IEC 62304 + ISO 14971 exigen.

---

## ¿Qué hay adentro?

| Pieza | Path | Qué es |
|---|---|---|
| **Reglamento del agente** | `CLAUDE.md` | La "Regla 0" (SaMD es prioridad absoluta) + cómo trabaja el agente, testing, orquestación multi-agente, estándares de backend/frontend. Es lo primero que tu agente lee. |
| **Equipo de 8 agentes** | `.claude/agents/` | Especialistas por capa: `backend`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `security-samd`, `samd-audit-trace` (audita), `docs-dhf` (escribe). |
| **Comando + skill** | `.claude/commands/`, `.claude/skills/` | `samd-trace`: análisis de impacto (§5.6) antes de declarar algo "arreglado". |
| **Workflows multi-agente** | `.claude/workflows/` | `samd-review`: revisión del diff por dimensiones de riesgo con verificación adversarial. |
| **Protocolo de desarrollo** | `.agents/workflows/protocolo_desarrollo.md` | Espejo agnóstico al agente del proceso estable. |
| **Memoria** | `memory/MEMORY.md` | Estructura de memoria persistente del agente (snapshots dinámicos, no reglas estables). |
| **Design History File (DHF)** | `docs/` | ~25 plantillas regulatorias: matriz de riesgo ISO 14971, trazabilidad SaMD, plan de desarrollo IEC 62304, clasificación de seguridad, SOUP, evaluación/validación clínica, post-market, IFU, privacidad, gestión de configuración, runbooks, RFCs, y más. |
| **RFCs de ejemplo** | `docs/05_design_decisions/RFC-001..003` | Tres decisiones SaMD reales ya escritas (cifrado en reposo, identidad JWT-only, scheduler externo) — modelo para tus propias RFCs. |
| **CI/CD funcional** | `.github/workflows/` | `ci.yml` (lint+types+tests+drift de contrato), `security-audit.yml` (Trivy+Semgrep), `nightly-mutation.yml` (Stryker). Sobre el **stack de referencia** (React+TS / Python+FastAPI) — adaptá los `run:` a tu stack. |
| **Scaffolding** | `frontend/` `app/` `tests/` `scripts/` | Carpetas de arranque + scripts reales (`init_kit`, `check_doc_links`, `run_local_ci`, `sast`, `export_openapi`). |

---

## La idea: cumplimiento por diseño, no como sprint aparte

La regla central (heredada del proyecto que originó este kit) es la **Regla 0**: *toda decisión técnica se subordina al cumplimiento SaMD*. En la práctica eso significa cuatro hábitos que el equipo de agentes hace cumplir solo:

1. **Trazabilidad obligatoria** (IEC 62304 §5.1/§5.7): cada cambio clínico/schema/seguridad deja rastro en el DHF en el mismo PR.
2. **Verificación demostrable** (§5.7): nada se declara "verde" sin correr los tests vinculados y reportar números.
3. **Fail-safe explícito** (ISO 14971): cuando algo falla, degrada de forma segura y predecible — nunca en silencio.
4. **Análisis de impacto antes de fixear** (§5.6): un bug se arregla tras revisar TODOS los consumidores del símbolo, no solo el archivo donde se reportó.

---

## Cómo arrancar tu proyecto desde el kit

### 1. Cloná y renombrá

```bash
git clone <este-repo> mi-dispositivo-medico
cd mi-dispositivo-medico
rm -rf .git && git init   # arrancá tu propia historia
```

### 2. Completá los marcadores

Todo el contenido usa marcadores `{{...}}`. Corré el script interactivo:

```bash
bash scripts/init_kit.sh
```

…o reemplazalos a mano. Los principales:

| Marcador | Qué poné |
|---|---|
| `{{PROJECT_NAME}}` | Nombre de tu producto. |
| `{{SAMD_CLASS}}` | Clase de seguridad IEC 62304: A, B o C. |
| `{{INTENDED_USE}}` | Declaración de uso previsto (define toda tu estrategia regulatoria). |
| `{{OWNER}}` | Dueño/responsable del repo. |
| `{{FRONTEND_STACK}}` / `{{BACKEND_STACK}}` / `{{DB_STACK}}` / `{{CLOUD_STACK}}` | Tu stack real. |
| `{{CHAT_LANG}}` | Idioma en que el agente te habla. |

### 3. Clasificá tu software (hacelo primero)

Editá `docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md`. La Clase (A/B/C) define el rigor de TODO lo demás. Sin esto, no sabés qué umbrales de testing ni qué documentos te exige el regulador.

### 4. Llená el Master Map y la Risk Matrix

`docs/00_master/MASTER_MAP.md` y `docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md` son el corazón vivo del DHF. Identificá tus módulos clínicos críticos y sus fail-safes desde el día 1.

### 5. Trabajá con el equipo de agentes

Con Claude Code, tu agente ya lee `CLAUDE.md` y puede delegar a los 8 especialistas. Patrón típico de una tarea:

```
backend/frontend/db-architect  → implementan
qa-mutation                    → endurecen los tests
samd-audit-trace               → audita la trazabilidad del changeset
docs-dhf                       → materializa los updates del DHF
```

---

## Reglas duras que el kit hace cumplir (no las anules)

- **Nadie commitea ni pushea sin OK explícito del dueño.**
- **El motor de mutation nunca corre en paralelo con agentes que escriben tests.**
- **Procesos pesados locales (mutation full, fuzz, suites completas) piden OK cada vez.**
- **Verificación adversarial obligatoria** sobre hallazgos clínicos/seguridad antes de actuar.
- **Identidad solo del token** (JWT-only) — nunca `user_id` desde el cliente.
- **Errores sin tracebacks al usuario** — mensajes empáticos + código HTTP correcto.

---

## Estándares normativos cubiertos

IEC 62304 (ciclo de vida del software médico) · ISO 14971 (gestión de riesgo) · ISO 13485 (sistema de gestión de calidad) · IEC 62366 (usabilidad) · WCAG 2.1 AA (accesibilidad) · GDPR + HIPAA (privacidad/seguridad de datos de salud).

> Este kit es un **andamiaje de proceso**, no asesoría regulatoria ni garantía de certificación. La clasificación, la evidencia clínica y la aprobación de un dispositivo médico requieren el juicio de profesionales regulatorios y, según el mercado, un Organismo Notificado o la autoridad sanitaria correspondiente.

---

## Licencia

Ver `LICENSE`.
