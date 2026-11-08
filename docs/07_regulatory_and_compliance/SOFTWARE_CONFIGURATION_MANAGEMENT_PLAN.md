# Plan de Gestión de Configuración del Software (SCM)

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.9 · **Fecha:** 2026-11-07

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
| Reglamento del agente (gobernanza) | `CLAUDE.md` (core) + `.claude/rules/` (por capa y transversales) + `.claude/output-styles/orquestador.md` (estilo de la sesión principal, activado en `.claude/settings.json`) + `AGENTS.md` (entrada para otras herramientas) | Repositorio + hash de commit |
| Equipo de agentes y procedimientos | `.claude/agents/`, `.claude/commands/`, `.claude/skills/`, `.claude/workflows/` | Repositorio + hash de commit |
| Dependencias de terceros | Manifiestos + lockfiles | Versión pineada |
| Artefactos de release | Imágenes/binarios | Tag + digest |

### 2.1 El reglamento se reparte según QUIÉN lo carga

Cada pieza del reglamento entra en el contexto de un conjunto distinto de sesiones, y lo que no hace falta en un sitio se paga en cada turno ahí:

| Pieza | La cargan | Contenido |
|---|---|---|
| `CLAUDE.md` + reglas transversales de `.claude/rules/` (sin `paths:`) | Sesión principal **y** cada subagente, en cada turno | Lo que obedecen todos: Regla 0, reglas comunes (git, zonas, diagnóstico, memoria), reglas duras de ejecución, comandos. |
| Reglas path-scoped de `.claude/rules/` | Quien toca un archivo de esa capa | Estándares de la capa. |
| `.claude/output-styles/orquestador.md` | Solo la sesión principal (y un *fork*, que hereda su prompt) | Preferencias del dueño (idioma, modo tutor, antes de actuar), orquestación (matriz de agentes, reglas A-F, anti-drift) y sesiones paralelas. |

**Activación:** `"outputStyle": "Orquestador SaMD"` en `.claude/settings.json`; el valor debe coincidir EXACTO con el `name:` del frontmatter del estilo, porque un nombre que no coincide cae en silencio al estilo por defecto. El estilo lleva `keep-coding-instructions: true` para no perder las instrucciones de ingeniería de software del prompt de sistema. **Red de seguridad:** `CLAUDE.md` §REGLAS COMUNES le ordena a la sesión principal leer el estilo entero si no lo tiene entre sus instrucciones. **Guardián:** `tests/test_estilo_orquestador_enchufado.py` (el nombre coincide, el estilo trae sus secciones y no quedaron duplicadas en `CLAUDE.md` ni en `.claude/rules/`).

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

**Equipo de un solo desarrollador.** Si el proyecto lo lleva una sola persona, la tabla de arriba se adapta en vez de simularse: **la revisión entre pares no existe**, y un PR que su propio autor aprueba es papeleo, no un control. Lo que **sí se conserva** porque son controles reales:

- **CI en verde antes de que el cambio quede en `main`** — la puerta técnica no depende de cuánta gente sea el equipo.
- **Commits atómicos con mensaje trazable** (qué cambió, por qué, con qué números se verificó): el historial de git ES el registro de control de cambios ante un auditor.
- **La revisión asistida sustituye a la humana** en los cambios no triviales: pasar el diff por `/code-review` y `/security-review` antes de cerrar (ver `CLAUDE.md` §ANÁLISIS DE IMPACTO), más la verificación adversarial entre agentes para hallazgos clínicos o de seguridad.
- **Las ramas de feature siguen siendo útiles** cuando el bloque es grande o experimental — pero por aislamiento del trabajo, no como ceremonia de aprobación.

Documentá acá cuál de los dos regímenes aplica a tu proyecto. Un plan que describe un control que no se ejerce es peor que no tenerlo: el auditor lo compara contra el historial real.

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
- **El CI compila el frontend** (`npm run build` en `.github/workflows/ci.yml`, tras lint, tipos y tests): el deploy corre ese mismo build, y sin ese paso un build roto solo se descubría al desplegar.

