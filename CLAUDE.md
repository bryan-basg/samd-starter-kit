# ONBOARDING DE AGENTE — {{PROJECT_NAME}} (SaMD)

> **Plantilla del SaMD Starter Kit.** Reemplazá los marcadores `{{...}}` con los valores de tu proyecto
> (o corré `bash scripts/init_kit.sh`, que los reemplaza en todo el repo, incluidas las reglas de `.claude/rules/` y el estilo de `.claude/output-styles/`).
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

Las secciones que siguen —y las **reglas en `.claude/rules/`** y el **estilo de salida «Orquestador SaMD»** (solo la sesión principal)— son **CONSECUENCIAS PRÁCTICAS** de la Regla 0. No son reglas independientes que el dev puede priorizar a gusto.

---

## MAPA DE ESTE CEREBRO — core + reglas en `.claude/rules/` + estilo de la sesión principal

Este `CLAUDE.md` (**core**) guarda la **espina de comportamiento** que aplica a cada turno sin importar qué archivo se toca —en la sesión principal **y en cada subagente**—: Regla 0, reglas comunes, empatía, boy scout, análisis de impacto y cierre de bloque.

El resto vive en tres lugares, según **quién** lo necesita:

**① Path-scoped** (frontmatter `paths:`) — **cargan solo cuando el agente lee/edita un archivo de esa capa**, aligerando el contexto cuando no se toca:

| Regla | Archivo | Carga automática al tocar |
| --- | --- | --- |
| Estándares del backend | `.claude/rules/backend.md` | `app/`, `alembic/`, `scripts/` (`*.py`) |
| UX clínica y accesibilidad | `.claude/rules/frontend-ux.md` | `frontend/src/**/*.{ts,tsx,css}` |
| Testing (verificación SaMD §5.7) | `.claude/rules/testing.md` | tests frontend/backend + configs de test |
| CI / GitHub Actions | `.claude/rules/github-actions.md` | `.github/workflows/*.yml` |
| Documentación del DHF | `.claude/rules/docs.md` | `docs/**/*.md` |

**② Transversales en archivo aparte** (SIN `paths:`) — **cargan siempre, igual que el core, y también en CADA subagente, que las relee en cada turno**. Por eso en ellas va solo lo que obedecen todos:

| Regla | Archivo |
| --- | --- |
| Reglas duras de ejecución + higiene de contexto + antes de cantar verde | `.claude/rules/orquestacion.md` |
| Comandos core | `.claude/rules/comandos.md` |

**③ Estilo de salida «Orquestador SaMD»** (`.claude/output-styles/orquestador.md`, activado por `outputStyle` en `.claude/settings.json`) — **solo la sesión principal** (los subagentes corren su propio prompt y no lo cargan): §1 cómo trabajar con {{OWNER}} (idioma y registro, modo tutor, antes de actuar), §2 orquestación (delegar y matriz de agentes, postura, anti-drift, reglas A-F), §3 sesiones paralelas (carriles y reglas de convivencia). Sacarlo de lo que heredan los agentes evita que cada uno relea, en cada turno, reglas que solo usa quien habla con el dueño u orquesta (SCMP §2.1).

**Salvaguarda SaMD:** todas son **CONSECUENCIAS PRÁCTICAS de la Regla 0** — no son opcionales. Al **razonar** sobre una capa sin haber abierto todavía un archivo (planeando, respondiendo una pregunta), tené presente que esa capa tiene reglas duras: **abrí el archivo o leé la regla antes de decidir**. Los agentes de `.claude/agents/` ya traen su regla de capa precargada, así que delegar al especialista nunca pierde la regla.

**Dónde va una regla nueva:** una regla de una capa concreta va a su archivo path-scoped en `.claude/rules/`; una regla que aplica siempre —también a los agentes— va al core (o a un rule transversal sin `paths:`); una que solo usa la sesión principal (cómo hablar con el dueño, cómo orquestar) va al estilo. **Nunca al revés** — una regla de capa en el core infla el contexto de todos los turnos; una regla universal escondida en un path-scoped o en el estilo no se lee cuando hace falta.

---

## REGLAS COMUNES (sesión principal y agentes)

> **Cómo se habla con {{OWNER}}, cómo se orquestan agentes y cómo conviven varias ventanas** vive en el estilo de salida **«Orquestador SaMD»** (`.claude/output-styles/orquestador.md`), que carga **solo la sesión principal**. ⚠️ **Si sos la sesión principal y ese estilo NO está entre tus instrucciones** (alguien cambió el `outputStyle` o lo desactivó), **leé ese archivo entero antes de responder**: sus reglas siguen siendo obligatorias.

