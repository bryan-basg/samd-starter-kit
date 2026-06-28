# El método "Mesa de Ingenieros" — orquestar un equipo de agentes de IA bajo regulación

> **English abstract:** A battle-tested method for orchestrating a team of AI coding agents on a regulated (SaMD) codebase without losing coherence. The core risk with many agents isn't individual quality — it's *drift*. This documents the anti-drift protocol, when to parallelize vs serialize, and the hard rules a better model does not get to override.

Cuando empezás a repartir trabajo entre muchos agentes de IA, descubrís rápido que el problema **no es la calidad de cada agente** (cada uno trae sus reglas). El problema es la **pérdida de cohesión**: el orquestador recibe el resumen de *lo que el agente intentó hacer*, no del *cambio real que quedó en el código*. A eso lo llamamos *drift*, y es lo que hunde un equipo grande de agentes.

Este documento captura el método que funcionó en un proyecto SaMD real para tener paralelismo agresivo **sin** perder coherencia.

## La postura: paralelismo agresivo con cohesión

Repartir en muchos agentes en paralelo cuando la tarea lo permite (búsquedas anchas, auditorías, mutation por archivo, refactors multi-archivo independientes). Lanzar agentes en la nube no consume la máquina propia → no hay que pedir permiso por cada ola. Pero la calidad **no se relaja por ir más rápido**.

## El protocolo anti-drift (obligatorio con 2+ agentes)

Esta es la columna vertebral del método. Siete pasos:

1. **Leo el brief y el contexto yo mismo** (el orquestador). Delego la ejecución, **no** el entendimiento.
2. **Escribo el contrato compartido** en el chat — campos, tipos, paths, defaults, validaciones exactas — y **espero el OK del dueño** antes de lanzar nada.
3. **Brief a cada agente citando el contrato literal**, no parafraseado. La paráfrasis es la grieta por donde entra el drift.
4. **Tras cada agente, leo el `git diff` REAL**, no el resumen del agente. El resumen dice la intención; el diff dice la verdad.
5. **Si hay drift, mando UN agente correctivo** — no re-lanzo a todos. Re-lanzar multiplica el caos.
6. **Audito la trazabilidad** del changeset completo (con el agente auditor) antes de cerrar.
7. **Cierro con números reales** (tests, archivos, gaps de documentación), no con impresiones.

> La regla de oro, condensada: **leé el diff real, no el resumen.** Si te quedás con una sola cosa de este método, que sea esa.

## Verificación adversarial (la regla SaMD que cambia todo)

Cuando un agente afirma un hallazgo que dispararía un cambio en **algoritmo clínico, schema, regla de negocio o flujo de seguridad**, otro agente independiente tiene que **intentar refutarlo** antes de actuar.

Un hallazgo no verificado **no es** "un bug encontrado" — es una hipótesis. Bajo regulación (IEC 62304 §5.6), actuar sobre una hipótesis no refutada es exactamente lo que produce los falsos arreglos. El kit trae esto codificado en el workflow `samd-review`: cada hallazgo se refuta con un agente escéptico antes de reportarse.

## Cuándo paralelizar y cuándo serializar

**Paralelizá** cuando las tareas son independientes y el contrato es estable: búsquedas, auditorías por dimensión, mutation por archivo, refactors que no se pisan.

**Serializá** (un agente por vez) cuando:
- El contrato es complejo o cambiante (cada agente necesita ver el resultado del anterior).
- Hay dependencia de tipos generados (ej. un contrato OpenAPI que se regenera).
- El símbolo tocado cruza 3+ capas (un cambio en una rompe a las otras).

## Diseño del equipo: muchos agentes no es gratis

La sobrecarga de coordinar crece rápido (aprox. N²: más agentes = más decisiones de "cuál hace qué" + más diffs que revisar + más drift posible). El equipo se **diseña con disciplina, no se infla**:

- **Tamaño:** un puñado de especialistas permanentes por **capa** (datos, API, UI, plataforma, testing, seguridad, auditoría regulatoria, escritura documental). Antes de crear uno nuevo: ¿es una capa diferenciable? ¿tiene reglas duras propias, no 80% solapadas? ¿la frecuencia justifica el costo? Si alguna falla, ampliá uno existente.
- **Cuál elegir en solapamiento:** gana el más específico (un especialista de mutation > el de backend para una tarea de mutation). Empate → el más regulatorio.
- **Cuándo NO delegar:** tarea que cruza 4+ capas con dependencias; diagnóstico abierto sin hipótesis; iteración de UX en vivo con el dueño; cambio de 1-2 líneas. Eso lo hace el chat principal.
- **Señales de equipo inflado (parar y consolidar):** pasás más tiempo decidiendo *cuál* agente que trabajando; dos agentes editan el mismo archivo; el dueño pierde el hilo; la síntesis de los diffs deja de ser manejable.

## Las reglas duras que un modelo mejor NO anula

Estas no son limitaciones de inteligencia — son **mecánica, factura y contrato**. Un modelo más capaz no las deroga:

1. **El motor de mutation nunca corre en paralelo con agentes que escriben tests** (congela la lista de tests en su dry-run; los nuevos no entran).
2. **Procesos pesados locales piden OK cada vez** (consumen la CPU de la máquina del dueño; "vamos con todo" cubre el plan, no los subprocesos pesados implícitos).
3. **Fugas de estado por mocks globales** entre tests: verificar la suite completa antes de cantar verde.
4. **Atacar el umbral por archivo, no en superficie** (un irreducible se resuelve con refactor mínimo, no relajando el target).
5. **La suite de mutation es load-bearing:** tocar el literal de producción obliga a tocar su killer en el mismo PR.

## Por qué esto importa bajo regulación

Sin este método, un equipo de agentes produce mucho código rápido y **pierde la trazabilidad** — justo lo que SaMD prohíbe. El método existe para que la velocidad de N agentes no destruya la cohesión que IEC 62304 §5.6/§5.7 exige. Velocidad **y** trazabilidad, no una a costa de la otra.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
