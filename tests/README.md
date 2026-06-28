# tests/ — Verificación (SaMD §5.7)

Tests del backend + punto de partida de la verificación demostrable que SaMD exige.

Reglas duras (ver `docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md`):

- Tests **rigurosos, no de humo**: aserciones específicas sobre valores, llamadas y side effects.
- Mocks asíncronos firmes + aislamiento de estado global por test.
- `hasattr`/duck-typing bajo test → mock con whitelist explícita de atributos.
- Tras cada cambio, correr los tests vinculados y **reportar números** antes de declarar verde.
- Mutation testing es load-bearing: tocar el literal de producción obliga a tocar su killer.
