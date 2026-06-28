# Documentación de Flujo de Datos

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla. Reemplace el diagrama y las tablas-placeholder por el flujo real del proyecto. Documento de referencia para el análisis de riesgo (ISO 14971) y el modelo de amenazas.

---

## 1. Propósito

Describir el recorrido de los datos (incluidos PII/PHI) a través de **{{PROJECT_NAME}}**: dónde se generan, transmiten, procesan, cifran y almacenan; las fronteras de confianza y los puntos de cifrado. Sustenta GDPR Art. 30 (registro de actividades de tratamiento) y el modelo de amenazas de `COMPLIANCE_AND_SECURITY_MASTER.md`.

---

## 2. Diagrama de flujo (alto nivel)

```
                 [ Frontera de confianza 1 ]
   ┌──────────┐    TLS 1.2+ (cifrado tránsito)   ┌──────────────────┐
   │ CLIENTE  │ ───────────────────────────────► │     BACKEND      │
   │ {{FRONTEND_STACK}}                           │  {{BACKEND_STACK}}
   │  - Sin secretos                              │  - Verifica JWT  │
   │  - Solo vars públicas                        │  - Identidad solo│
   └──────────┘ ◄─────────────────────────────── │    del token     │
        ▲          Errores SIN traceback          │  - Audit (mut.)  │
        │                                         └────────┬─────────┘
        │                                                  │
        │                            [ Frontera de confianza 2 ]
        │                              TLS + cifrado columna AES-256-GCM
        │                                                  ▼
        │                                         ┌──────────────────┐
        │                                         │  BASE DE DATOS   │
        │                                         │   {{DB_STACK}}   │
        │                                         │  - PII/PHI cifrada│
        │                                         │    en reposo     │
        │                                         └────────┬─────────┘
        │                                                  │
        │                            [ Frontera de confianza 3 ]
        │                              TLS + IAM mínimo privilegio
        │                                                  ▼
        │                                         ┌──────────────────┐
        └──────── notificaciones / assets ◄────── │  NUBE / SERVICIOS│
                                                  │  {{CLOUD_STACK}} │
                                                  │  - Gestor de     │
                                                  │    secretos      │
                                                  └──────────────────┘
```

---

## 3. Fronteras de confianza

| # | Frontera | Control de cruce | Riesgo principal |
|---|---|---|---|
| 1 | Cliente ↔ Backend | TLS 1.2+; verificación de JWT; nunca `user_id` desde body/query | Suplantación / IDOR |
| 2 | Backend ↔ Base de datos | TLS; credenciales en gestor de secretos; cifrado de columna AES-256-GCM | Fuga de PII/PHI en reposo |
| 3 | Backend ↔ Nube/Terceros | TLS; IAM mínimo privilegio; secretos por referencia | Exfiltración / acceso indebido |

---

## 4. Puntos de cifrado

| Punto | Mecanismo | Clave | Ubicación de la clave |
|---|---|---|---|
| Tránsito cliente↔backend | TLS 1.2+ | Certificado TLS | <completar> |
| Tránsito backend↔BD/nube | TLS | Certificado TLS | <completar> |
| Reposo (columnas PII/PHI) | AES-256-GCM | `ENCRYPTION_KEY` | Gestor de secretos (distinta de `SECRET_KEY`) |
| Backups | <completar> | <completar> | <completar> |

---

## 5. Inventario de datos PII/PHI

| Dato | Clasificación | En tránsito | En reposo | Cifrado en reposo |
|---|---|---|---|---|
| <completar> | PII | Sí | Sí | Sí (AES-256-GCM) |
| <completar> | PHI | Sí | Sí | Sí (AES-256-GCM) |
| <completar> | Técnico (sin PII) | Sí | Logs | No requerido |

---

## 6. Tratamiento en logs y auditoría

- **Audit middleware:** persiste solo mutaciones a BD, sin PII/PHI (identidad + acción + recurso + timestamp).
- **Logs técnicos:** estructurados, sin PII/PHI.
- Detalle en `COMPLIANCE_AND_SECURITY_MASTER.md` §5.3 y §5.5.

---

## 7. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
