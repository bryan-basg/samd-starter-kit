---
paths:
  - "app/**/*.py"
  - "alembic/**/*.py"
  - "scripts/**/*.py"
---

# ESTÁNDARES DEL BACKEND (consecuencia SaMD §5.5 — implementación robusta)

> Regla **por-capa** del cerebro SaMD; las reglas **transversales** viven en `CLAUDE.md`. Esta regla carga sola cuando el agente lee/edita el backend. Es una **CONSECUENCIA PRÁCTICA de la Regla 0** (cumplimiento SaMD): no es opcional. Capa/agente dueño: `backend` (+ `db-architect` para datos/migraciones, `clinical-algorithms` para la lógica clínica).
>
> **Adaptá los `paths:` de arriba y los valores de abajo a tu stack real** (`{{BACKEND_STACK}}` / `{{DB_STACK}}`). Lo que sigue son los principios estables; los valores concretos (pools, tiers, env vars) deben citar `archivo:línea` del código real, no recopiarse.

* **Identidad por token, nunca por cliente**: el `user_id` depende exclusivamente del token/JWT decodificado por el proveedor de auth. NUNCA aceptes `user_id` desde body, query ni headers custom — es un vector de escalada garantizado.
* **Asincronía máxima**: prohibidas funciones I/O bloqueantes en el path de request. Usá el modelo async del framework.
* **Tipado estricto**: prohibido `any`. Validación de esquemas obligatoria. El type-checker estricto pasa en CI.
* **Errores en API**: NUNCA devolver tracebacks, logs técnicos, metadatos internos de BD o SQL al cliente. Solo mensajes empáticos + código HTTP correcto.
* **Cifrado en reposo**: campos PII/PHI cifrados con AES-256-GCM (o equivalente auditado). La clave de cifrado vive en un gestor de secretos / KMS — NUNCA hardcodeada, NUNCA reusando otra clave.
* **Migraciones de schema controladas**: el deploy debe migrar de forma atómica y abortar si falla (prod protegida). **NUNCA confiar en el verde de una migración sin verificar la revisión real aplicada en el entorno destino** — un CI que migra contra un motor distinto al de producción (p. ej. SQLite vs Postgres) oculta fallos que solo aparecen en prod.
* **Variables de entorno en producción**: viven en el gestor de secretos, no en el `.env` del repo. Cuidado con comandos de deploy que **reemplazan** la lista completa de env vars en vez de hacer merge.
* **Techo de conexiones alineado con el tier**: si tenés varios motores/pools (principal, logs, jobs), el **techo agregado de TODOS** debe ser menor que las conexiones que da tu tier de BD, contando el número máximo de instancias. Los pools secundarios **SÍ cuentan** aunque parezcan marginales. Valores vivos = código; si subís el tier, reevaluá los tres juntos.
* **Auditoría**: persistir a BD las mutaciones (POST/PUT/DELETE/PATCH); las lecturas van a logging estructurado para no consumir el pool. Compatible con SaMD §5.7 (trazabilidad de cambios).
* **`.env.example` cubre TODO el código vivo**: si añadís una var nueva en config o leés por entorno en services/middleware, **DEBES** añadirla a `.env.example` con un comentario SaMD-aware. Lo mismo del lado frontend con su propio `.env.example`. El onboarding de devs no se rompe en silencio.
* **Jobs programados**: preferí un scheduler externo al proceso de la API (un scheduler embebido se duplica con cada instancia). Si existe el embebido, que venga apagado por default detrás de una env var y se encienda solo en dev local.
