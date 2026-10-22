"""tests/test_qhawana_sola.py — el Observatorio arranca SOLO, con el anfitrión mínimo de Tiqsi, sin Qillqa ni base de
datos (proyecto Qhawana Q2; fase 10.2b, 2026-10-20; app/qhawana_sola.py). Su página se prueba en vivo
(qillqa/scripts/verde.sh sola-qhawana).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SECRETO = "k" * 40


def _entorno_limpio(tmp_path) -> dict:
    return {"HOME": os.environ.get("HOME", "/tmp"), "PATH": os.environ.get("PATH", ""),
            "QHAWANA_DIR": str(tmp_path / "qhawana"), "JWT_SECRET": SECRETO}


def test_solo_no_carga_nada_de_qillqa(tmp_path):
    codigo = ("import sys, json; import qhawana.sola as m; "
              "print(json.dumps({'ajenos': sorted(x for x in sys.modules if x == 'app' or x.startswith('app.')), "
              "'informe': m.app.state.anfitrion.informe(), 'capacidades': m.app.state.anfitrion.capacidades.ofrecidas()}))")
    r = subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, env=_entorno_limpio(tmp_path),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr[-2000:]
    datos = json.loads(r.stdout.strip().splitlines()[-1])
    assert datos["ajenos"] == []                                    # nada de Qillqa
    assert datos["informe"] == [{"id": "observatorio", "nombre": "Observatorio de datos", "version": "0.1.0"}]
    assert set(datos["capacidades"]) == {"identidad.v1"}


def test_solo_sin_su_carpeta_o_sin_secreto_no_arranca(tmp_path):
    for falta in ("QHAWANA_DIR", "JWT_SECRET"):
        entorno = {k: v for k, v in _entorno_limpio(tmp_path).items() if k != falta}
        r = subprocess.run([sys.executable, "-c", "import qhawana.sola"], cwd=RAIZ, env=entorno,
                           capture_output=True, text=True, timeout=120)
        assert r.returncode != 0 and falta in r.stderr, falta