* **Lo que se escribe para {{OWNER}} —incluidos los informes de los agentes— va en {{CHAT_LANG}}, también cuando la fuente está en inglés**: traducí ANTES de escribir. En código, tests y `docs/` el tecnicismo y la precisión son obligatorios (SaMD).

### Git y commits
* **Nunca commitees ni pushees sin que el dueño lo pida.** Antes de cada commit, reportá qué archivos se suben y esperá su OK. Ningún agente commitea/pushea — esa decisión es exclusiva del dueño.
* **Nunca pushees a remoto sin autorización explícita**, aunque ya esté commiteado local.
* **Operaciones destructivas** (`reset --hard`, `push --force`, borrar branches) → pedí OK aunque parezcan inocuas.
* **Tras un push a la rama principal, no hagas un segundo push hasta que el CI del primero termine.**
* **Commit selectivo con sesión paralela activa**: `git add` **EXPLÍCITO** de tus archivos (nunca `-A` / `-u`) **y confirmá con `git commit -m "<msg>" -- <tus rutas>`**. ⚠️ **El `git add` explícito NO basta, y esto es mecánica de git, no descuido**: el índice es **UNO por repositorio**, así que si la otra ventana ya preparó SUS archivos, un `git commit` normal —aunque vos solo hayas hecho `add` de los tuyos— **se lleva también los suyos**, dentro de un commit cuyo mensaje no los describe. La forma con rutas ignora el índice para todo lo demás y deja intacto lo que la otra ventana tenía preparado. Comprobación previa innegociable: `git diff --cached --name-only` **justo antes de commitear** — si aparece algo que no es tuyo, la forma con rutas es obligatoria. Convivencia completa entre ventanas: estilo «Orquestador SaMD» §3. Aparte: tras revertir un PR grande, verificá qué sub-cambios NO volvieron (pueden haber quedado solo en la rama revertida).
* **Comandos que el clasificador de permisos bloquea → los corre el dueño** (con `!` o a mano): operaciones sobre secretos productivos vivos, el primer push tras un OK vago, alta de infraestructura sensible (runners, credenciales). El agente prepara el comando/YAML; el dueño lo ejecuta.

### Zonas off-limits
* **Zonas del producto marcadas off-limits por el dueño = prohibido tocar sin pedido dirigido.** Un "vamos con todo" sobre un módulo NO autoriza cruzar a una zona declarada aparte (ej. el código de cara al usuario final si el pedido era solo sobre el panel interno/admin). Si una utility global de la zona que estás tocando cae en cascada sobre una zona off-limits, avisá ANTES de aplicar el cambio.

### Diagnóstico de bugs (verificar antes de fixear)
* **Verificá antes de fixear**: ante un bug reportado, investigá primero — no saltes a escribir código.
* **Bug tras un deploy** → revisá logs estructurados de la plataforma cloud **antes** de teorizar sobre cache/Service Worker/navegador.
* **Bug solo en el dispositivo móvil (no en PC)** → conectate vos por las herramientas de depuración remota y capturá la petición/respuesta desde la terminal. No guíes al dueño paso a paso por un inspector que no usa a diario.

### Memoria vs este documento (anti-saturación)
* Este `CLAUDE.md`, `.claude/rules/` y el estilo «Orquestador SaMD» = reglas **ESTABLES** (bugs conocidos, comandos, protocolo, valores de config que apuntan al código). Los **snapshots dinámicos** (estado de tests, hallazgos de sesión, lecciones puntuales, estado del plan) van en la **memoria del agente** (`memory/MEMORY.md`), NO acá — para no inflar el documento. El procedimiento de escritura (filtro de qué va y qué no, ficha por tema, compresión del índice en la MISMA pasada y verificación con números): skill `/memoria`.

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

## ARREGLAR, NO ENVOLVER (consecuencia SaMD §5.7 — mantenibilidad)

**Prohibido apilar código de protección alrededor de la lógica existente cuando el arreglo real es REESCRIBIRLA.** Validadores explícitos de más, estructuras defensivas, tipados estrictos puestos como muleta y envoltorios locales (`safeX`, `validatedX`) **no son arreglos**: son una capa que tapa el defecto y lo deja volver por la puerta de al lado.

