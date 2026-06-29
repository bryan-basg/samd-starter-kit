# FDA Submission Mapping — Puente al Marco Regulatorio de EE. UU.

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Puente entre el DHF de **{{PROJECT_NAME}}** (construido sobre IEC 62304 + ISO 14971 + ISO 13485) y el marco regulatorio de la **U.S. Food and Drug Administration (FDA)**. Mapea cada requisito de una *premarket submission* para SaMD al documento del DHF que lo cubre.
>
> **Esto NO es una sumisión ni una declaración de conformidad con la FDA.** Es un andamio de mapeo. El producto **no** afirma estar autorizado, despejado (*cleared*) ni aprobado por la FDA. Cada celda de evidencia se completa con el documento real al armar el expediente. `{{VERIFICAR_CLAUSULA}}` = referencia normativa pendiente de verificación.
>
> Mantenida por `docs-dhf`. La vía regulatoria, la clase FDA y el *Documentation Level* los fija el responsable regulatorio ({{OWNER}}); este documento no los presume.

---

## 1. Determinación de la vía regulatoria

La FDA clasifica los dispositivos en **Class I / II / III** (eje propio, distinto de la Clase SaMD {{SAMD_CLASS}} de IEC 62304) y asigna la vía según el riesgo y la existencia de un *predicate*.

| Vía | Cuándo aplica | Base legal | Clase FDA típica |
|---|---|---|---|
| **Exenta de 510(k)** | Dispositivo Class I (y algunos II) exento por regulación | 21 CFR 8xx (lista de exenciones) | I |
| **510(k)** (Premarket Notification) | Existe un *predicate* legalmente comercializado; se demuestra **equivalencia sustancial** | §510(k) FD&C Act | II (mayoría) |
| **De Novo** | Riesgo bajo/moderado **sin** predicate adecuado; crea una nueva clasificación | §513(f)(2) FD&C Act | I / II |
| **PMA** (Premarket Approval) | Alto riesgo; sostiene la vida o presenta riesgo potencial irrazonable | §515 FD&C Act | III |

| Pregunta de decisión | Respuesta del proyecto |
|---|---|
| ¿Cuál es el uso previsto declarado? | {{INTENDED_USE}} |
| ¿Existe un *predicate* legalmente comercializado? | {{TODO: sí/no + identificación del predicate}} |
| ¿La función es de *Clinical Decision Support* (CDS) potencialmente no-dispositivo? | {{TODO — evaluar contra la guía CDS Software (Sep 2022)}} |
| Clase FDA estimada | {{TODO: I / II / III}} |
| **Vía seleccionada** | {{TODO: Exenta / 510(k) / De Novo / PMA}} |

> **Nota CDS:** algunas funciones de soporte a la decisión quedan **fuera** de la definición de dispositivo (§520(o) FD&C Act). Si la función califica como CDS no-dispositivo, no requiere sumisión — pero esa determinación la documenta el responsable regulatorio, no se asume.

---

## 2. Contenido de una premarket submission para SaMD ↔ DHF

Mapeo del contenido esperado (alineado con *Content of Premarket Submissions for Device Software Functions*, FDA, Jun 2023) al documento del DHF que lo cubre.

> El **Documentation Level** (Basic vs Enhanced) reemplazó al antiguo "Level of Concern". Lo determina el riesgo de la función de software; lo fija {{OWNER}}: **Documentation Level = {{TODO: Basic / Enhanced}}**.

