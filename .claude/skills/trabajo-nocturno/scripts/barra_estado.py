#!/usr/bin/env python3
"""Barra de estado mínima de Claude Code que guarda los límites de uso para `gasto.py`.

Claude Code le pasa a la barra de estado, por stdin, un JSON con `rate_limits` (el % real
de la ventana de 5 h y de la semana). Es la única vía por la que ese dato sale de la
herramienta, así que este script lo copia a `$SAMD_STATUSLINE_DIR` (por defecto
`~/.cache/samd-statusline`) y muestra una línea corta. Si ya tenés tu propia barra, no
hace falta este archivo: basta con que la tuya guarde el JSON de entrada igual que acá.

Activarla (en tu `~/.claude/settings.json`, no en el del proyecto: la barra es personal):
    "statusLine": {"type": "command", "command": "python3 <ruta>/barra_estado.py"}
"""
import json
import os
import sys


def main() -> int:
    try:
        d = json.load(sys.stdin)
    except ValueError:
        print("barra: entrada ilegible")
        return 0
    try:
        carpeta = os.path.expanduser(os.environ.get("SAMD_STATUSLINE_DIR", "~/.cache/samd-statusline"))
        os.makedirs(carpeta, exist_ok=True)
        destino = os.path.join(carpeta, f"sesion-{d.get('session_id', 'x')}.json")
        with open(destino + ".tmp", "w", encoding="utf-8") as f:
            json.dump(d, f)
        os.replace(destino + ".tmp", destino)  # atómico: gasto.py nunca lee un archivo a medias
    except OSError:
        pass  # la barra nunca debe romper la sesión; gasto.py dirá «SIN DATO»
    partes = [(d.get("model") or {}).get("display_name", "?")]
    cinco = (d.get("rate_limits") or {}).get("five_hour")
    if cinco:
        partes.append(f"5 h {cinco['used_percentage']:.0f} %")
    print(" · ".join(partes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
