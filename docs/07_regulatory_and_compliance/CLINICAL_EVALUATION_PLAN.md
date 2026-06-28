# Plan de Evaluación Clínica (CEP)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** YYYY-MM-DD

> Documento plantilla del SaMD Starter Kit. Reemplace los marcadores `{{...}}` y las filas-placeholder (`<descripción>`, `YYYY-MM-DD`) con el contenido real del proyecto. No declare evidencia clínica que no exista.

---

## 1. Propósito y alcance

Este Plan de Evaluación Clínica (CEP, *Clinical Evaluation Plan*) define el proceso sistemático y planificado para generar, recolectar, analizar y evaluar la evidencia clínica relativa a **{{PROJECT_NAME}}**, con el fin de verificar su seguridad, su desempeño y el beneficio clínico bajo el uso previsto.

| Campo | Valor |
|---|---|
| Fabricante / responsable | {{OWNER}} |
| Producto | {{PROJECT_NAME}} |
| Clase SaMD | {{SAMD_CLASS}} |
| Uso previsto declarado | {{INTENDED_USE}} |
| Stack tecnológico | {{FRONTEND_STACK}} / {{BACKEND_STACK}} / {{DB_STACK}} / {{CLOUD_STACK}} |
| Marco normativo de referencia | MDR (UE) 2017/745 Anexo XIV Parte A · MEDDEV 2.7/1 Rev.4 · ISO 14155 · IEC 62304 · ISO 14971 |

**Fuera de alcance:** `<funcionalidades o indicaciones explícitamente excluidas de la evaluación clínica>`.

---

## 2. Objetivo de uso clínico

| Atributo | Descripción |
|---|---|
| Condición / estado clínico abordado | {{INTENDED_USE}} |
| Población de usuarios prevista | `<descripción de la población diana>` |
| Usuario previsto (operador) | `<paciente / profesional / cuidador>` |
| Entorno de uso | `<domiciliario / ambulatorio / hospitalario>` |
| Función del software (significado clínico) | `<informar / impulsar / diagnosticar / tratar — categoría IMDRF>` |
| Beneficio clínico declarado | `<descripción cuantificable del beneficio>` |

> Clasifíquese el significado clínico según el marco **IMDRF SaMD N12** (estado de la condición × significado de la información proporcionada).

---

## 3. Evidencia clínica buscada

| ID | Pregunta clínica (PICO) | Tipo de evidencia | Endpoint / métrica | Estado |
|---|---|---|---|---|
| CE-01 | `<población-intervención-comparador-resultado>` | `<literatura / datos del producto / estudio>` | `<métrica>` | Pendiente |
| CE-02 | `<...>` | `<...>` | `<...>` | Pendiente |

**Estado del arte / alternativas:** `<resumen del estándar de cuidado actual y dispositivos equivalentes>`.

---

## 4. Métodos de evaluación

### 4.1 Revisión sistemática de literatura
- **Bases de datos:** `<PubMed / Embase / Cochrane / otras>`.
- **Estrategia de búsqueda:** `<términos, operadores booleanos, filtros>`.
- **Criterios de inclusión/exclusión:** `<criterios>`.
- **Criterios de apreciación (appraisal):** relevancia y calidad metodológica según MEDDEV 2.7/1 Rev.4 §9.3.
- **Protocolo de selección:** diagrama de flujo PRISMA.

### 4.2 Datos del producto / datos de campo
- **Fuentes:** `<datos de uso anonimizados, registros de incidentes, feedback de usuarios, PMS/PMCF>`.
- **Equivalencia (si aplica):** demostración de equivalencia clínica, técnica y biológica con `<dispositivo>` (MEDDEV 2.7/1 Rev.4 §A1).

### 4.3 Datos de verificación y validación (V&V)
- Vínculo con verificación de software **IEC 62304 §5.5–§5.7** y validación de usabilidad **IEC 62366-1**.
- Vínculo con la gestión de riesgo **ISO 14971** (ver `ISO_14971_RISK_MATRIX.md`).

---

## 5. Criterios de éxito / aceptación

| Criterio | Umbral de aceptación | Justificación |
|---|---|---|
| Seguridad | `<sin riesgos residuales inaceptables>` | ISO 14971 |
| Desempeño técnico | `<métrica ≥ umbral>` | `<referencia>` |
| Beneficio clínico | `<métrica ≥ umbral>` | `<referencia>` |
| Aceptabilidad / usabilidad | `<métrica>` | IEC 62366-1 |

El balance **beneficio/riesgo** debe resultar favorable para todas las indicaciones declaradas (MDR Anexo I §1, §8).

---

## 6. Cronograma

| Hito | Entregable | Responsable | Fecha objetivo |
|---|---|---|---|
| Aprobación del CEP | Este documento firmado | `<rol>` | YYYY-MM-DD |
| Revisión de literatura completa | Informe de búsqueda | `<rol>` | YYYY-MM-DD |
| Recolección de datos del producto | Dataset consolidado | `<rol>` | YYYY-MM-DD |
| Análisis y apreciación | Tablas de evidencia | `<rol>` | YYYY-MM-DD |
| Reporte de Validación Clínica (CER) | `CLINICAL_VALIDATION_REPORT.md` | `<rol>` | YYYY-MM-DD |

---

## 7. Roles y responsabilidades

| Rol | Responsabilidad | Persona |
|---|---|---|
| Evaluador clínico | Conducción de la evaluación, apreciación de evidencia | `<nombre>` |
| Responsable regulatorio | Cumplimiento normativo y trazabilidad | `<nombre>` |
| Gestor de riesgo | Vínculo con ISO 14971 | `<nombre>` |
| Aprobador | Liberación del plan | `<nombre>` |

> El evaluador clínico debe documentar su cualificación (MEDDEV 2.7/1 Rev.4 §6.4).

---

## 8. Control de cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | `<autor>` | Creación de la plantilla |

---

## 9. Referencias normativas

- MDR (UE) 2017/745, Anexo XIV Parte A — Evaluación clínica.
- MEDDEV 2.7/1 Rev.4 — Clinical Evaluation: Guide for manufacturers and notified bodies.
- ISO 14155 — Investigación clínica de productos sanitarios en humanos.
- IMDRF/SaMD WG/N12 — *Software as a Medical Device: Possible Framework for Risk Categorization*.
- IEC 62304 — Procesos del ciclo de vida del software de dispositivos médicos.
- ISO 14971 — Aplicación de la gestión de riesgos a productos sanitarios.
