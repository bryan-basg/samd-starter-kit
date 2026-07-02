# ONBOARDING DE AGENTE — {{PROJECT_NAME}} (SaMD)

> **Plantilla del SaMD Starter Kit.** Reemplazá los marcadores `{{...}}` con los valores de tu proyecto.
> Marcadores principales: `{{PROJECT_NAME}}`, `{{SAMD_CLASS}}` (A/B/C), `{{INTENDED_USE}}`,
> `{{OWNER}}` (dueño del repo), `{{FRONTEND_STACK}}`, `{{BACKEND_STACK}}`, `{{DB_STACK}}`,
> `{{CLOUD_STACK}}`, `{{CHAT_LANG}}` (idioma del chat). Borrá esta nota cuando termines de adaptar.

---

## REGLA 0 — CUMPLIMIENTO SaMD ES LA PRIORIDAD ABSOLUTA

**Uso previsto (Intended Use):** {{INTENDED_USE}} — esta declaración es la que fija la clasificación SaMD y el alcance de lo que el software puede (y NO puede) afirmar.

Este software está bajo regulación **SaMD (Software as a Medical Device) Clase {{SAMD_CLASS}}** según **IEC 62304** + **ISO 14971** + **WCAG 2.1 AA** + **GDPR/HIPAA**.

**TODA decisión técnica se subordina a SaMD.** Cuando una regla operativa parezca en conflicto con la conveniencia del desarrollador, el cumplimiento SaMD GANA siempre.

### Lo que esto exige al agente

1. **Trazabilidad obligatoria** (IEC 62304 §5.1, §5.7): cada cambio en algoritmo clínico, esquema de BD, regla de negocio o flujo de seguridad debe registrarse en `docs/08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md`, en `docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md` cuando aplique, y reflejarse en el Master Map.
2. **No alucinar arquitectura, schemas ni reglas clínicas.** Si no estás 100% seguro, **DETENTE Y LEE** la documentación. Contexto maestro: `docs/00_master/MASTER_MAP.md`, `docs/03_software_development_plan/`, `.agents/workflows/protocolo_desarrollo.md`.
3. **No eliminar documentación existente** sobre arquitectura o algoritmos clínicos sin reporte de trazabilidad. Está prohibido.
4. **Verificación obligatoria** (IEC 62304 §5.7): no se declara una tarea "verde" sin haber corrido los tests vinculados y reportado los números.
5. **Fail-safe explícito** (ISO 14971): cuando un módulo clínico falle (red, BD, IA), el sistema degrada de forma segura y predecible — nunca silenciosa, nunca con tracebacks expuestos al usuario.
6. **Análisis de impacto antes de fixear** (IEC 62304 §5.6): un bug se considera "arreglado" solo tras revisar TODOS los consumidores del símbolo modificado, no solo el archivo donde se reportó.

Las secciones que siguen son **CONSECUENCIAS PRÁCTICAS** de la Regla 0.

---

## CÓMO TRABAJAR CON {{OWNER}} (preferencias del dueño)

### Idioma y registro
* **Siempre en {{CHAT_LANG}}.** Al explicar problemas, hallazgos, opciones o decisiones: **lenguaje cotidiano**, con **analogías de la vida real** cuando ayuden. **Sin jerga técnica innecesaria** (siglas regulatorias, `archivo:línea`, terminología de BD) salvo que se pida. (Variables y sintaxis en inglés; análisis y razonamiento en {{CHAT_LANG}}.)
* **Opciones a elegir → en palabras simples** (pequeño/mediano/grande, "me importa romper / no me importa"), no en letras/números técnicos.
* **Terminá siempre con una recomendación tuya**, justificada en una frase corta.
* **Excepción**: si se pide algo técnico explícito ("dame el comando", "mostrame el código"), entregalo sin diluir. Reportes en `docs/`, código y tests SÍ van con tecnicismo y precisión (obligatorio por SaMD) — solo cambia la capa de chat.