| Elemento de la submission FDA | Documento DHF que lo cubre | Evidencia / estado |
|---|---|---|
| **Documentation Level Evaluation** | `SOFTWARE_SAFETY_CLASSIFICATION.md` (mapear Clase {{SAMD_CLASS}} → Basic/Enhanced) | {{Pendiente de evidencia}} |
| **Software Description** | `02_architecture_and_design/ARCHITECTURE_OVERVIEW.md` | {{Pendiente de evidencia}} |
| **System and Software Architecture Diagram** | `02_architecture_and_design/ARCHITECTURE_OVERVIEW.md`; `DATA_FLOW_DOCUMENTATION.md` | {{Pendiente de evidencia}} |
| **Risk Management File** | `ISO_14971_RISK_MATRIX.md`; `RISK_CONTROL_TRACEABILITY.md` | {{Pendiente de evidencia}} |
| **Software Requirements Specification (SRS)** | `TRACEABILITY_MATRIX_SAMD.md` (columna REQ) + `SOFTWARE_DEVELOPMENT_PLAN.md` | {{Pendiente de evidencia}} |
| **Software Design Specification (SDS)** | `05_design_decisions/RFC-*.md`; `ARCHITECTURE_OVERVIEW.md` | {{Pendiente de evidencia}} |
| **Traceability** | `TRACEABILITY_MATRIX_SAMD.md` | {{Pendiente de evidencia}} |
| **Software Development / Configuration / Maintenance Practices** | `SOFTWARE_DEVELOPMENT_PLAN.md`; `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md`; `SOFTWARE_MAINTENANCE_PLAN.md` | {{Pendiente de evidencia}} |
| **Verification & Validation (V&V) Testing** | `COMPLETE_TESTING_STRATEGY.md`; `CLINICAL_VALIDATION_REPORT.md` | {{Pendiente de evidencia}} |
| **Revision Level History** | `REGULATORY_VERSION_LOG.md`; `04_user_documentation/RELEASE_NOTES_TEMPLATE.md` | {{Pendiente de evidencia}} |
| **Unresolved Anomalies (bugs/known issues)** | `08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md` | {{Pendiente de evidencia}} |
| **SOUP / Off-the-shelf Software** | `SOUP_INVENTORY.md` | {{Pendiente de evidencia}} |

---

## 3. FDA Premarket Cybersecurity ↔ DHF

Alineado con *Cybersecurity in Medical Devices: Quality System Considerations and Content of Premarket Submissions* (FDA, Sep 2023) y **§524B FD&C Act** (requisitos de "cyber devices", añadidos por la Consolidated Appropriations Act 2023).

| Requisito de ciberseguridad FDA | Documento DHF que lo cubre | Evidencia / estado |
|---|---|---|
| **Secure Product Development Framework (SPDF)** | `COMPLIANCE_AND_SECURITY_MASTER.md`; `SOFTWARE_DEVELOPMENT_PLAN.md` | {{Pendiente de evidencia}} |
| **Threat Model** | `DATA_FLOW_DOCUMENTATION.md` (fronteras de confianza) | {{Pendiente de evidencia}} |
| **Cybersecurity Risk Assessment** | `ISO_14971_RISK_MATRIX.md` (riesgos `R-SEC-*`) | {{Pendiente de evidencia}} |
| **Software Bill of Materials (SBOM)** | `SBOM_MANAGEMENT_PLAN.md` + `.github/workflows/sbom.yml` + `sbom/` | {{Pendiente de evidencia}} |
| **Security Testing (SAST/DAST/fuzz/pentest)** | `COMPLIANCE_CHECKLIST.md` §A.4; `TESTING_TOOLS.md` | {{Pendiente de evidencia}} |
| **Vulnerability Management / Coordinated Disclosure** | `SBOM_MANAGEMENT_PLAN.md` §6; `INCIDENT_RESPONSE_PLAN.md` | {{Pendiente de evidencia}} |
| **Security Architecture views** | `ARCHITECTURE_OVERVIEW.md`; `DATA_FLOW_DOCUMENTATION.md` | {{Pendiente de evidencia}} |
| **Postmarket monitoring / patching plan** | `SOFTWARE_MAINTENANCE_PLAN.md`; `POST_MARKET_SURVEILLANCE_PLAN.md` | {{Pendiente de evidencia}} |

> **Controles técnicos vivos referenciados** (la fuente de verdad es el código; el path se confirma en `COMPLIANCE_CHECKLIST.md`):
> - Cifrado en reposo AES-256-GCM → `app/models/types.py` (ver checklist §A.1)
> - Identidad JWT-only → `app/dependencies.py` (ver checklist §A.2)
> - Audit middleware de mutaciones → `app/middleware/audit.py` (ver checklist §B.3)
> - SAST/SCA/SBOM en CI → `.github/workflows/` (ver checklist §A.4)

---

## 4. Predetermined Change Control Plan (PCCP) — funciones de IA/ML

