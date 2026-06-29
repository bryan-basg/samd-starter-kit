# EU MDR 2017/745 Mapping — Puente al Marco Regulatorio Europeo

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Puente entre el DHF de **{{PROJECT_NAME}}** y el **Reglamento (UE) 2017/745 sobre productos sanitarios (EU MDR)**. Cubre clasificación por **Regla 11**, requisitos generales de seguridad y funcionamiento (**GSPR, Anexo I**), documentación técnica (**Anexos II/III**), rol del **Notified Body** y la relación con las normas armonizadas IEC 62304 / ISO 14971 / ISO 13485 ya presentes en el DHF.
>
> **Esto NO es una Declaración de Conformidad ni implica marcado CE.** Es un andamio de mapeo. El producto **no** afirma tener marcado CE ni certificado de Notified Body. Cada celda se completa con evidencia real. `{{VERIFICAR_CLAUSULA}}` = referencia pendiente de verificación por el responsable regulatorio.
>
> Mantenida por `docs-dhf`. La clase MDR la determina formalmente el fabricante legal ({{OWNER}}); este documento no la presume.

---

## 1. Clasificación por Regla 11 (software)

La **Regla 11** del **Anexo VIII** clasifica el software que es un dispositivo en sí mismo. Es la regla decisiva para SaMD.

| Supuesto de la Regla 11 | Clase MDR |
|---|---|
| Software destinado a aportar información usada para tomar decisiones con fines de **valoración** o terapéuticos | **IIa** |
| …si esas decisiones pueden causar **muerte o deterioro irreversible** del estado de salud | **III** |
| …si pueden causar **deterioro grave** del estado de salud o una intervención quirúrgica | **IIb** |
| Software para **monitorizar procesos fisiológicos** | **IIa** |
| …si monitoriza **parámetros fisiológicos vitales** cuya variación puede crear **peligro inmediato** | **IIb** |
| **Todo el demás** software | **I** |

> **Nota de vigencia (a 2026-06-29):** existe una propuesta de la Comisión Europea (dic-2025) para ampliar qué software puede quedar en Clase I bajo la Regla 11. A esta fecha es **solo propuesta, no vigente** — el texto consolidado actual (piso IIa para software de decisión clínica) sigue siendo el legalmente vinculante. Registrar cualquier cambio en `REGULATORY_VERSION_LOG.md` cuando se publique.

| Pregunta de clasificación | Respuesta del proyecto |
|---|---|
| ¿El software es un dispositivo en sí mismo (no accesorio)? | {{TODO: sí/no}} |
| ¿Aporta información para decisiones de valoración/terapéuticas? | {{TODO}} |
| Severidad máxima del impacto de una decisión errónea | {{TODO: irreversible / grave / no grave}} |
| **Clase MDR resultante (Regla 11)** | {{TODO: I / IIa / IIb / III}} |

> **Relación con la Clase SaMD {{SAMD_CLASS}}:** la Clase de seguridad IEC 62304 (A/B/C) y la clase de riesgo MDR (I/IIa/IIb/III) son **ejes distintos**. La justificación cruzada vive en `SOFTWARE_SAFETY_CLASSIFICATION.md` y se categoriza también en `IMDRF_SAMD_FRAMEWORK.md`. No asumir correspondencia 1:1.

---

## 2. GSPR — Requisitos Generales de Seguridad y Funcionamiento (Anexo I)

El **Anexo I** define los GSPR. La evidencia se consolida en una *GSPR checklist* (este mapeo es el esqueleto). Capítulos: I (requisitos generales §1–§9), II (diseño y fabricación §10–§22), III (información suministrada §23).

