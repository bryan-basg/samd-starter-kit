# Security Policy

This project is a **template kit** for building Software as a Medical Device (SaMD), not a running service. As such, "vulnerabilities" here are predominantly **insecure defaults, unsafe example configurations, or bad practices baked into the templates** that could propagate into downstream medical devices if copied without review. We treat these with the same seriousness as a live exploit, because a flawed default in a SaMD scaffold can become a patient-safety or data-protection issue in production.

## Supported Versions

Security fixes are applied to the latest minor release line. Older lines are not patched; please upgrade.

| Version | Supported          |
| ------- | ------------------ |
| latest `main` | :white_check_mark: |
| most recent tagged release | :white_check_mark: |
| previous releases | :x:                |

## Reporting a Vulnerability

**Do not open a public GitHub issue, Discussion, or pull request for a security report.** Public disclosure before a fix is available can expose every downstream device built from the affected template.

Report privately to **{{OWNER}}** using one of:

1. GitHub's **private vulnerability reporting** ("Report a vulnerability" under the Security tab), preferred.
2. A direct, private message to **{{OWNER}}**.

Please include:

- The affected file(s) and template(s).
- A description of the insecure default, bad practice, or weakness.
- The realistic impact on a device built from the template (e.g., exposed PHI, weak crypto default, missing auth gate, secret leakage).
- A suggested remediation, if you have one.

## Disclosure Timeline

| Stage | Target |
| ----- | ------ |
| Acknowledgement of report | within **3 business days** |
| Initial assessment & severity triage | within **7 business days** |
| Fix or mitigation in `main` | within **30 days** for high/critical; best-effort for lower severity |
| Coordinated public disclosure | after a fix ships, by mutual agreement with the reporter |

We follow coordinated disclosure: we ask that you give us a reasonable window to remediate before any public write-up, and we will credit reporters who wish to be named.

## Scope

In scope:

- Insecure defaults or example values in templates, agent definitions, workflows, and configuration.
- Bad security practices in scaffolding that downstream adopters are likely to copy verbatim (hardcoded secrets, permissive CORS, missing input validation, weak or absent encryption-at-rest defaults, identity accepted from request body, tracebacks returned to clients).
- Insecure CI/CD or dependency defaults shipped by the kit.

Out of scope:

- Vulnerabilities in a device **you built** from this kit — those are your responsibility to manage under your own quality system.
- Issues in third-party dependencies (report upstream; we will update pins as fixes land).

## Full Process

The complete incident-response process this kit proposes — including triage roles, severity classification, regulatory notification considerations, and post-incident review — is documented in [`docs/07_regulatory_and_compliance/INCIDENT_RESPONSE_PLAN.md`](../docs/07_regulatory_and_compliance/INCIDENT_RESPONSE_PLAN.md).
