# Matriz de Gestión de Riesgo — ISO 14971

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Mantenida por `docs-dhf`. Cada control de riesgo se vincula a evidencia verificable (`ruta/test_archivo.py::test_nombre`). Un riesgo sin control implementado y verificado NO se considera mitigado.

## 1. Política de aceptabilidad del riesgo

| Severidad | Definición |
|---|---|
| Catastrófica | Muerte o daño irreversible. |
| Crítica | Daño serio reversible / intervención clínica requerida. |
| Seria | Daño moderado / retraso en cuidado. |
| Menor | Molestia / inconveniente sin daño. |

| Probabilidad | Definición |
|---|---|
| Frecuente | >1 por uso típico. |
| Probable | Ocasional en uso normal. |
| Ocasional | Esperable durante la vida del producto. |
| Remota | Improbable pero posible. |
| Improbable | Casi nunca. |

**Matriz de aceptabilidad** (severidad × probabilidad): definí qué celdas son ACEPTABLE / ALARP / INACEPTABLE según la política del proyecto. Todo riesgo INACEPTABLE requiere control antes de release.

## 2. Registro de riesgos

| ID | Peligro / situación peligrosa | Daño potencial | Sev. | Prob. | Riesgo inicial | Control de riesgo | Evidencia (`ruta/test_archivo.py::test_nombre`) | Riesgo residual | Estado |
|---|---|---|---|---|---|---|---|---|---|
| R001 | <ej. el motor de riesgo falla y no detecta crisis> | <daño> | Crítica | Ocasional | INACEPTABLE | <fail-safe: degrada a fallback seguro> | `tests/<...>.py::test_<...>_failsafe` | ALARP | Abierto |
| R002 | <ej. otro usuario accede a PHI por escalada de identidad> | <daño> | Crítica | Remota | INACEPTABLE | JWT-only; user_id solo del token | `tests/test_hard_rules.py::test_identity_comes_from_token_not_from_body` | Aceptable | Verificado |
| R005 | <ej. la IA responde sin validador clínico> | <daño> | Seria | Ocasional | INACEPTABLE | validador + disclaimer + fallback | `tests/<...>.py::test_<...>_validator` | ALARP | Abierto |
| R-SEC-01 | <ej. fuga de PII en logs / tracebacks al cliente> | <daño> | Seria | Ocasional | INACEPTABLE | handler global de errores con mensaje empático, sin traceback; los handlers de validación registran solo campo y motivo (`app/main.py::_resumen_de_errores`), nunca el valor enviado (PHI) | `tests/test_hard_rules.py::test_internal_error_never_leaks_a_traceback`, `tests/test_hard_rules.py::test_validation_failure_does_not_log_the_submitted_text`, `tests/test_hard_rules.py::test_unhandled_validation_error_does_not_log_the_value` | Aceptable | Verificado |
| R-SEC-03 | <ej. exfiltración de PHI por copia o volcado del almacenamiento> | <daño> | Crítica | Remota | INACEPTABLE | cifrado en reposo AES-256-GCM, nonce aleatorio por registro (RFC-001) | `tests/test_hard_rules.py::test_encryption_roundtrip_and_nonce_uniqueness`, `tests/test_hard_rules.py::test_tampered_ciphertext_is_rejected` | Aceptable | Verificado |
| R-IA-01 | <ej. el algoritmo entrega datos fantasma sin dato real> | <daño> | Seria | Remota | INACEPTABLE | guard "sin dato": estado `unclassified` en vez de inventar | `tests/<...>.py::test_<...>_no_data` | ALARP | Abierto |

> Las filas `R002`, `R-SEC-01` y `R-SEC-03` citan controles que el kit **ya trae** (`app/core/security.py`, `app/main.py`); el resto son ejemplos a reemplazar. Los mismos IDs se usan en [`RISK_CONTROL_TRACEABILITY.md`](RISK_CONTROL_TRACEABILITY.md) y [`TRACEABILITY_MATRIX_SAMD.md`](TRACEABILITY_MATRIX_SAMD.md): si renombrás uno, renombralo en los tres.

## 3. Riesgos de seguridad como riesgos clínicos

Cuando un vector de seguridad también es un riesgo clínico (auth roto → exposición de PHI; audit silenciado → no se reconstruye una crisis; cifrado roto → exfiltración), se registra acá Y se cruza con el reporte de seguridad. Convención: `R-SEC-*`, `R-IA-*`, `R-NOTIF-*`.

## 4. Riesgo residual global

Declaración de aceptabilidad del riesgo residual global tras todos los controles, firmada por el responsable de gestión de riesgo. Se revisa en cada release y ante cada reporte de post-market surveillance.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
