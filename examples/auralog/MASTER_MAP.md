# Master Map — AuraLog

> Mapa maestro del proyecto. **No asumir rutas; verificarlas.** Toda doc nueva, renombre o reorg se refleja acá (lo mantiene `docs-dhf`). Versión: v1.0.
>
> **Documento de EJEMPLO.** AuraLog es un dispositivo ficticio con fines didácticos. Paths y tests son ilustrativos.

## Identidad del dispositivo

| Campo | Valor |
|---|---|
| Producto | AuraLog |
| Uso previsto (Intended Use) | Aplicación para que pacientes con una condición crónica **registren y hagan seguimiento de sus síntomas** y reciban recordatorios. Genera **alertas informativas** ("consultá a tu profesional") cuando los patrones registrados cruzan umbrales configurados. NO diagnostica, NO recomienda tratamiento; las alertas son informativas y no sustituyen la valoración de un profesional de salud. |
| Clasificación SaMD | Clase B (IEC 62304 §4.3) |
| Marco regulatorio | IEC 62304 + ISO 14971 + ISO 13485 + GDPR + HIPAA + WCAG 2.1 AA |
| Stack frontend | React + TypeScript (offline-first, IndexedDB + outbox/sync) |
| Stack backend | Python + FastAPI |
| Stack datos | PostgreSQL (transaccional + auditoría) |
| Plataforma cloud | Google Cloud Platform (Cloud Run, Cloud SQL, Secret Manager, Cloud Scheduler) |

## Arquitectura (alto nivel)

```
[ Cliente React + TypeScript ]  --offline-first (outbox/sync)-->  [ IndexedDB del cliente ]
        |  (HTTP + token JWT)
        v
[ Backend Python + FastAPI ]  -->  [ PostgreSQL transaccional + auditoría ]
        |
        v
[ GCP: Cloud Run (cómputo), Secret Manager (claves), Cloud Scheduler (evaluación de umbrales), Cloud Logging (monitoring) ]
```

Flujo clínico nuclear: el paciente registra un síntoma → se persiste en IndexedDB (offline-first) → sync al backend → el **motor de alertas** (`alert_engine`) evalúa el patrón contra los umbrales configurados → si cruza un umbral, se crea una alerta informativa y se notifica al paciente. La evaluación se dispara tanto en la sincronización como en un barrido periódico de Cloud Scheduler (red de respaldo).

## Índice documental

| Carpeta | Contenido |
|---|---|
| `docs/00_master/` | Master Map, brújula documental. |
| `docs/01_governance_and_strategy/` | Visión, gobernanza, estrategia. |
| `docs/02_architecture_and_design/` | Arquitectura, diseño detallado, diagramas. |
| `docs/03_software_development_plan/` | Plan de desarrollo IEC 62304, estrategia de testing, guías. |
| `docs/04_user_documentation/` | Guía de usuario (IFU), notas de versión — documentación de cara al usuario. |
| `docs/05_design_decisions/` | RFCs (decisiones estructurales). |
| `docs/06_operations_and_runbooks/` | Runbooks de operación, deploy, incidentes. |
| `docs/07_regulatory_and_compliance/` | Matriz de riesgo ISO 14971, trazabilidad SaMD, validación clínica, IFU, post-market, SBOM, políticas. |
| `docs/08_verification_and_audits/` | Deuda técnica, historia de deuda, auditorías, reportes de verificación. |
| `docs/09_engineering_experience/` | Lecciones de producción, arquitectura de referencia, método multi-agente (capa de experiencia). |

## Módulos clínicos críticos

> Listá acá los módulos cuyo fallo tiene impacto clínico (motor de alertas, scheduler de evaluación, dispatcher de notificaciones, motor de sync…). Cada uno debe tener fail-safe explícito + entrada en la Risk Matrix + cobertura de tests verificada.

| Módulo | Path | Riesgo asociado | Control |
|---|---|---|---|
| Motor de alertas (evaluación de umbrales) | `app/services/alert_engine.py` | R001 | Si la evaluación falla, registra el error y reintenta en el siguiente barrido; nunca descarta silenciosamente un síntoma sin evaluar. |
| Validador de configuración de umbrales | `app/services/threshold_config.py` | R002 | Rechaza umbrales fuera de rango clínico plausible; valor inválido → conserva el umbral seguro previo y avisa. |
| Dispatcher de notificaciones de alerta | `app/services/alert_dispatcher.py` | R003 | Reintentos con backoff + cola persistente; alerta no entregada se reencola, no se pierde. |
| Barrido periódico de evaluación (red de respaldo) | `app/jobs/scheduled_evaluation.py` | R001 | Cloud Scheduler reevalúa registros pendientes cada N min por si la evaluación en-sync no corrió. |
| Motor de sincronización offline-first | `app/services/sync_service.py` | R004 | Outbox idempotente; un registro sin sincronizar no se borra del cliente hasta confirmar persistencia en el servidor. |
| Cifrado de datos de salud en reposo | `app/models/types.py` (`EncryptedString`) | R005 | AES-256-GCM con clave gestionada en Secret Manager; PHI nunca en claro en BD ni en logs. |

## Registro de versiones de docs

| Doc | Versión | Última actualización |
|---|---|---|
| MASTER_MAP | v1.0 | 2026-06-28 |
| SOFTWARE_SAFETY_CLASSIFICATION | v1.0 | 2026-06-28 |
| ISO_14971_RISK_MATRIX | v1.0 | 2026-06-28 |
| TRACEABILITY_MATRIX_SAMD | v1.0 | 2026-06-28 |
