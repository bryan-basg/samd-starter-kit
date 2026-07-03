# app/ — Backend {{BACKEND_STACK}}

Carpeta de arranque del backend (vive en la raíz `app/`, no en `backend/`). Los agentes `backend` y `db-architect` trabajan acá.

Estructura sugerida:

```
app/
├── routers/         # endpoints agrupados por contexto
├── services/        # lógica de negocio, módulos clínicos, scheduler, IA
├── schemas/         # validación de entrada/salida
├── models/          # modelos de datos + cifrado a nivel columna (AES-256-GCM)
├── middleware/      # auth, audit (solo-mutaciones), rate limit, observabilidad
├── core/            # config (Settings) — toda env var nueva va también a .env.example
└── dependencies.py  # token de auth -> user_id (NUNCA user_id desde el cliente)
```

Reglas duras (ver `.claude/agents/backend.md`): identidad solo del token, 100% async, tipado estricto, errores sin tracebacks, fail-safe con 503 + Retry-After, audit solo-mutaciones.

## Ejemplo ejecutable (borralo cuando traigas tu app)

Esta carpeta incluye un **slice mínimo** que demuestra las reglas duras en código real: identidad solo del token (`core/security.py`), cifrado AES-256-GCM en reposo (`core/encryption.py`), un recurso con aislamiento por dueño (`routers/notes.py`) y fail-safe sin traceback (`main.py`). Sin base de datos: el store es en memoria, así corre sin infra.

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt   # (en la raíz del repo)
uvicorn app.main:app --reload         # API en http://localhost:8000/docs
pytest                                # verificación: 16/16 verde
```

Cuando traigas tu backend real, reemplazá este ejemplo por tu estructura (la de arriba) — los tests en `tests/` te muestran qué reglas mantener verificadas.
