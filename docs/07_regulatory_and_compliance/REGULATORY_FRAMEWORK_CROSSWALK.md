# Regulatory Framework Crosswalk — Matriz Maestra de Cobertura

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Matriz maestra de cobertura cross-framework del DHF de **{{PROJECT_NAME}}**. Cruza **cada documento existente del DHF** contra la cláusula/sección del estándar que ayuda a satisfacer, en seis marcos: **IEC 62304**, **ISO 14971**, **ISO 13485**, **EU MDR 2017/745**, **FDA (21 CFR 820 + guías)** e **IMDRF SaMD**. Es el documento que un auditor abre primero para entrar al expediente.
>
> **Esto NO es una declaración de conformidad.** Cada celda indica *qué requisito ayuda a cubrir un documento*, no que el requisito esté satisfecho. La evidencia de cumplimiento vive en cada documento referenciado y en la matriz de trazabilidad. `N/A` = el documento no aplica a ese marco. `{{VERIFICAR_CLAUSULA}}` = número de cláusula pendiente de verificación por el responsable regulatorio antes de usar el mapeo en una sumisión.
>
> Mantenida por `docs-dhf`. Cada path debe existir HOY (verificado contra el árbol de `docs/`).

---

## 1. Cómo leer esta matriz

- **Fila** = un documento del DHF que existe hoy.
- **Columna** = un marco regulatorio.
- **Celda** = la cláusula/sección de ese marco a cuya evidencia contribuye el documento, o `N/A`.
- Un documento puede contribuir a varias cláusulas; se listan las principales.
- Los **números de cláusula** son orientativos: el responsable regulatorio los confirma contra la edición vigente de cada norma antes de cualquier sumisión.

**Ediciones de referencia asumidas** (confirmar vigencia en `REGULATORY_VERSION_LOG.md`):

| Marco | Edición de referencia |
|---|---|
| IEC 62304 | 2006 + Amд.1:2015 |
| ISO 14971 | 2019 (+ ISO/TR 24971:2020 como guía) |
| ISO 13485 | 2016 |
| EU MDR | Reglamento (UE) 2017/745 |
| FDA QSR/QMSR | 21 CFR 820 (QMSR, vigente 2026-02-02, incorpora ISO 13485:2016 por referencia) |
| IMDRF SaMD | N10 (definiciones) + N12 (categorización de riesgo) + N23 (QMS) + N41 (eval. clínica) |

---

## 2. Matriz de cobertura — documentos del DHF ↔ estándares

### 2.1 Gestión de riesgo y trazabilidad (`docs/07_*`)

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `ISO_14971_RISK_MATRIX.md` | §7 (gestión de riesgo) | §5–§8 (análisis, evaluación, control, riesgo residual) | §7.1 (planif. realización) | Anexo I §1–§9 (GSPR generales) | 21 CFR 820.30(g) | N12 (categorización de riesgo) |
| `TRACEABILITY_MATRIX_SAMD.md` | §5.1, §5.7, §7.3.3 | §7.4 (verificación de control) | §7.3.x (diseño y desarrollo) | Anexo II §3 (info de diseño/fabricación) | 21 CFR 820.30(j) (DHF) | N12 §8 (consideraciones) |
| `SOFTWARE_SAFETY_CLASSIFICATION.md` | §4.3 (clasificación A/B/C) | §4 (proceso de riesgo) | N/A | Regla 11 (Anexo VIII) | Documentation Level (Basic/Enhanced) — guía Premarket Jun-2023 | N12 (categoría I–IV) |
| `RISK_CONTROL_TRACEABILITY.md` | §7.3 (trazabilidad de control) | §7.4, §7.5 (verif. e impl. de control) | §7.3.6 (verif. de diseño) | Anexo I §4 (control de riesgo) | 21 CFR 820.30(f)(g) | N12 §7 |
| `CRITICAL_MODULES_INVENTORY.md` | §4.3, §5.3 (arquitectura por clase) | §5.4 (identificación de peligros) | §7.3.3 (entradas de diseño) | Anexo I §17 (sist. electrónicos prog.) | System/Software Architecture Diagram (guía Premarket Jun-2023) + Risk Management File | N12 (significancia de info) |

