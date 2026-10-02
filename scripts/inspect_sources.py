"""Inspección de CSV originales. Sin limpieza, imputación ni métricas comerciales.

Ejecutar desde cualquier directorio: python3 scripts/inspect_sources.py
Salidas regenerables: artifacts/inspeccion/{informe.html,resultado.json,ejecucion.txt}.
"""
import csv
import hashlib
import html
import json
import shlex
import sys
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_csv(path):
    """Cuenta registros después del encabezado, incluidas filas vacías/defectuosas."""
    before = digest(path)
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, delimiter=",", strict=True)
        columns = next(reader)
        if not columns or len(set(columns)) != len(columns):
            raise ValueError(f"Encabezado vacío/duplicado: {path.name}")
        missing = Counter({column: 0 for column in columns})
        seen = set()
        samples, issues, empty_records = [], [], []
        duplicates = 0
        ids, periods, categories = set(), set(), Counter()
        key_counts = Counter()
        amounts = {"zero_rows": 0, "negative_rows": 0, "invalid_records": []}
        total = Decimal(0)
        count = 0
        for count, values in enumerate(reader, 1):
            row = tuple(values)
            if row in seen:
                duplicates += 1
            seen.add(row)
            if count <= 3:
                samples.append({"record": count, "line_end": reader.line_num,
                                "values": values})
            if len(values) != len(columns):
                issues.append({"record": count, "line_end": reader.line_num,
                               "values": values, "reason": "Número de campos incorrecto"})
                continue
            record = dict(zip(columns, values))
            for column, value in record.items():
                missing[column] += not value.strip()
            if all(not value.strip() for value in values):
                empty_records.append(count)
                continue
            if record.get("ID", "").strip():
                ids.add(record["ID"])
            period = record.get("month", record.get("Month", ""))
            if period:
                periods.add(period)
            if "Industria" in record:
                categories[record["Industria"]] += 1
            if "ID" in record and "month" in record:
                key_counts[(record["ID"], record["month"])] += 1
            if "amount" in record:
                try:
                    amount = Decimal(record["amount"])
                    if not amount.is_finite():
                        raise InvalidOperation
                    total += amount
                    amounts["zero_rows"] += amount == 0
                    amounts["negative_rows"] += amount < 0
                except InvalidOperation:
                    amounts["invalid_records"].append(count)
        amounts["sum_original"] = str(total)
    after = digest(path)
    if before != after:
        raise RuntimeError(f"La fuente cambió durante la lectura: {path.name}")
    return {"filename": path.name, "sha256": before, "sha256_after": after,
            "bytes": path.stat().st_size, "rows": count, "columns": columns,
            "missing_by_column": dict(missing), "duplicate_rows": duplicates,
            "malformed_rows": len(issues), "issues": issues,
            "empty_records": empty_records, "samples": samples,
            "distinct_nonempty_ids": len(ids), "periods_original": sorted(periods),
            "categories": dict(categories), "amount": amounts,
            "duplicate_customer_month_keys": sum(n - 1 for n in key_counts.values())}


def cell(value):
    return html.escape(str(value), quote=True)


def table(headers, rows):
    return '<div class="scroll"><table><thead><tr>' + ''.join(
        f'<th>{cell(h)}</th>' for h in headers
    ) + '</tr></thead><tbody>' + ''.join(
        '<tr>' + ''.join(f'<td>{cell(v)}</td>' for v in row) + '</tr>'
        for row in rows
    ) + '</tbody></table></div>'


