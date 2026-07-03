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

## Ejemplo ejecutable (borralo cuando traigas tu app)

Esta carpeta incluye un **cliente mínimo** (Vite + React + TS) que demuestra las reglas neuro-UX: diseño plano y contraste WCAG AA (`src/App.css`), `prefers-reduced-motion` respetado, etiquetas accesibles y tests rigurosos con vitest (`src/__tests__/`).

```bash
cd frontend
npm install
npm run dev      # cliente en http://localhost:5173
npm test         # verificación: 5/5 verde
npm run build    # tsc estricto + build de producción
```

Cuando traigas tu cliente real, reemplazá `src/` por tu estructura (la de arriba). Los configs (`tsconfig.json`, `.eslintrc.cjs`, `stryker.conf.json`) ya están listos.

### Mutation testing (opt-in)

`stryker.conf.json` viene **configurado** (gate `break: 90` — el ≥90% que exige el `CLAUDE.md`), pero el **motor NO se instala por defecto**: se ata a la versión de tu test runner, así que lo elegís vos cuando traés tu app y no infla el lockfile del esqueleto desechable con ~100 dependencias de tooling. Para activarlo:

```bash
# instalá el motor que matchee tu vitest (ver compatibilidad de @stryker-mutator)
npm i -D @stryker-mutator/core @stryker-mutator/vitest-runner
npx stryker run     # usa stryker.conf.json; falla el build si el score < 90%
```
