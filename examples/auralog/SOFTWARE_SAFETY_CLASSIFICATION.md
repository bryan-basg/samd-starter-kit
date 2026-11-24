# Clasificación de Seguridad del Software

**Proyecto:** AuraLog · **Clase SaMD:** B · **Versión:** v1.1 · **Fecha:** 2026-11-24

> Documento de clasificación conforme a **IEC 62304 §4.3** (Clasificación de seguridad del software). Justifica la clase global asignada, analiza las consecuencias del fallo del software, segrega los ítems de software por clase y enumera las medidas de control de riesgo externas al software.
>
> **Documento de EJEMPLO.** AuraLog es un dispositivo ficticio con fines didácticos.

---

## 1. Resumen de la clasificación

| Campo | Valor |
|---|---|
| Dispositivo software | AuraLog |
| Uso previsto | App para que pacientes con una condición crónica **estable, ya valorada por un profesional, en la que retrasar una consulta no causa daño grave** (p. ej. rinitis alérgica); NO para condiciones en las que sí puede causarlo (p. ej. epilepsia, insuficiencia cardíaca, riesgo suicida) registren y sigan sus síntomas, reciban recordatorios y obtengan **alertas informativas** ("consultá a tu profesional") cuando los patrones cruzan umbrales configurados. NO diagnostica ni recomienda tratamiento. |
| Clase de seguridad global asignada | **B** |
| Norma de clasificación | IEC 62304 §4.3 (Ed. 2006 + Amd 1:2015) |
| Referencia de gestión de riesgo | ISO 14971 — matriz de riesgo `./ISO_14971_RISK_MATRIX.md` |
| Responsable de la clasificación | Responsable de Gestión de Riesgo, AuraLog (ejemplo) |

---

## 2. Criterios de clasificación IEC 62304 §4.3

| Clase | Definición (paráfrasis; contrastar con la norma) |
|---|---|
| **A** | El fallo o comportamiento inesperado del software **no puede contribuir** a una situación peligrosa, o la contribución no resulta en un riesgo inaceptable tras considerar las medidas de control de riesgo externas. |
| **B** | Tras las medidas externas el riesgo es inaceptable y el daño posible es **no grave**. |
| **C** | Tras las medidas externas el riesgo es inaceptable y el daño posible es **muerte o daño grave**. |

La clasificación se realiza **después** de considerar las medidas de control de riesgo externas al software (hardware, procedimientos, supervisión humana), conforme a §4.3.

---

## 3. Justificación de la Clase B

AuraLog **registra** los síntomas que el paciente ingresa y **alerta** de forma informativa cuando los patrones cruzan umbrales configurados. La cadena de eventos peligrosa más relevante es: el **motor de alertas** (`alert_engine`) falla o evalúa mal un patrón → **no se genera** la alerta "consultá a tu profesional" → el paciente **no es invitado a tiempo** a contactar a su profesional → se **retrasa** la consulta clínica.

Ese retraso constituye un daño **no grave y reversible**: AuraLog no diagnostica, no prescribe ni administra terapia, y la decisión clínica siempre recae en el profesional humano que el paciente consulta por las vías habituales. La alerta es un **recordatorio informativo**, no un acto médico. El paciente conserva sus canales clínicos ordinarios (turnos, urgencias, contacto directo con su profesional) con independencia de AuraLog; la app no es la única ni la principal vía de detección.

Tras aplicar las medidas de control de riesgo externas (etiquetado que declara el carácter informativo de las alertas, indicación de consultar siempre con el profesional, supervisión clínica del paciente fuera de la app), y suponiendo que el software **falla** (probabilidad 1, IEC 62304 §4.3), el daño posible no es grave. Los controles internos (§4) reducen el riesgo, pero **no cuentan** para clasificar. Por lo tanto la clase resultante es **B**.

| Pregunta de clasificación | Respuesta |
|---|---|
| ¿Puede el software contribuir a una situación peligrosa? | Sí — una alerta perdida o tardía puede retrasar la consulta con el profesional. |
| Severidad del daño potencial (ISO 14971) | No grave (retraso en el cuidado, reversible). |
| ¿Existen medidas externas que reduzcan el riesgo antes de clasificar? | Sí — etiquetado del carácter informativo, indicación explícita de consultar al profesional, canales clínicos del paciente independientes de la app. |
| Clase resultante tras medidas externas | **B** |

---

## 4. Análisis de fallo del software (¿qué pasa si falla?)

| ID | Componente / función | Modo de fallo | Consecuencia potencial | Severidad | Medida de control de riesgo | Clase del ítem |
|---|---|---|---|---|---|---|
| F-01 | `alert_engine` (motor de alertas) | No detecta el cruce de umbral; la alerta no se genera | El paciente no es invitado a consultar → retraso del cuidado | No grave | Interna SW: fail-safe + reintento; red de respaldo por scheduler (`scheduled_evaluation`) → R001 | B |
| F-02 | `threshold_config` (validador de umbrales) | Acepta un umbral fuera de rango → alerta nunca dispara o dispara siempre | Alertas perdidas o ruido que el paciente termina ignorando | No grave | Interna SW: validación de rango + conserva umbral seguro previo → R002 | B |
| F-03 | `alert_dispatcher` (entrega de notificación) | La alerta se genera pero no se entrega al dispositivo | El paciente no ve la alerta a tiempo → retraso | No grave | Interna SW: cola persistente + reintentos con backoff → R003 | B |
| F-04 | `sync_service` (sincronización offline) | Un registro hecho sin conexión se pierde al fallar el sync | Síntoma no evaluado → posible alerta no generada | No grave | Interna SW: outbox idempotente; el registro no se borra del cliente hasta confirmación → R004 | B |
| F-05 | `EncryptedString` (cifrado en reposo) | PHI almacenada o registrada en claro | Exposición de datos de salud del paciente | No grave (privacidad) | Interna SW + externa: AES-256-GCM, clave en Secret Manager, redacción en logs → R005 | B |
| F-06 | Capa de identidad / autorización | Un usuario accede a registros de otro paciente (IDOR) | Exposición de PHI de un tercero | No grave (privacidad) | Interna SW: identidad solo del token JWT; nunca user_id desde body/query → R006 | B |

