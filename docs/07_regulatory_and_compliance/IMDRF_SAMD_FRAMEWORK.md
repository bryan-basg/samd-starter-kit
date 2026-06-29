# IMDRF SaMD Framework — Categorización de Riesgo Internacional

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Ubicación de **{{PROJECT_NAME}}** dentro del marco del **International Medical Device Regulators Forum (IMDRF)** — el lenguaje común que armoniza FDA, EU MDR, Health Canada, PMDA y otros. Aplica la **matriz de categorización de riesgo SaMD** (estado de la condición de salud × significancia de la información) y conecta la Clase de seguridad IEC 62304 {{SAMD_CLASS}} con la categoría IMDRF.
>
> **Esto es un andamio de categorización, no una declaración regulatoria.** La categoría final la confirma el responsable regulatorio ({{OWNER}}). Documentos de referencia IMDRF: **N10** (Key Definitions), **N12** (Risk Categorization Framework), **N23** (QMS), **N41** (Clinical Evaluation). `{{VERIFICAR_CLAUSULA}}` = referencia pendiente de verificación.
>
> Mantenida por `docs-dhf`.

---

## 1. ¿Es {{PROJECT_NAME}} un SaMD? (IMDRF N10)

**SaMD** = software destinado a uno o más fines médicos, que cumple esos fines **sin formar parte del hardware** de un dispositivo médico (IMDRF N10, "Software as a Medical Device: Key Definitions").

| Criterio N10 | Respuesta del proyecto |
|---|---|
| ¿Cumple un fin médico definido en su uso previsto? | {{TODO: sí/no}} — uso previsto: {{INTENDED_USE}} |
| ¿Funciona sin ser parte del hardware de un dispositivo? | {{TODO}} |
| ¿Es accesorio de otro dispositivo (lo excluiría como SaMD-standalone)? | {{TODO}} |
| **¿Califica como SaMD?** | {{TODO}} |

---

## 2. Matriz de categorización de riesgo (IMDRF N12)

La categoría SaMD surge del cruce de dos ejes:

- **Estado de la condición/situación de salud** (gravedad del contexto clínico): **Crítico · Serio · No serio**.
- **Significancia de la información** que aporta el SaMD a la decisión sanitaria: **Tratar o diagnosticar · Impulsar la gestión clínica · Informar la gestión clínica**.

> Glosario clínico pre-certificación: en texto de cara al usuario, *diagnosticar* → **valoración**, *clínico* → **profesional**. En este documento regulatorio se conserva la terminología IMDRF estándar para fidelidad normativa, sin afirmar estatus de certificación que el proyecto no posee.

### 2.1 Definición de los ejes

| Estado de la condición de salud | Definición (N12) |
|---|---|
| **Crítico** | Situaciones donde una intervención precisa y/o a tiempo es vital para evitar muerte, discapacidad de largo plazo u otro deterioro grave; condiciones de progresión rápida. |
| **Serio** | Situaciones donde una intervención precisa importa, pero no es típicamente crítica para una acción inmediata; condiciones de progresión moderada. |
| **No serio** | Situaciones donde una intervención precisa no es crítica para la acción y la condición es de progresión lenta o de bajo impacto. |

| Significancia de la información | Definición (N12) |
|---|---|
| **Tratar o diagnosticar** | La información se usa para tomar una acción inmediata o casi inmediata de tratamiento/valoración. Máxima significancia. |
| **Impulsar la gestión clínica** (drive) | La información se usa para guiar el próximo paso (p. ej. ayudar a decidir, predecir, priorizar). |
| **Informar la gestión clínica** (inform) | La información se agrega a otras; no desencadena por sí sola una acción inmediata. Mínima significancia. |

### 2.2 Matriz de categorías (N12)

Categorías de **I (menor impacto)** a **IV (mayor impacto)**:

| Estado de la condición ↓ \ Significancia → | Tratar o diagnosticar | Impulsar gestión clínica | Informar gestión clínica |
|---|---|---|---|
| **Crítico** | **IV** | **III** | **II** |
| **Serio** | **III** | **II** | **I** |
| **No serio** | **II** | **I** | **I** |

### 2.3 Ubicación de este proyecto

| Pregunta | Respuesta del proyecto |
|---|---|
| Estado de la condición de salud abordada | {{TODO: Crítico / Serio / No serio}} |
| Significancia de la información que aporta | {{TODO: Tratar-diagnosticar / Impulsar / Informar}} |
| **Categoría IMDRF resultante (I–IV)** | {{TODO}} |
| Justificación (remitir al uso previsto, sin inventar contenido clínico) | {{TODO}} |

---

## 3. Correspondencia entre ejes regulatorios

Los ejes son **independientes**; esta tabla es orientativa, NO una equivalencia normativa. La correspondencia exacta la confirma el responsable regulatorio.

