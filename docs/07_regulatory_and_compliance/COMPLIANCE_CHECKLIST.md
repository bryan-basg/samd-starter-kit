**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

# Compliance Checklist — GDPR Art.32 + HIPAA Security Rule

> Checklist operativo **control-por-control** para **{{PROJECT_NAME}}** (SaMD
> {{SAMD_CLASS}}, uso previsto: {{INTENDED_USE}}). Cada salvaguarda lista
> **dónde se verifica en el código** mediante un placeholder `<archivo:línea>`
> que el equipo rellena al implementar. Responsable: {{OWNER}}.
>
> Estados: `[ ]` pendiente · `[~]` parcial · `[x]` verificado.
> Stacks: backend {{BACKEND_STACK}} · frontend {{FRONTEND_STACK}} ·
> datos {{DB_STACK}} · cloud {{CLOUD_STACK}}.

---

## A. GDPR Artículo 32 — Seguridad del tratamiento

### A.1 Seudonimización y cifrado (Art.32.1.a)

- [ ] **Cifrado en reposo** de datos personales/de salud (AES-256 o superior).
  Verificación: `<app/models/types.py:línea>` (tipo `EncryptedString` o equivalente).
- [ ] **Cifrado en tránsito** TLS 1.2+ forzado; sin downgrade a HTTP.
  Verificación: `<app/main.py:línea>` (HSTS / redirect) + config {{CLOUD_STACK}}.
- [ ] **Gestión de claves** vía secret manager (NUNCA hardcodeadas ni reusando
  el `SECRET_KEY` de la app). Verificación: `<app/core/config.py:línea>`.
- [ ] **Seudonimización** antes de enviar datos a terceros (IA, analytics).
  Verificación: `<app/services/<pseudonymize>.py:línea>`.

### A.2 Confidencialidad, integridad, disponibilidad, resiliencia (Art.32.1.b)

- [ ] **Identidad desde el token verificado**, nunca desde body/query.
  Verificación: `<app/dependencies.py:línea>` (`get_current_user`).
- [ ] **Autorización por recurso** (anti-IDOR): cada acceso valida ownership.
  Verificación: `<app/routers/<recurso>.py:línea>`.
- [ ] **Fail-safe explícito** ante fallo de dependencia (BD/IA/red): degradación
  predecible, sin tracebacks al cliente. Verificación: `<app/core/error_handlers.py:línea>`.
- [ ] **Rate limiting / circuit breakers** en endpoints sensibles.
  Verificación: `<app/middleware/<rate_limit>.py:línea>`.
- [ ] **Cabeceras de seguridad** (CSP, COOP, Permissions-Policy, X-Content-Type-Options).
  Verificación: `<app/middleware.py:línea>`.

### A.3 Restauración de disponibilidad (Art.32.1.c)

- [ ] **Backups** automáticos de la BD con restauración probada.
  Verificación: config {{CLOUD_STACK}} (`<infra/backup.*:línea>`).
- [ ] **Migraciones reversibles** y aplicadas antes de publicar.
  Verificación: `<scripts/run_migrations.py:línea>` + workflow de deploy.

### A.4 Proceso de verificación y evaluación regular (Art.32.1.d)

- [ ] **SAST** (Semgrep) en CI. Verificación: `<.github/workflows/security-audit.yml:línea>`.
- [ ] **SCA / CVEs** (Trivy + Dependabot) + **SBOM**. Verificación:
  `.github/workflows/sbom.yml` + [`SBOM_MANAGEMENT_PLAN.md`](./SBOM_MANAGEMENT_PLAN.md).
- [ ] **DAST** (OWASP ZAP). Verificación: `.github/workflows/dast.yml`.
- [ ] **Fuzz de contrato** (Schemathesis). Verificación: `.github/workflows/schemathesis.yml`.
- [ ] **Detección de secretos** en todo el historial. Verificación:
  `scripts/run_gitleaks.sh` + `.gitleaks.toml`.

### A.5 Riesgos del tratamiento (Art.32.2)

- [ ] **Análisis de riesgo** vinculado a cada control en
  [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md).
- [ ] **No exposición accidental** de datos en logs (redacción de PII/PHI).
  Verificación: `<app/core/logging_conf.py:línea>`.

---

## B. HIPAA Security Rule (45 CFR Part 164)

### B.1 Salvaguardas administrativas (§164.308)

- [ ] **Análisis de riesgo** documentado (§164.308(a)(1)(ii)(A)).
  Verificación: [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md).
- [ ] **Gestión de accesos** por rol (§164.308(a)(4)).
  Verificación: `<app/dependencies.py:línea>` (roles / scopes).
- [ ] **Registro de auditoría** de accesos y mutaciones a PHI (§164.308(a)(1)(ii)(D)).
  Verificación: `<app/middleware/audit.py:línea>`.
- [ ] **Plan de respuesta a incidentes** (§164.308(a)(6)).
  Verificación: [`INCIDENT_RESPONSE_PLAN.md`](./INCIDENT_RESPONSE_PLAN.md).

### B.2 Salvaguardas físicas (§164.310)

- [ ] **Hosting con controles físicos certificados** (datacenter {{CLOUD_STACK}}).
  Verificación: contrato BAA / DPA del proveedor `<docs/.../BAA.*>`.
- [ ] **Disposición segura** de medios y datos al fin de retención.
  Verificación: [`DATA_RETENTION_POLICY.md`](./DATA_RETENTION_POLICY.md).

### B.3 Salvaguardas técnicas (§164.312)

- [ ] **Control de acceso único** por usuario (§164.312(a)(2)(i)).
  Verificación: `<app/dependencies.py:línea>` (identidad por token).
- [ ] **Logoff automático** / expiración de sesión (§164.312(a)(2)(iii)).
  Verificación: `<frontend/src/<auth>/session.ts:línea>` + TTL del token.
- [ ] **Cifrado/descifrado de PHI** (§164.312(a)(2)(iv)).
  Verificación: `<app/models/types.py:línea>`.
- [ ] **Controles de auditoría** (§164.312(b)).
  Verificación: `<app/middleware/audit.py:línea>`.
- [ ] **Integridad** — detección de alteración no autorizada de PHI (§164.312(c)(1)).
  Verificación: `<app/services/<integrity>.py:línea>` o checksums de BD.
- [ ] **Autenticación de entidad** (§164.312(d)).
  Verificación: `<app/dependencies.py:línea>` (verificación del token).
- [ ] **Seguridad en transmisión** — cifrado de PHI en tránsito (§164.312(e)(1)).
  Verificación: `<app/main.py:línea>` (TLS/HSTS).

### B.4 Notificación de brechas (Breach Notification Rule, §164.400-414)

- [ ] **Procedimiento de notificación** dentro de los plazos legales.
  Verificación: [`BREACH_NOTIFICATION_TEMPLATE.md`](./BREACH_NOTIFICATION_TEMPLATE.md).

---

## C. Cómo usar este checklist

1. Reemplazar cada `<archivo:línea>` por la referencia real al implementar el control.
2. Marcar el estado (`[ ]`/`[~]`/`[x]`) en cada revisión.
3. Todo control en `[ ]` o `[~]` debe tener una entrada de deuda asociada en el DHF.
4. Re-revisar el checklist completo en cada release y ante cambios normativos.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
