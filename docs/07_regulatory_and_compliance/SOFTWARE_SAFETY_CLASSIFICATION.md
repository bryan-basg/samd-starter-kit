# Clasificación de Seguridad del Software

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Documento de clasificación conforme a **IEC 62304 §4.3** (Clasificación de seguridad del software). Justifica la clase global asignada, analiza las consecuencias del fallo del software, segrega los ítems de software por clase y enumera las medidas de control de riesgo externas al software. Toda fila `<...>` es un placeholder a completar.

---

## 1. Resumen de la clasificación

| Campo | Valor |
|---|---|
| Dispositivo software | {{PROJECT_NAME}} |
| Uso previsto | {{INTENDED_USE}} |
| Clase de seguridad global asignada | **{{SAMD_CLASS}}** |
| Norma de clasificación | IEC 62304 §4.3 (Ed. y enmienda aplicable) |
| Referencia de gestión de riesgo | ISO 14971 — matriz de riesgo `<path>` |
| Responsable de la clasificación | {{OWNER}} |

---

## 2. Criterios de clasificación IEC 62304 §4.3

| Clase | Definición normativa |
|---|---|
| **A** | El fallo o comportamiento inesperado del software **no puede contribuir** a una situación peligrosa, o la contribución no resulta en un riesgo inaceptable tras considerar las medidas de control de riesgo externas. |
| **B** | El fallo puede contribuir a una situación peligrosa que resulte en **daño no grave**. |
| **C** | El fallo puede contribuir a una situación peligrosa que resulte en **muerte o daño grave**. |

La clasificación se realiza **después** de considerar las medidas de control de riesgo externas al software (hardware, procedimientos, supervisión humana), conforme a §4.3.

---

## 3. Justificación de la Clase {{SAMD_CLASS}}

`<Justificación narrativa: describir la cadena de eventos peligrosa que el software podría originar o a la que podría contribuir, la severidad del daño potencial según la matriz ISO 14971, y por qué tras aplicar las medidas de control de riesgo externas la clase resultante es {{SAMD_CLASS}}. No inventar contenido clínico concreto; remitir al uso previsto {{INTENDED_USE}}.>`

| Pregunta de clasificación | Respuesta |
|---|---|
| ¿Puede el software contribuir a una situación peligrosa? | `<sí/no + explicación>` |
| Severidad del daño potencial (ISO 14971) | `<no grave / grave / muerte>` |
| ¿Existen medidas externas que reduzcan el riesgo antes de clasificar? | `<descripción>` |
| Clase resultante tras medidas externas | **{{SAMD_CLASS}}** |

---

## 4. Análisis de fallo del software (¿qué pasa si falla?)

| ID | Componente / función | Modo de fallo | Consecuencia potencial | Severidad | Medida de control de riesgo | Clase del ítem |
|---|---|---|---|---|---|---|
| F-`<01>` | `<componente>` | `<descripción del fallo>` | `<consecuencia>` | `<no grave/grave/muerte>` | `<interna SW / externa>` | `<A/B/C>` |
| F-`<02>` | `<componente>` | `<descripción del fallo>` | `<consecuencia>` | `<...>` | `<...>` | `<A/B/C>` |

> Cada modo de fallo relevante debe enlazarse con un riesgo de la matriz ISO 14971 (`R<nn>`) y con la prueba que verifica su control.

---

## 5. Segregación de ítems de software por clase (IEC 62304 §4.3 c) / §5.3)

La segregación permite asignar clases distintas a ítems de software dentro del mismo sistema, siempre que se justifique la **independencia** entre ítems (sin acoplamiento que propague el fallo de un ítem de clase superior a uno inferior).

| Ítem de software | Función | Clase asignada | Justificación de segregación / independencia |
|---|---|---|---|
| `<módulo / servicio>` | `<descripción>` | `<A/B/C>` | `<cómo se garantiza la independencia frente a ítems de clase superior>` |
| `<módulo / servicio>` | `<descripción>` | `<A/B/C>` | `<...>` |

**Mecanismos de segregación aplicados:** `<p. ej. separación de procesos, aislamiento de datos, validación en frontera, ausencia de dependencias compartidas; referenciar archivo:línea cuando exista>`.

> Si no se aplica segregación, todos los ítems heredan la clase global {{SAMD_CLASS}} y esta tabla lo declara explícitamente.

---

## 6. Medidas de control de riesgo externas al software

Medidas que **no** residen en el software y que reducen el riesgo antes de la clasificación (IEC 62304 §4.3, ISO 14971 §7).

| ID | Medida externa | Tipo | Riesgo mitigado (ISO 14971) | Evidencia / responsable |
|---|---|---|---|---|
| EXT-`<01>` | `<supervisión humana / procedimiento / hardware / etiquetado>` | `<procedimental/físico/informativo>` | R`<nn>` | `<responsable / documento>` |
| EXT-`<02>` | `<...>` | `<...>` | R`<nn>` | `<...>` |

> Tipos según ISO 14971: seguridad inherente por diseño, medidas de protección, e información de seguridad (etiquetado/instrucciones). Las medidas informativas son las de menor prioridad.

---

## 7. Conclusión de la clasificación

`<Declaración formal: el sistema {{PROJECT_NAME}} se clasifica globalmente como Clase {{SAMD_CLASS}} bajo IEC 62304 §4.3; los ítems segregados conservan las clases de la sección 5; las actividades del ciclo de vida aplicables se definen en ../03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md §4.>`

---

## 8. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | `<autor>` | `<descripción del cambio>` |

> Toda reclasificación (cambio de clase de un ítem o del sistema) exige re-evaluar las actividades obligatorias del SDP y registrar el impacto en la matriz de trazabilidad y en el plan de mantenimiento.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
