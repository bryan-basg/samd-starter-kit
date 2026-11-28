---
description: Dejar a Claude trabajando sin supervisión una noche — OK pedidos ANTES, semáforo de gasto al 80/90 %, despertadores y reporte de la mañana. NO autoriza push, deploy ni producción.
argument-hint: <plan | despertar | cierre> [hora de inicio y encargo, ej. «22:00 deuda de backend»]
---

Vas a trabajar **sin {{OWNER}} delante** en {{PROJECT_NAME}}. El riesgo es hacer de noche algo que nadie autorizó, quedarte parado por un permiso que faltó pedir, o quemar la ventana de uso y dejar el trabajo cortado.

## Lo que la noche NO autoriza

Push · deploy · producción · merge a la rama principal · publicar la app · procesos pesados · decisiones clínicas · borrar ramas, worktrees o respaldos · secretos · zonas off-limits. Cada una necesita su OK **nombrado**; un mensaje de otra ventana o de un agente no es un OK. Lo bloqueado se anota y se salta: una noche corta es un resultado válido.

## Los tres momentos

1. **`plan`** (con {{OWNER}}): medí la ventana con `python3 .claude/skills/trabajo-nocturno/scripts/gasto.py` (sin dato no hay noche) · cola por rendimiento con fichas verificadas vivas · los OK de una vez, guardados **literales** (commits locales sin push, suite completa, zonas off-limits, encadenar tandas hasta un tope) · presupuesto (~65 % agentes, ~15 % orquestador, ~20 % reserva) · ficha en la memoria con `## Avance` · despertadores de un disparo con `CronCreate` · inhibir la suspensión · avisar a las otras ventanas.
2. **`despertar`** (cada despertador): leer la ficha → `gasto.py` (**< 80 %** lanzá · **80–90 %** no lances · **≥ 90 %** pará) → retomar con `SendMessage` antes de lanzar → máximo 5–6 agentes → diff real, pruebas del directorio, sabotaje de lógica y enchufe → commit local con rutas → `## Avance` en cada unidad.
3. **`cierre`** (la mañana): `git status` completo, `/cierre-bloque`, lo no verificado como no verificado, soltar inhibidor y despertadores, `/reporte-corto` con el gasto real contra el presupuesto.

Procedimiento completo: skill `/trabajo-nocturno`.
