# Procedimiento de Resolución de Problemas del Software

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla conforme a IEC 62304 §9 (proceso de resolución de problemas del software). Ajuste clasificaciones, responsables y umbrales a la realidad del proyecto.

---

## 1. Propósito y alcance

Establecer cómo **{{PROJECT_NAME}}** registra, analiza, clasifica, corrige, verifica y comunica los problemas del software detectados en cualquier fase del ciclo de vida, conforme a IEC 62304 §9.

---

## 2. Registro del problema (IEC 62304 §9.1)

Todo problema se documenta en un registro central con, como mínimo:

| Campo | Descripción |
|---|---|
| ID | Identificador único del problema |
| Fecha de detección | YYYY-MM-DD |
| Origen | Usuario / test / monitoreo / auditoría / SAST |
| Descripción | Qué se observó (sin PII en el registro) |
| Severidad provisional | Ver §4 |
| Componente afectado | `archivo:línea` / módulo |
| Estado | Abierto / En análisis / Corregido / Verificado / Cerrado |

---

## 3. Análisis de impacto (IEC 62304 §9.2 y §5.6)

Para cada problema se evalúa:

1. **¿Afecta seguridad o eficacia clínica?** Si sí, se conecta con el archivo de gestión de riesgo (ISO 14971) y se reevalúa el riesgo.
2. **Consumidores afectados:** búsqueda global de todos los usos del símbolo/esquema implicado antes de corregir.
3. **Otros productos/versiones afectados** por la misma causa raíz.
4. Resultado del análisis documentado en el registro del problema.

---

## 4. Clasificación

| Severidad | Criterio | Acción |
|---|---|---|
| Crítica | Riesgo para el paciente / brecha de seguridad / pérdida de datos | Corrección inmediata + evaluación de campo |
| Alta | Funcionalidad clínica degradada sin daño directo | Corrección priorizada |
| Media | Defecto funcional acotado | Planificada |
| Baja | Cosmético / menor | Backlog |

Los problemas con impacto en seguridad se enlazan con `INCIDENT_RESPONSE_PLAN.md` cuando corresponda.

---

## 5. Corrección (IEC 62304 §9.3)

- La corrección se realiza bajo gestión de cambios (ver `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md` §5): rama, PR, revisión por pares.
- El cambio referencia el ID del problema.
- Se deja el código más limpio (mantenibilidad, §5.7).

---

## 6. Verificación (IEC 62304 §9.4 y §5.7)

- No se declara un problema "resuelto" sin ejecutar los tests vinculados y reportar los números.
- Se añade/actualiza un test que reproduce el problema (regresión) cuando es posible.
- Verificación adversarial para hallazgos de seguridad/clínicos críticos: refutación por un revisor independiente antes de cerrar.

---

## 7. Comunicación (IEC 62304 §9.5)

| Parte interesada | Qué se comunica | Cuándo |
|---|---|---|
| Equipo de desarrollo | Estado y resolución | Continuo |
| Titular del producto ({{OWNER}}) | Problemas críticos/altos | Inmediato |
| Usuarios / clientes | Avisos de seguridad relevantes | Según severidad |
| Autoridad regulatoria | Cuando aplique notificación | Según marco legal |

---

## 8. Uso de la información de tendencias (IEC 62304 §9.6)

Análisis periódico de los problemas registrados para detectar patrones, causas raíz recurrentes y oportunidades de mejora preventiva (CAPA). Resultados alimentan el modelo de amenazas y la matriz de riesgo.

---

## 9. Cierre

Un problema se cierra solo cuando: corrección integrada en baseline, verificación pasada y reportada, trazabilidad documental actualizada y comunicación realizada.

---

## 10. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
