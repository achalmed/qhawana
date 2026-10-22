"""qhawana/generar.py — la página del Observatorio de datos: la construye datafw con el tema de quien la muestra (proyecto Qhawana Q1; fase 10.2b,
2026-10-20). Simula por omisión: muestra el tema y lo que haría.

    python -m qhawana.generar                          # simula, con el tema de Unancha (solo)
    python -m qhawana.generar --tema-de tema.json      # simula, con el tema que da el anfitrión
    python -m qhawana.generar [--tema-de …] --aplicar  # escribe plataforma.html y estado.json

El tema del anfitrión es un JSON {clara, oscura, letra, apariencia, origen, pie} (Qillqa lo arma desde su paleta en
`scripts/observatorio.py`); sin él, sale de Unancha (UNANCHA_DIR). La página va a QHAWANA_DIR; datafw, de DATAFW_DIR.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from qhawana import config as cfg
from qhawana.tema import tema, tema_unancha

CLAVES_TEMA = ("clara", "oscura", "letra")


def texto_tema(tema_de: Path | None) -> str:
    """El tema: el del anfitrión (su JSON) o, solo, el de Unancha."""
    if tema_de is not None:
        d = json.loads(tema_de.read_text(encoding="utf-8"))
        faltan = [k for k in CLAVES_TEMA if not d.get(k)]
        if faltan:
            raise SystemExit(f"El tema de {tema_de} no trae {', '.join(faltan)}.")
        extra = {k: d[k] for k in ("apariencia", "origen", "pie") if d.get(k)}
        return tema(d["clara"], d["oscura"], d["letra"], **extra)
    tokens = cfg.tokens_unancha()
    if tokens is None or not (tokens / "colors.json").is_file():
        raise SystemExit("Sin tema del anfitrión hace falta Unancha: UNANCHA_DIR (con tokens/colors.json).")
    clara, oscura, letra = tema_unancha(tokens)
    return tema(clara, oscura, letra)


def escribir_estado(pagina: Path) -> dict:
    """estado.json desde el JSON que la página lleva dentro (su fecha y su resumen)."""
    html = pagina.read_text(encoding="utf-8")
    marca = '<script id="datos" type="application/json">'
    inicio = html.index(marca) + len(marca)
    datos = json.loads(html[inicio:html.index("</script>", inicio)])
    r = datos["resumen"]
    estado = {"generado": datos["generado"], "indicadores": r["n"], "estudios": r["n_estudios"]}
    (pagina.parent / "estado.json").write_text(json.dumps(estado, ensure_ascii=False) + "\n", encoding="utf-8")
    return estado


def generar(tema_de: Path | None = None, aplicar: bool = False) -> int:
    generador, carpeta = cfg.generador(), cfg.carpeta()
    if generador is None or not generador.is_file():
        print(f"No se encontró datafw (DATAFW_DIR → {generador}).", file=sys.stderr)
        return 1
    if carpeta is None:
        print("Falta QHAWANA_DIR (la carpeta de la página del observatorio).", file=sys.stderr)
        return 1
    texto = texto_tema(tema_de)
    salida = carpeta / "plataforma.html"
    if not aplicar:
        print(texto)
        print(f"(simulación: con --aplicar se genera {salida} con {generador})")
        return 0
    carpeta.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as t:
        t.write(texto)
    try:
        r = subprocess.run([sys.executable, str(generador), "--tema", t.name, "--salida", str(salida)], cwd=generador.parents[1])
    finally:
        os.unlink(t.name)
    if r.returncode:
        return r.returncode
    estado = escribir_estado(salida)
    print(f"Escrito {salida} ({estado['indicadores']} indicadores, {estado['estudios']} estudios).")
    return 0


def _principal(argv: list[str]) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="python -m qhawana.generar", description="La página del observatorio.")
    p.add_argument("--tema-de", type=Path, help="el tema del anfitrión (JSON); sin él, el de Unancha")
    p.add_argument("--aplicar", action="store_true", help="escribir la página (sin esto, solo simula)")
    a = p.parse_args(argv)
    return generar(a.tema_de, a.aplicar)


if __name__ == "__main__":
    raise SystemExit(_principal(sys.argv[1:]))
