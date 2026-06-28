# Plan de Respuesta a Incidentes

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla. Asigne roles reales, contactos y plazos antes de su activación. Cumple GDPR Art. 33/34 (notificación de brechas) y HIPAA §164.308(a)(6) (procedimientos de respuesta a incidentes de seguridad).

---

## 1. Propósito y alcance

Definir cómo **{{PROJECT_NAME}}** detecta, contiene, erradica y se recupera de incidentes de seguridad y violaciones de datos personales, incluyendo la notificación obligatoria a autoridades y titulares.

---

## 2. Roles y responsabilidades

| Rol | Responsable | Responsabilidad principal |
|---|---|---|
| Coordinador de incidente (IC) | <completar> | Dirige la respuesta de extremo a extremo |
| Responsable técnico | <completar> | Contención y erradicación técnica |
| DPO / Privacidad | <completar> | Evalúa obligación de notificar (GDPR/HIPAA) |
| Comunicación | <completar> | Comunicación interna/externa |
| Responsable legal | <completar> | Asesoría legal y regulatoria |
| Titular del producto | {{OWNER}} | Decisión final y rendición de cuentas |

---

## 3. Clasificación de severidad

| Severidad | Criterio | Ejemplo | Tiempo objetivo de respuesta |
|---|---|---|---|
| SEV-1 Crítico | Brecha confirmada de PHI/PII o caída total | Exfiltración de datos de salud | Inmediato (< 1 h) |
| SEV-2 Alto | Riesgo elevado, sin brecha confirmada | Vulnerabilidad crítica explotable | < 4 h |
| SEV-3 Medio | Impacto limitado y contenido | Intento de acceso bloqueado | < 24 h |
| SEV-4 Bajo | Sin impacto en datos | Anomalía menor | < 72 h |

---

## 4. Fases de respuesta

### 4.1 Detección e identificación
- Fuentes: alertas de monitoreo, SAST/DAST, reportes de usuarios, logs de auditoría.
- Registrar el incidente con ID, hora de detección, severidad provisional y evidencia. Ver `SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md` para la trazabilidad.

### 4.2 Contención
- Contención inmediata (aislar servicio/credencial) y a corto plazo.
- Rotar secretos y claves comprometidas en el gestor de secretos.
- Fail-closed: si hay duda, restringir acceso.

### 4.3 Erradicación
- Eliminar la causa raíz (parche, revocación, corrección de configuración).
- Verificar que no queden persistencias ni accesos residuales.

### 4.4 Recuperación
- Restaurar servicio desde estado seguro/backups verificados.
- Monitoreo reforzado durante el período de observación.

### 4.5 Post-mortem
- Análisis de causa raíz sin culpabilización (blameless), en plazo de <p. ej. 5 días hábiles>.
- Acciones correctivas/preventivas (CAPA) con responsable y fecha.
- Actualizar modelo de amenazas y controles si procede.

---

## 5. Notificación de brechas de datos

| Destinatario | Plazo | Base legal | Condición |
|---|---|---|---|
| Autoridad de control (p. ej. AEPD/EDPB) | **72 h** desde el conocimiento | GDPR Art. 33 | Brecha con riesgo para derechos y libertades |
| Titulares afectados | Sin dilación indebida | GDPR Art. 34 | Alto riesgo para el titular |
| Autoridades HIPAA / afectados | Sin demora, máx. 60 días | HIPAA §164.404–410 | Brecha de PHI no asegurada |

La evaluación de "riesgo" y la decisión de notificar recae en el DPO/Legal y queda documentada aunque se decida **no** notificar.

---

## 6. Registro y evidencia

Todo incidente se documenta en un registro central: cronología, decisiones, evidencias, notificaciones y CAPA. Conservación según `DATA_RETENTION_POLICY.md`.

---

## 7. Contactos de emergencia

| Contacto | Canal | Disponibilidad |
|---|---|---|
| <completar> | <completar> | <completar> |

---

## 8. Pruebas del plan

Este plan se ejercita (tabletop/simulacro) con periodicidad <completar> y se actualiza tras cada incidente real o ejercicio.

---

## 9. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
