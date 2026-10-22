"""qhawana/manifiesto.py — el manifiesto del Observatorio de datos (proyecto Qhawana; fase 10.2b de docs/plataforma/propuesta-repositorios.md,
2026-10-20).

Q1 (hecha): su configuración (servicios/qhawana_config.py), su generador (servicios/qhawana_generar.py: datafw construye
la página con el tema que le dan; solo, el de Unancha, servicios/qhawana_tema.py) y su API (api/observatorio.py: su página
y su estado, desde QHAWANA_DIR). No tiene base de datos ni necesita nada del anfitrión: Qillqa solo le pasa su tema
(scripts/observatorio.py) y lo muestra en un marco. Q2: su web aislada y su página sola.
"""
from __future__ import annotations

from tiqsi import Manifiesto

from qhawana import api as observatorio

VERSION = "0.1.0"

MANIFIESTO = Manifiesto(
    id="observatorio", nombre="Observatorio de datos", version=VERSION, contrato="^0.1",
    routers=[observatorio.router],
    # Los prefijos con que se apaga (los del registro de módulos encendibles, servicios/modulos.py).
    prefijos=("/api/observatorio",), publico=True,
)