### 7.1 Dependencias de terceros (SOUP, IEC 62304 §8)

- **Qué vigila Dependabot** (`.github/dependabot.yml`): `npm` (`frontend/`), `pip` (`requirements*.txt` de la raíz) y `github-actions`. Cada actualización entra por PR con el CI en verde; las de efecto real (versión mayor, seguridad, la librería de cifrado de PHI) se registran en el `CHANGELOG.md` con su análisis de impacto (§5.6).
- **Un piso (`>=`) no cambia lo que el CI instala**: `pip` toma la última versión que cumple el rango. Antes de dar por probado un cambio de piso se mira en el log del job qué versión se instaló de verdad; mover un **techo** (`<`) sí cambia lo instalado.
- **Las excepciones llevan su motivo y su condición de retiro** en el propio `dependabot.yml`. Se frena solo con `update-types: ["version-update:semver-major"]` y nunca con `versions:`, que también silenciaría los avisos de seguridad.
- **Paquetes que se declaran entre sí viajan juntos**: `react`, `react-dom` y sus tipos son un solo grupo (un PR); subirlos por separado rompe `npm ci` por dependencias de pares.
- **Una sola versión mayor de Node** en todos los sitios: `ci.yml`, `deploy.yml`, `nightly-mutation.yml`, `sbom.yml`, `docker-compose.yml`, `.devcontainer/devcontainer.json` y `frontend/package.json` (`engines` y `@types/node`). Cambiar de major obliga a tocar los siete en el mismo PR y a retirar la excepción de `@types/node` en `dependabot.yml`.
- **Lockfile del frontend con npm 11** (el de Node 24): npm 10 borra las marcas `libc` de los binarios nativos y el lockfile pierde la distinción glibc/musl. Regenerarlo con `npx -y npm@11 install --package-lock-only --ignore-scripts` y comprobar que `grep -c '"libc"' package-lock.json` da el mismo número antes y después.
- **`cooldown` de 14 días en los tres ecosistemas** de `dependabot.yml`: Dependabot espera ese tiempo desde que se publica una versión antes de proponerla, porque una versión recién publicada es justo la que puede traer un paquete comprometido (cadena de suministro). Frena SOLO las actualizaciones de versión; los avisos de seguridad (CVE) llegan igual y de inmediato.
- **Acciones de CI pineadas a SHA de 40 caracteres, y un test lo vigila** (`tests/test_workflows_pineados_a_sha.py`): el conjunto se deriva de los workflows en disco (uno nuevo entra solo) y el filtro `backend` de `ci.yml` incluye `.github/workflows/**`, para que un PR que cambia otro workflow dispare el guardián. Una regla en prosa que nada comprueba se erosiona sin ruido.
- **`mutmut` fijado a `==2.5.1`** (`requirements-dev.txt`) y con `ignore` de versión mayor en `dependabot.yml`: mutmut 3 eliminó `--paths-to-mutate` y `--runner` y cambió el cache, así que subirlo solo rompería la mutación backend sin aviso. `tests/test_mutmut_gate.py` ancla el pin (`MUTMUT_PIN` de `scripts/run_mutmut.sh` debe coincidir con `requirements-dev.txt`). Condición de retiro: migrar `run_mutmut.sh` y `check_mutmut_score.py` a mutmut 3.

---

## 8. Auditoría de configuración

Verificación periódica de que el estado desplegado coincide con el baseline aprobado y de que no existen SCI fuera de control de versiones.

---

