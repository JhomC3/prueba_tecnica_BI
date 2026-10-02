"""Genera la capa ejecutiva `ejecutiva` en cro.json y cfo.json.

Uso: python3 scripts/set_ejecutiva.py
Esquema común AJUSTE-NARRATIVA (apertura A–F + escenas con preguntas).
Editorial autorizado con referencia al original; preguntas oficiales del
reto NO figuran como priorizadas. No toca notebooks, CSV, métricas,
conclusiones analíticas ni preguntas originales.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RETO_PATH = RAIZ / "docs" / "fuentes" / "reto-tecnico.md"
if not RETO_PATH.exists():
    raise SystemExit(f"falta {RETO_PATH}: el enunciado es privado y no se incluye en la copia pública")
RETO = RETO_PATH.read_text(encoding="utf-8")

CRO = {
    "apertura": {
        "cita_titular": "Estamos generando más leads, pero no estamos vendiendo más",
        "pregunta_editorial": "¿Realmente aumentó New y, si aumentó, disminuyó la conversión de New a Won en un mismo plazo?",
        "pregunta_ref": "recorrido.pregunta_principal",
        "sintesis_preocupacion": "El volumen crece en New, pero no se convierte en clientes nuevos; hay varias explicaciones posibles y ninguna medición que las separe.",
        "datos_intro": "Para responder, contamos con:",
        "datos": [
            "Importes mensuales por cliente.",
            "Clientes e industria.",
            "Gastos mensuales de Sales y Marketing.",
        ],
        "insuficiencia": "Estos datos no permiten reconstruir las etapas del funnel ni sus tiempos de atención.",
        "preguntas_rotulo": "Preguntas que priorizamos para el análisis",
        "preguntas": [
            {"texto": "¿Realmente aumentó New?", "ref": "C01"},
            {"texto": "¿Qué plazo usamos para comparar New y Won?", "ref": "C02-mediana"},
            {"texto": "¿Disminuyó la conversión de New a Won en ese plazo?", "ref": "C02-conv-total"},
            {"texto": "¿Cambió la calidad de los leads o su calificación?", "ref": "C03"},
            {"texto": "¿En qué transiciones cambió la conversión?", "ref": "C04"},
            {"texto": "¿Cambió la capacidad o la rapidez de atención?", "ref": "C05"},
        ],
        "necesidad_intro": "Para responder estas preguntas necesitamos:",
        "necesidad": "Entradas y cambios de etapa con fechas, canal, puntuación y calificación de leads, capacidad e intentos de atención.",
        "sinteticos_frase": "Para este ejercicio generamos datos sintéticos con esta información.",
        "puente": "Comenzamos por verificar el aumento de New.",
    },
    "escenas": [
        {
            "id": "e-new",
            "titulo": "¿Realmente aumentó New?",
            "transicion": "Entradas a New por mes, enero–agosto de 2026.",
            "bloques": ["C01-total"],
            "detalle": {"titulo": "Desglose por canal", "bloques": ["C01-canal"]},
            "limite": "",
            "puente": "Antes de comparar la conversión, definimos un plazo común de seguimiento.",
        },
        {
            "id": "e-plazo",
            "titulo": "¿Qué plazo usamos para comparar New y Won?",
            "bloques": ["C02-mediana"],
            "sintesis": "32 días entre los ganados de enero–agosto; 30 entre los de enero–abril. Conservamos 30 para comparar abril y mayo con el mismo plazo.",
            "limite": "Mediana solo entre cuentas que llegaron a Won: 32 días general (432) y 30 días histórica (178). No representa a todos los New ni es conversión final.",
            "puente": "Con 30 días como plazo común, comparamos qué porcentaje llegó a Won.",
        },
        {
            "id": "e-conversion",
            "titulo": "¿Qué porcentaje de New llegó a Won en 30 días?",
            "transicion": "Cohortes de abril y mayo, mismo reloj desde New.",
            "bloques": ["C02-conv-total", "C02-conv-canal"],
            "limite": "Menor avance dentro del plazo; no es pérdida definitiva de clientes.",
            "puente": "Antes de localizar etapas, revisamos si cambió la calidad.",
        },
        {
            "id": "e-calidad",
            "titulo": "¿Cambió la calidad de los leads o su calificación?",
            "transicion": "Puntuación sintética de 0 a 100.",
            "bloques": ["C03-global"],
            "detalle": {"titulo": "Por canal", "bloques": ["C03-canal"]},
            "limite": "Puntuación sintética: no demuestra ni descarta la calidad real.",
            "puente": "Sin explicación por calidad con estos datos, localizamos en qué transiciones cambió la conversión.",
        },
        {
            "id": "e-transiciones",
            "titulo": "¿En qué transiciones cambió la conversión?",
            "transicion": "Niveles del funnel a 30 días desde New.",
            "bloques": ["C04-global"],
            "detalle": {"titulo": "Por canal", "bloques": ["C04-canales", "C04-canales-demo"]},
            "limite": "Se priorizan por sus mayores caídas.",
            "puente": "Localizadas las caídas, revisamos capacidad y atención en esos focos.",
        },
        {
            "id": "e-capacidad",
            "titulo": "¿Cambió la capacidad o la rapidez de atención?",
            "transicion": "Focos Demo y Proposal.",
            "bloques": ["C05-carga", "C05-demora"],
            "limite": "La carga usa mes de servicio; la demora usa cohortes New y solo cuentas con intento. Señales compatibles con presión de capacidad, no prueba de causalidad.",
            "puente": "Con la evidencia localizada, cerramos con propuesta y seguimiento.",
        },
    ],
}

CFO = {
    "apertura": {
        "cita_titular": "¿Por qué cambió nuestro MRR?",
        "pregunta_despues": "¿La política de descuentos mejora o deteriora el ingreso recurrente neto y el valor económico de los clientes durante el horizonte evaluado?",
        "sintesis_preocupacion": "Los pagos cambian, pero el dato no dice si es por servicios, tarifas o descuentos.",
        "datos_intro": "Para responder, contamos con:",
        "datos": [
            "Importes mensuales por cliente.",
            "Clientes e industria.",
            "Gastos mensuales de Sales y Marketing.",
        ],
        "insuficiencia": "Estos datos muestran lo pagado, pero no separan suscripción, descuentos y causas del cambio.",
        "preguntas_rotulo": "Preguntas que priorizamos para el análisis",
        "preguntas": [
            {"texto": "¿Qué puede explicar el modelo actual?", "ref": "S02", "nota": "El original también pregunta qué no puede responder."},
            {"texto": "¿Cómo separar suscripción, precio, descuento y pago?", "ref": "S03"},
            {"texto": "¿Cómo cambia el MRR frente a la referencia?", "ref": "S05"},
            {"texto": "¿Cuánto ingreso dejamos de capturar por la política?", "ref": "S06"},
            {"texto": "¿Qué explica la diferencia?", "ref": "S07"},
        ],
        "necesidad_intro": "Para responder estas preguntas necesitamos:",
        "necesidad": "Historia de suscripciones, servicios y cantidades, tarifas, descuentos y vigencias, estados y pagos.",
        "sinteticos_frase": "Para este ejercicio generamos datos sintéticos con esta información.",
        "puente": "Comenzamos por separar qué observamos de qué podemos explicar.",

    },
    "escenas": [
        {
            "id": "f-modelo",
            "titulo": "¿Cómo se calcula el MRR neto?",
            "transicion": "Nueve tablas con vigencias; el detalle queda plegado.",
            "bloques": ["S03-modelo"],
            "detalle": {"titulo": "Ejemplos de clasificación", "bloques": ["S01-r1", "S01-r2", "S01-r3"]},
            "limite": "Valor de suscripción − descuento = MRR neto; el pago puede diferir por pendientes y cargos no recurrentes.",
            "puente": "Con el modelo que separa causas, lo probamos con una política concreta.",
        },
        {
            "id": "f-politica",
            "titulo": "¿Cómo cambia el MRR frente a la referencia?",
            "transicion": "Escenario principal con referencia pareada.",
            "bloques": ["S04-diseno", "S05-mrr"],
            "limite": "Unidades monetarias sintéticas, no COP observado; la ampliación no es igual entre alternativas.",
            "puente": "El cierre mejora; comprobamos si compensa los descuentos.",
        },
        {
            "id": "f-recupero",
            "titulo": "¿Compensa la ampliación los descuentos?",
            "transicion": "Acumulado julio 2025–marzo 2026.",
            "bloques": ["S06-recuperacion"],
            "detalle": {"titulo": "Comparativa y fases", "bloques": ["S06-comparativa", "S07-fases"]},
            "limite": "Son ingresos, no utilidad ni LTV completo.",
            "puente": "Sin recuperación en nueve meses; cerramos con ajuste y validación.",
        },
    ],
    "cierre": {
        "decision": "Ajustar el monto o la duración del descuento.",
        "responsable": "Finanzas y Comercial.",
        "exito": "Más ingreso acumulado sin superar el límite de bajas acordado antes de la prueba.",
        "supuestos": "El umbral de 30 UM depende de los supuestos del escenario: misma ampliación y permanencia.",
    },
}

for caso, dato in (("cro", CRO), ("cfo", CFO)):
    p = RAIZ / f"src/content/{caso}.json"
    c = json.loads(p.read_text(encoding="utf-8"))
    a = dato["apertura"]
    assert a["cita_titular"] in RETO, f"titular no literal {caso}"
    if caso == "cro":
        assert a["pregunta_editorial"]
        assert c["recorrido"]["pregunta_principal"] != a["pregunta_editorial"]
    else:
        assert a["pregunta_despues"] == c["recorrido"]["pregunta_principal"]
    a["cita_completa"] = c["requerimiento_original"]["texto"]
    ids = {b["id"] for cap in c["recorrido"]["capitulos"] for b in cap["bloques"]}
    for e in dato["escenas"]:
        for b in e["bloques"]:
            assert b in ids, f"bloque inexistente {b}"
        for b in (e.get("detalle") or {}).get("bloques", []):
            assert b in ids, f"detalle inexistente {b}"
    c["ejecutiva"] = dato
    p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{caso}: ejecutiva lista ({len(dato['escenas'])} escenas)")
