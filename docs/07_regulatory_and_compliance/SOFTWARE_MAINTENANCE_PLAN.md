# Plan de Mantenimiento del Software

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Plan conforme a **IEC 62304 §6** (Proceso de mantenimiento del software). Define cómo se reciben, analizan y resuelven los problemas tras la liberación, cómo se gestionan los cambios, cómo se re-verifica el software y cómo se mantiene el SOUP a lo largo del tiempo. Se integra con la resolución de problemas (§9) y la gestión de configuración (§8). Toda fila `<...>` es un placeholder a completar.

---

## 1. Propósito y alcance

| Campo | Valor |
|---|---|
| Dispositivo software | {{PROJECT_NAME}} |
| Uso previsto | {{INTENDED_USE}} |
| Clase de seguridad | {{SAMD_CLASS}} |
| Responsable de mantenimiento | {{OWNER}} |
| Plataforma de despliegue | {{CLOUD_STACK}} |
| Documento padre | `../03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md` |

El mantenimiento comienza tras la primera liberación (§5.8) y se extiende durante todo el ciclo de vida del producto en el mercado.

---

## 2. Establecimiento del plan de mantenimiento (IEC 62304 §6.1)

| Aspecto | Definición |
|---|---|
| Canales de recepción de retroalimentación | `<soporte, telemetría/observabilidad, reportes de usuarios/profesionales, avisos de SOUP>` |
| Registro de incidencias | `<sistema de tickets / issue tracker; archivo:línea o repositorio>` |
| Criterio para tratar una incidencia como problema | `<umbral que convierte feedback en problema formal>` |
| Vínculo con vigilancia post-comercialización | `<proceso ISO 13485 / regulatorio aplicable>` |

---

## 3. Análisis de problemas (IEC 62304 §6.2 / §9.1–§9.3)

Cada problema reportado pasa por un análisis estructurado **antes** de proponer cambios (verificar antes de arreglar).

| Paso | Actividad | Salida |
|---|---|---|
| 1 | Registro del problema (§9.1) | `<id, fecha YYYY-MM-DD, severidad, descripción reproducible>` |
| 2 | Evaluación de impacto en la seguridad (§6.2.1.1) | `<¿afecta a un riesgo ISO 14971? ¿cambia la clase del ítem?>` |
| 3 | Notificación a partes interesadas (§6.2.1.3) | `<a quién y cuándo se comunica si hay impacto en seguridad>` |
| 4 | Análisis de causa raíz | `<diagnóstico antes de codificar el arreglo>` |
| 5 | Análisis de impacto sobre consumidores del símbolo (§5.6) | `<lista de archivos/módulos afectados>` |

| ID problema | Fecha | Severidad | ¿Impacto en seguridad? | Riesgo asociado | Estado |
|---|---|---|---|---|---|
| PRB-`<01>` | YYYY-MM-DD | `<baja/media/alta/crítica>` | `<sí/no>` | R`<nn>` | `<abierto/en análisis/resuelto>` |

---

## 4. Gestión de cambios y modificaciones (IEC 62304 §6.3 / §8.2)

Toda modificación se trata como un cambio controlado bajo el proceso de gestión de configuración.

| Paso | Actividad | Cláusula |
|---|---|---|
| 1 | Solicitud de cambio aprobada | §6.3.1 / §8.2.1 |
| 2 | Uso del proceso de desarrollo para implementar el cambio | §6.3.1 |
| 3 | Re-evaluación de riesgo (¿el cambio introduce o modifica un riesgo?) | ISO 14971 |
| 4 | Implementación con trazabilidad al problema/solicitud | §8.2.2 |
| 5 | Aprobación de la liberación de la modificación | §6.3.2 |

| ID cambio | Problema origen | Tipo | Riesgo re-evaluado | Aprobado por | Fecha |
|---|---|---|---|---|---|
| CHG-`<01>` | PRB-`<01>` | `<corrección/mejora/SOUP>` | `<sí/no + ref>` | `<rol>` | YYYY-MM-DD |

---

## 5. Gestión de SOUP a lo largo del tiempo (IEC 62304 §6.1 / §7.1.3)

| Actividad | Definición |
|---|---|
| Monitoreo continuo de CVEs / avisos | `<herramienta SCA + cadencia>` |
| Disparadores de actualización de SOUP | `<nuevo CVE, fin de soporte, cambio funcional requerido>` |
| Evaluación de impacto de cada actualización | `<análisis de riesgo + alcance de re-verificación>` |
| Actualización del inventario | Toda alta/baja/cambio se refleja en `SOUP_INVENTORY.md`. |
| Anomalías no resueltas | Registrar en `SOUP_INVENTORY.md §4` con su evaluación de seguridad. |

> Un nuevo CVE relevante para la seguridad se trata como un problema (sección 3) y, si procede, como un cambio (sección 4).

---

## 6. Re-verificación y pruebas de regresión (IEC 62304 §6.3.1 / §5.7)

| Aspecto | Definición |
|---|---|
| Alcance de la re-verificación | `<determinado por el análisis de impacto del cambio; mínimo afecta a unidades, integración y sistema impactados>` |
| Suite de regresión | `<automatizada en CI; verde obligatorio antes de liberar>` |
| Criterio de aceptación | `<todos los tests vinculados pasan + números reportados>` |
| Fail-safe | `<verificar que el comportamiento degradado seguro se mantiene tras el cambio>` (ISO 14971) |
| Actualización de trazabilidad | `<la matriz Riesgo→Requisito→Diseño→Código→Prueba se actualiza en el mismo cambio>` |

> Ninguna modificación se libera sin re-verificación proporcional a su impacto. Un cambio que toca un ítem de Clase C exige el conjunto completo de actividades de su clase.

---

## 7. Liberación de versiones de mantenimiento (IEC 62304 §6.3.2 / §5.8)

| Aspecto | Definición |
|---|---|
| Numeración de versiones | `<esquema SemVer u otro; ver SDP §8>` |
| Registro de la liberación | `<release notes + lista de problemas resueltos + anomalías conocidas residuales>` |
| Aprobación | `<rol aprobador>` |
| Baseline de configuración | `<artefacto que congela la versión liberada>` |
| Comunicación a usuarios | `<si el cambio afecta a la seguridad o al uso previsto>` |

---

## 8. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | `<autor>` | `<descripción del cambio>` |