### Git y commits
* **Nunca commitees ni pushees sin que el dueño lo pida.** Antes de cada commit, reportá qué archivos se suben y esperá su OK. Ningún agente commitea/pushea — esa decisión es exclusiva del dueño.
* **Nunca pushees a remoto sin autorización explícita**, aunque ya esté commiteado local.
* **Operaciones destructivas** (`reset --hard`, `push --force`, borrar branches) → pedí OK aunque parezcan inocuas.
* **Tras un push a la rama principal, no hagas un segundo push hasta que el CI del primero termine.**
* **Commit selectivo con sesión paralela activa**: si hay otra sesión con cambios sin commitear, `git add` **EXPLÍCITO** de tus archivos (nunca `-A` / `-u`) — podés arrastrar cambios ajenos a medio terminar. Tras revertir un PR grande, verificá qué sub-cambios NO volvieron (pueden haber quedado solo en la rama revertida).
* **Comandos que el clasificador de permisos bloquea → los corre el dueño** (con `!` o a mano): operaciones sobre secretos productivos vivos, el primer push tras un OK vago, alta de infraestructura sensible (runners, credenciales). El agente prepara el comando/YAML; el dueño lo ejecuta.

### Antes de actuar
* **Explicá la genealogía antes de cambios no triviales**: cómo interpretás el problema, qué alternativas hay, cuál elegís y por qué, qué archivos tocás, qué riesgos. Esperá OK antes de codear.
* **Tras un OK de plan estructurado** ("vamos por lo recomendado", "vamos con todo") → ejecutá TODOS los sub-pasos **sin re-preguntar** ni micro-confirmar.
* **Zonas del producto marcadas off-limits por el dueño = prohibido tocar sin pedido dirigido.** Un "vamos con todo" sobre un módulo NO autoriza cruzar a una zona declarada aparte (ej. el código de cara al usuario final si el pedido era solo sobre el panel interno/admin). Si una utility global de la zona que estás tocando cae en cascada sobre una zona off-limits, avisá ANTES de aplicar el cambio.

### Diagnóstico de bugs (verificar antes de fixear)
* **Verificá antes de fixear**: ante un bug reportado, investigá primero — no saltes a escribir código.
* **Bug tras un deploy** → revisá logs estructurados de la plataforma cloud **antes** de teorizar sobre cache/Service Worker/navegador.

### Memoria vs este documento (anti-saturación)
* Este `CLAUDE.md` = reglas **ESTABLES** (bugs conocidos, comandos, protocolo, valores de config que apuntan al código). Los **snapshots dinámicos** (estado de tests, hallazgos de sesión, lecciones puntuales, estado del plan) van en la **memoria del agente** (`memory/MEMORY.md`), NO acá — para no inflar el documento.

---

## COMUNICACIÓN — EMPATÍA CON USUARIOS (consecuencia SaMD §5.4 + UX clínica)

* Toasts, errores y mensajes en pantalla: **claros, empáticos, sin jerga técnica**. Un usuario en crisis no debe ver "500 Internal Server Error".
* **Glosario clínico pre-certificación**: el frontend NO usa lenguaje que afirme función de dispositivo médico aún no certificado mientras la certificación esté pendiente. Reemplazos canónicos sugeridos: *clínico* → **profesional**, *diagnóstico* → **valoración**. Disclaimers legales exentos. No reintroducir claims de dispositivo médico no certificado. Texto nuevo en cualquier idioma respeta el glosario.

---

## BOY SCOUT (consecuencia SaMD §5.7 — mantenibilidad)

Cuando completes una tarea o modifiques un archivo:

* **Deja el código más limpio que lo encontraste.** Refactorizá al menos un pedazo de deuda en el archivo tocado (imports no usados, `any`, función >80 LOC sin justificación, etc).
* **Documentá y actualizá** el Master Map y el DHF. La documentación va junto con el cambio, no en sprints aparte.

---

## ANÁLISIS DE IMPACTO ANTES DE DECLARAR "ARREGLADO" (consecuencia SaMD §5.6)

