"""Exporta historia CRO desde el notebook terminado, sin modificar fuentes.

Lee (fuente):
- notebooks/02_modelo_cro.ipynb (rev. 987c30a9, 53 celdas, 12 Plotly)
- resultados/cro/metricas/referencia/*.csv, control_coherencia.json
- datos/sinteticos/cro/referencia/dim_capacidad.csv

Escribe (dest):
- public/charts/cro-story/*.html (Plotly con biblioteca local compartida ../plotly.min.js)
- public/charts/plotly.min.js (copia de la biblioteca v4.1.1 verificada)
- public/data/cro-story-manifest.json (hashes, revision, escenario, validaciones)

Elimina HTML de figuras que el notebook terminado ya no contiene.
No modifica notebook/CSV ni genera metricas nuevas. No usa analisis.html antiguo.
La reescritura del cargador cambia bytes, no datos: el exportador comprueba
que no quede CDN y registra el hash de la biblioteca compartida.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ESPERADO_NOTEBOOK_SHA = "987c30a9ccc181c30143229c4d584c2a7fdffdac1ca92c8aa505c58d6c8f711d"
ESPERADO_CELDAS = 53
ESPERADO_PLOTLY = 12


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

    nb_path = fuente / "notebooks/02_modelo_cro.ipynb"
    if not nb_path.exists():
        raise SystemExit(f"falta notebook: {nb_path}")
    h_nb = sha256(nb_path)
    if h_nb != ESPERADO_NOTEBOOK_SHA:
        raise SystemExit(f"notebook cambio: {h_nb} != esperado {ESPERADO_NOTEBOOK_SHA}. Abortar y repetir archivos afectados.")
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    if len(nb.get("cells", [])) != ESPERADO_CELDAS:
        raise SystemExit(f"celdas inesperadas: {len(nb['cells'])}")
    n_plotly = sum(1 for c in nb["cells"] if c.get("cell_type") == "code" for o in c.get("outputs", []) if "application/vnd.plotly.v1+json" in o.get("data", {}))
    if n_plotly != ESPERADO_PLOTLY:
        raise SystemExit(f"plotly inesperados: {n_plotly}")

    mapa_path = dest / "docs/web/cro-mapa.json"
    mapa = json.loads(mapa_path.read_text(encoding="utf-8"))
    if mapa["snapshot"]["notebook_sha256"] != h_nb:
        raise SystemExit("mapa y notebook no coinciden en hash")

    ref = fuente / "resultados/cro/metricas/referencia"
    demanda = leer_csv_dict(ref / "demanda.csv")
    d = {(r["mes"]): int(r["entradas_new"]) for r in demanda if r.get("dimension") == "total" and r.get("segmento") == "Todos"}
    if d.get("2026-04") != 133 or d.get("2026-05") != 179:
        raise SystemExit(f"New 04/05 inesperado: {d.get('2026-04')}/{d.get('2026-05')}")
    cohortes = leer_csv_dict(ref / "cohortes.csv")
    coh = {(r["mes_entrada"], r["segmento"]): float(r["conversion_new_won_pct"]) for r in cohortes if r.get("dimension") == "total" and r.get("ventana") == "30"}
    if round(coh.get(("2026-04", "Todos")), 1) != 21.1 or round(coh.get(("2026-05", "Todos")), 1) != 6.7:
        raise SystemExit(f"cohortes 04/05 inesperadas: {coh.get(('2026-04', 'Todos'))}/{coh.get(('2026-05', 'Todos'))}")
    etapas = leer_csv_dict(ref / "etapas_new.csv")
    et = {(r["mes"], r["etapa"]): round(float(r["conversion_pct"]), 1) for r in etapas if r.get("dimension") == "total" and r.get("segmento") == "Todos" and r.get("ventana") == "30"}
    esperado_et = {("2026-04", "Demo"): 76.2, ("2026-05", "Demo"): 61.8, ("2026-04", "Proposal"): 58.3, ("2026-05", "Proposal"): 19.0}
    if et and {k: et.get(k) for k in esperado_et} != esperado_et:
        raise SystemExit(f"etapas inesperadas: {et}")
    at = leer_csv_dict(ref / "atencion_focos_new.csv")
    dem = {(r["mes"], r["etapa"]): (r["cuentas_con_visita"], r["cuentas_con_intento"], r["mediana_primer_intento"]) for r in at if r.get("dimension") == "total" and r.get("segmento") == "Todos"}
    if dem.get(("2026-04", "Demo")) != ("58", "41", "3.0") or dem.get(("2026-05", "Proposal")) != ("63", "29", "4.0"):
        raise SystemExit(f"demora inesperada: {dem.get(('2026-04', 'Demo'))}/{dem.get(('2026-05', 'Proposal'))}")
    cap = leer_csv_dict(fuente / "datos/sinteticos/cro/referencia/dim_capacidad.csv")
    per = {(r["mes"], r["id_etapa"]): (r["personal_disponible"], r["capacidad_mensual_por_persona"]) for r in cap}
    if per.get(("2026-04", "Demo")) != ("10", "11") or per.get(("2026-05", "Proposal")) != ("8", "10"):
        raise SystemExit(f"capacidad inesperada: {per.get(('2026-04', 'Demo'))}/{per.get(('2026-05', 'Proposal'))}")
    control = json.loads((ref / "control_coherencia.json").read_text(encoding="utf-8"))
    if control.get("cohortes_conciliadas", 0) <= 0:
        raise SystemExit("control_coherencia sin cohortes conciliadas")

    try:
        import plotly.io as pio
    except ImportError:
        raise SystemExit("falta plotly en el entorno Python (.venv con plotly requerido, sin añadir paquetes por defecto)")
    import plotly.graph_objects as go
    out_dir = dest / "public/charts/cro-story"
    out_dir.mkdir(parents=True, exist_ok=True)
    lib_origen = fuente / "resultados/cfo/graficas/principal/plotly.min.js"
    lib_texto = lib_origen.read_text(encoding="utf-8")
    if "plotly.js v4.1.1" not in lib_texto[:500]:
        raise SystemExit("biblioteca local inesperada: no es plotly v4.1.1")
    lib_dest = dest / "public/charts/plotly.min.js"
    lib_dest.write_text(lib_texto, encoding="utf-8")
    exportados = []
    for cap in mapa["capitulos"]:
        for b in cap["bloques"]:
            figref = b.get("figura")
            if not figref:
                continue
            outs = nb["cells"][figref["cell"]].get("outputs", [])
            if figref["output"] >= len(outs):
                raise SystemExit(f"output fuera de rango {cap['id']}/{b['id']}")
            data = outs[figref["output"]].get("data", {})
            if "application/vnd.plotly.v1+json" not in data:
                raise SystemExit(f"output no es plotly {cap['id']}/{b['id']}")
            fig = go.Figure(data["application/vnd.plotly.v1+json"])
            titulo_original = fig.layout.title.text if fig.layout.title else None
            titulo_web = figref.get("titulo_web") or figref["titulo"]
            if titulo_web != titulo_original:
                fig.update_layout(title_text=titulo_web)
            dest_file = out_dir / figref["export"]
            pio.write_html(fig, str(dest_file), full_html=True, include_plotlyjs="cdn", config={"responsive": True, "displaylogo": False})
            html = dest_file.read_text(encoding="utf-8")
            cdn_tag = [l for l in html.split("src=") if "cdn.plot.ly" in l]
            if not cdn_tag:
                raise SystemExit(f"sin etiqueta CDN para sustituir {cap['id']}/{b['id']}")
            import re as _re
            html2, n = _re.subn(r'<script[^>]*src="https://cdn\.plot\.ly/[^"]*"[^>]*></script>', '<script charset="utf-8" src="../plotly.min.js"></script>', html)
            if n != 1 or "cdn.plot.ly" in html2:
                raise SystemExit(f"sustitución del cargador fallida {cap['id']}/{b['id']}")
            dest_file.write_text(html2, encoding="utf-8")
            exportados.append({"bloque": b["id"], "archivo": f"charts/cro-story/{figref['export']}", "sha256": sha256(dest_file), "cell": figref["cell"], "output": figref["output"], "titulo_original": titulo_original, "titulo_web": titulo_web})
    esperados = {e["archivo"] for e in exportados}
    for viejo in out_dir.glob("*.html"):
        if f"charts/cro-story/{viejo.name}" not in esperados:
            viejo.unlink()
            print(f"retirada figura obsoleta: {viejo.name}")

    manifest = {
        "revision": "notebook-final-987c30a9",
        "fecha": "2026-10-02",
        "escenario": "referencia (datos sintéticos)",
        "poblacion": "cuentas que entraron por New; SQL directo y producto fuera de New→Won",
        "fuentes": {
            "notebook": {"archivo": "notebooks/02_modelo_cro.ipynb", "sha256": h_nb},
            "demanda_csv_sha256": sha256(ref / "demanda.csv"),
            "cohortes_csv_sha256": sha256(ref / "cohortes.csv"),
            "etapas_new_sha256": sha256(ref / "etapas_new.csv"),
            "atencion_focos_new_sha256": sha256(ref / "atencion_focos_new.csv"),
            "dim_capacidad_sha256": sha256(fuente / "datos/sinteticos/cro/referencia/dim_capacidad.csv"),
            "control_coherencia": control,
        },
        "validaciones": {
            "celdas": len(nb["cells"]),
            "plotly": n_plotly,
            "new_abril": d.get("2026-04"),
            "new_mayo": d.get("2026-05"),
            "conv_abril": round(coh.get(("2026-04", "Todos")), 1),
            "conv_mayo": round(coh.get(("2026-05", "Todos")), 1),
            "demo_abril": et.get(("2026-04", "Demo")),
            "demo_mayo": et.get(("2026-05", "Demo")),
            "proposal_abril": et.get(("2026-04", "Proposal")),
            "proposal_mayo": et.get(("2026-05", "Proposal")),
            "cohortes_conciliadas": control.get("cohortes_conciliadas"),
        },
        "figuras": exportados,
        "plotly_lib": {"archivo": "charts/plotly.min.js", "sha256": sha256(lib_dest), "version": "4.1.1", "origen": "resultados/cfo/graficas/principal/plotly.min.js"},
        "nota": "Figuras ya calculadas exportadas sin reescribir ejes/unidades/títulos. Conclusiones como texto en src/content/cro.json; este manifiesto no duplica textos.",
    }
    man_path = dest / "public/data/cro-story-manifest.json"
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"figuras exportadas: {len(exportados)}")
    for e in exportados:
        print(f" - {e['bloque']}: {e['archivo']}")
    print("manifiesto: public/data/cro-story-manifest.json")


if __name__ == "__main__":
    main()
