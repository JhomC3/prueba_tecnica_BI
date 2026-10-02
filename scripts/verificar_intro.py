"""Verificación en navegador de la intro «cómo se construyó» (CRO/CFO).

Uso:
    pnpm exec vite --host 127.0.0.1 --port 60403   # terminal 1
    /private/var/folders/.../pw-env/bin/python scripts/verificar_intro.py   # terminal 2
    # (entorno con `playwright` instalado; reutiliza los navegadores de `npx playwright`)

Comprueba: intro visible en ambos casos, ancla directa, multiselección real,
retirar/limpiar/reseleccionar, separación por caso, descarga real y móvil 390.
No envía nada a red: la selección de archivos no debe generar peticiones.
"""
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("FINORA_URL", "http://127.0.0.1:60403")
RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "docs/web/capturas-intro"
OUT.mkdir(parents=True, exist_ok=True)
TMP = Path(os.environ.get("TMPDIR", "/tmp")) / "adjuntos-prueba"
TMP.mkdir(exist_ok=True)
F1 = TMP / "notas-cartera.csv"
F1.write_text("cuenta,nota\nC001,llamar en junio\n", encoding="utf-8")
F2 = TMP / "descuento-extra.csv"
F2.write_bytes(b"cuenta,monto\nC002,30\n")

red = []
errores = []

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errores.append(str(e)))
    pg.on("request", lambda r: red.append(f"{r.method} {r.url}") if r.method != "GET" else None)

    for caso in ["cro", "cfo"]:
        pg.goto(f"{BASE}/#/{caso}", wait_until="domcontentloaded")
        pg.wait_for_selector("#intro", timeout=10000)
        pg.wait_for_timeout(2500)
        pg.screenshot(path=str(OUT / f"{caso}-intro.png"))
        assert pg.locator("#intro .cab h2").first.inner_text() == "Cómo se construyó este análisis"
        assert "Archivo recibido" in pg.content()
        pg.goto(f"{BASE}/#/{caso}/intro", wait_until="domcontentloaded")
        pg.wait_for_timeout(800)
        assert pg.locator("#intro").count() == 1

    pg.goto(f"{BASE}/#/cro", wait_until="domcontentloaded")
    pg.wait_for_selector("#adjuntos-cro input[type=file]")
    n_red_antes = len(red)
    pg.locator("#adjuntos-cro input[type=file]").set_input_files([str(F1), str(F2)])
    pg.wait_for_timeout(500)
    estado = pg.locator("#adjuntos-cro [data-rol=estado]").inner_text()
    items = pg.locator("#adjuntos-cro [data-rol=lista] li").all_inner_texts()
    print("CRO estado:", estado)
    print("CRO items:", items)
    assert "2 archivo(s) seleccionado(s) localmente" in estado
    assert any("notas-cartera.csv" in i and "Seleccionado localmente" in i for i in items)
    assert len(red) == n_red_antes, f"la selección generó red: {red[n_red_antes:]}"
    pg.locator("#adjuntos-cro").scroll_into_view_if_needed()
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT / "cro-adjuntos.png"))

    pg.locator("#adjuntos-cro [data-retirar='0']").click()
    pg.wait_for_timeout(300)
    assert "1 archivo(s)" in pg.locator("#adjuntos-cro [data-rol=estado]").inner_text()
    pg.locator("#adjuntos-cro input[type=file]").set_input_files([str(F1)])
    pg.wait_for_timeout(300)
    assert "2 archivo(s)" in pg.locator("#adjuntos-cro [data-rol=estado]").inner_text()
    pg.locator("#adjuntos-cro [data-rol=limpiar]").click()
    pg.wait_for_timeout(300)
    assert "Ningún archivo" in pg.locator("#adjuntos-cro [data-rol=estado]").inner_text()

    pg.locator("#adjuntos-cro input[type=file]").set_input_files([str(F1)])
    pg.wait_for_timeout(300)
    pg.goto(f"{BASE}/#/cfo", wait_until="domcontentloaded")
    pg.wait_for_selector("#adjuntos-cfo input[type=file]")
    assert "Ningún archivo" in pg.locator("#adjuntos-cfo [data-rol=estado]").inner_text()
    pg.locator("#adjuntos-cfo input[type=file]").set_input_files([str(F2)])
    pg.wait_for_timeout(300)
    assert "1 archivo(s)" in pg.locator("#adjuntos-cfo [data-rol=estado]").inner_text()
    pg.goto(f"{BASE}/#/cro", wait_until="domcontentloaded")
    pg.wait_for_selector("#adjuntos-cro input[type=file]")
    pg.wait_for_timeout(400)
    assert "1 archivo(s)" in pg.locator("#adjuntos-cro [data-rol=estado]").inner_text()
    print("separación por caso OK")

    pg.locator("#intro details summary", has_text="D. Datos").click()
    pg.wait_for_timeout(400)
    with pg.expect_download() as dl:
        pg.locator("#intro a[download]").first.click()
    d = dl.value
    ruta = OUT / ("descarga-" + d.suggested_filename)
    d.save_as(str(ruta))
    print("descarga:", ruta, ruta.stat().st_size, "B")

    m = b.new_page(viewport={"width": 390, "height": 844})
    m.goto(f"{BASE}/#/cfo", wait_until="domcontentloaded")
    m.wait_for_selector("#intro", timeout=10000)
    m.wait_for_timeout(2000)
    m.screenshot(path=str(OUT / "cfo-intro-mobile.png"))
    desborde = m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    print("desborde móvil:", desborde)
    assert desborde <= 1
    b.close()

print("errores consola:", errores if errores else "ninguno")
print("peticiones no-GET:", red if red else "ninguna")
print("TODO-NAVEGADOR-OK")
