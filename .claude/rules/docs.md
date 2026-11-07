---
paths:
  - "docs/**/*.md"
---

# DOCUMENTACIÓN DEL DHF (consecuencia SaMD §5.1 + §5.7 — la documentación es un entregable verificable)

> Regla **por-capa** del cerebro SaMD; las reglas **transversales** viven en `CLAUDE.md`. Esta regla carga sola cuando el agente lee/edita un `.md` bajo `docs/`. Es una **CONSECUENCIA PRÁCTICA de la Regla 0** (cumplimiento SaMD): no es opcional. Capa/agente dueño: `docs-dhf` (escribe) + `samd-audit-trace` (audita; un agente que audita no escribe, y uno que escribe no se auto-audita).
>
> ⚠️ **Límite honesto de la carga automática:** esta regla se activa cuando el agente *lee o edita* un archivo de `docs/` con sus herramientas de archivo. Si editás documentos **por script** (`sed`, `python`, un heredoc de shell), la regla NO se carga sola: abrí este archivo antes de empezar. Lo que SIEMPRE aplica, cargue o no esta regla, es la obligación del core (`CLAUDE.md` §CIERRE DE BLOQUE GRANDE): trazabilidad antes de cerrar, poda por lote y números de verificación.

## Reorg de carpetas y enlaces

* **Reorg de carpetas en `docs/`** → tras renombrar/mover cualquier `.md`, correr el link-checker cross-doc (**`bash scripts/check_doc_links.sh`**) y resolver enlaces rotos en el mismo PR. ⚠️ **El comando tiene que RESOLVER cada enlace contra el disco.** Un `grep -rEn "\(\.{1,2}/[^)]+\.md" docs/` pelado — que esta regla mandaba hasta el 2026-08-23 — **no verifica nada**: LISTA todos los enlaces relativos, rotos y sanos por igual, con lo cual "corrí el link-checker" era un verde vacío. El script del repo sí resuelve con `realpath`, sale con exit 1 y lo corre el CI (`.github/workflows/ci.yml` + `kit-quality.yml`). **Ningún PR de reorg cierra sin que el link-checker reporte 0 broken.**
* **Renombrar un TÍTULO rompe los enlaces `#ancla` que apuntan a él, y el link-checker no lo ve**: `check_doc_links.sh` comprueba que exista el ARCHIVO y descarta el fragmento. El hueco lo cubre **`python3 scripts/check_doc_anchors.py`** (mismo slug que GitHub: acentos conservados, duplicados con sufijo `-1`, `-2`; también los `<a id>` explícitos). Lo corre el CI junto al link-checker, y vale el mismo criterio: **0 rotas** antes de cerrar. Un ancla escrita a mano sin acento (`#refutacion`) contra un título «Refutación» es el caso típico.

## TRACEABILITY_MATRIX_SAMD

* **TRACEABILITY_MATRIX_SAMD.md** → cada REQ-XXX en la matriz debe apuntar a `archivo:línea` verificable + nombre de test que existe HOY. Frases vagas sin path NO son trazabilidad SaMD aceptable. Un auditor externo lo levanta primero.

## Poda obligatoria de documentos vivos

* **Poda obligatoria de documentos vivos**: los docs DHF crecen por acumulación append-only y terminan siendo ilegibles (un `TECHNICAL_DEBT_SUMMARY` de cientos de KB no lo lee nadie, ni vos ni un auditor). En cada cierre, archivá en un `TECHNICAL_DEBT_HISTORY.md` toda sección con más de 30 días de antigüedad Y sin deuda referenciada en el índice de deuda VIVA (la sección completa, nunca una entrada suelta). Mismo principio para los changelogs del Master Map y la matriz de trazabilidad: van a un `_CHANGELOG.md` aparte. **Excepción `ISO_14971_RISK_MATRIX.md`**: su cuerpo por riesgo es una lista de controles **acumulada por diseño** (ISO 14971 §7-8), no deuda — no se poda; la intervención segura ahí es un índice de navegación aditivo.
* **La poda corre en el cierre de CADA LOTE**, no de cada bloque (un lote no es un bloque, y una regla que dice "en cada cierre de BLOQUE" se pospone para siempre), y se **reporta el número de secciones archivadas**. "0 archivadas" solo vale si el medidor dice 0 elegibles.

## Presupuesto de escritura — la poda sola no alcanza

Podar lo viejo mientras cada lote añade decenas de líneas nuevas es vaciar con un dedal. Por eso, al escribir en los documentos vivos:

* **Fila del índice de deuda VIVA ≤ 2 líneas**: `ID | prioridad | UNA frase de qué está roto | enlace a su sección`. El análisis, la evidencia y el historial de intentos viven en la sección enlazada, **nunca dentro de la celda**. Una tabla es un índice, no un informe.
* **Sección de cierre de lote ≤ 40 líneas** en el doc vivo: qué se cerró, los números de verificación y el enlace. Lo que exceda **nace directamente en el archivo histórico** — no se escribe en el vivo "por ahora" para archivarlo después, porque ese "después" no llega.
* **Verificación obligatoria antes de cerrar** (números, no impresión): `du -h` del doc tocado y `wc -l` de la sección añadida. Si el doc vivo **creció** en un cierre que también podaba, se reporta y se explica.

> Si un lote necesita más espacio que los topes, es señal de que el detalle va al histórico — no de subir el tope. (Los topes de la **memoria del agente** —ficha y tablero— viven en el core, porque aplican en sesiones que no tocan `docs/`.)
