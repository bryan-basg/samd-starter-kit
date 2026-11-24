# Trazabilidad de Controles de Riesgo

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Vista de una página que cierra el lazo **ISO 14971 §6-7 (control de riesgo) ↔ IEC 62304 §5.7 (verificación)**. Cada riesgo identificado debe rastrearse hasta un control implementado (`ruta/archivo.py::símbolo`), un requisito (REQ-XXX), un test que lo verifica y un riesgo residual evaluado. Una fila sin las cinco columnas pobladas NO se considera trazable y bloquea el release.

---

## 1. Propósito y alcance

Este documento es el **artefacto de cierre del lazo de control de riesgo**. Cruza, en una sola tabla auditable:

- **Riesgo (R-XXX):** entrada del registro de `ISO_14971_RISK_MATRIX.md`.
- **Control (`ruta/archivo.py::símbolo`):** medida de control de riesgo implementada en el código (ISO 14971:2019 §7.1–§7.2).
- **REQ:** requisito de software/sistema que materializa el control (`TRACEABILITY_MATRIX_SAMD.md`).
- **Test:** evidencia de verificación que demuestra que el control funciona (IEC 62304 §5.7).
- **Riesgo residual:** evaluación tras el control (ISO 14971:2019 §7.3 / §8).

Toda modificación de un control clínico o de seguridad obliga a revisar la fila correspondiente en la **misma pasada** (análisis de impacto, IEC 62304 §7.4).

---

## 2. Convenciones

| Campo | Regla |
|---|---|
| ID de riesgo | `R-XXX` (clínico), `R-SEC-XX` (seguridad), `R-IA-XX` (IA/algoritmo). Debe existir en la matriz ISO 14971. |
| Control | `ruta/archivo.py::símbolo` verificable HOY; nunca una frase genérica sin path. |
| REQ | `REQ-XXX` existente en la matriz de trazabilidad. |
| Test | Nombre de test que existe HOY (`test_...`) + ruta. |
| Riesgo residual | ACEPTABLE / ALARP / INACEPTABLE (criterio de la política de aceptabilidad). |
| Estado del control | Implementado / En curso / Pendiente / Verificado. `Verificado` exige un test que existe HOY: un marcador `<...>` es `Pendiente`. En `ISO_14971_RISK_MATRIX` el RIESGO queda `Abierto` hasta que su control esté `Verificado`. |

---

## 3. Matriz de trazabilidad de controles

| Riesgo (R-XXX) | Peligro / situación peligrosa | Control de riesgo (`ruta/archivo.py::símbolo`) | REQ | Test de verificación (`ruta/test_archivo.py::test_nombre`) | Riesgo inicial | Riesgo residual | Estado |
|---|---|---|---|---|---|---|---|
| R001 | <ej. el motor clínico falla y no degrada de forma segura> | <fail-safe a fallback> `app/services/<...>.py::<símbolo>` | REQ-CLN-01 | `tests/<...>.py::test_<...>_failsafe` | INACEPTABLE | ALARP | Pendiente |
| R002 | <ej. escalada de identidad expone datos de otro titular (IDOR)> | identidad solo del token `app/core/security.py::get_current_user_id` | REQ-SEC-02 | `tests/test_hard_rules.py::test_identity_comes_from_token_not_from_body` | INACEPTABLE | ALARP | Verificado |
| R005 | <ej. la IA responde sin validación de seguridad> | validador + disclaimer + fallback `app/services/<...>.py::<símbolo>` | REQ-AI-01 | `tests/<...>.py::test_<...>_validator` | INACEPTABLE | ALARP | Pendiente |
| R-SEC-01 | <ej. fuga de PII en logs / tracebacks al cliente> | redacción de errores `app/main.py::unhandled_exception_handler` y `app/main.py::_resumen_de_errores` (los logs de validación llevan campo y motivo, no el valor); salida única hacia el servidor `app/main.py::AppSinDatosEnElLog` con `app/main.py::_diagnostico` (tipos y pila, nunca mensajes) | REQ-UX-01 | `tests/test_hard_rules.py::test_internal_error_never_leaks_a_traceback`, `tests/test_hard_rules.py::test_validation_failure_does_not_log_the_submitted_text`, `tests/test_hard_rules.py::test_unhandled_validation_error_does_not_log_the_value`, `tests/test_hard_rules.py::test_real_server_log_never_carries_the_value`, `tests/test_hard_rules.py::test_exit_gate_covers_outer_middleware_and_websockets` | INACEPTABLE | Aceptable | Verificado |
| R-SEC-03 | <ej. exfiltración de PHI por copia o volcado del almacenamiento> | cifrado en reposo `app/core/encryption.py::encrypt` | REQ-SEC-01 | `tests/test_hard_rules.py::test_encryption_roundtrip_and_nonce_uniqueness`, `tests/test_hard_rules.py::test_tampered_ciphertext_is_rejected` | INACEPTABLE | ALARP | Verificado |
| R-IA-01 | <ej. el algoritmo entrega datos fantasma sin dato real> | guard "sin dato" `app/services/<...>.py::<símbolo>` | REQ-AI-02 | `tests/<...>.py::test_<...>_no_data` | INACEPTABLE | ALARP | Pendiente |

---

## 4. Controles sin verificación (gap activo)

Lista viva de controles declarados pero **aún sin test que los verifique**. Cada entrada bloquea el cierre de release hasta que su fila en la §3 quede `Verificado`.

| Riesgo | Control declarado (`ruta/archivo.py::símbolo`) | Test faltante | Responsable | Fecha objetivo |
|---|---|---|---|---|
| R0XX | `<...>` | `<test pendiente>` | {{OWNER}} | YYYY-MM-DD |

---

## 5. Riesgos sin control implementado (gap activo)

| Riesgo | Peligro | Decisión | Justificación | Fecha objetivo |
|---|---|---|---|---|
| R0XX | `<...>` | Diferido / En diseño | `<...>` | YYYY-MM-DD |

---

## 6. Declaración de cierre del lazo

Cuando todas las filas de la §3 estén en estado `Verificado`, las §4 y §5 vacías, y el riesgo residual global aceptado en `ISO_14971_RISK_MATRIX.md §4`, el responsable de gestión de riesgo firma el cierre del lazo de control para esta versión.

| Versión cerrada | Fecha | Responsable | Riesgos trazados | Gaps abiertos |
|---|---|---|---|---|
| vX.Y | YYYY-MM-DD | {{OWNER}} | NN | NN |

---

## 7. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
