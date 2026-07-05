---
name: commit-selectivo-parcial
description: Des-mezcla un archivo compartido (config generada, locale, tipos de contrato) que quedó entreverado con el trabajo de otra sesión paralela, para commitear SOLO lo propio sin pisar lo ajeno. Úsala cuando hay una sesión paralela activa tocando los mismos archivos y necesitás separar tus cambios de los ajenos antes de commitear.
---

# commit-selectivo-parcial — separar cambios propios de una sesión paralela

Separá tus cambios cuando hay una **sesión paralela activa** tocando los mismos archivos. El objetivo: commitear SOLO tus cambios sin barrer ni pisar el trabajo de la otra sesión. NUNCA uses `git add -A`/`-u`; siempre `git add` EXPLÍCITO de tus archivos.

## Cuándo usarla

- Dos sesiones (o dos agentes) editan el mismo archivo de datos/config compartido al mismo tiempo (locale, feature flags, fixture) y las claves de ambas quedaron mezcladas en el working tree.
- Necesitás commitear/pushear tu parte sin esperar a que la otra sesión termine, y sin arrastrar su trabajo a medio terminar.
- Tocaste código que alimenta un archivo generado (contrato de API, tipos derivados) y hay una sesión paralela con cambios sin commitear que podrían colarse si regenerás desde el working tree.

## Caso 1 — archivo de datos/config compartido mezclado con cambios de otra sesión

Ejemplos típicos: un archivo de locale (`translation.json`), un archivo de feature flags, un fixture compartido. Tiene tus entradas nuevas MEZCLADAS con un bloque de otra sesión. Receta que separa sin pisar:

1. **Backup** del archivo actual (con TODO mezclado) a un lugar temporal.
2. **`git checkout <archivo>`** → lo revierte a HEAD (borra tus entradas Y las ajenas del working tree).
3. **Reaplicá SOLO lo tuyo con un script** que navegue la estructura real (JSON/YAML) y sobreescriba ÚNICAMENTE tus claves (nunca dejes que un agente reescriba el archivo entero — se pierde estructura y claves dinámicas). Este es el "merge controlado": el molde solo trae tus entradas; el script las inyecta sobre la versión de HEAD.
4. **`git add`** explícito de esos archivos + `git commit` (con OK del dueño si es push; el commit local no necesita OK).
5. **Restaurá el backup** al working tree → devuelve el bloque ajeno de la otra sesión intacto (para que siga trabajando).

Si el archivo tiene un contrato propio (placeholders, glosario de términos, formatos de plural, claves que no se traducen), respetalo al reaplicar y verificá con el linter/checker del proyecto si existe uno.

## Caso 2 — archivos GENERADOS (contrato de API, tipos derivados) con sesión paralela sin commitear

Si tu framework publica algo del código (ej. docstrings de rutas) como parte de un contrato generado (OpenAPI u equivalente), tocar ese código dispara drift y hay que regenerar el contrato.

**Regla dura**: regenerá el archivo generado desde un `git worktree` limpio del commit, NUNCA desde el working tree, cuando hay una sesión paralela con código sin commitear. Si regenerás desde el working tree sucio, el código ajeno en vuelo (ej. un endpoint nuevo de la otra sesión) se cuela en el contrato. `git stash` NO sirve para esto — usá worktree:

```bash
git worktree add /tmp/proyecto-clean-contrato <commit-o-branch-limpio>
# regenerar el archivo DENTRO del worktree limpio
# copiar el resultado de vuelta a tu working tree
git worktree remove /tmp/proyecto-clean-contrato
```

## Cierre

Antes de declarar hecho: `git status` y confirmá que SOLO tus archivos quedaron staged, que el bloque/código ajeno sigue en el working tree sin tocar, y (si tocaste un contrato generado) que no arrastró símbolos de la otra sesión. Reportá qué archivos entran en tu commit y qué quedó afuera (de la sesión paralela).
