# Makefile — atajos a los scripts y comandos YA existentes del kit.
# No reinventa lógica: cada target delega en scripts/*.sh o en los comandos
# canónicos de CLAUDE.md ("COMANDOS CORE"). `make` sin target = `make help`.
#
# Stack de referencia: backend Python/FastAPI (app/) + frontend React/TS/Vite (frontend/).

.DEFAULT_GOAL := help

# Entorno canónico de tests del backend (idéntico a scripts/run_local_ci.sh).
TEST_ENV := TESTING=True DATABASE_URL="sqlite+aiosqlite:///:memory:"

.PHONY: help setup dev dev-backend dev-frontend test test-backend test-frontend \
        lint ci mutation security placeholders clean

help: ## Lista los targets disponibles
	@echo "SaMD Starter Kit — make targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Instala deps de backend (runtime+dev) y frontend (npm ci)
	pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm ci

dev: ## Levanta backend + frontend con hot-reload (docker compose up)
	docker compose up

dev-backend: ## Solo backend: uvicorn app.main:app --reload (puerto 8000)
	uvicorn app.main:app --reload --port 8000

dev-frontend: ## Solo frontend: Vite dev server (puerto 5173)
	cd frontend && npm run dev

test: test-backend test-frontend ## Corre toda la suite (backend + frontend)

test-backend: ## Tests del backend (pytest, SQLite en memoria)
	$(TEST_ENV) pytest -q

test-frontend: ## Tests del frontend (vitest run)
	cd frontend && npm test

lint: ## Lint + types: ruff + mypy (backend) y eslint + tsc (frontend)
	ruff check app/ --select F401,F841,F811
	mypy .
	cd frontend && npm run lint && npm run typecheck

ci: ## CI local pre-push completo -> scripts/run_local_ci.sh
	bash scripts/run_local_ci.sh

mutation: ## Mutation testing del frontend -> scripts/run_stryker.sh (pesado)
	bash scripts/run_stryker.sh

security: ## SAST/CVEs -> scripts/run_trivy.sh + scripts/run_semgrep.sh (pesado)
	bash scripts/run_trivy.sh
	bash scripts/run_semgrep.sh

placeholders: ## Verifica que no queden marcadores {{...}} sin reemplazar
	bash scripts/check_placeholders.sh

clean: ## Borra caches y builds locales (no toca node_modules ni venv)
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage .coverage.* \
		frontend/dist frontend/reports reports/ coverage/ .stryker-tmp
	find . -type d -name __pycache__ -not -path './venv/*' -prune -exec rm -rf {} + 2>/dev/null || true
