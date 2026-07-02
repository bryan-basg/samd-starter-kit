---
name: mesa-ingenieros
description: Método "Mesa de Ingenieros por Sección" — abrir un cajón por sesión, que los agentes de la capa traigan un menú de mejoras de fondo con evidencia, el dueño del proyecto elige, y lo elegido va en PR aislado con trazabilidad DHF. Úsala cuando el dueño quiera atacar deuda técnica de fondo por capas (no un bug puntual urgente), cuando pida "pensar como varios ingenieros" sobre una sección de la app, o cuando quiera abrir un "cajón" (backend, frontend, seguridad, infraestructura, regulatorio) de forma sistemática con evidencia y elección explícita.
---

# mesa-ingenieros — Método "Mesa de Ingenieros por Sección"

Este método sirve para que {{OWNER}} (dev principal, a menudo abrumado por el tamaño de la app) pueda "pensar como varios ingenieros" sin ahogarse en una sola sesión. Es para **deuda técnica de fondo**, no para bugs puntuales urgentes. Si el proyecto lleva un plan de ejecución versionado para esto, registralo en `docs/03_software_development_plan/` (ej. `ENGINEERING_ROUNDTABLE_EXECUTION_PLAN.md`) y leelo primero para el estado y el menú acumulado.

## Cuándo usarla

- {{OWNER}} quiere atacar deuda técnica de fondo por capas, no arreglar un bug puntual.
- {{OWNER}} pide explícitamente "pensar como varios ingenieros" sobre una sección de la app.
- Se quiere abrir un "cajón" (backend+datos, frontend, seguridad+tests, infraestructura, regulatorio/DHF, síntesis cross-capa) de forma sistemática, con evidencia `archivo:línea` y elección explícita del dueño.
- Ya existe un plan de ejecución versionado (`ENGINEERING_ROUNDTABLE_EXECUTION_PLAN.md` o similar) y toca continuar/retomar una sección.

## El método (una sección/cajón por sesión)

1. **Abrir UN cajón** (sección) por sesión — no varios a la vez. Seis secciones típicas (adaptá a las capas reales del proyecto):
   1. backend + datos
   2. lo que el usuario vive (frontend)
   3. que no se rompa (seguridad + tests)
   4. la nube / infraestructura
   5. camino a certificarte (DHF / regulatorio)
   6. síntesis cross-capa

2. **Generar el menú**: lanzá los agentes especialistas de ESA capa en paralelo (ej. `backend` + `db-architect` para la 1; `frontend` ×N para la 2; `security-samd` + `qa-mutation` para la 3; `cloud-ops` para la 4; `samd-audit-trace` + `docs-dhf` para la 5). Cada uno **lee código real** y trae **4-6 mejoras de FONDO (no parches)**, cada una con **evidencia `archivo:línea`**. Agrupá el menú por riesgo (verde/candado/rumbo/higiene).

3. **Verificación adversarial ANTES de ejecutar lo clínico/seguridad** (SaMD §5.6): un hallazgo que dispara cambio en algoritmo de riesgo, schema, regla de negocio o flujo de seguridad debe ser refutado por otro agente independiente antes de tocar código. Este paso existe para cazar falsos positivos (hallazgos que parecen bugs pero son premisas equivocadas) y para no "arreglar" algo que no estaba roto.

4. **{{OWNER}} elige del menú** (sí/no, en sus propias palabras: pequeño/mediano/grande, "me importa romper / no me importa"). Presentá el menú claro, con una recomendación propia justificada en una frase.

5. **Ejecutar lo elegido en PR aislado** con trazabilidad DHF: código + tests verdes (números reales) + papelería (`docs-dhf`: TECHNICAL_DEBT_SUMMARY, ISO_14971_RISK_MATRIX, TRACEABILITY_MATRIX_SAMD, Master Map; códigos de deuda/riesgo; link-checker en 0 rotos). Commit en rama/working limpio; **push/deploy lo decide {{OWNER}}**.

## Reglas de cohesión (anti-drift, con 2+ agentes)

- Leé el **`git diff` REAL** de cada agente, no su resumen, y validá coherencia entre lo que dicen que hicieron y lo que efectivamente cambiaron. Drift → 1 agente correctivo, NO re-lanzar a todos.
- Ningún agente toca trazabilidad directamente: la propone `samd-audit-trace`, la escribe `docs-dhf`, la ejecuta el orquestador. Esto evita que la documentación regulatoria quede redactada por quien tiene incentivo a minimizar su propio hallazgo.
- **Verificación en cascada**: al integrar varias cajas + sesiones paralelas, corré la suite COMPLETA antes de cantar verde — las pasadas individuales no ven regresiones que solo aparecen al juntar todo (killers de mutation rotos por otro cajón, tests que dependían de un cambio de otra sección).
- Si el proyecto tiene una suite de mutation testing load-bearing (tests que verifican contratos específicos, no solo cobertura), tocar un literal/valor de producción obliga a tocar su killer en el mismo PR.

## Cierre de cada cajón

Actualizá el plan de ejecución (si se lleva versionado) con lo ejecutado / diferido / rechazado — incluí la razón cuando algo se rechaza ("la premisa del menú era falsa" es un cierre válido y valioso, no un fracaso). Corré un script de foto de estado del repo (ramas sin mergear, stashes, cambios sin commitear, deuda abierta) antes de declarar la sección cerrada. Reportá a {{OWNER}}: qué se hizo, números de tests, qué quedó en backlog, y qué falta pushear/desplegar (esa decisión es de {{OWNER}}).
