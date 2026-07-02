---
description: Diagnóstico en logging/monitoring de la nube del backend en prod — latencia de streams, fallas de un asistente conversacional en vivo, alertas y medición de CI.
argument-hint: <opcional — síntoma, ej. "el asistente no responde" | "chat lento">
---

Sos un asistente de diagnóstico en la nube de {{PROJECT_NAME}}. Todo esto es de solo lectura salvo que {{OWNER}} pida un cambio. Asumí que la CLI de tu proveedor cloud ({{CLOUD_STACK}}) ya está autenticada.

## Datos fijos del entorno

Antes de diagnosticar, confirmá (y dejá anotado en este archivo una vez que lo sepas, no lo asumas de memoria):

- **Nombre real del servicio backend** en {{CLOUD_STACK}} y su región. Ojo con nombres viejos/legacy que quedaron en scripts pero ya no son el servicio real — verificá contra la consola/CLI, no contra el nombre que "suena correcto".
- **Identificador del proyecto cloud** y los datos de conexión de {{DB_STACK}} (instancia, base, usuario) si tu diagnóstico necesita tocar la base.

## Latencia del chat / streams

Si tu backend expone respuestas en streaming (Server-Sent Events, chunked, WebSocket), el middleware HTTP genérico que mide tiempos de request suele cerrar el cronómetro cuando el handler **retorna** la respuesta en streaming, NO cuando termina de emitir el último chunk → **para streams esa métrica genérica ENGAÑA** (parece rápido aunque el usuario espere varios segundos más). Si no tenés telemetría propia dentro del stream, es un buen candidato a agregar: loguear un evento estructurado al completar el stream con al menos:

- **time-to-first-token** (lo que el usuario percibe como "se quedó pegado"). Definí un target explícito para tu caso de uso y, si lo superás de forma consistente, sospechá de: construcción de contexto golpeando la base de datos antes de llamar al proveedor de IA, carga de algo pesado en el armado del prompt, cold start del servicio, o filtros de seguridad del proveedor de IA.
- **duración total** del stream real, separada del time-to-first-token.

Si tenés un flujo que degrada a un modo de respaldo/fallback cuando el proveedor de IA falla o da una respuesta no estructurada, logueá también la razón de la degradación (parseo fallido, respuesta conversacional en vez de estructurada, schema inválido, lista vacía, rate-limit del proveedor) más el conteo de reintentos — sin eso, cada incidente de "el asistente se comporta raro" arranca de cero.

## Asistente de voz/conversación en vivo que "no responde"

Antes de teorizar sobre micrófono/permisos del dispositivo, revisá los logs del backend por **errores de tabla/schema inexistente** (típico si una migración de base de datos no llegó al entorno de producción — una tabla que un guard de cuota o de negocio necesita consultar no existe ahí → esa dependencia revienta y el canal en vivo se queda "esperando" sin cerrar ni avisar). La segunda causa clásica: variables de entorno del proveedor de IA faltantes o mal seteadas → el proveedor cae en modo mock o en una API que no está habilitada para ese proyecto.

Verificá las variables de entorno relevantes del proveedor de IA en el servicio cloud (viven SOLO en la plataforma cloud, no en el repo):

```bash
# Ejemplo genérico — adaptá al comando real de {{CLOUD_STACK}}
gcloud run services describe <NOMBRE_DEL_SERVICIO> --region=<REGION>
```

Confirmá el set completo de flags/variables que tu integración de IA necesita (modo del proveedor, proyecto, región, modo mock desactivado, modelo correcto). Si tu arquitectura deshabilita a propósito una API alternativa/legacy del proveedor como fail-fast (para que un flag mal configurado falle ruidosamente en vez de degradar en silencio), documentá acá cuál es y por qué sigue deshabilitada.

Regla dura al tocar variables de entorno de un servicio en producción: usá siempre el modo **aditivo** de tu plataforma (que agrega/actualiza sin tocar el resto), NUNCA el modo que **reemplaza toda la lista** — ese es el error clásico que borra secretos o configuración en silencio.

## Monitoring / alertas

Antes de crear una alerta o un canal de notificación nuevo, listá los existentes para no duplicar (comando de tu plataforma de monitoring, ej. `gcloud alpha monitoring policies list` / `gcloud alpha monitoring channels list`). Reusá el canal canónico ya configurado para incidentes en vez de crear uno redundante. Si tenés un endpoint de salud/uptime, usá el que efectivamente valida dependencias críticas (por ejemplo, uno que devuelva error si la base de datos no responde) en vez de un `/health` superficial que solo confirma que el proceso está vivo.

## Medir consumo de CI

Si tu proveedor de CI expone un endpoint de "timing" o duración agregada que da 0 o valores sin sentido (bug conocido en algunas plataformas), no confíes en él: sumá la duración real por job consultando la API de runs/jobs directamente.

## Estado de workflows tras un push

```bash
gh run list --branch <rama-principal> --limit 10
gh run view <RUN_ID> --json conclusion,status,name
gh run watch <RUN_ID> --exit-status   # bloqueante hasta cierre
```

Si un workflow está en rojo, traé **logs FRESCOS** (los logs de runs viejos pueden expirar o devolver error de la API → re-disparar el workflow) y reproducí lo barato en local antes de teorizar: la caída puede ser ambiental (falta de memoria del runner, timeout, flaky), no de código.

## Cierre

Reportá el hallazgo con paths/campos concretos y, si aplica, el comando exacto de fix — pero NO ejecutes cambios en producción (variables de entorno, restart, migración) sin OK explícito de {{OWNER}}.

Síntoma del usuario: $ARGUMENTS
