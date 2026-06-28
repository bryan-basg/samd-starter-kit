**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** vX.Y · **Fecha:** YYYY-MM-DD

# SBOM Management Plan

> Plan de generación, almacenamiento y revisión del **Software Bill of
> Materials (SBOM)** del producto **{{PROJECT_NAME}}** (SaMD {{SAMD_CLASS}}).
> Uso previsto del producto: {{INTENDED_USE}}. Responsable del plan: {{OWNER}}.

## 1. Propósito

Establecer el procedimiento formal para **producir, almacenar, auditar y
comunicar** el SBOM del producto. El SBOM es evidencia regulatoria obligatoria:

- **IEC 62304 §8** (gestión de software de mantenimiento) + **§5.1.4** define
  `SOUP (Software of Unknown Provenance)` y obliga a documentar cada componente
  de terceros individualmente.
- **IEC 81001-5-1 §4.1.5** exige inventario completo de componentes y
  trazabilidad de cambios para todo software médico.
- **FDA Cybersecurity in Medical Devices Guidance (Sep 2023) §V.B** requiere el
  SBOM en submissions premarket (510(k), De Novo, PMA).
- **EU Cyber Resilience Act (CRA)** lo impone como entregable de cadena de
  suministro de software con productos digitales en el mercado europeo.
- **US Executive Order 14028** y **NTIA Minimum Elements for an SBOM (2021)**
  fijan el contenido mínimo (suppliers, componentes, versiones, relaciones).

## 2. Alcance

Cubre todo software que se ejecuta dentro del producto final:

- **Backend** ({{BACKEND_STACK}}): dependencias Python declaradas en
  `requirements.txt` + el grafo transitivo real instalado en el venv.
- **Frontend** ({{FRONTEND_STACK}}): dependencias de runtime en
  `frontend/package-lock.json` (se omite `dev` por defecto).
- **Infraestructura de despliegue** ({{CLOUD_STACK}}): imágenes base de
  contenedor y dependencias de sistema se inventarían vía el escaneo SCA
  (Trivy) y se referencian, no se duplican, en este SBOM de aplicación.

Fuera de alcance: tooling de desarrollo no embarcado (linters, mutation
testing) salvo que se solicite un SBOM `-with-dev`.

## 3. Formato y herramientas

| Capa | Herramienta | Formato | Comando |
|------|-------------|---------|---------|
| Python | `cyclonedx-py environment` | CycloneDX 1.5 JSON | `scripts/generate_sbom.sh --backend` |
| Node | `@cyclonedx/cyclonedx-npm` | CycloneDX 1.5 JSON | `scripts/generate_sbom.sh --frontend` |

CycloneDX 1.5 JSON es el formato canónico (legible por máquina, soportado por
los principales escáneres de CVE y aceptado por FDA/CRA). El script produce
además un resumen Markdown legible por humanos.

## 4. Procedimiento de generación

1. **Local**: `bash scripts/generate_sbom.sh` (requiere venv activo + lockfile
   del frontend íntegro). Salida a `sbom/` con archivos fechados + punteros
   estables `sbom-latest-{backend,frontend}.json`.
2. **CI**: el workflow `.github/workflows/sbom.yml` regenera el SBOM ante
   cualquier cambio de lockfiles (paths-filter) + cron semanal de detección de
   drift. Falla si el SBOM sale vacío (guard de 0 componentes).
3. **Reproducibilidad**: `npm ci` (no `npm install`) y `--output-reproducible`
   garantizan que el mismo lockfile produzca el mismo SBOM.

## 5. Almacenamiento y versionado por release

- El SBOM se **versiona en Git** dentro de `sbom/` → snapshot permanente y
  auditable (la retención larga regulatoria NO depende de artifacts de CI).
- En **cada release** se etiqueta el SBOM con la versión del producto y se
  archiva junto al registro de release (IEC 62304 §5.7.4 / §8 release records).
- Los artifacts de CI son copias de conveniencia con retención de 30 días.

## 6. Revisión y respuesta a vulnerabilidades

1. Cada SBOM nuevo se cruza con feeds de CVE: **Trivy** (imágenes + deps),
   `pip-audit`, `npm audit` y **Dependabot**.
2. Todo hallazgo **HIGH/CRITICAL** se registra en
   [`ISO_14971_RISK_MATRIX.md`](./ISO_14971_RISK_MATRIX.md) con plazo de
   remediación y propietario.
3. El diff SBOM-vs-baseline (componentes añadidos/removidos/cambiados) se
   adjunta al PR que toca dependencias → trazabilidad de cambios de SOUP.

## 7. Roles y cadencia

| Actividad | Responsable | Cadencia |
|-----------|-------------|----------|
| Generación automática | CI (`sbom.yml`) | Por cambio de deps + semanal |
| Revisión de CVEs | {{OWNER}} / security | Semanal + ante cada release |
| Archivado por release | {{OWNER}} | Cada release |
| Auditoría del plan | {{OWNER}} / QA regulatorio | Anual o ante cambio normativo |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