**El filo — esto NO deroga la validación obligatoria.** Siguen siendo innegociables: **(a)** la validación de **FRONTERA** (dato externo entrando: schema de request, validador del cliente, tope de escritura) — una vez, donde entra; **(b)** el **fail-safe clínico** declarado (ISO 14971: degradar hacia MÁS alerta, estado `estimated`/`unclassified`, fusible 503) — eso es conducta del producto, no protección de código; **(c)** las **guardas de seguridad en el punto de decisión** (JWT, portero de acceso). *La legítima vive en la frontera y corre UNA vez; la prohibida vive encima de la lógica y se repite porque nadie confía en lo que hay debajo.*

**Test decisivo, antes de dar por cerrado cualquier arreglo defensivo:** *si alguien llama mañana a la función original **saltándose** mi envoltorio, ¿vuelve el defecto?* Si la respuesta es sí, escribiste un consejo, no un control. Jerarquía, de mejor a peor: **hacer el estado imposible** (un tipo que no compila si falta un caso) → **puerta única derivada** que todos los consumidores usan → **validar en la frontera** → ❌ envolver el uso.

**Válvula honesta:** si de verdad no se puede reescribir (la frontera, el fail-safe, o el productor es de terceros), se justifica **en el propio código**. «No me animo a tocarlo» / «rompe muchos tests» **no es justificación: es una ficha de deuda** en `TECHNICAL_DEBT_SUMMARY.md`. Un envoltorio sin ficha es deuda invisible. Las 6 señales de que estás envolviendo y el procedimiento de 5 pasos: skill **`/arreglar-no-envolver`**.

---

## ANÁLISIS DE IMPACTO ANTES DE DECLARAR "ARREGLADO" (consecuencia SaMD §5.6)

* **Búsqueda global obligatoria** cuando modifiques un parámetro, retorno, schema o constante: `grep` en todo el repo para encontrar TODOS los consumidores. (Para el análisis de impacto de un símbolo puntual: skill `/samd-trace`.)
* **EL ENCHUFE, no solo la pieza — «¿el camino real usa MI versión?»** La búsqueda de consumidores responde *quién usa este símbolo*; esta responde *si lo que escribiste es lo que se ejecuta*. Un arreglo puede estar impecable y **perfectamente testeado en aislamiento** y aun así no proteger nada porque **nadie lo llama** (se escribió el helper y no se enganchó al flujo) o porque **se llama a otra versión** (un `__init__` que reexporta la función cruda hace que reasignar el alias dentro del módulo no cambie nada, y el arreglo queda escrito pero MUERTO). Los tests unitarios de la pieza pasan verdes en ambos casos. Por eso, antes de declarar "arreglado": **(a)** un test que recorra el **flujo real** (endpoint/servicio de entrada), no solo la unidad nueva; **(b)** si el símbolo tiene **dos rutas de import**, verificá que apuntan al MISMO objeto y anclalo con un test.
* **Saboteá el ENCHUFE, no solo la lógica**: en la verificación adversarial, además de romper el cuerpo de la función, **borrá su llamada del flujo** y confirmá que algo rojea. El sabotaje de la lógica pasa aunque el arreglo esté desconectado; el del enchufe es el que lo caza.
* **Cambio de endpoint** → actualizá inmediatamente su consumidor en el frontend, regenerá tipos del contrato (OpenAPI u equivalente) si aplica.
* **Regenerá el contrato (OpenAPI u equivalente) desde un `git worktree` limpio, no del working tree**, cuando haya sesión paralela sin commitear — código ajeno a medio terminar puede colarse en el contrato publicado. Si tu framework publica docstrings de rutas como descripción del contrato, tocarlos también dispara drift. NUNCA usar `git stash` para esto.
* **Verificación obligatoria** antes de declarar verde: corré los tests locales vinculados y reportá números.
* **Revisión asistida del diff**: ante un cambio no trivial, ofrecé al dueño pasar el diff por `/code-review` (caza bugs en lo cambiado) — y `/security-review` si toca auth/PHI/cifrado/superficie de red — antes de declarar verde. Complementan a `/samd-trace` (impacto de un símbolo) y a los tests; no los reemplazan.
* **Documentación (`docs/`)**: tras una reorg, link-checker (`bash scripts/check_doc_links.sh`), anclas (`python3 scripts/check_doc_anchors.py`) **y** citas al código por nombre (`python3 scripts/check_doc_citations.py`) con **0 rotos** en el mismo PR; cada REQ de `TRACEABILITY_MATRIX_SAMD.md` apunta a una cita verificable + un test que existe HOY. El detalle vive en `.claude/rules/docs.md` (carga al tocar `docs/**/*.md`; **si editás docs por script, abrila antes**).
* **Propagación de reglas y valores de config — anti-drift de la fuente de verdad**: cuando cambies una **regla viva** o un **valor de configuración volátil**, propagalo en la **MISMA pasada** a TODOS sus espejos: `CLAUDE.md`, `.claude/rules/*.md`, `.claude/agents/*.md`, `.claude/commands/*.md`, `.claude/skills/*/SKILL.md`, docs DHF y memoria. **El código es la fuente de verdad** — los demás citan el valor + apuntan al archivo, no lo recopian. Antes de cerrar: `grep` el valor/regla vieja en `CLAUDE.md .claude/ docs/` → **0 residuos**, y verificá que ningún lugar contradiga a otro. Una regla que se contradice a sí misma entre dos archivos es peor que no tenerla.

