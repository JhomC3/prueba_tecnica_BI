"""Sincroniza CRO con notebook 987c30a9 (53 celdas): celdas y conclusiones.

Uso: python3 scripts/sync_cro_final.py
Actualiza docs/web/cro-mapa.json y src/content/cro.json con las mismas
cadenas (conclusiones literales del notebook, celdas verificadas).
No toca notebooks, CSV ni métricas.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NB_SHA = "987c30a9ccc181c30143229c4d584c2a7fdffdac1ca92c8aa505c58d6c8f711d"

CELDAS = {
    "C01-total": (18, 0),
    "C01-canal": (23, 0),
    "C02-mediana": (29, 0),
    "C02-conv-total": (31, 0),
    "C02-conv-canal": (33, 0),
    "C03-global": (37, 0),
    "C03-canal": (37, 1),
    "C04-global": (40, 0),
    "C04-canales": (44, 0),
    "C04-canales-demo": (44, 2),
    "C05-carga": (46, 0),
    "C05-demora": (48, 0),
}

CONCLUSIONES = {
    "C01-total": "Se confirma un crecimiento de New entre abril y mayo: pasó de 133 a 179 entradas (+34,6%). Fue el mayor aumento mensual del periodo analizado. Entre mayo y agosto, las entradas oscilaron entre 173 y 183 por mes.",
    "C02-mediana": "La mediana de New a Won es 32 días en general (enero–agosto, 432 cuentas) y 30 días entre enero y abril (178 cuentas). Mantenemos ese plazo histórico de 30 para comparar abril y mayo: distingue la mediana previa de 30 de la general actual de 32 (que incluye la demora May+) y conserva 30/60/90 y meses maduros.",
    "C04-global": "De abril a mayo: • Demo → Proposal: 76,2% → 61,8%. • Proposal → Won: 58,3% → 19,0%. Por sus mayores caídas, priorizamos Demo → Proposal, Proposal → Won para investigar las causas.",
    "C04-canales": "Proposal → Won: De abril a mayo, la conversión cayó en los 3 canales, por lo que mantenemos todos para investigar la causa en esta transición.",
    "C04-canales-demo": "Demo → Proposal: De abril a mayo, la conversión cayó en los 3 canales, por lo que mantenemos todos para investigar la causa en esta transición.",
    "C05-carga": "De abril a mayo, la carga por persona aumentó un 55,7% en Demo y un 5,5% en Proposal. Después se mantuvo por encima de abril, con el mismo personal. Revisamos si aumentó la demora de atención.",
    "C05-demora": "De abril a mayo, la mediana hasta el primer intento de contacto aumentó de 3,0 a 4,0 días en Demo y de 2,0 a 4,0 días en Proposal. En junio, ambas mantuvieron esos tiempos. Después disminuyeron en ambas etapas.",
    "C06-sintesis": "El volumen aumentó sin ampliar el personal. La atención se hizo más lenta en Demo y Proposal y cayó la conversión de New a Won dentro de 30 días. Esto muestra menor avance en ese plazo, no pérdidas definitivas de clientes.",
}

CIERRE_SINTESIS = "El volumen aumentó sin ampliar el personal. La atención se hizo más lenta en Demo y Proposal y cayó la conversión de New a Won dentro de 30 días. Esto muestra menor avance en ese plazo, no pérdidas definitivas de clientes."

CIERRE_ACCIONES = "Se proponen dos refuerzos de capacidad (Demo y Proposal) con responsable Sales propuesto y evaluación en octubre–noviembre de 2026."

CIERRE_EVAL_COMUN = "octubre–noviembre de 2026 (corte 2026-12-31, 30 días desde New): ¿bajan demora y carga y sube conversión? mediana primer intento Demo ≤ 3,0 días y Proposal ≤ 2,0 días; carga Demo < 12,3 y Proposal < 9,6 con volumen similar a mayo; conversión Demo→Proposal ≥ 76,2%, Proposal→Won ≥ 58,3% y New→Won ≥ 21,1% (referencia abril)."


def main() -> None:
    mapa_p = RAIZ / "docs/web/cro-mapa.json"
    mapa = json.loads(mapa_p.read_text(encoding="utf-8"))
    mapa["snapshot"]["notebook_sha256"] = NB_SHA
    mapa["snapshot"]["celdas"] = 53
    mapa["snapshot"]["fecha_revision"] = "2026-10-02"
    mapa["snapshot"]["estado"] = "notebook final; cifras y conclusiones verificadas contra resultados/cro"
    for cap in mapa["capitulos"]:
        for b in cap["bloques"]:
            if b["id"] in CELDAS:
                cell, out = CELDAS[b["id"]]
                b["figura"]["cell"] = cell
                b["figura"]["output"] = out
            if b["id"] in CONCLUSIONES:
                b["conclusion"] = CONCLUSIONES[b["id"]]
            if b["id"] == "C07-acciones":
                b["conclusion"] = CIERRE_ACCIONES
                b["tabla"]["columnas"] = [
                    {"campo": "hallazgo", "etiqueta": "Hallazgo"},
                    {"campo": "accion", "etiqueta": "Acción propuesta"},
                    {"campo": "responsable", "etiqueta": "Responsable"},
                ]
                b["tabla"]["caption"] = "Hallazgos, acciones propuestas y responsables"
                for f in b["tabla"]["filas"]:
                    f.pop("evaluacion", None)
                b["evaluacion_comun"] = CIERRE_EVAL_COMUN
    mapa_p.write_text(json.dumps(mapa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cont_p = RAIZ / "src/content/cro.json"
    cont = json.loads(cont_p.read_text(encoding="utf-8"))
    for cap in cont["recorrido"]["capitulos"]:
        for b in cap["bloques"]:
            if b["id"] in CONCLUSIONES:
                b["conclusion"] = CONCLUSIONES[b["id"]]
    for cap in mapa["capitulos"]:
        if cap["id"] == "C06":
            for b in cap["bloques"]:
                if b["id"] == "C06-sintesis":
                    for ccap in cont["recorrido"]["capitulos"]:
                        if ccap["id"] == "C06":
                            for cb in ccap["bloques"]:
                                if cb["id"] == "C06-sintesis":
                                    cb["conclusion"] = b["conclusion"]
    cont["recorrido"]["cierre"]["sintesis"] = CIERRE_SINTESIS
    cont["recorrido"]["cierre"]["acciones"]["conclusion"] = CIERRE_ACCIONES
    cont["recorrido"]["cierre"]["acciones"]["evaluacion_comun"] = CIERRE_EVAL_COMUN
    cont["recorrido"]["cierre"]["acciones"]["tabla"]["columnas"] = [
        {"campo": "hallazgo", "etiqueta": "Hallazgo"},
        {"campo": "accion", "etiqueta": "Acción propuesta"},
        {"campo": "responsable", "etiqueta": "Responsable"},
    ]
    cont["recorrido"]["cierre"]["acciones"]["tabla"]["caption"] = "Hallazgos, acciones propuestas y responsables"
    for f in cont["recorrido"]["cierre"]["acciones"]["tabla"]["filas"]:
        f.pop("evaluacion", None)
    cont_p.write_text(json.dumps(cont, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("mapa + contenido CRO actualizados:", NB_SHA[:12])


if __name__ == "__main__":
    main()
