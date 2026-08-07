# AGENTES ESPECIALIZADOS (consecuencia SaMD §5.6 + §5.7 — aislamiento de contexto por capa)

> Regla **transversal** del cerebro SaMD, en archivo aparte solo por legibilidad del core — **NO lleva `paths:`**, carga en cada sesión igual que `CLAUDE.md`. Mapa completo: `CLAUDE.md` §MAPA DE ESTE CEREBRO. El régimen de orquestación (cuándo lanzar, cuántos, cuál elegir) vive en `.claude/rules/orquestacion.md`.

El proyecto tiene un equipo de agentes de capa (hoy **12**, sin tope numérico fijo — ver `.claude/rules/orquestacion.md`, regla A) en `.claude/agents/`, cada uno cargado con las reglas SaMD de su capa. **Cuando la tarea encaja claramente en una capa, delegá al especialista** en vez de trabajar en el chat principal. Mejora la calidad (cada agente trae sus reglas duras precargadas), la velocidad (paralelización) y el aislamiento de contexto.

## Cuándo usar cada uno

| Agente | Capa | Invocar cuando la tarea sea sobre… |
| --- | --- | --- |
| `db-architect` | Datos | Schemas, migraciones, pool de conexiones, cifrado en reposo, reglas de BD, índices, performance de queries. |
| `backend` | API + lógica | Routers, services, schemas, dependencias, auth, audit middleware, fusibles de resiliencia, scheduler, tests. (La lógica clínica la lleva `clinical-algorithms`.) |
| `clinical-algorithms` | Clínico (núcleo SaMD) | Escalas autoinforme y cuestionarios validados, scoring y bandas de severidad con cortes citados, red de crisis y alertas de riesgo, PHI clínica cifrada, idempotencia anti-duplicado, disclaimers de no-diagnóstico, funciones puras verificadas. NO escribe migraciones (eso es `db-architect`) ni UI (eso es `frontend`). |
| `frontend` | UI + cliente | Componentes, hooks, DAOs HTTP, sync offline-first, cache de datos, tests de unidad/componente, mutation, UX clínica y accesibilidad. |
| `e2e-integration` | Testing E2E / integración | Suite de extremo a extremo que cruza frontend + backend + servicios, el harness (config, setup global, usuarios sembrados por worker), los workflows de humo/regresión, sharding y triage de flaky **AMBIENTAL** (timeout de runner, BD no fresca, colisión de shards, OOM). Verifica corriendo la suite. Distinto de `frontend` (unidad/componente) y `qa-mutation` (mutación). |
| `cloud-ops` | Plataforma | Cloud, BD gestionada, scheduler, gestor de secretos, hosting, CI/CD, monitoring, deploys. |
| `qa-mutation` | Testing / mutation | Olas de mutation testing, killers de mutantes, configs scoped, ratchet de score. NO lanza procesos pesados sin OK. |
| `samd-audit-trace` | Regulatorio (audita) | Auditar un changeset contra IEC 62304 §5.1/§5.7 + ISO 14971 antes de cerrar fase/PR. Detecta gaps, NO los escribe. |
| `docs-dhf` | Regulatorio (escribe) | Materializar updates en Master Map, TECHNICAL_DEBT_SUMMARY, ISO_14971_RISK_MATRIX, TRACEABILITY_MATRIX_SAMD, RFCs. Verifica `archivo:línea` + tests reales. Corre el link-checker. |
| `security-samd` | Seguridad regulatoria | SAST, cifrado, gestión de claves, JWT-only, audit sin PII, pentest contra el contrato OpenAPI. Reporta D-SEC-XX; NO escribe docs ni toca secretos. |
| `i18n-translations` | Internacionalización | Locales en todos los idiomas (frontend + backend), paridad y anti "copiado sin traducir", glosario clínico pre-certificación, placeholders y plurales. |
| `mobile-native` | Nativo móvil | Empaquetado del cliente web en app nativa, plugins nativos, auth nativa, persistencia nativa, push, build/firma/distribución. Verifica EN DEVICE real. Distinto del `frontend` (web). |

## Reglas de uso (las que NO cubre `.claude/rules/orquestacion.md`)

* **Antes de declarar verde** un cambio multi-capa, considerá pasar el changeset por `samd-audit-trace` para verificar la trazabilidad documental (TECHNICAL_DEBT_SUMMARY + Master Map + ISO_14971_RISK_MATRIX + TRACEABILITY_MATRIX_SAMD).
* **Reglas duras heredadas**: cada agente respeta las mismas reglas SaMD de `CLAUDE.md` y de `.claude/rules/`. **No se relajan reglas por delegar.** (Commits/pushes: ver `CLAUDE.md` §Git y commits — decisión exclusiva del dueño.)
* **Un agente que audita no escribe, y uno que escribe no se auto-audita**: la separación entre `samd-audit-trace` (detecta) y `docs-dhf` (materializa) es deliberada — quien encuentra el gap no debería ser quien decide que ya está cerrado.

> Para **cuándo lanzar agente**, **cuántos en paralelo**, **cuál elegir en solapamiento** y **cuándo NO usar agente**, ver `.claude/rules/orquestacion.md` → Reglas A-F. No se duplica acá.
