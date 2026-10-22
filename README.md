# Qhawana — un observatorio de datos

Qhawana («mirador» en quechua) sirve una página de vistas, datos y gráficos que construye
[datafw](https://github.com/achalmed/datafw) con el tema de quien la muestra, en línea y con su estado. Es un módulo de
[Tiqsi](https://github.com/achalmed/tiqsi): funciona solo, con el anfitrión mínimo de Tiqsi, o dentro de una plataforma
que lo monte por su manifiesto (como Qillqa).

**Recorrido interactivo:** <https://achalmed.github.io/qhawana/> (el código del sitio está en [`sitio/`](sitio/)).

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -e '.[pruebas,sola]'   # requiere tiqsi
.venv/bin/python -m pytest -q tests
npm install && npm run web:construir
DATAFW_DIR=/ruta/datafw UNANCHA_DIR=/ruta/kit QHAWANA_DIR=/ruta/qhawana .venv/bin/python -m qhawana.generar --aplicar
QHAWANA_DIR=/ruta/qhawana JWT_SECRET=<32 o más caracteres> QHAWANA_WEB=web/dist .venv/bin/uvicorn qhawana.sola:app --port 8035
```

Esta es una **versión de demostración**. Licencia: AGPL-3.0 (`LICENSE`).
