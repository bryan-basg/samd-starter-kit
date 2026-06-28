# Inventario de Módulos Críticos y Clasificación de Seguridad

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

> Inventario que clasifica cada módulo de software por **clase de seguridad (A/B/C)** según **IEC 62304 §4.3** y fija el **rigor de testing y mutation** exigible a cada clase (§5.3). La clasificación se justifica por la peor consecuencia posible de un fallo del módulo, **antes** de medidas externas de control de riesgo. Un módulo sin clase asignada se trata como **Clase C** hasta demostrar lo contrario.

---

## 1. Criterio de clasificación (IEC 62304 §4.3)

| Clase | Definición (consecuencia de un fallo del software) |
|---|---|
| A | No puede contribuir a una situación peligrosa, o la contribución no resulta en daño. |
| B | Puede contribuir a una situación peligrosa que resulta en daño **no serio**. |
| C | Puede contribuir a una situación peligrosa que resulta en daño **serio o muerte**. |

**Regla de segregación:** si un módulo de clase inferior puede afectar a uno de clase superior sin una barrera demostrada (segregación de software), hereda la clase superior.

---

## 2. Umbrales de rigor por clase

| Clase | Cobertura de tests | Mutation score | Revisión | Verificación adversarial | Fail-safe obligatorio |
|---|---|---|---|---|---|
| A | ≥ <COV_A>% | No exigido | Estándar | No | Recomendado |
| B | ≥ <COV_B>% | ≥ <MUT_B>% | Doble | Recomendada | Sí |
| C | ≥ <COV_C>% | ≥ <MUT_C>% | Doble + auditoría | Obligatoria | Sí, verificado |

> Los valores `{{COV_*}}` / `{{MUT_*}}` se fijan en el plan de testing del proyecto (la **fuente de verdad es la config de la herramienta**, no esta tabla; aquí se cita el umbral acordado). Un módulo clínico o de seguridad NUNCA baja de su umbral sin justificación documentada en `TECHNICAL_DEBT_SUMMARY.md`.

---

## 3. Inventario de módulos

| ID | Módulo / componente | Ruta (`archivo`) | Responsabilidad | Clase (A/B/C) | Justificación de clase | Riesgos asociados | Umbral testing | Estado |
|---|---|---|---|---|---|---|---|---|
| MOD-01 | <ej. motor de evaluación clínica> | `app/services/<...>.py` | <qué hace> | C | Un fallo puede contribuir a daño serio (no detecta riesgo). | R001, R005 | Cov ≥ <COV_C>% / Mut ≥ <MUT_C>% | Verificado |
| MOD-02 | <ej. autenticación / identidad> | `app/dependencies.py` | <qué hace> | C | Un fallo expone PHI de otro titular (IDOR). | R002, R-SEC-01 | Cov ≥ <COV_C>% / Mut ≥ <MUT_C>% | Verificado |
| MOD-03 | <ej. motor de notificaciones> | `app/services/<...>.py` | <qué hace> | B | Un fallo retrasa un aviso; daño no serio. | R-NOTIF-01 | Cov ≥ <COV_B>% / Mut ≥ <MUT_B>% | Implementado |
| MOD-04 | <ej. capa de sincronización offline> | `frontend/src/<...>.ts` | <qué hace> | B | Pérdida temporal de datos del usuario; recuperable. | R-SYNC-01 | Cov ≥ <COV_B>% / Mut ≥ <MUT_B>% | Implementado |
| MOD-05 | <ej. panel de ajustes visuales> | `frontend/src/<...>.tsx` | <qué hace> | A | Un fallo no produce daño; solo inconveniente. | — | Cov ≥ <COV_A>% | Verificado |
| MOD-06 | <ej. middleware de auditoría> | `app/middleware/<...>.py` | <qué hace> | B | Un fallo impide reconstruir un evento; sin daño directo. | R-SEC-02 | Cov ≥ <COV_B>% / Mut ≥ <MUT_B>% | Implementado |

---

## 4. Análisis de segregación

Módulos de clase inferior que tocan datos o flujos de un módulo de clase superior, y la barrera que justifica no heredar la clase.

| Módulo inferior | Módulo superior afectado | Barrera de segregación (`archivo:línea`) | ¿Hereda clase? |
|---|---|---|---|
| MOD-0X | MOD-0Y | `<...>` | No / Sí |

---

## 5. Módulos por debajo de su umbral (deuda activa)

| Módulo | Clase | Umbral exigido | Valor actual | Causa | Plan de remediación | Fecha objetivo |
|---|---|---|---|---|---|---|
| MOD-0X | <A/B/C> | <umbral> | <valor> | <causa> | <plan> | YYYY-MM-DD |

---

## 6. Mantenimiento del inventario

- Todo módulo nuevo se clasifica **antes** de su primer release.
- Un cambio que eleve la consecuencia de fallo de un módulo (nuevo flujo clínico, acceso a PHI) **re-clasifica** el módulo y dispara revisión de umbrales en la misma pasada (IEC 62304 §5.6).
- La revisión periódica del inventario se sincroniza con la revisión de `ISO_14971_RISK_MATRIX.md`.

---

## 7. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
