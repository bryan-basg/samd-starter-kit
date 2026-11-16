# `/auditor-simulado` — anexo: de dónde sale cada cláusula

> Anexo de `SKILL.md`. Se lee para justificar o recalibrar; el procedimiento vive en `SKILL.md`.

## Origen

Nació en el proyecto de referencia (2026-11-08) cuando su dueño pidió «un agente que se haga pasar por auditor» tras preguntar qué falla en una auditoría ISO 13485. Se decidió **skill y no agente** porque se usa pocas veces (regla A del estilo «Orquestador SaMD»: crear un agente exige 3 SÍ y la frecuencia no los justifica) y un agente permanente carga contexto en cada sesión. Se portó al kit generalizado: sin los documentos propios de ese proyecto y sin sus costos de certificación.

## Por qué los 6 puntos

Salen de una búsqueda web hecha en el proyecto de referencia (2026-11-08). **Solo el informe de la TGA australiana trae conteos reales**: más de la mitad de los fabricantes auditados en 2 años tuvo no conformidades en control de documentos y registros. El resto son blogs de consultoras y certificadoras (PJR, Greenlight Guru, MedDeviceGuide, Johner Institute, Smithers): el orden es **orientativo**.

* Control de documentos — la más citada.
* Auditorías internas — a veces ni se hacen; su debilidad deja pasar otras fallas.
* CAPA — fuente frecuente de hallazgos graves (sin causa raíz ni verificación de eficacia).
* Controles de diseño — expediente de diseño incompleto, sobre todo en empresas de software.
* Validación del software de las herramientas — aparece en la lista de PJR para etapa 2, seguimiento y recertificación.
* Revisión por la dirección — cláusula 5.6, cruzada en los datos de la TGA.

Fuentes: [TGA](https://www.tga.gov.au/node/452778) · [PJR](https://www.pjr.com/standards/iso-13485/most-common-noncomformities-iso-13485-audits) · [MedDeviceGuide](https://meddeviceguide.com/blog/iso-13485-audit-findings-common-nonconformities-clause-guide) · [Greenlight Guru](https://www.greenlight.guru/blog/6-common-mistakes-iso-13485) · [Johner Institute](https://blog.johner-institute.com/regulatory-affairs/deviations-nonconformities/).

## Límites declarados

* **No es auditoría**: la certificadora acreditada de tu mercado es la única que emite el certificado.
* **Sin el texto de la norma** (de pago): el agente cita cláusulas desde resúmenes públicos y puede errar el número; por eso se avisa «contrastar con la norma».
* **Riesgo de falso verde o de hallazgo inventado**: de ahí las 4 cláusulas del brief y la verificación final abriendo cada archivo citado (ver `/ola-auditoria` y su `reference.md`).
* **Quién escribe y quién revisa**: con un equipo de una sola persona, el auditor real mirará la separación de roles; un agente no la resuelve.
* **Costos de certificación**: no se citan acá a propósito — varían por mercado y año, y las fuentes que los publican tienen interés comercial. Pedí cotización a una certificadora acreditada.
