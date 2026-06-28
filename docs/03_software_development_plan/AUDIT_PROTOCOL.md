# Protocolo de Auditoría Interna

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Define cómo se audita un changeset o una fase contra el marco SaMD antes de declararlo cerrado.

---

## 1. Propósito

Garantizar que ningún cambio que toque algoritmo clínico, esquema de datos, regla de negocio o flujo de seguridad llegue a producción sin **trazabilidad** (IEC 62304 §5.1/§5.7), **análisis de impacto** (§5.6) y **verificación demostrable** (§5.7).

---

## 2. Cuándo se dispara una auditoría

| Disparador | Alcance de auditoría |
|---|---|
| Cambio en algoritmo clínico | Completa (trazabilidad + riesgo + verificación) |
| Cambio de schema / migración | Completa |
| Cambio en flujo de seguridad / auth | Completa |
| Cierre de fase / sprint / bloque grande | Completa + checklist de cierre |
| Cambio de UI sin impacto clínico | Ligera (verificación + a11y) |
| Refactor sin cambio de comportamiento | Ligera |

---

## 3. Procedimiento de auditoría de un changeset

1. **Leer el `git diff` real** del changeset (no el resumen de quien lo hizo).
2. **Análisis de impacto** (§5.6): buscar globalmente TODOS los consumidores de cada símbolo, parámetro, retorno, schema o constante modificada. Actualizar cada consumidor en el mismo cambio.
3. **Verificación** (§5.7): correr los tests vinculados y registrar números reales (pasados/fallados/cobertura/mutation cuando aplique).
4. **Verificación adversarial** sobre hallazgos clínicos o de seguridad: un segundo revisor independiente debe refutar el hallazgo antes de actuar. Hallazgo no verificado ≠ arreglado.
5. **Fail-safe**: confirmar que los modos de fallo degradan seguro y no exponen tracebacks.
6. **Trazabilidad**: cada cambio relevante referencia REQ-XXX y/o Riesgo-XXX con `archivo:línea` verificable y nombre de test existente HOY.

---

## 4. Rol de los agentes regulatorios

| Agente | Hace | NO hace |
|---|---|---|
| `samd-audit-trace` | Audita el changeset contra IEC 62304 §5.1/§5.7 + ISO 14971; **detecta** gaps de trazabilidad y propone qué falta. | No escribe documentación; no decide el fix. |
| `docs-dhf` | **Materializa** las actualizaciones: Master Map, resumen de deuda técnica, matriz de riesgos, matriz de trazabilidad, RFCs, guías. Verifica `archivo:línea` + tests reales. Corre el link-checker cross-doc. | No audita por sí solo; complementa a `samd-audit-trace`. |

Regla de cohesión: ningún agente de ejecución toca trazabilidad; la **propone** `samd-audit-trace` y la **ejecuta** el orquestador vía `docs-dhf`.

---

## 5. Checklist de cierre de bloque grande

> Un "bloque grande" es un sprint o fase. El patrón canónico de cierre actualiza los 7 artefactos:

- [ ] **Audit** — auditoría del changeset completa, hallazgos resueltos o anotados.
- [ ] **Spec** — especificación/diseño actualizado al comportamiento real.
- [ ] **TECHNICAL_DEBT** — deuda nueva registrada; deuda cerrada marcada con su D-code.
- [ ] **Guide** — guía de desarrollo/usuario actualizada si cambió el flujo.
- [ ] **RFCs** — RFC creado/actualizado para cada decisión de arquitectura/schema/clínica/seguridad.
- [ ] **Master Map** — versión incrementada; el cambio aparece en el mapa maestro.
- [ ] **Risk Matrix** — riesgos nuevos/modificados reflejados en la matriz ISO 14971.

Verificaciones finales:

- [ ] Link-checker cross-doc reporta **0 enlaces rotos**.
- [ ] Cada REQ-XXX nuevo apunta a `archivo:línea` + test existente.
- [ ] Tests vinculados corridos; números reportados.
- [ ] Sin residuos de valores/reglas viejas tras propagar (grep en `docs/` y configuración → 0 residuos).

---

## 6. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |
