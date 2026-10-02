"""Exporta historia CFO desde resultados vigentes, sin modificar fuentes.

Lee (fuente):
- notebooks/03_modelo_cfo.ipynb (rev. 298dbb74, 23 celdas, 2 Plotly)
- resultados/cfo/graficas/principal/{10_evolucion_principal,12_recuperacion_foco}.html + plotly.min.js
- resultados/cfo/metricas/principal/*.csv + foco_resumen.json

Escribe (dest):
- public/charts/cfo/*.html + plotly.min.js (copia exacta de bytes)
- public/data/cfo-story-manifest.json (hashes, revision, escenario, validaciones)

Verifica coherencia figura↔CSV↔conclusión antes de copiar. No modifica
notebook/CSV ni genera metricas nuevas.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

ESPERADO_NOTEBOOK_SHA = "298dbb74c6bb5f9eb7b1fa780ab428c8a8d17af3b38cadd8967697677fa5f315"
ESPERADO_CELDAS = 23
ESPERADO_PLOTLY = 2
FIGURAS = [
    ("S05-mrr", 14, 0, "MRR bruto y neto con y sin política", "10_evolucion_principal.html"),
    ("S06-recuperacion", 17, 0, "¿La ampliación compensa los descuentos?", "12_recuperacion_foco.html"),
]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def leer_csv_dict(p: Path):
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fuente", required=True)
    ap.add_argument("--dest", required=True)
    args = ap.parse_args()
    fuente = Path(args.fuente)
    dest = Path(args.dest)

    nb_path = fuente / "notebooks/03_modelo_cfo.ipynb"
    h_nb = sha256(nb_path)
    if h_nb != ESPERADO_NOTEBOOK_SHA:
        raise SystemExit(f"notebook cambio: {h_nb} != esperado {ESPERADO_NOTEBOOK_SHA}. Abortar y repetir archivos afectados.")
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    if len(nb.get("cells", [])) != ESPERADO_CELDAS:
        raise SystemExit(f"celdas inesperadas: {len(nb['cells'])}")
    n_plotly = sum(1 for c in nb["cells"] if c.get("cell_type") == "code" for o in c.get("outputs", []) if "application/vnd.plotly.v1+json" in o.get("data", {}))
    if n_plotly != ESPERADO_PLOTLY:
        raise SystemExit(f"plotly inesperados: {n_plotly}")

    mapa = json.loads((dest / "docs/web/cfo-mapa.json").read_text(encoding="utf-8"))
    if mapa["snapshot"]["notebook_sha256"] != h_nb:
        raise SystemExit("mapa y notebook no coinciden en hash")

    met = fuente / "resultados/cfo/metricas/principal"
    men = leer_csv_dict(met / "mensual.csv")
    if any(abs(float(r["bruto"]) - float(r["descuentos"]) - float(r["neto"])) > 0.01 for r in men):
        raise SystemExit("bruto − descuento != neto en mensual.csv")
    cierre = {(r["mes"], r["grupo"]): float(r["neto"]) / 100 for r in men if r["mes"] == "2026-03-01"}
    if cierre.get(("2026-03-01", "con_descuento")) != 10300.0 or cierre.get(("2026-03-01", "sin_descuento")) != 9800.0:
        raise SystemExit(f"cierre inesperado: {cierre}")
    foco = {r["mes"]: (float(r["diferencia_acumulada"]) / 100, float(r["aumento_bruto_acumulado"]) / 100, float(r["descuento_acumulado"]) / 100) for r in leer_csv_dict(met / "foco_comparacion.csv")}
    if foco.get("2026-03-01") != (-1500.0, 4500.0, 6000.0):
        raise SystemExit(f"recuperacion inesperada: {foco.get('2026-03-01')}")
    resumen = json.loads((met / "foco_resumen.json").read_text(encoding="utf-8"))
    if resumen.get("diferencia_acumulada") != -150000 or resumen.get("aumento_bruto_acumulado") != 450000 or resumen.get("descuento_acumulado") != 600000:
        raise SystemExit("foco_resumen no concilia +4500−6000=−1500")
    fases = {(r["poblacion"], r["fase"]): float(r["diferencia_neta"]) / 100 for r in leer_csv_dict(met / "focos.csv")}
    if fases.get(("Elegibles", "durante")) != -4500.0 or fases.get(("Elegibles", "posterior")) != 3000.0:
        raise SystemExit(f"fases inesperadas: {fases}")

    graf = fuente / "resultados/cfo/graficas/principal"
    for _, cell, out, titulo, _archivo in FIGURAS:
        outs = nb["cells"][cell].get("outputs", [])
        data = outs[out].get("data", {})
        if "application/vnd.plotly.v1+json" not in data:
            raise SystemExit(f"output no es plotly en celda {cell}")
        if data["application/vnd.plotly.v1+json"].get("layout", {}).get("title", {}).get("text") != titulo:
            raise SystemExit(f"titulo inesperado en celda {cell}")
    out_dir = dest / "public/charts/cfo"
    out_dir.mkdir(parents=True, exist_ok=True)
    lib_origen = graf / "plotly.min.js"
    lib_dest = dest / "public/charts/plotly.min.js"
    lib_dest.write_text(lib_origen.read_text(encoding="utf-8"), encoding="utf-8")
    if sha256(lib_dest) != sha256(lib_origen):
        raise SystemExit("copia de plotly.min.js difiere")
    exportados = []
    for bloque, _cell, _out, titulo, archivo in FIGURAS:
        origen = graf / archivo
        destino = out_dir / archivo
        html = origen.read_text(encoding="utf-8")
        if 'src="plotly.min.js"' not in html:
            raise SystemExit(f"cargador local inesperado en origen: {archivo}")
        html2 = html.replace('src="plotly.min.js"', 'src="../plotly.min.js"')
        if 'src="plotly.min.js"' in html2:
            raise SystemExit(f"sustitución del cargador fallida: {archivo}")
        destino.write_text(html2, encoding="utf-8")
        resto_origen = html.replace('src="plotly.min.js"', '')
        resto_destino = html2.replace('src="../plotly.min.js"', '')
        if resto_origen != resto_destino:
            raise SystemExit(f"cambio más allá del cargador: {archivo}")
        exportados.append({"bloque": bloque, "archivo": f"charts/cfo/{archivo}", "sha256": sha256(destino), "titulo": titulo})
    vieja = out_dir / "plotly.min.js"
    if vieja.exists():
        vieja.unlink()
        print("retirada copia duplicada: charts/cfo/plotly.min.js")

    manifest = {
        "revision": "notebook-final-298dbb74",
        "fecha": "2026-10-02",
        "escenario": "principal (datos sintéticos)",
        "poblacion": "110 clientes por alternativa; foco de 50 elegibles; referencia pareada",
        "periodo": "enero 2025–marzo 2026 (6 previos, 3 de descuento, 6 posteriores)",
        "fuentes": {
            "notebook": {"archivo": "notebooks/03_modelo_cfo.ipynb", "sha256": h_nb},
            "mensual_csv_sha256": sha256(met / "mensual.csv"),
            "foco_comparacion_sha256": sha256(met / "foco_comparacion.csv"),
            "focos_csv_sha256": sha256(met / "focos.csv"),
            "foco_resumen": resumen,
        },
        "validaciones": {
            "celdas": len(nb["cells"]),
            "plotly": n_plotly,
            "bruto_menos_descuento_igual_neto": True,
            "cierre_con": cierre.get(("2026-03-01", "con_descuento")),
            "cierre_sin": cierre.get(("2026-03-01", "sin_descuento")),
            "diferencia_acumulada": foco.get("2026-03-01")[0],
            "fases_elegibles": {"durante": fases.get(("Elegibles", "durante")), "posterior": fases.get(("Elegibles", "posterior"))},
        },
        "figuras": exportados,
        "plotly_lib": {"archivo": "charts/plotly.min.js", "sha256": sha256(lib_dest), "version": "4.1.1", "origen": "resultados/cfo/graficas/principal/plotly.min.js"},
        "nota": "Figuras con datos idénticos al origen; solo el cargador apunta a la biblioteca local compartida. Conclusiones como texto en src/content/cfo.json.",
    }
    (dest / "public/data/cfo-story-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"figuras exportadas: {len(exportados)}")
    for e in exportados:
        print(f" - {e['bloque']}: {e['archivo']}")
    print("manifiesto: public/data/cfo-story-manifest.json")


if __name__ == "__main__":
    main()
