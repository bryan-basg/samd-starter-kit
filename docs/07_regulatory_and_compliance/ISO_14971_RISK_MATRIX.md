# Matriz de Gestión de Riesgo — ISO 14971

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Mantenida por `docs-dhf`. Cada control de riesgo se vincula a evidencia verificable (`test:archivo:línea`). Un riesgo sin control implementado y verificado NO se considera mitigado.

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

| ID | Peligro / situación peligrosa | Daño potencial | Sev. | Prob. | Riesgo inicial | Control de riesgo | Evidencia (`test:archivo:línea`) | Riesgo residual | Estado |
|---|---|---|---|---|---|---|---|---|---|
| R001 | <ej. el motor de riesgo falla y no detecta crisis> | <daño> | Crítica | Ocasional | INACEPTABLE | <fail-safe: degrada a fallback seguro> | `test_...:app/services/...:NN` | ALARP | Abierto |
| R002 | <ej. otro usuario accede a PHI por escalada de identidad> | <daño> | Crítica | Remota | INACEPTABLE | JWT-only; user_id solo del token | `test_idor_...` | Aceptable | Abierto |
| R005 | <ej. la IA responde sin validador clínico> | <daño> | Seria | Ocasional | INACEPTABLE | validador + disclaimer + fallback | `...` | ALARP | Abierto |

## 3. Riesgos de seguridad como riesgos clínicos

Cuando un vector de seguridad también es un riesgo clínico (auth roto → exposición de PHI; audit silenciado → no se reconstruye una crisis; cifrado roto → exfiltración), se registra acá Y se cruza con el reporte de seguridad. Convención: `R-SEC-*`, `R-IA-*`, `R-NOTIF-*`.

## 4. Riesgo residual global

Declaración de aceptabilidad del riesgo residual global tras todos los controles, firmada por el responsable de gestión de riesgo. Se revisa en cada release y ante cada reporte de post-market surveillance.
