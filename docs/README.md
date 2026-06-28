# Design History File (DHF) — Índice navegable

Brújula del DHF de {{PROJECT_NAME}}. El **[Master Map](./00_master/MASTER_MAP.md)** es el mapa maestro vivo; lo mantiene el agente `docs-dhf`. Este índice enlaza **todos** los documentos para que el DHF se navegue solo.

## 00 · Master

- [MASTER_MAP](./00_master/MASTER_MAP.md) — mapa maestro: identidad del dispositivo, arquitectura, módulos clínicos críticos, versiones.

## 01 · Gobernanza y estrategia

- [VISION_AND_GOVERNANCE](./01_governance_and_strategy/VISION_AND_GOVERNANCE.md) — visión del producto, gobernanza, estrategia regulatoria, Regla 0.

## 02 · Arquitectura y diseño

- [ARCHITECTURE_OVERVIEW](./02_architecture_and_design/ARCHITECTURE_OVERVIEW.md) — visión de arquitectura, ítems de software y su clase, puntos de fail-safe.

## 03 · Plan de desarrollo de software (IEC 62304 §5.1)

- [SOFTWARE_DEVELOPMENT_PLAN](./03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md) — plan de ciclo de vida, actividades por clase, entregables.
- [DEVELOPMENT_GUIDE_COMPLETE](./03_software_development_plan/DEVELOPMENT_GUIDE_COMPLETE.md) — guía de desarrollo: setup, comandos, estándares, Definition of Done.
- [COMPLETE_TESTING_STRATEGY](./03_software_development_plan/COMPLETE_TESTING_STRATEGY.md) — estrategia de verificación SaMD-grade.
- [TESTING_TOOLS](./03_software_development_plan/TESTING_TOOLS.md) — guía maestra del stack de testing (qué herramienta, cuándo, comandos).
- [AUDIT_PROTOCOL](./03_software_development_plan/AUDIT_PROTOCOL.md) — protocolo de auditoría interna de changesets/fases.

## 05 · Decisiones de diseño (RFCs)

- [RFC-TEMPLATE](./05_design_decisions/RFC-TEMPLATE.md) — plantilla para proponer una decisión estructural.
- [RFC-001 · Cifrado en reposo](./05_design_decisions/RFC-001-encryption-at-rest.md) — AES-256-GCM a nivel columna.
- [RFC-002 · Identidad JWT-only](./05_design_decisions/RFC-002-identity-jwt-only.md) — identidad solo del token.
- [RFC-003 · Scheduler externo](./05_design_decisions/RFC-003-external-scheduler.md) — cron gestionado vs interno.

## 06 · Operaciones y runbooks

- [DEPLOY_RUNBOOK](./06_operations_and_runbooks/DEPLOY_RUNBOOK.md) — pre-checks, migración atómica, rollback, verificación post-deploy.
- [INCIDENT_RUNBOOK](./06_operations_and_runbooks/INCIDENT_RUNBOOK.md) — diagnóstico de incidentes en producción, síntomas comunes, escalada.
- [INCIDENT_POSTMORTEM_TEMPLATE](./06_operations_and_runbooks/INCIDENT_POSTMORTEM_TEMPLATE.md) — post-mortem sin culpa (timeline, causa raíz, CAPA, lecciones).
- [INCIDENT_RESPONSE_DRILL_REPORT](./06_operations_and_runbooks/INCIDENT_RESPONSE_DRILL_REPORT.md) — registro de simulacros periódicos de respuesta a incidentes.

## 07 · Regulatorio y compliance

**Gestión de riesgo y trazabilidad**
- [ISO_14971_RISK_MATRIX](./07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md) — matriz de gestión de riesgo.
- [TRACEABILITY_MATRIX_SAMD](./07_regulatory_and_compliance/TRACEABILITY_MATRIX_SAMD.md) — trazabilidad necesidad → REQ → diseño → verificación → riesgo.
- [SOFTWARE_SAFETY_CLASSIFICATION](./07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md) — clasificación de seguridad IEC 62304 §4.3.
- [RISK_CONTROL_TRACEABILITY](./07_regulatory_and_compliance/RISK_CONTROL_TRACEABILITY.md) — cruce riesgo → control → REQ → test → riesgo residual (cierra el loop).
- [CRITICAL_MODULES_INVENTORY](./07_regulatory_and_compliance/CRITICAL_MODULES_INVENTORY.md) — clasificación de módulos por criticidad y umbral de rigor de testing.

