# Master Map — DosiFicta

> Mapa maestro del proyecto. **No asumir rutas; verificarlas.** Toda doc nueva, renombre o reorg se refleja acá (lo mantiene `docs-dhf`). Versión: v1.1.
>
> **Documento de EJEMPLO.** DosiFicta es un dispositivo ficticio con fines didácticos; no calcula dosis reales. Paths, tests y rangos son ilustrativos.

## Identidad del dispositivo

| Campo | Valor |
|---|---|
| Producto | DosiFicta |
| Uso previsto (Intended Use) | Calculadora de bolo de insulina para **adultos con diabetes tipo 1** en tratamiento con múltiples inyecciones diarias. **Sugiere** una dosis de bolo a partir de la glucosa actual, los carbohidratos de la comida, los parámetros configurados por el profesional de salud y la insulina activa estimada. El paciente **confirma o corrige** la dosis antes de aplicarla. NO es para uso pediátrico, embarazo ni bombas de insulina. |
| Clasificación SaMD | **Clase C** (IEC 62304 §4.3) |
| Marco regulatorio | IEC 62304 + ISO 14971 + ISO 13485 + IEC 62366-1 + GDPR + HIPAA + WCAG 2.1 AA |
| Stack frontend | React + TypeScript (la UI **no calcula**: solo muestra lo que devuelve el núcleo) |
| Stack backend | Python + FastAPI; núcleo de cálculo en `app/dosing/` como **funciones puras** sin I/O |
| Stack datos | PostgreSQL (dosis confirmadas + auditoría inmutable) |
| Plataforma cloud | Google Cloud Platform (Cloud Run, Cloud SQL, Secret Manager) |

## Arquitectura (alto nivel)

```text
[ Cliente React ]  -- glucosa + carbohidratos -->  [ API FastAPI ]
                                                        |
                                    +-------------------+-------------------+
                                    v                                       v
                    [ Núcleo de cálculo app/dosing/ ]          [ Parámetros del profesional ]
                    funciones puras, sin red ni BD             (validados al guardarlos)
                    UNIT-01 … UNIT-06                                        |
                                    |                                       |
                                    +---------------> sugerencia <----------+
                                                        |
                              el paciente CONFIRMA  →  [ PostgreSQL: dosis + auditoría ]
```

**Decisión de diseño clave:** el cálculo vive en funciones **puras** (misma entrada → misma salida, sin leer reloj, red ni BD por su cuenta). Así cada unidad se prueba sola, con todos sus bordes, y su diseño detallado cabe en una página. Esa decisión es la que hace manejable la Clase C (ver [`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md) §2).

## Unidades de software críticas

> La **unidad de software** existe desde Clase B (IEC 62304 §5.4.1); en C cada una lleva además su diseño detallado (§5.4.2) y sus criterios de aceptación. Todas son Clase C (no hay segregación: ver [`SOFTWARE_SAFETY_CLASSIFICATION.md`](./SOFTWARE_SAFETY_CLASSIFICATION.md) §5).

| Unidad | Path | Qué hace | Riesgos | Control principal |
|---|---|---|---|---|
| UNIT-01 Validación de entrada | `app/dosing/input_validator.py` | Normaliza la glucosa a mg/dL, rechaza unidades ambiguas y valores fuera de rango, rechaza lecturas viejas | R002, R006 | Unidad **obligatoria y explícita** en el request; sin unidad → rechazo, nunca se adivina |
| UNIT-02 Validación de parámetros | `app/dosing/parameter_validator.py` | Valida los parámetros del profesional al guardarlos | R004 | Rango plausible + vista previa confirmada por el profesional, también en la primera carga |
| UNIT-03 Insulina activa | `app/dosing/insulin_on_board.py` | Estima la insulina que sigue actuando de dosis previas | R003, R009 | Curva fija documentada; sin historial confiable, o con una sugerencia sin cerrar → no sugiere |
| UNIT-04 Cálculo del bolo | `app/dosing/bolus_calculator.py` | Fórmula: comida + corrección − insulina activa | R001, R004 | Función pura, precisión decimal, sin redondeo intermedio; no calcula con parámetros sin confirmar |
| UNIT-05 Límites de seguridad | `app/dosing/safety_limits.py` | Tope por dosis y por insulina reciente, guarda de hipoglucemia, dosis negativa o mínima | R001, R002, R003 | Cualquiera de esos casos → **no sugiere** dosis, muestra qué hacer |
| UNIT-06 Redondeo | `app/dosing/rounding.py` | Redondea al incremento de la pluma | R005 | Siempre **hacia abajo** |
| UNIT-07 Registro de dosis | `app/services/dose_log.py` | Registra la sugerencia antes de mostrarla y la dosis confirmada, una sola vez | R009, R007 | Clave de idempotencia + cifrado de PHI |
| UNIT-08 Salida de errores | `app/main.py` | Convierte un fallo de cálculo en un mensaje seguro | R008 | Nunca un número ni un error técnico: qué hacer |

## Índice documental

| Documento | Qué contiene |
|---|---|
| [`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md) | Lo que Clase C exige además de Clase B, con el diseño detallado de UNIT-05 como ejemplo. |
| [`SOFTWARE_SAFETY_CLASSIFICATION.md`](./SOFTWARE_SAFETY_CLASSIFICATION.md) | Justificación de Clase C. |
| [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md) | Registro de riesgos R001-R009. |
| [`TRACEABILITY_MATRIX_SAMD.md`](./TRACEABILITY_MATRIX_SAMD.md) | REQ → unidad → código → tests → riesgo. |

## Registro de versiones de docs

| Doc | Versión | Última actualización |
|---|---|---|
| MASTER_MAP | v1.1 | 2026-11-24 |
| CLASS_C_DELTA | v1.1 | 2026-11-24 |
| SOFTWARE_SAFETY_CLASSIFICATION | v1.1 | 2026-11-24 |
| ISO_14971_RISK_MATRIX | v1.1 | 2026-11-24 |
| TRACEABILITY_MATRIX_SAMD | v1.1 | 2026-11-24 |

---
**Navegación:** [Índice del ejemplo](./README.md) · [Ejemplo Clase B (AuraLog)](../auralog/README.md)
