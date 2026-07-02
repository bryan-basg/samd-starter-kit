---
name: rotar-secreto-prod
description: Rota un secreto/llave en producción ({{CLOUD_STACK}} → consumidor → redeploy → verificar); para una llave de cifrado de datos sensibles incluye promover la llave nueva y re-cifrar el backlog. Úsala cuando el usuario pida rotar, renovar o "cambiar" un secreto/API key/llave de cifrado que ya vive en el gestor de secretos de producción, cuando un secreto quedó expuesto en una salida de agente o log, o cuando toque endurecer un cron/scheduler que hoy usa un secreto compartido en texto plano.
---

# rotar-secreto-prod — Rotación de un secreto en producción

Base: la plataforma cloud lee los secretos desde su gestor de secretos y SÓLO al arrancar el contenedor/proceso (no en caliente), así que rotar sin redeploy no cambia nada en prod. La lista de secretos consumidos por el backend vive en el workflow/manifiesto de deploy del backend (variables típicas: cadena de conexión a base de datos, llave de firma de sesión, credenciales de proveedores externos, llaves de cifrado en reposo).

## Cuándo usarla

- El usuario pide rotar, renovar o reemplazar un secreto/API key/llave de cifrado que ya está vivo en el gestor de secretos de {{CLOUD_STACK}}.
- Un secreto quedó visible en la salida de una sesión de agente, un log o un commit.
- Se necesita promover una llave de cifrado de datos sensibles (ej. `ENCRYPTION_KEY`) y re-cifrar el backlog viejo.
- Se va a migrar un cron/scheduler de un secreto compartido en texto plano a un mecanismo de autenticación más fuerte.

## Gotcha de permisos

El clasificador NO deja a Claude correr el comando que sube una nueva versión de un secreto vivo al gestor de secretos (ni con OK verbal), ni el primer push/redeploy post-OK vago. Pedile a {{OWNER}} el comando con `!` directamente para esos pasos.

## Receta genérica (secreto simple, p.ej. un secreto compartido de un cron) — ~30 min, cero código

El ORDEN importa (hay ventana de error de autenticación si te equivocás):

1. **Nueva versión en el gestor de secretos de {{CLOUD_STACK}}**:
   comando equivalente a `echo -n "<valor>" | gcloud secrets versions add <NOMBRE> --data-file=-` (adaptar al CLI de tu proveedor).
2. **Actualizar el consumidor** si el valor viaja también fuera del gestor de secretos. Ej. un cron/scheduler externo que manda un header con el secreto en texto plano en la config del job (limitación estructural común en schedulers gestionados) → actualizar esa config con el comando equivalente. Hacerlo ANTES del redeploy o coordinar en la misma ventana.
3. **Forzar reload del servicio** (los secretos sólo se leen al arrancar):
   comando equivalente a `gcloud run services update <servicio> --region=<region> --update-env-vars=RESTART_TRIGGER=$(date +%s)`
   (o re-run del workflow de deploy del backend).
4. **Verificar**: leer la versión activa del secreto desde el gestor + health check 200 + el flujo que usa el secreto responde OK.

## Receta llave de cifrado de datos sensibles — rotación versionada

Si el sistema soporta rotación versionada (blobs con prefijo de versión, ej. `v2:`, registry de llaves legacy vs nueva en el servicio de cifrado, script de re-cifrado idempotente con dry-run por default), la fase de mapear la llave legacy suele estar ya desplegada; los pasos que quedan:

1. **{{OWNER}} promueve la llave nueva** (comando con `!`, el clasificador bloquea esto):
   comando equivalente a `openssl rand -base64 48 | tr -d '\n' | gcloud secrets versions add <NOMBRE_LLAVE_NUEVA> --data-file=-`
   (antes, asegurarse de que la variable de llave legacy = la llave vieja/actual, para que el descifrado de datos viejos siga funcionando).
2. **Redeploy INMEDIATO** (re-run del workflow de deploy o el equivalente de tu CI) — minimiza la ventana en que una instancia nueva de la revisión vieja tomaría el secreto nuevo sin la legacy correcta. Evaluar el riesgo real según tráfico y cantidad de instancias corriendo en paralelo.
3. **Verificar**: health 200 + login + una pantalla/endpoint que lea datos cifrados (= descifrado con la llave legacy sigue funcionando).
4. **Re-cifrar el backlog** (blobs viejos siguen cifrados con la llave vieja): vía conexión directa a la base de datos con las env vars de prod (llave nueva, llave legacy, entorno=producción, cadena de conexión apuntando al proxy/túnel seguro):
   correr el script de re-cifrado en modo dry-run → revisar números → correrlo en modo aplicar.
5. **Cuando el backlog viejo llegue a 0**: retirar la variable de llave legacy (decisión aparte, no urgente) y cerrar la deuda técnica correspondiente en tu documento de deuda técnica (cualquier warning de "llave de cifrado igual a otra llave de propósito distinto" en la config debería desaparecer solo).

## Reglas duras

- Rotar SIEMPRE termina en redeploy/restart; sin eso, prod sigue con el valor viejo aunque el gestor de secretos esté actualizado. Avisar a {{OWNER}} del restart.
- El comando de actualizar variables de entorno de tu plataforma cloud puede REEMPLAZAR toda la lista en vez de mezclar; usar siempre la variante aditiva/update, nunca la que reemplaza todo.
- Un secreto que quedó visible en la salida de una sesión de agente conviene rotarlo.
- Para endpoints/flujos clínicos (ej. un cron que dispara notificaciones): si migrás de un secreto compartido a un mecanismo de autenticación más fuerte (ej. tokens firmados por la plataforma en vez de un header estático), es cambio de flujo de seguridad → verificación adversarial + tests + trazabilidad + ventana de doble-validación. Cambio destructivo → OK explícito de {{OWNER}}.