Aplica **solo si {{PROJECT_NAME}} incorpora una función de IA/ML adaptativa**. Alineado con *Marketing Submission Recommendations for a Predetermined Change Control Plan for Artificial Intelligence-Enabled Device Software Functions* (FDA, guía final Dic 2024).

> **Si el proyecto NO usa IA/ML, declarar N/A aquí explícitamente** y omitir el resto de esta sección. Estado actual: {{TODO: aplica / N/A}}.

Un PCCP permite preautorizar ciertos cambios al modelo sin nueva sumisión, si se especifican por adelantado. Tres componentes obligatorios:

| Componente PCCP | Contenido esperado | Documento DHF de apoyo | Estado |
|---|---|---|---|
| **Description of Modifications** | Qué cambios del modelo se preautorizan (reentrenamiento, umbrales, inputs) | `05_design_decisions/RFC-*.md` (RFC por cambio de modelo) | {{TODO}} |
| **Modification Protocol** | Cómo se desarrollan, validan e implementan los cambios (data management, reentrenamiento, V&V, update) | `COMPLETE_TESTING_STRATEGY.md`; `SOFTWARE_MAINTENANCE_PLAN.md` | {{TODO}} |
| **Impact Assessment** | Beneficios/riesgos de cada cambio preautorizado vs versión autorizada | `ISO_14971_RISK_MATRIX.md` (riesgos `R-IA-*`) | {{TODO}} |

**Good Machine Learning Practice (GMLP):** los cambios del PCCP deben respetar los *Guiding Principles* GMLP (FDA/Health Canada/MHRA, Oct 2021). Ver `IMDRF_SAMD_FRAMEWORK.md` §GMLP para el detalle de los 10 principios y su mapeo.

| Salvaguarda de IA pre-certificación | Dónde se garantiza | Estado |
|---|---|---|
| Sin claims de dispositivo no autorizado en UI (glosario clínico) | `MEDICAL_DEVICE_LABELING.md`; `USER_GUIDE.md` | {{Pendiente}} |
| Validador clínico + fallback seguro de la IA | `ISO_14971_RISK_MATRIX.md` (`R-IA-*`) + `app/services/` | {{Pendiente}} |
| Transparencia del modelo (versión, datos, limitaciones) | `INSTRUCTIONS_FOR_USE_IFU.md` | {{Pendiente}} |

---

## 5. QMS y 21 CFR 820 (QMSR)

Desde el **2026-02-02**, la **Quality Management System Regulation (QMSR)** incorpora **ISO 13485:2016 por referencia** en 21 CFR Part 820. La preparación del QMS para FDA reutiliza el plan ISO 13485 del DHF.

| Requisito QMS (21 CFR 820 / QMSR) | Documento DHF | Estado |
|---|---|---|
| Design Controls (820.30 → ISO 13485 §7.3) | `ISO_13485_READINESS_PLAN.md`; `TRACEABILITY_MATRIX_SAMD.md` | {{Pendiente}} |
| Document Controls (820.40 → §4.2) | `REGULATORY_VERSION_LOG.md` | {{Pendiente}} |
| CAPA (820.100 → §8.5) | `SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md` | {{Pendiente}} |
| Management Responsibility (820.20 → §5) | `VISION_AND_GOVERNANCE.md` | {{Pendiente}} |

---

## 6. Huecos y pendientes FDA

| Hueco | Acción pendiente | Responsable |
|---|---|---|
| Vía regulatoria sin confirmar | Determinar Exenta/510(k)/De Novo/PMA | {{OWNER}} |
| Documentation Level sin fijar | Basic vs Enhanced según riesgo de la función | {{OWNER}} |
| Determinación CDS no-dispositivo | Evaluar contra guía CDS (Sep 2022) | {{OWNER}} |
| PCCP — aplicabilidad de IA/ML | Confirmar si hay función adaptativa | {{OWNER}} |
| Referencias normativas | Verificadas contra fuentes FDA (guía Premarket Jun-2023, QMSR 21 CFR 820, 21 CFR 803/822, guía SaMD Clinical Evaluation); reconfirmar antes de una sumisión real | ✓ verificado |

---

## 7. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | {{OWNER}} | Mapeo FDA inicial (vías, premarket content, cybersecurity, PCCP). |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md) · [Crosswalk](./REGULATORY_FRAMEWORK_CROSSWALK.md)
</content>
