---
name: diagnostico-cloud
description: Diagnóstico en Cloud Logging / Monitoring del backend en prod — latencia de streams, fallas de un asistente conversacional en vivo, alertas y medición de GitHub Actions. Usala cuando el síntoma sea "el chat/asistente no responde", "se siente lento", una alerta de monitoring dudosa, o un workflow de CI en rojo tras un push y necesites ir a los logs de la nube en vez de teorizar desde el código.
---

# diagnostico-cloud — Diagnóstico en logging/monitoring de la nube (prod)

Esta skill es de solo lectura sobre el entorno cloud, salvo que el dueño del proyecto pida un cambio explícito. Asumí que la CLI del proveedor cloud ya está autenticada.

## Cuándo usarla

- El backend en producción muestra síntomas de latencia rara en un stream (chat, respuestas incrementales) que las métricas genéricas no explican.
- Un asistente de voz/conversación en vivo "no responde" y hay que descartar causas de backend antes de sospechar del dispositivo del usuario.
- Hace falta revisar o crear una alerta de monitoring sin duplicar canales existentes.
- Un workflow de CI quedó en rojo tras un push, o hace falta medir consumo real de minutos de CI.

## Datos fijos del entorno

Antes de diagnosticar, confirmá (y dejá anotado una vez que lo sepas, no lo asumas de memoria):

- **Nombre real del servicio backend** en la plataforma cloud y su región. Ojo con nombres viejos/legacy que quedaron en scripts pero ya no son el servicio real — verificá contra la consola/CLI, no contra el nombre que "suena correcto".
- **Identificador del proyecto cloud** y los datos de conexión de la base de datos (instancia, base, usuario) si el diagnóstico necesita tocarla.

## Latencia del chat / streams

Si el backend expone respuestas en streaming (Server-Sent Events, chunked, WebSocket), el middleware HTTP genérico que mide tiempos de request suele cerrar el cronómetro cuando el handler **retorna** la respuesta en streaming, NO cuando termina de emitir el último chunk → para streams esa métrica genérica ENGAÑA (parece rápido aunque el usuario espere varios segundos más). Si no hay telemetría propia dentro del stream, es un buen candidato a agregar: loguear un evento estructurado al completar el stream con al menos:

- **time-to-first-token** (lo que el usuario percibe como "se quedó pegado"). Definí un target explícito para el caso de uso y, si se supera de forma consistente, sospechá de: construcción de contexto golpeando la base de datos antes de llamar al proveedor de IA, carga de algo pesado en el armado del prompt, cold start del servicio, o filtros de seguridad del proveedor de IA.
- **duración total** del stream real, separada del time-to-first-token.

Si hay un flujo que degrada a un modo de respaldo/fallback cuando el proveedor de IA falla o da una respuesta no estructurada, logueá también la razón de la degradación (parseo fallido, respuesta conversacional en vez de estructurada, schema inválido, lista vacía, rate-limit del proveedor) más el conteo de reintentos — sin eso, cada incidente de "el asistente se comporta raro" arranca de cero.

## Asistente de voz/conversación en vivo que "no responde"

Antes de teorizar sobre micrófono/permisos del dispositivo, revisá los logs del backend por **errores de tabla/schema inexistente** (típico si una migración de base de datos no llegó al entorno de producción — una tabla que un guard de cuota o de negocio necesita consultar no existe ahí → esa dependencia revienta y el canal en vivo se queda "esperando" sin cerrar ni avisar). La segunda causa clásica: variables de entorno del proveedor de IA faltantes o mal seteadas → el proveedor cae en modo mock o en una API que no está habilitada para ese proyecto.

Verificá las variables de entorno relevantes del proveedor de IA en el servicio cloud (viven SOLO en la plataforma cloud, no en el repo):

```bash
# Ejemplo genérico — adaptá al comando real de tu proveedor cloud
gcloud run services describe <NOMBRE_DEL_SERVICIO> --region=<REGION>
```

Confirmá el set completo de flags/variables que la integración de IA necesita (modo del proveedor, proyecto, región, modo mock desactivado, modelo correcto). Si la arquitectura deshabilita a propósito una API alternativa/legacy del proveedor como fail-fast (para que un flag mal configurado falle ruidosamente en vez de degradar en silencio), documentá acá cuál es y por qué sigue deshabilitada.

Regla dura al tocar variables de entorno de un servicio en producción: usá siempre el modo **aditivo** de la plataforma (que agrega/actualiza sin tocar el resto), NUNCA el modo que **reemplaza toda la lista** — ese es el error clásico que borra secretos o configuración en silencio.

## Monitoring / alertas

Antes de crear una alerta o un canal de notificación nuevo, listá los existentes para no duplicar (comando de la plataforma de monitoring, ej. `gcloud alpha monitoring policies list` / `gcloud alpha monitoring channels list`). Reusá el canal canónico ya configurado para incidentes en vez de crear uno redundante. Si hay un endpoint de salud/uptime, usá el que efectivamente valida dependencias críticas (por ejemplo, uno que devuelva error si la base de datos no responde) en vez de un `/health` superficial que solo confirma que el proceso está vivo.

## Medir consumo de CI

Si el proveedor de CI expone un endpoint de "timing" o duración agregada que da 0 o valores sin sentido (bug conocido en algunas plataformas), no confíes en él: sumá la duración real por job consultando la API de runs/jobs directamente.

## Estado de workflows tras un push

```bash
gh run list --branch <rama-principal> --limit 10
gh run view <RUN_ID> --json conclusion,status,name
gh run watch <RUN_ID> --exit-status   # bloqueante hasta cierre
```

Si un workflow está en rojo, traé **logs FRESCOS** (los logs de runs viejos pueden expirar o devolver error de la API → re-disparar el workflow) y reproducí lo barato en local antes de teorizar: la caída puede ser ambiental (falta de memoria del runner, timeout, flaky), no de código.

## Cierre

Reportá el hallazgo con paths/campos concretos y, si aplica, el comando exacto de fix — pero NO ejecutes cambios en producción (variables de entorno, restart, migración) sin OK explícito del dueño del proyecto.
