# Matriz de Trazabilidad SaMD

**Proyecto:** DosiFicta · **Clase SaMD:** C · **Versión:** v1.0 · **Fecha:** 2026-11-16

> **Regla más estricta del DHF.** Cada `REQ-XXX` apunta a código citado por NOMBRE (`ruta/archivo.py::símbolo`) y a tests que existen HOY, citados igual. En Clase C se agrega una columna: la **unidad de software** (`UNIT-xx`), porque cada unidad tiene su propio diseño detallado y criterios de aceptación ([`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md)).
>
> **Documento de EJEMPLO.** DosiFicta es ficticio; las citas y los tests son ilustrativos.

## Cadena de trazabilidad (Clase C)

```text
Necesidad clínica → REQ → UNIT (diseño detallado + criterios de aceptación) → código (archivo::símbolo) → tests (unidad + límites + propiedades) → Riesgo
```

## Requisitos del sistema

| REQ | Descripción | Riesgo | Unidad | Implementación | Verificación | Estado |
|---|---|---|---|---|---|---|
| REQ-DOS-01 | Bolo = carbohidratos / relación + (glucosa − objetivo) / sensibilidad − insulina activa, calculado en decimal sin redondeo intermedio | R001 | UNIT-04 | `app/dosing/bolus_calculator.py::calculate_bolus` | `tests/dosing/test_bolus_calculator.py::test_matches_signed_reference_table`, `tests/dosing/test_bolus_calculator.py::test_more_carbs_never_lowers_dose` (propiedad) | ✓ |
| REQ-DOS-02 | Ninguna sugerencia supera el tope máximo por dosis configurado; por encima, no se sugiere número | R001 | UNIT-05 | `app/dosing/safety_limits.py::apply_limits` | `tests/dosing/test_safety_limits.py::test_never_suggests_above_max_bolus`, `tests/dosing/test_safety_limits.py::test_boundaries_max_bolus[justo_debajo,igual,justo_encima]` | ✓ |
| REQ-DOS-03 | Con glucosa por debajo del umbral de hipoglucemia no se sugiere bolo; se muestran instrucciones | R001 | UNIT-05 | `app/dosing/safety_limits.py::apply_limits` | `tests/dosing/test_safety_limits.py::test_low_glucose_blocks_bolus` | ✓ |
| REQ-DOS-04 | La glucosa exige unidad explícita (mg/dL o mmol/L); sin unidad, o con valor incompatible con la unidad, se rechaza | R002 | UNIT-01 | `app/dosing/input_validator.py::validate_meal_input` | `tests/dosing/test_input_validator.py::test_missing_unit_is_rejected`, `tests/dosing/test_input_validator.py::test_value_implausible_for_unit_is_rejected` | ✓ |
| REQ-DOS-05 | Una lectura con más de 15 min de antigüedad no se usa | R006 | UNIT-01 | `app/dosing/input_validator.py::validate_meal_input` | `tests/dosing/test_input_validator.py::test_stale_reading_is_rejected` | ✓ |
| REQ-DOS-06 | Se descuenta la insulina activa; sin historial confiable de las últimas horas, no se sugiere dosis | R003 | UNIT-03 | `app/dosing/insulin_on_board.py::insulin_on_board` | `tests/dosing/test_insulin_on_board.py::test_recent_dose_is_subtracted`, `tests/dosing/test_insulin_on_board.py::test_unknown_history_blocks_suggestion` | ✓ |
| REQ-DOS-07 | La dosis se redondea siempre hacia abajo al incremento de la pluma | R005 | UNIT-06 | `app/dosing/rounding.py::round_dose` | `tests/dosing/test_rounding.py::test_always_rounds_down` | ✓ |
| REQ-PAR-01 | Los parámetros del profesional se validan contra rango plausible; un cambio grande pide segunda confirmación | R004 | UNIT-02 | `app/dosing/parameter_validator.py::validate_parameters` | `tests/dosing/test_parameter_validator.py::test_rejects_out_of_range`, `tests/dosing/test_parameter_validator.py::test_large_change_requires_second_confirmation` | ✓ |
| REQ-LOG-01 | Cada confirmación se registra exactamente una vez; si el registro falla, se bloquea la próxima sugerencia y se avisa | R009 | UNIT-07 | `app/services/dose_log.py::record_confirmed_dose` | `tests/test_dose_log.py::test_same_confirmation_is_stored_once`, `tests/test_dose_log.py::test_failed_write_blocks_next_suggestion` | ✓ |
| REQ-SEC-01 | Dosis y glucosas cifradas en reposo; identidad solo del token | R007 | UNIT-07 | `app/services/dose_log.py::record_confirmed_dose` | `tests/test_dose_log.py::test_dose_fields_are_encrypted_at_rest` | ✓ |
| REQ-UX-01 | Un fallo de cálculo muestra un mensaje seguro ("no apliques una dosis basada en esta pantalla") y qué hacer, nunca un error técnico | R008 | — | `app/main.py::unhandled_exception_handler` | `tests/test_error_handler.py::test_calculation_failure_shows_safe_message` | ✓ |

## Qué cambia respecto de AuraLog (Clase B)

- **Columna "Unidad"**: el requisito no termina en un archivo; termina en una unidad con diseño detallado propio.
- **Varios tests por requisito**: el caso normal, los **límites** (justo debajo, igual, justo encima) y una **propiedad** (una regla que vale para miles de entradas generadas al azar, ej. "más carbohidratos nunca bajan la dosis").
- **Tabla de casos firmada**: `test_matches_signed_reference_table` compara contra una tabla de entradas → dosis esperadas calculada a mano y **firmada por el responsable clínico**. El test no inventa la respuesta correcta: la toma de quien tiene autoridad para darla.

## Verificación de integridad de la matriz

```bash
python3 scripts/check_doc_citations.py          # citas archivo::símbolo existen
pytest -q tests/dosing/                         # todas las unidades del núcleo
bash scripts/run_mutmut.sh                      # mutación sobre app/dosing/ (pide OK: proceso pesado)
```

> En este ejemplo ficticio los comandos no devolverán resultados reales: ilustran el procedimiento.

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de DosiFicta](./MASTER_MAP.md)
