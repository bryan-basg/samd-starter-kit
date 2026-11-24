# Qué exige la Clase C que la Clase B no — guía para el programador

**Proyecto:** DosiFicta · **Clase SaMD:** C · **Versión:** v1.1 · **Fecha:** 2026-11-24

> **Documento de EJEMPLO.** DosiFicta es ficticio; no calcula dosis reales. Las cláusulas citadas son orientativas según IEC 62304:2006 + Amd 1:2015 — **contrastalas con la norma** antes de usarlas en un expediente real.

---

## 1. En una frase

En Clase B identificás y verificás las unidades, y probás que **el sistema** hace lo que dicen los requisitos. En Clase C, además, **cada pieza chica del código (unidad)** tiene escrito **antes** cómo funciona y qué tiene que cumplir para darse por buena, y se prueba contra eso, incluidos sus bordes.

Analogía: en Clase B se inspecciona el edificio terminado; en Clase C también se inspecciona **cada viga** antes de montarla, contra su plano.

---

## 2. La diferencia, actividad por actividad

| Actividad (IEC 62304) | Clase B | Clase C | Qué hacés distinto el lunes |
|---|---|---|---|
| Plan: estándares, métodos y herramientas (§5.1.4) | No exigido | **Obligatorio** | Dejás escrito qué guía de estilo, qué linters, qué type-checker y qué versiones usás. El [SDP §7](../../docs/03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md) del kit ya tiene la tabla: llenala. |
| Arquitectura (§5.3) | Obligatorio | Obligatorio | Igual. |
| **Segregación necesaria para control de riesgo** (§5.3.5) | No exigido | **Obligatorio** | Escribís qué controles dependen de que dos ítems estén separados y cómo demostrás que esa separación funciona. "Ninguno" vale si está escrito y justificado. |
| Subdividir en unidades (§5.4.1) | Obligatorio | Obligatorio | Igual. Elegir funciones puras para el núcleo (ver [`MASTER_MAP.md`](./MASTER_MAP.md)) es lo que hace todo lo demás barato. |
| **Diseño detallado por unidad** (§5.4.2) | No exigido | **Obligatorio** | Antes de codear una unidad crítica, una página: qué recibe, qué devuelve, cómo decide, cómo falla. Ejemplo completo en §3. |
| **Diseño de interfaces** (§5.4.3) | No exigido | **Obligatorio** | Tipos exactos de entrada/salida, unidades físicas (mg/dL vs mmol/L), qué pasa con `None`. |
| **Verificar el diseño detallado** (§5.4.4) | No exigido | **Obligatorio** | Otra persona revisa el diseño contra los requisitos y la arquitectura **antes** de implementar. Queda registro (un comentario aprobado en el PR sirve). |
| Criterios de aceptación de unidad (§5.5.3) | Obligatorio | Obligatorio | Igual. |
| **Criterios de aceptación adicionales** (§5.5.4) | No exigido | **Obligatorio** | Para cada unidad revisás 8 aspectos extra (secuencia de eventos, bordes, manejo de fallos…). Ver §4. |
| Verificación de unidad (§5.5.5) | Obligatorio | Obligatorio | Igual, pero contra los criterios de §4. |
| Integración, sistema, liberación (§5.6–§5.8) | Obligatorio | Obligatorio | Mismo proceso; lo que cambia es el **nivel de prueba exigido** a cada unidad (§5). |

> Lo que **no** cambia: trazabilidad, gestión de riesgo, gestión de configuración, resolución de problemas. El kit ya los trae para todas las clases.

---

## 3. Ejemplo: diseño detallado de UNIT-05 (límites de seguridad)

> En tu proyecto, esto vive en un archivo por unidad (ej. `docs/02_architecture_and_design/units/UNIT-05.md`) o como docstring extenso de la función, siempre que se pueda revisar y versionar.

**Unidad:** UNIT-05 · `app/dosing/safety_limits.py::apply_limits` · **Requisitos:** REQ-DOS-02, REQ-DOS-03, REQ-DOS-08, REQ-DOS-09 · **Riesgos:** R001, R002, R003

**Propósito.** Última barrera antes de mostrar un número: impide sugerir una dosis por encima del tope configurado o con la glucosa baja, y nunca muestra una dosis de cero ni negativa.

**Interfaz.**

