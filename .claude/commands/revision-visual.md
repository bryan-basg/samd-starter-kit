---
description: 'Mirada de diseñador sobre una pantalla o pieza de {{PROJECT_NAME}} — foto real, 6 lentes dentro de las reglas de UX clínica y un menú de mejoras para que {{OWNER}} elija. No aplica nada sin su elección.'
argument-hint: '<pantalla o pieza, ej. landing | inicio | panel-profesional | logo> [pregunta concreta]'
---

Vas a hacer de **diseñador gráfico con las reglas del proyecto en la cabeza**: traés un menú con evidencia y **{{OWNER}} elige**. Procedimiento completo y manual de marca: `.claude/skills/revision-visual/SKILL.md` y su `reference.md` (§7: lo que {{OWNER}} ya rechazó no se vuelve a proponer).

1. **Frenos**: en una zona off-limits se mira y se propone, no se toca sin pedido dirigido. Costo antes de lanzar un agente.
2. **Foto real, nunca un mockup**: `/captura-sin-login` si está detrás del login; cada tema que exista; **solo datos de ejemplo** (una captura con datos reales es PHI).
3. **6 lentes**: jerarquía · espaciado y ritmo · tipografía · color y contraste · coherencia de marca · **carga sensorial** (si choca «más lindo» con «menos carga», gana menos carga).
4. **La cancha**: `.claude/rules/frontend-ux.md` y sus guardianes `frontend/src/__tests__/disenoPlano.test.ts` y `frontend/src/__tests__/contraste.test.ts`. Lo que la rompe no entra al menú.
5. **Menú**: máximo ~6 mejoras, en lenguaje cotidiano, con tamaño y si toca una zona off-limits. «Está bien, no cambiaría nada» es un resultado válido. Terminá con tu recomendación.
6. **Aplicar lo elegido**: agente `frontend`; foto antes y después; guardianes + tests del componente + `npm run typecheck` + `npm run lint`.
