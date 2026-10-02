"""Exportación para la web: copia y verifica sin recalcular métricas.

Lee del checkout original (--fuente) y escribe en el worktree (--dest):
- public/charts/01_new_tendencia.html (copia exacta de bytes)
- public/data/new_serie_referencia.json (entradas_new + crecimiento_new_pct leído del CSV)
- public/content/*.json (copia de src/content/*.json)
- public/data/manifest.json (hashes y metadatos derivados, sin valores fijados)

La variación mensual se lee de la columna ya calculada `crecimiento_new_pct`
del CSV y solo se redondea a un decimal para la tabla. No se deriva de
`entradas_new`. Los meses y valores se validan por estructura (unicidad,
orden, tipos), no contra una lista fija.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

MES_RX = re.compile(r"^\d{4}-\d{2}$")
COLUMNAS_REQUERIDAS = {
    "mes", "segmento", "entradas_new", "crecimiento_new_pct", "dimension",
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fuente", required=True, help="Checkout original con resultados/cro")
    ap.add_argument("--dest", required=True, help="Raíz del worktree frontend")
    args = ap.parse_args()
    fuente = Path(args.fuente)
    dest = Path(args.dest)

    figura_origen = fuente / "resultados/cro/graficas/01_new_tendencia.html"
    demanda_origen = fuente / "resultados/cro/metricas/referencia/demanda.csv"
    for p in (figura_origen, demanda_origen):
        if not p.exists():
            raise SystemExit(f"falta fuente requerida: {p}")

    with demanda_origen.open(newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        if not COLUMNAS_REQUERIDAS.issubset(set(lector.fieldnames or [])):
            raise SystemExit(f"columnas inesperadas en demanda.csv: {lector.fieldnames}")
        filas = [r for r in lector if r["dimension"] == "total" and r["segmento"] == "Todos"]
    if not filas:
        raise SystemExit("sin filas total/Todos en demanda.csv")
    filas.sort(key=lambda r: r["mes"])

    meses = [r["mes"].strip() for r in filas]
    if len(set(meses)) != len(meses):
        raise SystemExit(f"meses duplicados: {meses}")
    if meses != sorted(meses):
        raise SystemExit(f"meses sin orden: {meses}")
    for m in meses:
        if not MES_RX.match(m):
            raise SystemExit(f"mes con formato inesperado: {m}")

    serie = []
    for r in filas:
        mes = r["mes"].strip()
        try:
            entradas = int(r["entradas_new"])
        except ValueError:
            raise SystemExit(f"entradas_new no entero en {mes}: {r['entradas_new']!r}")
        if entradas < 0:
            raise SystemExit(f"entradas_new negativo en {mes}: {entradas}")
        crudo = (r["crecimiento_new_pct"] or "").strip()
        var = None if crudo == "" else round(float(crudo), 1)
        serie.append({"mes": mes, "entradas_new": entradas, "variacion_mensual_pct": var})
    if serie[0]["variacion_mensual_pct"] is not None:
        raise SystemExit("la primera fila debe quedar sin comparación (crecimiento vacío)")

    (dest / "public/charts").mkdir(parents=True, exist_ok=True)
    (dest / "public/data").mkdir(parents=True, exist_ok=True)
    (dest / "public/content").mkdir(parents=True, exist_ok=True)

    figura_dest = dest / "public/charts/01_new_tendencia.html"
    shutil.copyfile(figura_origen, figura_dest)

    periodo = f"{meses[0]} a {meses[-1]}, por mes de entrada a New"
    serie_doc = {
        "escenario": "referencia (datos sintéticos)",
        "periodo": periodo,
        "unidad": "cuentas (entradas a New)",
        "poblacion": "cuentas que entraron por New, por mes de entrada",
        "fuente": "resultados/cro/metricas/referencia/demanda.csv (segmento total)",
        "nota_etiqueta": f"Datos sintéticos · escenario referencia · {meses[0]}–{meses[-1]}",
        "contexto": "Serie del CSV de referencia (segmento total). La variación mostrada es la columna crecimiento_new_pct ya calculada, redondeada a un decimal para la tabla; el primer mes no tiene comparación. Semilla, corte y reglas en docs/datos/modelo-cro-demo.md. No acredita qué pasó en Finora.",
        "valores": serie,
    }
    (dest / "public/data/new_serie_referencia.json").write_text(
        json.dumps(serie_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    contenidos = []
    for nombre in ("resumen.json", "cro.json", "cfo.json"):
        origen = dest / f"src/content/{nombre}"
        destino = dest / f"public/content/{nombre}"
        json.loads(origen.read_text(encoding="utf-8"))
        shutil.copyfile(origen, destino)
        contenidos.append({"archivo": f"content/{nombre}", "sha256": sha256(destino)})

    manifest = {
        "figura": {"archivo": "charts/01_new_tendencia.html", "sha256": sha256(figura_dest),
                   "origen_archivo": "resultados/cro/graficas/01_new_tendencia.html",
                   "origen_sha256": sha256(figura_origen)},
        "serie": {"archivo": "data/new_serie_referencia.json",
                  "sha256": sha256(dest / "public/data/new_serie_referencia.json"),
                  "origen_archivo": "resultados/cro/metricas/referencia/demanda.csv",
                  "origen_sha256": sha256(demanda_origen),
                  "n_meses": len(meses), "periodo": periodo, "meses": meses,
                  "nota_variacion": "columna crecimiento_new_pct del CSV, redondeada a 1 decimal"},
        "contenidos": contenidos,
    }
    if manifest["figura"]["sha256"] != manifest["figura"]["origen_sha256"]:
        raise SystemExit("la figura copiada difiere en bytes del original")
    (dest / "public/data/manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"figura bytes: {figura_dest.stat().st_size}")
    print(f"serie: {len(meses)} meses ({periodo})")
    print("contenidos:", ", ".join(c["archivo"] for c in contenidos))


if __name__ == "__main__":
    main()
