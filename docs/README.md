# Design History File (DHF) — Índice documental

Brújula del DHF de {{PROJECT_NAME}}. El **Master Map** (`00_master/MASTER_MAP.md`) es el mapa maestro vivo; lo mantiene el agente `docs-dhf`.

| Carpeta | Contenido | Norma principal |
|---|---|---|
| `00_master/` | Master Map. | — |
| `01_governance_and_strategy/` | Visión, gobernanza, estrategia regulatoria. | ISO 13485 |
| `02_architecture_and_design/` | Arquitectura, diseño detallado. | IEC 62304 §5.3/§5.4 |
| `03_software_development_plan/` | Plan de desarrollo, estrategia de testing, protocolo de auditoría, guía de desarrollo. | IEC 62304 §5.1 |
| `05_design_decisions/` | RFCs (decisiones estructurales) + plantilla. | — |
| `06_operations_and_runbooks/` | Runbooks de deploy e incidentes. | — |
| `07_regulatory_and_compliance/` | Risk matrix ISO 14971, trazabilidad SaMD, clasificación de seguridad, SOUP, evaluación/validación clínica, post-market, IFU, etiquetado, privacidad, retención, flujo de datos, respuesta a incidentes, gestión de configuración, resolución de problemas, compliance/seguridad maestro, cómo certificar. | IEC 62304 + ISO 14971 + ISO 13485 + GDPR/HIPAA |
| `08_verification_and_audits/` | Deuda técnica (summary + history), auditorías, reportes de verificación. | IEC 62304 §5.7 |

## Regla de integridad

Tras renombrar/mover/eliminar cualquier `.md`, corré el link-checker cross-doc y resolvé los rotos en el mismo PR:

```bash
grep -rEn "\(\.{1,2}/[^)]+\.md" docs/
```

Ningún PR de reorg cierra con enlaces rotos.
