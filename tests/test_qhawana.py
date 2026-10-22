"""tests/test_qhawana.py — el Observatorio de datos (Qhawana; nació en Qillqa el 2026-10-20): su tema sale del anfitrión o,
solo, de Unancha, y trae todo lo que datafw necesita; su API sirve su página EN LÍNEA (va en un marco) y su estado desde
su carpeta. El tema que pasa Qillqa se prueba en Qillqa (backend/tests/test_qhawana_en_qillqa.py).
"""
import json
import os
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
UNANCHA = Path(os.environ.get("UNANCHA_DIR") or RAIZ.parent / "unancha") / "tokens"


def _roles() -> set[str]:
    """Las claves de paleta que el tema usa (las de `_variables`, `integracion` y los roles de los chips)."""
    from qhawana import tema as qhawana_tema

    fuente = Path(qhawana_tema.__file__).read_text(encoding="utf-8")
    return set(re.findall(r"p\[['\"](\w+)['\"]\]", fuente)) | set(qhawana_tema.ROLES.values())


@pytest.mark.skipif(not (UNANCHA / "colors.json").is_file(), reason="sin Unancha en esta máquina")
def test_el_tema_de_unancha_trae_todos_los_roles_y_es_otro():
    from qhawana.tema import tema, tema_unancha

    clara, oscura, letra = tema_unancha(UNANCHA)
    assert _roles() - set(clara) == set() and _roles() - set(oscura) == set()
    assert clara["fondo"] == "#F5F1EC" and "Source Sans 3" in letra
    texto = tema(clara, oscura, letra)
    assert "<!-- tema:arranque -->" in texto and "qhawana_apariencia" in texto and "data-qillqa" not in texto


def test_el_generador_rechaza_un_tema_incompleto(tmp_path):
    """Un tema del anfitrión sin todas sus partes no construye nada (el de Qillqa se prueba en Qillqa)."""
    from qhawana.generar import texto_tema

    archivo = tmp_path / "tema.json"
    archivo.write_text(json.dumps({"clara": {}}), encoding="utf-8")
    with pytest.raises(SystemExit):
        texto_tema(archivo)


def test_la_api_sirve_su_pagina_en_linea_y_su_estado(tmp_path, monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from qhawana import api as observatorio
    from qhawana import config as qhawana_config

    app = FastAPI()
    app.include_router(observatorio.router)
    c = TestClient(app)
    monkeypatch.setattr(qhawana_config.config, "qhawana_dir", str(tmp_path))
    assert c.get("/api/observatorio/estado").status_code == 404
    (tmp_path / "plataforma.html").write_text("<html>observatorio</html>", encoding="utf-8")
    (tmp_path / "estado.json").write_text('{"generado": "2026-10-20", "indicadores": 3, "estudios": 1}', encoding="utf-8")
    assert c.get("/api/observatorio/estado").json()["indicadores"] == 3
    r = c.get("/api/observatorio/plataforma.html")
    assert r.status_code == 200 and r.text == "<html>observatorio</html>" and r.headers["content-type"].startswith("text/html")
    assert "attachment" not in r.headers.get("content-disposition", "")
