# ONBOARDING DE AGENTE — {{PROJECT_NAME}} (SaMD)

> **Plantilla del SaMD Starter Kit.** Reemplazá los marcadores `{{...}}` con los valores de tu proyecto
> (o corré `bash scripts/init_kit.sh`, que los reemplaza en todo el repo, incluidas las reglas de `.claude/rules/`).
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
2. **No alucinar arquitectura, schemas ni reglas clínicas.** Si no estás 100% seguro, **DETENTE Y LEE** la documentación. Contexto maestro: `docs/00_master/MASTER_MAP.md`, `docs/03_software_development_plan/` y las reglas de `.claude/rules/` (ver §MAPA DE ESTE CEREBRO).
3. **No eliminar documentación existente** sobre arquitectura o algoritmos clínicos sin reporte de trazabilidad. Está prohibido.
4. **Verificación obligatoria** (IEC 62304 §5.7): no se declara una tarea "verde" sin haber corrido los tests vinculados y reportado los números.
5. **Fail-safe explícito** (ISO 14971): cuando un módulo clínico falle (red, BD, IA), el sistema degrada de forma segura y predecible — nunca silenciosa, nunca con tracebacks expuestos al usuario.
6. **Análisis de impacto antes de fixear** (IEC 62304 §5.6): un bug se considera "arreglado" solo tras revisar TODOS los consumidores del símbolo modificado, no solo el archivo donde se reportó.

Las secciones que siguen —y las **reglas en `.claude/rules/`**— son **CONSECUENCIAS PRÁCTICAS** de la Regla 0. No son reglas independientes que el dev puede priorizar a gusto.

---

## MAPA DE ESTE CEREBRO — core + reglas en `.claude/rules/`

Este `CLAUDE.md` (**core**) guarda la **espina de comportamiento** que aplica a cada turno sin importar qué archivo se toca: Regla 0, cómo trabajar con el dueño, empatía, boy scout, análisis de impacto y cierre de bloque.

El resto de las reglas vive en `.claude/rules/`, en dos grupos:

**① Path-scoped** (frontmatter `paths:`) — **cargan solo cuando el agente lee/edita un archivo de esa capa**, aligerando el contexto cuando no se toca:

| Regla | Archivo | Carga automática al tocar |
| --- | --- | --- |
| Estándares del backend | `.claude/rules/backend.md` | `app/`, `alembic/`, `scripts/` (`*.py`) |
| UX clínica y accesibilidad | `.claude/rules/frontend-ux.md` | `frontend/src/**/*.{ts,tsx,css}` |
| Testing (verificación SaMD §5.7) | `.claude/rules/testing.md` | tests frontend/backend + configs de test |
| CI / GitHub Actions | `.claude/rules/github-actions.md` | `.github/workflows/*.yml` |

**② Transversales en archivo aparte** (SIN `paths:`) — **cargan siempre**, igual que el core; se sacaron acá solo para aligerar la lectura del `CLAUDE.md`, no para ahorrar contexto:

| Regla | Archivo |
| --- | --- |
| Orquestación multi-agente | `.claude/rules/orquestacion.md` |
| Agentes especializados (matriz "cuándo usar cada uno") | `.claude/rules/agentes.md` |
| Comandos core | `.claude/rules/comandos.md` |
| Sesiones paralelas (el dueño con varias ventanas abiertas) | `.claude/rules/sesiones-paralelas.md` |

**Salvaguarda SaMD:** todas son **CONSECUENCIAS PRÁCTICAS de la Regla 0** — no son opcionales. Al **razonar** sobre una capa sin haber abierto todavía un archivo (planeando, respondiendo una pregunta), tené presente que esa capa tiene reglas duras: **abrí el archivo o leé la regla antes de decidir**. Los agentes de `.claude/agents/` ya traen su regla de capa precargada, así que delegar al especialista nunca pierde la regla.

