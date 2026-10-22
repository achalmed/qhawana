"""qhawana/sola.py — el Observatorio de datos SOLO: sin Qillqa, con el anfitrión mínimo de Tiqsi (proyecto Qhawana Q2; fase 10.2b de
docs/plataforma/propuesta-repositorios.md, 2026-10-20). No tiene base
de datos: su página la construye datafw en su carpeta, con el tema de Unancha.

    QHAWANA_DIR=…  JWT_SECRET=<32 o más caracteres> \\
      .venv/bin/uvicorn qhawana.sola:app --port 8035

Las cuentas viven en QHAWANA_CUENTAS (por omisión <QHAWANA_DIR>/cuentas.json) y se crean con
`python -m tiqsi.minimo cuenta <archivo> <usuario> --rol administrador --nombre …`; la página se genera con
`DATAFW_DIR=… UNANCHA_DIR=… python -m qhawana.generar --aplicar`.
"""
from __future__ import annotations

import os
from pathlib import Path

from tiqsi.minimo import crear_app

from qhawana.config import config
from qhawana.manifiesto import MANIFIESTO

if not config.qhawana_dir:
    raise SystemExit("El Observatorio solo necesita su carpeta (su página y sus cuentas): QHAWANA_DIR.")
secreto = os.environ.get("JWT_SECRET", "")
if not secreto:
    raise SystemExit("El Observatorio solo necesita su secreto: JWT_SECRET (firma las sesiones).")

app = crear_app([MANIFIESTO], nombre="Observatorio de datos", secreto=secreto,
                cuentas=os.environ.get("QHAWANA_CUENTAS") or Path(config.qhawana_dir) / "cuentas.json",
                web=os.environ.get("QHAWANA_WEB") or None)
