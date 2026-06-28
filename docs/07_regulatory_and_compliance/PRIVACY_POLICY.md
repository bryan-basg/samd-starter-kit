# Política de Privacidad

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla. Sustituya los marcadores `{{...}}` y las filas-placeholder por la información real antes de su publicación. Esta política debe ser revisada por asesoría legal antes de su entrada en vigor.

---

## 1. Responsable del tratamiento

- **Responsable:** {{OWNER}}
- **Producto:** {{PROJECT_NAME}}
- **Datos de contacto:** {{placeholder: dirección postal, email}}
- **Delegado de Protección de Datos (DPO):** {{placeholder: nombre, email}}

---

## 2. Datos que recolectamos

| Categoría | Ejemplos | Origen | ¿Datos especiales (Art. 9 GDPR)? |
|---|---|---|---|
| Identificación | {{placeholder}} | Titular | No |
| Contacto | {{placeholder}} | Titular | No |
| Datos de salud (PHI) | {{placeholder}} | Titular / uso del producto | Sí (Art. 9 GDPR) |
| Datos de uso técnico | {{placeholder}} | Automático | No |
| Identificadores de dispositivo | {{placeholder}} | Automático | No |

Los datos de salud se tratan como **categoría especial** bajo el Art. 9 GDPR y como PHI bajo HIPAA, con salvaguardas reforzadas (cifrado AES-256-GCM en reposo, acceso de mínimo privilegio).

---

## 3. Finalidades y base legal (GDPR Art. 6 y Art. 9)

| Finalidad | Base legal (Art. 6) | Base para datos especiales (Art. 9) |
|---|---|---|
| Prestación del servicio | Art. 6(1)(b) ejecución de contrato | Art. 9(2)(a) consentimiento explícito |
| Seguridad y prevención de fraude | Art. 6(1)(f) interés legítimo | — |
| Obligaciones legales/regulatorias | Art. 6(1)(c) obligación legal | Art. 9(2)(h)/(i) fines sanitarios |
| Mejora del producto (datos agregados/anonimizados) | Art. 6(1)(f) interés legítimo | No aplica (anonimizados) |

---

## 4. Derechos del titular (GDPR Art. 15–22)

El titular puede ejercer, sin coste y en cualquier momento:

- **Acceso** (Art. 15)
- **Rectificación** (Art. 16)
- **Supresión / "derecho al olvido"** (Art. 17)
- **Limitación del tratamiento** (Art. 18)
- **Portabilidad** (Art. 20)
- **Oposición** (Art. 21)
- **No ser objeto de decisiones automatizadas** (Art. 22)
- **Retirar el consentimiento** en cualquier momento (Art. 7(3))

Solicitudes a: {{placeholder: email DPO}}. Plazo de respuesta: **1 mes** (Art. 12(3)), prorrogable a 3 meses en casos complejos.

---

## 5. Conservación de los datos

Los plazos de retención se detallan en `DATA_RETENTION_POLICY.md`. Como principio general, los datos se conservan solo durante el tiempo necesario para las finalidades descritas y las obligaciones legales aplicables.

---

## 6. Transferencias y encargados del tratamiento

| Encargado / Destinatario | Finalidad | Ubicación | Garantía de transferencia |
|---|---|---|---|
| {{CLOUD_STACK}} | Alojamiento / procesamiento | {{placeholder}} | {{placeholder: SCC / adecuación Art. 45–46}} |
| {{placeholder}} | {{placeholder}} | {{placeholder}} | {{placeholder}} |

Las transferencias internacionales fuera del EEE se amparan en decisiones de adecuación (Art. 45) o cláusulas contractuales tipo (Art. 46). Cuando aplique HIPAA, los encargados firman un Business Associate Agreement (BAA).

---

## 7. Seguridad de los datos

Aplicamos medidas técnicas y organizativas (GDPR Art. 32): cifrado en tránsito (TLS 1.2+) y en reposo (AES-256-GCM), control de acceso de mínimo privilegio, registro de auditoría sin PII y gestión de secretos. Ver `COMPLIANCE_AND_SECURITY_MASTER.md`.

---

## 8. Menores

{{placeholder: política sobre menores de edad y, en su caso, consentimiento parental conforme al Art. 8 GDPR.}}

---

## 9. Cambios en esta política

Notificaremos cambios sustanciales por {{placeholder: canal}}. La fecha de la última actualización figura en el encabezado.

---

## 10. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |
