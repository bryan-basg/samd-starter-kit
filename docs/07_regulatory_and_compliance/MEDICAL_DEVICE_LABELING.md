# Etiquetado del Dispositivo Médico

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** YYYY-MM-DD

> Documento plantilla del SaMD Starter Kit. Define los elementos de etiqueta y las reglas de claims permitidos/no permitidos. Para software, la "etiqueta" incluye pantallas de información del producto (acerca de, splash, pie de página). Reemplace los marcadores y filas-placeholder.

---

## 1. Identificación

| Campo | Valor |
|---|---|
| Producto | {{PROJECT_NAME}} |
| Fabricante / responsable | {{OWNER}} |
| Clase SaMD | {{SAMD_CLASS}} |
| Uso previsto | {{INTENDED_USE}} |
| Marco normativo | MDR (UE) 2017/745 Anexo I §23 · ISO 15223-1 · EN ISO 20417 · Reglamento UDI |

---

## 2. Elementos obligatorios de la etiqueta

| # | Elemento | Fuente / valor | Símbolo ISO 15223-1 | Ubicación en el software |
|---|---|---|---|---|
| 1 | Nombre del producto | {{PROJECT_NAME}} | — | `<splash / acerca de>` |
| 2 | Nombre y dirección del fabricante | {{OWNER}} | 🏭 *manufacturer* (5.1.1) | `<acerca de>` |
| 3 | Versión del software | `<vX.Y.Z>` | — | `<acerca de / pie>` |
| 4 | UDI (UDI-DI + UDI-PI) | `<UDI>` | UDI carrier (5.7.x) | `<acerca de>` |
| 5 | Indicación de dispositivo médico | `<...>` | MD (5.7.7) | `<acerca de>` |
| 6 | "Consulte las instrucciones de uso" | `INSTRUCTIONS_FOR_USE_IFU.md` | 📖 (5.4.3) | `<acerca de>` |
| 7 | Fecha de fabricación / liberación | YYYY-MM-DD | 📅 (5.1.3) | `<acerca de>` |
| 8 | Identificador del lote/build | `<build id>` | LOT (5.1.5) | `<acerca de>` |
| 9 | Advertencias y precauciones clave | `<...>` | ⚠️ (5.4.4) | `<...>` |
| 10 | Marcado de conformidad (cuando certificado) | `<CE / nº organismo notificado>` | CE | `<acerca de>` |

> La UDI debe registrarse en la base de datos correspondiente (EUDAMED / GUDID) cuando proceda.

---

## 3. Símbolos ISO 15223-1 aplicables

| Cláusula | Símbolo | Significado |
|---|---|---|
| 5.1.1 | Fabricante | Identifica al fabricante |
| 5.1.3 | Fecha de fabricación | Versión / build |
| 5.1.5 | Código de lote | Identificador de build |
| 5.4.3 | Consulte las IFU | Remite al usuario a las instrucciones |
| 5.4.4 | Advertencia / precaución | Riesgo a tener en cuenta |
| 5.7.7 | Dispositivo médico (MD) | Indica que el producto es un dispositivo médico |
| 5.7.10 | Traductor / contenido electrónico | `<si aplica>` |

---

## 4. Claims permitidos vs. NO permitidos (pre-certificación)

> Regla dura: **antes de obtener la certificación/marcado correspondiente, está PROHIBIDO afirmar función de dispositivo médico.** El lenguaje del producto no debe declarar diagnóstico, tratamiento ni prevención de enfermedad.

### 4.1 Claims NO permitidos (pre-certificación)

| Claim prohibido | Por qué | Reemplazo permitido |
|---|---|---|
| "diagnostica `<X>`" | Afirma función diagnóstica no certificada | "ayuda a registrar / organizar información sobre `<X>`" |
| "trata / cura `<X>`" | Afirma función terapéutica | "acompaña / apoya la gestión de `<X>`" |
| "dispositivo médico certificado" (sin serlo) | Falso claim regulatorio | `<omitir hasta certificar>` |
| "clínicamente probado" (sin evidencia) | Sin respaldo del CER | `<omitir o citar evidencia real>` |
| "sustituye al profesional de salud" | Riesgo de seguridad | "complementa, no sustituye, la atención profesional" |

### 4.2 Claims permitidos

| Claim permitido | Condición |
|---|---|
| `<descripción funcional neutra del producto>` | Siempre |
| "herramienta de apoyo / organización" | Siempre |
| "los resultados no constituyen un diagnóstico médico" | Disclaimer recomendado |
| Claims de función de dispositivo médico | **Solo tras certificación**, dentro del uso previsto autorizado |

### 4.3 Disclaimer legal canónico

> "{{PROJECT_NAME}} es una herramienta de apoyo y no reemplaza la valoración, el diagnóstico ni el tratamiento de un profesional de la salud. Ante una emergencia, contacte a los servicios de emergencia."

Los disclaimers legales están **exentos** de la restricción de glosario y deben permanecer claros y visibles.

---

## 5. Etiquetado electrónico (eIFU)

Si las instrucciones se suministran en formato electrónico, cumplir el **Reglamento (UE) 2021/2226** (eIFU): disponibilidad, soporte alternativo bajo solicitud, y trazabilidad de versiones.

| Requisito eIFU | Cumplimiento |
|---|---|
| Acceso a las IFU desde el producto | `<sí/no>` |
| IFU en papel bajo solicitud | `<sí/no — plazo>` |
| Indicación de versión y fecha | `<sí/no>` |

---

## 6. Verificación del etiquetado

| Verificación | Responsable | Resultado | Fecha |
|---|---|---|---|
| Todos los elementos obligatorios presentes | `<rol>` | `<OK/NOK>` | YYYY-MM-DD |
| Símbolos conformes a ISO 15223-1 | `<rol>` | `<OK/NOK>` | YYYY-MM-DD |
| Ausencia de claims no permitidos | `<rol>` | `<OK/NOK>` | YYYY-MM-DD |
| Disclaimer presente y visible | `<rol>` | `<OK/NOK>` | YYYY-MM-DD |

---

## 7. Control de cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | `<autor>` | Creación de la plantilla |

---

## 8. Referencias normativas

- MDR (UE) 2017/745 Anexo I §23 — Etiqueta e instrucciones de uso.
- ISO 15223-1 — Símbolos a utilizar en etiquetas de productos sanitarios.
- EN ISO 20417 — Información suministrada por el fabricante.
- Reglamento (UE) 2021/2226 — Instrucciones de uso en formato electrónico.
- Reglamento de implementación (UE) sobre sistema UDI.
- FDA 21 CFR Part 801 / UDI Rule — referencia para mercado estadounidense.
