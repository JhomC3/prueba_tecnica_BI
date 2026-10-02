"""Añade bloques consultables `respuestas_reto` a cro.json y cfo.json.

Uso: python3 scripts/set_respuestas_reto.py
Preguntas literales del reto (docs/fuentes/reto-tecnico.md); respuestas
breves derivadas del recorrido con enlaces a secciones existentes.
No toca notebooks, CSV ni métricas.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CRO = [
    {
        "id": "R-CRO1",
        "pregunta": "¿Cómo definirías y medirías el funnel si no todos los clientes lo recorren igual (self-serve, entrada directa a SQL, estancamientos de semanas)?",
        "respuesta": "Recorrido acotado New → Won con cohortes por primera entrada a New y reloj común de 30 días; SQL directo y producto son rutas distintas que explican el crecimiento total fuera de New → Won. Saltos y reingresos se miden con el mismo reloj; self-serve y abiertos recientes requieren definiciones propias aún no fijadas.",
        "evidencia": [
            {"ancla": "C02", "texto": "C02: cohortes, reloj y conversión comparable"},
            {"ancla": "C04", "texto": "C04: niveles y transiciones"},
            {"ancla": "intro", "texto": "Introducción: rutas y datos simulados"},
        ],
    },
    {
        "id": "R-CRO2",
        "pregunta": "¿Dónde y en qué segmentos se concentra la pérdida de crecimiento? ¿Qué métricas propondrías que hoy no existen?",
        "respuesta": "La caída se concentra en Demo → Proposal (76,2% → 61,8%) y Proposal → Won (58,3% → 19,0%), en los tres canales sin excluir ninguno. Métricas calculadas: entradas, conversión por nivel y cohorte, carga y demora. Propuestas aún no medidas: contacto efectivo y motivos de pérdida.",
        "evidencia": [
            {"ancla": "C01", "texto": "C01: crecimiento de New"},
            {"ancla": "C04", "texto": "C04: focos priorizados con criterio"},
            {"ancla": "C05", "texto": "C05: carga y demora"},
        ],
    },
    {
        "id": "R-CRO3",
        "pregunta": "¿Qué hipótesis explicarían el fenómeno (demanda, calidad, velocidad de atención, conversión post-SQL) y qué datos usarías para validar o descartar cada una?",
        "respuesta": "Demanda comprobada (New +34,6% abril–mayo); calidad no atribuible (puntuación aleatoria 46,5 → 53,4); atención más lenta con más carga y mismo personal; conversión post-SQL caída en los focos. Para descartar calidad real harían falta scoring comparable, contacto efectivo y motivos de pérdida.",
        "evidencia": [
            {"ancla": "C01", "texto": "C01: demanda"},
            {"ancla": "C03", "texto": "C03: calidad aleatoria"},
            {"ancla": "C05", "texto": "C05: atención y carga"},
            {"ancla": "C04", "texto": "C04: conversión post-SQL"},
        ],
    },
    {
        "id": "R-CRO4",
        "pregunta": "¿Qué solución analítica construirías para que el CRO opere el funnel de forma recurrente, y qué decisiones le permitiría tomar?",
        "respuesta": "Procedimiento propuesto: actualizar cuentas, visitas, interacciones y capacidad cada mes; revisar carga, conversión y atención contra abril; responsable propuesto Sales; decisiones posibles: reforzar capacidad en focos. Cadencia específica por acordar; es procedimiento propuesto, no automatización implementada.",
        "evidencia": [
            {"ancla": "cierre", "texto": "Cierre: acción y evaluación"},
            {"ancla": "intro", "texto": "Introducción: tablas del modelo"},
        ],
    },
]

CFO = [
    {
        "id": "R-CFO1",
        "pregunta": "¿Qué puede y qué no puede responder el modelo actual (cliente + mes + monto pagado)?",
        "respuesta": "Mide pagos y variaciones; no explica causas ni confirma estado contractual, ceros o inicio observado. Desarrollo completo en S02.",
        "evidencia": [{"ancla": "S02", "texto": "S02: modelo actual"}],
    },
    {
        "id": "R-CFO2",
        "pregunta": "¿Cómo separarías el valor de la suscripción del precio efectivamente pagado? ¿Qué campos, tablas o definiciones agregarías?",
        "respuesta": "Nueve tablas con grano, claves y vigencias: bruto = cantidad × tarifa, neto = bruto − descuento, pago conciliado aparte; componentes_mes y movimientos son derivadas. Desarrollo completo en S03.",
        "evidencia": [{"ancla": "S03", "texto": "S03: evolución del modelo"}],
    },
    {
        "id": "R-CFO3",
        "pregunta": "¿Cómo clasificarías el inicio y el fin de un descuento para que no se confundan con contracción o expansión reales?",
        "respuesta": "Por capa con fechas de inicio y fin: inicio sin cambio de bruto no es contracción; fin sin cambio de bruto es expansión del neto, no de servicios; cambios simultáneos se analizan por separado; la prórroga conserva la fecha anterior.",
        "evidencia": [
            {"ancla": "S01", "texto": "S01: tres respuestas"},
            {"ancla": "S03", "texto": "S03: vigencias"},
        ],
    },
    {
        "id": "R-CFO4",
        "pregunta": "¿Por qué cambió nuestro MRR? ¿Cuánto corresponde al comportamiento del cliente y cuánto a pricing o descuentos?",
        "respuesta": "El puente concilia saldo inicial + movimientos = saldo final por capas (subyacente, pricing, descuento) sin doble conteo; el cobro no equivale al MRR. Soporte: puente SQL publicado.",
        "evidencia": [
            {"ancla": "S05", "texto": "S05: MRR al corte"},
            {"ancla": "S06", "texto": "S06: acumulado y recuperación"},
            {"ancla": "S07", "texto": "S07: explicación por fases"},
        ],
    },
    {
        "id": "R-CFO-ejemplos",
        "pregunta": "Tres ejemplos del CFO: pago 100 → 80; suscripción 100 → 130 con descuento 30 y neto 100; vencimiento del descuento.",
        "respuesta": "100 → 80 sin descuento es contracción; con bruto en 100 y descuento 20 es reducción comercial. 100 → 130 con descuento 30 deja el neto en 100 (más servicios o mayor tarifa). Al vencer, el neto sube a 130: expansión del neto por fin del descuento, sin servicios nuevos.",
        "evidencia": [{"ancla": "S01", "texto": "S01: respuestas literales"}],
    },
]

for caso, lista in (("cro", CRO), ("cfo", CFO)):
    p = RAIZ / f"src/content/{caso}.json"
    c = json.loads(p.read_text(encoding="utf-8"))
    c["respuestas_reto"] = lista
    p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{caso}: {len(lista)} respuestas al reto")