| GSPR (Anexo I) | Requisito | Documento DHF que lo cubre | Estado |
|---|---|---|---|
| §1–§4 | Seguridad y funcionamiento generales; reducción de riesgos ALARP | `ISO_14971_RISK_MATRIX.md`; `RISK_CONTROL_TRACEABILITY.md` | {{Pendiente}} |
| §3 | Sistema de gestión de riesgos | `ISO_14971_RISK_MATRIX.md` | {{Pendiente}} |
| §5 | Riesgos asociados al uso (factores humanos) | `USER_GUIDE.md`; `CLINICAL_EVALUATION_PLAN.md` | {{Pendiente}} |
| §9 | Funcionamiento conforme al uso previsto | `CLINICAL_VALIDATION_REPORT.md` | {{Pendiente}} |
| §14.2 (d) | Interacción del software con su entorno IT (compatibilidad con sistemas previstos) | `COMPLETE_TESTING_STRATEGY.md` | Verificado (la repetibilidad/fiabilidad del software vive en §17.1, no aquí) |
| **§17.1** | Sistemas electrónicos programables — repetibilidad, fiabilidad, funcionamiento | `ARCHITECTURE_OVERVIEW.md` | {{Pendiente}} |
| **§17.2** | Software desarrollado conforme al estado del arte (ciclo de vida, gestión de riesgo, verificación, validación) | `SOFTWARE_DEVELOPMENT_PLAN.md`; `TRACEABILITY_MATRIX_SAMD.md` | {{Pendiente}} |
| **§17.3** | Software en plataformas móviles — entorno de uso | `MEDICAL_DEVICE_LABELING.md`; `USER_GUIDE.md` | {{Pendiente}} |
| **§17.4** | Requisitos mínimos de **seguridad informática** (IT security) | `COMPLIANCE_AND_SECURITY_MASTER.md`; `INFOSEC_READINESS_ISO27001_SOC2.md`; `DATA_FLOW_DOCUMENTATION.md` | {{Pendiente}} |
| §22 | Protección contra riesgos de dispositivos para legos (si aplica) | `USER_GUIDE.md` | Verificado (Anexo I, Cap. III, punto 22) |
| §23.1 | Etiqueta e instrucciones de uso | `MEDICAL_DEVICE_LABELING.md`; `INSTRUCTIONS_FOR_USE_IFU.md` | {{Pendiente}} |
| §23.4 | Contenido de las instrucciones de uso | `INSTRUCTIONS_FOR_USE_IFU.md` | {{Pendiente}} |

> §17 es el corazón de los GSPR para SaMD. Confirmar el desglose exacto §17.1–§17.4 contra el texto consolidado del Anexo I antes de la sumisión.

---

## 3. Documentación técnica (Anexos II y III) ↔ DHF

El **Anexo II** define la documentación técnica; el **Anexo III**, la documentación técnica de vigilancia post-comercialización.

| Sección Anexo II/III | Contenido | Documento DHF | Estado |
|---|---|---|---|
| Anexo II §1 | Descripción y especificación del producto, variantes, accesorios | `ARCHITECTURE_OVERVIEW.md`; `MEDICAL_DEVICE_LABELING.md` | {{Pendiente}} |
| Anexo II §2 | Información de etiquetado e instrucciones de uso | `MEDICAL_DEVICE_LABELING.md`; `INSTRUCTIONS_FOR_USE_IFU.md` | {{Pendiente}} |
| Anexo II §3 | Información de diseño y fabricación | `SOFTWARE_DEVELOPMENT_PLAN.md`; `RFC-*.md`; `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md` | {{Pendiente}} |
| Anexo II §4 | Requisitos GSPR (Anexo I) + justificación de soluciones | §2 de este documento + `ISO_14971_RISK_MATRIX.md` | {{Pendiente}} |
| Anexo II §5 | Análisis beneficio-riesgo y gestión de riesgos | `ISO_14971_RISK_MATRIX.md`; `RISK_CONTROL_TRACEABILITY.md` | {{Pendiente}} |
| Anexo II §6.1 | Verificación y validación (preclínica, incl. software) | `COMPLETE_TESTING_STRATEGY.md`; `CLINICAL_VALIDATION_REPORT.md` | {{Pendiente}} |
| Anexo II §6.1 (clínica) | Evaluación clínica (remite a Art. 61 + Anexo XIV) | `CLINICAL_EVALUATION_PLAN.md` | {{Pendiente}} |
| **Anexo III** | Documentación técnica de PMS (plan PMS, PSUR/PMSR) | `POST_MARKET_SURVEILLANCE_PLAN.md` | {{Pendiente}} |

---

## 4. Evaluación clínica y post-mercado

