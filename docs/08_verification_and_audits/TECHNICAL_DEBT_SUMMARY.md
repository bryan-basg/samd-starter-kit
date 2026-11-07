# Resumen de Deuda Técnica (DHF)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Fecha:** YYYY-MM-DD

> Registro vivo de deuda técnica con trazabilidad SaMD (IEC 62304 §5.1/§5.7). Cada entrada usa el código `D-XXX-NN` (`XXX` = scope, `NN` = secuencial). Mantenido por `docs-dhf`. Las deudas cerradas se mueven a `TECHNICAL_DEBT_HISTORY.md` (no se borran).

## Convención de códigos

| Scope | Significado |
|---|---|
| `D-DB-*` | Datos / schema / pool / migraciones. |
| `D-SEC-*` | Seguridad / cifrado / auth / audit. |
| `D-MUT-*` | Mutation testing. |
| `D-UX-*` | Neuro-UX / accesibilidad. |
| `D-DEPLOY-*` | Deploy / migraciones en prod. |
| `D-AUTH-*` | Identidad / lookup de sujetos. |
| `D-AI-*` | IA / validador / fail-safe. |

## Deudas abiertas

Cada fila declara su **cubo** — la pregunta que lo decide es *«si esto sigue roto un año, ¿alguien sale perjudicado, o solo el código es más feo?»*:

| Cubo | Qué es | Cuenta como deuda |
|---|---|---|
| 🔴 | Daña a un paciente, expone o pierde datos, o impide usar la app. | Sí — **meta: cero abiertas**. |
| 🟡 | Incumple un requisito de certificación (WCAG, GDPR, ISO 14971, trazabilidad). | Sí — **meta: cero abiertas antes de certificar**. |
| 🧊 | Calidad interna o producto sin decidir. | **No es deuda**: va a un backlog aparte, no a esta tabla. |

> La **severidad** (Crítica/Alta/Media/Baja) NO dice el cubo: una «Media» puede ser 🔴 y una «Alta» puede ser 🧊. Sin cubo declarado, una auditoría vuelca casi todo en 🔴 y la tabla pierde la señal de lo que de verdad urge (ver skill `/ola-auditoria`).

| Código | Cubo | Descripción | Impacto SaMD | Severidad | Riesgo asociado | Estado |
|---|---|---|---|---|---|---|
| D-XXX-01 | 🔴/🟡 | <descripción concreta con `archivo:línea`> | <§5.x / control de riesgo> | <Crítica/Alta/Media/Baja> | R-XXX-NN | Abierta |

## Deudas cerradas recientes

| Código | Cómo se cerró | Commit/PR | Fecha |
|---|---|---|---|
| <—> | <—> | <—> | YYYY-MM-DD |

> Al cerrar una deuda: estado `✅ CERRADA` + fecha + commit; mover a `TECHNICAL_DEBT_HISTORY.md`; si afectaba un control de riesgo, actualizar `ISO_14971_RISK_MATRIX.md`; si tenía REQ asociado, validar TRACEABILITY.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
