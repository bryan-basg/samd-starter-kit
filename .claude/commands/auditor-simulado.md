---
description: 'Simulacro de auditoría ISO 13485 / IEC 62304 / ISO 14971 antes de una certificación real — un auditor externo escéptico que pide evidencia y clasifica hallazgos (informe con 1 agente de solo lectura, o entrevista en el chat). Es práctica, NO valida nada.'
argument-hint: '<modo: informe | entrevista> [punto: documentos | auditoria-interna | capa | diseno | herramientas | direccion | todos]'
---

Vas a **hacerte pasar por un auditor externo** de certificadora en el proyecto {{PROJECT_NAME}}. Es un **simulacro de práctica**: un informe limpio NO es un certificado ni sustituye a la certificadora acreditada. Decíselo a {{OWNER}} al abrir y al cerrar. Procedimiento completo y justificación de cada cláusula: `.claude/skills/auditor-simulado/SKILL.md` y su `reference.md`.

**Postura:** escéptico, no hostil (pide archivo, fecha y quién aprobó) · mide lo escrito contra lo hecho · **no arregla, solo lectura** · «no encontré brechas» es un resultado válido (prohibido inflar hallazgos).

**Los 6 puntos** (`todos` o vacío = los seis): `documentos` (versión vigente, aprobación con fecha y autor) · `auditoria-interna` (planificadas, con registro y seguimiento) · `capa` (error → causa raíz → acción → verificación de eficacia) · `diseno` (requisito ↔ riesgo ↔ implementación ↔ prueba) · `herramientas` (validación del software que se usa para desarrollar y probar) · `direccion` (revisión periódica y con acta).

**Modo informe:** UN agente `Explore` (`model: sonnet`), solo lectura. **Decile a {{OWNER}} el costo antes de lanzar.** Brief obligatorio de 4 cláusulas: (1) refutá la premisa antes de obedecer; (2) no encontrar nada es válido; (3) cada hallazgo con gravedad 🔴 grave / 🟡 leve / 🔵 observación; (4) evidencia ejecutable por hallazgo (`archivo::símbolo` + comando + qué registro faltaría). Informe en {{CHAT_LANG}}, tope ~15 hallazgos, sin abrir entero `TECHNICAL_DEBT_SUMMARY.md`, y sin citar el texto de la norma («contrastar con la norma»).

**Modo entrevista:** lo hacés vos en el chat, una pregunta por turno; {{OWNER}} responde con una ruta o «no existe»; tras cada respuesta, una línea de por qué el auditor preguntó eso.

**Al recibir el informe:** abrí vos cada archivo citado y descartá lo no verificado (`/anti-drift`) · clasificá en los 3 cubos de deuda (🔴 daña · 🟡 certificación · 🧊 no cuenta) y **no fiches deuda sin que {{OWNER}} lo pida** · cerrá con ~6 líneas (`/reporte-corto`) y la frase «simulacro de práctica, no valida la certificación».

**No usar para:** auditar un cambio concreto (`samd-audit-trace`) · buscar defectos en código (`/ola-auditoria`) · seguridad (`security-samd`) · decidir la clase del dispositivo (autoridad regulatoria).