* **Búsqueda global obligatoria** cuando modifiques un parámetro, retorno, schema o constante: `grep` en todo el repo para encontrar TODOS los consumidores. (Para el análisis de impacto de un símbolo puntual: skill `/samd-trace`.)
* **Cambio de endpoint** → actualizá inmediatamente su consumidor en el frontend, regenerá tipos del contrato (OpenAPI u equivalente) si aplica.
* **Regenerá el contrato (OpenAPI u equivalente) desde un `git worktree` limpio, no del working tree**, cuando haya sesión paralela sin commitear — código ajeno a medio terminar puede colarse en el contrato publicado. Si tu framework publica docstrings de rutas como descripción del contrato, tocarlos también dispara drift. NUNCA usar `git stash` para esto.
* **Verificación obligatoria** antes de declarar verde: corré los tests locales vinculados y reportá números.
* **Reorg de carpetas en `docs/`** → tras renombrar/mover cualquier `.md`, correr el link-checker cross-doc (`grep -rEn "\(\.{1,2}/[^)]+\.md" docs/`) y resolver enlaces rotos en el mismo PR. **Ningún PR de reorg cierra sin que el link-checker reporte 0 broken.**
* **TRACEABILITY_MATRIX_SAMD.md** → cada REQ-XXX en la matriz debe apuntar a `archivo:línea` verificable + nombre de test que existe HOY. Frases vagas sin path NO son trazabilidad SaMD aceptable. Un auditor externo lo levanta primero.
* **Propagación de reglas y valores de config — anti-drift de la fuente de verdad**: cuando cambies una **regla viva** o un **valor de configuración volátil**, propagalo en la **MISMA pasada** a TODOS sus espejos: `CLAUDE.md`, `.claude/agents/*.md`, `.claude/commands/*.md`, docs DHF y memoria. **El código es la fuente de verdad** — los demás citan el valor + apuntan al archivo, no lo recopian. Antes de cerrar: `grep` el valor/regla vieja en `CLAUDE.md .claude/ docs/` → **0 residuos**.

---

## ESTÁNDARES DEL BACKEND (consecuencia SaMD §5.5 — implementación robusta)

> Adaptá esta sección a tu stack real (`{{BACKEND_STACK}}` / `{{DB_STACK}}`). Lo que sigue son los principios estables; los valores concretos (pools, tiers, env vars) deben citar `archivo:línea` del código real.

* **Identidad por token, nunca por cliente**: el `user_id` depende exclusivamente del token/JWT decodificado por el proveedor de auth. NUNCA aceptes `user_id` desde body, query ni headers custom — es un vector de escalada garantizado.
* **Asincronía máxima**: prohibidas funciones I/O bloqueantes en el path de request. Usá el modelo async del framework.
* **Tipado estricto**: prohibido `any`. Validación de esquemas obligatoria. El type-checker estricto pasa en CI.
* **Errores en API**: NUNCA devolver tracebacks, logs técnicos, metadatos internos de BD o SQL al cliente. Solo mensajes empáticos + código HTTP correcto.
* **Cifrado en reposo**: campos PII/PHI cifrados con AES-256-GCM (o equivalente auditado). La clave de cifrado vive en un gestor de secretos / KMS — NUNCA hardcodeada, NUNCA reusando otra clave.
* **Migraciones de schema controladas**: el deploy debe migrar de forma atómica y abortar si falla (prod protegida). NUNCA confiar en el verde de una migración sin verificar la revisión real aplicada en el entorno destino.
* **Variables de entorno en producción**: viven en el gestor de secretos, no en el `.env` del repo. Cuidado con comandos de deploy que **reemplazan** la lista completa de env vars en vez de hacer merge.
* **Auditoría**: persistir a BD las mutaciones (POST/PUT/DELETE/PATCH); las lecturas van a logging estructurado para no consumir el pool. Compatible con SaMD §5.7 (trazabilidad de cambios).
* **`.env.example` cubre TODO el código vivo**: si añadís una var nueva en config o leés por entorno en services/middleware, **DEBES** añadirla a `.env.example` con un comentario SaMD-aware.

---

## TESTING (consecuencia directa SaMD §5.7 — verificación)

SaMD exige verificación demostrable. Esto NO es negociable.

### Reglas duras

