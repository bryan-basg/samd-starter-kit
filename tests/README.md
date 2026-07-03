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
pytest                                # 16/16 verde
pytest -m security                    # solo los de seguridad
```

Usá estos tests como plantilla del nivel de rigor esperado; reemplazalos por los de tu app real.
