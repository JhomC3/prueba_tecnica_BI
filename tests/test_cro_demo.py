"""Controles independientes del primer modelo CRO."""
import unittest
import csv
import hashlib
import json
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from datetime import date
from scripts.cro_demo import generate, database, analyze, validate, build, FIELDS
from scripts.cro_complete import generate_full


def event(key, entered, exited=None, result="abierto", target=None):
    return dict(id_registro=key, id_cuenta=key, id_etapa="Working",
                entrada=entered, salida=exited, estado=result, id_etapa_destino=target)


class CroTests(unittest.TestCase):
    def test_proposal_won_and_derived_wins(self):
        accounts = [dict(id_cuenta=k, canal="Referidos", industria="Comercio", tipo_entrada="SQL") for k in ("A", "B", "C")]
        rows = [dict(id_registro="A1", id_cuenta="A", id_etapa="SQL", entrada="2026-01-01", salida="2026-01-10", estado="avance", id_etapa_destino="Demo"),
                dict(id_registro="A2", id_cuenta="A", id_etapa="Proposal", entrada="2026-01-20", salida="2026-01-25", estado="avance", id_etapa_destino="Won"),
                dict(id_registro="A3", id_cuenta="A", id_etapa="Won", entrada="2026-01-25", salida=None, estado="ganado", id_etapa_destino=None),
                dict(id_registro="B1", id_cuenta="B", id_etapa="Proposal", entrada="2026-01-20", salida="2026-01-26", estado="perdido", id_etapa_destino=None),
                dict(id_registro="C1", id_cuenta="C", id_etapa="Proposal", entrada="2026-02-25", salida=None, estado="abierto", id_etapa_destino=None)]
        with closing(database(accounts, rows)) as con:
            self.assertEqual(con.execute("SELECT siguiente FROM dim_etapas WHERE id_etapa='Proposal'").fetchone()[0], "Won")
            wins = [dict(r) for r in con.execute("SELECT * FROM vw_ganados")]
            self.assertEqual(len(wins), 1)
            self.assertEqual((wins[0]["id_cuenta"], wins[0]["fecha_won"], wins[0]["dias_hasta_won"]), ("A", "2026-01-25", 24))
            proposal = next(r for r in analyze(con, "2026-03-01", 30)["monthly"] if r["etapa"] == "Proposal" and r["mes"] == "2026-01")
            self.assertEqual((proposal["elegibles"], proposal["avances"], proposal["conversion"]), (2, 1, 50.0))

    def test_files_and_database_match_generated_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            payload = build(output, seed=17, size=6)
            for scenario in ("referencia", "conversion", "demora"):
                accounts, events, interactions, payments = generate_full(generate, scenario, seed=17, size=6)
                with closing(sqlite3.connect(output / "datos/bases/cro" / scenario / "modelo.sqlite")) as con:
                    self.assertEqual(con.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                    self.assertFalse(con.execute("PRAGMA foreign_key_check").fetchall())
                    with (output / "datos/sinteticos/cro" / scenario / "ganados.csv").open(newline="", encoding="utf-8") as f:
                        wins = list(csv.DictReader(f))
                    self.assertEqual({r["id_cuenta"] for r in wins}, {r["id_cuenta"] for r in events if r["estado"] == "ganado"})
                    self.assertEqual(len(wins), len({r["id_cuenta"] for r in wins}))
                    self.assertEqual(con.execute("SELECT COUNT(*) FROM vw_ganados").fetchone()[0], len(wins))
                    for table, expected in (("dim_cuentas", accounts), ("fact_etapas", events), ("interacciones", interactions), ("pagos", payments)):
                        with (output / "datos/sinteticos/cro" / scenario / f"{table}.csv").open(newline="", encoding="utf-8") as f:
                            reader = csv.DictReader(f)
                            self.assertEqual(reader.fieldnames, FIELDS[table])
                            rows = list(reader)
                        normalized = [{k: "" if v is None else str(v) for k, v in row.items()} for row in expected]
                        self.assertEqual(rows, normalized)
                        self.assertEqual(con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0], len(expected))
            manifest = json.loads((output / "resultados/cro/manifest.json").read_text())
            self.assertEqual(len(manifest["hashes"]), 57)
            for path, digest in manifest["hashes"].items():
                self.assertEqual(hashlib.sha256((output / path).read_bytes()).hexdigest(), digest)
            self.assertEqual(payload["config"]["seed"], 17)
            html = (output / "resultados/cro/tablas.html").read_text()
            self.assertIn("dim_cuentas", html)
            self.assertIn("fact_etapas", html)
            self.assertIn("id_etapa_destino", html)
            self.assertIn("Proposal → Won", html)
            self.assertEqual(len(payload["scenarios"]["referencia"]["samples"]["dim_etapas"]), 7)

    def test_window_and_open_cases(self):
        accounts = [dict(id_cuenta=str(i), canal="Referidos", industria="Comercio",
                         tipo_entrada="New") for i in range(1, 6)]
        events = [event("1", "2026-01-01", "2026-01-11", "avance", "Engaged"),
                  event("2", "2026-01-01", "2026-02-10", "avance", "Engaged"),
                  event("3", "2026-01-01", "2026-01-06", "perdido"),
                  event("4", "2026-01-01"), event("5", "2026-02-20")]
        con = database(accounts, events)
        rows = analyze(con, "2026-03-01", 30)["monthly"]
        jan = next(r for r in rows if r["mes"] == "2026-01")
        self.assertEqual((jan["entradas"], jan["elegibles"], jan["avances"],
                          jan["perdidos"], jan["sin_avance"]), (4, 4, 1, 1, 2))
        self.assertEqual(jan["conversion"], 25.0)
        self.assertEqual(jan["mediana_cerrados"], 10.0)  # durations 5,10,40
        self.assertEqual(jan["mediana_abiertos"], 59.0)
        feb = next(r for r in rows if r["mes"] == "2026-02")
        self.assertEqual(feb["elegibles"], 0)
        self.assertIsNone(feb["conversion"])
        # Exact cutoff/window boundary is eligible and inclusive.
        boundary = analyze(con, "2026-01-31", 30)["monthly"][0]
        self.assertEqual(boundary["elegibles"], 4)
        con.close()

    def test_reproducibility_censoring_and_join(self):
        a, e = generate("demora", seed=17, size=200)
        self.assertEqual((a, e), generate("demora", seed=17, size=200))
        validate(a, e, "2026-09-30")
        con = database(a, e)
        self.assertEqual(con.execute("SELECT COUNT(*) FROM fact_etapas f JOIN dim_cuentas c USING(id_cuenta) JOIN dim_etapas s USING(id_etapa)").fetchone()[0], len(e))
        self.assertFalse(con.execute("PRAGMA foreign_key_check").fetchall())
        self.assertTrue(all(x["entrada"] <= "2026-09-30" and
                            (not x["salida"] or x["salida"] <= "2026-09-30") for x in e))
        summary = analyze(con, "2026-09-30", 30)["monthly"]
        self.assertEqual(sum(r["entradas"] for r in summary), len(e))
        self.assertTrue(all(r["avances"] + r["perdidos"] + r["sin_avance"] == r["elegibles"] for r in summary))
        con.close()

    def test_scenarios_separate_conversion_and_time(self):
        results = {}
        for scenario in ("referencia", "conversion", "demora"):
            a, e = generate(scenario, seed=42, size=400)
            con = database(a, e)
            results[scenario] = analyze(con, "2026-09-30", 30)["comparison"]
            con.close()
        def recent(sc):
            return next(r for r in results[sc] if r["etapa"] == "Working" and r["periodo"] == "reciente")
        ref, drop, delay = map(recent, ("referencia", "conversion", "demora"))
        self.assertLess(drop["conversion"], ref["conversion"] - 20)
        self.assertGreater(delay["mediana_cerrados"], ref["mediana_cerrados"] + 15)
        self.assertLess(delay["conversion"], ref["conversion"])
        # Long follow-up demonstrates that delay is not a changed eventual probability.
        raw_ref = generate("referencia", seed=42, size=400, cutoff="2027-12-31")
        raw_delay = generate("demora", seed=42, size=400, cutoff="2027-12-31")
        for rows in zip(raw_ref[1], raw_delay[1]):
            self.assertEqual((rows[0]["id_cuenta"], rows[0]["id_etapa"], rows[0]["estado"]),
                             (rows[1]["id_cuenta"], rows[1]["id_etapa"], rows[1]["estado"]))

    def test_reject_duplicate_and_future(self):
        a, e = generate("referencia", size=2)
        with self.assertRaises(ValueError):
            validate(a + [a[0]], e, "2026-09-30")
        e[0]["entrada"] = "2030-01-01"
        with self.assertRaises(ValueError):
            validate(a, e, "2026-09-30")


if __name__ == "__main__":
    unittest.main()
