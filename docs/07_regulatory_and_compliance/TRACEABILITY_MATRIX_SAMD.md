# Matriz de Trazabilidad SaMD

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> **Regla más estricta del DHF.** Cada `REQ-XXX` apunta a (1) `archivo:línea` verificable HOY y (2) nombre de test que existe HOY. Frases vagas ("validado por X", "cubierto por la suite") sin path concreto NO son trazabilidad aceptable — el auditor externo las levanta primero. Mantenida por `docs-dhf`, que verifica path + test antes de escribir cada fila.

## Cadena de trazabilidad

```
Necesidad clínica  →  REQ (requisito)  →  Diseño (archivo:línea)  →  Verificación (test)  →  Riesgo (R-XXX-NN)
```

## Requisitos del sistema

| REQ | Descripción | Origen (necesidad/riesgo) | Implementación (`archivo:línea`) | Verificación (nombre de test) | Estado |
|---|---|---|---|---|---|
| REQ-SEC-01 | Cifrado en reposo de PII/PHI (AES-256-GCM) | GDPR Art.32 / HIPAA | `app/models/types.py:NN` | `test_encrypted_string_*` | <✓/pendiente> |
| REQ-SEC-02 | Identidad solo del token (JWT-only) | R-SEC / escalada | `app/dependencies.py:NN` | `test_idor_*` | <✓/pendiente> |
| REQ-CLN-01 | <requisito clínico nuclear> | R001 | `app/services/...:NN` | `test_...` | <✓/pendiente> |
| REQ-UX-01 | Fail-safe empático sin tracebacks | ISO 14971 / §5.4 | `app/middleware/...:NN` | `test_error_handler_*` | <✓/pendiente> |

## Categorías de requisitos sugeridas

- **REQ-CLN-*** — clínicos (algoritmos, escalas, motor de riesgo).
- **REQ-SEC-*** — seguridad (cifrado, auth, audit).
- **REQ-UX-*** — usabilidad clínica / accesibilidad (WCAG, neuro-UX).
- **REQ-SYNC-*** — sincronización offline-first / integridad de datos.
- **REQ-AI-*** — comportamiento de la IA (validador, fail-safe, sin claims no certificados).

## Verificación de integridad de la matriz

Antes de cerrar cualquier update:
```bash
# El path existe:
git ls-files | grep <archivo>
# El test existe HOY:
<runner> --list | grep "<nombre_test>"
```
