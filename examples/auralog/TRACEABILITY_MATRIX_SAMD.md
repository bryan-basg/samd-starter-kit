# Matriz de Trazabilidad SaMD

**Proyecto:** AuraLog · **Clase SaMD:** B · **Versión:** v1.0 · **Fecha:** 2026-06-28

> **Regla más estricta del DHF.** Cada `REQ-XXX` apunta a (1) `archivo:línea` verificable HOY y (2) nombre de test que existe HOY. Frases vagas ("validado por X", "cubierto por la suite") sin path concreto NO son trazabilidad aceptable — el auditor externo las levanta primero. Mantenida por `docs-dhf`, que verifica path + test antes de escribir cada fila.
>
> **Documento de EJEMPLO.** AuraLog es ficticio; los `archivo:línea` y tests son ilustrativos. En un proyecto real, cada fila se verifica con los comandos de la sección final.

## Cadena de trazabilidad

```
Necesidad clínica  →  REQ (requisito)  →  Diseño (archivo:línea)  →  Verificación (test)  →  Riesgo (R-XXX-NN)
```

## Requisitos del sistema

| REQ | Descripción | Origen (necesidad/riesgo) | Implementación (`archivo:línea`) | Verificación (nombre de test) | Estado |
|---|---|---|---|---|---|
| REQ-CLN-01 | El motor de alertas evalúa cada registro contra los umbrales configurados y genera la alerta informativa cuando se cruza un umbral; si la evaluación falla, no descarta el registro (fail-safe) | Necesidad clínica nuclear / R001 | `app/services/alert_engine.py:142` | `test_alert_engine_failsafe_reevaluates` | ✓ |
| REQ-CLN-02 | Los umbrales se validan contra un rango clínico plausible; un valor inválido conserva el último umbral seguro y avisa al paciente | R002 | `app/services/threshold_config.py:88` | `test_threshold_rejects_out_of_range` | ✓ |
| REQ-CLN-03 | Una alerta generada que no se entrega se reencola con backoff y nunca se descarta | R003 | `app/services/alert_dispatcher.py:74` | `test_dispatcher_requeues_undelivered` | ✓ |
| REQ-SYNC-01 | Todo registro de síntoma pasa por outbox idempotente; no se borra del cliente hasta confirmar persistencia en el servidor | Offline-first / R004 | `app/services/sync_service.py:210` | `test_sync_outbox_retains_until_confirmed` | ✓ |
| REQ-SEC-01 | Cifrado en reposo de PII/PHI (AES-256-GCM) y redacción de PHI en logs | GDPR Art.32 / HIPAA / R005 | `app/models/types.py:33` | `test_encrypted_string_roundtrip` | ✓ |
| REQ-SEC-02 | Identidad solo del token (JWT-only); nunca `user_id` desde body/query; verificación de propiedad por registro | R-SEC / escalada / R006 | `app/dependencies.py:57` | `test_idor_cannot_read_other_patient_logs` | ✓ |
| REQ-UX-01 | Fail-safe empático: ningún fallo del backend expone tracebacks al paciente; mensaje claro y sin jerga técnica | IEC 62304 §5.4 / R007 | `app/middleware/error_handler.py:40` | `test_error_handler_no_traceback_to_client` | ✓ |

## Categorías de requisitos sugeridas

- **REQ-CLN-*** — clínicos (motor de alertas, validación de umbrales, entrega de alertas).
- **REQ-SEC-*** — seguridad (cifrado, auth, audit).
- **REQ-UX-*** — usabilidad clínica / accesibilidad (WCAG, fail-safe empático).
- **REQ-SYNC-*** — sincronización offline-first / integridad de datos.
- **REQ-AI-*** — comportamiento de la IA (no aplica a AuraLog v1.0: no incorpora IA generativa; las alertas son deterministas por umbrales).

## Verificación de integridad de la matriz

Antes de cerrar cualquier update:
```bash
# El path existe:
git ls-files | grep app/services/alert_engine.py
# El test existe HOY:
pytest --collect-only -q | grep "test_alert_engine_failsafe_reevaluates"
```

> En este ejemplo ficticio los comandos no devolverán resultados reales: ilustran el procedimiento que `docs-dhf` ejecuta en un proyecto real antes de marcar una fila como `✓`.

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de AuraLog](./MASTER_MAP.md)