| Requisito MDR | Artículo / Anexo | Documento DHF | Estado |
|---|---|---|---|
| Evaluación clínica | Art. 61 + Anexo XIV Parte A | `CLINICAL_EVALUATION_PLAN.md` | {{Pendiente}} |
| Seguimiento clínico post-comercialización (PMCF) | Anexo XIV Parte B | `POST_MARKET_SURVEILLANCE_PLAN.md` | {{Pendiente}} |
| Sistema de vigilancia post-comercialización | Art. 83 | `POST_MARKET_SURVEILLANCE_PLAN.md` | {{Pendiente}} |
| Plan de vigilancia post-comercialización | Art. 84 + Anexo III | `POST_MARKET_SURVEILLANCE_PLAN.md` | {{Pendiente}} |
| Informe PMS / PSUR | Art. 85 (informe PMS, Clase I) / Art. 86 (PSUR, Clase IIa/IIb/III) | `POST_MARKET_SURVEILLANCE_PLAN.md` | Verificado |
| Notificación de incidentes graves y FSCA | Art. 87–89 | `INCIDENT_RESPONSE_PLAN.md`; `SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md` | {{Pendiente}} |

---

## 5. Evaluación de conformidad y rol del Notified Body

| Clase MDR | Intervención del Notified Body | Vía de conformidad (orientativa) |
|---|---|---|
| **I** | No (autocertificación), salvo Im/Is/Ir/Imeasurement | Declaración UE de Conformidad por el fabricante |
| **IIa** | Sí | QMS (Anexo IX) o verificación de producto (Anexo XI) |
| **IIb** | Sí | QMS (Anexo IX) + evaluación de doc. técnica |
| **III** | Sí (más intensivo) | QMS (Anexo IX) + examen del expediente de diseño |

> La **evaluación de conformidad** se rige por el **Art. 52** y los **Anexos IX–XI**. La selección de la vía depende de la clase determinada en §1.

| Elemento del proceso | Documento DHF | Estado |
|---|---|---|
| QMS conforme a Art. 10 §9 (basado en ISO 13485) | `ISO_13485_READINESS_PLAN.md` | {{Pendiente}} |
| Persona responsable del cumplimiento normativo (PRRC, Art. 15) | {{TODO: nombrar PRRC}} | {{Pendiente}} |
| Sistema de gestión de riesgos | `ISO_14971_RISK_MATRIX.md` | {{Pendiente}} |
| Identificación UDI / registro EUDAMED | {{TODO}} | {{Pendiente}} |
| Declaración UE de Conformidad (Anexo IV) | {{TODO — la emite el fabricante al cierre}} | {{Pendiente}} |

---

## 6. Normas armonizadas — del DHF al MDR

El DHF ya está construido sobre normas que dan **presunción de conformidad** con GSPR cuando están armonizadas bajo MDR (confirmar estado de armonización vigente en el *Official Journal*).

| Norma del DHF | GSPR / requisito MDR que soporta | Documento DHF de entrada |
|---|---|---|
| IEC 62304 | Anexo I §17.2 (ciclo de vida del software) | `SOFTWARE_DEVELOPMENT_PLAN.md` |
| ISO 14971 | Anexo I §3–§4 (gestión de riesgos) | `ISO_14971_RISK_MATRIX.md` |
| ISO 13485 | Art. 10 §9 (QMS) | `ISO_13485_READINESS_PLAN.md` |
| IEC 62366-1 | Anexo I §5 (factores humanos / usabilidad) | `CERTIFICATION_HOWTO.md` §4 |
| IEC 81001-5-1 | Anexo I §17.4 (seguridad informática) | `SBOM_MANAGEMENT_PLAN.md`; `COMPLIANCE_AND_SECURITY_MASTER.md` |

---

## 7. Huecos y pendientes MDR

| Hueco | Acción pendiente | Responsable |
|---|---|---|
| Clase MDR (Regla 11) sin confirmar | Determinar I/IIa/IIb/III | {{OWNER}} |
| GSPR checklist por requisito individual sin completar | Expandir §2 a checklist completa del Anexo I | {{OWNER}} |
| PRRC sin designar | Nombrar persona responsable (Art. 15) | {{OWNER}} |
| Estado de armonización de normas | Verificar contra Official Journal vigente | {{OWNER}} |
| Referencias de cláusula | Verificadas contra el texto consolidado (§14.2(d), §17.1–§17.4, §22, Art. 85/86, Regla 11) | ✓ verificado |

---

## 8. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | {{OWNER}} | Mapeo EU MDR inicial (Regla 11, GSPR, Anexos II/III, Notified Body). |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md) · [Crosswalk](./REGULATORY_FRAMEWORK_CROSSWALK.md)
</content>
