# Documento Maestro de Seguridad y Cumplimiento

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla de referencia. Reemplace los marcadores `{{...}}` y las filas-placeholder por los valores reales del proyecto antes de declararlo aprobado. Este documento es la fuente única de verdad de seguridad/cumplimiento; cualquier control que no esté aquí no se considera implementado.

---

## 1. Propósito y alcance

Este documento consolida el modelo de amenazas, los controles de seguridad por capa y el mapeo a marcos regulatorios (OWASP, GDPR, HIPAA, ISO 27001) de **{{PROJECT_NAME}}**, un dispositivo software médico (SaMD) Clase **{{SAMD_CLASS}}**.

- **Uso previsto:** {{INTENDED_USE}}
- **Responsable (titular):** {{OWNER}}
- **Marco normativo aplicable:** IEC 62304 (ciclo de vida del software), ISO 14971 (gestión de riesgo), ISO 27001 (SGSI), GDPR (UE 2016/679), HIPAA (45 CFR Parts 160/164).

**Fuera de alcance:** seguridad física de las instalaciones del proveedor de nube (delegada al proveedor bajo modelo de responsabilidad compartida) y dispositivos del usuario final.

---

## 2. Stack tecnológico de referencia

| Capa | Tecnología | Notas de seguridad |
|---|---|---|
| Frontend | {{FRONTEND_STACK}} | Sin secretos embebidos; solo variables públicas `VITE_*`/equivalentes. |
| Backend | {{BACKEND_STACK}} | Identidad derivada solo del token; tipado estricto. |
| Base de datos | {{DB_STACK}} | Cifrado en reposo de columnas con PII/PHI. |
| Nube / Plataforma | {{CLOUD_STACK}} | Secretos en gestor de secretos; IAM de mínimo privilegio. |

---

## 3. Modelo de amenazas (resumen STRIDE)

| Amenaza (STRIDE) | Vector representativo | Control mitigante | Referencia |
|---|---|---|---|
| Spoofing (suplantación) | Reuso de token, `user_id` falsificado en body/query | Identidad **solo** del JWT verificado; nunca se acepta `user_id` desde body/query | §5.1 · `{{archivo:línea}}` |
| Tampering (manipulación) | Alteración de datos en tránsito o en reposo | TLS 1.2+ en tránsito; AES-256-GCM en reposo; audit de mutaciones | §5.2, §5.3 |
| Repudiation (repudio) | Usuario niega una acción de mutación | Audit middleware solo-mutaciones con identidad y timestamp | §5.3 |
| Information Disclosure (fuga) | Traceback con datos internos; PII en logs | Errores sin traceback al cliente; logs sin PII | §5.4, §5.5 |
| Denial of Service | Saturación de endpoints | Rate limiting, timeouts duros, límites de concurrencia | §5.6 |
| Elevation of Privilege | Acceso a recurso de otro sujeto (IDOR) | Autorización por sujeto del token en cada acceso a recurso | §5.1 |

**Activos críticos:** PII y PHI del titular de los datos, claves de cifrado, claves de firma de tokens, credenciales de servicio.

**Fronteras de confianza:** (1) cliente ↔ backend, (2) backend ↔ base de datos, (3) backend ↔ servicios de nube/terceros. Ver `DATA_FLOW_DOCUMENTATION.md`.

---

## 4. Principios rectores de seguridad

1. **Mínimo privilegio** en IAM, roles de BD y scopes de token.
2. **Defensa en profundidad**: ningún control único es suficiente.
3. **Fail-safe / fail-closed**: ante fallo de un control de seguridad, se deniega.
4. **Privacidad por diseño y por defecto** (GDPR Art. 25).
5. **Secretos fuera del repositorio**: nunca en `.env` versionado ni en código.

---

## 5. Controles por capa

### 5.1 Autenticación y autorización

- La identidad se deriva **exclusivamente** del token verificado (JWT-only). El backend **nunca** acepta `user_id` desde body, query o headers no verificados.
- Verificación de firma y expiración del token en cada petición autenticada.
- Autorización por recurso: cada acceso valida que el sujeto del token sea el propietario o tenga rol autorizado (anti-IDOR).
- Implementación: `{{archivo:línea}}` (dependencia de identidad), `{{archivo:línea}}` (verificación de propiedad).

### 5.2 Cifrado

