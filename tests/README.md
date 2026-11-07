# tests/ — Verificación (SaMD §5.7)

Tests del backend + punto de partida de la verificación demostrable que SaMD exige.

Reglas duras (ver `docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md`):

- Tests **rigurosos, no de humo**: aserciones específicas sobre valores, llamadas y side effects.
- Mocks asíncronos firmes + aislamiento de estado global por test.
- `hasattr`/duck-typing bajo test → mock con whitelist explícita de atributos.
- Tras cada cambio, correr los tests vinculados y **reportar números** antes de declarar verde.
- Mutation testing es load-bearing: tocar el literal de producción obliga a tocar su killer.

## Ejemplo ejecutable (borralo cuando traigas tu app)

`test_hard_rules.py` verifica el slice de ejemplo de `app/` con pruebas reales (no de humo): identidad desde el token y no desde el body, aislamiento por dueño, cifrado en reposo, error sin traceback y fail-safe 503. `conftest.py` aísla el estado global entre tests.

```bash
pip install -r requirements-dev.txt   # (en la raíz del repo)
pytest                                # todo verde (el resumen final trae el conteo real)
pytest -m security                    # solo los de seguridad
```

Usá estos tests como plantilla del nivel de rigor esperado; reemplazalos por los de tu app real.

## Guardianes del propio kit (NO los borres al traer tu app)

Estos dos archivos no prueban `app/`: **vigilan que una regla del kit se siga cumpliendo**. Una regla escrita en prosa que nada comprueba se erosiona sin ruido; un guardián la vuelve verificable (IEC 62304 §5.7).

- `test_workflows_pineados_a_sha.py` — toda acción de `.github/workflows/` pineada a un SHA de 40 caracteres (cadena de suministro, SOUP §8), con una sola versión por acción y la versión legible en comentario. Se deriva de los workflows en disco: uno nuevo entra solo. Si adaptás el kit a menos acciones, bajá `MINIMO_DE_REFERENCIAS`; su trabajo es no aprobar por vacío.
- `test_mutmut_gate.py` — el gate de mutación backend (`scripts/check_mutmut_score.py`), el runner de pytest para mutmut y el cableado de `scripts/run_mutmut.sh` (flag `--CI`, sin `|| true`, versión fijada igual a `requirements-dev.txt`). Si quitás la mutación backend de tu proyecto, quitá este archivo junto con los tres scripts.
