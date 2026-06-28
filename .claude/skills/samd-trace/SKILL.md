---
name: samd-trace
description: Análisis de impacto SaMD §5.6 — busca consumidores de un símbolo/archivo y propone tests a correr antes de declarar verde. Úsalo antes de declarar "arreglado" cualquier cambio que toque un símbolo compartido (función, schema, endpoint, constante).
---

# samd-trace — Análisis de impacto (IEC 62304 §5.6)

Un bug se considera "arreglado" SOLO tras revisar **todos los consumidores** del símbolo modificado, no solo el archivo donde se reportó. Esta skill materializa ese análisis.

## Cuándo usarla

- Antes de modificar un parámetro, retorno, schema, constante o endpoint compartido.
- Antes de declarar verde un fix que toca un símbolo usado en más de un lugar.
- Cuando el usuario pide "análisis de impacto" de un cambio.

## Procedimiento

1. **Genealogía del símbolo**: localizá dónde está definido (`grep -rn "def <símbolo>\|class <símbolo>\|const <símbolo>"`), su firma y su tipo.

2. **Consumidores directos**: `grep -rn "<símbolo>"` en `frontend/`, `app/` y `tests/`. Listá cada archivo.

3. **Consumidores indirectos**: si es un schema de validación o un endpoint, buscá el DAO frontend que lo consume y los tipos generados del contrato.

4. **Tests vinculados**: listá los archivos de test que ejercitan el símbolo. Si alguno falta, marcá falta de cobertura (bloqueante SaMD).

5. **Documentación a tocar** (si el símbolo es clínico): TECHNICAL_DEBT_SUMMARY + ISO_14971_RISK_MATRIX (si toca fail-safe) + MASTER_MAP.

6. **Comando de verificación**: entregá el comando exacto que corre los tests vinculados.

## Reglas duras

- NO declares "arreglado" sin chequear TODOS los consumidores.
- Cambio en API pública (endpoint/schema) → regenerar tipos del contrato en el frontend.
- Cambio en schema → recordar verificar la revisión de migración real aplicada en el entorno destino.
- Salida en {{CHAT_LANG}}, formato bullet, con paths exactos.