- **En tránsito:** TLS 1.2+ obligatorio; HSTS habilitado.
- **En reposo:** columnas con PII/PHI cifradas con **AES-256-GCM**. La clave de cifrado (`ENCRYPTION_KEY`) reside en el gestor de secretos y es **distinta de la clave de firma de tokens** (`SECRET_KEY`).
- Rotación de claves documentada en `{{archivo:línea}}`.
- Cumple ISO 27001 A.10 (criptografía), HIPAA §164.312(a)(2)(iv) y §164.312(e)(2)(ii).

### 5.3 Auditoría (audit middleware)

- El middleware de auditoría persiste **solo mutaciones** (POST/PUT/DELETE/PATCH) a la base de datos.
- Las lecturas (GET) se registran en el sistema de logging centralizado, no en la BD.
- Los registros de auditoría **no contienen PII/PHI**: solo identidad del sujeto, acción, recurso, timestamp y resultado.
- Cumple IEC 62304 §5.7 (trazabilidad) y HIPAA §164.312(b) (controles de auditoría).

### 5.4 Manejo de errores

- El cliente **nunca** recibe tracebacks, consultas SQL, metadatos internos ni detalles de implementación.
- Respuestas de error: mensaje claro para el usuario + código HTTP correcto. Detalle técnico solo en logs internos.

### 5.5 Logging

- Logs estructurados, sin PII/PHI. Los identificadores sensibles se seudonimizan o se omiten.
- Retención de logs según `DATA_RETENTION_POLICY.md`.

### 5.6 Resiliencia de API

- Rate limiting, timeouts duros y límites de concurrencia.
- Degradación segura y predecible ante fallo de dependencias (ISO 14971 — fail-safe).

### 5.7 Gestión de secretos

- Todos los secretos en el gestor de secretos del proveedor de nube; inyectados por referencia en tiempo de ejecución.
- Prohibido versionar secretos. `.env.example` documenta variables **sin** valores reales.

---

## 6. SAST y pruebas de seguridad

| Herramienta | Objetivo | Frecuencia | Gate |
|---|---|---|---|
| Trivy | CVEs en dependencias e imágenes de contenedor | CI + nightly | Bloquea CVEs críticos sin excepción documentada |
| Semgrep | SAST código (backend + frontend) | CI | Bloquea hallazgos altos |
| Fuzz de OpenAPI | Fuzzing de contrato API | Nightly | Bloquea desviaciones de contrato/errores 5xx |
| DAST (opcional) | Escaneo dinámico | Nightly | Bloquea fallos confirmados |

---

## 7. Mapeo a marcos regulatorios

| Control interno | OWASP Top 10 | GDPR | HIPAA | ISO 27001 |
|---|---|---|---|---|
| Identidad JWT-only / anti-IDOR | A01 Broken Access Control | Art. 32 | §164.312(a) | A.9 |
| Cifrado en reposo AES-256-GCM | A02 Cryptographic Failures | Art. 32(1)(a) | §164.312(a)(2)(iv) | A.10 |
| Cifrado en tránsito TLS | A02 Cryptographic Failures | Art. 32 | §164.312(e) | A.13 |
| Errores sin traceback | A05 Security Misconfiguration | Art. 32 | §164.312 | A.14 |
| Audit middleware sin PII | A09 Logging Failures | Art. 30 | §164.312(b) | A.12 |
| Gestión de secretos | A05 Security Misconfiguration | Art. 32 | §164.312 | A.9 / A.10 |
| SAST + fuzz | A06 Vulnerable Components | Art. 32(1)(d) | §164.308(a)(8) | A.12 / A.14 |

---

## 8. Índice de reportes de seguridad

| ID | Documento | Última revisión | Estado |
|---|---|---|---|
| SEC-01 | `PRIVACY_POLICY.md` | YYYY-MM-DD | {{placeholder}} |
| SEC-02 | `DATA_RETENTION_POLICY.md` | YYYY-MM-DD | {{placeholder}} |
| SEC-03 | `DATA_FLOW_DOCUMENTATION.md` | YYYY-MM-DD | {{placeholder}} |
| SEC-04 | `INCIDENT_RESPONSE_PLAN.md` | YYYY-MM-DD | {{placeholder}} |
| SEC-05 | Reporte de pruebas SAST/DAST | YYYY-MM-DD | {{placeholder}} |

---

## 9. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |
