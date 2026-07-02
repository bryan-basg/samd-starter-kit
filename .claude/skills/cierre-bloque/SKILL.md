---
name: cierre-bloque
description: Checklist canónico de cierre de un bloque grande (sprint/fase) — foto del estado + actualizar los documentos DHF + link-checker. Úsala cuando el usuario quiera declarar cerrado un sprint, fase o bloque grande de trabajo, antes de dar por "verde" o "terminado" cualquier entrega de ese tamaño.
---

# cierre-bloque — Checklist de cierre de bloque grande

Sos el que cierra un **bloque grande** (sprint, fase) del proyecto {{PROJECT_NAME}}. **NO declares cerrado sin la foto de estado.**

## Cuándo usarla

- El usuario pide cerrar/dar por terminado un sprint, fase o bloque grande de trabajo.
- Antes de declarar "verde" o "listo" una entrega que tocó varios archivos o varias sesiones.
- Cuando hay sospecha de que quedó trabajo o deuda vivo en ramas, stashes o worktrees sin fusionar.
- Tras una reorganización de documentación (mover/renombrar `.md`) que podría haber roto enlaces cruzados.

## Procedimiento

1. **Foto del estado OBLIGATORIA**: `bash scripts/audit_project_state.sh` — barre los rincones donde se esconde trabajo y deuda (ramas sin mergear, ramas solo-en-disco, stashes, worktrees, cambios sin commitear, deuda abierta, enlaces rotos). Resolvé o anotá lo **VIVO** antes de cerrar; el desfase entre "lo que creemos hecho" y "lo que está en la rama principal/producción" es la fuga real. El script solo INFORMA — borrar/archivar algo es una decisión destructiva que requiere el OK de {{OWNER}}.

2. **Patrón canónico de cierre — actualizá**: `TECHNICAL_DEBT_SUMMARY` + Master Map + `ISO_14971_RISK_MATRIX` (si el bloque tocó producto: algoritmo clínico, schema, regla de negocio o seguridad) y cualquier plan/guide/RFC que el bloque haya vuelto obsoleto.

3. **Link-checker cross-doc** tras mover/renombrar cualquier `.md`: `grep -rEn "\(\.{1,2}/[^)]+\.md" docs/` y resolver los rotos en el mismo PR → **0 broken**. Una reorg de documentación no muestra sus propios enlaces rotos en el archivo que tocaste — hace falta el barrido global sobre todo `docs/` para verlos.

4. **Cerrá con números reales** (tests, coverage) — no se declara "verde" sin haber corrido los tests vinculados al bloque y reportado los números (consecuencia directa de la verificación obligatoria de IEC 62304 §5.7).

Regla de fondo: el costo de un cierre mal hecho no es el bloque en sí, es la próxima persona (o el próximo yo) que asume que algo está en la rama principal/producción cuando en realidad quedó vivo en una rama, un stash o un doc desactualizado. La foto de estado existe para que esa fuga no dependa de la memoria de nadie.
