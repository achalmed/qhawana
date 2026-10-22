"""qhawana/tema.py — el tema del Observatorio de datos (proyecto Qhawana Q1; fase 10.2b, 2026-10-20): de unas paletas a las secciones que
datafw pone en su página (`tools/plataforma.py --tema`). Nació en Qillqa (`scripts/observatorio.py`), que ahora solo le
pasa su paleta como anfitrión: el Observatorio no lee nada de Qillqa.

- `tema(clara, oscura, letra, …)`: el tema desde dos paletas con los roles de la web (fondo, superficie, texto, primario…);
- `tema_unancha(tokens)`: las dos paletas y la letra desde la identidad común (Unancha), para cuando corre SOLO: papel,
  tinta y Puka en claro; grafito en oscuro (la web de Qillqa usa su paleta neutra del rediseño, no esta).
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

# Series de los gráficos. La paleta de datos de la marca no sirve en pantalla (#EAB61E da 1,72:1
# sobre el fondo); estas son tonos apagados de la familia del rediseño (rojo, arena, azul, salvia,
# violeta, petróleo), legibles sobre el fondo claro (#F5F5F7, contraste ≥ 3:1) y, subidas de luz,
# sobre el oscuro (#1E1E20). Sin naranja ni rosa.
SERIES = ["#B5484D", "#9A7A3C", "#2F5DA8", "#5C8A1E", "#7350A8", "#00866E"]
SERIES_OSCURO = ["#E08287", "#CFAF6E", "#8FAEE0", "#9BC47A", "#B59CE0", "#6FC2B0"]

# Los roles solo pintan el TEXTO de un chip que ya dice su nombre (Dato, Cálculo, Estimación):
# se exige contraste de texto AA (≥ 4,5:1), no las reglas de serie.
ROLES = {"dato": "info", "calculo": "exito", "estimacion": "avisoOscuro"}


def integracion(p: dict) -> str:
    """Reglas que acomodan el núcleo al lenguaje de la plataforma (el de la web de Qillqa).

    Van en la sección de estilos, que el núcleo pone ANTES de sus reglas: por
    eso cada una sube de especificidad con `:root[data-qhawana]` (lo fija el
    arranque) y solo las que pelean con un `style=""` del núcleo llevan
    !important. Lo que depende de estar en el marco (ocultar la barra) se
    condiciona a `[data-incrustado]`.
    """
    r = ":root[data-qhawana]"
    return "\n".join([
        "/* ── Integración con la plataforma (Qhawana, servicios/qhawana_tema.py) ── */",
        "/* Una sola navegación: dentro del marco, las vistas están en la franja del sistema. */",
        ":root[data-incrustado] .barra { display: none; }",
        f"{r} .hoja {{ padding: 0 24px 64px; }}",
        f"@media (max-width: 600px) {{ {r} .hoja {{ padding: 0 12px 48px; }} }}",
        "/* Cabecera de vista: compacta, como el título de Estadísticas; sin retícula ni filete. */",
        f"{r} .portada {{ padding: 24px 0 18px !important; border-bottom: 1px solid var(--lab-border); }}",
        f"{r} .portada::before, {r} .portada h1::before {{ display: none; }}",
        f"{r} .portada h1 {{ font-size: clamp(1.06rem, 1rem + 0.35vw, 1.19rem) !important; font-weight: 600;",
        "  letter-spacing: 0; line-height: 1.3; margin: 0 0 6px; max-width: none; }",
        f"{r} .lead {{ font-size: 0.9rem; line-height: 1.55; max-width: 80ch; }}",
        f"{r} h1, {r} h2, {r} h3 {{ font-weight: 600; letter-spacing: 0; }}",
        f"{r} h2.titulo-seccion {{ font-size: 0.95rem; margin: 32px 0 4px; padding-bottom: 6px; }}",
        f"{r} .sub {{ font-size: 0.875rem; margin: 6px 0 16px; }}",
        # Las tarjetas de tema (núcleo, 2026-10-19) ya vienen con borde fino y radio 10: solo el título.
        f"{r} .tema h3 {{ font-size: 1rem; }}",
        f"{r} .ficha-cab h1 {{ font-size: clamp(1.1rem, 1rem + 0.6vw, 1.4rem); letter-spacing: 0; }}",
        f"{r} .prosa h3 {{ font-size: 1rem; margin-top: 24px; }}",
        f"{r} .prosa p, {r} .prosa li {{ font-size: 0.92rem; line-height: 1.6; }}",
        f"{r} .hero-num b {{ font-size: clamp(2rem, 1.6rem + 1.6vw, 2.6rem); font-weight: 700; letter-spacing: -0.01em; }}",
        "/* Rótulos: las versalitas del subtitle2 del tema MUI, en la letra de la interfaz. */",
        f"{r} .eyebrow, {r} .campo > span, {r} .cifras dt, {r} .bloque h3, {r} .instrumento, {r} .escalera b {{",
        "  font-family: var(--sans); font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em; }",
        f"{r} .eyebrow {{ margin: 0 0 4px; }}",
        "/* Cifras en la letra de la interfaz, alineadas (la monoespaciada queda para código e identificadores). */",
        f"{r} .num, {r} .cuantos, {r} .tema .cuenta, {r} .chispa .v, {r} .lista-simple .num, {r} .tt b,",
        f"{r} table.datos td:first-child, {r} table.datos th:first-child {{",
        "  font-family: var(--sans); font-variant-numeric: tabular-nums; letter-spacing: 0; }",
        "/* Tarjetas de cifra: las de Estadísticas (planas, superficie tenue, radio 4). */",
        f"{r} .cifras {{ gap: 12px; margin-top: 20px; }}",
        f"{r} .cifras div {{ background: var(--lab-code-bg); border-radius: 10px; box-shadow: none; padding: 12px 14px; }}",
        f"{r} .cifras div:hover {{ transform: none; box-shadow: none; border-color: var(--lab-border); }}",
        f"{r} .cifras dd {{ font-weight: 700; font-size: 1.6rem; letter-spacing: 0; }}",
        "/* Pastillas: como la etiqueta de estado (fondo teñido, caja de oración). */",
        f"{r} .chip {{ font-family: var(--sans); font-size: 0.72rem; font-weight: 600; letter-spacing: 0.01em;",
        "  text-transform: none; border: 0; padding: 0.2em 0.7em;",
        "  background: color-mix(in srgb, currentColor 9%, transparent); }",
        "/* Campos y botones: los de MUI (small, radio 4, foco del color principal). */",
        f"{r} input[type=\"search\"], {r} select {{ border-radius: 10px; padding: 8.5px 12px; font-size: 0.875rem; }}",
        f"{r} input[type=\"search\"]:focus, {r} select:focus {{ border-color: var(--lab-accent);",
        "  box-shadow: inset 0 0 0 1px var(--lab-accent); }",
        "@media (max-width: 600px) { :root[data-qhawana] input[type=\"search\"], :root[data-qhawana] select { font-size: 16px; } }",
        f"{r} .volver {{ color: var(--lab-accent); border-color: {p['bordeFuerte']}; border-radius: 10px;",
        "  font-weight: 600; font-size: 0.8125rem; margin: 18px 0 16px; }",
        f"{r} .volver:hover {{ background: var(--lab-accent-bg); border-color: var(--lab-accent); color: var(--lab-accent); transform: none; }}",
        f"{r} .boton-sec {{ border-radius: 10px; font-weight: 600; }}",
        f"{r} .cesta-it, {r} .aviso, {r} .tt {{ border-radius: 10px; }}",
        # Avisos como en la web de Qillqa (2026-10-19): tarjeta con borde fino, sin franja lateral.
        f"{r} .aviso {{ box-shadow: none; border: 1px solid var(--lab-border); border-left-width: 1px; background: var(--lab-bg-elevated); }}",
        f"{r} .ind {{ border-radius: 10px; }}",
        f"{r} .tabla-ind {{ border-top-width: 1px; }}",
        f"{r} .prosa code, {r} footer code {{ border-radius: 10px; }}",
        f"{r} footer {{ margin-top: 40px; }}",
    ])


def _variables(p: dict, series: list[str]) -> str:
    """Las variables de datafw desde una paleta (claro u oscuro), con los roles del rediseño (las claves de la
    paleta de la web de Qillqa: fondo, superficie, texto, primario…)."""
    s = "; ".join(f"--s{i}: {c}" for i, c in enumerate(series, 1))
    return "\n".join([
        f"  --lab-bg: {p['fondo']};  --lab-bg-surface: {p['superficieTenue']};  --lab-bg-elevated: {p['superficie']};",
        f"  --lab-ink: {p['texto']}; --lab-ink-2: {p['textoSecundario']};       --lab-muted: {p['textoTenue']};",
        # Un acento: la tinta; el azul solo en enlaces (lo pone el núcleo con --lab-accent en botones).
        f"  --lab-accent: {p['primario']}; --lab-accent-2: {p['primarioClaro']}; --lab-on-accent: {p['sobrePrimario']};",
        f"  --lab-accent-bg: {p['primarioSuave']};",
        f"  --lab-green: {p['exito']}; --lab-green-bg: {p['exitoFondo']};",
        f"  --lab-border: {p['borde']}; --lab-border-strong: {p['bordeFuerte']};",
        f"  --lab-code-bg: {p['superficieTenue']}; --lab-selection: {p['superficieMedia']};",
        "  --lab-shadow-sm: none;",
        f"  --lab-shadow-md: {p['sombra']};",
        "  --lab-grid-line: transparent;",
        # El marco de las tablas: un borde fuerte, no la tinta (superficies planas de la web).
        f"  --lab-table-frame: {p['bordeFuerte']}; --lab-row-hover: {p['velo']};",
        f"  {s};",
        f"  --rol-dato: {p[ROLES['dato']]}; --rol-calculo: {p[ROLES['calculo']]}; --rol-estimacion: {p[ROLES['estimacion']]};",
    ])


def tema(clara: dict, oscura: dict, letra: str, *, apariencia: str = "qhawana_apariencia", origen: str = "Unancha",
         pie: str = "Observatorio de datos.", series: list[str] | None = None, series_oscuro: list[str] | None = None) -> str:
    """El tema en el formato de secciones de datafw (plataforma_temas/web.html): las dos paletas (claro y oscuro), la
    letra, la clave de `localStorage` con la apariencia elegida y el pie. Los da el anfitrión (Qillqa: su paleta y la
    de su cuenta) o, solo, Unancha (`tema_unancha`)."""
    estilos = "\n".join([
        f"/* Tema de {origen}. Claro por omisión; oscuro cuando la página lleva data-tema=\"oscuro\" (la misma",
        "   regla que la web). Series y roles: ver servicios/qhawana_tema.py. */",
        ":root {",
        "  color-scheme: light;",
        _variables(clara, series or SERIES),
        f"  --serif: {letra};",
        f"  --prosa: {letra};",
        f"  --sans: {letra};",
        '  --mono: ui-monospace, "JetBrains Mono", "SF Mono", SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;',
        # El ancho de un Container maxWidth="xl" de MUI, como Estadísticas.
        "  --ancho: 1536px;",
        "}",
        ':root[data-tema="oscuro"] {',
        "  color-scheme: dark;",
        _variables(oscura, series_oscuro or SERIES_OSCURO),
        "}",
        integracion(clara),
    ])
    arranque = (
        f"<!-- GENERADO por el Observatorio (Qhawana, servicios/qhawana_tema.py; {date.today().isoformat()}) con el tema de "
        f"{origen}; no editar. -->\n"
        "<script>\n"
        "(function () {\n"
        "  var raiz = document.documentElement;\n"
        "  /* La apariencia elegida (en Qillqa, en el menú de la cuenta) o la del aparato. */\n"
        f"  var a = null; try {{ a = localStorage.getItem({json.dumps(apariencia)}) }} catch (e) {{}}\n"
        "  var oscuro = a === 'oscuro' || (a === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);\n"
        '  raiz.setAttribute("data-theme", oscuro ? "dark" : "light");\n'
        '  if (oscuro) raiz.setAttribute("data-tema", "oscuro");\n'
        '  raiz.setAttribute("data-qhawana", "");\n'
        "  /* Dentro del marco del anfitrión la navegación es la suya (se oculta la barra). */\n"
        '  try { if (window.self !== window.top) raiz.setAttribute("data-incrustado", ""); }\n'
        '  catch (e) { raiz.setAttribute("data-incrustado", ""); }\n'
        "})();\n"
        "</script>"
    )
    secciones = {
        "arranque": arranque,
        "estilos": estilos,
        # Sin regreso ni interruptor: el marco del anfitrión pone la marca y la navegación.
        "herramientas": "",
        "pie": f"    {pie}",
    }
    return "".join(f"<!-- tema:{k} -->\n{v}\n" for k, v in secciones.items())


def tema_unancha(tokens: Path) -> tuple[dict, dict, str]:
    """(clara, oscura, letra) desde los tokens de Unancha (colors.json y typography.json), con los roles de `_variables`."""
    c = json.loads((tokens / "colors.json").read_text(encoding="utf-8"))
    t = json.loads((tokens / "typography.json").read_text(encoding="utf-8"))
    e, g = c["escalas"], c["interfaz"]["grafito"]
    puka, qillu, neutral = e["puka"], e["qillu"], e["neutral"]
    clara = {
        "fondo": c["fondos"]["papel"]["hex"], "superficie": c["fondos"]["blanco"]["hex"], "superficieTenue": neutral["200"],
        "superficieMedia": neutral["300"], "texto": neutral["900"], "textoSecundario": neutral["700"], "textoTenue": neutral["600"],
        "primario": puka["800"], "primarioClaro": puka["600"], "sobrePrimario": c["fondos"]["blanco"]["hex"],
        "primarioSuave": puka["50"], "exito": c["funcionales"]["exito"], "exitoFondo": "rgba(46, 125, 50, 0.10)",
        "borde": neutral["300"], "bordeFuerte": neutral["400"], "sombra": "0 1px 3px rgba(36, 31, 28, 0.12)",
        "velo": "rgba(36, 31, 28, 0.04)", "info": c["funcionales"]["info_data_only"], "avisoOscuro": qillu["700"],
    }
    oscura = {
        "fondo": g["900"], "superficie": g["800"], "superficieTenue": g["850"], "superficieMedia": g["700"],
        "texto": neutral["100"], "textoSecundario": g["300"], "textoTenue": g["400"],
        "primario": puka["300"], "primarioClaro": puka["200"], "sobrePrimario": g["950"], "primarioSuave": "rgba(229, 130, 146, 0.14)",
        "exito": c["interfaz"]["exito"]["hex"], "exitoFondo": "rgba(93, 179, 126, 0.14)", "borde": g["650"], "bordeFuerte": g["500"],
        "sombra": "0 1px 3px rgba(0, 0, 0, 0.5)", "velo": "rgba(255, 255, 255, 0.05)", "info": g["300"], "avisoOscuro": qillu["300"],
    }
    letra = ", ".join(f'"{f}"' if " " in f else f for f in t["familias"]["body"]["stack"])
    return clara, oscura, letra
