# Matriz de Trazabilidad SaMD

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> **Regla más estricta del DHF.** Cada `REQ-XXX` apunta a (1) código citado por NOMBRE (`ruta/archivo.py::símbolo`) verificable HOY y (2) un test que existe HOY, citado igual (`ruta/test_archivo.py::test_nombre`). El número de línea no se usa: caduca con el siguiente commit; el nombre lo comprueba `scripts/check_doc_citations.py` en el CI. Frases vagas ("validado por X", "cubierto por la suite") sin path concreto NO son trazabilidad aceptable — el auditor externo las levanta primero. Mantenida por `docs-dhf`, que verifica path + test antes de escribir cada fila.

## Cadena de trazabilidad

```
Necesidad clínica  →  REQ (requisito)  →  Diseño (ruta/archivo.py::símbolo)  →  Verificación (test)  →  Riesgo (R-XXX-NN)
```

## Requisitos del sistema

| REQ | Descripción | Origen (necesidad/riesgo) | Implementación (`ruta/archivo.py::símbolo`) | Verificación (`tests/…::test`) | Estado |
|---|---|---|---|---|---|
| REQ-SEC-01 | Cifrado en reposo de PII/PHI (AES-256-GCM) | GDPR Art.32 / HIPAA | `app/core/encryption.py::encrypt`, `app/core/encryption.py::decrypt` | `tests/test_hard_rules.py::test_encryption_roundtrip_and_nonce_uniqueness`, `tests/test_hard_rules.py::test_tampered_ciphertext_is_rejected` | ✓ |
| REQ-SEC-02 | Identidad solo del token (JWT-only) | R-SEC / escalada | `app/core/security.py::get_current_user_id` | `tests/test_hard_rules.py::test_identity_comes_from_token_not_from_body` | ✓ |
| REQ-CLN-01 | <requisito clínico nuclear> | R001 | `app/services/<módulo>.py::<función>` | `tests/test_<...>.py::test_<...>` | <✓/pendiente> |
| REQ-UX-01 | Fail-safe empático sin tracebacks | ISO 14971 / §5.4 | `app/main.py::unhandled_exception_handler` | `tests/test_hard_rules.py::test_internal_error_never_leaks_a_traceback` | ✓ |

## Categorías de requisitos sugeridas

- **REQ-CLN-*** — clínicos (algoritmos, escalas, motor de riesgo).
- **REQ-SEC-*** — seguridad (cifrado, auth, audit).
- **REQ-UX-*** — usabilidad clínica / accesibilidad (WCAG, neuro-UX).
- **REQ-SYNC-*** — sincronización offline-first / integridad de datos.
- **REQ-AI-*** — comportamiento de la IA (validador, fail-safe, sin claims no certificados).

## Verificación de integridad de la matriz

Antes de cerrar cualquier update:
```bash
# El archivo existe y el símbolo está definido (código Y test), citados por nombre:
python3 scripts/check_doc_citations.py
# El test además pasa HOY:
pytest -q "tests/test_hard_rules.py::test_encryption_roundtrip_and_nonce_uniqueness"
```

> El verificador solo mira las citas con `::`. Una cita vieja `archivo.py:123` se cuenta pero no se comprueba: al tocar una fila, pasala a la forma por nombre.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
