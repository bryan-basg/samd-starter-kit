# Guía de Certificación SaMD

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Orienta el camino a certificación para la Clase {{SAMD_CLASS}}. No sustituye asesoría regulatoria formal; ajustá a tu vía y mercado.

---

## 1. Punto de partida

| Pregunta | Respuesta |
|---|---|
| ¿Cuál es el uso previsto? | {{INTENDED_USE}} |
| ¿Qué clase SaMD se busca? | Clase {{SAMD_CLASS}} |
| ¿Qué mercados? | _(UE / EE. UU. / otros)_ |
| ¿Qué vía regulatoria? | _(marcado CE bajo MDR / 510(k) / De Novo / otra)_ |
| ¿Hay un sistema de gestión de calidad (ISO 13485)? | _(sí/no — alcance)_ |

La Clase determina el rigor de verificación y la documentación exigida. **A** = sin contribución a daño; **B** = daño no serio posible; **C** = daño serio o muerte posible.

---

## 2. Documentos del DHF necesarios

> El Design History File (DHF) es el expediente que demuestra que el ciclo de vida se siguió. Para Clase {{SAMD_CLASS}} se esperan, como mínimo:

| Documento | Norma | Estado |
|---|---|---|
| Declaración de uso previsto y clasificación | — | _(pendiente)_ |
| Plan de desarrollo de software | IEC 62304 §5.1 | _(pendiente)_ |
| Especificación de requisitos (REQ) | IEC 62304 §5.2 | _(pendiente)_ |
| Arquitectura y diseño detallado | IEC 62304 §5.3/§5.4 | _(pendiente)_ |
| Plan y resultados de verificación (tests) | IEC 62304 §5.5/§5.7 | _(pendiente)_ |
| Matriz de riesgos | ISO 14971 | _(pendiente)_ |
| Matriz de trazabilidad (REQ ↔ Riesgo ↔ Código ↔ Test) | IEC 62304 §5.1 | _(pendiente)_ |
| Gestión de configuración y cambios | IEC 62304 §8 | _(pendiente)_ |
| Plan y resultados de usabilidad | IEC 62366-1 | _(pendiente)_ |
| Evaluación clínica / evidencia | _(marco aplicable)_ | _(pendiente)_ |
| Plan de vigilancia post-mercado | _(marco aplicable)_ | _(pendiente)_ |
| Análisis de software de terceros (SOUP) | IEC 62304 §8.1.2 | _(pendiente)_ |
| Ciberseguridad y privacidad | _(GDPR/HIPAA + guías)_ | _(pendiente)_ |

---

## 3. Pasos recomendados (orden sugerido)

1. **Fijar el uso previsto y la Clase** — todo lo demás se deriva de aquí. No avanzar sin esto cerrado.
2. **Montar el QMS / control documental** (aunque sea mínimo) — versionado, control de cambios, trazabilidad.
3. **Requisitos (REQ)** — cada función clínica como requisito verificable.
4. **Análisis de riesgos ISO 14971** — peligros, secuencias de eventos, medidas de control; trazar a REQ.
5. **Arquitectura + clasificación de ítems de software** — clase de seguridad por ítem.
6. **Verificación** — tests con aserciones reales; cobertura/mutation según política; números registrados.
7. **Usabilidad IEC 62366** — análisis de tareas, evaluación formativa y sumativa.
8. **Evidencia clínica** — según vía y clase; puede requerir estudio.
9. **Trazabilidad cerrada** — cada REQ ↔ Riesgo ↔ Código (`archivo:línea`) ↔ Test existente.
10. **Vigilancia post-mercado** — plan de monitoreo, reporte de incidentes, mejora continua.
11. **Sumisión** — armar el expediente técnico según la vía elegida.

---

## 4. Gaps típicos (los que más frenan)

| Gap | Por qué frena | Mitigación |
|---|---|---|
| **Usabilidad (IEC 62366)** subestimada | Suele faltar evaluación sumativa con usuarios representativos | Planificar tempranamente; presupuestar reclutamiento |
| **Evidencia clínica** insuficiente | Claims sin respaldo proporcional al riesgo | Definir estrategia clínica al fijar el uso previsto |
| **Trazabilidad débil** | Frases genéricas ("validado por X") sin `archivo:línea` ni test | Cada REQ apunta a código + test que existe HOY |
| **SOUP sin gestionar** | Dependencias de terceros sin análisis ni control de CVEs | Inventario + escaneo continuo de CVEs |
| **Ciberseguridad** tardía | Cifrado/gestión de claves/control de acceso como afterthought | Diseñar desde el inicio; SAST/DAST en CI |
| **Claims fuera del uso previsto** | El producto afirma función no certificada | Glosario controlado; revisar todo texto de cara al usuario |

---

## 5. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
