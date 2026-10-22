"""qhawana/api.py — la API del Observatorio de datos (proyecto Qhawana Q1; fase 10.2b, 2026-10-20): su página y de cuándo es.

- `GET /api/observatorio/estado`: {generado, indicadores, estudios} de la página vigente; 404 si aún no se generó;
- `GET /api/observatorio/plataforma.html`: la página (la construye datafw: servicios/qhawana_generar.py), EN LÍNEA para
  mostrarla en un marco.

Públicas, como antes `/obs/`: son indicadores de fuentes oficiales, el mismo observatorio de la web.
"""
from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from qhawana import config as cfg

router = APIRouter(prefix="/api/observatorio", tags=["observatorio"])


def _archivo(nombre: str):
    carpeta = cfg.carpeta()
    ruta = carpeta / nombre if carpeta is not None else None
    if ruta is None or not ruta.is_file():
        raise HTTPException(404, "El observatorio aún no tiene su página.")
    return ruta


@router.get("/estado")
async def estado() -> dict:
    return json.loads(_archivo("estado.json").read_text(encoding="utf-8"))


@router.get("/plataforma.html")
async def pagina() -> FileResponse:
    # En línea (no como descarga: va en un marco) y revalidada cada vez (la web pide ?v=<generado>).
    return FileResponse(_archivo("plataforma.html"), media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-cache"})