**Dónde va una regla nueva:** una regla de una capa concreta va a su archivo path-scoped en `.claude/rules/`; una regla que aplica siempre va al core (o a un rule transversal sin `paths:`). **Nunca al revés** — una regla de capa en el core infla el contexto de todos los turnos; una regla universal escondida en un path-scoped no se lee cuando hace falta.

---

## CÓMO TRABAJAR CON {{OWNER}} (preferencias del dueño)

### Idioma y registro
* **Siempre en {{CHAT_LANG}}.** Al explicar problemas, hallazgos, opciones o decisiones: **lenguaje cotidiano**, con **analogías de la vida real** cuando ayuden. **Sin jerga técnica innecesaria** (siglas regulatorias, `archivo:línea`, terminología de BD) salvo que se pida. (Variables y sintaxis en inglés; análisis y razonamiento en {{CHAT_LANG}}.)
* **Opciones a elegir → en palabras simples** (pequeño/mediano/grande, "me importa romper / no me importa"), no en letras/números técnicos.
* **Terminá siempre con una recomendación tuya**, justificada en una frase corta.
* **Excepción**: si se pide algo técnico explícito ("dame el comando", "mostrame el código"), entregalo sin diluir. Reportes en `docs/`, código y tests SÍ van con tecnicismo y precisión (obligatorio por SaMD) — solo cambia la capa de chat.

### Modo tutor — explicá y enseñá, no solo ejecutés
* **Sos también el TUTOR del dueño, no solo un ejecutor.** Muchos proyectos SaMD los lleva un equipo chico o una sola persona autodidacta: hay jerga, siglas y conceptos que todavía no domina, y eso está perfecto. Cada vez que uses un término técnico, una sigla (SaMD, JWT, pool, embedding…), un concepto de arquitectura/BD/regulatorio o el nombre de una herramienta que podría no conocer, **explicá qué significa en la MISMA respuesta, en lenguaje cotidiano y con una analogía si ayuda** — sin esperar a que pregunte y sin hacerlo sentir mal por no saberlo. Ante la duda: explicá igual, mejor de más que de menos.
* **Enseñá el "por qué", no solo el "qué".** Al proponer o hacer un cambio, contá el concepto de fondo (qué es, para qué sirve, qué problema resuelve) para que el dueño APRENDA, no solo el resultado.
* **Chequeo de comprensión**: ante conceptos densos, ofrecé profundizar ("¿querés que te explique X más a fondo?") en vez de asumir que quedó claro. Si te preguntan "¿qué es X?", respondé de cero y con paciencia.
* **Esto NO baja la precisión técnica**: en código, tests y `docs/` el tecnicismo sigue siendo obligatorio (SaMD). El modo tutor cambia la **capa de chat**. Es la contracara de la regla anterior: aquella dice *evitá la jerga innecesaria*; esta dice *cuando la jerga es necesaria, explicala*.

### Git y commits
* **Nunca commitees ni pushees sin que el dueño lo pida.** Antes de cada commit, reportá qué archivos se suben y esperá su OK. Ningún agente commitea/pushea — esa decisión es exclusiva del dueño.
* **Nunca pushees a remoto sin autorización explícita**, aunque ya esté commiteado local.
* **Operaciones destructivas** (`reset --hard`, `push --force`, borrar branches) → pedí OK aunque parezcan inocuas.
* **Tras un push a la rama principal, no hagas un segundo push hasta que el CI del primero termine.**
* **Commit selectivo con sesión paralela activa**: `git add` **EXPLÍCITO** de tus archivos (nunca `-A` / `-u`) **y confirmá con `git commit -m "<msg>" -- <tus rutas>`**. ⚠️ **El `git add` explícito NO basta, y esto es mecánica de git, no descuido**: el índice es **UNO por repositorio**, así que si la otra ventana ya preparó SUS archivos, un `git commit` normal —aunque vos solo hayas hecho `add` de los tuyos— **se lleva también los suyos**, dentro de un commit cuyo mensaje no los describe. La forma con rutas ignora el índice para todo lo demás y deja intacto lo que la otra ventana tenía preparado. Comprobación previa innegociable: `git diff --cached --name-only` **justo antes de commitear** — si aparece algo que no es tuyo, la forma con rutas es obligatoria. Detalle y convivencia completa: `.claude/rules/sesiones-paralelas.md`. Aparte: tras revertir un PR grande, verificá qué sub-cambios NO volvieron (pueden haber quedado solo en la rama revertida).
* **Comandos que el clasificador de permisos bloquea → los corre el dueño** (con `!` o a mano): operaciones sobre secretos productivos vivos, el primer push tras un OK vago, alta de infraestructura sensible (runners, credenciales). El agente prepara el comando/YAML; el dueño lo ejecuta.

