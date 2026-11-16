# Clasificación de Seguridad del Software

**Proyecto:** DosiFicta · **Clase SaMD:** C · **Versión:** v1.0 · **Fecha:** 2026-11-16

> **Documento de EJEMPLO.** DosiFicta es un dispositivo ficticio; no calcula dosis reales. Componentes, rangos y tests son ilustrativos. La clasificación real de un producto la decide el fabricante con criterio regulatorio y, según el mercado, la revisa el organismo notificado.

---

## 1. Resumen de la clasificación

| Campo | Valor |
|---|---|
| Dispositivo software | DosiFicta |
| Uso previsto | Sugerir una dosis de bolo de insulina a adultos con diabetes tipo 1 (múltiples inyecciones diarias), a partir de la glucosa, los carbohidratos, los parámetros del profesional y la insulina activa. El paciente confirma antes de aplicar. |
| Clase de seguridad global asignada | **C** |
| Norma de clasificación | IEC 62304 §4.3 (Ed. 2006 + Amd 1:2015) |
| Referencia de gestión de riesgo | ISO 14971 — [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md) |
| Responsable de la clasificación | Responsable de Gestión de Riesgo, DosiFicta (ejemplo) |

---

## 2. Criterios de clasificación IEC 62304 §4.3

| Clase | Definición (paráfrasis; contrastar con la norma) |
|---|---|
| **A** | El fallo no puede contribuir a una situación peligrosa, o no resulta en un riesgo inaceptable tras las medidas externas. |
| **B** | El fallo puede contribuir a una situación peligrosa que resulte en **daño no grave**. |
| **C** | El fallo puede contribuir a una situación peligrosa que resulte en **muerte o daño grave**. |

La clase se asigna mirando la severidad del daño **después** de considerar las medidas de control **externas** al software (no las internas).

---

## 3. Justificación de la Clase C

| Pregunta de clasificación | Respuesta |
|---|---|
| ¿Puede el software contribuir a una situación peligrosa? | Sí — una dosis sugerida mayor a la necesaria, si se aplica, produce hipoglucemia. |
| Severidad del daño potencial (ISO 14971) | **Grave o muerte**: la hipoglucemia severa puede causar convulsiones, pérdida de conciencia, coma o muerte. |
| ¿Existen medidas externas que reduzcan el riesgo? | Parcialmente: el paciente confirma la dosis, recibe formación de su profesional y puede medir su glucosa después. |
| ¿Las medidas externas bastan para bajar la clase? | **No.** La confirmación del paciente es débil justamente cuando más importa: un paciente que confía en la calculadora rara vez rehace la cuenta a mano, y una hipoglucemia previa reduce su capacidad de detectar un número raro. Ninguna medida externa **independiente** del software impide que se aplique una dosis errónea. |
| Clase resultante | **C** |

> Comparación: en AuraLog (Clase B) la medida externa ("es una alerta informativa; tu profesional sigue a cargo") sí acota el daño a un retraso. Acá el software produce el número que entra al cuerpo del paciente.

---

## 4. Análisis de fallo del software (¿qué pasa si falla?)

| ID | Unidad | Modo de fallo | Consecuencia potencial | Severidad | Control de riesgo (interno) | Riesgo |
|---|---|---|---|---|---|---|
| F-01 | UNIT-04 `bolus_calculator` | Error en la fórmula (signo, orden de operaciones, factor invertido) | Dosis sobrestimada → hipoglucemia grave | Catastrófica | Función pura + tests de propiedades + tabla de casos firmada por el responsable clínico | R001 |
| F-02 | UNIT-01 `input_validator` | Glucosa en mmol/L tomada como mg/dL (o al revés) | Corrección 18 veces menor/mayor → hipo o hiperglucemia grave | Catastrófica | Unidad obligatoria y explícita; sin unidad → rechazo | R002 |
| F-03 | UNIT-03 `insulin_on_board` | No descuenta la insulina activa de una dosis reciente | Dosis "apilada" → hipoglucemia grave | Catastrófica | Sin historial confiable → no sugiere dosis | R003 |
| F-04 | UNIT-02 `parameter_validator` | Acepta un parámetro absurdo (ej. sensibilidad 5 en vez de 50) | Correcciones muy grandes en cada uso | Catastrófica | Rango plausible + doble confirmación del profesional | R004 |
| F-05 | UNIT-05/06 | Supera el tope o redondea hacia arriba | Dosis mayor a la calculada | Crítica | Tope duro + redondeo siempre hacia abajo | R001, R005 |
| F-06 | UNIT-01 | Usa una lectura de glucosa vieja | Corrección sobre un valor que ya cambió | Crítica | Lectura con más de 15 min → se pide una nueva | R006 |
| F-07 | UNIT-07 `dose_log` | Registra dos veces la misma dosis o ninguna | Insulina activa mal estimada en el próximo cálculo | Catastrófica | Clave de idempotencia; registro fallido → aviso visible | R009 |

---

## 5. Segregación de ítems de software por clase (IEC 62304 §4.3, §5.3)

Un ítem de software puede tener clase menor que el sistema **solo si** está separado de forma demostrable (que su fallo no pueda afectar al ítem de clase mayor).

| Ítem | Clase | Decisión |
|---|---|---|
| Núcleo de cálculo `app/dosing/` (UNIT-01…06) | C | Corazón del riesgo. |
| Registro de dosis `app/services/dose_log.py` (UNIT-07) | C | Alimenta la insulina activa del próximo cálculo: su fallo **sí** afecta la dosis. |
| Pantalla de historial y gráficos | C | **No se segregó.** Comparte proceso y base de datos con el núcleo; demostrar la separación costaba más que tratarla como C. |
| Exportar informe PDF para el profesional | C | Ídem. |

> Lección para el programador: **segregar es una decisión de costo**. Si separar un módulo (otro proceso, sin acceso de escritura a los datos del núcleo) es barato, permite tratarlo como B o A. Si no, todo es C y se trabaja con el rigor de C.

---

## 6. Medidas externas consideradas (no bajan la clase)

| ID | Medida | Por qué no basta |
|---|---|---|
| EXT-01 | Confirmación explícita de la dosis por el paciente | Depende de que el paciente detecte el error; ver §3. |
| EXT-02 | Formación del paciente por su profesional | No es independiente del momento del uso. |
| EXT-03 | Medición de glucosa posterior | Detecta el daño, no lo evita. |

---

## 7. Conclusión

DosiFicta se clasifica **Clase C**: su fallo puede contribuir a muerte o daño grave y ninguna medida externa independiente acota ese daño. Se aplican todas las actividades de IEC 62304 para Clase C; lo que cambia en el trabajo diario está en [`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md).

## 8. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | 2026-11-16 | Responsable de Gestión de Riesgo (ejemplo) | Clasificación inicial |

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de DosiFicta](./MASTER_MAP.md)
