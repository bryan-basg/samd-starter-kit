# SBOM Summary — 2026-06-30

> Generado por `scripts/generate_sbom.sh` el 2026-06-30T16:55:58-0500.
> Proyecto: {{PROJECT_NAME}} · Clase SaMD: {{SAMD_CLASS}}.
> Formato fuente: CycloneDX 1.5 JSON.
> Marco regulatorio: IEC 81001-5-1 §4.1.5 + FDA Cybersecurity 2023 + EO 14028 + EU CRA.

## Totales

| Ecosistema | Archivo CycloneDX | Componentes |
|------------|-------------------|-------------|
| Backend (Python) | sbom-backend-cyclonedx-2026-06-30.json | N/A |
| Frontend (Node)  | sbom-frontend-cyclonedx-2026-06-30.json | 5 |

## Proximos pasos

1. Cruzar con feeds de CVE (Trivy + npm audit + pip-audit + Dependabot).
2. Registrar HIGH/CRITICAL en `ISO_14971_RISK_MATRIX.md` con plazo de remediacion.
3. Versionar este SBOM en Git para trazabilidad SaMD §5.7.

Ver `docs/07_regulatory_and_compliance/SBOM_MANAGEMENT_PLAN.md` para la politica completa.
