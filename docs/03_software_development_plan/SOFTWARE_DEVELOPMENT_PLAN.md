# Plan de Desarrollo de Software (SDP)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Documento maestro del proceso de desarrollo conforme a **IEC 62304 §5.1** (Planificación del desarrollo de software). Define el ciclo de vida, las actividades exigidas por la clase de seguridad, los roles, los entregables, las herramientas y los mecanismos de trazabilidad y verificación. Toda fila marcada con `<...>`, `YYYY-MM-DD` o `archivo:línea` es un placeholder que el equipo debe completar.

---

## 1. Propósito y alcance

| Campo | Valor |
|---|---|
| Nombre del dispositivo software | {{PROJECT_NAME}} |
| Uso previsto (intended use) | {{INTENDED_USE}} |
| Clase de seguridad IEC 62304 | {{SAMD_CLASS}} |
| Responsable / fabricante legal | {{OWNER}} |
| Stack frontend | {{FRONTEND_STACK}} |
| Stack backend | {{BACKEND_STACK}} |
| Stack de base de datos | {{DB_STACK}} |
| Plataforma cloud / infraestructura | {{CLOUD_STACK}} |
| Idioma de comunicación interna | {{CHAT_LANG}} |

Este plan cubre el desarrollo completo del software, desde la definición de requisitos hasta la liberación y el traspaso al proceso de mantenimiento (ver `SOFTWARE_MAINTENANCE_PLAN.md`). Excluye los procesos de gestión de riesgo (ver `../07_regulatory_and_compliance/`) y de gestión de calidad ISO 13485, referenciados donde corresponde.

---

## 2. Modelo de ciclo de vida (IEC 62304 §5.1.1)

| Atributo | Definición |
|---|---|
| Modelo seleccionado | `<iterativo / incremental / en V / híbrido>` |
| Justificación | `<por qué este modelo se ajusta al producto y a la Clase {{SAMD_CLASS}}>` |
| Fases | `<Requisitos → Diseño arquitectónico → Diseño detallado → Implementación → Integración → Verificación de sistema → Liberación>` |
| Criterios de entrada/salida por fase | `<documentar gate de cada transición>` |
| Hitos (milestones) | `<lista de hitos con fecha YYYY-MM-DD>` |

Cada iteración produce un incremento verificable. Ninguna fase se declara cerrada sin cumplir su criterio de salida documentado.

---

## 3. Clasificación de seguridad del software (IEC 62304 §4.3)

La clasificación global asignada es **Clase {{SAMD_CLASS}}**. La justificación completa, el análisis de fallo y la segregación de ítems de software por clase residen en `../07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md`.

| Clase | Definición IEC 62304 | Aplica a |
|---|---|---|
| A | El fallo no puede causar daño ni deterioro de la salud | `<ítems clase A>` |
| B | El fallo puede causar un daño no grave | `<ítems clase B>` |
| C | El fallo puede causar muerte o daño grave | `<ítems clase C>` |

> La clase determina el conjunto de actividades obligatorias (sección 4). Un ítem hereda la clase más alta de los riesgos que mitiga, salvo segregación justificada y documentada.

---

## 4. Actividades por clase de seguridad (IEC 62304 §5–§9)

Leyenda: ● obligatorio · ○ no exigido por la norma (puede adoptarse voluntariamente).

| Actividad | Cláusula | Clase A | Clase B | Clase C |
|---|---|:---:|:---:|:---:|
| Plan de desarrollo de software | §5.1 | ● | ● | ● |
| Requisitos de software | §5.2 | ● | ● | ● |
| Diseño arquitectónico | §5.3 | ○ | ● | ● |
| Diseño detallado de unidades | §5.4 | ○ | ○ | ● |
| Implementación y verificación de unidades | §5.5 | ● | ● | ● |
| Verificación de integración | §5.6 | ○ | ● | ● |
| Pruebas del sistema de software | §5.7 | ○ | ● | ● |
| Liberación del software | §5.8 | ● | ● | ● |
| Gestión de configuración | §8 | ● | ● | ● |
| Resolución de problemas | §9 | ● | ● | ● |
| Gestión de riesgo del software | ISO 14971 + §7 | ● | ● | ● |

**Decisión para {{PROJECT_NAME}} (Clase {{SAMD_CLASS}}):** `<enumerar las actividades efectivamente aplicadas y justificar cualquier exclusión / tailoring>`.

---

## 5. Roles y responsabilidades

| Rol | Responsabilidad principal | Asignado a | Suplente |
|---|---|---|---|
| Responsable regulatorio (RA/QA) | Conformidad IEC 62304 / ISO 14971 / ISO 13485 | `<nombre>` | `<nombre>` |
| Arquitecto de software | Diseño arquitectónico y segregación de ítems | `<nombre>` | `<nombre>` |
| Desarrollador(es) | Implementación y verificación de unidades | `<nombre>` | `<nombre>` |
| Ingeniero de verificación / QA | Pruebas de integración y de sistema | `<nombre>` | `<nombre>` |
| Gestor de configuración | Control de versiones y baselines | `<nombre>` | `<nombre>` |
| Gestor de riesgo | Mantenimiento de la matriz ISO 14971 | `<nombre>` | `<nombre>` |
| Aprobador de liberación | Autoriza la liberación (§5.8) | `<nombre>` | `<nombre>` |