| Entrada | Tipo | Unidad | Origen |
|---|---|---|---|
| `raw_dose` | `Decimal` (**puede ser negativo**: es un resultado válido) | unidades de insulina (U) | UNIT-04 |
| `glucose_mg_dl` | `Decimal` | mg/dL (ya normalizada) | UNIT-01 |
| `max_bolus` | `Decimal`, > 0 | U | parámetros validados por UNIT-02 |
| `hypo_threshold_mg_dl` | `Decimal` | mg/dL | parámetros validados por UNIT-02 |
| `meter_max_mg_dl` | `Decimal` | mg/dL, máximo que informa el medidor | constante del producto |
| `pen_increment` | `Decimal`, > 0 | U | parámetros validados por UNIT-02 |
| `recent_total` | `Decimal`, ≥ 0 | U de las últimas horas, **sin** descontar curva | historial de UNIT-07, sin pasar por UNIT-03 |
| `max_recent` | `Decimal`, > 0 | U | parámetros validados por UNIT-02 |

| Salida | Cuándo (se evalúa en este orden) |
|---|---|
| `Blocked(reason="LOW_GLUCOSE")` | Glucosa < umbral (**primero**, aun si `raw_dose` llegó inválida) |
| `Blocked(reason="IMPLAUSIBLE_GLUCOSE")` | Glucosa > máximo del medidor (típico de una unidad mal interpretada) |
| `Blocked(reason="MAY_GO_LOW")` | `raw_dose` < 0: la glucosa puede bajar |
| `Blocked(reason="BELOW_MIN_DOSE")` | 0 ≤ `raw_dose` < `pen_increment` |
| `Blocked(reason="ABOVE_MAX")` | `raw_dose` > `max_bolus` |
| `Blocked(reason="ABOVE_RECENT_MAX")` | `recent_total` + `raw_dose` > `max_recent` |
| `Suggestion(dose=raw_dose)` | Ninguna de las anteriores |

**Algoritmo.**

```text
si glucosa, umbral o meter_max no son Decimal finitos → lanza
si glucose_mg_dl < hypo_threshold_mg_dl  → Blocked(LOW_GLUCOSE)
si glucose_mg_dl > meter_max_mg_dl       → Blocked(IMPLAUSIBLE_GLUCOSE)
si alguna otra entrada es None, no finita o viola su rango → lanza
si raw_dose < 0                          → Blocked(MAY_GO_LOW)
si raw_dose < pen_increment              → Blocked(BELOW_MIN_DOSE)
si raw_dose > max_bolus                  → Blocked(ABOVE_MAX)
si recent_total + raw_dose > max_recent  → Blocked(ABOVE_RECENT_MAX)
si no                                    → Suggestion(raw_dose)
```

("Viola su rango" no aplica a `raw_dose`, que admite negativos.)

**Decisiones y por qué.**
- Por encima del tope **no se recorta al tope**: se bloquea. Recortar mostraría un número "válido" para una entrada probablemente errónea; bloquear obliga a revisar.
- La guarda de glucosa baja va primero, **también antes de validar `raw_dose`**: un fallo de cálculo no puede tapar una hipoglucemia. El flujo la evalúa además apenas UNIT-01 valida la glucosa, antes de UNIT-03/04: un historial desconocido tampoco la tapa.
- Una dosis negativa **no es un error**: hay más insulina activa (o menos glucosa) de la que la comida cubre. `MAY_GO_LOW` avisa que la glucosa puede bajar; nunca dice "no necesitás insulina".
- `BELOW_MIN_DOSE`: UNIT-06 redondea hacia abajo, así que una dosis menor al incremento se mostraría como "0 U". Por eso UNIT-05 va **antes** de UNIT-06: redondear primero llevaría "tope + 0.3" justo al tope, que es el recorte que este diseño prohíbe.
- `Decimal`, no `float`: `0.1 + 0.2` en `float` no da `0.3`, y en una dosis eso importa.

**Manejo de fallos.** Si una entrada llega `None`, `NaN` o fuera de su rango y la glucosa no es baja, la función **lanza** un error que el handler convierte en el mensaje seguro de REQ-UX-01. No devuelve un valor por defecto.

**Dependencias.** Ninguna: no lee reloj, red, base de datos ni variables de entorno.

---

## 4. Criterios de aceptación de UNIT-05 (§5.5.3 + §5.5.4)

La norma pide revisar, para Clase C, aspectos adicionales "cuando corresponda". Así quedan aplicados a UNIT-05:

