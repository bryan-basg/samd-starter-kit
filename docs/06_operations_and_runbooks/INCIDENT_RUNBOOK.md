# Runbook de Incidentes en Producción

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Adaptá nombres de servicios y canales a tu organización.

---

## 1. Regla de oro: leer los logs estructurados PRIMERO

Ante un incidente o un workflow en rojo, **leer los logs estructurados frescos de producción antes de teorizar** sobre cache, navegador o configuración. Los logs viejos pueden expirar: re-disparar para obtener el error real. Antes de asumir bug de código, descartar causa **ambiental** (OOM del runner, timeout, flaky).

```bash
<comando-ver-logs-estructurados>      # filtrar por severidad ERROR + ventana de tiempo
```

---

## 2. Triage inicial

| Paso | Acción |
|---|---|
| 1 | Confirmar el síntoma real (reproducir o ver evidencia), no el reportado de oído. |
| 2 | Medir alcance: ¿todos los usuarios o un subconjunto? ¿una plataforma (ej. móvil) o todas? |
| 3 | Clasificar severidad (sección 4). |
| 4 | ¿Coincide con un deploy reciente? Ver `DEPLOY_RUNBOOK.md` → rollback. |

---

## 3. Síntomas comunes y causa probable

| Síntoma | Causa probable | Acción |
|---|---|---|
| **401 masivo + 500 sin autenticación** | **Pool de conexiones de BD agotado** (no caben más conexiones; auth no puede consultar) | Revisar `max-instances × pool_size` vs límite del tier; reducir concurrencia o subir tier; ver logs de saturación |
| Latencia alta generalizada | Saturación de cómputo / consultas lentas / dependencia externa lenta | Escalar instancias; revisar consultas; circuit-breaker a la dependencia |
| 503 + Retry-After esperado | Fail-safe activo por carga | Verificar que es degradación controlada, no caída; escalar si persiste |
| Errores solo en una plataforma (ej. móvil) | Bug específico de cliente/WebView | Capturar request/response del dispositivo; no guiar al usuario por DevTools |
| Migración falló en deploy | Driver/schema incompatible | El deploy abortó; producción intacta; investigar log del job |
| Tracebacks visibles al usuario | Fail-safe roto | Hotfix para envolver el error; revisar manejo de excepciones |

---

## 4. Severidad y escalada

| Nivel | Definición | Respuesta | Escalar a |
|---|---|---|---|
| **SEV-1** | Caída total o riesgo clínico/seguridad (PHI expuesta, alerta clínica perdida) | Inmediata, todo el equipo | Propietario + responsable regulatorio + seguridad |
| **SEV-2** | Degradación grave de una función clínica | < 1 h | Líder técnico + responsable clínico |
| **SEV-3** | Función no crítica degradada | Día hábil | Líder técnico |
| **SEV-4** | Cosmético / sin impacto clínico | Backlog | — |

> Cualquier incidente con posible exposición de PHI/PII es **SEV-1** y dispara obligaciones de notificación según la normativa de privacidad aplicable.

---

## 5. Comunicación

- **Interna**: canal de incidentes; un único *incident commander* coordina.
- **A usuarios**: mensajes claros y empáticos, sin jerga técnica. Un usuario en crisis no debe ver "500 Internal Server Error".
- **Regulatoria/legal**: el responsable regulatorio evalúa si el incidente requiere reporte a la autoridad (vigilancia post-mercado) o notificación de brecha.

---

## 6. Post-mortem (sin culpa)

Tras resolver, dentro de <N> días hábiles:

- [ ] Línea de tiempo de los hechos (detección → mitigación → resolución).
- [ ] Causa raíz (técnica y de proceso).
- [ ] Impacto: usuarios afectados, datos, duración, ¿hubo daño clínico?
- [ ] Qué funcionó y qué no en la respuesta.
- [ ] Acciones correctivas con responsable y fecha.
- [ ] Trazabilidad: ¿nuevo riesgo para la matriz ISO 14971? ¿deuda técnica? ¿RFC?
- [ ] Test de regresión que habría cazado el incidente.

---

## 7. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