* **Tests rigurosos, no de humo:** "renderiza sin crashear" NO es un test SaMD. Exigir aserciones específicas sobre valores, llamadas y side effects.
* **Mutation score** (recomendado): Frontend GLOBAL ≥90% (Stryker o equivalente). Backend ≥80% en módulos clínicos críticos (mutmut o equivalente). Ajustá los umbrales a la criticidad de tu Clase {{SAMD_CLASS}}.
* **Mocks asíncronos firmes** + aislamiento de estado global en cada test.
* **Si el código bajo test usa `hasattr`/duck-typing**, mockear con whitelist explícita de atributos. Un mock plano deja mutantes vivos.
* **No correr el type-checker/tests unitarios mientras corre mutation testing** — son CPU-intensivos y los procesos se contaminan.
* **No improvisar detección de imports muertos a ojo** — usar el linter (riesgo de borrar imports usados vía side effects).

### Estrategia

Consultá `docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md` antes de tocar la suite.

---

## ORQUESTACIÓN MULTI-AGENTE (consecuencia SaMD §5.6 análisis de impacto + §5.7 verificación)

### Postura: paralelismo agresivo con cohesión

* **Repartir en muchos agentes en paralelo** cuando la tarea lo permita (búsquedas anchas, mutation por archivo, auditorías, refactors multi-archivo independientes).
* **Verificación adversarial OBLIGATORIA sobre hallazgos clínicos/seguridad** (§5.6): un hallazgo que dispara cambio en algoritmo clínico, schema, regla de negocio o flujo de seguridad debe ser refutado por otro agente independiente antes de actuar. Hallazgo no verificado ≠ "arreglado".
* **Encadenar sub-pasos sin micro-confirmar** tras un OK de plan.
* **`worktree`** cuando varios agentes muten archivos en paralelo y puedan pisarse. **No dejes el `cwd` dentro de un worktree antes de lanzar agentes**: heredan el cwd y editan archivos DENTRO del worktree en vez del repo — volvé al repo raíz antes de repartir.
* **Tamaño de ola**: escalar a lo que la tarea justifique. La calidad **no se relaja por ir más rápido**.

### Protocolo anti-drift (OBLIGATORIO con 2+ agentes)

Con 2+ agentes el riesgo no es la calidad individual sino la **pérdida de cohesión**: el orquestador recibe summaries de *lo que el agente intentó*, no del *diff real*. **Regla dura: escribí el contrato compartido (campos/tipos/paths/defaults exactos) con OK del dueño antes de lanzar; tras cada agente leé el `git diff` REAL, nunca el summary; drift → 1 agente correctivo (no re-lances a todos). Serializá (no paralelices) si el contrato es complejo/cambiante, hay tipos generados (OpenAPI o equivalente) o un símbolo cruza 3+ capas.** Procedimiento completo (los 7 pasos + reglas de cohesión): skill `/anti-drift`.

---

## AGENTES ESPECIALIZADOS (consecuencia SaMD §5.6 + §5.7 — aislamiento de contexto por capa)

El proyecto tiene un equipo de agentes en `.claude/agents/`, cada uno cargado con las reglas SaMD de su capa. **Cuando la tarea encaja claramente en una capa, delegá al especialista** en vez de trabajar en el chat principal.

