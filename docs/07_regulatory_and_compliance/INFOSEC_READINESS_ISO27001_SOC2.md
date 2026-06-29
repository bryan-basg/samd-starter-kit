# InfoSec Readiness — ISO/IEC 27001:2022 + SOC 2

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Readiness de seguridad de la información de **{{PROJECT_NAME}}**: mapea los controles técnicos ya presentes en el kit (cifrado AES-256-GCM en reposo, identidad JWT-only, audit middleware, gestión de secretos/KMS, SAST/DAST/SBOM en CI) contra los controles de **ISO/IEC 27001:2022 Anexo A** y los **SOC 2 Trust Services Criteria (TSC 2017, rev. 2022)**.
>
> **Esto NO es una certificación ISO 27001 ni un reporte SOC 2.** Un reporte SOC 2 lo emite un auditor (CPA) independiente; la certificación ISO 27001 la emite un organismo acreditado. Este documento es un andamio de preparación con **celdas de evidencia** para que {{OWNER}} complete. `{{...}}` / "Pendiente de evidencia" = aún sin completar.
>
> **Fuente de verdad = el código.** Los paths que siguen citan el archivo real; el `archivo:línea` exacto se confirma en `COMPLIANCE_CHECKLIST.md`, que es el documento operativo control-por-control. Mantenida por `docs-dhf`.

---

## 1. Alcance y relación con el resto del DHF

- **Alcance:** los controles de seguridad de la información del producto y su pipeline. No reemplaza a `COMPLIANCE_AND_SECURITY_MASTER.md` (visión maestra) ni a `COMPLIANCE_CHECKLIST.md` (GDPR/HIPAA control-por-control); los **complementa** con la lente ISO 27001 / SOC 2.
- **Por qué importa a un SaMD:** EU MDR Anexo I §17.4 y la FDA Cybersecurity Guidance exigen un programa de seguridad de la información maduro. Una postura ISO 27001 / SOC 2 es la forma habitual de demostrarlo a clientes empresariales y aseguradoras.
- **Relación con riesgo clínico:** todo control roto que exponga PHI es además un riesgo clínico (`R-SEC-*` en `ISO_14971_RISK_MATRIX.md`).

| Documento relacionado | Rol |
|---|---|
| `COMPLIANCE_CHECKLIST.md` | Control-por-control GDPR Art.32 + HIPAA (con `archivo:línea`). |
| `COMPLIANCE_AND_SECURITY_MASTER.md` | Documento maestro de seguridad/compliance. |
| `DATA_FLOW_DOCUMENTATION.md` | Fronteras de confianza / modelo de amenazas. |
| `SBOM_MANAGEMENT_PLAN.md` | Gestión de SBOM y vulnerabilidades. |
| `INCIDENT_RESPONSE_PLAN.md` | Respuesta a incidentes y notificación de brechas. |

---

## 2. Inventario de controles técnicos vivos del kit

Controles que el starter kit ya implementa o tiene cableados en CI. El `archivo:línea` exacto se rellena en `COMPLIANCE_CHECKLIST.md`.

| Control del kit | Dónde vive (path) | Evidencia de prueba |
|---|---|---|
| Cifrado en reposo AES-256-GCM (PII/PHI) | `app/models/types.py` (`EncryptedString` o equiv.) | {{test_encrypted_string_*}} |
| Identidad solo del token (JWT-only) | `app/dependencies.py` (`get_current_user`) | {{test_idor_*}} |
| Autorización por recurso (anti-IDOR) | `app/routers/<recurso>.py` | {{Pendiente de evidencia}} |
| Audit middleware de mutaciones (POST/PUT/DELETE/PATCH) | `app/middleware/audit.py` | {{Pendiente de evidencia}} |
| Gestión de secretos / KMS (claves no hardcodeadas) | `app/core/config.py` + secret manager {{CLOUD_STACK}} | {{Pendiente de evidencia}} |
| Fail-safe sin tracebacks al cliente | `app/core/error_handlers.py` | {{test_error_handler_*}} |
| Cabeceras de seguridad (CSP/COOP/etc.) | `app/middleware.py` | {{Pendiente de evidencia}} |
| Redacción de PII/PHI en logs | `app/core/logging_conf.py` | {{Pendiente de evidencia}} |
| SAST (Semgrep) en CI | `.github/workflows/security-audit.yml` | {{Pendiente de evidencia}} |
| SCA + CVEs (Trivy + Dependabot) | `.github/workflows/` + `SBOM_MANAGEMENT_PLAN.md` | {{Pendiente de evidencia}} |
| SBOM (CycloneDX) | `.github/workflows/sbom.yml` + `sbom/` | {{Pendiente de evidencia}} |
| DAST (OWASP ZAP) | `.github/workflows/dast.yml` | {{Pendiente de evidencia}} |
| Fuzz de contrato (Schemathesis) | `.github/workflows/schemathesis.yml` | {{Pendiente de evidencia}} |
| Detección de secretos (Gitleaks) | `scripts/run_gitleaks.sh` + `.gitleaks.toml` | {{Pendiente de evidencia}} |

