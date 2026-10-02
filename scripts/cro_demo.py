"""Demo CRO reproducible: generación -> SQLite -> SQL -> HTML autónomo.

Solo biblioteca estándar. Fuentes originales no se leen ni modifican.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import sqlite3
import statistics
from contextlib import closing
from datetime import date, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ["New", "Working", "Engaged", "SQL", "Demo", "Proposal", "Won"]
CHANNELS = ["Marketing pago", "Orgánico", "Referidos"]
SCENARIOS = {"referencia": "Referencia", "conversion": "Menor conversión", "demora": "Mayor permanencia"}
FIELDS = {
    "dim_cuentas": ["id_cuenta", "canal", "industria", "tipo_entrada"],
    "dim_etapas": ["id_etapa", "orden", "siguiente"],
    "fact_etapas": ["id_registro", "id_cuenta", "id_etapa", "entrada", "salida", "estado", "id_etapa_destino"],
    "vw_ganados": ["id_cuenta", "canal", "industria", "tipo_entrada", "fecha_entrada_inicial", "fecha_won", "dias_hasta_won"],
}
CSV_NAMES = {"vw_ganados": "ganados"}
DICTIONARY = {
    "dim_cuentas": ("Cuentas", "Empresas potenciales: cuándo llegaron, su origen, segmento y evaluación de calidad. Una fila por empresa; una oportunidad por empresa en esta demo.", {
        "id_cuenta": ("Texto · clave", "Identificador de la cuenta"),
        "canal": ("Texto", "Origen de captación"),
        "industria": ("Texto", "Sector de actividad"),
        "tipo_entrada": ("Texto", "Primera etapa: New o SQL"),
    }),
    "dim_etapas": ("Etapas", "Una fila por etapa del funnel.", {
        "id_etapa": ("Texto · clave", "Nombre de la etapa"),
        "orden": ("Entero", "Posición en el funnel"),
        "siguiente": ("Texto · relación", "Etapa siguiente; vacío para Won"),
    }),
    "fact_etapas": ("Registros de etapas", "Visitas de empresas a las etapas: fechas de entrada/salida y resultado. Sirve para medir conversión y permanencia; una empresa puede tener varias visitas.", {
        "id_registro": ("Texto · clave", "Identificador de esta entrada"),
        "id_cuenta": ("Texto · relación", "Cuenta que entró"),
        "id_etapa": ("Texto · relación", "Etapa a la que entró"),
        "entrada": ("Fecha", "Día de entrada a la etapa"),
        "salida": ("Fecha opcional", "Día de avance o pérdida; vacío si abierto o Won"),
        "estado": ("Texto", "avance, perdido, abierto o ganado"),
        "id_etapa_destino": ("Texto opcional · relación", "Siguiente etapa alcanzada; solo en avances"),
    }),
    "vw_ganados": ("Ganados", "Vista calculada: una fila por cuenta con primer Won en este conjunto, no prueba de primer pago.", {
        "id_cuenta": ("Texto · relación", "Cuenta ganada"),
        "canal": ("Texto", "Origen de captación"),
        "industria": ("Texto", "Sector de actividad"),
        "tipo_entrada": ("Texto", "Primera etapa: New o SQL"),
        "fecha_entrada_inicial": ("Fecha", "Primera entrada al funnel observada en el conjunto"),
        "fecha_won": ("Fecha", "Primer cierre Won observado"),
        "dias_hasta_won": ("Entero · días", "Días entre primera entrada y Won; incluye entrada directa por SQL"),
    }),
}


try:
    from scripts.cro_complete import install_metadata, generate_full, validate_full, complete_metrics, RULES
except ModuleNotFoundError:
    from cro_complete import install_metadata, generate_full, validate_full, complete_metrics, RULES
install_metadata(FIELDS, DICTIONARY)


def generate(scenario="referencia", seed=42, size=180, cutoff="2026-09-30", stage="Working"):
    if scenario not in SCENARIOS or stage not in STAGES[:-1] or size < 1:
        raise ValueError("Escenario/etapa inválidos o tamaño menor que uno")
    cut = date.fromisoformat(cutoff)
    accounts, records = [], []
    for month in range(1, 9):
        # Crecimiento controlado de demanda desde mayo; no es calibración real.
        n = size if month < 5 else int(size * 1.5)
        for person in range(n):
            account_id = f"C{month:02d}-{person:05d}"
            rng = random.Random(f"{seed}:{account_id}")
            draws = [(rng.random(), rng.randint(2, 8)) for _ in STAGES]
            channel = CHANNELS[rng.randrange(len(CHANNELS))]
            kind = "SQL" if rng.random() < .2 else "New"
            accounts.append(dict(id_cuenta=account_id, canal=channel,
                                 industria=rng.choice(["Comercio", "Servicios", "Manufactura"]),
                                 tipo_entrada=kind))
            entered = date(2026, month, rng.randint(1, 25))
            for index in range(STAGES.index(kind), len(STAGES)):
                if entered > cut:
                    break
                name = STAGES[index]
                target = STAGES[index + 1] if index + 1 < len(STAGES) else None
                chance, duration = draws[index]
                probability = [.94, .82, .85, .8, .78, .85, 1][index]
                changed = month >= 5 and name == stage
                if scenario == "conversion" and changed:
                    probability = max(.05, probability - .35)
                if scenario == "demora" and changed:
                    duration += 28
                passed = chance < probability
                exited = entered + timedelta(days=duration)
                if name == "Won":
                    state, observed_exit, destination = "ganado", None, None
                elif exited > cut:
                    state, observed_exit, destination = "abierto", None, None
                else:
                    state = "avance" if passed else "perdido"
                    observed_exit = exited.isoformat()
                    destination = target if passed else None
                records.append(dict(id_registro=f"{account_id}-{index}", id_cuenta=account_id,
                                    id_etapa=name, entrada=entered.isoformat(), salida=observed_exit,
                                    estado=state, id_etapa_destino=destination))
                if not passed or name == "Won" or exited > cut:
                    break
                entered = exited
    return accounts, records


def validate(accounts, records, cutoff):
    cut = date.fromisoformat(cutoff)
    ids = {a["id_cuenta"] for a in accounts}
    if len(ids) != len(accounts):
        raise ValueError("Cuenta duplicada")
    keys, pairs, by_account = set(), set(), {}
    for row in records:
        key = row["id_registro"]
        pair = row["id_cuenta"], row["id_etapa"]
        if key in keys or pair in pairs or row["id_cuenta"] not in ids or row["id_etapa"] not in STAGES:
            raise ValueError("Clave o relación inválida")
        keys.add(key)
        pairs.add(pair)
        entered = date.fromisoformat(row["entrada"])
        exited = date.fromisoformat(row["salida"]) if row["salida"] else None
        if entered > cut or (exited and (exited < entered or exited > cut)):
            raise ValueError("Fecha fuera del alcance")
        state, target = row["estado"], row["id_etapa_destino"]
        if state not in ("avance", "perdido", "abierto", "ganado"):
            raise ValueError("Estado inválido")
        if state == "avance":
            index = STAGES.index(row["id_etapa"])
            if not exited or index == len(STAGES)-1 or target != STAGES[index+1]:
                raise ValueError("Avance sin fecha/destino válido")
        elif target is not None or (state == "perdido" and not exited):
            raise ValueError("Resultado incoherente")
        if state in ("abierto", "ganado") and exited is not None:
            raise ValueError("Abierto/cierre terminal no debe tener salida")
        if (state == "ganado") != (row["id_etapa"] == "Won"):
            raise ValueError("Won incoherente")
        by_account.setdefault(row["id_cuenta"], []).append(row)
    for account in accounts:
        rows = sorted(by_account.get(account["id_cuenta"], []), key=lambda r: STAGES.index(r["id_etapa"]))
        if not rows or rows[0]["id_etapa"] != account["tipo_entrada"]:
            raise ValueError("Entrada inicial ausente")
        for current, following in zip(rows, rows[1:]):
            if (current["estado"] != "avance" or current["id_etapa_destino"] != following["id_etapa"]
                    or current["salida"] != following["entrada"]):
                raise ValueError("Continuidad entre etapas inválida")
        if rows[-1]["estado"] == "avance":
            raise ValueError("Avance sin entrada de destino")
    return {"cuentas_unicas": len(ids), "registros_unicos": len(keys),
            "fechas_y_relaciones": "correctas", "continuidad": "correcta"}


class Median:
    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(value)

    def finalize(self):
        return statistics.median(self.values) if self.values else None


class P90(Median):
    def finalize(self):
        # Percentil de rango más próximo: posición ceil(0.9*n).
        return sorted(self.values)[math.ceil(.9 * len(self.values))-1] if self.values else None


def database(accounts, records, interactions=(), payments=()):
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.create_aggregate("mediana", 1, Median)
    con.create_aggregate("p90", 1, P90)
    con.executescript((ROOT / "sql/cro/schema.sql").read_text())
    stages = [dict(id_etapa=s, orden=i+1, siguiente=STAGES[i+1] if i < 6 else None)
              for i, s in enumerate(STAGES)]
    # Insertar dimensiones sin FK autorreferida pendiente, luego actualizar siguiente.
    con.executemany("INSERT INTO dim_etapas(id_etapa,orden) VALUES (?,?)", [(s["id_etapa"], s["orden"]) for s in stages])
    con.executemany("UPDATE dim_etapas SET siguiente=? WHERE id_etapa=?", [(s["siguiente"], s["id_etapa"]) for s in stages])
    for table, rows in (("dim_cuentas", accounts), ("fact_etapas", records), ("interacciones", interactions), ("pagos", payments)):
        fields = FIELDS[table]
        con.executemany(f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})",
                        [[r.get(f) for f in fields] for r in rows])
    con.commit()
    return con


def analyze(con, cutoff, window, channel="", kind=""):
    if window < 1:
        raise ValueError("Ventana debe ser positiva")
    template = (ROOT / "sql/cro/metricas.sql").read_text()
    params = dict(corte=cutoff, ventana=window, canal=channel, tipo=kind)
    def query(group, condition, label):
        sql = template.replace("__GRUPO__", group).replace("__FILTRO_PERIODO__", condition)
        rows = [dict(r) for r in con.execute(sql, params)]
        for row in rows:
            row[label] = row.pop("grupo")
        return rows
    monthly = query("substr(entrada,1,7)", "", "mes")
    comparison = query("CASE WHEN entrada < '2026-05-01' THEN 'base' ELSE 'reciente' END",
                       "WHERE entrada >= '2026-01-01' AND entrada < '2026-09-01'", "periodo")
    for r in monthly:
        if r["avances"] + r["perdidos"] + r["sin_avance"] != r["elegibles"]:
            raise ValueError("No concilia la población elegible")
    joined = con.execute("SELECT COUNT(*) FROM fact_etapas JOIN dim_cuentas USING(id_cuenta) JOIN dim_etapas USING(id_etapa)").fetchone()[0]
    total = con.execute("SELECT COUNT(*) FROM fact_etapas").fetchone()[0]
    if joined != total or con.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("Join o claves inválidos")
    return dict(monthly=monthly, comparison=comparison)


def csv_file(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def model_html():
    """Tarjetas con columnas en filas, utilizables en HTML y Jupyter."""
    cards = []
    for table in ("dim_cuentas", "fact_etapas", "interacciones", "pagos", "dim_etapas"):
        title, grain, columns = DICTIONARY[table]
        fields = "".join(f"<tr><td><code>{escape(field)}</code></td><td>{escape(kind)}</td></tr>"
                         for field, (kind, _) in columns.items())
        cards.append(f'<article class="entity"><h3>{title}</h3><p><code>{table}</code></p><p>{grain}</p>'
                     f'<table><thead><tr><th>Columna</th><th>Tipo</th></tr></thead><tbody>{fields}</tbody></table></article>')
    return ('<div class="model">' + ''.join(cards) + '</div>'
            '<p>Cuatro tablas de negocio: prospectos/cuentas, visitas de etapas, interacciones y pagos. '
            'El catálogo de etapas es auxiliar. Cuenta → visitas y pagos: 1 a muchos. '
            'Visita → interacciones: 1 a muchos. Ganados y métricas son resultados calculados.</p>')



def preview_table(fields, rows):
    heads = "".join(f"<th>{escape(f)}</th>" for f in fields)
    body = "".join("<tr>" + "".join(f"<td>{escape(str(row[f])) if row[f] is not None else '—'}</td>" for f in fields) + "</tr>" for row in rows)
    return f'<div class="scroll"><table><thead><tr>{heads}</tr></thead><tbody>{body}</tbody></table></div>'


def tables_html(payload):
    config = payload["config"]
    blocks = []
    for scenario, item in payload["scenarios"].items():
        body = []
        for table in ("dim_cuentas", "fact_etapas", "interacciones", "pagos", "dim_etapas", "vw_ganados"):
            title, grain, columns = DICTIONARY[table]
            body.append(f'<h3>{title} · {item["tables"][table]["count"]:,} filas</h3><p>{grain} '
                        f'<a href="../../datos/sinteticos/cro/{scenario}/{CSV_NAMES.get(table, table)}.csv" download>Ver CSV completo</a></p>'
                        + preview_table(FIELDS[table], item["samples"][table]))
        body.append('<details><summary>Archivos de métricas (consulta opcional)</summary>' + ''.join(
            f'<p><a href="metricas/{scenario}/{name}.csv">{escape(name)}</a></p>'
            for name in item['metricas_completas']) + '</details>')
        body.append(f'<p><a href="../../datos/bases/cro/{scenario}/modelo.sqlite" download>Base de datos completa</a> · '
                    f'<a href="metricas/{scenario}/metricas_mensuales.csv" download>Métricas calculadas</a></p>')
        blocks.append(f'<details {"open" if scenario == "referencia" else ""}><summary>{item["label"]}</summary>{"".join(body)}</details>')
    dictionary = []
    for table, (title, grain, columns) in DICTIONARY.items():
        rows = [dict(columna=f, tipo=t, significado=d) for f, (t, d) in columns.items()]
        dictionary.append(f'<h3>{title}</h3>' + preview_table(["columna", "tipo", "significado"], rows))
    style = '''body{font:16px/1.5 system-ui,sans-serif;background:#f5f7fb;color:#1c3048;margin:0}
main{max-width:1260px;margin:auto;padding:32px}h1{margin:8px 0;font-size:32px}h2{margin-top:36px}
.note{background:#e9f0fa;padding:14px 18px;border-radius:10px}.model{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));align-items:start;gap:8px;margin:24px 0}
.entity,details{background:white;border:1px solid #d5deeb;border-radius:12px;padding:18px}.entity h3{margin:0;color:#245bae}
.entity p{font-size:13px;margin:8px 0}.entity td{font-size:12px;padding:7px 4px}.relation{align-self:center;text-align:center;font-size:12px;color:#245bae}
table{border-collapse:collapse;width:100%;white-space:nowrap}th,td{text-align:left;padding:10px;border-bottom:1px solid #e4eaf2;font-size:14px}th{background:#eef3fa}
.scroll{overflow-x:auto}details{margin:16px 0}summary{cursor:pointer;font-size:20px;font-weight:650}a{color:#245bae}code{font-size:.9em}
@media(max-width:1000px){.model{grid-template-columns:1fr}.relation{padding:8px}main{padding:18px}}
@media print{details{break-inside:avoid}.scroll{overflow:visible}main{padding:0}}'''
    return (f'<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>CRO · tablas de demostración</title><style>{style}</style><main>'
            '<h1>Modelo y tablas del CRO</h1><p class="note">Catálogo de consulta. El recorrido principal está en el notebook 02_modelo_cro.ipynb: tablas explicadas y una pregunta a la vez. Datos sintéticos.</p>'
            f'<p>Entradas: enero–agosto de 2026. Corte: {config["cutoff"]}. Semilla: {config["seed"]}. '
            f'Ventana de conversión ilustrativa: {config["window"]} días.</p>'
            '<nav><a href="#modelo">Modelo</a> · <a href="#tablas">Tablas</a> · <a href="#diccionario">Significado de columnas</a></nav>'
            '<h2 id="modelo">Tablas conectadas</h2>' + model_html()
            + '<p>Dimensiones: cuentas y etapas. Hechos: visitas, interacciones y pagos; no unirlos sin controlar duplicados.</p>'
            + '<h2 id="tablas">Muestras de tablas y catálogo completo de etapas</h2><p>El catálogo incluye la transición Proposal → Won.</p>' + "".join(blocks)
            + '<h2 id="diccionario">Significado de las columnas</h2>' + "".join(dictionary)
            + '<h2>Definiciones de la demo</h2><p>Calidad: perfil objetivo, necesidad e intención; evaluación v1. Plazo de primer intento: 2 días, supuesto ilustrativo. Incluye compras desde producto, entradas directas, saltos y reingresos. Won y pago se miden separados. No son reglas confirmadas de Finora.</p>'
            + '<p>Los vacíos son datos no aplicables o pendientes; no equivalen a cero. Una cuenta representa una oportunidad en esta demo.</p></main></html>')


def analysis_html(payload):
    """Gráficos descriptivos de resultados SQL ya calculados; sin recalcular tasas."""
    cfg = payload["config"]
    pairs = {}
    for scenario, item in payload["scenarios"].items():
        rows = {(r["etapa"], r["periodo"]): r for r in item["views"]["|"]["comparison"]}
        pairs[scenario] = [(s, rows.get((s, "base")), rows.get((s, "reciente"))) for s in STAGES[:-1]]
    times = [r["mediana_cerrados"] for stages in pairs.values() for _, a, b in stages
             for r in (a, b) if r and r["mediana_cerrados"] is not None]
    time_max = max(10, math.ceil(max(times, default=0) / 10) * 10)

    def chart(stages, metric, scale, unit):
        out = []
        for stage, before, after in stages:
            bars = []
            for period, row in (("base", before), ("reciente", after)):
                value = row[metric] if row else None
                text = f"{value:.1f}{unit}" if value is not None else "Sin datos"
                denominator = row["elegibles"] if row and metric == "conversion" else row["cerrados"] if row else 0
                width = 100 * value / scale if value is not None else 0
                bars.append(f'<div class="barrow"><span>{"Anterior" if period == "base" else "Reciente"}</span>'
                            f'<div class="track"><div class="bar {period}" style="width:{width:.3f}%"></div></div>'
                            f'<strong>{text}</strong></div><div class="n">{denominator} entradas '
                            f'{"comparables" if metric == "conversion" else "con salida registrada"}</div>')
            label = f"{stage} → {STAGES[STAGES.index(stage)+1]}" if metric == "conversion" else stage
            out.append(f'<div class="stage"><h3>{label}</h3>{"".join(bars)}</div>')
        return "".join(out)

    panels = []
    for scenario, stages in pairs.items():
        item = payload["scenarios"][scenario]
        target = next((p for p in stages if p[0] == cfg["stage"]), None)
        if target and target[1] and target[2]:
            _, before, after = target
            rate = lambda r: f'{r["conversion"]:.1f}%' if r["conversion"] is not None else "sin datos"
            duration = lambda r: f'{r["mediana_cerrados"]:.1f} días' if r["mediana_cerrados"] is not None else "sin datos"
            headline = (f'<p class="headline"><strong>{cfg["stage"]}:</strong> conversión {rate(before)} → {rate(after)}. '
                        f'Permanencia mediana {duration(before)} → {duration(after)}.</p>')
        else:
            headline = '<p class="headline">No hay datos comparables para la etapa seleccionada.</p>'
        panels.append(f'<section class="panel" id="panel-{scenario}"><h2>{item["label"]}</h2>{headline}'
                      f'<div class="charts"><article><h2>¿Cuántos avanzan?</h2><p>Conversión a la siguiente etapa en '
                      f'{cfg["window"]} días. Escala de 0 a 100%.</p>{chart(stages,"conversion",100,"%")}</article>'
                      f'<article><h2>¿Cuánto duran en la etapa?</h2><p>Mediana de entradas que ya salieron, por avance o pérdida. '
                      f'Escala de 0 a {time_max} días.</p>{chart(stages,"mediana_cerrados",time_max," d")}</article></div>'
                      '<p class="note">Los abiertos quedan fuera de la mediana de salidas. Una menor conversión en una ventana corta '
                      'puede reflejar demora; por sí sola no prueba peor calidad ni mala gestión.</p>'
                      f'<p><a href="../metricas/{scenario}/metricas_mensuales.csv">Métricas mensuales completas</a> · '
                      f'<a href="../tablas.html#tablas">Ver tablas y ganados</a></p></section>')
    choices = ''.join(f'<input class="choice" type="radio" name="scenario" id="{key}" '
                      f'{"checked" if key == "conversion" else ""}><label for="{key}">{item["label"]}</label>'
                      for key, item in payload["scenarios"].items())
    style = '''body{margin:0;background:#f4f7fc;color:#20334b;font:16px/1.45 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:28px}
h1{font-size:30px;margin:8px 0}h2{font-size:21px}h3{font-size:15px;margin:0 0 6px}.intro,.n{color:#53647b}.note{background:#eaf0fa;padding:14px;border-radius:10px}
.choice{margin:16px 5px 16px 12px}label{cursor:pointer}.panel{display:none}.choice#referencia:checked~.panels #panel-referencia,.choice#conversion:checked~.panels #panel-conversion,.choice#demora:checked~.panels #panel-demora{display:block}
.headline{font-size:18px;padding:16px;background:white;border-left:4px solid #285bad;border-radius:6px}.charts{display:grid;grid-template-columns:1fr 1fr;gap:24px}
article{background:white;border:1px solid #d8e1ec;border-radius:12px;padding:20px}.stage{margin:19px 0}.barrow{display:grid;grid-template-columns:66px 1fr 72px;align-items:center;gap:9px;font-size:13px}
.track{height:13px;background:#e9eef6;border-radius:4px}.bar{height:100%;border-radius:4px}.base{background:#8898af}.reciente{background:#285bad}.n{font-size:11px;margin:1px 0 6px 75px}a{color:#245bae}
@media(max-width:800px){.charts{grid-template-columns:1fr}main{padding:16px}.barrow{grid-template-columns:60px 1fr 65px}}'''
    return ('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>CRO · primer análisis</title><style>{style}</style><main><h1>Conversión y permanencia por etapa</h1>'
            '<p class="intro">Demostración con datos sintéticos. Anterior: enero–abril de 2026. Reciente: mayo–agosto de 2026. '
            f'Corte: {cfg["cutoff"]}. Se agrupa por fecha de entrada a cada etapa.</p>'
            '<p>Elige un escenario para ver qué cambia. Gris: anterior. Azul: reciente.</p>'
            + choices + '<div class="panels">' + ''.join(panels)
            + '</div><details><summary>Definiciones y límites</summary><p>Conversión = avances en la ventana / entradas con seguimiento suficiente. '
            'Los porcentajes se calculan sobre todos los registros elegibles del periodo, no promediando tasas mensuales. '
            'Entradas por New y SQL combinadas; la segmentación está pendiente de esta vista. '
            'Won cuenta cierres comerciales. Pagos y adquisición real siguen pendientes de datos. Calidad y atención no se han descartado.</p>'
            '<p>Permanencia de terminados no representa por sí sola a los abiertos. Los números describen estos escenarios, no causas históricas de Finora.</p></details></main></html>')


def build(output, seed=42, size=180, window=30, cutoff="2026-09-30", stage="Working"):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    data_dir = output / "datos/sinteticos/cro"
    db_dir = output / "datos/bases/cro"
    results_dir = output / "resultados/cro"
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "graficas").mkdir(exist_ok=True)
    payload = dict(config=dict(seed=seed, size=size, window=window, cutoff=cutoff, stage=stage, reglas=RULES),
                   stages=STAGES, channels=CHANNELS, scenarios={})
    for scenario, label in SCENARIOS.items():
        accounts, records, interactions, payments = generate_full(generate, scenario, seed, size, cutoff, stage)
        con = database(accounts, records, interactions, payments)
        controls = validate_full(con, cutoff)
        folder = data_dir / scenario
        folder.mkdir(parents=True, exist_ok=True)
        database_folder = db_dir / scenario
        database_folder.mkdir(parents=True, exist_ok=True)
        metrics_folder = results_dir / "metricas" / scenario
        metrics_folder.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(database_folder / "modelo.sqlite")) as saved:
            con.backup(saved)
        samples, tables = {}, {}
        for table, fields in FIELDS.items():
            rows = [dict(r) for r in con.execute(f"SELECT * FROM {table}")]
            csv_file(folder / f"{CSV_NAMES.get(table, table)}.csv", fields, rows)
            samples[table] = rows if table == "dim_etapas" else rows[:5]
            tables[table] = dict(fields=fields, count=len(rows))
        views = {}
        for channel, kind in itertools.product([""] + CHANNELS, ["", "New", "SQL", "Producto"]):
            views[f"{channel}|{kind}"] = analyze(con, cutoff, window, channel, kind)
        all_rows = views["|"]["monthly"]
        if sum(r["entradas"] for r in all_rows) != len({(r["id_cuenta"],r["id_etapa"]) for r in records}):
            raise ValueError("Resumen no concilia con detalle")
        csv_file(metrics_folder / "metricas_mensuales.csv", list(all_rows[0]), all_rows)
        complete = complete_metrics(con, cutoff)
        for name, rows in complete.items():
            if rows:
                csv_file(metrics_folder / f"{name}.csv", list(rows[0]), rows)
        for r in complete['etapas']:
            r['sin_avance_ventana'] = r['elegibles']-r['avances_siguiente']-r['saltos']-r['perdidos']
            r['perdida_pct'] = 100*r['perdidos']/r['elegibles'] if r['elegibles'] else None
            r['sin_avance_pct'] = 100*r['sin_avance_ventana']/r['elegibles'] if r['elegibles'] else None
            if r['sin_avance_ventana'] < 0:
                raise ValueError('Población de etapas no concilia')
        csv_file(metrics_folder / 'etapas.csv',list(complete['etapas'][0]),complete['etapas'])
        payload["scenarios"][scenario] = dict(label=label, views=views, tables=tables,
                                              samples=samples, controls=controls, metricas_completas=complete,
                                              wins_monthly=[dict(r) for r in con.execute(
                                                  "SELECT substr(fecha_won,1,7) AS mes_cierre, COUNT(*) AS cuentas_ganadas FROM vw_ganados GROUP BY mes_cierre ORDER BY mes_cierre")])
        won_records = sum(r["id_etapa"] == "Won" and r["estado"] == "ganado" for r in records)
        if tables["vw_ganados"]["count"] != won_records:
            raise ValueError("Ganados no concilia con eventos Won")
        con.close()
    (results_dir / "resultados.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {}
    for path in sorted([*data_dir.glob("*/*.csv"), *(results_dir / "metricas").glob("*/*.csv")]):
        manifest[str(path.relative_to(output))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (results_dir / "manifest.json").write_text(json.dumps(dict(config=payload["config"], hashes=manifest,
                                                         origen="Generador sintético local, versión 2; reglas en config"), indent=2), encoding="utf-8")
    (results_dir / "tablas.html").write_text(tables_html(payload), encoding="utf-8")
    # Las gráficas se definirán con el candidato. No generar ni actualizar aquí.
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(ROOT), help="Raíz donde crear datos/ y resultados/")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--size", type=int, default=180, help="Cuentas por mes base")
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--cutoff", default="2026-09-30")
    parser.add_argument("--stage", choices=STAGES[:-1], default="Working")
    args = parser.parse_args()
    build(args.output, args.seed, args.size, args.window, args.cutoff, args.stage)
    print(f"Tablas generadas: {Path(args.output) / 'resultados/cro/tablas.html'}")


if __name__ == "__main__":
    main()
