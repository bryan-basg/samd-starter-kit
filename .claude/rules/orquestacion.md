# ORQUESTACIÓN MULTI-AGENTE (consecuencia SaMD §5.6 análisis de impacto + §5.7 verificación)

> Regla **transversal** del cerebro SaMD, en archivo aparte solo por legibilidad del core — **NO lleva `paths:`**, así que carga en cada sesión igual que `CLAUDE.md`. Mapa completo: `CLAUDE.md` §MAPA DE ESTE CEREBRO. Esto es **un agente repartiendo sub-agentes**; que el dueño tenga varias ventanas abiertas a la vez es otra cosa y vive en `.claude/rules/sesiones-paralelas.md`.

## Postura: paralelismo agresivo con cohesión

* **Repartir en muchos agentes en paralelo** cuando la tarea lo permita (búsquedas anchas, mutation por archivo, auditorías, refactors multi-archivo independientes). Lanzar agentes **no consume la máquina del dueño** → no cae bajo "procesos pesados", no pedir OK por cada ola.
* **Verificación adversarial OBLIGATORIA sobre hallazgos clínicos/seguridad** (§5.6): un hallazgo que dispara cambio en algoritmo clínico, schema, regla de negocio o flujo de seguridad debe ser refutado por otro agente independiente antes de actuar. Hallazgo no verificado ≠ "arreglado".
* **A los agentes verificadores NO les des capacidad de sub-delegar.** Un verificador que puede lanzar sub-agentes se queda esperándolos y aparenta estar colgado; peor, un reporte de estado intermedio puede leerse como resultado final.
* **Encadenar sub-pasos sin micro-confirmar** tras un OK de plan ("vamos", "vamos con todo").
* **`worktree`** cuando varios agentes muten archivos en paralelo y puedan pisarse. **No dejes el `cwd` dentro de un worktree antes de lanzar agentes**: heredan el cwd y editan archivos DENTRO del worktree en vez del repo — volvé al repo raíz antes de repartir.
* **Tamaño de ola**: escalar a lo que la tarea justifique. La calidad **no se relaja por ir más rápido**.

## Reglas duras que un modelo mejor NO anula (mecánica, no torpeza)

Estas no son limitaciones del modelo: son mecánica de las herramientas, factura o contrato regulatorio. Un modelo más capaz las sigue teniendo que respetar.

1. **El motor de mutación nunca en paralelo con agentes que escriben tests** *(herramienta)*: el motor congela la lista de tests en su arranque; los tests nuevos no entran. Patrón correcto: agentes → suite verde → **entonces** mutación.
2. **Procesos pesados locales piden OK CADA vez** *(CPU del dueño)*: mutación, fuzz, suites completas, escaneos de seguridad. "Vamos con todo" cubre el plan, **no** los subprocesos pesados implícitos. (Los agentes en la nube NO entran acá.)
3. **Fugas de estado entre tests con mocks globales** *(herramienta)*: los mocks de módulos globales con closure local se filtran entre archivos. Verificar la suite **COMPLETA** antes de cantar verde; el `worktree` mitiga pero no exime.
4. **Checklist físico antes de una corrida de mutación completa** *(hardware)*: refrigeración OK, navegador cerrado, sin runners en paralelo, procesos de fondo matados, concurrencia = núcleos − 4.
5. **Los tests killer de mutación son load-bearing** *(contrato SaMD §5.7)*: los literales empáticos, logs, etiquetas ARIA y fórmulas que un killer verifica son **contratos verificados**. Tocar el literal de producción obliga a tocar su killer en el mismo PR. Aflojar killers sin justificación SaMD documentada: prohibido.

## Protocolo anti-drift (OBLIGATORIO con 2+ agentes)

Con 2+ agentes el riesgo no es la calidad individual (cada uno trae sus reglas) sino la **pérdida de cohesión**: el orquestador recibe summaries de *lo que el agente intentó*, no del *diff real*. **Regla dura: escribí el contrato compartido (campos/tipos/paths/defaults exactos) con OK del dueño antes de lanzar; tras cada agente leé el `git diff` REAL, nunca el summary; drift → 1 agente correctivo (no re-lances a todos). Serializá (no paralelices) si el contrato es complejo/cambiante, hay tipos generados (OpenAPI o equivalente) o un símbolo cruza 3+ capas.** Procedimiento completo (los 7 pasos + reglas de cohesión): skill `/anti-drift`.

## Diseño de equipo — reglas A-F

Muchos agentes NO es gratis (sobrecarga del orquestador ≈ N², tokens, drift, solapamiento). El equipo se diseña con disciplina, no se infla.

**Palanca de costo/velocidad — enrutar modelo por agente**: no todo agente necesita el modelo tope. Mandá los sub-pasos baratos y de alto volumen a un modelo económico, el grueso agéntico a uno intermedio, y reservá el modelo tope para lo clínico/crítico y la recuperación de errores. Reducir la *cantidad* de agentes no es la única palanca — el *mix* de modelos es la otra.

* **A — Tamaño**: **sin tope numérico fijo.** El número de agentes en disco no cuesta por sí solo; el costo real es el **solapamiento** (dos agentes pisándose) y que el orquestador pierda tiempo decidiendo CUÁL. El portón para crear uno nuevo es **3 SÍ rotundos**: ¿capa diferenciable? ¿reglas duras distintas (no 80% solapamiento)? ¿la frecuencia justifica el costo? Si alguna falla → ampliar uno existente, no crear. El "¿cuándo es demasiado?" lo responde la regla **F**, no un número.
* **B — Paralelo por turno**: tope duro **12**. No es capricho: es el techo de coordinación del orquestador (overhead ≈ N²) más el presupuesto de tokens. Las verificaciones factuales simples (¿existe X en `archivo:línea`?) se hacen por lectura directa del orquestador, **NO** con un agente. A más agentes simultáneos, más rigor anti-drift.
* **C — Cuándo lanzar** (los 3 a la vez): capa identificable + tarea de ≥3 pasos no triviales + brief cerrado. Si falta alguno → chat principal.
* **D — Cuál gana en solapamiento**: **el más específico** (`qa-mutation` > `backend` para mutación; `clinical-algorithms` > `backend`/`db-architect` para lógica clínica y scoring — pero la mecánica de migraciones sigue en `db-architect`; `e2e-integration` > `frontend` para pruebas de extremo a extremo — unidad/componente sigue en `frontend`, mutación en `qa-mutation`, infra del runner en `cloud-ops`). Empate → el más regulatorio (`docs-dhf` > `samd-audit-trace`). Sigue el empate → decide el chat principal y lo documenta.
* **E — Fallback al chat principal** (NUNCA delegar): la tarea cruza 4+ capas con dependencias; diagnóstico abierto sin hipótesis (saltar al fix antes del diagnóstico falla); iteración de UX en vivo con el dueño; cambio de 1-2 líneas.
* **F — Señales de equipo inflado** (parar y consolidar): >30% del tiempo decidiendo CUÁL agente; dos agentes editando el mismo archivo; el dueño pierde el hilo; la síntesis del diff deja de ser manejable; re-invocaciones correctivas por briefs mal armados (deberían ser 0).
