# Manual de Usuario — {{PROJECT_NAME}}

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Documentación de usuario final. Junto con las [Instrucciones de Uso (IFU)](../07_regulatory_and_compliance/INSTRUCTIONS_FOR_USE_IFU.md) y el [etiquetado](../07_regulatory_and_compliance/MEDICAL_DEVICE_LABELING.md), forma la **información de seguridad** que acompaña al dispositivo (IEC 62304 §5.8, IEC 62366-1, ISO 14971 §7 — medidas informativas). Todo texto de cara al usuario respeta el **glosario clínico pre-certificación**: no afirmar función de dispositivo médico no certificado. Toda fila `<...>` es un placeholder a completar.

---

## 1. Para quién es este manual

| Campo | Valor |
|---|---|
| Usuario previsto | `<perfil del usuario: paciente / cuidador / profesional>` |
| Uso previsto | {{INTENDED_USE}} |
| Lo que el producto **sí** hace | `<funciones reales>` |
| Lo que el producto **NO** hace | `<límites explícitos — p. ej. no diagnostica, no recomienda tratamiento>` |
| Contraindicaciones / advertencias | `<cuándo NO debe usarse>` |

> La frontera entre lo que hace y lo que no hace sostiene la clasificación de seguridad. Mantené este apartado coherente con la [clasificación](../07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md).

---

## 2. Primeros pasos

1. `<requisitos: dispositivo, sistema operativo, conexión>`
2. `<cómo instalar / acceder>`
3. `<cómo crear cuenta / iniciar sesión>`
4. `<configuración inicial mínima>`

---

## 3. Tareas principales (paso a paso)

> Cada tarea debería corresponder a un caso de uso analizado en usabilidad (IEC 62366-1). Redacción clara, sin jerga técnica, con lenguaje empático.

| Tarea | Cómo se hace | Resultado esperado |
|---|---|---|
| `<tarea 1>` | `<pasos>` | `<qué ve el usuario>` |
| `<tarea 2>` | `<pasos>` | `<...>` |

---

## 4. Mensajes, alertas y qué hacer ante ellos

> Las alertas son medidas de control de riesgo: el usuario debe entender qué significan y qué acción tomar. Sin tracebacks ni códigos técnicos de cara al usuario.

| Mensaje / alerta | Qué significa | Qué debe hacer el usuario |
|---|---|---|
| `<mensaje>` | `<significado en lenguaje claro>` | `<acción recomendada>` |
| `<alerta de seguridad>` | `<...>` | `<a quién contactar / qué revisar>` |

---

## 5. Privacidad de tus datos

`<Resumen en lenguaje claro de qué datos se recogen, para qué, y los derechos del usuario. Remitir a la política completa.>` Ver [Política de Privacidad](../07_regulatory_and_compliance/PRIVACY_POLICY.md).

---

## 6. Resolución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `<síntoma>` | `<causa>` | `<pasos>` |
| Sin conexión | `<comportamiento offline-first>` | `<qué sigue funcionando y qué se sincroniza luego>` |

---

## 7. Soporte y reporte de problemas

| Canal | Detalle |
|---|---|
| Soporte | `<email / formulario / horario>` |
| Reporte de un problema de seguridad del paciente | `<vía de reporte — alimenta la vigilancia post-mercado>` |
| Responsable del producto | {{OWNER}} |

> Los reportes de usuario alimentan el [Plan de Vigilancia Post-Mercado](../07_regulatory_and_compliance/POST_MARKET_SURVEILLANCE_PLAN.md). Un evento adverso sigue el [procedimiento de resolución de problemas](../07_regulatory_and_compliance/SOFTWARE_PROBLEM_RESOLUTION_PROCEDURE.md).

---

## 8. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | `<autor>` | `<descripción>` |

> El manual de usuario es parte del expediente. Cada cambio de función de cara al usuario exige actualizar este manual, la IFU y el etiquetado en el mismo ciclo de release.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md) · [IFU](../07_regulatory_and_compliance/INSTRUCTIONS_FOR_USE_IFU.md)