| Agente | Capa | Invocar cuando la tarea sea sobre… |
| --- | --- | --- |
| `db-architect` | Datos | Schemas, migraciones, pool de conexiones, cifrado en reposo, reglas de BD, performance de queries. |
| `backend` | API + lógica | Routers, services, schemas, dependencias, auth, audit middleware, fusibles de resiliencia, scheduler, IA backend, tests. |
| `frontend` | UI + cliente | Componentes, hooks, DAOs HTTP, sync offline-first, cache de datos, tests de UI, mutation, neuro-UX. |
| `cloud-ops` | Plataforma | Cloud Run/equivalente, BD gestionada, scheduler, gestor de secretos, hosting, IA cloud, CI/CD, monitoring, deploys. |
| `qa-mutation` | Testing / mutation | Olas de mutation testing, killers de mutantes, configs scoped, ratchet de score. NO lanza procesos pesados sin OK. |
| `samd-audit-trace` | Regulatorio (audita) | Auditar un changeset contra IEC 62304 §5.1/§5.7 + ISO 14971 antes de cerrar fase/PR. Detecta gaps, NO los escribe. |
| `docs-dhf` | Regulatorio (escribe) | Materializar updates en Master Map, TECHNICAL_DEBT_SUMMARY, ISO_14971_RISK_MATRIX, TRACEABILITY_MATRIX_SAMD, RFCs. Corre link-checker. |
| `security-samd` | Seguridad regulatoria | SAST (Trivy + Semgrep + fuzz de API), cifrado, gestión de claves, JWT-only, audit sin PII, pentest contra el contrato OpenAPI. Reporta D-SEC-XX; NO escribe docs ni toca secretos. |
| `i18n-translations` | Internacionalización | Locales en todos los idiomas (frontend + backend), paridad y anti "copiado sin traducir", glosario clínico pre-certificación (sin claims de dispositivo médico no certificado), placeholders y plurales. |
| `mobile-native` | Nativo móvil | Empaquetado del cliente web en app nativa (Capacitor/React Native/equiv.), plugins nativos, auth nativa, persistencia nativa, push, build/firma/distribución. Verifica EN DEVICE real. Distinto del `frontend` (web). |

---

## COMANDOS CORE (adaptar a tu stack)

```bash
# Frontend dev y test  ({{FRONTEND_STACK}})
cd frontend && npm run dev
cd frontend && npm run test

# Backend tests y tipos  ({{BACKEND_STACK}})
# (activá el entorno virtual / toolchain correspondiente)
pytest -q                                  # suite (esqueleto de referencia: Python/pytest)
pytest --cov=app --cov-report=term-missing # cobertura canónica
mypy .                                     # type-checker estricto

# CI local pre-push
bash scripts/run_local_ci.sh

# Stack SaMD-grade (lentos — correr con OK explícito)
bash scripts/run_stryker.sh      # mutation frontend
bash scripts/run_schemathesis.sh # fuzz API contra el contrato OpenAPI
bash scripts/run_trivy.sh        # CVEs deps + Docker
bash scripts/run_semgrep.sh      # SAST
```

* **Higiene de procesos dev locales**: tras levantar emuladores/servidor/frontend para una prueba, matalos y liberá los puertos que hayas ocupado. Los procesos pesados (tests, mutación, cobertura) corren en la máquina local; los agentes en la nube solo razonan.
* Para levantar el stack local completo con datos de prueba sembrados, ver la skill `/arrancar-stack-local`.

---

## CI / GITHUB ACTIONS (adaptar a tu proveedor de CI real)

* Optimizaciones recomendadas en todo workflow nuevo: cancelación de runs duplicados, cache de dependencias, `timeout-minutes` duro, filtros por paths cuando el repo crece.
* **Workflow en rojo → logs FRESCOS antes de teorizar** (§5.6): reproducí lo barato en local antes de asumir bug de código o config; la caída puede ser **ambiental** (timeout, OOM del runner, flaky), no de código. Diagnóstico paso a paso: skill `/ci-rojo`.

---

## CIERRE DE BLOQUE GRANDE

* **SALVAGUARDA SIEMPRE-ON — no depende de acordarse de invocar la skill.** Antes de declarar cerrado **cualquier** bloque o PR —incluso si parece "solo docs" o "solo config"— pasá por: **(1) trazabilidad** — `TECHNICAL_DEBT_SUMMARY` + Master Map + `ISO_14971_RISK_MATRIX` (si toca el producto: algoritmo clínico, schema, regla de negocio, seguridad) **o** `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN` + Master Map (si cambia el **proceso/gobernanza**: agentes, reglas, skills, CI); **(2) verificación** — tests/CI vinculados con números reales.
* Al cerrar un **bloque grande** (sprint/fase): correr la foto de estado (`bash scripts/audit_project_state.sh`) ANTES de declarar cerrado, y NO cerrar con trabajo/deuda **vivo** sin anotar — el desfase entre "lo que creemos hecho" y "lo que está en producción" es la fuga real. El script solo INFORMA; borrar/archivar lo decide el dueño (destructivo con OK). Checklist canónico completo (los docs DHF + link-checker cross-doc): skill `/cierre-bloque`.
