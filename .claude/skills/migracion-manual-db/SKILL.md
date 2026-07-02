---
name: migracion-manual-db
description: Aplica una migración de esquema MANUAL contra la base de datos de producción desde local (túnel/proxy al motor gestionado + driver síncrono + comando de migración). Úsala cuando haya que correr un paso de migración diferido, una recuperación, o una rotación de claves/re-cifrado de datos sensibles fuera del deploy automático — nunca como reemplazo del flujo normal de migración en el pipeline.
---

# migracion-manual-db — Migración manual de esquema contra producción

Aplica una migración de esquema MANUAL contra la base de datos de producción de {{PROJECT_NAME}} ({{DB_STACK}} sobre {{CLOUD_STACK}}) desde el entorno local, mediante un túnel/proxy al motor gestionado + driver síncrono + el comando de migración del proyecto.

**Ojo de proceso:** si el deploy normal migra solo vía un job/paso automatizado (que aborta el deploy si la migración falla), esta receta MANUAL es sólo para pasos diferidos, recuperación, o rotación de claves/re-cifrado de datos sensibles — NO reemplaza el flujo normal.

## Cuándo usarla

- Hay que aplicar un paso de migración que quedó diferido o que el job automático de deploy no cubrió.
- Se necesita recuperar el esquema de producción a una revisión específica fuera del ciclo normal de deploy.
- Se está rotando una clave o re-cifrando datos sensibles y eso requiere tocar producción directamente desde local.
- El usuario pide correr `alembic upgrade` (o el comando de migración equivalente) contra la base de datos de producción.

## Por qué hay que reescribir la cadena de conexión

- El secreto de conexión en prod suele estar en formato **driver asíncrono + socket propio de la nube** (ej. `postgresql+asyncpg://USER:PASS@/DBNAME?host=/ruta/socket/INSTANCIA`).
- Dos problemas típicos al migrar desde local:
  1. La herramienta de migración (Alembic, Flyway, etc.) suele correr con un motor **síncrono** → un driver asíncrono revienta con errores de tipo "missing greenlet" o equivalente; hay que pasar el esquema de la URL al driver síncrono (ej. `psycopg2`) que ya debería estar disponible en el entorno virtual/dependencias de dev.
  2. El socket/ruta propio de la nube no existe en local → reemplazarlo por `127.0.0.1:<puerto del túnel>` (usar un puerto distinto al de la Postgres/DB local de desarrollo si corre en la misma máquina, para no pisarlo).

## Datos de conexión (completar con los del proyecto)

- Instancia gestionada: `<proyecto>:<región>:<instancia>` ({{DB_STACK}})
- Secreto de conexión: `DATABASE_URL` (o el nombre que se use en el gestor de secretos de {{CLOUD_STACK}})
- Binarios: el proxy/túnel del proveedor de nube (ej. `cloud-sql-proxy` o equivalente) y el binario de migración del entorno virtual (ej. `venv/bin/alembic`)

## Procedimiento (4 pasos)

```bash
# 1) Levantar el proxy/túnel en background contra un puerto local libre
<binario-proxy-de-tu-nube> --port=5433 \
  <proyecto>:<región>:<instancia> &

# 2) Esperar a que el puerto esté listo
until ss -tln | grep -q ':5433 '; do sleep 0.3; done

# 3) Reescribir DATABASE_URL a driver síncrono + TCP y aplicar
cd "<ruta-del-repo>"
export DATABASE_URL=$(<comando-de-tu-gestor-de-secretos> access latest --secret=DATABASE_URL | python3 -c "
import sys, re
v = sys.stdin.read().strip()
m = re.match(r'postgresql\+asyncpg://([^:]+):([^@]+)@/([^?]+)\?host=', v)
print(f'postgresql+psycopg2://{m.group(1)}:{m.group(2)}@127.0.0.1:5433/{m.group(3)}')
")
venv/bin/alembic current    # ver en qué revisión está prod
venv/bin/alembic upgrade head

# 4) Cerrar el proxy
pkill -f "<binario-proxy-de-tu-nube> --port=5433"
```

## Verificar antes y después

- `venv/bin/alembic current` → revisión aplicada en prod.
- `venv/bin/alembic heads` → revisión target en el código.
- La diferencia entre ambas = migraciones pendientes.

## Reglas duras

- Requiere el entorno virtual del proyecto activo (sin él, la herramienta de migración y el driver síncrono del sistema pueden fallar o resolver versiones distintas a las del proyecto).
- Si el flujo normal migra solo vía un job/paso automatizado en el deploy, esta receta es la excepción (pasos diferidos, recuperación, rotación de claves/re-cifrado de datos sensibles vía túnel manual).
- Un CI que migra contra un motor de base de datos distinto al de producción (ej. SQLite en CI vs Postgres en prod) puede ocultar errores específicos del driver de prod (como el problema del motor síncrono/asíncrono de arriba). NUNCA confiar en el verde de la migración del CI sin verificar la revisión real aplicada en el entorno destino.
- Cerrar SIEMPRE el proxy/túnel al terminar (`pkill` o equivalente) — dejarlo abierto es una conexión viva innecesaria contra prod.
