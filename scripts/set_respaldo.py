"""Genera la clave `respaldo` y ajusta evidencias/D-preguntas en cro/cfo.json.

Uso: python3 scripts/set_respaldo.py
Respaldo = 3 grupos (definiciones, fuentes, respuestas). Reutiliza textos
vigentes sin inventar cálculos; las fuentes JSON/documentos/Git conservan
el historial. No toca notebooks, CSV, métricas ni preguntas originales.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CRO_DEF = [
    {"termino": "Población", "definicion": "Cuentas que entraron por New; SQL directo y producto quedan fuera de New → Won."},
    {"termino": "Reloj común", "definicion": "30 días desde la primera entrada a New; cohortes por mes de entrada."},
    {"termino": "Mediana", "definicion": "Solo entre cuentas que llegaron a Won (32 días general, 30 histórica); no es conversión final."},
    {"termino": "Niveles", "definicion": "La conversión utiliza niveles alcanzados o superados con el mismo reloj desde New. La atención utiliza visitas reales, sin crear visitas para etapas saltadas."},
    {"termino": "Límites", "definicion": "Escenario sintético; coincidencia temporal no es causalidad; sin intervención ejecutada ni impacto medido."},
]

CFO_DEF = [
    {"termino": "Bruto y neto", "definicion": "MRR neto = bruto − descuentos."},
    {"termino": "Pago", "definicion": "Cobro con pendientes y cargos no recurrentes; no equivale al MRR."},
    {"termino": "Vigencias", "definicion": "Descuentos y tarifas con inicio y fin; el fin del descuento expande el neto sin nuevos servicios."},
    {"termino": "Horizonte", "definicion": "Enero 2025–marzo 2026; nueve meses de ingresos no son utilidad ni LTV."},
    {"termino": "Umbral", "definicion": "30 UM al mes durante 3 meses equilibra el resultado bajo misma ampliación y permanencia."},
    {"termino": "Lo que el dato actual no explica", "definicion": "Causas del cambio, estado contractual, ceros e inicio observado."},
]

CRO_EVIDENCIA = {
    "R-CRO1": [("e-plazo", "Plazo común de 30 días"), ("e-conversion", "Conversión a 30 días")],
    "R-CRO2": [("e-transiciones", "Transiciones priorizadas"), ("e-capacidad", "Carga y demora")],
    "R-CRO3": [("e-calidad", "Hipótesis de calidad"), ("e-capacidad", "Atención y carga")],
    "R-CRO4": [("cierre", "Cierre: acción y evaluación")],
}

CFO_EVIDENCIA = {
    "R-CFO1": [("f-modelo", "Modelo que separa causas")],
    "R-CFO2": [("f-modelo", "Modelo que separa causas")],
    "R-CFO3": [("f-modelo", "Modelo y ejemplos de clasificación")],
    "R-CFO4": [("f-politica", "MRR frente a la referencia"), ("f-recupero", "Recuperación acumulada")],
    "R-CFO-ejemplos": [("f-modelo", "Ejemplos de clasificación")],
}

CFO_D1 = "¿Qué puede y qué no puede explicar el modelo actual?"


def descargas_de(construccion):
    out = []
    for t in (construccion.get("sinteticos") or {}).get("tablas", []):
        if t.get("descarga"):
            out.append({
                "archivo": t["descarga"].split("/")[-1],
                "ruta": t["descarga"],
                "descripcion": t["necesidad"],
            })
    return out


def main() -> None:
    for caso, definiciones in (("cro", CRO_DEF), ("cfo", CFO_DEF)):
        p = RAIZ / f"src/content/{caso}.json"
        c = json.loads(p.read_text(encoding="utf-8"))
        if caso == "cfo":
            s09 = next((k for k in c["recorrido"]["capitulos"] if k["id"] == "S09"), None)
            amp = []
            if s09:
                amp = (s09["bloques"][0].get("lista") or [])
            definiciones = definiciones + [
                {"termino": "Ampliaciones posibles", "definicion": " ".join(amp) if amp else "Permanencia, LTV, adopción y rentabilidad."}
            ]
            for r in c.get("respuestas_reto", []):
                if r["id"] in CFO_EVIDENCIA:
                    r["evidencia"] = [{"ancla": a, "texto": t} for a, t in CFO_EVIDENCIA[r["id"]]]
            for q in c["ejecutiva"]["apertura"]["preguntas"]:
                if q.get("ref") == "S02":
                    q["texto"] = CFO_D1
                    q.pop("nota", None)
        else:
            for r in c.get("respuestas_reto", []):
                if r["id"] in CRO_EVIDENCIA:
                    r["evidencia"] = [{"ancla": a, "texto": t} for a, t in CRO_EVIDENCIA[r["id"]]]
        con = c.get("construccion", {})
        sintetico = (con.get("sinteticos") or {}).get("escenario", "Datos sintéticos de demostración.")
        derivadas = [t["archivo"] for t in (con.get("sinteticos") or {}).get("tablas", []) if t.get("origen") == "derivada"]
        c["respaldo"] = {
            "etiqueta": "Fuentes, método y respuestas al reto",
            "definiciones": {"titulo": "Definiciones y límites", "items": definiciones},
            "fuentes": {
                "titulo": "Fuentes y material de soporte",
                "recibidas": "Transactions.csv (importes mensuales por cliente), Industry.csv (cliente e industria) y S&M_spend.csv (gasto mensual por categoría). No se publican los originales.",
                "sinteticos": sintetico,
                "derivadas": ", ".join(derivadas) if derivadas else "ninguna listada",
                "descargas": descargas_de(con),
                "nota": "Descargas parciales para trazabilidad; no constituyen un paquete reproducible completo.",
            },
        }
        p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{caso}: respaldo listo ({len(definiciones)} definiciones, {len(c['respaldo']['fuentes']['descargas'])} descargas)")


if __name__ == "__main__":
    main()
