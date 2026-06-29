# Cómo contribuir — {{PROJECT_NAME}}

**[English](CONTRIBUTING.md) · Español**

> Bienvenido. Este proyecto es **Software as a Medical Device (SaMD) Clase {{SAMD_CLASS}}** bajo IEC 62304 + ISO 14971. El proceso de cambios está controlado y es **evidencia regulatoria** (IEC 62304 §5/§8): no es burocracia, es lo que permite certificar. Esta página es la puerta de entrada; el detalle vive en los documentos enlazados abajo.

## Las reglas no negociables

1. **Nadie commitea ni pushea sin OK explícito del dueño ({{OWNER}}).** Antes de cada commit se reporta qué archivos suben y se espera autorización. Operaciones destructivas (`reset --hard`, `push --force`, borrar branches) piden OK aparte.
2. **Tests verdes con números reportados.** Nada se declara "hecho" sin correr los tests vinculados al cambio y reportar los resultados (SaMD §5.7). "Renderiza sin crashear" no es un test válido.
3. **El usuario nunca ve un traceback.** Errores en pantalla: mensajes empáticos + código HTTP correcto. Un usuario en crisis no debe ver "500 Internal Server Error".
4. **Trazabilidad en el MISMO PR.** Si tocás algoritmo clínico, schema, regla de negocio o flujo de seguridad, actualizás el DHF (TECHNICAL_DEBT_SUMMARY + Master Map + Risk Matrix / TRACEABILITY si aplica) en el mismo PR, no en un sprint aparte.
5. **Identidad solo del token.** Nunca aceptar `user_id` desde body, query ni headers — solo del token decodificado.
6. **Análisis de impacto antes de declarar "arreglado".** Revisá TODOS los consumidores del símbolo que tocaste (`grep` global), no solo el archivo donde se reportó el bug.

## Flujo de trabajo

```
1. Rama desde tu rama por defecto:  git switch -c feat/mi-cambio
2. Implementá + tests      (delegá a los agentes de .claude/agents/ cuando encaje la capa)
3. CI local en verde:      bash scripts/run_local_ci.sh
4. Reportá los archivos a commitear y esperá el OK del dueño
5. Abrí el PR; el CI corre lint + types + tests + drift de contrato + trazabilidad
6. Antes de cerrar bloque grande: bash scripts/audit_project_state.sh
```

## Definition of Done

1. Pasa linting + CI local (`scripts/run_local_ci.sh`).
2. Tests vinculados verdes, números reportados.
3. Se redujo deuda técnica en al menos un punto (Boy Scout).
4. Documentación al día (Master Map, TECHNICAL_DEBT, TRACEABILITY, y Risk Matrix si aplica).
5. UI accesible (contraste WCAG AA, diseño plano, modales canónicos).
6. Cambio comunicado al dueño con genealogía clara y autorizado explícitamente.

## Documentos de referencia

- **`CLAUDE.md`** — reglamento del agente: Regla 0, estándares de backend/frontend, orquestación multi-agente, testing.
- **`.agents/workflows/protocolo_desarrollo.md`** — el proceso de desarrollo estable, agnóstico al agente.
- **`docs/03_software_development_plan/DEVELOPMENT_GUIDE_COMPLETE.md`** — guía completa: setup, comandos, estándares, flujo de PR.
- **`docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md`** — estrategia de verificación SaMD-grade.
- **`docs/03_software_development_plan/AUDIT_PROTOCOL.md`** — cómo se audita un changeset/fase contra SaMD.
- **`docs/05_design_decisions/RFC-TEMPLATE.md`** — plantilla para proponer una decisión estructural.

## Reportar un problema de seguridad

Las vulnerabilidades NO se reportan en issues públicos. Contactá en privado a {{OWNER}}. Ver `docs/07_regulatory_and_compliance/INCIDENT_RESPONSE_PLAN.md`.
