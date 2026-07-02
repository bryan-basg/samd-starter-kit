---
description: Aplica una migración de esquema MANUAL contra la base de datos de producción desde local (túnel/proxy al motor gestionado + driver síncrono + comando de migración).
argument-hint: <opcional — revisión o "head">
---

Sos un asistente que aplica una migración de esquema manual contra la base de datos de producción de {{PROJECT_NAME}} ({{DB_STACK}} sobre {{CLOUD_STACK}}). **Ojo de proceso:** si tu deploy normal migra solo vía un job/paso automatizado (que aborta el deploy si la migración falla), esta receta MANUAL es sólo para pasos diferidos, recuperación, o rotación de claves/re-cifrado de datos sensibles — NO reemplaza el flujo normal.

## Por qué hay que reescribir la cadena de conexión

- El secreto de conexión en prod suele estar en formato **driver asíncrono + socket propio de la nube** (ej. `postgresql+asyncpg://USER:PASS@/DBNAME?host=/ruta/socket/INSTANCIA`).
- Dos problemas típicos al migrar desde local: (1) la herramienta de migración (Alembic, Flyway, etc.) suele correr con un motor **síncrono** → un driver asíncrono revienta con errores de tipo "missing greenlet" o equivalente; hay que pasar el esquema de la URL al driver síncrono (ej. `psycopg2`) que ya debería estar disponible en tu entorno virtual/dependencias de dev. (2) El socket/ruta propio de la nube no existe en local → reemplazarlo por `127.0.0.1:<puerto del túnel>` (usá un puerto distinto al de tu Postgres/DB local de desarrollo si corre en la misma máquina, para no pisarlo).

## Datos de conexión (completá con los de tu proyecto)

- Instancia gestionada: `<proyecto>:<región>:<instancia>` ({{DB_STACK}})
- Secreto de conexión: `DATABASE_URL` (o el nombre que uses en tu gestor de secretos de {{CLOUD_STACK}})
- Binarios: el proxy/túnel del proveedor de nube (ej. `cloud-sql-proxy` o equivalente) y el binario de migración de tu entorno virtual (ej. `venv/bin/alembic`)

## Receta (4 pasos)

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
- Si tu flujo normal migra solo vía un job/paso automatizado en el deploy, esta receta es la excepción (pasos diferidos, recuperación, rotación de claves/re-cifrado de datos sensibles vía túnel manual).
- Un CI que migra contra un motor de base de datos distinto al de producción (ej. SQLite en CI vs Postgres en prod) puede ocultar errores específicos del driver de prod (como el problema del motor síncrono/asíncrono de arriba). NUNCA confiar en el verde de la migración del CI sin verificar la revisión real aplicada en el entorno destino.
- Cerrar SIEMPRE el proxy/túnel al terminar (`pkill` o equivalente) — dejarlo abierto es una conexión viva innecesaria contra prod.

Revisión objetivo: $ARGUMENTS
