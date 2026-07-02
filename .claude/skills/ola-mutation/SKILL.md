---
name: ola-mutation
description: Procedimiento completo de una ola de mutation testing (Stryker/mutmut o equivalente) — candidatos, agentes escriben tests, suite verde, OK para correr el motor, leer scores. Úsala cuando el usuario pida atacar mutantes sobrevivientes de un área/archivos concretos, subir el score de mutación de un módulo, u organizar una tanda de tests killer antes de correr el motor de mutation.
---

# ola-mutation — Ola de mutation testing por área

Orquesta una ola de mutation testing del proyecto con el motor de mutation configurado (frontend/backend, SaMD Clase B §5.7.4, meta según umbral vigente del proyecto). Se ataca por ÁREAS acotadas, no una corrida full de varias horas de una sola vez. El patrón canónico es: candidatos → agentes escriben tests killer → suite unitaria local VERDE → recién ahí OK para correr el motor de mutation → leer scores.

## Cuándo usarla

- El usuario pide subir el mutation score de un área/módulo/archivos concretos.
- Hay un reporte de mutación baseline con mutantes `Survived`/`NoCoverage` que atacar.
- Se va a repartir la escritura de tests killer entre varios agentes en paralelo antes de una corrida de mutation.
- Toca decidir si conviene correr el motor scoped a una ola o si hace falta backupear/restaurar el reporte global antes de una corrida.

## Patrón canónico (en ESTE orden, es load-bearing)

1. **Identificar candidatos** (barato, sin máquina): del reporte de mutación baseline (ej. `mutation.json` o equivalente del motor usado), priorizar archivos con más mutantes vivos (`Survived`/`NoCoverage`). Extraé la lista de survivors por archivo ANTES de lanzar agentes.
2. **Lanzar agentes en paralelo, uno por archivo**, con brief duro: target ≥ umbral individual, listado de survivors específico, y las reglas anti-drift del proyecto. Regla dura: **NO lanzar los agentes que escriben tests EN PARALELO con el motor de mutation** — el motor congela la lista de tests en el dry-run inicial y los tests nuevos no entran.
3. **Esperar a que TODOS los agentes terminen.**
4. **Correr la suite de tests unitarios COMPLETA** (no sólo los archivos nuevos): los flakys orden-dependientes por fuga de estado entre tests sólo se exponen en la suite full. Arreglar rojos antes de seguir. Si aparece una fuga de estado, diagnosticar por bisección (aislar el archivo sospechoso, correr en orden fijo, identificar quién contamina a quién) antes de tocar producción.
5. **Pedir OK explícito al dueño del proyecto para correr el motor de mutation** (proceso pesado local — checklist antes de una corrida full: refrigeración del equipo OK, navegador pesado cerrado, sin paralelismo de otros runners, procesos idle matados, concurrencia configurada dejando núcleos libres para el SO).
6. **Correr el motor scoped** (acotado a la ola) y leer los scores. Commit selectivo de los tests killer.

## Config scoped (para no correr full)

- Creá una config efímera de mutation que mute sólo los archivos de la ola (ej. `stryker.conf.olaXX.json` o el equivalente de tu motor), con el modo incremental desactivado y el reporte apuntando a un archivo propio de la ola (para no pisar el reporte global).
  - Revisá la forma exacta en que tu motor acepta overrides de CLI vs config file — algunos flags sueltos se interpretan como argumento posicional o como opción desconocida en vez de aplicarse; la vía segura suele ser la config JSON/YAML dedicada.
  - Un override de CLI para acotar a un solo archivo puntual en un remate final suele funcionar aparte de la config de la ola.
- Reusá (o derivá) una config de test runner para la ola que EXCLUYA los tests que estén en rojo por trabajo sin commitear de sesiones paralelas — un solo test rojo puede abortar el dry-run completo del motor de mutation. Identificá los rojos corriendo la suite con salida en JSON antes de lanzar el motor.
- **Backup del reporte global de mutación** antes de cada corrida scoped, y restaurarlo después. Aunque la config scoped redirija su propio reporte, conviene backupear igual por seguridad.
- Referenciá el script wrapper del proyecto para mutation (variantes: incremental por defecto / subset acotado / full completo — full solo con OK y checklist).

## Señal de alarma (tests no incluidos)

Si tras una corrida del motor el score subió **muy poco** pese a haber agregado muchos tests killer → sospechar que los tests NO se incluyeron (se crearon después del dry-run). Verificá en el log del motor la línea que reporta cuántos archivos y tests encontró, y comparala con los timestamps de los archivos de test nuevos. Si el conteo de tests es viejo, re-correr el motor (el modo incremental suele ser rápido porque el cache ya está caliente).

## Otras trampas comunes de mutation testing

- Un mock de la función de traducción/formato que ignora la clave real puede generar cientos de mutantes de literales de texto falsos-equivalentes. Palanca principal: convertir el mock en un spy que preserve el comportamiento real y assertar sobre los argumentos recibidos.
- Constantes definidas a nivel de módulo (arrays/objetos evaluados al cargar el archivo) pueden reportarse como vivas bajo un análisis de cobertura "por test" — cambiar a análisis de cobertura global para ese batch.
- Archivos mockeados globalmente en el setup de tests, si se testean re-importando el módulo real dentro de un test puntual, el motor puede no rastrear esa cobertura — hay que des-mockear dinámicamente e importar la versión real dentro del test.
- Un agente que "amplía" un test puede BORRAR cobertura existente sin darse cuenta (ej. al reemplazar una interacción por otra más simple) → verificá `NoCoverage` contra el baseline, no sólo el score total.

## Reglas duras

- Atacar el umbral objetivo por archivo, no en superficie. Irreducibles reales → refactor de producción mínimo y justificado (inyección de dependencia con valor por defecto, extraer una función pura, nombrar una constante que antes era inline), NO cerrar por debajo del umbral sin justificación. Si tras 2 pasadas sigue por debajo sin refactor posible, dejarlo como deuda explícita en el documento de deuda técnica del proyecto (con un identificador propio, ej. `D-MUT-<archivo>-...`), NO marcarlo como "cerrado".
- No modificar tests de zonas sensibles del producto (áreas de uso final del usuario, no de administración/desarrollo) sin OK explícito; si un archivo pide refactor de producción, preguntar antes.
- Producción intacta salvo el refactor mínimo justificado.