> Una misma persona puede asumir varios roles si la organización lo documenta y no se viola la independencia exigida para la verificación.

---

## 6. Entregables del ciclo de vida

| Entregable | Cláusula | Ubicación / artefacto | Estado |
|---|---|---|---|
| Plan de desarrollo de software | §5.1 | este documento | `<borrador/aprobado>` |
| Especificación de requisitos de software (SRS) | §5.2 | `<path>` | `<estado>` |
| Documento de diseño arquitectónico | §5.3 | `<path>` | `<estado>` |
| Documento de diseño detallado | §5.4 | `<path>` | `<estado>` |
| Código fuente y unidades verificadas | §5.5 | `<repo>` | `<estado>` |
| Informe de verificación de integración | §5.6 | `<path>` | `<estado>` |
| Informe de pruebas del sistema | §5.7 | `<path>` | `<estado>` |
| Registro de liberación / release notes | §5.8 | `<path>` | `<estado>` |
| Inventario SOUP | §8.1.2 | `SOUP_INVENTORY.md` | `<estado>` |
| Matriz de trazabilidad | §5.1.1 | `<path>` | `<estado>` |
| Matriz de riesgo ISO 14971 | ISO 14971 | `<path>` | `<estado>` |

---

## 7. Herramientas de desarrollo, verificación y configuración

| Categoría | Herramienta | Versión | Propósito | Validación de la herramienta |
|---|---|---|---|---|
| Control de versiones | `<herramienta>` | `<vX.Y>` | Gestión de configuración (§8) | `<requerida sí/no>` |
| IDE / editor | `<herramienta>` | `<vX.Y>` | Implementación | `<n/a>` |
| Compilador / runtime | `<herramienta>` | `<vX.Y>` | Build | `<validación>` |
| Framework de pruebas (frontend) | `<herramienta>` | `<vX.Y>` | Verificación §5.5–§5.7 | `<validación>` |
| Framework de pruebas (backend) | `<herramienta>` | `<vX.Y>` | Verificación §5.5–§5.7 | `<validación>` |
| Análisis estático / linter | `<herramienta>` | `<vX.Y>` | Calidad de código | `<validación>` |
| Pruebas de mutación | `<herramienta>` | `<vX.Y>` | Rigor de la suite | `<validación>` |
| Escáner de vulnerabilidades / SCA | `<herramienta>` | `<vX.Y>` | Monitoreo SOUP / CVEs | `<validación>` |
| CI/CD | `<herramienta>` | `<vX.Y>` | Build + verificación automatizada | `<validación>` |

> Conforme a IEC 62304 §5.1.4, toda herramienta cuyo fallo pueda introducir un defecto no detectado debe evaluarse y, si procede, validarse. Documentar la decisión en la columna correspondiente.

---

## 8. Gestión de configuración del software (IEC 62304 §8)

| Aspecto | Definición |
|---|---|
| Identificación de configuración (§8.1) | `<esquema de versionado, p. ej. SemVer; convención de tags/baselines>` |
| Ítems de configuración controlados | `<código, documentos, SOUP, scripts de build, infraestructura como código>` |
| Control de cambios (§8.2) | `<flujo de revisión y aprobación; ver SOFTWARE_MAINTENANCE_PLAN.md>` |
| Registro de estado de configuración (§8.3) | `<dónde se registra el historial; trazabilidad de cada baseline>` |
| Gestión de SOUP | `<referencia a SOUP_INVENTORY.md>` |
| Baseline de liberación | `<artefacto que congela la versión liberada>` |

---

## 9. Verificación (IEC 62304 §5.5.5, §5.6, §5.7)

| Nivel | Método | Criterio de aceptación | Evidencia |
|---|---|---|---|
| Unidad (§5.5) | `<pruebas unitarias / revisión>` | `<umbral cobertura / criterios>` | `<informe>` |
| Integración (§5.6) | `<pruebas de integración>` | `<criterios de aceptación>` | `<informe>` |
| Sistema (§5.7) | `<pruebas de sistema / aceptación>` | `<requisitos cubiertos>` | `<informe>` |
| Regresión | `<suite automatizada en CI>` | `<verde obligatorio antes de merge>` | `<run de CI>` |

**Reglas duras de verificación:**
- Ninguna tarea se declara completa sin ejecutar las pruebas vinculadas y reportar resultados numéricos.
- Las pruebas degradan de forma segura ante fallo de dependencias externas (fail-safe explícito, ISO 14971).
- Antes de modificar un símbolo compartido, ejecutar análisis de impacto sobre todos sus consumidores (§5.6).

---

## 10. Trazabilidad (IEC 62304 §5.1.1)

Se mantiene una matriz de trazabilidad bidireccional que enlaza:

`Riesgo (ISO 14971) → Requisito → Diseño → Código (archivo:línea) → Prueba (nombre de test que existe HOY)`

| ID Requisito | Riesgo asociado | Diseño | Código | Prueba | Estado |
|---|---|---|---|---|---|
| REQ-`<nnn>` | R`<nn>` | `<ref diseño>` | `archivo:línea` | `<nombre_test>` | `<verificado/pendiente>` |

> Cada entrada debe apuntar a un `archivo:línea` verificable y a un test existente. Frases genéricas sin path no constituyen trazabilidad aceptable.

---

## 11. Control de revisiones de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | `<autor>` | `<descripción del cambio>` |
