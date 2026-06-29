# Matriz de Gestión de Riesgo — ISO 14971

**Proyecto:** AuraLog · **Clase SaMD:** B · **Versión:** v1.0 · **Fecha:** 2026-06-28

> Mantenida por `docs-dhf`. Cada control de riesgo se vincula a evidencia verificable (`test:archivo:línea`). Un riesgo sin control implementado y verificado NO se considera mitigado.
>
> **Documento de EJEMPLO.** AuraLog es un dispositivo ficticio; los paths y tests son ilustrativos.

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

**Matriz de aceptabilidad** (severidad × probabilidad): para AuraLog (Clase B, sin daños catastróficos plausibles) se define:

| | Frecuente | Probable | Ocasional | Remota | Improbable |
|---|---|---|---|---|---|
| **Crítica** | INACEPTABLE | INACEPTABLE | INACEPTABLE | ALARP | ALARP |
| **Seria** | INACEPTABLE | INACEPTABLE | ALARP | ALARP | ACEPTABLE |
| **Menor** | ALARP | ALARP | ACEPTABLE | ACEPTABLE | ACEPTABLE |

Todo riesgo **INACEPTABLE** requiere control antes de release. Los riesgos **ALARP** se reducen tan bajo como sea razonablemente posible y se documentan; los **ACEPTABLE** se monitorean en post-market.

## 2. Registro de riesgos

| ID | Peligro / situación peligrosa | Daño potencial | Sev. | Prob. | Riesgo inicial | Control de riesgo | Evidencia (`test:archivo:línea`) | Riesgo residual | Estado |
|---|---|---|---|---|---|---|---|---|---|
| R001 | El motor de alertas falla o no evalúa un registro y la alerta "consultá a tu profesional" no se genera | Retraso de la consulta clínica | Seria | Ocasional | ALARP | Fail-safe en `alert_engine`: error registrado + reintento; red de respaldo `scheduled_evaluation` reevalúa registros pendientes por Cloud Scheduler | `test_alert_engine_failsafe_reevaluates:app/services/alert_engine.py:142` | ALARP | Abierto |
| R002 | Un umbral se configura fuera de rango clínico plausible → la alerta nunca dispara (o dispara siempre y el paciente la ignora) | Alerta perdida o ruido que enmascara una real | Seria | Remota | ALARP | `threshold_config` valida rango y rechaza valores inválidos; conserva el último umbral seguro y avisa al paciente que reconfigure con su profesional | `test_threshold_rejects_out_of_range:app/services/threshold_config.py:88` | Aceptable | Abierto |
| R003 | La alerta se genera pero el dispatcher no la entrega al dispositivo | El paciente no ve la alerta a tiempo → retraso | Seria | Remota | ALARP | `alert_dispatcher` con cola persistente + reintentos con backoff; alerta no entregada se reencola, no se descarta | `test_dispatcher_requeues_undelivered:app/services/alert_dispatcher.py:74` | Aceptable | Abierto |
| R004 | Un registro hecho sin conexión se pierde al fallar la sincronización → el síntoma nunca se evalúa | Síntoma no evaluado → posible alerta no generada | Seria | Remota | ALARP | `sync_service` con outbox idempotente; el registro no se borra del cliente hasta confirmar persistencia en el servidor | `test_sync_outbox_retains_until_confirmed:app/services/sync_service.py:210` | Aceptable | Abierto |
| R005 | Datos de salud (síntomas, notas) almacenados o registrados en claro | Exposición de PHI del paciente | Seria | Remota | ALARP | Cifrado en reposo AES-256-GCM vía `EncryptedString`; clave en Secret Manager; redacción de PHI en logs | `test_encrypted_string_roundtrip:app/models/types.py:33` | Aceptable | Abierto |
| R006 | Escalada de identidad: un usuario lee registros de otro paciente (IDOR) | Exposición de PHI de un tercero | Seria | Remota | ALARP | Identidad resuelta solo desde el token JWT; nunca se acepta `user_id` desde body/query; verificación de propiedad en cada acceso a registros | `test_idor_cannot_read_other_patient_logs:app/dependencies.py:57` | Aceptable | Abierto |
| R007 | Un fallo del backend expone un traceback / error técnico crudo al paciente | Confusión y ansiedad del paciente (posiblemente en crisis); pérdida de confianza; el paciente no entiende qué hacer | Menor | Ocasional | Aceptable | Handler global de errores: ningún traceback al cliente; mensaje empático en el idioma del usuario, sin jerga técnica, + código HTTP correcto | `test_error_handler_no_traceback_to_client:app/middleware/error_handler.py:40` | Aceptable | Abierto |

## 3. Riesgos de seguridad como riesgos clínicos

Cuando un vector de seguridad también es un riesgo clínico (auth roto → exposición de PHI; sync roto → síntoma no evaluado), se registra acá Y se cruza con el reporte de seguridad. Convención: `R-SEC-*`, `R-NOTIF-*`.

- **R005** y **R006** son riesgos de seguridad (cifrado, IDOR) tratados como riesgos clínicos por exponer PHI; se cruzan con el reporte de seguridad (`R-SEC-CIFRADO`, `R-SEC-IDOR`).
- **R003** (entrega de alerta) se cruza como `R-NOTIF-ENTREGA`: una notificación clínica no entregada es un fallo con impacto clínico, no solo técnico.

## 4. Riesgo residual global

Tras aplicar los controles internos (fail-safe del motor de alertas, red de respaldo por scheduler, validación de umbrales, outbox idempotente, cifrado en reposo, JWT-only) y las medidas externas (etiquetado del carácter informativo, canales clínicos independientes del paciente), el **riesgo residual global de AuraLog se considera ACEPTABLE** para un dispositivo Clase B: ningún riesgo residual supera severidad "Seria" con probabilidad mayor a "Remota", y ninguno alcanza daño irreversible. Se revisa en cada release y ante cada reporte de post-market surveillance.

Firmado por: Responsable de Gestión de Riesgo, AuraLog (ejemplo) — 2026-06-28.

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de AuraLog](./MASTER_MAP.md)
