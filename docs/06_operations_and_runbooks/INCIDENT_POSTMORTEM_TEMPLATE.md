# Plantilla de Post-Mortem de Incidente (sin culpa)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Plantilla de análisis post-incidente **sin culpa (blameless)**. El objetivo es entender **qué** falló en el sistema y los procesos, no **quién** se equivocó. Todo incidente con impacto en usuarios, datos o disponibilidad genera un post-mortem. Si el incidente implicó datos personales/de salud, se cruza con `../07_regulatory_and_compliance/BREACH_NOTIFICATION_TEMPLATE.md`. Alimenta CAPA (ISO 13485 §8.5) y el análisis de impacto (IEC 62304 §5.6).

---

## 1. Resumen ejecutivo

| Campo | Valor |
|---|---|
| ID de incidente | <INC-XXXX> |
| Título | <descripción breve> |
| Severidad | SEV-1 (crítico) / SEV-2 (alto) / SEV-3 (medio) / SEV-4 (bajo) |
| Fecha del incidente | YYYY-MM-DD |
| Duración total | <HH:MM> (desde inicio hasta resolución) |
| Autor del post-mortem | <persona> |
| Estado | Borrador / En revisión / Cerrado |
| ¿Implicó datos personales/PHI? | Sí → activar notificación de brecha / No |

**Narrativa (2-3 frases, lenguaje claro):** <qué pasó, a quién afectó y cómo se resolvió>.

---

## 2. Impacto

| Dimensión | Detalle |
|---|---|
| Usuarios afectados | <N estimado / %> |
| Funcionalidad degradada | <qué dejó de funcionar> |
| Datos afectados | <ninguno / pérdida / exposición / corrupción> |
| Impacto clínico / de seguridad | <¿pudo contribuir a daño? referencia a riesgo R-XXX> |
| Impacto regulatorio | <¿activa brecha / reporte? referencia> |
| Detección | <cómo se detectó: alerta automática / reporte de usuario / monitoreo> |

---

## 3. Línea de tiempo (timeline)

> Horas en TZ explícita. Hechos objetivos, sin atribución de culpa.

| Hora (TZ) | Evento | Fuente |
|---|---|---|
| HH:MM | <cambio/deploy/condición que originó el incidente> | <commit / log> |
| HH:MM | <primer síntoma observable> | <métrica / alerta> |
| HH:MM | <detección y declaración del incidente> | <alerta / reporte> |
| HH:MM | <acciones de diagnóstico> | <log estructurado> |
| HH:MM | <mitigación aplicada> | <acción> |
| HH:MM | <resolución / servicio restaurado> | <verificación> |

---

## 4. Análisis de causa raíz

| Campo | Detalle |
|---|---|
| Causa raíz | <la condición de fondo, no el síntoma> |
| Causas contribuyentes | <factores secundarios> |
| Método de análisis | 5 Porqués / Ishikawa / Árbol de fallos |
| ¿Por qué no se detectó antes? | <gap de monitoreo/test> |
| ¿Por qué escaló a este impacto? | <gap de contención/fail-safe> |

**Cadena de 5 Porqués (ejemplo de estructura):**
1. ¿Por qué ocurrió el síntoma? → <...>
2. ¿Por qué ocurrió eso? → <...>
3. ¿Por qué? → <...>
4. ¿Por qué? → <...>
5. ¿Por qué? → <causa raíz sistémica>

---

## 5. Lo que funcionó / lo que no

| Funcionó bien | Falló o faltó |
|---|---|
| <ej. la alerta disparó a tiempo> | <ej. no había runbook para este caso> |
| <ej. el fail-safe degradó seguro> | <ej. el rollback fue manual y lento> |

---

## 6. Acciones correctivas y preventivas

| ID | Acción | Tipo | Prioridad | Responsable | Fecha objetivo | Estado | Verificación (`archivo:línea`/test) |
|---|---|---|---|---|---|---|---|
| AC-1 | <corrección inmediata del defecto> | Correctiva | Alta | <responsable> | YYYY-MM-DD | Abierta | `test_<...>` |
| AC-2 | <test de regresión que cubra el gap> | Preventiva | Alta | <responsable> | YYYY-MM-DD | Abierta | `<...>` |
| AC-3 | <alerta/monitoreo para detección temprana> | Preventiva | Media | <responsable> | YYYY-MM-DD | Abierta | `<...>` |
| AC-4 | <runbook / automatización de rollback> | Preventiva | Media | <responsable> | YYYY-MM-DD | Abierta | `<...>` |

---

## 7. Trazabilidad regulatoria

| Vínculo | Referencia |
|---|---|
| Riesgo(s) ISO 14971 afectados | R-XXX → `../07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md` |
| ¿Requiere nuevo control de riesgo? | Sí/No → `../07_regulatory_and_compliance/RISK_CONTROL_TRACEABILITY.md` |
| ¿Notificación de brecha activada? | Sí/No → `../07_regulatory_and_compliance/BREACH_NOTIFICATION_TEMPLATE.md` |
| Entrada CAPA (ISO 13485 §8.5) | <CAPA-XXX> |
| Deuda técnica registrada | `../08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md` |

---

## 8. Lecciones aprendidas

<Resumen narrativo de aprendizajes sistémicos. Foco en procesos y barreras, nunca en personas. Qué cambia en la forma de trabajar a partir de aquí.>

---

## 9. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
