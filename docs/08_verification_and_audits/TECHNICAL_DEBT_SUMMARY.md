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

| Código | Descripción | Impacto SaMD | Severidad | Riesgo asociado | Estado |
|---|---|---|---|---|---|
| D-XXX-01 | <descripción concreta con `archivo:línea`> | <§5.x / control de riesgo> | <Crítica/Alta/Media/Baja> | R-XXX-NN | Abierta |

## Deudas cerradas recientes

| Código | Cómo se cerró | Commit/PR | Fecha |
|---|---|---|---|
| <—> | <—> | <—> | YYYY-MM-DD |

> Al cerrar una deuda: estado `✅ CERRADA` + fecha + commit; mover a `TECHNICAL_DEBT_HISTORY.md`; si afectaba un control de riesgo, actualizar `ISO_14971_RISK_MATRIX.md`; si tenía REQ asociado, validar TRACEABILITY.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
