#!/usr/bin/env python3
"""export_openapi.py — Exporta el contrato OpenAPI del backend a JSON.

Stack de referencia: FastAPI. El CI lo usa para detectar drift entre el contrato
y los tipos generados del frontend. Adaptá el import de `app` a tu aplicación real.

Uso: python scripts/export_openapi.py --out frontend/src/api/openapi.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Agregar la raíz del proyecto al sys.path para importar 'app' correctamente
sys.path.insert(0, os.getcwd())



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="frontend/src/api/openapi.json")
    args = parser.parse_args()

    try:
        # Adaptá esta ruta de import a tu aplicación FastAPI real.
        from app.main import app  # type: ignore
    except Exception as exc:  # pragma: no cover - guía de adaptación
        print(
            "No se pudo importar `app.main:app`. Ajustá el import a tu aplicación "
            f"FastAPI real en scripts/export_openapi.py. Detalle: {exc}",
            file=sys.stderr,
        )
        return 1

    schema = app.openapi()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(schema, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print(f"Contrato OpenAPI exportado a {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
