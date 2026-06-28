---
description: Protocolo de desarrollo agnóstico al agente para {{PROJECT_NAME}} — alineado con SaMD Clase {{SAMD_CLASS}} (IEC 62304 + ISO 14971 + WCAG 2.1 AA).
---

# Protocolo de Desarrollo — {{PROJECT_NAME}}

> Este protocolo es **agnóstico al agente**: captura el **proceso estable** de cómo se trabaja en este repo, aplicable a cualquier asistente de IA que opere sobre él. Las reglas dinámicas (estado de tests, deuda en curso) viven en `docs/` y en la memoria del agente.
>
> **Fuente de verdad:** el canon es el `CLAUDE.md` del proyecto. Este protocolo es su **espejo** y debe mantenerse sincronizado. Si divergen, manda el `CLAUDE.md` y, por encima de todo, la **realidad del código**.

---

## Regla 0 — Cumplimiento SaMD es la prioridad absoluta

Este software es **SaMD Clase {{SAMD_CLASS}}** bajo **IEC 62304 + ISO 14971 + WCAG 2.1 AA + GDPR/HIPAA**. Toda decisión técnica se subordina al cumplimiento SaMD.

Consecuencias prácticas:

1. **Trazabilidad obligatoria** (§5.1, §5.7): cada cambio en algoritmo clínico, schema de BD, regla de negocio o flujo de seguridad se registra en TECHNICAL_DEBT_SUMMARY, en ISO_14971_RISK_MATRIX cuando aplique, y se refleja en el Master Map.
2. **No alucinar arquitectura, schemas ni reglas clínicas.** Sin certeza → detenete y leé la documentación maestra.
3. **Prohibido eliminar documentación** sobre arquitectura o algoritmos clínicos sin reporte de trazabilidad.
4. **Verificación obligatoria** (§5.7): no se declara "verde" sin correr los tests vinculados y reportar números.
5. **Fail-safe explícito** (ISO 14971): cuando un módulo clínico falle, el sistema degrada de forma segura y predecible — nunca silenciosa, nunca con tracebacks expuestos.
6. **Análisis de impacto antes de fixear** (§5.6): un bug se arregla solo tras revisar **todos los consumidores** del símbolo modificado.

---

## 1. Fase de análisis e investigación (lectura previa obligatoria)

Antes de cualquier cambio estructural, leer: `docs/00_master/MASTER_MAP.md`, el protocolo de auditoría, la estrategia de testing y los RFCs vigentes en `docs/05_design_decisions/`. **Búsqueda de impacto** antes de tocar contratos: `grep` sobre `frontend/`, `app/` y `tests/`.

## 2. Comunicación — Idioma y empatía

- **Chat**: {{CHAT_LANG}}, claro, directo, empático. Sin jerga regulatoria innecesaria.
- **Código**: inglés (variables, tipos, commits).
- **Reportes formales** (docs, tests): tecnicismo y precisión — obligatorio por SaMD.
- **Mensajes al usuario final**: empáticos, sin jerga. Un usuario en crisis no debe ver "500 Internal Server Error".
- **Glosario clínico pre-certificación**: el frontend no afirma función de dispositivo médico no certificado mientras la certificación esté pendiente.

## 3. Boy Scout (mantenibilidad — §5.7)

Deja el código más limpio que lo encontraste (refactorizá al menos un pedazo de deuda en el archivo tocado). Documentá junto con el cambio — Master Map y DHF en el mismo PR.

## 4. Análisis de impacto antes de declarar "arreglado" (§5.6)

- Búsqueda global al modificar parámetro, retorno, schema o constante.
- Cambio de endpoint → actualizar consumidor frontend + regenerar tipos del contrato.
- Bug reportado → investigar primero, no saltar a código.
- Bug tras deploy → revisar logs estructurados de la plataforma cloud antes de teorizar.
- Reorg de `docs/` → link-checker cross-doc en 0 broken antes de cerrar el PR.
- Propagación anti-drift: una regla viva o valor de config volátil se propaga a TODOS sus espejos en la misma pasada; el código es la fuente de verdad.

## 5. Estándares del backend

Adaptá a tu stack ({{BACKEND_STACK}} / {{DB_STACK}}). Principios estables: identidad por token (nunca por cliente), 100% async/no-blocking, tipado estricto, cifrado en reposo AES-256-GCM con clave en gestor de secretos, migraciones atómicas con verificación de la revisión real, env vars de prod en el gestor de secretos, audit middleware solo-mutaciones, fail-safe con 503 + Retry-After.

## 6. Estándares del frontend

Adaptá a tu stack ({{FRONTEND_STACK}}). Principios: offline-first (mutaciones por outbox), librería de fetch+cache obligatoria, modal canónico, diseño plano con contraste WCAG AA, `prefers-reduced-motion` incondicional, ARIA correcto, anti-flood de toasts, sin emoji en aria-labels críticos, no tocar componentes compartidos sin pedido explícito.

## 7. Testing (verificación SaMD §5.7 — no negociable)

- Tests rigurosos, no de humo. Tras cada Edit/Write, correr los tests vinculados y reportar números.
- Mutation score: frontend GLOBAL ≥90%, backend ≥80% en módulos clínicos (ajustá a tu Clase).
- Mocks asíncronos firmes + aislamiento de estado global. Mock con whitelist para `hasattr`/duck-typing.
- No correr tests/type-checker mientras corre mutation testing.
- El motor de mutation NUNCA en paralelo con agentes que escriben tests.

## 8. Orquestación multi-agente (anti-drift y cohesión)

- Por defecto, paralelismo agresivo cuando la tarea lo permita.
- Verificación adversarial obligatoria sobre hallazgos clínicos/seguridad.
- Protocolo anti-drift con 2+ agentes: (1) leo brief yo, (2) escribo contrato compartido y espero OK, (3) brief citando el contrato literal, (4) leo el `git diff` REAL, (5) drift → 1 agente correctivo, (6) auditoría de trazabilidad, (7) cierro con números reales.
- Serializar cuando el contrato es complejo/cambiante o el símbolo cruza 3+ capas.

## 9. Definition of Done

1. El código pasa linting + CI local.
2. Los tests vinculados verdes y los números reportados.
3. Se redujo deuda técnica en al menos un punto (Boy Scout).
4. La documentación está al día (Master Map, spec, TECHNICAL_DEBT, TRACEABILITY, y Risk Matrix si aplica).
5. La UI es accesible (contraste WCAG AA, diseño plano, modales canónicos).
6. El cambio fue comunicado al dueño con genealogía clara antes de commit, y autorizado explícitamente.