> Los paths a `app/`, `.github/`, `scripts/` son del esqueleto de referencia; verificar contra el código real del proyecto antes de citar `archivo:línea` en una auditoría.

---

## 3. Mapeo a ISO/IEC 27001:2022 Anexo A

Anexo A 2022 organizado en 4 temas: **A.5** organizacionales, **A.6** personas, **A.7** físicos, **A.8** tecnológicos. Tabla de gaps con celda de evidencia para completar.

| Control Anexo A | Tema | Control del kit que lo soporta | Evidencia / estado |
|---|---|---|---|
| A.5.7 Inteligencia de amenazas | Org. | `DATA_FLOW_DOCUMENTATION.md` (modelo de amenazas) | {{Pendiente de evidencia}} |
| A.5.15 Control de acceso | Org. | Identidad JWT-only + autorización por recurso | {{Pendiente de evidencia}} |
| A.5.16 Gestión de identidad | Org. | `app/dependencies.py` | {{Pendiente de evidencia}} |
| A.5.17 Información de autenticación | Org. | Tokens + gestión de secretos | {{Pendiente de evidencia}} |
| A.5.18 Derechos de acceso | Org. | Autorización por recurso / roles | {{Pendiente de evidencia}} |
| A.5.23 Seguridad para uso de servicios en la nube | Org. | Config {{CLOUD_STACK}} + BAA/DPA del proveedor | {{Pendiente de evidencia}} |
| A.5.24–A.5.28 Gestión de incidentes | Org. | `INCIDENT_RESPONSE_PLAN.md` | {{Pendiente de evidencia}} |
| A.8.2 Derechos de acceso privilegiado | Tec. | {{Pendiente — política de acceso privilegiado}} | {{Pendiente de evidencia}} |
| A.8.3 Restricción de acceso a la información | Tec. | Autorización por recurso (anti-IDOR) | {{Pendiente de evidencia}} |
| A.8.5 Autenticación segura | Tec. | JWT-only + TTL del token | {{Pendiente de evidencia}} |
| A.8.8 Gestión de vulnerabilidades técnicas | Tec. | Trivy + Dependabot + `SBOM_MANAGEMENT_PLAN.md` | {{Pendiente de evidencia}} |
| A.8.9 Gestión de la configuración | Tec. | `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md` | {{Pendiente de evidencia}} |
| A.8.12 Prevención de fuga de datos | Tec. | Redacción de PII/PHI en logs + cifrado en reposo | {{Pendiente de evidencia}} |
| A.8.15 Registro (logging) | Tec. | Audit middleware + logging estructurado | {{Pendiente de evidencia}} |
| A.8.16 Actividades de monitoreo | Tec. | Monitoring {{CLOUD_STACK}} | {{Pendiente de evidencia}} |
| A.8.24 Uso de criptografía | Tec. | AES-256-GCM en reposo + TLS en tránsito + KMS | {{Pendiente de evidencia}} |
| A.8.25 Ciclo de vida de desarrollo seguro | Tec. | `SOFTWARE_DEVELOPMENT_PLAN.md` | {{Pendiente de evidencia}} |
| A.8.26 Requisitos de seguridad de la aplicación | Tec. | `COMPLIANCE_CHECKLIST.md` | {{Pendiente de evidencia}} |
| A.8.28 Codificación segura | Tec. | SAST (Semgrep) + revisión de código | {{Pendiente de evidencia}} |
| A.8.29 Pruebas de seguridad en desarrollo y aceptación | Tec. | SAST + DAST + fuzz + Gitleaks en CI | {{Pendiente de evidencia}} |

> **Documentos del SGSI que ISO 27001 exige y NO están cubiertos por controles técnicos** (cláusulas §4–§10 del cuerpo de la norma, no del Anexo A): política del SGSI, evaluación de riesgos de seguridad de la información, **Statement of Applicability (SoA)**, objetivos, competencias, auditoría interna y revisión por la dirección. Marcados como gap organizacional en §5.

---

## 4. Mapeo a SOC 2 Trust Services Criteria

SOC 2 cubre **Security** (Common Criteria CC1–CC9, obligatoria) y, opcionalmente, **Availability (A1)**, **Processing Integrity (PI1)**, **Confidentiality (C1)** y **Privacy (P)**. Foco en los criterios con soporte técnico directo en el kit.