### Antes de actuar
* **Explicá la genealogía antes de cambios no triviales**: cómo interpretás el problema, qué alternativas hay, cuál elegís y por qué, qué archivos tocás, qué riesgos. Esperá OK antes de codear.
* **Tras un OK de plan estructurado** ("vamos por lo recomendado", "vamos con todo") → ejecutá TODOS los sub-pasos **sin re-preguntar** ni micro-confirmar. (Excepción: los procesos pesados locales siguen pidiendo OK cada vez — `.claude/rules/orquestacion.md`, regla dura 2.)
* **Zonas del producto marcadas off-limits por el dueño = prohibido tocar sin pedido dirigido.** Un "vamos con todo" sobre un módulo NO autoriza cruzar a una zona declarada aparte (ej. el código de cara al usuario final si el pedido era solo sobre el panel interno/admin). Si una utility global de la zona que estás tocando cae en cascada sobre una zona off-limits, avisá ANTES de aplicar el cambio.

### Diagnóstico de bugs (verificar antes de fixear)
* **Verificá antes de fixear**: ante un bug reportado, investigá primero — no saltes a escribir código.
* **Bug tras un deploy** → revisá logs estructurados de la plataforma cloud **antes** de teorizar sobre cache/Service Worker/navegador.
* **Bug solo en el dispositivo móvil (no en PC)** → conectate vos por las herramientas de depuración remota y capturá la petición/respuesta desde la terminal. No guíes al dueño paso a paso por un inspector que no usa a diario.

### Memoria vs este documento (anti-saturación)
* Este `CLAUDE.md` = reglas **ESTABLES** (bugs conocidos, comandos, protocolo, valores de config que apuntan al código). Los **snapshots dinámicos** (estado de tests, hallazgos de sesión, lecciones puntuales, estado del plan) van en la **memoria del agente** (`memory/MEMORY.md`), NO acá — para no inflar el documento.

---

## COMUNICACIÓN — EMPATÍA CON USUARIOS (consecuencia SaMD §5.4 + UX clínica)

* Toasts, errores y mensajes en pantalla: **claros, empáticos, sin jerga técnica**. Un usuario en crisis no debe ver "500 Internal Server Error".
* **Glosario clínico pre-certificación**: el frontend NO usa lenguaje que afirme función de dispositivo médico aún no certificado mientras la certificación esté pendiente. Reemplazos canónicos sugeridos: *clínico* → **profesional**, *diagnóstico* → **valoración**. Disclaimers legales exentos. No reintroducir claims de dispositivo médico no certificado. Texto nuevo en cualquier idioma respeta el glosario.

---

## BOY SCOUT (consecuencia SaMD §5.7 — mantenibilidad)

Cuando completes una tarea o modifiques un archivo:

* **Dejá el código más limpio que lo encontraste, de forma oportunista — no es obligatorio en cada archivo.** Si ves deuda chica y evidente en el archivo tocado (imports no usados, `any`, función >80 LOC sin justificación), limpiala. **Pero si limpiarla infla el diff de un fix puntual** (extraer un archivo, tocar lógica de negocio no relacionada), NO lo hagas ahí: anotá la deuda en `TECHNICAL_DEBT_SUMMARY.md` y atacala en una sesión dedicada (skill `/mesa-ingenieros`). Más superficie tocada = más riesgo de regresión en código médico; un "fix de lint" no debe terminar siendo un refactor de módulo. (La versión obligatoria de esta regla se probó y se descartó: empujaba refactors de más en fixes puntuales.)
* **Documentá y actualizá** el Master Map y el DHF. La documentación va junto con el cambio, no en sprints aparte.

