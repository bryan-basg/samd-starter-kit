# RFC-XXX — {{Título de la decisión}}

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla de RFC del SaMD Starter Kit. Copiá este archivo a `RFC-NNN-titulo-corto.md`, asigná el número siguiente y completá las secciones. Toda decisión de arquitectura, schema, regla clínica o flujo de seguridad necesita su RFC.

---

## Metadatos

| Campo | Valor |
|---|---|
| ID | RFC-XXX |
| Estado | _(propuesto / aceptado / implementado / reemplazado por RFC-YYY)_ |
| Autor | _(nombre)_ |
| Revisores | _(nombres)_ |
| Fecha de propuesta | YYYY-MM-DD |
| Fecha de decisión | YYYY-MM-DD |
| Capa afectada | _(datos / API / frontend / cloud / seguridad / clínica)_ |
| Clase de seguridad del ítem | _(A / B / C)_ |

---

## 1. Contexto

> Estado actual, restricciones, y qué motiva considerar un cambio. Referenciar código con `archivo:línea` cuando aplique.

## 2. Problema

> El problema concreto a resolver, en una o dos frases verificables. Qué pasa si no se resuelve.

## 3. Alternativas consideradas

| # | Alternativa | Pros | Contras | Riesgo SaMD |
|---|---|---|---|---|
| A | _(descripción)_ | _(…)_ | _(…)_ | _(…)_ |
| B | _(descripción)_ | _(…)_ | _(…)_ | _(…)_ |
| C | _(no hacer nada)_ | _(…)_ | _(…)_ | _(…)_ |

## 4. Decisión

> La alternativa elegida y la justificación en una frase. Qué se construye exactamente: archivos, símbolos, schema, endpoints, defaults, validaciones.

## 5. Consecuencias

- **Positivas**: _(qué mejora)_
- **Negativas / costo**: _(qué se paga)_
- **Impacto en consumidores** (§5.6): _(símbolos/archivos afectados; migración necesaria)_
- **Fail-safe**: _(cómo degrada seguro el nuevo comportamiento)_
- **Deuda técnica generada**: _(D-code si aplica)_

## 6. Trazabilidad

| Vínculo | Referencia |
|---|---|
| Requisito(s) | REQ-XXX |
| Riesgo(s) ISO 14971 | R0XX |
| Código | `archivo:línea` |
| Test(s) de verificación | `nombre_del_test` en `archivo` |
| Entrada en Master Map | _(versión vMM.mm)_ |

## 7. Historial

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | _(autor)_ | Propuesta inicial |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
