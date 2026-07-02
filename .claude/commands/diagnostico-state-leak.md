---
description: Diagnostica flakys/state-leak entre tests — falla en suite full pero pasa aislado; bisección, orden fijo, sonda contaminante→víctima, error primario.
argument-hint: <test o archivo que flakea>
---

Sos un asistente que diagnostica un flaky de tests que sospechás es state-leak (backend {{BACKEND_STACK}} o frontend {{FRONTEND_STACK}}) en {{PROJECT_NAME}}. NO "arreglar" el fixture global sin reproducir primero — verificá la hipótesis con una sonda antes de tocar un fixture que corre sobre miles de tests.

## Cómo saber si es state-leak (no bug semántico)

- **El test FALLA en la suite full pero PASA aislado → es state-leak, no bug real.**
- **Si cada corrida full falla tests DISTINTOS** (una vez un archivo, otra otro, otra un grupo de componentes) → state-leak entre archivos, orden-dependiente. Hipótesis primera: un mock global se aplicó persistentemente y un archivo posterior lo heredó.
- **Si "primera mitad pasa" Y "segunda mitad pasa" pero "ambas juntas fallan"** → es acumulación/interacción, NO un archivo contaminante único.
- Un cambio de ORDEN (merge que agrega archivos, paralelización con workers, desactivar aleatorización) puede DETONAR un leak latente sin que cambie el código de producción.

## Receta de diagnóstico

1. **Fijar el orden** para reproducir de forma determinista: desactivar la aleatorización del runner (orden fijo); en el frontend, correr la suite completa, no sólo los archivos nuevos.
2. **Bisección por bloques contiguos de archivos + 1 víctima conocida**: acotar dónde está el envenenador. Si el runner reparte tests entre workers, recordá que distintas estrategias de reparto (por archivo, por scope, aleatorio) exponen leaks distintos.
3. **Sonda de 2 tests (contaminante→víctima)** ANTES de tocar cualquier fixture: confirmá que ese par reproduce el leak. Bisección rápida: renombrar/excluir el archivo sospechoso (p.ej. `archivo.test.ext.bak`) y re-correr la suite para confirmar si es el contaminante.
4. **Capturar el ERROR PRIMARIO, no el secundario**: correr con máximo detalle de traceback y detención en el primer fallo (`-x` o equivalente) sobre el subconjunto mínimo que reproduce. El secundario suele ser un error disperso (`KeyError`, `AssertionError` genérico); el primario revela la causa real (p.ej. una llamada de red real porque el mock se desmontó, un 401 en cascada, un token/clave que dejó de validar).

## Causas raíz típicas (backend)

- Un fixture que reasigna una función de servicio (mock de auth, de un proveedor externo) **sin autouse ni restore** → si algo lo resetea, cae al servicio real → fallos en cascada.
- Un test que recarga un módulo (`importlib.reload` o equivalente) con una variable de entorno alterada y **NO restaura** → el estado global queda mutado para los tests siguientes (ejemplo típico: una clave de firma que cambia y los tokens previos dejan de validar).
- **Fix patrón**: fijar en import-time (en el `conftest`/setup global) los valores fijos que el código lee al importar, y usar fixtures `autouse` con teardown que restauren el estado original. Preferir siempre fixtures con teardown que restauren, sobre monkeypatch sin restore.

## Causas raíz típicas (frontend)

- Mocks de módulos globales (router, i18n, data-fetching) con **closure local** (p.ej. una función de navegación mockeada) que persisten entre archivos del mismo worker.
- **Limpieza robusta obligatoria después de cada test**: resetear timers, volver a timers reales, y desmontar el DOM/componentes montados.
- **Cura de raíz**: NO re-mockear lo que ya está en el setup global de tests. Preferir un wrapper real (p.ej. un router real en memoria) en vez de mockear el módulo completo. Si el leak no se ubica en un tiempo razonable, revertir los tests nuevos y dejar la deuda anotada explícitamente en el registro de deuda técnica del proyecto.

## Reglas duras

- Reproducir con sonda ANTES de tocar un fixture global de miles de tests (lección de oro).
- Si hay otra persona/sesión trabajando en paralelo sobre el mismo árbol de trabajo (archivos ajenos sin commitear), PAUSAR las corridas: cambios a medio guardar falsean el diagnóstico.
- Verificar la SUITE COMPLETA antes de cantar verde; un flaky orden-dependiente no se ve corriendo sólo tu archivo.

Test/archivo que flakea: $ARGUMENTS