---

## CIERRE DE BLOQUE GRANDE

* **SALVAGUARDA SIEMPRE-ON — no depende de acordarse de invocar la skill.** Antes de declarar cerrado **cualquier** bloque o PR —incluso si parece "solo docs" o "solo config"— pasá por: **(1) trazabilidad** — `TECHNICAL_DEBT_SUMMARY` + Master Map + `ISO_14971_RISK_MATRIX` (si toca el producto: algoritmo clínico, schema, regla de negocio, seguridad) **o** `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN` + Master Map (si cambia el **proceso/gobernanza**: agentes, reglas, skills, CI); **(2) verificación** — tests/CI vinculados con números reales.
* Al cerrar un **bloque grande** (sprint/fase): correr la foto de estado (`bash scripts/audit_project_state.sh`) ANTES de declarar cerrado, y NO cerrar con trabajo/deuda **vivo** sin anotar — el desfase entre "lo que creemos hecho" y "lo que está en producción" es la fuga real. El script solo INFORMA; borrar/archivar lo decide el dueño (destructivo con OK). Checklist canónico completo: skill `/cierre-bloque`.
* **Poda obligatoria de documentos vivos**: los docs DHF crecen por acumulación append-only y terminan siendo ilegibles. **La poda corre en el cierre de CADA LOTE** (no solo de cada bloque: un lote no es un bloque) y se **reporta el número de secciones archivadas** ("0 archivadas" solo vale si el medidor dice 0 elegibles). Qué se archiva, a dónde, y la excepción de `ISO_14971_RISK_MATRIX.md` → `.claude/rules/docs.md`.

### PRESUPUESTO DE ESCRITURA — la poda sola no alcanza

Podar lo viejo mientras cada lote añade decenas de líneas nuevas es vaciar con un dedal. Por eso hay topes:

* **Documentos vivos** (tope de la fila del índice de deuda y de la sección de cierre de lote; el detalle excedente nace en el histórico): los valores viven en `.claude/rules/docs.md`, no se copian acá.
* **Ficha de memoria ≤ ~6 KB y tablero vivo ≤ ~40 KB**: al añadir una tanda nueva, **comprimí las viejas en la misma pasada** (las cerradas y en producción bajan a 2-3 líneas + commit).
* **Verificación obligatoria antes de cerrar** (números, no impresión): `du -h` del doc tocado y `wc -l` de la sección añadida. Si el doc vivo **creció** en un cierre que también podaba, se reporta y se explica.

> Si un lote necesita más espacio que los topes, es señal de que el detalle va al histórico — no de subir el tope.

---

## INSTRUCCIONES DE COMPACTACIÓN (al resumir la conversación)

Cuando una sesión larga se resume (a mano con `/compact` o sola, al llegar al umbral de contexto que tengas configurado), el resumen decide qué recuerda la sesión siguiente. Al resumir, conservá **literal**: (1) cada OK o decisión de {{OWNER}} **con su alcance** (plan vs gasto, qué zona autorizó); (2) los archivos tocados y si están commiteados o pusheados; (3) los IDs de fichas (`D-XXX`) y riesgos tocados; (4) los números de tests con el comando que los dio; (5) el carril de la ventana y los agentes o procesos en curso; (6) lo pendiente. Lo que ya está resumido en esos seis puntos (salidas de herramientas, lecturas de archivos) se descarta.

**Por qué importa en SaMD:** un resumen que pierde el *alcance* de un OK ("autorizó el plan" se vuelve "autorizó todo") convierte una decisión del dueño en un permiso que nunca dio; y uno que pierde los números de verificación obliga a declarar "verde" sin evidencia (§5.7).
