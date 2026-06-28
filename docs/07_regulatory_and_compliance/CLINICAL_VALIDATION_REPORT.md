# Reporte de Validación Clínica (CER)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** YYYY-MM-DD

> Documento plantilla del SaMD Starter Kit. Es el entregable que cierra el ciclo abierto por `CLINICAL_EVALUATION_PLAN.md`. Complete cada sección con datos reales; las celdas `<...>` y `YYYY-MM-DD` son placeholders. No declare conclusiones sin evidencia documentada.

---

## 1. Identificación

| Campo | Valor |
|---|---|
| Fabricante / responsable | {{OWNER}} |
| Producto | {{PROJECT_NAME}} |
| Versión de software evaluada | `<vX.Y.Z>` |
| Clase SaMD | {{SAMD_CLASS}} |
| Uso previsto evaluado | {{INTENDED_USE}} |
| Plan de evaluación de referencia | `CLINICAL_EVALUATION_PLAN.md` v`<X.Y>` |
| Periodo de evaluación | YYYY-MM-DD – YYYY-MM-DD |

---

## 2. Resumen ejecutivo

`<Síntesis de 1–2 párrafos: alcance evaluado, volumen de evidencia analizada, conclusión global del balance beneficio/riesgo y aptitud para el uso previsto.>`

---

## 3. Metodología aplicada

Describir cómo se ejecutó lo planificado en el CEP y documentar cualquier desviación.

| Método | Ejecutado según plan | Desviaciones |
|---|---|---|
| Revisión de literatura | `<sí/no>` | `<descripción>` |
| Datos del producto / campo | `<sí/no>` | `<descripción>` |
| Datos de V&V (IEC 62304) | `<sí/no>` | `<descripción>` |
| Validación de usabilidad (IEC 62366-1) | `<sí/no>` | `<descripción>` |

---

## 4. Resultados

### 4.1 Evidencia de literatura

| Ref. | Cita | Nivel de evidencia | Relevancia | Hallazgo clave |
|---|---|---|---|---|
| L-01 | `<autor, año, fuente>` | `<I–IV>` | `<alta/media/baja>` | `<...>` |

### 4.2 Datos del producto / campo

| ID dataset | Fuente | n | Periodo | Resultado |
|---|---|---|---|---|
| D-01 | `<...>` | `<n>` | YYYY-MM-DD / YYYY-MM-DD | `<...>` |

### 4.3 Evaluación frente a criterios de éxito

| Criterio (del CEP) | Umbral | Resultado obtenido | ¿Cumple? |
|---|---|---|---|
| Seguridad | `<umbral>` | `<valor>` | `<sí/no>` |
| Desempeño técnico | `<umbral>` | `<valor>` | `<sí/no>` |
| Beneficio clínico | `<umbral>` | `<valor>` | `<sí/no>` |
| Usabilidad | `<umbral>` | `<valor>` | `<sí/no>` |

---

## 5. Análisis de beneficio/riesgo

| Beneficio identificado | Riesgo asociado | Medida de control (ISO 14971) | Riesgo residual | Aceptable |
|---|---|---|---|---|
| `<...>` | `<...>` | `<ref. a ISO_14971_RISK_MATRIX.md>` | `<bajo/medio/alto>` | `<sí/no>` |

**Conclusión del balance:** `<favorable / no favorable>`, conforme a MDR Anexo I §1 y §8.

---

## 6. Limitaciones y datos faltantes

`<Brechas de evidencia, sesgos, tamaño muestral, generalización. Indicar qué se traslada al PMCF (ver POST_MARKET_SURVEILLANCE_PLAN.md).>`

---

## 7. Conclusiones

`<Declaración explícita de si {{PROJECT_NAME}} cumple los requisitos de seguridad y desempeño para el uso previsto, y si el balance beneficio/riesgo es aceptable.>`

---

## 8. Plan de seguimiento clínico post-comercialización (PMCF)

Las brechas de evidencia de §6 se gestionan según el `POST_MARKET_SURVEILLANCE_PLAN.md`. Resumen de actividades PMCF derivadas:

| ID | Actividad PMCF | Objetivo de evidencia | Fecha objetivo |
|---|---|---|---|
| PMCF-01 | `<...>` | `<...>` | YYYY-MM-DD |

---

## 9. Firmas

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Evaluador clínico | `<nombre>` | ________ | YYYY-MM-DD |
| Responsable regulatorio | `<nombre>` | ________ | YYYY-MM-DD |
| Gestor de riesgo | `<nombre>` | ________ | YYYY-MM-DD |
| Aprobador / representante de la dirección | `<nombre>` | ________ | YYYY-MM-DD |

---

## 10. Control de cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | `<autor>` | Creación de la plantilla |

---

## 11. Referencias normativas

- MDR (UE) 2017/745, Anexo XIV Parte A — Evaluación clínica; Anexo I §1, §8 — Requisitos generales de seguridad y rendimiento.
- MEDDEV 2.7/1 Rev.4 §10–§11 — Reporte de evaluación clínica.
- ISO 14971 — Gestión de riesgos.
- IEC 62304 §5.7 — Pruebas del sistema de software.
- IEC 62366-1 — Aplicación de la ingeniería de usabilidad.
