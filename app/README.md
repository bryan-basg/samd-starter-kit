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