| Criterio TSC | Categoría | Control del kit que lo soporta | Evidencia / estado |
|---|---|---|---|
| CC6.1 Acceso lógico (autorización + cifrado) | Security | JWT-only + autorización por recurso + AES-256-GCM | {{Pendiente de evidencia}} |
| CC6.2 Registro y autorización de usuarios | Security | Gestión de identidad / alta de usuarios | {{Pendiente de evidencia}} |
| CC6.6 Protección de fronteras (perímetro) | Security | Cabeceras de seguridad + config de red {{CLOUD_STACK}} | {{Pendiente de evidencia}} |
| CC6.7 Cifrado en transmisión | Security | TLS 1.2+ / HSTS | {{Pendiente de evidencia}} |
| CC6.8 Prevención de software malicioso / cambios no autorizados | Security | Gitleaks + SCA + control de configuración | {{Pendiente de evidencia}} |
| CC7.1 Detección de vulnerabilidades | Security | Trivy + Dependabot + SAST | {{Pendiente de evidencia}} |
| CC7.2 Monitoreo de anomalías | Security | Logging estructurado + monitoring | {{Pendiente de evidencia}} |
| CC7.3 Evaluación de eventos de seguridad | Security | `INCIDENT_RESPONSE_PLAN.md` | {{Pendiente de evidencia}} |
| CC7.4 Respuesta a incidentes | Security | `INCIDENT_RESPONSE_PLAN.md` + `BREACH_NOTIFICATION_TEMPLATE.md` | {{Pendiente de evidencia}} |
| CC8.1 Gestión de cambios | Security | `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md` + CI | {{Pendiente de evidencia}} |
| A1.2 Respaldo y recuperación | Availability | Backups {{CLOUD_STACK}} + migraciones reversibles | {{Pendiente de evidencia}} |
| PI1.x Integridad de procesamiento | Proc. Integrity | Validación de esquemas + audit de mutaciones | {{Pendiente de evidencia}} |
| C1.1 Identificación y protección de info confidencial | Confidentiality | Cifrado en reposo + clasificación de datos | {{Pendiente de evidencia}} |
| C1.2 Disposición de info confidencial | Confidentiality | `DATA_RETENTION_POLICY.md` | {{Pendiente de evidencia}} |
| P (Privacy) | Privacy | `PRIVACY_POLICY.md` + GDPR/HIPAA en `COMPLIANCE_CHECKLIST.md` | {{Pendiente de evidencia}} |

> CC6.2 (registro/autorización de usuarios) y PI1.x (integridad de procesamiento, PI1.1–PI1.5) verificados verbatim contra los *2017 Trust Services Criteria* del AICPA (revisión 2022). Reconfirmar contra la edición vigente de los TSC antes de usarlos en un reporte de auditoría formal.

---

## 5. Tabla de gaps organizacionales (no cubiertos por código)

Estos gaps son de **proceso/gobernanza**, no de código — son los que más frenan una auditoría de seguridad y NO los resuelve el starter kit:

| Gap | Marco | Acción pendiente | Responsable | Estado |
|---|---|---|---|---|
| Política del SGSI / programa de seguridad | ISO 27001 §5.2 | Redactar y aprobar política | {{OWNER}} | {{Pendiente}} |
| Evaluación de riesgos de seguridad de la información | ISO 27001 §6.1.2 | Metodología + registro de riesgos InfoSec | {{OWNER}} | {{Pendiente}} |
| Statement of Applicability (SoA) | ISO 27001 §6.1.3 | Declarar aplicabilidad de cada control del Anexo A | {{OWNER}} | {{Pendiente}} |
| Auditoría interna del SGSI | ISO 27001 §9.2 | Programa de auditoría interna | {{OWNER}} | {{Pendiente}} |
| Revisión por la dirección | ISO 27001 §9.3 | Acta periódica | {{OWNER}} | {{Pendiente}} |
| Definición del sistema y límites (system description) | SOC 2 | Descripción del sistema para el auditor | {{OWNER}} | {{Pendiente}} |
| Selección del período de observación (Type II) | SOC 2 | Definir ventana de evidencia | {{OWNER}} | {{Pendiente}} |
| Acceso privilegiado y gestión de proveedores | ISO 27001 A.8.2 / A.5.19–A.5.22 | Política + registros | {{OWNER}} | {{Pendiente}} |
| Formación y concienciación en seguridad | ISO 27001 A.6.3 | Plan de formación | {{OWNER}} | {{Pendiente}} |

---

## 6. Cómo usar este documento

1. Completar cada celda `{{...}}` / "Pendiente de evidencia" con la referencia real (`archivo:línea` vía `COMPLIANCE_CHECKLIST.md`, o documento de proceso).
2. Para ISO 27001, derivar el **SoA** de la §3 marcando aplicabilidad y justificación de exclusiones.
3. Para SOC 2, decidir Type I (punto en el tiempo) vs Type II (período) y qué TSC opcionales se incluyen.
4. Revisar en cada release y ante cambio de superficie de seguridad.

---

## 7. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | {{OWNER}} | Readiness InfoSec inicial (ISO 27001:2022 Anexo A + SOC 2 TSC). |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md) · [Crosswalk](./REGULATORY_FRAMEWORK_CROSSWALK.md)
</content>
