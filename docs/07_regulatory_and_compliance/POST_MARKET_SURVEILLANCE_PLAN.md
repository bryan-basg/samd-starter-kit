# Plan de Vigilancia Post-Comercialización (PMS)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** YYYY-MM-DD

> Documento plantilla del SaMD Starter Kit. Define cómo se recolectan y usan los datos de campo tras la puesta en el mercado. Reemplace los marcadores y filas-placeholder con el contenido real.

---

## 1. Propósito

Este Plan de Vigilancia Post-Comercialización (PMS, *Post-Market Surveillance*) establece el sistema proactivo y sistemático para recopilar y revisar la experiencia obtenida de **{{PROJECT_NAME}}** una vez comercializado, conforme a **ISO 13485 §8.2** y **MDR (UE) 2017/745 Art. 83–86**. Sus salidas retroalimentan la gestión de riesgo (ISO 14971) y la evaluación clínica (PMCF).

| Campo | Valor |
|---|---|
| Fabricante / responsable | {{OWNER}} |
| Producto | {{PROJECT_NAME}} |
| Clase SaMD | {{SAMD_CLASS}} |
| Uso previsto | {{INTENDED_USE}} |
| Infraestructura de despliegue | {{CLOUD_STACK}} |

---

## 2. Fuentes de datos de campo

| Fuente | Descripción | Canal de recolección | Responsable |
|---|---|---|---|
| Reclamos / quejas de usuarios | `<...>` | `<formulario / soporte>` | `<rol>` |
| Incidentes y casi-incidentes | `<...>` | `<sistema de tickets>` | `<rol>` |
| Telemetría / logs de uso | `<errores, crashes, uso de funciones>` | `<{{CLOUD_STACK}} monitoring>` | `<rol>` |
| Feedback proactivo de usuarios | `<encuestas, NPS>` | `<...>` | `<rol>` |
| Literatura y vigilancia externa | `<alertas de autoridades, recalls similares>` | `<...>` | `<rol>` |
| Datos PMCF | `<seguimiento clínico>` | `<...>` | `<rol>` |

> Toda recolección respeta minimización de datos y protección de datos personales (GDPR / normativa aplicable). No se recolecta PHI/PII más allá de lo estrictamente necesario.

---

## 3. Indicadores de seguridad y desempeño (PMS)

| ID | Indicador | Definición | Umbral de alerta | Frecuencia de medición |
|---|---|---|---|---|
| KPI-01 | Tasa de incidentes | `<incidentes / usuarios activos>` | `<umbral>` | `<mensual>` |
| KPI-02 | Tasa de error de software | `<crashes / sesiones>` | `<umbral>` | `<semanal>` |
| KPI-03 | Tiempo de resolución de quejas | `<días>` | `<umbral>` | `<mensual>` |
| KPI-04 | Satisfacción / usabilidad | `<métrica>` | `<umbral>` | `<trimestral>` |

Superar un umbral dispara el proceso de **acciones correctivas y preventivas (CAPA)** y, si procede, una **acción de seguridad de campo (FSCA)**.

---

## 4. Periodicidad de revisión

| Actividad | Frecuencia | Entregable |
|---|---|---|
| Revisión operativa de indicadores | `<mensual>` | Tablero de KPIs |
| Revisión por la dirección | `<según ISO 13485 §5.6>` | Acta de revisión |
| Informe periódico de seguridad (PSUR) — Clase IIa+/SaMD B–C | `<anual o bienal, MDR Art. 86>` | PSUR |
| Informe de vigilancia post-comercialización — Clase I | `<según necesidad, MDR Art. 85>` | PMS Report |

---

## 5. Retroalimentación a la gestión de riesgo

Los datos de campo se evalúan contra la `ISO_14971_RISK_MATRIX.md`:

1. ¿Aparecen **peligros o situaciones peligrosas no previstas**? → abrir nuevo ítem de riesgo.
2. ¿La **probabilidad real** de un riesgo conocido difiere de la estimada? → recalcular riesgo residual.
3. ¿El balance **beneficio/riesgo** global sigue siendo aceptable? → si no, acción de campo / actualización.

| Hallazgo de campo | Riesgo afectado | Acción | Estado |
|---|---|---|---|
| `<...>` | `<R-XX>` | `<actualizar matriz / CAPA / FSCA>` | Pendiente |

---

## 6. Seguimiento clínico post-comercialización (PMCF)

Conforme a **MDR Anexo XIV Parte B**, el PMCF cierra las brechas de evidencia identificadas en el `CLINICAL_VALIDATION_REPORT.md`.

| ID PMCF | Objetivo de evidencia | Método | Criterio de éxito | Fecha objetivo |
|---|---|---|---|---|
| PMCF-01 | `<...>` | `<encuesta / estudio observacional / análisis de datos reales>` | `<...>` | YYYY-MM-DD |

Si el producto se declara **exento de PMCF**, justifíquese aquí: `<justificación>`.

---

## 7. Reporte a autoridades

| Evento | Plazo de reporte | Autoridad | Referencia |
|---|---|---|---|
| Incidente grave | `<≤ 15 días; ≤ 2 días si amenaza grave a la salud pública>` | `<autoridad competente>` | MDR Art. 87 |
| Acción correctiva de seguridad de campo (FSCA) | `<inmediato>` | `<autoridad competente>` | MDR Art. 87 |
| Tendencia de incidentes no graves | `<según procedimiento>` | `<autoridad competente>` | MDR Art. 88 |

---

## 8. Roles y responsabilidades

| Rol | Responsabilidad | Persona |
|---|---|---|
| Responsable de vigilancia (PMS) | Coordinación del plan y los informes | `<nombre>` |
| Persona responsable de cumplimiento (PRRC) | Reporte a autoridades (MDR Art. 15) | `<nombre>` |
| Gestor de riesgo | Actualización de ISO 14971 | `<nombre>` |
| Dirección | Revisión y recursos | `<nombre>` |

---

## 9. Control de cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | `<autor>` | Creación de la plantilla |

---

## 10. Referencias normativas

- ISO 13485 §8.2 — Seguimiento y medición; §5.6 — Revisión por la dirección.
- MDR (UE) 2017/745 Art. 83–88 — Vigilancia post-comercialización; Anexo III — Plan PMS; Anexo XIV Parte B — PMCF.
- ISO 14971 §10 — Información de producción y posproducción.
- IMDRF/SaMD WG/N12 — Categorización de riesgo SaMD.