> Cada modo de fallo se enlaza con un riesgo de la matriz ISO 14971 (`R001`…`R006`) y con la prueba que verifica su control (ver `./TRACEABILITY_MATRIX_SAMD.md`).

---

## 5. Segregación de ítems de software por clase (IEC 62304 §4.3 d) / §5.3)

La segregación permite asignar clases distintas a ítems de software dentro del mismo sistema, siempre que se justifique la **independencia** entre ítems (sin acoplamiento que permita que el fallo de un ítem de clase **inferior** afecte a uno de clase **superior**).

| Ítem de software | Función | Clase asignada | Justificación de segregación / independencia |
|---|---|---|---|
| `app/services/alert_engine.py` | Evalúa patrones de síntomas contra umbrales y genera alertas informativas | B | Núcleo del impacto clínico; concentra la lógica que puede contribuir al retraso del cuidado. |
| `app/services/alert_dispatcher.py` | Entrega la alerta al dispositivo del paciente | B | Acoplado al motor de alertas; un fallo de entrega también retrasa el aviso. |
| `app/jobs/scheduled_evaluation.py` | Red de respaldo: reevalúa registros pendientes | B | Mitiga F-01; comparte la criticidad clínica del motor. |
| `app/services/reminders.py` (recordatorios de registro) | Recuerda al paciente que registre sus síntomas | B | Si falla, el paciente no registra y la alerta no se genera (ver F-04). |
| `app/services/analytics_dashboard.py` | Gráficos de tendencia para el paciente (solo lectura) | B | Un gráfico erróneo puede retrasar la consulta; comparte proceso y BD con el camino de alertas. |
| `badges` (insignias de constancia) | Insignias motivacionales | A | Servicio de Cloud Run aparte, credencial de BD de solo lectura sobre vistas propias; su fallo no llega al camino de alertas. |

**Mecanismos de segregación aplicados:** solo `badges` está segregado: otro proceso, otro despliegue y una credencial que no puede escribir ni leer las tablas de registros y alertas. Los demás ítems comparten proceso y base de datos con `alert_engine`, así que no se los puede tratar como A.

> Un ítem solo baja de clase con segregación demostrada; si no, hereda la B.

---

## 6. Medidas de control de riesgo externas al software

Medidas que **no** residen en el software y que reducen el riesgo antes de la clasificación (IEC 62304 §4.3, ISO 14971 §7).

| ID | Medida externa | Tipo | Riesgo mitigado (ISO 14971) | Evidencia / responsable |
|---|---|---|---|---|
| EXT-01 | Etiquetado e IFU que declaran que las alertas son **informativas, no diagnósticas**, y que el paciente debe consultar siempre a su profesional | Informativo | R001, R002 | IFU de AuraLog (ejemplo) / Asuntos Regulatorios |
| EXT-02 | El paciente conserva sus canales clínicos ordinarios (turnos, urgencias) independientes de la app | Procedimental | R001, R003 | Programa de cuidado del paciente / profesional tratante |
| EXT-03 | Onboarding que instruye a configurar los umbrales **con** el profesional, no por cuenta propia | Procedimental | R002 | Material de onboarding / profesional tratante |
| EXT-04 | Aviso de privacidad y consentimiento informado sobre el tratamiento de datos de salud | Informativo | R005, R006 | Política de privacidad / DPO |

> Tipos según ISO 14971: seguridad inherente por diseño, medidas de protección, e información de seguridad (etiquetado/instrucciones). Las medidas informativas son las de menor prioridad y nunca sustituyen a los controles internos del software.

---

## 7. Conclusión de la clasificación

El sistema **AuraLog** se clasifica globalmente como **Clase B** bajo IEC 62304 §4.3: su fallo puede contribuir a una situación peligrosa (retraso de la consulta clínica por una alerta perdida o tardía) cuyo daño es no grave y reversible. El ítem segregado `badges` es **Clase A** por la independencia justificada en la sección 5; recordatorios y gráficos son B. Las actividades del ciclo de vida aplicables a Clase B se definen en el Plan de Desarrollo de Software ([`docs/03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md`](../../docs/03_software_development_plan/SOFTWARE_DEVELOPMENT_PLAN.md) §4, plantilla del kit).

---

## 8. Control de revisiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | 2026-06-28 | Asuntos Regulatorios, AuraLog (ejemplo) | Clasificación inicial de AuraLog como Clase B; segregación de `gamification` y `analytics_dashboard` como Clase A. |
| v1.1 | 2026-11-24 | Asuntos Regulatorios, AuraLog (ejemplo) | Uso previsto acotado; los controles internos dejan de contar para clasificar; recordatorios y gráficos pasan a B (no estaban segregados) y solo `badges` queda en A. |

> Toda reclasificación (cambio de clase de un ítem o del sistema) exige re-evaluar las actividades obligatorias del SDP y registrar el impacto en la matriz de trazabilidad y en el plan de mantenimiento.

---
**Navegación:** [Índice del ejemplo](./README.md) · [Master Map de AuraLog](./MASTER_MAP.md)
