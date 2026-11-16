# Matriz de Gestión de Riesgo — ISO 14971

**Proyecto:** DosiFicta · **Clase SaMD:** C · **Versión:** v1.0 · **Fecha:** 2026-11-16

> Mantenida por `docs-dhf`. Cada control de riesgo se vincula a evidencia verificable (`ruta/test_archivo.py::test_nombre`). Un riesgo sin control implementado y verificado NO se considera mitigado.
>
> **Documento de EJEMPLO.** DosiFicta es un dispositivo ficticio; los paths, tests y rangos son ilustrativos.

## 1. Política de aceptabilidad del riesgo

| Severidad | Definición |
|---|---|
| Catastrófica | Muerte o daño irreversible. |
| Crítica | Daño serio reversible / intervención clínica requerida. |
| Seria | Daño moderado / retraso en cuidado. |
| Menor | Molestia / inconveniente sin daño. |

Probabilidades: Frecuente · Probable · Ocasional · Remota · Improbable (mismas definiciones que la [plantilla](../../docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md)).

**Matriz de aceptabilidad** — a diferencia de AuraLog, acá existe la fila **Catastrófica**, y para ella solo "Improbable" llega a ALARP:

| | Frecuente | Probable | Ocasional | Remota | Improbable |
|---|---|---|---|---|---|
| **Catastrófica** | INACEPTABLE | INACEPTABLE | INACEPTABLE | INACEPTABLE | ALARP |
| **Crítica** | INACEPTABLE | INACEPTABLE | INACEPTABLE | ALARP | ALARP |
| **Seria** | INACEPTABLE | INACEPTABLE | ALARP | ALARP | ACEPTABLE |
| **Menor** | ALARP | ALARP | ACEPTABLE | ACEPTABLE | ACEPTABLE |

**Regla de DosiFicta para riesgos catastróficos:** al menos **dos controles independientes** (si uno falla, el otro sigue en pie) y cada uno con su test. Un solo control, por bueno que sea, no alcanza.

## 2. Registro de riesgos

| ID | Peligro / situación peligrosa | Daño | Sev. | Prob. inicial | Riesgo inicial | Controles (unidad) | Evidencia (`ruta/test_archivo.py::test_nombre`) | Prob. residual | Residual |
|---|---|---|---|---|---|---|---|---|---|
| R001 | Dosis sugerida mayor a la necesaria por error de cálculo | Hipoglucemia grave | Catastrófica | Ocasional | INACEPTABLE | (1) Fórmula pura con tabla de casos firmada (UNIT-04); (2) tope máximo por dosis (UNIT-05) | `tests/dosing/test_bolus_calculator.py::test_matches_signed_reference_table`, `tests/dosing/test_safety_limits.py::test_never_suggests_above_max_bolus` | Improbable | ALARP |
| R002 | Glucosa ingresada en mmol/L interpretada como mg/dL (o al revés) | Hipo o hiperglucemia grave | Catastrófica | Probable | INACEPTABLE | (1) Unidad obligatoria en el request, sin valor por defecto (UNIT-01); (2) valor incompatible con la unidad declarada → rechazo (UNIT-01) | `tests/dosing/test_input_validator.py::test_missing_unit_is_rejected`, `tests/dosing/test_input_validator.py::test_value_implausible_for_unit_is_rejected` | Improbable | ALARP |
| R003 | Insulina activa de una dosis reciente no descontada ("apilamiento") | Hipoglucemia grave | Catastrófica | Ocasional | INACEPTABLE | (1) Descuento de insulina activa (UNIT-03); (2) sin historial de las últimas horas → **no sugiere** dosis (UNIT-03) | `tests/dosing/test_insulin_on_board.py::test_recent_dose_is_subtracted`, `tests/dosing/test_insulin_on_board.py::test_unknown_history_blocks_suggestion` | Improbable | ALARP |
| R004 | Parámetro del profesional fuera de rango plausible | Dosis erróneas repetidas | Catastrófica | Remota | INACEPTABLE | (1) Validación de rango al guardar (UNIT-02); (2) cambio de más de 50 % respecto del anterior → doble confirmación (UNIT-02) | `tests/dosing/test_parameter_validator.py::test_rejects_out_of_range`, `tests/dosing/test_parameter_validator.py::test_large_change_requires_second_confirmation` | Improbable | ALARP |
| R005 | Redondeo hacia arriba | Dosis algo mayor a la calculada | Crítica | Probable | INACEPTABLE | Redondeo siempre hacia abajo al incremento de la pluma (UNIT-06) | `tests/dosing/test_rounding.py::test_always_rounds_down` | Improbable | ALARP |
| R006 | Cálculo con una lectura de glucosa vieja | Corrección inadecuada | Crítica | Ocasional | INACEPTABLE | Lectura con más de 15 min → se pide una nueva (UNIT-01) | `tests/dosing/test_input_validator.py::test_stale_reading_is_rejected` | Remota | ALARP |
| R007 | Datos de salud expuestos (dosis, glucosas) | Exposición de PHI | Seria | Remota | ALARP | Cifrado en reposo + identidad solo del token (UNIT-07 y capa de auth) | `tests/test_dose_log.py::test_dose_fields_are_encrypted_at_rest` | Remota | ALARP |
| R008 | Error técnico crudo en pantalla durante el cálculo | El paciente no sabe si inyectarse o no | Seria | Ocasional | ALARP | Handler global: mensaje claro "no pudimos calcular, **no apliques una dosis basada en esta pantalla**" + qué hacer | `tests/test_error_handler.py::test_calculation_failure_shows_safe_message` | Remota | ALARP |
| R009 | Dosis confirmada registrada dos veces (o ninguna) | Insulina activa mal estimada → R003 | Catastrófica | Ocasional | INACEPTABLE | (1) Clave de idempotencia por confirmación (UNIT-07); (2) registro fallido → aviso visible y bloqueo de la próxima sugerencia hasta resolverlo (UNIT-07) | `tests/test_dose_log.py::test_same_confirmation_is_stored_once`, `tests/test_dose_log.py::test_failed_write_blocks_next_suggestion` | Improbable | ALARP |

> Las situaciones de "no sugiere dosis" (glucosa baja o dosis sobre el tope en UNIT-05, historial desconocido en R003, registro fallido en R009) **no dejan al paciente sin salida**: la pantalla explica qué hacer (medir de nuevo, seguir el plan escrito de su profesional, contactarlo). Fallar "en seguro" en Clase C significa **no dar un número dudoso**, nunca dejar a la persona sin instrucciones.

## 3. Riesgos de seguridad como riesgos clínicos

- **R007** se cruza con el reporte de seguridad (`R-SEC-CIFRADO`).
- **R009** es un riesgo de **integridad de datos** con consecuencia clínica directa: no se trata como un bug de base de datos sino como un riesgo catastrófico.

## 4. Riesgo residual global

Tras los controles internos (todos con dos barreras en los catastróficos) y las medidas externas (confirmación del paciente, formación), el **riesgo residual global se considera ACEPTABLE** con la condición de que **cada release** pase la verificación de [`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md) §4. Ningún riesgo catastrófico queda con probabilidad mayor a "Improbable". Se revisa en cada release y ante cada reporte de post-market.

Firmado por: Responsable de Gestión de Riesgo y Responsable Clínico, DosiFicta (ejemplo) — 2026-11-16.

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de DosiFicta](./MASTER_MAP.md)
