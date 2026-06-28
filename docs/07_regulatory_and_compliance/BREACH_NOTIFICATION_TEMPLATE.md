# Plantilla de Notificación de Brecha de Datos Personales / de Salud

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Plantilla para notificar una brecha de seguridad de datos personales y/o de salud a la **autoridad de control** y a los **titulares afectados**. Cumple **GDPR Art. 33 (notificación a la autoridad, plazo 72 h) y Art. 34 (comunicación al interesado)** y la **HIPAA Breach Notification Rule (45 CFR §§164.400-414)**. Una brecha confirmada activa este flujo de inmediato; no se espera al cierre del análisis forense para arrancar el reloj de 72 h.

---

## 1. Reloj regulatorio (plazos máximos)

| Obligación | Marco | Plazo | Cuenta desde |
|---|---|---|---|
| Notificación a la autoridad de control | GDPR Art. 33 | **72 horas** | Conocimiento de la brecha por el responsable. |
| Comunicación a los interesados | GDPR Art. 34 | **Sin demora indebida** | Confirmación de alto riesgo para derechos y libertades. |
| Notificación a individuos | HIPAA §164.404 | **≤ 60 días** | Descubrimiento de la brecha. |
| Notificación a HHS / autoridad (≥ umbral) | HIPAA §164.408 | **≤ 60 días** (o anual si < umbral) | Descubrimiento de la brecha. |
| Notificación a medios (≥ <MEDIA_THRESHOLD> afectados) | HIPAA §164.406 | **≤ 60 días** | Descubrimiento de la brecha. |

> Si no es posible aportar toda la información en plazo, GDPR Art. 33(4) permite **notificación por fases**. Documentar el retraso y su justificación.

---

## 2. Datos de identificación de la brecha

| Campo | Valor |
|---|---|
| ID interno de incidente | <INC-XXXX> |
| Fecha y hora de detección | YYYY-MM-DD HH:MM (TZ) |
| Fecha y hora estimada de inicio | YYYY-MM-DD HH:MM (TZ) |
| Fecha y hora de contención | YYYY-MM-DD HH:MM (TZ) |
| Detectada por | <persona / sistema / alerta> |
| Estado | En curso / Contenida / Cerrada |
| Responsable del tratamiento (titular) | {{OWNER}} |
| Delegado de Protección de Datos (DPO) | <DPO> |
| Encargado(s) del tratamiento implicado(s) | <proveedores> |

---

## 3. Naturaleza de la brecha

| Campo | Valor |
|---|---|
| Tipo de incidente | Confidencialidad / Integridad / Disponibilidad |
| Vector | <ej. acceso no autorizado, exfiltración, pérdida, ransomware, error de configuración> |
| Categorías de datos afectados | <PII: nombre/contacto/identificadores> · <PHI / datos de salud> · <credenciales> |
| ¿Datos especiales (GDPR Art. 9) / PHI? | Sí / No |
| ¿Datos cifrados en reposo? | Sí (AES-256-GCM) / No / Parcial |
| Volumen estimado de registros | <N> |
| Número estimado de interesados afectados | <N> |
| Categorías de interesados | <usuarios / profesionales / menores> |

---

## 4. Evaluación de riesgo para los interesados

| Factor | Valoración |
|---|---|
| Probabilidad de daño | Alta / Media / Baja |
| Severidad del daño potencial | Catastrófica / Crítica / Seria / Menor |
| ¿Alto riesgo para derechos y libertades (umbral Art. 34)? | Sí / No |
| Justificación | <razonamiento> |

> Si la valoración da **alto riesgo**, se activa la comunicación a los interesados (§6). Si los datos estaban **cifrados de forma robusta** y las claves no se vieron comprometidas, GDPR Art. 34(3)(a) puede eximir de la comunicación individual — documentar la justificación.

---

## 5. Plantilla — Notificación a la autoridad de control (GDPR Art. 33)

> Destinatario: <SUPERVISORY_AUTHORITY>. Enviar dentro de las 72 h.

**Asunto:** Notificación de violación de seguridad de datos personales — {{PROJECT_NAME}} — <INC-XXXX>

1. **Naturaleza de la violación:** <descripción; categorías y número aproximado de interesados y de registros afectados>.
2. **Datos de contacto del DPO:** <DPO> — <correo/teléfono>.
3. **Consecuencias probables:** <descripción del impacto esperado>.
4. **Medidas adoptadas o propuestas:** <contención, mitigación, prevención de recurrencia>.
5. **Notificación por fases:** Sí / No. Si Sí: <información pendiente y fecha estimada>.

| Campo de envío | Valor |
|---|---|
| Fecha y hora de envío | YYYY-MM-DD HH:MM (TZ) |
| Dentro de plazo 72 h | Sí / No (justificar) |
| Acuse de recibo | <referencia> |

---

## 6. Plantilla — Comunicación a los titulares afectados (GDPR Art. 34 / HIPAA §164.404)

> Lenguaje claro y sencillo, sin jerga técnica. Empático y accionable.

Estimado/a usuario/a:

Le informamos de que el <YYYY-MM-DD> se produjo un incidente de seguridad que pudo afectar a los siguientes datos suyos: <categorías de datos>. 

**Qué ocurrió:** <descripción breve y honesta>.
**Qué información estuvo implicada:** <categorías>.
**Qué hemos hecho:** <medidas de contención y mitigación>.
**Qué puede hacer usted:** <recomendaciones: cambio de contraseña, vigilancia, contacto>.
**Cómo contactarnos:** <SUPPORT_CONTACT>.

Lamentamos sinceramente las molestias y mantenemos su confianza como prioridad.

| Campo de envío | Valor |
|---|---|
| Canal de comunicación | <correo / notificación in-app / aviso público> |
| Fecha de envío | YYYY-MM-DD |
| Interesados notificados | <N> |

---

## 7. Registro de cumplimiento del flujo

| Acción | Responsable | Plazo aplicable | Fecha real | En plazo |
|---|---|---|---|---|
| Detección y registro del incidente | <responsable> | Inmediato | YYYY-MM-DD | Sí / No |
| Evaluación de riesgo (§4) | <DPO> | < 72 h | YYYY-MM-DD | Sí / No |
| Notificación a la autoridad (§5) | {{OWNER}} | 72 h (GDPR) | YYYY-MM-DD | Sí / No |
| Comunicación a interesados (§6) | <DPO> | Sin demora / 60 d (HIPAA) | YYYY-MM-DD | Sí / No |
| Vínculo con post-mortem | <responsable> | Tras contención | `INCIDENT_POSTMORTEM_TEMPLATE.md` | — |

---

## 8. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
