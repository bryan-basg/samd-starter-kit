# Estrategia Completa de Testing (SaMD §5.7)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}}

> Verificación demostrable es un requisito SaMD, no una opción. Esta guía es la fuente de la estrategia; los números vivos (cobertura actual, mutation score) van en la memoria del agente, no acá.

## Pirámide de verificación

| Nivel | Herramienta (adaptá) | Umbral | Cuándo corre |
|---|---|---|---|
| Unit + integración | runner del stack | Cobertura GLOBAL ≥95% (capa datos/SQL ≥95%) | Cada PR (CI) + local pre-push |
| Type checking | type-checker estricto | 0 errores | Cada PR + local |
| Mutation testing | Stryker (FE) / mutmut (BE) o equiv. | FE módulos clínicos/críticos ≥90% · resto FE ≥75% piso · BE módulos clínicos ≥80% | Nightly incremental + mensual full |
| SAST | Semgrep | 0 findings High/Critical sin waiver | Nightly + PR con paths-filter |
| Deps / CVEs | Trivy | 0 CVE High/Critical sin waiver | Nightly + PR |
| Fuzz de contrato | schemathesis vs OpenAPI | 0 fallos de contrato | Paths-filter API |
| DAST | OWASP ZAP o equiv. | 0 FAIL | Nightly |
| E2E | Playwright o equiv. | flujos clínicos críticos verdes | Pre-release |

## Reglas duras (no negociables)

1. **Tests rigurosos, no de humo.** Aserciones específicas sobre valores, llamadas y side effects.
2. **Tras cada Edit/Write**, correr los tests vinculados y **reportar números** antes de declarar hecho.
3. **Mocks asíncronos firmes** + aislamiento de estado global por test.
4. **`hasattr`/duck-typing bajo test** → mock con whitelist explícita de atributos.
5. **WebSocket tests** vía doble sobre el orquestador, no cliente síncrono que dispare el lifespan.
6. **No correr unit/type-checker mientras corre mutation** — se contaminan.
7. **El motor de mutation NUNCA en paralelo con agentes que escriben tests** — fija el conteo en el dry-run inicial. Patrón: agentes → suite verde → mutation.
8. **Procesos pesados (mutation full, fuzz, suite completa) piden OK explícito CADA vez.**

## Mutation testing — disciplina

- `ignoreStatic: true` para no malgastar tiempo mutando constantes estáticas.
- Atacar el umbral **por archivo**, no en superficie. Irreducibles → refactor de producción mínimo justificado, no cerrar por debajo del umbral.
- Los tests de mutation son **load-bearing**: tocar el literal de producción obliga a tocar su killer en el mismo PR.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
