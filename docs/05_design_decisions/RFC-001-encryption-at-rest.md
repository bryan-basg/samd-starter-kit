# RFC-001 — Cifrado en reposo de PII/PHI a nivel columna (AES-256-GCM)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** 2026-01-15

> RFC del SaMD Starter Kit. Ejemplo didáctico de una decisión de diseño de la capa de datos. Documenta cómo y por qué se cifra la información sensible del paciente antes de persistirla.

---

## Metadatos

| Campo | Valor |
|---|---|
| ID | RFC-001 |
| Estado | **Implementado** |
| Autor | Equipo de Plataforma |
| Revisores | Responsable de Seguridad, Responsable de Gestión de Riesgo (ISO 14971) |
| Fecha de propuesta | 2026-01-08 |
| Fecha de decisión | 2026-01-15 |
| Capa afectada | datos / seguridad |
| Clase de seguridad del ítem | B |

---

## 1. Contexto

El sistema persiste datos personales (PII) y datos de salud (PHI) en {{DB_STACK}}: identificadores de contacto, notas clínicas, respuestas a escalas autoaplicadas y metadatos de comportamiento. Bajo GDPR Art. 32 e HIPAA Security Rule (§164.312(a)(2)(iv)), estos datos exigen protección criptográfica en reposo proporcional al riesgo.

El estado inicial almacenaba los campos sensibles en texto plano en columnas estándar (`String`/`Text`). El cifrado en tránsito (TLS) ya estaba resuelto a nivel de {{CLOUD_STACK}}, pero **un volcado de la base, una réplica de backup mal protegida o un acceso indebido al almacenamiento subyacente exponían PHI directamente legible** (`app/models/types.py:11`, columnas declaradas como `String`).

## 2. Problema

Si un atacante o un tercero no autorizado obtiene una copia física de la base de datos (backup, snapshot, réplica, archivo de disco), debe encontrar la PII/PHI **ilegible sin la clave**, y esa clave no debe vivir en el mismo dominio de confianza que los datos ni reutilizar la clave de firma de sesión. Sin esto, una sola exfiltración del almacenamiento compromete a todos los pacientes a la vez.

## 3. Alternativas consideradas

| # | Alternativa | Pros | Contras | Riesgo SaMD |
|---|---|---|---|---|
| A | **SQLCipher / cifrado de la BD entera** | Cifra todo sin tocar el modelo; transparente para la app | Acopla a un motor concreto (rompe portabilidad del tier gestionado); cifra también datos no sensibles (costo CPU innecesario); la clave debe estar viva en cada conexión → granularidad nula; difícil rotar por columna; no aplica a backups lógicos (`pg_dump`) | Falsa sensación de protección: el dump lógico sale en claro |
| B | **Cifrado a nivel columna AES-256-GCM** (elegida) | Solo se cifra lo sensible; granularidad por campo; AEAD (confidencialidad + integridad/autenticación); clave gestionada fuera de la BD; portable entre motores; el dump lógico sale cifrado | Búsqueda exacta/`LIKE` sobre el campo cifrado se pierde (requiere índice ciego o columna hash aparte); costo de cifrado por fila en lectura/escritura | Aceptable: el campo viaja ilegible en cualquier export |
| C | **Cifrado en disco del proveedor** (encryption-at-rest gestionado del {{CLOUD_STACK}}) | Cero código; activado por defecto en el tier | Protege solo contra robo del disco físico; la app, los backups lógicos y cualquier credencial con acceso a la BD ven texto plano; no satisface "separación de la clave" | No mitiga exfiltración lógica ni acceso indebido con credencial válida |
| D | No hacer nada | — | PHI en claro ante cualquier copia de la BD | INACEPTABLE |

## 4. Decisión

Se adopta la **Alternativa B: cifrado a nivel columna con AES-256-GCM**, implementado como un `TypeDecorator` reutilizable de {{DB_STACK}} (`EncryptedString` en `app/models/types.py:11`) que cifra al escribir y descifra al leer de forma transparente para la capa de servicios.

Detalles de construcción:
- **Algoritmo:** AES-256-GCM (AEAD) vía librería criptográfica auditada (no implementación propia). Cada valor lleva su nonce de 96 bits único y su tag de autenticación; un tag inválido aborta la lectura (no se sirve dato corrupto).
- **Clave:** `ENCRYPTION_KEY` de 256 bits, provista por el gestor de secretos de {{CLOUD_STACK}} (Secret Manager / KMS). **Está prohibido reutilizar `SECRET_KEY`** (la clave de firma de sesión/JWT) ni hardcodearla. Dominios de confianza separados: comprometer la firma de sesión no descifra PHI, y viceversa.
- **Aplicación:** todas las columnas con PII/PHI declaran `EncryptedString` en lugar de `String`/`Text`.
- **Rotación:** la clave admite versionado (prefijo de versión en el ciphertext) para rotar sin descifrar toda la tabla de golpe.

## 5. Consecuencias

- **Positivas**: un volcado lógico o físico de la BD sale ilegible; integridad autenticada (GCM detecta manipulación); granularidad por campo; clave fuera del dominio de la BD.
- **Negativas / costo**: no se puede hacer `WHERE campo = ?` ni `LIKE` directo sobre columnas cifradas (requiere columna hash determinista aparte para lookups exactos); pequeño costo de CPU por fila; la clave perdida = datos irrecuperables (obliga a custodia y backup de clave disciplinados).
- **Impacto en consumidores** (§5.6): cualquier servicio que filtre o ordene por un campo recién cifrado debe migrar a un índice ciego o columna hash. Búsqueda global obligatoria de los consumidores del campo antes de cifrarlo.
- **Fail-safe**: un tag GCM inválido o una clave ausente **aborta la operación con error empático** (sin traceback al cliente) en vez de servir datos corruptos o en claro.
- **Deuda técnica generada**: `D-SEC-ENCRYPTED-LOOKUP-01` — definir estrategia de búsqueda ciega para los campos cifrados que hoy requieren filtrado.

## 6. Trazabilidad

| Vínculo | Referencia |
|---|---|
| Requisito(s) | REQ-SEC-01 — Cifrado en reposo de PII/PHI (AES-256-GCM) |
| Riesgo(s) ISO 14971 | R-SEC-01 — Exfiltración de PHI por copia/volcado del almacenamiento (Sev. Crítica × Prob. Remota → INACEPTABLE → residual Aceptable) |
| Código | `app/models/types.py:11` (`EncryptedString`); clave en gestor de secretos del {{CLOUD_STACK}} |
| Test(s) de verificación | `test_encrypted_string_roundtrip`, `test_encrypted_string_rejects_tampered_tag`, `test_encryption_key_not_equal_secret_key` en `tests/test_encryption_at_rest.py` |
| Entrada en Master Map | v1.0 |

## 7. Historial

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-08 | Equipo de Plataforma | Propuesta inicial |
| v1.0 | 2026-01-15 | Equipo de Plataforma | Aceptada e implementada; columnas PII/PHI migradas a `EncryptedString` |
