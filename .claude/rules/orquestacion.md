# REGLAS DURAS DE EJECUCIÓN — las obedecen TODOS (consecuencia SaMD §5.6 análisis de impacto + §5.7 verificación)

> Regla **transversal** sin `paths:`: carga en cada sesión **y en cada subagente**, que la relee en cada turno — por eso solo lleva lo que obedecen todos. **Cómo se orquesta** (delegar, postura, anti-drift, diseño de equipo A-F) vive en el estilo de salida «Orquestador SaMD» §2 (`.claude/output-styles/orquestador.md`), que solo carga la sesión principal; las sesiones paralelas, en su §3. Mapa del cerebro: `CLAUDE.md` §MAPA DE ESTE CEREBRO.

## Reglas duras que un modelo mejor NO anula (mecánica, no torpeza)

Estas no son limitaciones del modelo: son mecánica de las herramientas, factura o contrato regulatorio. Un modelo más capaz las sigue teniendo que respetar.

1. **El motor de mutación nunca en paralelo con agentes que escriben tests** *(herramienta)*: el motor congela la lista de tests en su arranque; los tests nuevos no entran. Patrón correcto: agentes → suite verde → **entonces** mutación.
2. **Procesos pesados locales piden OK CADA vez** *(CPU del dueño)*: mutación, fuzz, suites completas (incluidos el tier de BD real con docker y el stress del pool), suite E2E completa. "Vamos con todo" cubre el plan, **no** los subprocesos pesados implícitos.
   ⚠️ **Un SUBAGENTE que corre una suite completa SÍ entra en esta regla.** Lanzar un agente no consume la máquina del dueño, pero lo que el agente hace después sí: un subagente que ejecuta `Bash` corre en la máquina de {{OWNER}} **venga la orden de quien venga** — por eso el brief de cada agente le dice que corre SOLO los tests de su propio directorio o archivo; la suite completa la corre el orquestador UNA sola vez, al final, con el árbol quieto. Candado mecánico: `.claude/scripts/candado_suite_completa.py` (hook `PreToolUse` en `.claude/settings.json`, documentado en `SOFTWARE_CONFIGURATION_MANAGEMENT_PLAN.md`) lo deniega dentro de cualquier subagente — incluido `pytest tests/ -k <patrón>`, que recorre todo pese a parecer acotado (un patrón sobre el directorio entero no es una ruta). Lo que NO deniega, a propósito: `pytest -q tests/<archivo>.py` y `npm test -- <archivo>` / `vitest run <archivo>`, porque son justo los tests propios que el brief le pide correr a un agente.
   **Excepción — los escaneos CORTOS no piden OK**: los que terminan en un par de minutos (en este kit, `run_trivy.sh` ~30 s y `run_semgrep.sh` ~2 min) corren solos. Exigir permiso para eso solo lograba que **no se corrieran**, que es peor que el costo que ahorraba. Regla de corte: **cualquier cosa más larga que el SAST cae del lado que pide OK**; ante la duda sobre una herramienta nueva, **pedí OK**. La lista canónica vive en `.claude/rules/comandos.md`, partida en esas dos mitades.
3. **Fugas de estado entre tests con mocks globales** *(herramienta)*: los mocks de módulos globales con closure local se filtran entre archivos. Verificar la suite **COMPLETA** antes de cantar verde; el `worktree` mitiga pero no exime.
4. **Checklist físico antes de una corrida de mutación completa** *(hardware)*: refrigeración OK, navegador cerrado, sin runners en paralelo, procesos de fondo matados, concurrencia = núcleos − 4.
5. **Los tests killer de mutación son load-bearing** *(contrato SaMD §5.7)*: los literales empáticos, logs, etiquetas ARIA y fórmulas que un killer verifica son **contratos verificados**. Tocar el literal de producción obliga a tocar su killer en el mismo PR. Aflojar killers sin justificación SaMD documentada: prohibido.

## Higiene de contexto (sesión principal y agentes)

Cada turno relee todo lo anterior, así que lo que un comando devuelve **se paga en cada turno siguiente** — y en un subagente, eso pesa más que las reglas que heredó al nacer.

* **Buscá antes de leer**: primero qué archivos contienen algo (`grep -l`, o la herramienta de búsqueda en modo archivos), después solo el tramo que importa (`sed -n 'A,Bp'`, lectura con `offset`/`limit`). No leas un archivo entero para encontrar una función.
* **Nunca abras entero un documento vivo grande** (`TECHNICAL_DEBT_SUMMARY.md`, un `*_HISTORY*.md`): `grep -n` del ID y lectura del rango.
* **Recortá las salidas**: `git diff --stat` antes del diff completo; tests con `-q` y `| tail -N`; `grep` con `| head`.
* **No releas** lo que ya leíste en esta conversación, salvo que haya cambiado.

## Antes de cantar verde (todos)

Son las reglas 5-7 de sesiones paralelas (estilo «Orquestador SaMD» §3); viven acá porque un agente que verifica las necesita igual que la sesión principal.

* **Los tests que comparten recurso necesitan aislamiento por proceso.** Dos corridas simultáneas de la suite que usan el mismo archivo de base de datos **se la borran entre sí**. Sufijá el recurso con el PID del proceso para que cada corrida tenga el suyo, y verificalo con sabotaje (sin el sufijo, debe romper).
* **Bajá la concurrencia de las suites E2E cuando la máquina está compartida.** El techo pensado para "una sola cosa corriendo" satura la máquina entera si hay otras ventanas o agentes trabajando.
* **Mirá el `git status` completo, no solo tus archivos.** Si aparece trabajo de otra ventana o de otro agente a medio hacer, tu type-check o tu lint puede estar leyendo un archivo a mitad de edición. **El verde no vale hasta repetirlo con el árbol quieto.**
