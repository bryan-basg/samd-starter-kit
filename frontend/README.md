# frontend/ — Cliente {{FRONTEND_STACK}}

Carpeta de arranque del cliente. El agente `frontend` trabaja acá bajo las reglas neuro-UX + WCAG 2.1 AA del `CLAUDE.md`.

Estructura sugerida:

```
frontend/src/
├── features/        # agrupado por dominio clínico (crisis, onboarding, dashboard...)
├── components/common/   # Modal canónico, ConfirmDialog, sistema de iconos, NotifyService
├── services/        # DAOs HTTP + motor de sync offline-first (outbox)
├── hooks/           # fetch+cache, presencia, onboarding
└── themes/          # diseño plano, contraste WCAG AA
```

Reglas duras (ver `.claude/agents/frontend.md`): offline-first por outbox, librería de fetch+cache obligatoria, `prefers-reduced-motion` incondicional, diseño plano (sin glassmorphism), sin emoji en aria-labels críticos, no tocar componentes compartidos sin pedido explícito.
