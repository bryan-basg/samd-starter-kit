#!/usr/bin/env python3
"""Semáforo de gasto para /trabajo-nocturno. Solo lee; no escribe nada.

El % es el real que Claude Code le pasa a la barra de estado (`rate_limits`): lo guarda
`barra_estado.py` (misma carpeta) en `$SAMD_STATUSLINE_DIR` (por defecto
`~/.cache/samd-statusline`). Sin ese dato el semáforo NO adivina: dice «SIN DATO» y sale
con código 2 — fail-safe, nunca un verde inventado.

Los USD son equivalentes a precio de API (peso relativo de cada token), no dinero cobrado:
con una suscripción, lo que manda es el %, y los USD sirven para comparar tandas entre sí.
"""
import glob
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

# USD por millón (entrada, salida) y multiplicador de lectura de caché, de
# https://platform.claude.com/docs/en/about-claude/pricing (leído 2026-11-27). La PRIMERA
# clave contenida en el id del modelo gana: las específicas van antes que las genéricas.
# Haiku 5.5 sube de precio con prompts de más de 100 k tokens; acá va el tramo bajo.
# Los precios cambian: reverificalos contra la página oficial antes de confiar en un número.
PRECIOS = {
    "fable-5-2": (8, 40, 0.025), "mythos-5-2": (8, 40, 0.025),
    "fable-5-1": (10, 50, 0.025), "mythos-5-1": (10, 50, 0.025),
    "fable": (10, 50, 0.1), "mythos": (10, 50, 0.1),
    "opus-5-5": (4, 20, 0.05), "opus": (5, 25, 0.1),
    "sonnet-5-5": (2, 10, 0.05), "sonnet-5": (2, 10, 0.1), "sonnet": (3, 15, 0.1),
    "haiku-5-5": (0.10, 0.50, 0.1), "haiku": (1, 5, 0.1),
}
ESCRITURA_5M, ESCRITURA_1H = 1.25, 2.0  # multiplicadores oficiales de escritura de caché
VENTANA_5H = 5 * 3600
EDAD_MAXIMA = 15 * 60  # un % más viejo que esto no vale: los agentes pudieron gastar mucho entretanto


def carpeta_barra() -> str:
    return os.path.expanduser(os.environ.get("SAMD_STATUSLINE_DIR", "~/.cache/samd-statusline"))


def leer_limites() -> Tuple[Optional[Dict[str, Any]], float]:
    """Último registro de la barra de estado que traiga límites, y su antigüedad en segundos."""
    patron = os.path.join(carpeta_barra(), "sesion-*.json")
    for ruta in sorted(glob.glob(patron), key=os.path.getmtime, reverse=True):
        try:
            with open(ruta, encoding="utf-8") as f:
                limites = json.load(f).get("rate_limits")
        except (OSError, ValueError):
            continue
        if limites and limites.get("five_hour"):
            return limites, time.time() - os.path.getmtime(ruta)
    return None, 0.0


def precio(uso: Dict[str, Any], modelo: str) -> float:
    entrada, salida, lectura = next((v for k, v in PRECIOS.items() if k in modelo), PRECIOS["opus"])
    cache = uso.get("cache_creation") or {}
    c5 = cache.get("ephemeral_5m_input_tokens", 0)
    c1h = cache.get("ephemeral_1h_input_tokens", 0)
    if not cache:
        c5 = uso.get("cache_creation_input_tokens", 0)
    total: float = (
        uso.get("input_tokens", 0) * entrada
        + c5 * ESCRITURA_5M * entrada
        + c1h * ESCRITURA_1H * entrada
        + uso.get("cache_read_input_tokens", 0) * lectura * entrada
        + uso.get("output_tokens", 0) * salida
    ) / 1e6
    return total


def gasto_desde(inicio: float) -> Tuple[float, Dict[str, float], Dict[str, float]]:
    """USD equivalentes desde `inicio` (epoch): total, por modelo y por subagente."""
    total, vistos = 0.0, set()
    por_modelo: Dict[str, float] = defaultdict(float)
    por_agente: Dict[str, float] = defaultdict(float)
    base = os.path.expanduser("~/.claude/projects")
    for ruta in glob.glob(base + "/**/*.jsonl", recursive=True):
        if os.path.getmtime(ruta) < inicio:
            continue
        nombre = os.path.basename(ruta)
        with open(ruta, encoding="utf-8", errors="ignore") as f:
            for linea in f:
                if '"usage"' not in linea:
                    continue
                try:
                    d = json.loads(linea)
                except ValueError:
                    continue
                m = d.get("message")
                if d.get("type") != "assistant" or not isinstance(m, dict) or "usage" not in m:
                    continue
                t = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).timestamp()
                clave = (m.get("id"), d.get("requestId"))  # la misma respuesta se registra varias veces
                if t < inicio or clave in vistos:
                    continue
                vistos.add(clave)
                usd = precio(m["usage"], m.get("model", ""))
                total += usd
                por_modelo[m.get("model", "?")] += usd
                if nombre.startswith("agent-"):
                    por_agente[nombre] += usd
    return total, por_modelo, por_agente


def semaforo(peor: float) -> str:
    if peor >= 90:
        return "ROJO — pará y esperá la renovación."
    if peor >= 80:
        return "AMARILLO — no lances; revisá y documentá lo que ya volvió."
    return "VERDE — se puede lanzar."


def main() -> int:
    limites, edad = leer_limites()
    if limites is None:
        print(f"SIN DATO de la barra de estado en {carpeta_barra()}: no lances agentes hasta saber el %. "
              "Configurala con barra_estado.py (ver SKILL.md, paso 1).")
        return 2
    v5 = limites["five_hour"]
    usado, renueva = v5["used_percentage"], v5["resets_at"]
    ahora = time.time()
    if edad > EDAD_MAXIMA:
        print(f"SIN DATO fresco: el último % es de hace {edad / 60:.0f} min (tope {EDAD_MAXIMA // 60}). "
              "No lances: releé tras tu próximo turno, que refresca la barra de estado.")
        return 2
    if renueva <= ahora:
        print("La ventana de 5 h del último dato YA se renovó: % viejo, releé tras tu próximo turno.")
        return 2

    def hora(epoch: float) -> str:
        return datetime.fromtimestamp(epoch).strftime("%m-%d %H:%M")

    print(f"5 h: {usado} % · renueva {hora(renueva)} (en {(renueva - ahora) / 3600:.1f} h) · dato de hace {edad / 60:.0f} min")
    semana = limites.get("seven_day")
    if semana:
        print(f"semana: {semana['used_percentage']} % · renueva {hora(semana['resets_at'])}")

    total, modelos, agentes = gasto_desde(renueva - VENTANA_5H)
    detalle = ", ".join(f"{m} {u:.0f}" for m, u in sorted(modelos.items(), key=lambda x: -x[1]))
    print(f"ventana actual: {total:.0f} USD equivalentes ({detalle})")
    if usado >= 5:  # con menos, el redondeo del % domina
        print(f"calibración: 1 % ≈ {total / usado:.1f} USD equivalentes")
    if agentes:
        print(f"subagentes: {len(agentes)} · media {sum(agentes.values()) / len(agentes):.1f} USD · máx {max(agentes.values()):.1f}")

    print("SEMÁFORO: " + semaforo(max(usado, semana["used_percentage"] if semana else 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
