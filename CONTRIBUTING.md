# Contributing — {{PROJECT_NAME}}

**English · [Español](CONTRIBUTING.es.md)**

> Welcome. This project is **Software as a Medical Device (SaMD) Class {{SAMD_CLASS}}** under IEC 62304 + ISO 14971. The change process is controlled and is **regulatory evidence** (IEC 62304 §5/§8): it isn't bureaucracy, it's what makes certification possible. This page is the front door; the detail lives in the documents linked below.

## The non-negotiable rules

1. **No one commits or pushes without the owner's explicit OK ({{OWNER}}).** Before each commit, report which files go up and wait for authorization. Destructive operations (`reset --hard`, `push --force`, deleting branches) require a separate OK.
2. **Green tests with reported numbers.** Nothing is declared "done" without running the tests tied to the change and reporting the results (SaMD §5.7). "Renders without crashing" is not a valid test.
3. **The user never sees a traceback.** On-screen errors: empathetic messages + the correct HTTP code. A user in crisis must not see "500 Internal Server Error".
4. **Traceability in the SAME PR.** If you touch a clinical algorithm, a schema, a business rule, or a security flow, you update the DHF (TECHNICAL_DEBT_SUMMARY + Master Map + Risk Matrix / TRACEABILITY when applicable) in the same PR, not in a separate sprint.
5. **Identity from the token only.** Never accept `user_id` from the body, query, or headers — only from the decoded token.
6. **Impact analysis before declaring "fixed".** Review ALL consumers of the symbol you touched (global `grep`), not just the file where the bug was reported.

## Workflow

```
1. Branch from your default branch:  git switch -c feat/my-change
2. Implement + tests       (delegate to the agents in .claude/agents/ when the layer fits)
3. Local CI green:         bash scripts/run_local_ci.sh
4. Report the files to commit and wait for the owner's OK
5. Open the PR; CI runs lint + types + tests + contract drift + traceability
6. Before closing a large block: bash scripts/audit_project_state.sh
```

## Definition of Done

1. Passes linting + local CI (`scripts/run_local_ci.sh`).
2. Tied tests green, numbers reported.
3. Technical debt reduced by at least one point (Boy Scout rule).
4. Documentation up to date (Master Map, TECHNICAL_DEBT, TRACEABILITY, and Risk Matrix when applicable).
5. Accessible UI (WCAG AA contrast, flat design, canonical modals).
6. Change communicated to the owner with a clear rationale and explicitly authorized.

## Reference documents

- **`CLAUDE.md`** — the agent ruleset: Rule 0, backend/frontend standards, multi-agent orchestration, testing.
- **`.agents/workflows/protocolo_desarrollo.md`** — the stable, agent-agnostic development process.
- **`docs/03_software_development_plan/DEVELOPMENT_GUIDE_COMPLETE.md`** — the complete guide: setup, commands, standards, PR flow.
- **`docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md`** — the SaMD-grade verification strategy.
- **`docs/03_software_development_plan/AUDIT_PROTOCOL.md`** — how a changeset/phase is audited against SaMD.
- **`docs/05_design_decisions/RFC-TEMPLATE.md`** — template for proposing a structural decision.

## Reporting a security issue

Vulnerabilities are NOT reported in public issues. Contact {{OWNER}} privately. See `docs/07_regulatory_and_compliance/INCIDENT_RESPONSE_PLAN.md`.