**Ciclo de vida y mantenimiento**
- [SOUP_INVENTORY](./07_regulatory_and_compliance/SOUP_INVENTORY.md) — inventario de Software of Unknown Provenance.
- [SOFTWARE_MAINTENANCE_PLAN](./07_regulatory_and_compliance/SOFTWARE_MAINTENANCE_PLAN.md) — plan de mantenimiento IEC 62304 §6.
- [SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN](./07_regulatory_and_compliance/SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md) — gestión de configuración.
- [SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE](./07_regulatory_and_compliance/SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md) — resolución de problemas IEC 62304 §9.
- [SBOM_MANAGEMENT_PLAN](./07_regulatory_and_compliance/SBOM_MANAGEMENT_PLAN.md) — generación, almacenamiento y revisión del SBOM por release.
- [REGULATORY_VERSION_LOG](./07_regulatory_and_compliance/REGULATORY_VERSION_LOG.md) — control de versiones de todos los docs regulatorios (ISO 13485).

**Evidencia clínica y post-market**
- [CLINICAL_EVALUATION_PLAN](./07_regulatory_and_compliance/CLINICAL_EVALUATION_PLAN.md) — plan de evaluación clínica.
- [CLINICAL_VALIDATION_REPORT](./07_regulatory_and_compliance/CLINICAL_VALIDATION_REPORT.md) — reporte de validación clínica.
- [POST_MARKET_SURVEILLANCE_PLAN](./07_regulatory_and_compliance/POST_MARKET_SURVEILLANCE_PLAN.md) — vigilancia post-comercialización.

**Etiquetado e instrucciones**
- [INSTRUCTIONS_FOR_USE_IFU](./07_regulatory_and_compliance/INSTRUCTIONS_FOR_USE_IFU.md) — instrucciones de uso.
- [MEDICAL_DEVICE_LABELING](./07_regulatory_and_compliance/MEDICAL_DEVICE_LABELING.md) — etiquetado del dispositivo.

**Seguridad y privacidad**
- [COMPLIANCE_AND_SECURITY_MASTER](./07_regulatory_and_compliance/COMPLIANCE_AND_SECURITY_MASTER.md) — documento maestro de seguridad/compliance.
- [PRIVACY_POLICY](./07_regulatory_and_compliance/PRIVACY_POLICY.md) — política de privacidad.
- [DATA_RETENTION_POLICY](./07_regulatory_and_compliance/DATA_RETENTION_POLICY.md) — política de retención.
- [DATA_FLOW_DOCUMENTATION](./07_regulatory_and_compliance/DATA_FLOW_DOCUMENTATION.md) — flujo de datos y fronteras de confianza.
- [INCIDENT_RESPONSE_PLAN](./07_regulatory_and_compliance/INCIDENT_RESPONSE_PLAN.md) — respuesta a incidentes y notificación de brechas.
- [COMPLIANCE_CHECKLIST](./07_regulatory_and_compliance/COMPLIANCE_CHECKLIST.md) — checklist operativo control-por-control GDPR Art.32 + HIPAA.
- [BREACH_NOTIFICATION_TEMPLATE](./07_regulatory_and_compliance/BREACH_NOTIFICATION_TEMPLATE.md) — notificación de brecha a autoridad y titulares (plazos GDPR/HIPAA).

**Certificación**
- [CERTIFICATION_HOWTO](./07_regulatory_and_compliance/CERTIFICATION_HOWTO.md) — cómo llegar a certificación para tu clase.
- [ISO_13485_READINESS_PLAN](./07_regulatory_and_compliance/ISO_13485_READINESS_PLAN.md) — preparación del QMS hacia auditoría externa (gaps y checkpoints).

## 08 · Verificación y auditorías (IEC 62304 §5.7)

- [TECHNICAL_DEBT_SUMMARY](./08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md) — deuda técnica abierta (códigos D-XXX-NN).
- [TECHNICAL_DEBT_HISTORY](./08_verification_and_audits/TECHNICAL_DEBT_HISTORY.md) — archivo cronológico de deuda cerrada.

## 09 · Experiencia de ingeniería

- [PRODUCTION_LESSONS](./09_engineering_experience/PRODUCTION_LESSONS.md) — field notes: lecciones de producción (síntoma → causa → lección).
- [REFERENCE_ARCHITECTURE](./09_engineering_experience/REFERENCE_ARCHITECTURE.md) — patrón híbrido offline-first y el porqué de cada decisión.
- [MULTI_AGENT_ENGINEERING_METHOD](./09_engineering_experience/MULTI_AGENT_ENGINEERING_METHOD.md) — método "Mesa de Ingenieros" (anti-drift + verificación adversarial).

---

## Regla de integridad

Tras renombrar/mover/eliminar cualquier `.md`, corré el link-checker cross-doc y resolvé los rotos en el mismo PR:

```bash
bash scripts/check_doc_links.sh
```

Ningún PR de reorg cierra con enlaces rotos.
