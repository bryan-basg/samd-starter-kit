# Visión y Gobernanza

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Reemplazá todos los marcadores `{{...}}` y borrá las notas en bloque `>` antes de publicar.

---

## 0. Regla 0 — El cumplimiento SaMD es la prioridad absoluta

Este software está regulado como **Software as a Medical Device (SaMD) Clase {{SAMD_CLASS}}** bajo **IEC 62304** + **ISO 14971** + **WCAG 2.1 AA** + el marco de privacidad aplicable (GDPR/HIPAA según mercado).

**Toda decisión técnica se subordina al cumplimiento SaMD.** Cuando una conveniencia de desarrollo entre en conflicto con una obligación regulatoria, **gana siempre el cumplimiento**.

Consecuencias prácticas (no son reglas opcionales):

1. **Trazabilidad obligatoria** (IEC 62304 §5.1, §5.7): todo cambio en algoritmo clínico, esquema de datos, regla de negocio o flujo de seguridad se registra en el resumen de deuda técnica, en la matriz de riesgos (cuando aplique) y en el Master Map.
2. **No alucinar arquitectura ni reglas clínicas.** Ante la duda, leer la documentación maestra antes de codear.
3. **No eliminar documentación** de arquitectura o algoritmos clínicos sin reporte de trazabilidad.
4. **Verificación demostrable** (IEC 62304 §5.7): ninguna tarea se declara "lista" sin correr los tests vinculados y reportar números.
5. **Fail-safe explícito** (ISO 14971): ante fallo de un módulo clínico (red, BD, IA), el sistema degrada de forma segura, predecible y visible — nunca en silencio, nunca exponiendo tracebacks al usuario.
6. **Análisis de impacto antes de fixear** (IEC 62304 §5.6): un bug se considera arreglado solo tras revisar TODOS los consumidores del símbolo modificado.

---

## 1. Visión del producto

| Campo | Valor |
|---|---|
| Nombre | {{PROJECT_NAME}} |
| Uso previsto (*intended use*) | {{INTENDED_USE}} |
| Población objetivo | <describir usuarios/pacientes> |
| Problema clínico que resuelve | <describir> |
| Lo que el producto NO hace | <límites explícitos del *intended use*; claims fuera de alcance> |
| Propietario / *legal manufacturer* | {{OWNER}} |
| Stack frontend | {{FRONTEND_STACK}} |
| Stack backend | {{BACKEND_STACK}} |
| Stack de datos | {{DB_STACK}} |
| Plataforma cloud | {{CLOUD_STACK}} |
| Idioma de trabajo | {{CHAT_LANG}} |

### 1.1 Declaración de uso previsto

> Redactar en una frase verificable: a quién va dirigido, qué función clínica cumple, en qué contexto de uso, y con qué grado de autonomía (informa / impulsa / dirige / diagnostica). Este texto fija la Clase SaMD y es la frontera de todos los *claims*.

`{{INTENDED_USE}}`

---

## 2. Gobernanza del proyecto

### 2.1 Roles y responsabilidades

| Rol | Responsable | Responsabilidad principal |
|---|---|---|
| Propietario del producto | {{OWNER}} | Decisión final, *intended use*, autorización de release |
| Responsable regulatorio (QA/RA) | <nombre> | DHF, matriz de riesgos, trazabilidad, auditorías |
| Líder técnico | <nombre> | Arquitectura, estándares de código, integridad técnica |
| Responsable clínico | <nombre> | Validez de algoritmos clínicos, evidencia |
| Responsable de seguridad | <nombre> | Cifrado, gestión de claves, control de acceso, SAST/DAST |
| DPO / privacidad | <nombre> | GDPR/HIPAA, minimización de PII/PHI, derechos del titular |

### 2.2 Toma de decisiones

- **Decisiones de arquitectura, schema, regla clínica o flujo de seguridad** se documentan vía RFC (ver `docs/05_design_decisions/RFC-TEMPLATE.md`) y se trazan a REQ/Risk.
- **Cambios destructivos** (datos, ramas, infraestructura) requieren OK explícito del propietario.
- **Release a producción**: lo autoriza el propietario tras *Definition of Done* y cierre de bloque (ver protocolo de auditoría).

### 2.3 Equipo de auditoría asistida

| Agente | Capa | Función |
|---|---|---|
| `samd-audit-trace` | Regulatorio (audita) | Detecta gaps de trazabilidad IEC 62304 §5.1/§5.7 + ISO 14971. No los escribe. |
| `docs-dhf` | Regulatorio (escribe) | Materializa Master Map, deuda técnica, matriz de riesgos, RFCs. Verifica `archivo:línea` + tests reales. |

---

## 3. Estrategia regulatoria

| Decisión | Valor |
|---|---|
| Clasificación objetivo | SaMD Clase {{SAMD_CLASS}} |
| Norma de ciclo de vida | IEC 62304 |
| Gestión de riesgos | ISO 14971 |
| Accesibilidad | WCAG 2.1 AA |
| Privacidad | <GDPR / HIPAA / otra, según mercado> |
| Mercados objetivo | <UE / EE. UU. / LATAM / otro> |
| Vía regulatoria | <marcado CE bajo MDR / 510(k) / De Novo / otra> |
| Sistema de gestión de calidad | <ISO 13485 — alcance> |

### 3.1 Hitos regulatorios

| Hito | Estado | Fecha objetivo |
|---|---|---|
| Definición de *intended use* y Clase | <pendiente/hecho> | YYYY-MM-DD |
| DHF base completo | <pendiente> | YYYY-MM-DD |
| Matriz de riesgos ISO 14971 cerrada | <pendiente> | YYYY-MM-DD |
| Evaluación de usabilidad IEC 62366 | <pendiente> | YYYY-MM-DD |
| Evidencia clínica | <pendiente> | YYYY-MM-DD |
| Sumisión regulatoria | <pendiente> | YYYY-MM-DD |

Detalle de la ruta de certificación: `docs/07_regulatory_and_compliance/CERTIFICATION_HOWTO.md`.

---

## 4. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
