# Disciplina de arranque — qué priorizar antes de escribir código

> **English abstract:** What to prioritize in the first days of a Class B SaMD project: a
> compliance-first mindset, memory discipline, shipping discipline, avoiding over-building before
> validation, calibrated security judgment, and empathetic UX as a clinical decision — not a
> cosmetic one. This document is the process/mindset layer that sits *around* its two siblings: it
> does not repeat the technical war stories in [`PRODUCTION_LESSONS.md`](PRODUCTION_LESSONS.md) nor
> the agent-orchestration method in
> [`MULTI_AGENT_ENGINEERING_METHOD.md`](MULTI_AGENT_ENGINEERING_METHOD.md) — it points to them where
> relevant and covers what they don't.

Estas son las decisiones de **proceso y criterio** que definen si un equipo (con o sin agentes de
IA) construye un SaMD con disciplina desde el día 1, o lo descubre tarde y caro. Generalizadas de
experiencia real, sin datos del producto de origen.

Formato flexible: **Síntoma → Causa → Lección** cuando la lección nació de un incidente concreto;
solo **Lección** cuando es una práctica que conviene adoptar de entrada, sin esperar el golpe.

---

## Cumplimiento primero, código después

### Sin una jerarquía explícita, el cumplimiento pierde contra la fecha de entrega

- **Síntoma:** trazabilidad y análisis de impacto que se van posponiendo "para la próxima", release
  tras release, hasta que un auditor los pide y no están.
- **Causa:** no había una regla explícita de que el cumplimiento gana cuando choca con la
  conveniencia técnica — quedaba a criterio de cada momento, y el criterio siempre cede ante la
  urgencia del día.
- **Lección:** escribí una "Regla 0" al principio de tus instrucciones del proyecto: *toda decisión
  técnica se subordina al cumplimiento*. Que cada regla operativa del documento se lea como
  consecuencia práctica de esa regla, no como algo negociable aparte.

### La trazabilidad que se pospone no llega nunca

- **Lección:** cada cambio en algoritmo clínico, esquema de datos, regla de negocio o flujo de
  seguridad se registra en tus documentos regulatorios (matriz de riesgos, deuda técnica, mapa
  maestro) **en el mismo cambio**, no en un sprint aparte. Cada requisito debe apuntar a
  `archivo:línea` verificable y a un test que existe HOY — "validado por [autoridad]" sin ruta no es
  trazabilidad aceptable ante un auditor.

### El código es la fuente de verdad; los documentos lo citan, no lo copian

- **Síntoma:** un valor de configuración (un umbral, un límite) dice una cosa en un documento y otra
  en el código, y nadie nota la contradicción hasta que alguien confía en el documento equivocado.
- **Causa:** al cambiar el valor en el código, no se propagó a todos sus espejos en la misma pasada.
- **Lección:** cuando cambies un valor vivo o una regla, propagalo de inmediato a TODOS sus espejos
  (instrucciones, docs, config de agentes) — pero que cada espejo *apunte* al valor en el código, no
  lo duplique. Una regla que se contradice entre dos archivos es peor que no tenerla.

---

## Verificación con evidencia, no con impresión

> El *cómo* coordinar un equipo de agentes sin perder cohesión (leer el diff real, verificación
> adversarial, cuándo paralelizar) ya está en
> [El método "Mesa de Ingenieros"](MULTI_AGENT_ENGINEERING_METHOD.md). Acá van dos hábitos de
> verificación que aplican más allá de coordinar agentes.

### Antes de preguntarle al dueño un hecho, buscalo vos

- **Lección:** si la duda es del tipo "¿esto se usa?", "¿corre X en producción?", el código deja
  huellas — imports, rutas, configs, logs. Buscá ahí primero. El dueño no recuerda cada detalle
  operativo, y devolverle la pregunta lo carga; preguntale solo lo que SOLO él sabe (decisiones de
  negocio, secretos, preferencias futuras).

### "Compila" no es verificación