---

## ANÁLISIS DE IMPACTO ANTES DE DECLARAR "ARREGLADO" (consecuencia SaMD §5.6)

* **Búsqueda global obligatoria** cuando modifiques un parámetro, retorno, schema o constante: `grep` en todo el repo para encontrar TODOS los consumidores. (Para el análisis de impacto de un símbolo puntual: skill `/samd-trace`.)
* **EL ENCHUFE, no solo la pieza — «¿el camino real usa MI versión?»** La búsqueda de consumidores responde *quién usa este símbolo*; esta responde *si lo que escribiste es lo que se ejecuta*. Un arreglo puede estar impecable y **perfectamente testeado en aislamiento** y aun así no proteger nada porque **nadie lo llama** (se escribió el helper y no se enganchó al flujo) o porque **se llama a otra versión** (un `__init__` que reexporta la función cruda hace que reasignar el alias dentro del módulo no cambie nada, y el arreglo queda escrito pero MUERTO). Los tests unitarios de la pieza pasan verdes en ambos casos. Por eso, antes de declarar "arreglado": **(a)** un test que recorra el **flujo real** (endpoint/servicio de entrada), no solo la unidad nueva; **(b)** si el símbolo tiene **dos rutas de import**, verificá que apuntan al MISMO objeto y anclalo con un test.
* **Saboteá el ENCHUFE, no solo la lógica**: en la verificación adversarial, además de romper el cuerpo de la función, **borrá su llamada del flujo** y confirmá que algo rojea. El sabotaje de la lógica pasa aunque el arreglo esté desconectado; el del enchufe es el que lo caza.
* **Cambio de endpoint** → actualizá inmediatamente su consumidor en el frontend, regenerá tipos del contrato (OpenAPI u equivalente) si aplica.
* **Regenerá el contrato (OpenAPI u equivalente) desde un `git worktree` limpio, no del working tree**, cuando haya sesión paralela sin commitear — código ajeno a medio terminar puede colarse en el contrato publicado. Si tu framework publica docstrings de rutas como descripción del contrato, tocarlos también dispara drift. NUNCA usar `git stash` para esto.
* **Verificación obligatoria** antes de declarar verde: corré los tests locales vinculados y reportá números.
* **Revisión asistida del diff**: ante un cambio no trivial, ofrecé al dueño pasar el diff por `/code-review` (caza bugs en lo cambiado) — y `/security-review` si toca auth/PHI/cifrado/superficie de red — antes de declarar verde. Complementan a `/samd-trace` (impacto de un símbolo) y a los tests; no los reemplazan.
* **Reorg de carpetas en `docs/`** → tras renombrar/mover cualquier `.md`, correr el link-checker cross-doc (`grep -rEn "\(\.{1,2}/[^)]+\.md" docs/`) y resolver enlaces rotos en el mismo PR. **Ningún PR de reorg cierra sin que el link-checker reporte 0 broken.**
* **TRACEABILITY_MATRIX_SAMD.md** → cada REQ-XXX en la matriz debe apuntar a `archivo:línea` verificable + nombre de test que existe HOY. Frases vagas sin path NO son trazabilidad SaMD aceptable. Un auditor externo lo levanta primero.
* **Propagación de reglas y valores de config — anti-drift de la fuente de verdad**: cuando cambies una **regla viva** o un **valor de configuración volátil**, propagalo en la **MISMA pasada** a TODOS sus espejos: `CLAUDE.md`, `.claude/rules/*.md`, `.claude/agents/*.md`, `.claude/commands/*.md`, `.claude/skills/*/SKILL.md`, docs DHF y memoria. **El código es la fuente de verdad** — los demás citan el valor + apuntan al archivo, no lo recopian. Antes de cerrar: `grep` el valor/regla vieja en `CLAUDE.md .claude/ docs/` → **0 residuos**, y verificá que ningún lugar contradiga a otro. Una regla que se contradice a sí misma entre dos archivos es peor que no tenerla.