## 9. Control de cambios del documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | YYYY-MM-DD | {{OWNER}} | Versión inicial de plantilla. |
| v1.1 | 2026-07-05 | Claude Sonnet 5 | Sincronización de reglas de Boy Scout (oportunista) y mutation score. Agregado comando `commit-selectivo-parcial`. |
| v1.2 | 2026-08-07 | Claude Opus 5 | El reglamento del agente pasa a ser SCI explícito (`CLAUDE.md` + `.claude/`). Reestructuración de gobernanza: core + 8 reglas en `.claude/rules/` (4 path-scoped, 4 transversales). Equipo ampliado a 12 agentes (`clinical-algorithms`, `e2e-integration`). Endurecida la regla de commit selectivo (`git commit -- <rutas>`) y agregado el presupuesto de escritura de documentos vivos. |
| v1.3 | 2026-08-23 | Claude Opus 5 | Sincronización de gobernanza con el proyecto de referencia. **Corregido un control que no controlaba**: el link-checker cross-doc que el reglamento mandaba correr (`grep` de enlaces) no verificaba nada — los 5 sitios pasan a invocar `scripts/check_doc_links.sh`, que es el mismo verificador que corre el CI. Nuevas skills `/tandas-agentes` (presupuesto y parada obligatoria entre tandas de subagentes) y `/memoria`. `github-actions.md` suma §Los rojos que NO se ven (job centinela, relojes anidados, `cancel-in-progress` gateado por evento, `continue-on-error`) y §Mediciones y umbrales. Seis workflows con `schedule` dejaban de cancelar sus propias corridas programadas. |
| v1.4 | 2026-10-12 | Claude Sonnet 5 | Sincronización de gobernanza con el proyecto de referencia. **Corregida una ambigüedad real** en `.claude/rules/orquestacion.md` regla dura 2: el paréntesis "los agentes en la nube NO entran acá" podía leerse como que un SUBAGENTE corriendo en la máquina del dueño también quedaba exento — se reemplaza por una aclaración completa (lo que exime es el proceso en la nube que NO toca la máquina local, no el origen de la orden) y se la respalda con un candado mecánico: nuevo hook `PreToolUse` (`.claude/settings.json` + `.claude/scripts/candado_suite_completa.py`) que deniega a un subagente correr la suite completa o un proceso pesado vía `Bash`. **Corregido el mismo bug que el proyecto de referencia encontró en el suyo**: la palanca de costo/velocidad (enrutar `model:` por agente) estaba escrita en prosa pero nunca cableada — los 12 agentes de `.claude/agents/` no declaraban `model:` en su frontmatter; ahora todos lo declaran (`opus` para `clinical-algorithms` y `security-samd`, `sonnet` para el resto). `github-actions.md` suma 2 modos de fallo a los "rojos que no se ven" (ahora 6, no 4): el job centinela necesita la misma puerta anti-fork que los jobs que vigila en runner `self-hosted`, y `semgrep` sale con exit 0 aunque haya hallazgos salvo que lleve `--error`. Nueva skill `/ola-auditoria` (clasificación de hallazgos en cubos 🔴/🟡/🧊 — la prioridad nominal P1/P2/P3 no dice el cubo) para contrarrestar la tendencia medida de un agente tasked con "encontrar" a inflar hallazgos de prioridad baja. |
| v1.5 | 2026-10-12 | Claude Sonnet 5.5 | Gestión de dependencias de terceros (SOUP) formalizada en §7.1 tras activar Dependabot para `npm` y `pip`: política de pisos/techos, excepciones con motivo, grupo `react`, Node 24 en un solo major y lockfile con npm 11. El CI pasa a compilar el frontend (§7). Sin cambios en el producto. |
| v1.6 | 2026-11-07 | Claude Sonnet 5.5 | Sincronización de gobernanza con el proyecto de referencia (69 commits desde el 2026-10-12). **Corregido un control que no controlaba**: el gate de mutación backend (`check_mutmut_score.py`) parseaba `mutmut results`, que NO lista los mutantes muertos, así que nunca podía dar verde; `run_mutmut.sh` además estaba roto con mutmut 3 (rechaza `--paths-to-mutate`) y `mutmut` no estaba fijado. Ahora: `mutmut==2.5.1`, gate sobre el cache SQLite, `--CI` sin tragarse el exit de mutmut, runner propio que cuenta todo exit ≠ 0 como muerto, 14 tests de anclaje. Nuevo guardián de pineo de acciones por SHA (§7.1) y `cooldown` de 14 días en Dependabot. `github-actions.md` pasa a **7** modos de fallo (`concurrency.group` largo tumba el arranque; el centinela excluye también a `dependabot[bot]`); `testing.md` suma 3 reglas de flaky (tiempo en CPU, nivel de log, valor con contexto). Nueva skill `/arreglar-no-envolver` + sección en `CLAUDE.md`; sección de instrucciones de compactación; `AGENTS.md`; plantilla de deuda con columna **Cubo** (🔴/🟡/🧊). Corregida una contradicción en `MULTI_AGENT_ENGINEERING_METHOD.md` (lanzar un agente no consume la máquina, pero lo que su `Bash` ejecuta sí) y la ruta de `TESTING_TOOLS.md` citada mal en dos reglas. Sin cambios en el producto. |
| v1.7 | 2026-11-07 | Claude Sonnet 5.5 | Segunda tanda de sincronización de gobernanza con el proyecto de referencia ("lote grande"). **Tres controles de documentación que antes no existían**: `scripts/check_doc_anchors.py` (enlaces `#sección` rotos tras renombrar un título, que `check_doc_links.sh` no ve) y `scripts/check_doc_citations.py` (citas al código por NOMBRE `ruta/archivo.py::símbolo`, verificadas por AST en `.py`; las viejas por número de línea se cuentan pero no se verifican), ambos en `ci.yml`, `kit-quality.yml` y `scripts/run_local_ci.sh`, con `tests/test_citas_del_dhf.py` (30 tests). Nueva regla path-scoped `.claude/rules/docs.md` (las reglas de escribir en `docs/` salen del core). Nuevo workflow `.github/workflows/main-en-rojo.yml` (un Issue por workflow que rojea en `main`; cierra el hueco "un rojo que nadie mira") con `tests/test_workflow_main_en_rojo.py` (30 tests, lógica del script ejecutada con `node`); cierra además un hueco del original (un PR de fork con rama llamada `main`) y `pyyaml` queda declarado en `requirements-dev.txt`. Nueva skill `/reporte-corto` (el cierre de una tarea cabe en un celular) y su espejo en `CLAUDE.md`. Límite honesto: el disparo real de `workflow_run` solo se puede probar tras el merge a `main`. Sin cambios en el producto. Verificación: 124 tests ✅, mypy/ruff limpios, 0 enlaces/anclas/citas rotas. |
| v1.8 | 2026-11-07 | Claude Opus 5.5 | El reglamento se reparte según quién lo carga (§2.1). Nuevo estilo de salida `.claude/output-styles/orquestador.md`, activado con `outputStyle` en `.claude/settings.json`: recibe las preferencias del dueño (idioma, modo tutor, antes de actuar) de `CLAUDE.md`, la orquestación de `.claude/rules/orquestacion.md` y `.claude/rules/agentes.md` (matriz de agentes) y las sesiones paralelas de `.claude/rules/sesiones-paralelas.md`, de modo que los subagentes no relean cada turno lo que solo usa la sesión principal. Se eliminan `agentes.md` y `sesiones-paralelas.md`; `orquestacion.md` queda con las reglas duras de ejecución, una sección nueva de higiene de contexto y las reglas de "antes de cantar verde" que también obedecen los agentes. `CLAUDE.md` conserva en §REGLAS COMUNES git, zonas off-limits, diagnóstico y memoria, más una red de seguridad que remite al estilo. Guardián nuevo `tests/test_estilo_orquestador_enchufado.py`; `scripts/lint_agents.py` lintea también los estilos. Sin cambios en el producto. |
| v1.9 | 2026-11-07 | Claude Opus 5.5 | Auditoría con 4 agentes de solo lectura + refutador independiente para seguridad, y arreglos en una rama. Proceso/gobernanza: el candado de suite completa (`.claude/scripts/candado_suite_completa.py`) describe lo que bloquea de verdad y gana test propio; espejos en `.claude/commands/` para las 3 skills que no lo tenían; CI con mínimo privilegio, imágenes pineadas por digest, guardián de coherencia de `needs`, piso de cobertura cableado en `ci.yml` y build estricto de docs en PR; scripts locales que fallan en vez de saltear. Producto: JWT con `exp` obligatorio y guard de secretos vacíos/cortos (detalle en CHANGELOG). |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
