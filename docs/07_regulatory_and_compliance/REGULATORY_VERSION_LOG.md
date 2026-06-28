# Registro de Control de Versiones de Documentos Regulatorios

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Registro único de control de versiones de **todos** los documentos regulatorios del DHF. Implementa **ISO 13485:2016 §4.2.4 (control de documentos)** e **IEC 62304 §5.1.9 (control de configuración del software)**. Ningún documento regulatorio se considera vigente si su última versión no figura aquí. Las versiones obsoletas se retienen, no se borran (ISO 13485 §4.2.5, control de registros).

---

## 1. Propósito y alcance

Centraliza la identificación, aprobación, vigencia y obsolescencia de cada documento regulatorio. Garantiza que:

- Solo circulan **versiones aprobadas y vigentes**.
- Cada cambio queda **trazado** (qué, cuándo, quién, por qué).
- Las versiones **obsoletas** se identifican como tales y se retienen para auditoría.
- La numeración de versión es **coherente** con la del propio documento (cabecera `Versión: vX.Y`).

**Regla de numeración:** incremento mayor (`vX.0`) ante cambio estructural o de alcance; incremento menor (`vX.Y`) ante corrección o ampliación dentro del mismo alcance.

---

## 2. Estado de vigencia de documentos regulatorios

| ID | Documento | Versión vigente | Fecha aprobación | Aprobador | Próxima revisión | Estado |
|---|---|---|---|---|---|---|
| REG-01 | `COMPLIANCE_AND_SECURITY_MASTER.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | Vigente |
| REG-02 | `ISO_14971_RISK_MATRIX.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | Vigente |
| REG-03 | `RISK_CONTROL_TRACEABILITY.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | Vigente |
| REG-04 | `TRACEABILITY_MATRIX_SAMD.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | Vigente |
| REG-05 | `CRITICAL_MODULES_INVENTORY.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | Vigente |
| REG-06 | `ISO_13485_READINESS_PLAN.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | En revisión |
| REG-07 | `BREACH_NOTIFICATION_TEMPLATE.md` | vX.Y | YYYY-MM-DD | {{OWNER}} | YYYY-MM-DD | Vigente |

---

## 3. Historial de cambios (bitácora cronológica)

Una fila por cada cambio de versión de cualquier documento regulatorio. Append-only; no se reescriben filas pasadas.

| Fecha | Documento | De versión | A versión | Autor | Aprobador | Cambio (resumen) | Motivo / disparador |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | `<documento>.md` | — | v1.0 | {{OWNER}} | {{OWNER}} | Creación inicial. | <plan de desarrollo> |
| YYYY-MM-DD | `ISO_14971_RISK_MATRIX.md` | v1.0 | v1.1 | <autor> | {{OWNER}} | <alta de riesgo R0XX + control>. | <hallazgo de auditoría> |
| YYYY-MM-DD | `RISK_CONTROL_TRACEABILITY.md` | v1.0 | v1.1 | <autor> | {{OWNER}} | <cierre de lazo R0XX>. | <verificación de test> |

---

## 4. Documentos obsoletos / retirados

Versiones superadas que se retienen como registro (no se eliminan). ISO 13485 §4.2.4(f).

| Documento | Versión obsoleta | Fecha de retiro | Reemplazada por | Ubicación del archivo retenido |
|---|---|---|---|---|
| `<documento>.md` | vX.Y | YYYY-MM-DD | vX.Z | `<ruta/git tag/commit>` |

---

## 5. Distribución y acceso

| Documento | Audiencia | Medio de distribución | Control de acceso |
|---|---|---|---|
| <documento> | <equipo / auditor / autoridad> | <repositorio DHF / export PDF firmado> | <rol mínimo requerido> |

---

## 6. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
