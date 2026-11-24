# Ejemplo trabajado — DosiFicta (SaMD Clase C ficticio)

> **Dispositivo ficticio y propósito didáctico. NO es un software para calcular dosis reales.** DosiFicta **no existe**; es un dispositivo inventado para mostrar qué cambia en el trabajo diario del programador cuando el software es **Clase C**. Ninguna cita `archivo::símbolo`, test, fecha, umbral ni número de esta carpeta corresponde a un producto real, ni es una recomendación clínica. Los rangos numéricos son **ilustrativos**: en un proyecto real los fija y firma el responsable clínico.

## ¿Qué es DosiFicta?

DosiFicta es una **calculadora de bolo de insulina** para adultos con diabetes tipo 1 en tratamiento con inyecciones. Antes de comer, el paciente ingresa su glucosa actual y los carbohidratos que va a comer; DosiFicta **sugiere una dosis** usando los parámetros que configuró su profesional de salud (relación insulina/carbohidratos, factor de sensibilidad, objetivo de glucosa) y descontando la insulina que todavía está activa de dosis anteriores. **El paciente confirma o corrige la dosis antes de aplicarla.**

## ¿Por qué es Clase C y AuraLog es Clase B?

La diferencia está en **qué pasa si el software se equivoca**:

| | AuraLog (Clase B) | DosiFicta (Clase C) |
|---|---|---|
| Qué hace | Avisa "consultá a tu profesional" | Sugiere **un número** que el paciente se inyecta |
| Peor fallo | La alerta no llega → la consulta se **retrasa** | La dosis sale el doble → **hipoglucemia grave**, que puede causar convulsiones, coma o muerte |
| Daño | No grave, reversible | **Grave o muerte** |

Analogía: AuraLog es el testigo del tablero del auto que se olvida de encenderse; DosiFicta es el **freno**. Si el testigo falla, llegás tarde al mecánico; si el freno falla, chocás. Al freno se le exige mucho más antes de salir a la calle.

## Documentos que muestra este ejemplo

| Archivo de ejemplo | Qué demuestra | Plantilla vacía equivalente en `docs/` |
|---|---|---|
| [`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md) | **Empezá por acá.** Qué hace distinto el programador en Clase C: diseño detallado por unidad, criterios de aceptación por unidad, pruebas extra. Con un ejemplo completo de una unidad. | [`SOFTWARE_DEVELOPMENT_PLAN.md` §4](../../docs/03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md) |
| [`MASTER_MAP.md`](./MASTER_MAP.md) | Identidad del dispositivo, arquitectura, las 8 **unidades** de software críticas y su riesgo. | [`docs/00_master/MASTER_MAP.md`](../../docs/00_master/MASTER_MAP.md) |
| [`SOFTWARE_SAFETY_CLASSIFICATION.md`](./SOFTWARE_SAFETY_CLASSIFICATION.md) | Justificación de Clase C (IEC 62304 §4.3) y por qué las medidas externas no alcanzan para bajarla. | [`docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md`](../../docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md) |
| [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md) | 9 riesgos, varios **catastróficos** (dosis sobrestimada, confusión de unidades, insulina activa no descontada), cada uno de esos con controles en dos unidades distintas. | [`docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md`](../../docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md) |
| [`TRACEABILITY_MATRIX_SAMD.md`](./TRACEABILITY_MATRIX_SAMD.md) | Requisitos trazados **hasta la unidad** (`UNIT-xx`) y a varios tests por requisito: límites y propiedades. | [`docs/07_regulatory_and_compliance/TRACEABILITY_MATRIX_SAMD.md`](../../docs/07_regulatory_and_compliance/TRACEABILITY_MATRIX_SAMD.md) |

## Cómo leerlo

1. Leé primero [`CLASS_C_DELTA.md`](./CLASS_C_DELTA.md): es la respuesta a "¿qué hago distinto el lunes?".
2. Compará cada documento con su par de [`examples/auralog/`](../auralog/README.md): el molde es el mismo, cambia la **profundidad**.
3. Fijate en la coherencia cruzada: las mismas unidades (`UNIT-01`…`UNIT-08`), los mismos riesgos (`R001`…`R009`) y los mismos requisitos (`REQ-DOS-01`…) aparecen en los cinco documentos.

> Recordatorio: las citas (`app/dosing/bolus_calculator.py::calculate_bolus`) y los tests son **ilustrativos**. En un proyecto real, `docs-dhf` verifica que existan HOY antes de escribir la fila.