### 2.2 Ciclo de vida y mantenimiento (`docs/07_*`)

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `SOUP_INVENTORY.md` | §5.1.5, §8.1.2 (SOUP) | §7 (riesgo de terceros) | §7.4 (compras) | Anexo I §17.2 | FDA Cybersecurity Guidance §V.B (SBOM) | N23 (QMS) |
| `SOFTWARE_MAINTENANCE_PLAN.md` | §6 (proceso de mantenimiento) | §10 (post-producción) | §7.5 (provisión del servicio) | Art. 83 (vigilancia post-mercado) | 21 CFR 820.30(i) (cambios de diseño) | N23 |
| `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md` | §8 (gestión de configuración) | N/A | §4.2.4/§4.2.5 (control de docs/registros) | Anexo II §1–§2 | 21 CFR 820.30(j), 21 CFR 11 | N23 |
| `SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md` | §9 (resolución de problemas) | §10 (info de producción/post-prod.) | §8.3, §8.5 (no conforme, CAPA) | Art. 87–88 (vigilancia, reporte) | 21 CFR 820.100 (CAPA) | N23 |
| `SBOM_MANAGEMENT_PLAN.md` | §8, §5.1.4 | §7 (riesgo de SOUP) | §7.4 | FDA Cybersecurity Guidance (Sep 2023) §V.B; §524B FD&C | Art. 17 (CRA, mercado UE) | N23 |
| `REGULATORY_VERSION_LOG.md` | §5.1, §8.2.4 | N/A | §4.2.4 (control de documentos) | Anexo II §1 (doc técnica) | 21 CFR 820.40 (control de documentos) | N23 |

### 2.3 Evidencia clínica y post-market (`docs/07_*`)

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `CLINICAL_EVALUATION_PLAN.md` | N/A | §3 (uso previsto) | §7.3.3 (entradas de diseño) | Art. 61 + Anexo XIV Parte A | Guía FDA *SaMD: Clinical Evaluation* (3 pilares IMDRF: asociación clínica válida, validación analítica, validación clínica) | N41 (eval. clínica) |
| `CLINICAL_VALIDATION_REPORT.md` | §5.7 (verif. de sistema) | §7.4 (verif. de control) | §7.3.7 (validación de diseño) | Art. 61 + Anexo XIV | 21 CFR 820.30(g) (validación) | N41 |
| `POST_MARKET_SURVEILLANCE_PLAN.md` | §6.1 (plan de mantenimiento) | §10 (post-producción) | §8.2.1 (retroalimentación) | Art. 83–86 + Anexo III | 21 CFR 803 (reporte rutinario de eventos); 21 CFR 822 solo si la FDA emite una orden §522 | N23 |

### 2.4 Etiquetado e instrucciones (`docs/07_*`)

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `INSTRUCTIONS_FOR_USE_IFU.md` | N/A | §8 (info de seguridad) | §7.5.1 | Anexo I §23 (etiqueta e IFU) | 21 CFR 801 (labeling) | N10 (definiciones) |
| `MEDICAL_DEVICE_LABELING.md` | N/A | §8 (info residual) | §7.5.1 | Anexo I §23 | 21 CFR 801 | N/A |

### 2.5 Seguridad y privacidad (`docs/07_*`)

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `COMPLIANCE_AND_SECURITY_MASTER.md` | §5.1 (planificación) | §4 (proceso) | §4.1 (QMS general) | Anexo I §17.4 (ciberseguridad) | FDA Cybersecurity Guidance (Sep 2023) | N23 |
| `COMPLIANCE_CHECKLIST.md` | §5.5 (implementación) | §7 (control) | §7.5 | Anexo I §17.2 | FDA Cybersecurity Guidance §V | N/A |
| `PRIVACY_POLICY.md` | N/A | N/A | N/A | (GDPR — fuera de MDR) | HIPAA 45 CFR 164 | N/A |
| `DATA_RETENTION_POLICY.md` | N/A | N/A | §4.2.5 (control de registros) | (GDPR Art. 5) | HIPAA 45 CFR 164.310(d) | N/A |
| `DATA_FLOW_DOCUMENTATION.md` | §5.3 (arquitectura) | §5.4 (peligros) | §7.3.3 | Anexo I §17.4 (seguridad) | FDA Cybersecurity Guidance §IV (threat model) | N23 |
| `INCIDENT_RESPONSE_PLAN.md` | §9 (resolución) | §10 (post-prod.) | §8.5 (CAPA) | Art. 87–89 (incidentes/FSCA) | FDA Cybersecurity §VI; §524B | N23 |
| `BREACH_NOTIFICATION_TEMPLATE.md` | N/A | N/A | §8.3 | (GDPR Art. 33–34) | HIPAA 45 CFR 164.400–414 | N/A |

### 2.6 Certificación y QMS (`docs/07_*`)

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `CERTIFICATION_HOWTO.md` | §5.1 (planificación global) | §4 | §7.3 (diseño y desarrollo) | Art. 52 (eval. de conformidad) | 510(k)/De Novo/PMA | N23 |
| `ISO_13485_READINESS_PLAN.md` | N/A | N/A | §4–§8 (QMS completo) | Art. 10 §9 (QMS del fabricante) | 21 CFR 820 / QMSR | N23 |
| `FDA_SUBMISSION_MAPPING.md` (este eje) | §5.x (mapeo) | §7 | N/A | N/A | 510(k)/De Novo/PMA + PCCP | N12 |
| `EU_MDR_MAPPING.md` (este eje) | §4.3 (clasif.) | §5–§8 | §7.3 | Regla 11 + Anexo I/II/III | N/A | N12 |
| `IMDRF_SAMD_FRAMEWORK.md` (este eje) | §4.3 | §4–§5 | N/A | Regla 11 (paralelo) | Risk-based framework (paralelo) | N10 + N12 |
| `INFOSEC_READINESS_ISO27001_SOC2.md` (este eje) | N/A | N/A | §6.3 (infraestructura) | Anexo I §17.4 | FDA Cybersecurity Guidance | N23 |

