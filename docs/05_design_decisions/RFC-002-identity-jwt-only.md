# RFC-002 — Identidad derivada solo del token (JWT-only)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** 2026-01-22

> RFC del SaMD Starter Kit. Ejemplo didáctico de una decisión de diseño de la capa de API/seguridad. Documenta cómo el backend determina "quién es el usuario" en cada request.

---

## Metadatos

| Campo | Valor |
|---|---|
| ID | RFC-002 |
| Estado | **Implementado** |
| Autor | Equipo de Backend |
| Revisores | Responsable de Seguridad, Responsable de Gestión de Riesgo (ISO 14971) |
| Fecha de propuesta | 2026-01-16 |
| Fecha de decisión | 2026-01-22 |
| Capa afectada | API / seguridad |
| Clase de seguridad del ítem | B |

---

## 1. Contexto

El backend {{BACKEND_STACK}} expone endpoints que leen y mutan PHI de un sujeto concreto (p. ej. `GET /records/me`, `POST /scales/{id}/answers`). Cada request autenticado llega con un token (JWT) emitido por el proveedor de identidad, que el backend verifica y decodifica en una dependencia de autenticación (`app/dependencies.py:NN`, `get_current_user`).

El riesgo aparece cuando un endpoint, por conveniencia, acepta **además** un identificador de usuario desde el cuerpo, el query string o un header (`?user_id=...`, `{"user_id": ...}`). En ese momento el cliente puede declarar ser cualquiera.

## 2. Problema

Si cualquier endpoint deriva la identidad del sujeto desde un dato controlado por el cliente, un usuario autenticado puede **sustituir el identificador por el de otro paciente y leer o mutar PHI ajena** (escalada horizontal / IDOR). Un solo endpoint que confíe en un `user_id` de entrada rompe el aislamiento de todos los pacientes.

## 3. Alternativas consideradas

| # | Alternativa | Pros | Contras | Riesgo SaMD |
|---|---|---|---|---|
| A | **Confiar en el `user_id` que envía el cliente** | Trivial de implementar; flexible para herramientas internas | El cliente declara su propia identidad → IDOR directo; imposible de auditar con confianza; un único endpoint descuidado compromete todo | INACEPTABLE: acceso a PHI ajena por manipulación trivial del request |
| B | **Identidad solo del token (JWT-only)** (elegida) | El sujeto sale exclusivamente del token verificado (firma + `aud` + `iss` + expiración); el cliente no puede declarar ser otro; superficie de IDOR cerrada por construcción | Requiere disciplina: ningún endpoint debe aceptar `user_id` de entrada; obliga a lookup de sujeto server-side | Aceptable: la identidad es no-falsificable sin la clave del emisor |
| C | **mTLS (identidad por certificado de cliente)** | Identidad criptográfica fuerte a nivel de transporte | Sobrecarga operativa enorme para clientes móviles/web públicos; gestión y rotación de certificados por usuario inviable a escala; no resuelve la autorización fina, solo autentica el canal | Desproporcionado para el modelo de cliente; no cierra IDOR por sí solo |
| D | No hacer nada / mezclar criterios por endpoint | — | Inconsistencia: algunos endpoints seguros, otros no; el auditor no puede garantizar la propiedad globalmente | INACEPTABLE |

## 4. Decisión

Se adopta la **Alternativa B: JWT-only**. La identidad del sujeto se deriva **exclusivamente** del token decodificado y verificado, nunca de body, query ni header.

Detalles de construcción:
- **Verificación del token** en `app/dependencies.py:NN` (`get_current_user`): firma válida contra la clave del emisor, `audience` esperado, `issuer` esperado y expiración no vencida. Cualquier fallo → 401 (sin filtrar el motivo técnico).
- **Regla dura**: ninguna firma de endpoint ni schema de entrada acepta `user_id`/`subject_id`. El identificador que cuenta es el del claim del token. Un test de contrato verifica que ningún router lo expone.
- **Autorización por recurso**: para acceder a un recurso, el `owner_id` del recurso debe coincidir con el sujeto del token; si no, 404/403 (preferentemente 404 para no filtrar existencia).
- **Multi-sujeto** (cuando aplica, p. ej. roles distintos): la resolución del tipo de sujeto también parte del token + lookup server-side, nunca de un campo declarado por el cliente.

## 5. Consecuencias

- **Positivas**: la superficie de IDOR por suplantación de identidad queda cerrada por construcción; los logs de auditoría reflejan al sujeto real; la propiedad es verificable globalmente con un test de contrato.
- **Negativas / costo**: cada endpoint que necesite operar sobre "otro" sujeto legítimamente (p. ej. un profesional sobre su paciente vinculado) debe pasar por una verificación de vínculo explícita server-side, no por un `user_id` de entrada.
- **Impacto en consumidores** (§5.6): cualquier handler que hoy lea `user_id` del request debe migrar al claim del token; búsqueda global de `user_id` en routers y schemas obligatoria.
- **Fail-safe**: token ausente/inválido/expirado → 401 con mensaje empático; recurso de otro sujeto → 404/403 sin traceback ni metadatos internos.
- **Deuda técnica generada**: `D-SEC-IDOR-CONTRACT-TEST-01` — test de contrato que falle si cualquier endpoint reintroduce `user_id` de entrada.

## 6. Trazabilidad

| Vínculo | Referencia |
|---|---|
| Requisito(s) | REQ-SEC-02 — Identidad solo del token (JWT-only) |
| Riesgo(s) ISO 14971 | R-SEC-02 (≅ R002) — Escalada horizontal: otro usuario accede a PHI ajena por suplantación de identidad (Sev. Crítica × Prob. Remota → INACEPTABLE → residual Aceptable) |
| Código | `app/dependencies.py:NN` (`get_current_user`); regla "sin `user_id` de entrada" aplicada en routers |
| Test(s) de verificación | `test_idor_rejects_foreign_user_id`, `test_endpoint_ignores_body_user_id`, `test_jwt_validates_audience_and_issuer` en `tests/test_identity_jwt_only.py` |
| Entrada en Master Map | v1.0 |

## 7. Historial

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-16 | Equipo de Backend | Propuesta inicial |
| v1.0 | 2026-01-22 | Equipo de Backend | Aceptada e implementada; auditoría de routers + test de contrato anti-IDOR |
