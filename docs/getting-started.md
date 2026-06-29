# Getting started

> The canonical, always-up-to-date guide lives at the repo root in
> **[`GETTING_STARTED.md`](https://github.com/bryan-basg/samd-starter-kit/blob/main/GETTING_STARTED.md)**.
> This page is a short mirror so the guided path is reachable from the docs site.

The kit is a **process scaffold**, not an application — scaffolding and methodology
so you (and your AI coding agent) can start a SaMD from scratch without reinventing
the compliance, testing and traceability process that **IEC 62304 + ISO 14971** demand.

## The 60-second start

```bash
git clone https://github.com/bryan-basg/samd-starter-kit my-medical-device
cd my-medical-device
rm -rf .git && git init -b main   # start your own history
bash scripts/init_kit.sh          # interactive & re-runnable: fills the {{...}} placeholders
```

## The guided path

The full guide walks you through, in order:

1. **Classify your software** (Class A / B / C) — this fixes which activities and
   documents actually apply to *you*. See
   [Software Safety Classification](07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md).
2. **Fill the four foundation documents** — start with the
   [Master Map](00_master/MASTER_MAP.md) and
   [Vision & Governance](01_governance_and_strategy/VISION_AND_GOVERNANCE.md).
3. **Wire your stack** and learn the daily loop with the
   [agent team and SaMD flow](02_architecture_and_design/AGENT_TEAM_AND_FLOW.md).
4. **Adopt the verification discipline** — see the
   [Testing Strategy](03_software_development_plan/COMPLETE_TESTING_STRATEGY.md).

For the complete step-by-step, open the canonical
[**`GETTING_STARTED.md`**](https://github.com/bryan-basg/samd-starter-kit/blob/main/GETTING_STARTED.md).

---

**Navigation:** [DHF Index](README.md) · [Master Map](00_master/MASTER_MAP.md) · [Roadmap](roadmap.md)
