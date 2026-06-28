# Política de Retención de Datos

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla. Ajuste plazos, categorías y bases legales a la realidad del proyecto y a la legislación aplicable antes de su aprobación.

---

## 1. Propósito

Definir cuánto tiempo se conserva cada categoría de datos de **{{PROJECT_NAME}}**, cuándo y cómo se borran o anonimizan, y la base legal de cada plazo. Cumple el principio de **limitación del plazo de conservación** (GDPR Art. 5(1)(e)) y HIPAA §164.316(b)(2).

---

## 2. Principios

1. **Minimización temporal:** se conserva solo el tiempo necesario para la finalidad.
2. **Borrado o anonimización al vencimiento** del plazo, salvo obligación legal de conservación.
3. **Trazabilidad:** cada borrado masivo programado se registra.

---

## 3. Categorías de datos y plazos

| Categoría | Plazo de retención | Acción al vencer | Base legal |
|---|---|---|---|
| Datos de cuenta / identificación | {{placeholder}} | Borrado | GDPR Art. 5(1)(e); contrato |
| Datos de salud (PHI) | {{placeholder}} | Borrado / anonimización | GDPR Art. 9; HIPAA §164.316 |
| Registros de auditoría (mutaciones) | {{placeholder, p. ej. 6 años}} | Borrado | HIPAA §164.316(b)(2); IEC 62304 §5.7 |
| Logs técnicos (sin PII) | {{placeholder, p. ej. 14–90 días}} | Borrado | Interés legítimo; seguridad |
| Backups | {{placeholder}} | Rotación / expiración | GDPR Art. 32; continuidad |
| Datos de soporte / incidencias | {{placeholder}} | Borrado | Interés legítimo |
| Consentimientos | Mientras dure el tratamiento + {{placeholder}} | Archivo / borrado | GDPR Art. 7(1) (prueba del consentimiento) |

---

## 4. Borrado y anonimización

- **Borrado:** eliminación física o criptográfica (destrucción de la clave de cifrado de la columna/registro).
- **Anonimización:** transformación irreversible que impide reidentificar al titular; los datos anonimizados quedan fuera del ámbito del GDPR.
- **Solicitudes del titular (Art. 17):** se ejecutan en el plazo de 1 mes, salvo excepción legal documentada.

---

## 5. Excepciones y bloqueos legales

Cuando exista una obligación legal de conservación o un litigio en curso (legal hold), el dato se bloquea en lugar de borrarse y se documenta el motivo y la duración esperada.

---

## 6. Verificación

| Control | Mecanismo | Frecuencia |
|---|---|---|
| Job de borrado programado | `{{archivo:línea}}` | {{placeholder}} |
| Revisión de cumplimiento de plazos | Auditoría interna | {{placeholder}} |

---

## 7. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |
