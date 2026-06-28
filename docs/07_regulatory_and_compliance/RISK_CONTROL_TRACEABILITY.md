# Trazabilidad de Controles de Riesgo

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Vista de una página que cierra el lazo **ISO 14971 §6-7 (control de riesgo) ↔ IEC 62304 §5.7 (verificación)**. Cada riesgo identificado debe rastrearse hasta un control implementado (`archivo:línea`), un requisito (REQ-XXX), un test que lo verifica y un riesgo residual evaluado. Una fila sin las cinco columnas pobladas NO se considera trazable y bloquea el release.

---

## 1. Propósito y alcance

Este documento es el **artefacto de cierre del lazo de control de riesgo**. Cruza, en una sola tabla auditable:

- **Riesgo (R-XXX):** entrada del registro de `ISO_14971_RISK_MATRIX.md`.
- **Control (`archivo:línea`):** medida de control de riesgo implementada en el código (ISO 14971 §6.2).
- **REQ:** requisito de software/sistema que materializa el control (`TRACEABILITY_MATRIX_SAMD.md`).
- **Test:** evidencia de verificación que demuestra que el control funciona (IEC 62304 §5.7).
- **Riesgo residual:** evaluación tras el control (ISO 14971 §6.4 / §7).

Toda modificación de un control clínico o de seguridad obliga a revisar la fila correspondiente en la **misma pasada** (análisis de impacto, IEC 62304 §5.6).

---

## 2. Convenciones

| Campo | Regla |
|---|---|
| ID de riesgo | `R-XXX` (clínico), `R-SEC-XX` (seguridad), `R-IA-XX` (IA/algoritmo). Debe existir en la matriz ISO 14971. |
| Control | `archivo:línea` verificable HOY; nunca una frase genérica sin path. |
| REQ | `REQ-XXX` existente en la matriz de trazabilidad. |
| Test | Nombre de test que existe HOY (`test_...`) + ruta. |
| Riesgo residual | ACEPTABLE / ALARP / INACEPTABLE (criterio de la política de aceptabilidad). |
| Estado del control | Implementado / En curso / Pendiente / Verificado. |

---

## 3. Matriz de trazabilidad de controles

| Riesgo (R-XXX) | Peligro / situación peligrosa | Control de riesgo (`archivo:línea`) | REQ | Test de verificación (`archivo:línea`) | Riesgo inicial | Riesgo residual | Estado |
|---|---|---|---|---|---|---|---|
| R001 | <ej. el motor clínico falla y no degrada de forma segura> | <fail-safe a fallback> `app/services/<...>.py:NN` | REQ-CLN-01 | `test_<...>_failsafe` `tests/<...>.py:NN` | INACEPTABLE | ALARP | Verificado |
| R002 | <ej. escalada de identidad expone datos de otro titular (IDOR)> | identidad solo del token `app/dependencies.py:NN` | REQ-SEC-01 | `test_idor_<...>` `tests/<...>.py:NN` | INACEPTABLE | Aceptable | Verificado |
| R005 | <ej. la IA responde sin validación de seguridad> | validador + disclaimer + fallback `app/services/<...>.py:NN` | REQ-AI-01 | `test_<...>_validator` `tests/<...>.py:NN` | INACEPTABLE | ALARP | Implementado |
| R-SEC-01 | <ej. fuga de PII en logs / tracebacks al cliente> | redacción de errores `app/core/<...>.py:NN` | REQ-SEC-02 | `test_<...>_no_traceback` `tests/<...>.py:NN` | INACEPTABLE | Aceptable | Verificado |
| R-IA-01 | <ej. el algoritmo entrega datos fantasma sin dato real> | guard "sin dato" `app/services/<...>.py:NN` | REQ-AI-02 | `test_<...>_no_data` `tests/<...>.py:NN` | INACEPTABLE | ALARP | En curso |

---

## 4. Controles sin verificación (gap activo)

Lista viva de controles declarados pero **aún sin test que los verifique**. Cada entrada bloquea el cierre de release hasta que su fila en la §3 quede `Verificado`.

| Riesgo | Control declarado (`archivo:línea`) | Test faltante | Responsable | Fecha objetivo |
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
