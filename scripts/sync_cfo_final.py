"""Sincroniza CFO con notebook 298dbb74 (23 celdas): celdas y conclusiones.

Uso: python3 scripts/sync_cfo_final.py
Actualiza docs/web/cfo-mapa.json y src/content/cfo.json con las mismas
cadenas (conclusiones literales del notebook, celdas verificadas).
La estructura S01–S09 + cierre se conserva; 3.3 vive en la conclusión
de 3.2 (celda 17). No toca notebooks, CSV ni métricas.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NB_SHA = "298dbb74c6bb5f9eb7b1fa780ab428c8a8d17af3b38cadd8967697677fa5f315"

CELDAS = {
    "S01-r1": "3, 4", "S01-r2": "3, 4", "S01-r3": "3, 4",
    "S02-modelo": "2",
    "S03-modelo": "5–11",
    "S04-diseno": "12",
    "S05-mrr": "14",
    "S06-comparativa": "16", "S06-recuperacion": "16, 17",
    "S07-fases": "17",
    "S09-vision": "21",
}

S06_REC = ("El ingreso por ampliación suma 4.500 UM y los descuentos aplicados suman 6.000 UM. "
    "La diferencia de ingreso neto acumulado frente a no aplicar la política es -1.500 UM. "
    "Al finalizar marzo, todavía no se compensan los descuentos. "
    "El mayor MRR final no basta para concluir que la política compensa el descuento. "
    "Durante el descuento, los 50 clientes generan 4.500 UM menos que sin política; después, 3.000 UM más. "
    "El resultado cubre nueve meses; evaluar el valor del cliente durante toda su relación (LTV) requiere "
    "comparar permanencia e ingresos con y sin política.")

S07_FASES = ("Durante el descuento, los 50 clientes generan 4.500 UM menos que sin política; "
    "después, 3.000 UM más.")

ACCIONES = ("Decisión propuesta: ajustar monto o duración. 30 unidades monetarias al mes durante 3 meses "
    "equilibra el resultado; un monto menor lo supera. La tabla también compara acortar un mes el descuento. "
    "Esto supone la misma ampliación y permanencia. Acción: Finanzas y Comercial deben probar la oferta "
    "ajustada y comprobar su aceptación.")

EVALUACION = ("Evaluación propuesta: probar la oferta ajustada con dos grupos de clientes similares: uno con "
    "política y otro sin ella, asignados al azar si es posible. Seguir ambos grupos cada mes durante 9 meses: "
    "3 con descuento y 6 después del vencimiento. Comparar ingreso neto acumulado por cliente y bajas. "
    "La política funciona si genera más ingreso acumulado sin superar el límite de bajas acordado antes de la prueba.")


def retocar_mapa(mapa: dict) -> None:
    mapa["snapshot"]["notebook_sha256"] = NB_SHA
    mapa["snapshot"]["celdas"] = 23
    mapa["snapshot"]["fecha_revision"] = "2026-10-02"
    mapa["snapshot"]["estado"] = "notebook final; cifras y conclusiones verificadas contra resultados/cfo"
    for sec in mapa["secciones"]:
        for b in sec["bloques"]:
            if b["id"] in CELDAS:
                b["referencias"]["celdas"] = CELDAS[b["id"]]
            fig = b.get("figura")
            if fig and b["id"] == "S05-mrr":
                fig["cell"] = 14
            if fig and b["id"] == "S06-recuperacion":
                fig["cell"] = 17
            if b["id"] == "S06-recuperacion":
                b["conclusion"] = S06_REC
            if b["id"] == "S07-fases":
                b["conclusion"] = S07_FASES
    mapa["cierre"]["acciones"]["conclusion"] = ACCIONES
    mapa["cierre"]["evaluacion"] = EVALUACION


def main() -> None:
    mapa_p = RAIZ / "docs/web/cfo-mapa.json"
    mapa = json.loads(mapa_p.read_text(encoding="utf-8"))
    retocar_mapa(mapa)
    mapa_p.write_text(json.dumps(mapa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cont_p = RAIZ / "src/content/cfo.json"
    cont = json.loads(cont_p.read_text(encoding="utf-8"))
    for cap in cont["recorrido"]["capitulos"]:
        for b in cap["bloques"]:
            if b["id"] == "S06-recuperacion":
                b["conclusion"] = S06_REC
            if b["id"] == "S07-fases":
                b["conclusion"] = S07_FASES
            if b["id"] == "S09-vision":
                b["datos"] = "Notebook 21."
    cont["recorrido"]["cierre"]["acciones"]["conclusion"] = ACCIONES
    cont["recorrido"]["cierre"]["evaluacion"] = EVALUACION
    cont_p.write_text(json.dumps(cont, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("mapa + contenido CFO actualizados:", NB_SHA[:12])


if __name__ == "__main__":
    main()
