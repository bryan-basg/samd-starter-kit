# Ejemplo trabajado — AuraLog (SaMD Clase B ficticio)

> **Dispositivo ficticio y propósito didáctico.** AuraLog **no existe**; es un dispositivo software médico inventado para mostrar el SaMD Starter Kit "en acción". Ninguno de los `archivo:línea`, tests, fechas ni números de esta carpeta corresponde a un producto real — son valores plausibles para que veas **cómo se rellenan las plantillas vacías** del kit.

## ¿Qué es AuraLog?

AuraLog es una app de **registro y seguimiento de síntomas** para pacientes con una condición crónica. El paciente anota sus síntomas diarios y recibe recordatorios. Cuando los patrones registrados cruzan umbrales configurados, AuraLog genera una **alerta informativa de tipo "consultá a tu profesional"**.

AuraLog **NO diagnostica** y **NO recomienda tratamiento**: solo **registra** lo que el paciente ingresa y **alerta** de forma informativa. Esa frontera (registrar + alertar, nunca diagnosticar) es la que sostiene la clasificación **Clase B**: una alerta perdida puede **retrasar** la consulta con el profesional (daño no serio, reversible), pero el software no toma decisiones clínicas por sí mismo.

## Stack de ejemplo

| Capa | Tecnología |
|---|---|
| Frontend | React + TypeScript (offline-first) |
| Backend | Python + FastAPI |
| Datos | PostgreSQL (transaccional + auditoría) |
| Cloud | Google Cloud Platform (Cloud Run, Cloud SQL, Secret Manager, Cloud Scheduler) |

## Documentos que muestra este ejemplo

| Archivo de ejemplo | Qué demuestra | Plantilla vacía equivalente en `docs/` |
|---|---|---|
| [`MASTER_MAP.md`](./MASTER_MAP.md) | Identidad del dispositivo, arquitectura, módulos clínicos críticos (motor de alertas), índice documental y registro de versiones. | [`docs/00_master/MASTER_MAP.md`](../../docs/00_master/MASTER_MAP.md) |
| [`SOFTWARE_SAFETY_CLASSIFICATION.md`](./SOFTWARE_SAFETY_CLASSIFICATION.md) | Justificación formal de Clase B según IEC 62304 §4.3: qué pasa si el motor de alertas falla, segregación de ítems y medidas externas. | [`docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md`](../../docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md) |
| [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md) | Registro de 6 riesgos reales de AuraLog (alerta perdida, umbral mal configurado, exposición de PHI, fallo offline…) con control y evidencia verificable. | [`docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md`](../../docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md) |
| [`TRACEABILITY_MATRIX_SAMD.md`](./TRACEABILITY_MATRIX_SAMD.md) | 6 requisitos (REQ) trazados a `archivo:línea` + nombre de test + riesgo asociado, la cadena de trazabilidad completa. | [`docs/07_regulatory_and_compliance/TRACEABILITY_MATRIX_SAMD.md`](../../docs/07_regulatory_and_compliance/TRACEABILITY_MATRIX_SAMD.md) |

## Cómo leerlo

1. Abrí primero la plantilla vacía en `docs/` para ver los marcadores `{{...}}` y `<...>`.
2. Abrí el archivo equivalente acá para ver esos marcadores ya reemplazados por datos de AuraLog.
3. Fijate en la **coherencia entre los 4 documentos**: los mismos módulos (motor de alertas `alert_engine`), los mismos riesgos (`R001`…`R006`) y los mismos requisitos (`REQ-CLN-01`, `REQ-SEC-01`…) se referencian de forma cruzada. Esa coherencia es justamente lo que un auditor externo verifica.

> Recordatorio: los paths de código (`app/services/alert_engine.py:NN`) y los nombres de test son **ilustrativos**. En un proyecto real, `docs-dhf` verifica que cada path y cada test **existan HOY** antes de escribir la fila.