### 2.7 Documentos fuera de `07_*` que también son evidencia regulatoria

| Documento DHF | IEC 62304 | ISO 14971 | ISO 13485 | EU MDR 2017/745 | FDA | IMDRF SaMD |
|---|---|---|---|---|---|---|
| `02_architecture_and_design/ARCHITECTURE_OVERVIEW.md` | §5.3 (arquitectura) | §5.4 | §7.3.3 | Anexo I §17.1 | 21 CFR 820.30(c)(d) | N12 |
| `03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md` | §5.1 (plan de desarrollo) | §4.4 (plan de riesgo) | §7.3.2 (planif. de diseño) | Anexo II §6 | 21 CFR 820.30(b) | N23 |
| `03_software_development_plan/COMPLETE_TESTING_STRATEGY.md` | §5.5–§5.7 (verif.) | §7.4 | §7.3.6 (verif. de diseño) | Anexo II §6.1 | 21 CFR 820.30(f) | N23 |
| `03_software_development_plan/AUDIT_PROTOCOL.md` | §5.1.4, §9 | §9 (revisión) | §8.2.4 (auditoría interna) | Anexo II | 21 CFR 820.22 | N23 |
| `01_governance_and_strategy/VISION_AND_GOVERNANCE.md` | §5.1.1 (proceso) | §4.2 (responsabilidades) | §5 (resp. de dirección) | Art. 10 §9 | 21 CFR 820.20 (mgmt resp.) | N23 |
| `04_user_documentation/USER_GUIDE.md` | N/A | §8 (info de seguridad) | §7.2.1 | Anexo I §23 (IFU) | 21 CFR 801 | N10 |
| `05_design_decisions/RFC-*.md` | §5.4 (diseño detallado) | §7.1 (opciones de control) | §7.3.3 | Anexo II §3 | 21 CFR 820.30(c) | N/A |
| `06_operations_and_runbooks/DEPLOY_RUNBOOK.md` | §5.8 (release) | N/A | §7.5.1 | N/A | 21 CFR 820.70 | N/A |
| `08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md` | §5.7, §9 (problemas conocidos) | §10 | §8.3 (no conforme) | Art. 88 (tendencias) | 21 CFR 820.100 (CAPA) | N23 |

---

## 3. Cobertura inversa — ¿qué documento responde cada marco?

Tabla de entrada rápida para el auditor: dado un marco, ¿dónde empieza a leer?

| Marco | Documento de entrada recomendado | Documento de profundidad |
|---|---|---|
| IEC 62304 | `03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md` | `TRACEABILITY_MATRIX_SAMD.md` |
| ISO 14971 | `ISO_14971_RISK_MATRIX.md` | `RISK_CONTROL_TRACEABILITY.md` |
| ISO 13485 | `ISO_13485_READINESS_PLAN.md` | `REGULATORY_VERSION_LOG.md` |
| EU MDR 2017/745 | `EU_MDR_MAPPING.md` | `CLINICAL_EVALUATION_PLAN.md` |
| FDA | `FDA_SUBMISSION_MAPPING.md` | `SBOM_MANAGEMENT_PLAN.md` |
| IMDRF SaMD | `IMDRF_SAMD_FRAMEWORK.md` | `SOFTWARE_SAFETY_CLASSIFICATION.md` |
| ISO/IEC 27001 / SOC 2 | `INFOSEC_READINESS_ISO27001_SOC2.md` | `COMPLIANCE_CHECKLIST.md` |

---

## 4. Huecos conocidos del crosswalk

Marcá acá toda celda donde el mapeo está incompleto o pendiente de verificación, para que el auditor no la descubra primero:

| Hueco | Marco afectado | Acción pendiente | Responsable |
|---|---|---|---|
| Nivel de documentación FDA por riesgo (Basic/Enhanced) sin fijar | FDA | Determinar nivel según *Content of Premarket Submissions for Device Software Functions* (Jun 2023) | {{OWNER}} |
| Referencias de cláusula de la §2 | Varios | Verificadas contra fuentes oficiales (FDA/EUR-Lex/IMDRF/AICPA); reconfirmar contra la edición vigente antes de una sumisión | ✓ verificado |
| Mapeo de GSPR Anexo I por requisito individual | EU MDR | Completar en `EU_MDR_MAPPING.md` §GSPR | {{OWNER}} |

---

## 5. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | {{OWNER}} | Crosswalk inicial cross-framework (eje cobertura regulatoria global). |

> Toda doc nueva del DHF debe añadirse a esta matriz en la misma pasada (lo verifica `docs-dhf` junto al Master Map).

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
</content>
</invoke>
