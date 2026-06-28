# Reporte de Simulacro de Respuesta a Incidentes

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Plantilla para registrar los **simulacros periódicos** de respuesta a incidentes (tabletop o en vivo). Verifica que el plan de respuesta funciona **antes** de un incidente real: que los roles están claros, los plazos regulatorios se cumplen y los runbooks existen. Cumple la prueba periódica de los planes de contingencia exigida por **HIPAA §164.308(a)(7)(ii)(D)** e **ISO 27001 A.5.24-A.5.30**. Recomendado al menos <DRILL_FREQUENCY>.

---

## 1. Identificación del simulacro

| Campo | Valor |
|---|---|
| ID del simulacro | <DRILL-XXXX> |
| Fecha de ejecución | YYYY-MM-DD |
| Tipo | Tabletop (mesa) / Funcional / Simulación en vivo |
| Duración | <HH:MM> |
| Facilitador | <persona> |
| Alcance | <sistemas/procesos cubiertos> |
| Plan evaluado | `INCIDENT_RESPONSE_PLAN.md` vX.Y |
| Anunciado / sorpresa | Anunciado / No anunciado |

---

## 2. Escenario simulado

| Campo | Detalle |
|---|---|
| Título del escenario | <ej. exfiltración de datos por credencial comprometida> |
| Categoría | Seguridad / Disponibilidad / Integridad de datos / Fallo clínico |
| Severidad simulada | SEV-1 / SEV-2 / SEV-3 |
| Condiciones iniciales | <qué se le presenta al equipo> |
| Inyecciones (eventos durante el ejercicio) | <complicaciones añadidas para probar la respuesta> |
| ¿Involucra datos personales/PHI? | Sí (probar notificación de brecha) / No |

---

## 3. Participantes y roles

| Rol | Persona | ¿Presente? | Desempeño observado |
|---|---|---|---|
| Comandante de incidente | <persona> | Sí / No | <observación> |
| Responsable técnico | <persona> | Sí / No | <observación> |
| Comunicaciones | <persona> | Sí / No | <observación> |
| DPO / cumplimiento | <DPO> | Sí / No | <observación> |
| Observador / evaluador | <persona> | Sí / No | — |

---

## 4. Línea de tiempo del ejercicio

| Hora (TZ) | Evento del escenario / acción del equipo | ¿Esperado? | Comentario |
|---|---|---|---|
| HH:MM | Inicio del simulacro / detección simulada | — | — |
| HH:MM | <primera acción del equipo> | Sí / No | <...> |
| HH:MM | <inyección> | — | <...> |
| HH:MM | <decisión de escalado / notificación> | Sí / No | <...> |
| HH:MM | Cierre del simulacro | — | — |

---

## 5. Métricas medidas

| Métrica | Objetivo | Resultado | Cumple |
|---|---|---|---|
| Tiempo hasta detección (MTTD) | < <MTTD_TARGET> | <valor> | Sí / No |
| Tiempo hasta contención | < <MTTC_TARGET> | <valor> | Sí / No |
| Tiempo hasta decisión de notificar | < 72 h (GDPR Art. 33) | <valor> | Sí / No |
| Roles correctamente asumidos | 100% | <valor> | Sí / No |
| Runbook disponible y utilizable | Sí | Sí / No | Sí / No |

---

## 6. Hallazgos

| ID | Hallazgo | Tipo | Severidad | Evidencia |
|---|---|---|---|---|
| H-1 | <ej. no existía runbook para revocar tokens en masa> | Gap de proceso | Alta | <observación> |
| H-2 | <ej. ambigüedad sobre quién declara la brecha> | Gap de roles | Media | <observación> |
| H-3 | <ej. el plazo de 72 h no se conocía> | Gap de formación | Media | <observación> |

---

## 7. Acciones de mejora

| ID | Acción | Responsable | Fecha objetivo | Estado | Vínculo |
|---|---|---|---|---|---|
| AM-1 | <crear/actualizar runbook> | <responsable> | YYYY-MM-DD | Abierta | `INCIDENT_RESPONSE_PLAN.md` |
| AM-2 | <aclarar matriz de roles> | <responsable> | YYYY-MM-DD | Abierta | <...> |
| AM-3 | <formación sobre plazos regulatorios> | <DPO> | YYYY-MM-DD | Abierta | `../07_regulatory_and_compliance/BREACH_NOTIFICATION_TEMPLATE.md` |

---

## 8. Evaluación global y próximo simulacro

| Campo | Valor |
|---|---|
| Veredicto general | Satisfactorio / Satisfactorio con reservas / Insatisfactorio |
| ¿Requiere re-simulacro? | Sí / No |
| Próximo simulacro programado | YYYY-MM-DD |
| Plan actualizado tras el ejercicio | Sí (vX.Y) / No |

---

## 9. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