---

## CIERRE DE BLOQUE GRANDE

* **SALVAGUARDA SIEMPRE-ON — no depende de acordarse de invocar la skill.** Antes de declarar cerrado **cualquier** bloque o PR —incluso si parece "solo docs" o "solo config"— pasá por: **(1) trazabilidad** — `TECHNICAL_DEBT_SUMMARY` + Master Map + `ISO_14971_RISK_MATRIX` (si toca el producto: algoritmo clínico, schema, regla de negocio, seguridad) **o** `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN` + Master Map (si cambia el **proceso/gobernanza**: agentes, reglas, skills, CI); **(2) verificación** — tests/CI vinculados con números reales.
* Al cerrar un **bloque grande** (sprint/fase): correr la foto de estado (`bash scripts/audit_project_state.sh`) ANTES de declarar cerrado, y NO cerrar con trabajo/deuda **vivo** sin anotar — el desfase entre "lo que creemos hecho" y "lo que está en producción" es la fuga real. El script solo INFORMA; borrar/archivar lo decide el dueño (destructivo con OK). Checklist canónico completo: skill `/cierre-bloque`.
* **Poda obligatoria de documentos vivos**: los docs DHF crecen por acumulación append-only y terminan siendo ilegibles (un `TECHNICAL_DEBT_SUMMARY` de cientos de KB no lo lee nadie, ni vos ni un auditor). En cada cierre, archivá en un `TECHNICAL_DEBT_HISTORY.md` toda sección con más de 30 días de antigüedad Y sin deuda referenciada en el índice de deuda VIVA (la sección completa, nunca una entrada suelta). Mismo principio para los changelogs del Master Map y la matriz de trazabilidad: van a un `_CHANGELOG.md` aparte. **Excepción `ISO_14971_RISK_MATRIX.md`**: su cuerpo por riesgo es una lista de controles **acumulada por diseño** (ISO 14971 §7-8), no deuda — no se poda; la intervención segura ahí es un índice de navegación aditivo.

### PRESUPUESTO DE ESCRITURA — la poda sola no alcanza

Podar lo viejo mientras cada lote añade decenas de líneas nuevas es vaciar con un dedal. Y una regla de poda que dice "en cada cierre de BLOQUE" se pospone para siempre, porque **un lote no es un bloque**. Por eso:

* **La poda corre en el cierre de CADA LOTE**, no de cada bloque, y se **reporta el número de secciones archivadas**. "0 archivadas" solo vale si el medidor dice 0 elegibles.
* **Fila del índice de deuda VIVA ≤ 2 líneas**: `ID | prioridad | UNA frase de qué está roto | enlace a su sección`. El análisis, la evidencia y el historial de intentos viven en la sección enlazada, **nunca dentro de la celda**. Una tabla es un índice, no un informe.
* **Sección de cierre de lote ≤ 40 líneas** en el doc vivo: qué se cerró, los números de verificación y el enlace. Lo que exceda **nace directamente en el archivo histórico** — no se escribe en el vivo "por ahora" para archivarlo después, porque ese "después" no llega.
* **Ficha de memoria ≤ ~6 KB y tablero vivo ≤ ~40 KB**: al añadir una tanda nueva, **comprimí las viejas en la misma pasada** (las cerradas y en producción bajan a 2-3 líneas + commit).
* **Verificación obligatoria antes de cerrar** (números, no impresión): `du -h` del doc tocado y `wc -l` de la sección añadida. Si el doc vivo **creció** en un cierre que también podaba, se reporta y se explica.

> Si un lote necesita más espacio que los topes, es señal de que el detalle va al histórico — no de subir el tope.
