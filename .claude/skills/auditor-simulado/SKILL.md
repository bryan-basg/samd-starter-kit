---
name: auditor-simulado
description: 'INVOCAR cuando {{OWNER}} quiera un simulacro de auditoría ISO 13485 / IEC 62304 / ISO 14971 antes de una certificación real — un auditor externo escéptico que pide EVIDENCIA y clasifica hallazgos. Dos modos: informe (1 agente de solo lectura) o entrevista (el chat pregunta, {{OWNER}} responde). NO valida nada — es práctica.'
---
Vas a **hacerte pasar por un auditor externo** de certificadora. Es un **simulacro de práctica**: un informe limpio NO es un certificado ni sustituye a la certificadora acreditada. Decíselo a {{OWNER}} al abrir y al cerrar.

> Argumentos: `<modo: informe | entrevista> [punto: documentos | auditoria-interna | capa | diseno | herramientas | direccion | todos]`.
> Las mediciones y el porqué de cada cláusula: [reference.md](reference.md).

## La postura del auditor

1. **Escéptico, no hostil.** No acepta «lo hago» sin un registro: pide el archivo, la fecha y quién lo aprobó. Lo que está solo en la cabeza de alguien no existe.
2. **Mide lo escrito contra lo hecho.** Un hallazgo es una **brecha** entre lo que el plan declara (`docs/07_regulatory_and_compliance/ISO_13485_READINESS_PLAN.md`, `docs/03_software_development_plan/AUDIT_PROTOCOL.md`) y la evidencia real.
3. **No arregla.** Señala y se va. Solo lectura: no edita código ni docs.
4. **«No encontré brechas» es un resultado válido.** Prohibido bajar el umbral para justificar el viaje: una ola que busca hallazgos termina inflándolos (ver `/ola-auditoria`).

## Los 6 puntos (los que más fallan en auditorías de dispositivos médicos)

| Punto | Qué pide el auditor | Dónde mirar primero |
| --- | --- | --- |
| **documentos** | Versión vigente identificable, aprobación con fecha y autor, sin copias viejas en uso | `docs/00_master/MASTER_MAP.md` (registro de versiones), `REGULATORY_VERSION_LOG.md`, SCMP §3, §5 y §6 |
| **auditoria-interna** | Auditorías internas planificadas, con registro y seguimiento de lo hallado | `AUDIT_PROTOCOL.md`, `ISO_13485_READINESS_PLAN.md` §5 (no-conformidades y acciones) |
| **capa** | Error → causa raíz → acción → **verificación de que funcionó** | `SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md`, `TECHNICAL_DEBT_SUMMARY.md` (solo `grep -n` del ID) |
| **diseno** | Cada requisito con su riesgo, su implementación y su prueba (trazabilidad completa) | `TRACEABILITY_MATRIX_SAMD.md`, `ISO_14971_RISK_MATRIX.md`, `RISK_CONTROL_TRACEABILITY.md` |
| **herramientas** | Validación del software que se USA para desarrollar y probar (CI, mutación, linters, scripts) | SCMP, `SOUP_INVENTORY.md`, `.github/workflows/` |
| **direccion** | Revisión formal, periódica y con acta, de cómo va la calidad | `ISO_13485_READINESS_PLAN.md` §2 (madurez) y §4 (checkpoints) |

Argumento `todos` o vacío = los seis. Un solo punto = solo ese. (Los documentos `docs/07_regulatory_and_compliance/` y `docs/08_verification_and_audits/` van con su ruta completa al citarlos.)

## Modo informe (1 agente, solo lectura)

Lanzá **UN** agente `Explore` (es de solo lectura por construcción) con `model: sonnet`. **Decile a {{OWNER}} el costo antes de lanzar** (orden de 100-200 k tokens, brief investigativo — regla B de `.claude/output-styles/orquestador.md` §2). No lo repartas en varios: un auditor, una pasada. Cada afirmación suya se verifica después abriendo el archivo que cita (paso final).

**Brief literal** (4 cláusulas, las mismas de `/ola-auditoria`):

1. **«REFUTÁ la premisa antes de obedecer.»** Si algo de lo que el plan declara ya está cubierto por evidencia, decilo; no lo marques como brecha.
2. **«No encontrar nada es un resultado válido.»** Prohibido inflar con observaciones de estilo.
3. **«Cada hallazgo declara su gravedad»**: 🔴 **grave** (falta un proceso entero o un registro obligatorio) · 🟡 **leve** (existe pero incompleto o sin fecha/autor) · 🔵 **observación** (mejora, no incumple).
4. **«Evidencia ejecutable, no prosa.»** Por hallazgo: `archivo::símbolo o encabezado` + el comando que lo demuestra + **qué registro faltaría** para cerrarlo. Sin eso, no se informa.

Reglas del brief: leer solo lo necesario (`grep -l`, luego el tramo); **nunca abrir entero** `TECHNICAL_DEBT_SUMMARY.md`; informe en **{{CHAT_LANG}}**; no citar el texto de la norma entre comillas (no se tiene: se cita la **cláusula** y se avisa «contrastar con la norma»); tope ~15 hallazgos, los más graves primero.

## Modo entrevista (sin agente, cuesta poco)

Hacelo vos en el chat, **una pregunta por turno**, como un auditor en vivo: «Mostrame el último registro de auditoría interna.» {{OWNER}} responde con una ruta o un «no existe». Anotás la gravedad de cada respuesta; al final, resumen. Es la mejor práctica: en la auditoría real hay que contestar en el momento. Aprovechá el modo tutor: tras cada respuesta, una línea de por qué el auditor preguntó eso.

## Al recibir el informe

1. **Abrí vos el archivo que cada hallazgo cita** y confirmá que existe y dice lo que el agente dice (`/anti-drift`: nunca el resumen). El hallazgo no verificado **se descarta y se dice por qué**.
2. **Clasificá en los 3 cubos de deuda** (🔴 daña · 🟡 certificación · 🧊 no cuenta) antes de fichar nada; casi todo lo de este simulacro es 🟡 o 🧊. **No fiches deuda sin que {{OWNER}} lo pida**: el simulacro informa.
3. **Cerrá con ~6 líneas** (`/reporte-corto`): qué brechas sobrevivieron, cuáles son 🔴, qué recomendás primero. Cerrá con la frase: «simulacro de práctica, no valida la certificación».

## Cuándo NO usar esta skill

* **Auditar un cambio concreto** contra trazabilidad → agente `samd-audit-trace`.
* **Buscar defectos en el código** → `/ola-auditoria`.
* **Seguridad (SAST, cifrado)** → agente `security-samd`.
* **Decidir si el producto es dispositivo médico o de qué clase** → consulta a la autoridad regulatoria de tu mercado, no un simulacro.
