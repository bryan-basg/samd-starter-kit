# Master Map — {{PROJECT_NAME}}

> Mapa maestro del proyecto. **No asumir rutas; verificarlas.** Toda doc nueva, renombre o reorg se refleja acá (lo mantiene `docs-dhf`). Versión: vX.Y.

## Identidad del dispositivo

| Campo | Valor |
|---|---|
| Producto | {{PROJECT_NAME}} |
| Uso previsto (Intended Use) | {{INTENDED_USE}} |
| Clasificación SaMD | Clase {{SAMD_CLASS}} (IEC 62304 §4.3) |
| Marco regulatorio | IEC 62304 + ISO 14971 + ISO 13485 + GDPR + HIPAA + WCAG 2.1 AA |
| Stack frontend | {{FRONTEND_STACK}} |
| Stack backend | {{BACKEND_STACK}} |
| Stack datos | {{DB_STACK}} |
| Plataforma cloud | {{CLOUD_STACK}} |

## Arquitectura (alto nivel)

```
[ Cliente {{FRONTEND_STACK}} ]  --offline-first (outbox/sync)-->  [ BD del cliente ]
        |  (HTTP + token)
        v
[ Backend {{BACKEND_STACK}} ]  -->  [ {{DB_STACK}} transaccional + auditoría ]
        |
        v
[ {{CLOUD_STACK}}: cómputo, secretos, scheduler, IA, monitoring ]
```

## Índice documental

| Carpeta | Contenido |
|---|---|
| `docs/00_master/` | Master Map, brújula documental. |
| `docs/01_governance_and_strategy/` | Visión, gobernanza, estrategia. |
| `docs/02_architecture_and_design/` | Arquitectura, diseño detallado, diagramas. |
| `docs/03_software_development_plan/` | Plan de desarrollo IEC 62304, estrategia de testing, guías. |
| `docs/05_design_decisions/` | RFCs (decisiones estructurales). |
| `docs/06_operations_and_runbooks/` | Runbooks de operación, deploy, incidentes. |
| `docs/07_regulatory_and_compliance/` | Matriz de riesgo ISO 14971, trazabilidad SaMD, validación clínica, IFU, post-market, SBOM, políticas. |
| `docs/08_verification_and_audits/` | Deuda técnica, historia de deuda, auditorías, reportes de verificación. |
| `docs/09_engineering_experience/` | Lecciones de producción, arquitectura de referencia, método multi-agente (capa de experiencia). |

## Módulos clínicos críticos

> Listá acá los módulos cuyo fallo tiene impacto clínico (motor de riesgo, crisis, scheduler, dispatcher, validador de IA…). Cada uno debe tener fail-safe explícito + entrada en la Risk Matrix + cobertura de tests verificada.

| Módulo | Path | Riesgo asociado | Control |
|---|---|---|---|
| <ejemplo> | `app/services/<...>` | R-XXX-NN | <fail-safe> |

## Registro de versiones de docs

| Doc | Versión | Última actualización |
|---|---|---|
| MASTER_MAP | vX.Y | YYYY-MM-DD |
| ISO_14971_RISK_MATRIX | vX.Y | YYYY-MM-DD |
| TRACEABILITY_MATRIX_SAMD | vX.Y | YYYY-MM-DD |
