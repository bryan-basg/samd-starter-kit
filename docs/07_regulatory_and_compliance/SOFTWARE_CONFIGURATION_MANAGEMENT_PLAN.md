# Plan de Gestión de Configuración del Software (SCM)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** YYYY-MM-DD

> Plantilla conforme a IEC 62304 §5.1.9 (planificación de gestión de configuración) y §8 (gestión de configuración del software). Ajuste ramas, herramientas y baselines a la realidad del proyecto.

---

## 1. Propósito y alcance

Definir cómo se identifican, controlan y versionan los elementos de configuración del software (SCI) de **{{PROJECT_NAME}}**, asegurando reproducibilidad y trazabilidad conforme a IEC 62304 §8.

---

## 2. Elementos de configuración (SCI)

| SCI | Descripción | Identificación |
|---|---|---|
| Código fuente backend | {{BACKEND_STACK}} | Repositorio + hash de commit |
| Código fuente frontend | {{FRONTEND_STACK}} | Repositorio + hash de commit |
| Esquema de BD / migraciones | {{DB_STACK}} | Revisión de migración |
| Infraestructura como código | {{CLOUD_STACK}} | Versionado en repo |
| Documentación regulatoria (DHF) | `docs/` | Versión semántica del doc |
| Dependencias de terceros | Manifiestos + lockfiles | Versión pineada |
| Artefactos de release | Imágenes/binarios | Tag + digest |

---

## 3. Control de versiones

- **SCV:** <p. ej. Git>. Todo SCI versionado; nada fuera de control de versiones.
- **Versionado semántico** (MAJOR.MINOR.PATCH) para releases.
- **Secretos NUNCA** se versionan (ver `COMPLIANCE_AND_SECURITY_MASTER.md` §5.7).

---

## 4. Estrategia de ramas

| Rama | Propósito | Protección |
|---|---|---|
| `main` / release | Estado estable, desplegable | Protegida; PR + revisión + CI verde |
| Ramas de feature | Trabajo en curso | Se integran vía PR |
| Ramas de hotfix | Correcciones urgentes | PR acelerado + CI |

Reglas: PR obligatorio, al menos una revisión, CI (build + tests + SAST) en verde antes de fusionar. Sin push directo a la rama protegida.

---

## 5. Gestión de cambios

1. Todo cambio nace de un ítem rastreable (issue/ticket/problema).
2. **Análisis de impacto** (IEC 62304 §5.6): identificar todos los consumidores del símbolo/esquema modificado antes de aprobar.
3. Revisión por pares vía PR.
4. Verificación: tests vinculados ejecutados y reportados (§5.7).
5. Trazabilidad documental actualizada en el mismo cambio (DHF / matriz de trazabilidad).
6. Aprobación e integración.

---

## 6. Identificación de configuración y baseline

- Cada **release** establece un **baseline**: conjunto inmutable de SCI identificados por sus versiones/hashes.
- El baseline incluye: hash de código, versiones de dependencias (lockfile), revisión de BD aplicada, versión de docs DHF y digest del artefacto desplegado.
- Un baseline aprobado permite reconstruir exactamente la versión liberada.

| Campo del baseline | Valor (ejemplo) |
|---|---|
| Versión de release | `<completar>` |
| Hash de commit | `<completar>` |
| Revisión de migración BD | `<completar>` |
| Digest de artefacto | `<completar>` |
| Versión DHF asociada | `<completar>` |
| Fecha | YYYY-MM-DD |

---

## 7. Build y release reproducibles

- Dependencias pineadas (lockfiles); builds deterministas.
- Pipeline CI/CD documentado; el deploy registra la revisión realmente aplicada (no se asume el verde sin verificar).

---

## 8. Auditoría de configuración

Verificación periódica de que el estado desplegado coincide con el baseline aprobado y de que no existen SCI fuera de control de versiones.

---

## 9. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
