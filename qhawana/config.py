"""qhawana/config.py — la configuración PROPIA del Observatorio de datos (proyecto Qhawana Q1; fase 10.2b de docs/plataforma/propuesta-repositorios.md,
2026-10-20). No depende de `app.config`: viaja con el módulo.

- QHAWANA_DIR: la carpeta de su página (`plataforma.html` y `estado.json`); sin ella, el observatorio no tiene página;
- DATAFW_DIR: datafw, que construye la página (tools/plataforma.py: vistas, datos y gráficos);
- UNANCHA_DIR: la identidad común, de la que sale su tema cuando corre solo (con un anfitrión, el tema lo pone él).
"""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class ConfigQhawana(BaseSettings):
    qhawana_dir: str = ""
    datafw_dir: str = ""
    unancha_dir: str = ""


config = ConfigQhawana()


def carpeta() -> Path | None:
    """Donde vive su página; None si no se configuró."""
    return Path(config.qhawana_dir) if config.qhawana_dir else None


def generador() -> Path | None:
    return Path(config.datafw_dir) / "tools" / "plataforma.py" if config.datafw_dir else None


def tokens_unancha() -> Path | None:
    return Path(config.unancha_dir) / "tokens" if config.unancha_dir else None