| Aspecto (§5.5.4) | Criterio concreto para UNIT-05 | Cómo se verifica |
|---|---|---|
| Secuencia correcta de eventos | La guarda de glucosa baja se evalúa antes que todo lo demás | `test_low_glucose_wins_over_above_max`, `test_low_glucose_wins_over_invalid_raw` |
| Flujo de datos y de control | Las 7 salidas son alcanzables y no hay otra | Cobertura de ramas 100 % en `safety_limits.py` |
| Asignación de recursos | No aplica (sin I/O, sin hilos) | Revisión del diseño |
| Manejo de fallos | Entrada `None`, `NaN` o fuera de rango, con glucosa no baja → excepción, nunca un valor | `test_invalid_input_raises` |
| Inicialización de variables | Sin estado global ni valores por defecto en los parámetros | Revisión + type-checker estricto |
| Autodiagnóstico | No aplica | Revisión del diseño |
| Gestión de memoria | No aplica (Python, sin buffers propios) | Revisión del diseño |
| **Condiciones de borde** | Glucosa = umbral → permite; dosis = tope → permite; tope + 0.01 → bloquea; dosis = 0 e incremento − 0.01 → `BELOW_MIN_DOSE`; = incremento → permite; −0.01 → `MAY_GO_LOW` | `test_boundaries_max_bolus[justo_debajo,igual,justo_encima]` + equivalentes para glucosa, incremento, `meter_max` y `max_recent` |

> "No aplica" es una respuesta válida **si está escrita y justificada**. Lo que no vale es dejar la fila vacía.

---

## 5. Nivel de prueba: qué se exige a una unidad Clase C

| Prueba | Clase B (kit por defecto) | Clase C (DosiFicta) |
|---|---|---|
| Casos normales | Sí | Sí |
| Bordes (justo debajo, igual, justo encima) | Recomendado | **Obligatorio** en cada umbral |
| Tabla de referencia firmada por el responsable clínico | — | **Obligatorio** para la fórmula (UNIT-04) |
| Propiedades (reglas que valen para miles de entradas al azar, con una librería como `hypothesis`) | — | **Obligatorio** en UNIT-04 y UNIT-05 |
| Cobertura de ramas | Gate global del kit (≥ 95 % de líneas) | **100 % de ramas** en `app/dosing/` y `app/services/dose_log.py` |
| Mutación (¿los tests detectan cambios en el código?) | Umbral por defecto 80 % | **≥ 95 %** sobre `app/dosing/` y `app/services/dose_log.py`; cada sobreviviente se mata o se justifica por escrito |
| Revisión del código | 1 revisor | Revisor **distinto** del autor, con el diseño detallado al lado |

Con el kit, la mutación del núcleo se configura sin tocar scripts:

```bash
MUTMUT_PATHS=app/dosing/ MUTMUT_TESTS=tests/dosing/ MUTMUT_SCORE_THRESHOLD=95 bash scripts/run_mutmut.sh
```

Repetí con `MUTMUT_PATHS=app/services/dose_log.py MUTMUT_TESTS=tests/test_dose_log.py`. El resto (endpoints, `app/main.py`) también es C: lleva §3-§4; el umbral de mutación del núcleo no se le exige porque no calcula ni guarda dosis. (El 100 % de ramas y el 95 % son decisión de este proyecto, no de la norma.)

(Proceso pesado: pide OK cada vez. Hoy corre a mano; si querés que sea periódico, agregá el job de CI como dice [`TESTING_TOOLS.md`](../../docs/03_software_development_plan/TESTING_TOOLS.md).)

---

## 6. Antes de cada release (checklist Clase C)

- [ ] Toda unidad nueva o cambiada tiene diseño detallado **revisado por otra persona** antes del merge.
- [ ] Sus criterios de §4 están escritos y cada uno tiene test o justificación.
- [ ] `tests/dosing/` y `tests/test_dose_log.py` en verde, cobertura de ramas 100 % en `app/dosing/` y `app/services/dose_log.py`, mutación ≥ 95 % (números en el registro de release).
- [ ] La tabla de referencia de UNIT-04 no cambió, o el cambio está firmado otra vez.
- [ ] La matriz de riesgo y la de trazabilidad reflejan el cambio (`check_doc_citations.py` en 0 rotas).

---

## 7. Cómo arrancar un proyecto Clase C con este kit

1. Corré `bash scripts/init_kit.sh` y declarás `SAMD_CLASS=C`.
2. En la [clasificación](../../docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md), decidí qué ítems segregás (ver [`SOFTWARE_SAFETY_CLASSIFICATION.md`](./SOFTWARE_SAFETY_CLASSIFICATION.md) §5 de este ejemplo).
3. Aislá el núcleo crítico en funciones puras, en su propia carpeta.
4. Por cada unidad crítica, copiá la estructura de §3 y §4 de este documento.
5. Subí los umbrales de §5 para esa carpeta (no para todo el repo).

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de DosiFicta](./MASTER_MAP.md)