- **Síntoma:** un cambio se declara listo porque corre sin errores.
- **Causa:** verificar solo que el código *arranca*, no que *se comporta* como debe.
- **Lección:** bajo SaMD la verificación es demostrable — corré la suite vinculada y reportá números
  reales (cuántos pasaron, cobertura si aplica) antes de declarar algo terminado. (Para las trampas
  técnicas específicas de testing y mutation, ver
  [Field Notes → Testing](PRODUCTION_LESSONS.md#testing-y-mutation).)

---

## Memoria: destilar, y desconfiar de tu propia nota

> La mecánica de cómo escribir una memoria vive en [`MEMORY.md`](../../memory/MEMORY.md). Acá van
> dos hábitos que la mecánica sola no te da.

### La memoria sin destilar se vuelve un pantano

- **Lección:** cada tanto, elevá las lecciones acumuladas: las reglas van al documento de
  instrucciones o a la config de los agentes; los procedimientos repetibles se vuelven "recetas"
  reutilizables; las fichas ya exprimidas se archivan. Un archivo de memoria que solo crece y nunca
  se destila deja de ser útil — nadie encuentra nada ahí.

### Tu nota dice "pendiente"; el repo puede decir otra cosa

- **Síntoma:** una nota de "esto sigue sin subir" resulta estar ya en producción desde hace días (o
  al revés).
- **Causa:** la nota es una foto del momento en que se escribió; el repo sigue cambiando después.
- **Lección:** antes de actuar sobre un pendiente anotado, reverificá contra el estado real de git
  (¿qué commit está en la rama de producción? ¿qué deploy corrió?). Nunca asumas que la nota sigue
  vigente solo porque está ahí.

---

## Subí a producción con disciplina

### Definí sin ambigüedad qué significa "subir"

- **Lección:** acordá una sola definición con el dueño (p. ej. "subir/publicar = llega a
  producción"). El dueño piensa en "lo que ven los usuarios", no en topología de git — pararlo a
  elegir ramas lo frustra. Gestioná esa complejidad vos.

### Un `git add` amplio se lleva puesto el trabajo ajeno

- **Síntoma:** un commit termina incluyendo cambios de otra sesión de trabajo que todavía no estaban
  listos, o un revert grande se lleva sub-cambios que quedan huérfanos solo en una rama.
- **Causa:** agregar "todo" al staging en vez de listar archivos explícitos.
- **Lección:** si el árbol tiene cambios de otra sesión sin commitear, agregá EXPLÍCITAMENTE tus
  archivos, nunca "agregar todo". Tras un revert grande, verificá qué NO volvió a producción.

### Las operaciones sin vuelta atrás piden confirmación explícita, sí o sí

- **Lección:** reset duro, force push, borrar ramas, DROP de columnas con datos — confirmación
  explícita siempre, por más inocuas que parezcan. Aislar el paso irreversible tras una confirmación
  manual es la única red que importa cuando no hay forma de deshacer.

### Los commits y pushes son decisión del dueño, no del agente

- **Lección:** el agente prepara todo y frena; el push lo da la persona. Mantiene control humano
  sobre lo que llega a los usuarios — sano bajo cualquier regulación. Y no encadenes pushes: esperá
  a que el CI del primero termine antes de lanzar el segundo.

---

## No sobre-construyas antes de validar

### La documentación puede estar mintiendo sobre el estado real

- **Síntoma:** un plan de trabajo dice "agregar X" cuando X ya existe, construido en otra capa que
  nadie miró antes de escribir el plan.
- **Causa:** se asumió ausencia sin buscar en todas las capas (un caso típico: mirar solo el
  frontend y concluir que "esta integración no existe", cuando estaba entera en el backend sin
  interfaz visible).
- **Lección:** reconciliá periódicamente lo que tu documentación dice como "pendiente" contra lo que
  el código realmente tiene. Nunca declares ausencia de algo sin haber buscado en TODAS las capas.

### El "% completo" inflado explota cerca de la certificación

- **Lección:** distinguí siempre tres estados — "confirmado real", "a medias" (ej. backend sí,
  interfaz no) y "ausente" (0 código). Un roadmap que dice "100%" donde la validación formal no está
  hecha genera sorpresas caras justo cuando menos conviene.

### Sumá herramientas por dolor real, no por moda

- **Lección:** antes de instalar tooling nuevo, preguntá qué agujero concreto tapa. A veces la mejor
  herramienta ya la tenés a medias construida y nadie lo sabe — revisá antes de sumar una más.

### El trabajo terminado que no llega a producción es deuda invisible

- **Lección:** la frustración más cara no suelen ser los bugs, sino bloques enteros terminados que
  viven en ramas y nunca se despliegan. Antes de declarar cerrado un bloque grande, corré una "foto
  del estado" del repo — y no cierres con deuda viva sin anotarla. (Regla del boy scout: al tocar un
  archivo, saldá al menos un pedazo de deuda — con herramientas para detectar imports muertos, no a
  ojo.)

---

## Seguridad: calibrá el riesgo, no solo la técnica

> Los fundamentos técnicos — identidad solo por token nunca por el cliente, secretos con doble
> fuente (`.env` local vs gestor de secretos en producción), logs de auditoría sin PII — ya están en
> [Field Notes → Seguridad](PRODUCTION_LESSONS.md#seguridad). Acá van dos decisiones de **criterio**
> que la técnica sola no resuelve.

### Una rotación de llave a medio camino es más peligrosa que no haberla empezado

- **Lección:** si arrancás a rotar la llave de cifrado de datos sensibles, completá la secuencia
  completa (llave nueva desplegada → re-cifrar histórico → retirar la vieja) o dejala en un estado
  estable y documentado — nunca a medias sin registro. Diseñá el cifrado con soporte de versiones
  desde el principio (blobs etiquetados, registro de llaves, script de re-cifrado idempotente con
  modo de prueba) para que rotar sea seguro y reversible.

### No todo hallazgo de seguridad pesa igual

- **Lección:** calibrá la severidad preguntando "¿este riesgo es contra mí/mi repo, o contra el
  usuario final del dispositivo?". Con un equipo chico y sin usuarios reales todavía, algunas cosas
  bajan de prioridad — pero NUNCA se relajan los vectores contra el usuario final, lo que corre en
  el cliente, los bloqueos regulatorios, ni los datos personales en logs. Y no justifiques urgencia
  con "los usuarios lo sufren" si todavía no hay usuarios: la razón válida para arreglar algo antes
  de tener usuarios es la higiene, no el impacto.

---

## UX empática es una decisión clínica, no cosmética

### Un placeholder copiado pasa todas las validaciones y falla igual

- **Síntoma:** la app muestra el idioma base en pantallas de otro idioma, a pesar de que el checador
  de traducciones da todo en verde.
- **Causa:** un script de emergencia copió el texto del idioma base como placeholder; la clave
  técnica existía, así que la paridad "pasaba", pero el contenido nunca se tradujo de verdad.
- **Lección:** tu validador de traducciones tiene que detectar DOS cosas: claves faltantes Y "valor
  idéntico al idioma base" (copiado sin traducir) — con una lista blanca para las coincidencias
  legítimas (marca, siglas).

### La accesibilidad no se negocia por estética

- **Lección:** respetá las preferencias de accesibilidad (como el movimiento reducido)
  incondicionalmente, en toda la interfaz. Mantené el offline-first real — nunca una pantalla en
  blanco por un error de red; siempre un estado útil y un reintento.

### "Unificar la estética" casi nunca se logra maquillando archivo por archivo

- **Síntoma:** una ronda de cambios cosméticos en varios archivos (pesos de fuente, bordes) no
  transforma nada perceptible, y termina revertida entera.
- **Causa:** confundir "pulir adornos" con "rediseño estructural" cuando el pedido real era lo
  segundo.
- **Lección:** ante un pedido de "unificá todo", preguntá si quieren pulir superficialmente (rápido,
  riesgo de no satisfacer) o copiar el molde estructural de una zona de referencia ya validada — y
  recomendá lo segundo cuando el pedido es a nivel "todo el panel".

---

## Un cambio se propaga distinto según el artefacto que lo recibe

### "Lo cambié y no se aplica" casi nunca es azar

- **Síntoma:** un cambio confirmado en el deploy no se ve para el usuario — o peor, algo que
  funcionaba deja de andar sin explicación aparente.
- **Causa:** una web que se refresca sola, una app instalada que hay que reconstruir, y una caché que
  sirve la versión vieja hasta que el usuario cierra y reabre, se actualizan cada una a su propio
  ritmo. Tratarlas como si fueran lo mismo genera falsas alarmas de "regresión".
- **Lección:** documentá el ciclo de actualización de cada artefacto de tu producto. Al confirmar un
  deploy, decile al dueño el paso EXACTO para verlo (cerrar/reabrir, reinstalar, reconstruir) — y
  antes de aceptar "no se aplicó" como bug, confirmá tres cosas: el deploy quedó en verde, no hay
  commits sin subir, y no es la caché/service worker sirviendo la versión anterior.

---

## Cierre

Ningún consejo de este documento salió de un manual: cada uno es un error que se convirtió en
regla, igual que sus dos documentos hermanos. La diferencia es la capa — [Field
Notes](PRODUCTION_LESSONS.md) te cubre las trampas técnicas, [Mesa de
Ingenieros](MULTI_AGENT_ENGINEERING_METHOD.md) te cubre cómo coordinar el equipo de agentes, y este
documento te cubre el criterio de fondo: cumplimiento primero, memoria destilada, shipping con
disciplina, no sobre-construir, y una vara de UX/seguridad calibrada al riesgo real. Si un proyecto
nuevo adopta ese criterio desde el día 1, se ahorra la mitad de las cicatrices que documentan los
otros dos.

---

**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md) ·
[Field Notes](PRODUCTION_LESSONS.md) · [Método Mesa de Ingenieros](MULTI_AGENT_ENGINEERING_METHOD.md)