| Marco | Eje del proyecto | Valor |
|---|---|---|
| IEC 62304 §4.3 | Clase de seguridad del software (A/B/C) | **{{SAMD_CLASS}}** |
| IMDRF N12 | Categoría SaMD (I–IV) | {{TODO}} (ver §2.3) |
| EU MDR | Clase Regla 11 (I/IIa/IIb/III) | {{TODO}} (ver `EU_MDR_MAPPING.md`) |
| FDA | Clase de dispositivo (I/II/III) + Documentation Level | {{TODO}} (ver `FDA_SUBMISSION_MAPPING.md`) |

> **Advertencia anti-alucinación:** NO existe un mapeo automático "Clase C ⇒ Categoría IV ⇒ MDR III ⇒ FDA III". Cada autoridad aplica su propio esquema. Documentar cada eje por separado y justificar.

---

## 4. Consideraciones por categoría (N12 §7–§8)

A mayor categoría, mayor rigor esperado en V&V, evidencia clínica y control de cambios. Mapeo al DHF:

| Consideración IMDRF | Documento DHF que la soporta | Estado |
|---|---|---|
| Rigor de verificación proporcional a la categoría | `COMPLETE_TESTING_STRATEGY.md`; `CRITICAL_MODULES_INVENTORY.md` | {{Pendiente}} |
| Evaluación clínica proporcional (N41) | `CLINICAL_EVALUATION_PLAN.md`; `CLINICAL_VALIDATION_REPORT.md` | {{Pendiente}} |
| QMS (N23) | `ISO_13485_READINESS_PLAN.md` | {{Pendiente}} |
| Gestión de riesgo | `ISO_14971_RISK_MATRIX.md` | {{Pendiente}} |
| Trazabilidad de socio-técnica a decisión clínica | `TRACEABILITY_MATRIX_SAMD.md` | {{Pendiente}} |

---

## 5. Good Machine Learning Practice (GMLP) — si aplica IA/ML

Aplica **solo si {{PROJECT_NAME}} incorpora IA/ML**. Estado actual: {{TODO: aplica / N/A}}.

Los **10 Guiding Principles de GMLP** (FDA / Health Canada / MHRA, Oct 2021; alineados con el trabajo IMDRF sobre ML — ver N67 para términos clave) y su mapeo al DHF:

| # | Principio GMLP (resumen) | Documento DHF de apoyo | Estado |
|---|---|---|---|
| 1 | Experiencia multidisciplinaria a lo largo del ciclo de vida | `VISION_AND_GOVERNANCE.md` | {{TODO}} |
| 2 | Buenas prácticas de ingeniería de software y seguridad | `SOFTWARE_DEVELOPMENT_PLAN.md`; `COMPLIANCE_AND_SECURITY_MASTER.md` | {{TODO}} |
| 3 | Datos representativos de la población de uso prevista | `CLINICAL_EVALUATION_PLAN.md` | {{TODO}} |
| 4 | Independencia entre datos de entrenamiento y de test | `COMPLETE_TESTING_STRATEGY.md` | {{TODO}} |
| 5 | Reference standard basado en la mejor evidencia disponible | `CLINICAL_VALIDATION_REPORT.md` | {{TODO}} |
| 6 | Diseño del modelo adecuado a los datos y al uso previsto | `RFC-*.md` (RFC del modelo) | {{TODO}} |
| 7 | Foco en el desempeño del equipo humano-IA (si hay humano en el loop) | `USER_GUIDE.md`; `CLINICAL_EVALUATION_PLAN.md` | {{TODO}} |
| 8 | Pruebas en condiciones clínicamente relevantes | `CLINICAL_VALIDATION_REPORT.md` | {{TODO}} |
| 9 | Información clara para los usuarios (limitaciones, datos, desempeño) | `INSTRUCTIONS_FOR_USE_IFU.md` | {{TODO}} |
| 10 | Monitoreo del modelo desplegado y gestión de reentrenamiento | `POST_MARKET_SURVEILLANCE_PLAN.md`; `SOFTWARE_MAINTENANCE_PLAN.md` | {{TODO}} |

> El control de cambios del modelo se preautoriza vía **PCCP** (ver `FDA_SUBMISSION_MAPPING.md` §4). Toda salida de la IA respeta el glosario clínico pre-certificación: sin claims de dispositivo no certificado, con validador y fallback seguro (riesgos `R-IA-*` en `ISO_14971_RISK_MATRIX.md`).

---

## 6. Huecos y pendientes IMDRF

| Hueco | Acción pendiente | Responsable |
|---|---|---|
| Categoría SaMD (I–IV) sin confirmar | Completar §2.3 con justificación | {{OWNER}} |
| Aplicabilidad de GMLP | Confirmar si hay función de IA/ML | {{OWNER}} |
| Referencia N67 (ML key terms) | Verificar número y vigencia del documento IMDRF | {{OWNER}} |
| Referencias IMDRF | Matriz N12 §7.2 verificada verbatim contra el documento oficial; reconfirmar N-docs (N10/N23/N41/N67) contra el catálogo IMDRF vigente | ✓ verificado |

---

## 7. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vX.Y | YYYY-MM-DD | {{OWNER}} | Marco IMDRF inicial (matriz N12, correspondencia de ejes, GMLP). |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md) · [Crosswalk](./REGULATORY_FRAMEWORK_CROSSWALK.md)
</content>