def report_html(result):
    overview = table(["Archivo", "Registros", "Campos", "Vacíos completos", "Defectuosos"],
                     [[p["filename"], p["rows"], len(p["columns"]),
                       len(p["empty_records"]), p["malformed_rows"]]
                      for p in result["sources"]])
    sections = []
    for p in result["sources"]:
        samples = table(["Registro", "Línea final"] + p["columns"],
                        [[s["record"], s["line_end"]] + s["values"]
                         for s in p["samples"]])
        controls = table(["Comprobación", "Resultado"], [
            ["Campos vacíos (filas con número de campos correcto)",
             json.dumps(p["missing_by_column"], ensure_ascii=False)],
            ["Filas repetidas exactas", p["duplicate_rows"]],
            ["IDs distintos no vacíos, sin normalizar", p["distinct_nonempty_ids"]],
            ["Periodos originales, sin convertir", ', '.join(p["periods_original"])],
            ["Registros completamente vacíos", str(p["empty_records"])],
            ["Campos incorrectos", json.dumps(p["issues"], ensure_ascii=False)],
            ["Archivo intacto antes/después", p["sha256"] == p["sha256_after"]],
        ])
        amount = ''
        if 'amount' in p['columns']:
            amount = table(["Importes originales, sin unidad inferida", "Resultado"], [
                ["Ceros", p["amount"]["zero_rows"]],
                ["Negativos", p["amount"]["negative_rows"]],
                ["Registros no numéricos/finitos", p["amount"]["invalid_records"]],
                ["Suma decimal original", p["amount"]["sum_original"]],
                ["Duplicados ID + month", p["duplicate_customer_month_keys"]],
            ])
        comparison = table(["Control frente al perfil anterior", "Coincide"],
                           p["baseline_checks"].items())
        sections.append(f'<section><h2>{cell(p["filename"])}</h2>'
                        f'<p>Primeros tres registros de datos; encabezado excluido.</p>{samples}'
                        f'<details><summary>Controles y contraste anterior</summary>{controls}'
                        f'{amount}{comparison}<p>SHA-256: <code>{p["sha256"]}</code></p>'
                        '</details></section>')
    return f'''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Inspección de fuentes</title><style>
body{{font:16px/1.5 system-ui;background:#f4f6f8;color:#172334;margin:0}}
main{{max-width:1050px;margin:auto;padding:28px}}section{{background:white;padding:20px;margin:20px 0;border-radius:10px}}
h1,h2{{line-height:1.2}}table{{width:100%;border-collapse:collapse;margin:12px 0}}
th,td{{text-align:left;padding:9px;border-bottom:1px solid #dce2e8;vertical-align:top}}
th{{background:#eaf0f5}}.scroll{{overflow-x:auto}}code{{overflow-wrap:anywhere}}
summary{{cursor:pointer;font-weight:600}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
</style><main><h1>Inspección de fuentes</h1>
<p>{cell(result["executed_at"])} · Ejecución: Codex · Revisión del candidato: pendiente.</p>
<p>Lectura de CSV UTF-8, coma como separador. Fuentes intactas; sin limpieza, joins, conversión de unidades ni conclusiones comerciales.</p>
{overview}{''.join(sections)}
<section><h2>Lo que estos controles no demuestran</h2>
<p>Los ceros no prueban churn. La suma de amount no prueba MRR. S&amp;M conserva textos monetarios sin interpretar escala. Los IDs de Industry y Transactions necesitan una regla de correspondencia validada. Faltan eventos de etapas/contactos del CRM.</p></section>
<section><h2>Reproducir y revisar</h2><pre>{cell(result["command"])}</pre>
<p>Script: scripts/inspect_sources.py. Resultados completos: resultado.json. Registro de ejecución: ejecucion.txt.
Las muestras son verificables por registro/línea en inputs/. El contraste anterior comprueba consistencia técnica; no sustituye revisión humana ni prueba significado comercial.</p>
<p>Versión Python: {cell(result["python_version"])}. SHA-256 del script: <code>{result["script_sha256"]}</code></p></section></main></html>'''


def main():
    baseline = json.loads((ROOT / "docs/datos/data_profile.json").read_text())
    result = {"executed_at": datetime.now(ZoneInfo("America/Bogota")).isoformat(),
              "command": shlex.join([sys.executable, str(Path(__file__).resolve())]),
              "python_version": sys.version.split()[0],
              "script_sha256": digest(Path(__file__)),
              "human_review": "Pendiente", "sources": []}
    passed = True
    for old in baseline["sources"]:
        path = ROOT / old["filename"]
        current = inspect_csv(path)
        current["filename"] = old["filename"]
        current["baseline_checks"] = {
            name: current[name] == old[name]
            for name in ["sha256", "rows", "columns", "missing_by_column",
                         "duplicate_rows", "malformed_rows"]
        }
        if "amount" in current["columns"]:
            current["baseline_checks"].update({
                "zero_amount_rows": current["amount"]["zero_rows"] == old["zero_amount_rows"],
                "negative_amount_rows": current["amount"]["negative_rows"] == old["negative_amount_rows"],
                "amount_sum_original": Decimal(current["amount"]["sum_original"]) == Decimal(old["amount_sum_original"]),
                "duplicate_customer_month_keys": current["duplicate_customer_month_keys"] == old["duplicate_customer_month_keys"],
            })
        passed = passed and all(current["baseline_checks"].values())
        result["sources"].append(current)
    result["baseline_matches"] = passed
    output = ROOT / "artifacts/inspeccion"
    output.mkdir(parents=True, exist_ok=True)
    (output / "resultado.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (output / "informe.html").write_text(report_html(result), encoding="utf-8")
    lines = [result["executed_at"], result["command"],
             f'Script SHA-256: {result["script_sha256"]}',
             *[f'{p["filename"]}: {p["rows"]} registros; SHA-256 {p["sha256"]}; '
               f'contraste anterior {all(p["baseline_checks"].values())}' for p in result["sources"]],
             f'Controles anteriores coinciden: {passed}',
             'Ejecución: Codex. Revisión del candidato: pendiente.',
             'Código de salida: ' + ('0' if passed else '1')]
    (output / "ejecucion.txt").write_text('\n'.join(lines) + '\n', encoding="utf-8")
    print('\n'.join(lines))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
