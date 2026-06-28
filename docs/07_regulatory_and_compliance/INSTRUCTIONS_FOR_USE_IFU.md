# Instrucciones de Uso (IFU)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** YYYY-MM-DD

> Documento plantilla del SaMD Starter Kit. Las Instrucciones de Uso son información suministrada por el fabricante (MDR Anexo I §23). Redáctelas en lenguaje claro para el usuario previsto; reemplace los marcadores y filas-placeholder.

---

## 1. Identificación del producto

| Campo | Valor |
|---|---|
| Nombre del producto | {{PROJECT_NAME}} |
| Versión del software | `<vX.Y.Z>` |
| Fabricante / responsable | {{OWNER}} |
| Clase SaMD | {{SAMD_CLASS}} |
| Identificador único del dispositivo (UDI-DI) | `<UDI>` |
| Idioma de estas instrucciones | {{CHAT_LANG}} |

---

## 2. Uso previsto

{{INTENDED_USE}}

| Atributo | Descripción |
|---|---|
| Usuario previsto | `<paciente / profesional / cuidador>` |
| Población diana | `<...>` |
| Entorno de uso | `<domiciliario / clínico>` |
| Función clínica | `<informar / impulsar / apoyar la gestión>` |

---

## 3. Contraindicaciones

`<Situaciones en las que el producto NO debe utilizarse.>`

- `<contraindicación 1>`
- `<contraindicación 2>`

---

## 4. Advertencias y precauciones

> ⚠️ **Advertencia:** {{PROJECT_NAME}} no sustituye el juicio clínico profesional ni la atención médica de urgencia. En caso de emergencia, contacte a los servicios de emergencia locales.

| Tipo | Mensaje |
|---|---|
| Advertencia | `<...>` |
| Precaución | `<...>` |
| Nota de seguridad | `<comportamiento fail-safe ante fallo de red/servidor: el sistema degrada de forma segura y avisa al usuario>` |

---

## 5. Instrucciones paso a paso

### 5.1 Primer uso / configuración
1. `<paso>`
2. `<paso>`

### 5.2 Uso habitual
1. `<paso>`
2. `<paso>`

### 5.3 Interpretación de resultados / salidas
`<Explicar qué significan las salidas y qué NO significan. Recordar las limitaciones del uso previsto.>`

### 5.4 Qué hacer ante un error
`<Mensajes de error esperados, en lenguaje no técnico, y la acción recomendada. Nunca se muestran trazas técnicas al usuario.>`

---

## 6. Requisitos del sistema

| Componente | Requisito mínimo |
|---|---|
| Cliente / frontend | {{FRONTEND_STACK}} — `<navegador / SO / versión mínima>` |
| Conectividad | `<requisitos de red; comportamiento sin conexión si aplica>` |
| Servidor / backend | {{BACKEND_STACK}} (gestionado por el fabricante) |
| Almacenamiento de datos | {{DB_STACK}} — `<cifrado en reposo>` |
| Infraestructura | {{CLOUD_STACK}} |

---

## 7. Seguridad y privacidad de datos

- Los datos personales y de salud se tratan conforme a `<GDPR / HIPAA / normativa aplicable>`.
- Cifrado en tránsito (TLS) y en reposo.
- `<Política de retención y derechos del usuario: acceso, rectificación, supresión.>`

---

## 8. Soporte y contacto

| Canal | Detalle |
|---|---|
| Soporte técnico | `<email / formulario>` |
| Reporte de incidentes de seguridad | `<email>` |
| Fabricante | {{OWNER}} — `<dirección>` |

---

## 9. Símbolos utilizados

Conforme a **ISO 15223-1** y **EN ISO 20417**.

| Símbolo | Significado |
|---|---|
| 🏭 / *factory* | Fabricante |
| 📅 / *date* | Fecha de fabricación / versión |
| 📖 / *book* | Consulte las instrucciones de uso |
| UDI | Identificador único del dispositivo |
| ⚠️ | Advertencia / precaución |
| MD | Dispositivo médico (*Medical Device*) |

> Reemplace por los pictogramas oficiales ISO 15223-1 en el material publicado.

---

## 10. Control de cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | `<autor>` | Creación de la plantilla |

---

## 11. Referencias normativas

- MDR (UE) 2017/745 Anexo I §23 — Información suministrada por el fabricante.
- ISO 15223-1 — Símbolos para etiquetas de productos sanitarios.
- EN ISO 20417 — Información suministrada por el fabricante.
- IEC 62366-1 — Ingeniería de usabilidad.
- IEC 62304 §5.1 — Documentación del software.
