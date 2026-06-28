# Inventario SOUP (Software of Unknown Provenance)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Inventario conforme a **IEC 62304 §8.1.2** (Identificación de SOUP) y **§5.3.3 / §7.1.3** (requisitos y riesgo de SOUP). SOUP = todo componente de software incorporado que no fue desarrollado bajo el proceso del ciclo de vida de {{PROJECT_NAME}} (librerías de terceros, dependencias del runtime, componentes de la plataforma cloud {{CLOUD_STACK}}, etc.). Toda fila `<...>` es un placeholder a completar y mantener vivo.

---

## 1. Alcance y criterios

| Campo | Valor |
|---|---|
| Stack frontend | {{FRONTEND_STACK}} |
| Stack backend | {{BACKEND_STACK}} |
| Stack base de datos | {{DB_STACK}} |
| Plataforma cloud | {{CLOUD_STACK}} |
| Criterio de inclusión | Todo componente de terceros que ejecute en producción o en la cadena de build/verificación cuyo fallo pueda afectar el comportamiento del dispositivo. |
| Fuente de versiones | `<lockfiles, manifiestos de dependencias; archivo:línea>` |
| Monitoreo de CVEs | `<herramienta SCA / fuente de avisos>` |

---

## 2. Inventario de componentes SOUP

| Componente | Versión | Capa | Propósito | Requisitos funcionales esperados | Requisitos de rendimiento esperados | CVEs conocidos monitoreados | Plan de mitigación |
|---|---|---|---|---|---|---|---|
| `<nombre>` | `<vX.Y.Z>` | `<frontend/backend/db/cloud/build>` | `<para qué se usa>` | `<comportamiento que se espera del componente>` | `<latencia/throughput/límites esperados>` | `<CVE-AAAA-NNNN o "ninguno conocido a la fecha">` | `<actualizar / aislar / control compensatorio / aceptar riesgo>` |
| `<nombre>` | `<vX.Y.Z>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| `<nombre>` | `<vX.Y.Z>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

> Conforme a §5.3.3, cada SOUP que sea parte de la arquitectura debe tener documentados sus **requisitos funcionales y de rendimiento** necesarios para su uso previsto. Conforme a §7.1.3, las características publicadas del SOUP relevantes para la seguridad deben evaluarse frente a los riesgos del sistema.

---

## 3. Evaluación de riesgo de SOUP (IEC 62304 §7.1.3)

| Componente | Riesgo identificado | Riesgo asociado (ISO 14971) | Severidad | Control aplicado | Estado |
|---|---|---|---|---|---|
| `<nombre>` | `<modo de fallo del SOUP relevante para seguridad>` | R`<nn>` | `<no grave/grave/muerte>` | `<control>` | `<abierto/cerrado>` |
| `<nombre>` | `<...>` | R`<nn>` | `<...>` | `<...>` | `<...>` |

---

## 4. Anomalías conocidas no resueltas (IEC 62304 §7.1.3)

Lista de anomalías publicadas del SOUP (bugs/avisos del proveedor) que permanecen abiertas y su evaluación de impacto en la seguridad.

| Componente | Anomalía / aviso | Fecha detección | Impacto en seguridad | Decisión |
|---|---|---|---|---|
| `<nombre>` | `<id/descr>` | YYYY-MM-DD | `<evaluación>` | `<mitigar / monitorear / aceptar>` |

---

## 5. Proceso de mantenimiento del inventario

| Aspecto | Definición |
|---|---|
| Frecuencia de revisión | `<periódica + ante cada cambio de dependencias>` |
| Disparadores de actualización | `<nuevo CVE publicado, cambio de versión, nueva dependencia añadida>` |
| Responsable | `<rol>` |
| Vínculo con gestión de cambios | Ver `SOFTWARE_MAINTENANCE_PLAN.md §5` (gestión de SOUP en el tiempo). |
| Vínculo con configuración | Ver `../03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md §8`. |

> Toda alta, baja o cambio de versión de un SOUP es un cambio controlado: dispara análisis de impacto, posible re-verificación y actualización de esta tabla y de la matriz de trazabilidad.

---

## 6. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | `<autor>` | `<descripción del cambio>` |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
