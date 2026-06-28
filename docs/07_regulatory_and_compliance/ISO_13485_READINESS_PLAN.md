# Plan de Preparación del QMS hacia Auditoría Externa — ISO 13485:2016

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Plan de preparación del Sistema de Gestión de Calidad (QMS) hacia la auditoría de certificación **ISO 13485:2016**. Identifica gaps por cláusula, fija checkpoints y asigna responsables. Vive junto al DHF; se revisa antes de cada hito de certificación. No reemplaza al Manual de Calidad: lo prepara para auditoría.

---

## 1. Propósito y alcance

- **Objetivo:** alcanzar el estado de "listo para auditoría externa" del QMS aplicable a **{{PROJECT_NAME}}** (SaMD Clase **{{SAMD_CLASS}}**).
- **Uso previsto del dispositivo:** {{INTENDED_USE}}
- **Responsable de calidad:** <QUALITY_MANAGER>
- **Titular / fabricante legal:** {{OWNER}}
- **Norma de referencia:** ISO 13485:2016. Normas conexas: IEC 62304 (ciclo de vida del software), ISO 14971 (gestión de riesgo), IEC 62366-1 (usabilidad).
- **Organismo de certificación (objetivo):** <NOTIFIED_BODY>

**Fuera de alcance:** producción física de hardware (el dispositivo es software puro) y procesos delegados al proveedor de nube bajo responsabilidad compartida.

---

## 2. Estado de madurez del QMS

| Nivel | Definición |
|---|---|
| 0 — Ausente | No existe proceso documentado. |
| 1 — Definido | Proceso documentado, sin evidencia de ejecución. |
| 2 — Implementado | Proceso ejecutándose, evidencia parcial. |
| 3 — Verificado | Proceso ejecutándose con registros completos y auditables. |
| 4 — Listo auditoría | Verificado + auditoría interna pasada sin no-conformidades mayores. |

---

## 3. Evaluación de gaps por cláusula ISO 13485:2016

| Cláusula | Requisito | Evidencia esperada | Estado actual | Madurez | Gap | Responsable |
|---|---|---|---|---|---|---|
| §4.1 | Requisitos generales del QMS | Manual de Calidad, mapa de procesos | <documento/path> | 2 | <gap> | <QUALITY_MANAGER> |
| §4.2 | Control de documentos y registros | `REGULATORY_VERSION_LOG.md` | <path> | 3 | <gap> | <QUALITY_MANAGER> |
| §5 | Responsabilidad de la dirección | Política de calidad, revisión por la dirección | <acta> | 1 | <gap> | {{OWNER}} |
| §6 | Gestión de recursos | Registros de competencia/formación | <registro> | 1 | <gap> | <responsable> |
| §7.3 | Diseño y desarrollo (DHF) | Plan de desarrollo, trazabilidad, V&V | `docs/03_software_development_plan/` | 2 | <gap> | <responsable> |
| §7.5 | Producción y prestación del servicio | Control de release, despliegue, configuración | <pipeline/path> | 2 | <gap> | <responsable> |
| §8.2.1 | Retroalimentación / vigilancia post-mercado | Plan de post-market surveillance | <path> | 1 | <gap> | <responsable> |
| §8.2.4 | Auditoría interna | Programa y registros de auditoría interna | <path> | 0 | <gap> | <QUALITY_MANAGER> |
| §8.3 | Control de producto no conforme | Procedimiento CAPA | <path> | 1 | <gap> | <responsable> |
| §8.5 | Acción correctiva y preventiva (CAPA) | Registros CAPA cerrados | <path> | 1 | <gap> | <responsable> |

---

## 4. Hoja de ruta de checkpoints

| Checkpoint | Hito | Criterio de salida | Fecha objetivo | Responsable | Estado |
|---|---|---|---|---|---|
| CP-1 | Cierre de gaps de documentación (§4) | Todos los procedimientos en estado ≥ Definido | YYYY-MM-DD | <QUALITY_MANAGER> | Pendiente |
| CP-2 | Revisión por la dirección (§5.6) | Acta firmada + acciones asignadas | YYYY-MM-DD | {{OWNER}} | Pendiente |
| CP-3 | Trazabilidad DHF completa (§7.3) | Lazo riesgo↔control↔REQ↔test cerrado | YYYY-MM-DD | <responsable> | Pendiente |
| CP-4 | Auditoría interna (§8.2.4) | 0 no-conformidades mayores | YYYY-MM-DD | <QUALITY_MANAGER> | Pendiente |
| CP-5 | Cierre de CAPA de auditoría interna | Todas las acciones cerradas y verificadas | YYYY-MM-DD | <responsable> | Pendiente |
| CP-6 | Etapa 1 (revisión documental del organismo) | Sin hallazgos bloqueantes | YYYY-MM-DD | <NOTIFIED_BODY> | Pendiente |
| CP-7 | Etapa 2 (auditoría in situ) | Recomendación de certificación | YYYY-MM-DD | <NOTIFIED_BODY> | Pendiente |

---

## 5. Registro de no-conformidades y acciones

| ID | Origen | Cláusula | Descripción | Severidad | Acción correctiva | Responsable | Fecha objetivo | Estado |
|---|---|---|---|---|---|---|---|---|
| NC-001 | Auditoría interna | §<X.Y> | <descripción> | Mayor / Menor | <acción> | <responsable> | YYYY-MM-DD | Abierta |

---

## 6. Riesgos del proyecto de certificación

| Riesgo | Impacto | Probabilidad | Mitigación | Responsable |
|---|---|---|---|---|
| <ej. evidencia de V&V incompleta para la fecha> | Retraso de etapa 2 | <alta/media/baja> | <mitigación> | <responsable> |

---

## 7. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
