# Runbook de Deploy

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Ajustá comandos a {{CLOUD_STACK}} y {{DB_STACK}}. El deploy a producción lo autoriza el propietario.

---

## 1. Pre-checks (antes de tocar producción)

- [ ] CI completo verde en la revisión a desplegar (tests, tipos, lint, seguridad).
- [ ] Changeset auditado según `docs/03_software_development_plan/AUDIT_PROTOCOL.md` si tocó capa regulada.
- [ ] Variables de entorno nuevas registradas en el gestor de secretos y en `.env.example`.
- [ ] Migraciones revisadas: ¿alguna es **irreversible** (drop/rename de columna, cambio de tipo con pérdida)?
- [ ] Ventana de deploy acordada; propietario dio OK.
- [ ] Plan de rollback claro (sección 5).

---

## 2. Migración de base de datos

> Política: **el deploy migra solo** y **aborta el deploy si la migración falla** — producción queda protegida en la versión previa.

```
deploy ──► job de migración (espera resultado, --wait)
              │ falla ──► ABORTAR deploy, no publicar imagen nueva
              │ ok    ──► publicar servicio nuevo
```

- El servicio de runtime arranca con las migraciones **deshabilitadas** (las corre el job, no el arranque).
- **Verificar la revisión REAL aplicada**, no confiar en el "verde" del job:

```bash
<comando-ver-revision-actual-de-bd>   # ej. alembic current  (vía proxy a la BD de prod)
```

- **CUIDADO**: un CI que migra contra una BD distinta a la de producción (ej. SQLite vs el motor real) puede ocultar fallos específicos del driver. Verificar contra el motor real.

### 2.1 Backup antes de migración irreversible

> Obligatorio si la migración es destructiva/irreversible:

```bash
<comando-backup-bd>                   # snapshot/export con etiqueta + timestamp
# Verificar que el backup existe y es restaurable ANTES de migrar.
```

---

## 3. Deploy

```bash
<comando-deploy>                      # publica backend y/o frontend según target
```

- **Variables de entorno**: cuidado con comandos que **REEMPLAZAN toda la lista** de env vars en lugar de hacer merge. Usar la variante de *update/merge*, o leer el estado actual antes de setear, para no borrar variables existentes.

---

## 4. Verificación post-deploy

- [ ] Healthcheck del servicio responde OK.
- [ ] Revisión de la BD coincide con la esperada (sección 2).
- [ ] Logs estructurados sin errores/warnings nuevos en los primeros minutos.
- [ ] Smoke test de un flujo clínico crítico end-to-end.
- [ ] 100% del tráfico en la revisión nueva (si hay despliegue gradual).
- [ ] Métricas (latencia, errores, pool de BD) en rango normal.

---

## 5. Rollback

| Situación | Acción |
|---|---|
| Falla en migración | El deploy ya abortó; producción sigue en la versión previa. Investigar logs del job. |
| Falla post-deploy, schema compatible | Revertir el servicio a la revisión previa. |
| Falla post-deploy, schema incompatible | Revertir servicio + **restaurar backup** (sección 2.1) + migración de reversa verificada. |

```bash
<comando-rollback-servicio>           # apuntar tráfico a la revisión previa
<comando-restaurar-backup>            # solo si el schema cambió de forma incompatible
```

---

## 6. Notas de seguridad

- Las credenciales de cloud/BD viven en el gestor de secretos; **nunca** en el repo ni en la máquina de desarrollo.
- Tras un deploy a producción, esperar a que el CI/monitoring confirme antes de encadenar otro.

---

## 7. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |
