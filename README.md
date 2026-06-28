<div align="center">

# 🏥 SaMD Starter Kit

**A starter kit to build Software as a Medical Device (SaMD) with a team of AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![IEC 62304](https://img.shields.io/badge/IEC%2062304-software%20lifecycle-blue)](docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md)
[![ISO 14971](https://img.shields.io/badge/ISO%2014971-risk%20management-blue)](docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md)
[![WCAG 2.1 AA](https://img.shields.io/badge/WCAG%202.1-AA-blueviolet)](CLAUDE.md)
[![Built with Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-8A2BE2)](https://claude.com/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**🌎 English · [Español](README.es.md)**

</div>

---

This kit distills the experience of a real SaMD Class B project: a team of specialized AI agents, the compliance ruleset, multi-agent workflows, the persistent memory structure, and a complete regulatory Design History File (DHF) — all generalized into ready-to-adapt templates.

This repository is **not an application**. It is the **scaffolding and methodology** so that you (and your AI coding agent, such as Claude Code) can start a SaMD from scratch without reinventing the compliance, testing, and traceability process that **IEC 62304 + ISO 14971** demand.

## 🚀 60-second quickstart

```bash
git clone https://github.com/bryan-basg/samd-starter-kit my-medical-device
cd my-medical-device
rm -rf .git && git init        # start your own history
bash scripts/init_kit.sh       # fill the {{...}} placeholders with your project
```

Then classify your software (Class A/B/C) in `docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md` — it drives the rigor of everything else.

## 🎯 Who is this for?

- **A solo founder or startup** building health software who doesn't want to discover regulatory compliance the hard way.
- **A medtech / medical-device company** that wants a ready process scaffold (IEC 62304 + ISO 14971) with traceability by design.
- **Teams working with AI agents** (Claude Code) who want a crew of specialists with the SaMD rules pre-loaded.

## 📦 What's inside

| Piece | Path | What it is |
|---|---|---|
| **Agent ruleset** | `CLAUDE.md` | "Rule 0" (SaMD is the absolute priority) + how the agent works, testing, multi-agent orchestration. |
| **Team of 8 agents** | `.claude/agents/` | Per-layer specialists: `backend`, `frontend`, `db-architect`, `cloud-ops`, `qa-mutation`, `security-samd`, `samd-audit-trace`, `docs-dhf`. |
| **Command + skill** | `.claude/commands/`, `.claude/skills/` | `samd-trace`: impact analysis (§5.6) before declaring anything "fixed". |
| **Multi-agent workflow** | `.claude/workflows/` | `samd-review`: diff review across risk dimensions with adversarial verification. |
| **Development protocol** | `.agents/workflows/` | Agent-agnostic mirror of the stable process. |
| **Memory** | `memory/MEMORY.md` | The agent's persistent memory structure. |
| **Example RFCs** | `docs/05_design_decisions/RFC-001..003` | Three real SaMD decisions already written (encryption at rest, JWT-only identity, external scheduler). |
| **Design History File** | `docs/` | 30+ regulatory & process templates: ISO 14971, SaMD traceability, IEC 62304 plan, safety classification, SOUP, clinical evaluation/validation, post-market, IFU, privacy, runbooks. |
| **Working CI/CD** | `.github/workflows/` | `ci.yml`, `security-audit.yml` (Trivy+Semgrep), `nightly-mutation.yml` (Stryker). Reference stack: React+TS / Python+FastAPI. |

## 🧭 The idea: compliance by design, not as a separate sprint

The core rule is **Rule 0**: *every technical decision is subordinate to SaMD compliance*. In practice, four habits the agent team enforces on its own:

1. **Mandatory traceability** (§5.1/§5.7): every clinical/schema/security change is recorded in the DHF in the same PR.
2. **Demonstrable verification** (§5.7): nothing is declared "green" without running the linked tests and reporting numbers.
3. **Explicit fail-safe** (ISO 14971): when something fails, it degrades safely and predictably — never silently.
4. **Impact analysis before fixing** (§5.6): a bug is fixed after reviewing ALL consumers of the symbol, not just the file where it was reported.

## 🤖 The 8-agent team

| Agent | Layer | Use it for |
|---|---|---|
| `backend` | API + logic | Routers, services, schemas, auth, audit, resilience fuses, tests. |
| `frontend` | UI + client | Components, hooks, DAOs, offline-first sync, UI tests, mutation, neuro-UX. |
| `db-architect` | Data | Schemas, migrations, connection pool, at-rest encryption, access rules. |
| `cloud-ops` | Platform | Compute, managed DB, scheduler, secret manager, hosting, CI/CD, deploys. |
| `qa-mutation` | Testing | Mutation testing waves, mutant killers, scoped configs, score ratchet. |
| `security-samd` | Security | SAST (Trivy+Semgrep+fuzz), encryption, key management, JWT-only, audit. |
| `samd-audit-trace` | Regulatory (audits) | Audits a changeset against IEC 62304 §5.1/§5.7 + ISO 14971. Reports gaps. |
| `docs-dhf` | Regulatory (writes) | Materializes DHF updates: Master Map, risk matrix, traceability, RFCs. |

## ✅ Hard rules the kit enforces

- No one commits or pushes without the owner's explicit OK.
- The mutation engine never runs in parallel with agents writing tests.
- Adversarial verification is mandatory on clinical/security findings before acting.
- Identity comes only from the token (JWT-only) — never `user_id` from the client.
- Errors never expose tracebacks to the user — empathetic messages + correct HTTP code.

## 📐 Standards covered

IEC 62304 (medical software lifecycle) · ISO 14971 (risk management) · ISO 13485 (QMS) · IEC 62366 (usability) · WCAG 2.1 AA (accessibility) · GDPR + HIPAA (health data privacy/security).

## ⚠️ What this is NOT

This kit is a **process scaffold**, not regulatory advice and not a guarantee of certification. Safety classification, clinical evidence, and approval of a medical device require the judgment of regulatory professionals and, depending on the market, a Notified Body or the relevant health authority.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports: privately, see [SECURITY.md](.github/SECURITY.md). Be kind: [Code of Conduct](CODE_OF_CONDUCT.md).

## 📄 License

[MIT](LICENSE). Built distilling the experience of a real Class B SaMD project.
