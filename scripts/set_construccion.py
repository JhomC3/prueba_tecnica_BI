"""Añade el bloque `construccion` a cro.json y cfo.json (una sola edición).

Uso: python3 scripts/set_construccion.py
Lee los JSON de src/content, inserta `construccion` y reescribe.
No toca notebooks, CSV ni métricas.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def originales_cro():
    return [
        {
            "nombre": "Transactions.csv",
            "estado": "recibido",
            "descripcion": "Importes mensuales por cliente: columnas ID, month y amount.",
            "aporta": "Describir importes observados por mes y, tras validar el vínculo entre IDs, por industria.",
            "limite": "Los pagos no equivalen a eventos Won ni traen fechas del funnel; falta el vínculo comprobado con el CRM y la definición de nuevo pagador.",
            "descarga": None,
        },
        {
            "nombre": "Industry.csv",
            "estado": "recibido",
            "descripcion": "Cliente e industria: columnas ID e Industria.",
            "aporta": "Segmentar cuentas por industria una vez validada la correspondencia de IDs con Transactions.",
            "limite": "Faltan ruta, canal y calificación; no explica el avance por etapa.",
            "descarga": None,
        },
        {
            "nombre": "S&M_spend.csv",
            "estado": "recibido",
            "descripcion": "Gasto mensual de Sales & Marketing por categoría: columna Month más siete categorías, 34 meses (2022-01 a 2024-10).",
            "aporta": "Contexto agregado del gasto comercial por mes.",
            "limite": "Moneda y escala sin confirmar; sin atribución por equipo, canal o cliente; varias categorías necesitan definición antes de asignarles función comercial.",
            "descarga": None,
        },
    ]


def originales_cfo():
    return [
        {
            "nombre": "Transactions.csv",
            "estado": "recibido",
            "descripcion": "Importes mensuales por cliente: columnas ID, month y amount.",
            "aporta": "Monto pagado por cliente y total, variación entre meses y continuidad o interrupciones de pago.",
            "limite": "No identifica la causa del cambio ni contratos, descuentos, estados o vigencias; un pago ausente o cero puede ser un atraso.",
            "descarga": None,
        },
        {
            "nombre": "Industry.csv",
            "estado": "recibido",
            "descripcion": "Cliente e industria: columnas ID e Industria.",
            "aporta": "Añade la industria del cliente a cada registro de pago.",
            "limite": "No explica el cambio de la suscripción; la correspondencia de IDs con Transactions está por validar.",
            "descarga": None,
        },
        {
            "nombre": "S&M_spend.csv",
            "estado": "recibido",
            "descripcion": "Gasto mensual de Sales & Marketing por categoría: columna Month más siete categorías, 34 meses (2022-01 a 2024-10).",
            "aporta": "Contexto agregado del gasto comercial por mes.",
            "limite": "Moneda y escala sin confirmar; sin atribución por equipo, canal o cliente; no mide descuentos aplicados.",
            "descarga": None,
        },
    ]


CRO = {
    "pregunta": "¿La tasa de conversión de New a Won aumentó o disminuyó después del aumento de New?",
    "proposito": "Comprobar cuánto creció New, seguir las mismas entradas hasta Won, localizar dónde cambió el avance y proponer acciones con seguimiento.",
    "resumen": "Los archivos recibidos no traen funnel ni fechas: la demostración usa datos sintéticos del escenario referencia y el recorrido sigue New hasta Won.",
    "originales": originales_cro(),
    "nota_originales": "Archivos recibidos al inicio; se describen sin descarga en la web. Ninguno alimenta los cálculos de la demostración: esta usa datos sintéticos independientes.",
    "faltante": [
        {"tema": "Cuentas y origen de entrada", "detalle": "Identidad y eventos de entrada y salida por etapa, incluido Won; canal y tipo de entrada por cuenta."},
        {"tema": "Historial de etapas con fechas", "detalle": "Entradas y salidas por etapa para medir avance, demoras y reingresos con un reloj común."},
        {"tema": "Intentos de atención y contacto", "detalle": "Interacciones con tipo, fecha y resultado para explicar atención y avance."},
        {"tema": "Capacidad disponible", "detalle": "Personal y capacidad mensual por etapa para contrastar carga y demora."},
        {"tema": "Definiciones y evaluación de calidad", "detalle": "Criterios de calificación, motivos de pérdida y descalificación aplicados por cuenta."},
        {"tema": "Pagos vinculados", "detalle": "Vínculo comprobado entre los pagos y las mismas cuentas del funnel, con definición de nuevo pagador."},
    ],
    "sinteticos": {
        "etiqueta": "Datos sintéticos de demostración",
        "escenario": "Escenario referencia del notebook CRO vigente.",
        "nota": "Tablas independientes de los archivos recibidos; cubren las necesidades listadas arriba. Las tablas extensas se describen sin descarga.",
        "tablas": [
            {"archivo": "dim_cuentas.csv", "necesidad": "Cuentas y origen: canal, tipo de entrada, industria y calificación.", "descarga": None, "origen": "fuente"},
            {"archivo": "dim_etapas.csv", "necesidad": "Catálogo de etapas del funnel.", "descarga": "data/archivos/cro/dim_etapas.csv", "origen": "fuente"},
            {"archivo": "fact_etapas.csv", "necesidad": "Historial de pasos por etapa con fechas, estados y motivos de pérdida.", "descarga": None, "origen": "fuente"},
            {"archivo": "interacciones.csv", "necesidad": "Intentos de atención: tipo, fecha y resultado.", "descarga": None, "origen": "fuente"},
            {"archivo": "dim_capacidad.csv", "necesidad": "Capacidad mensual disponible por etapa.", "descarga": "data/archivos/cro/dim_capacidad.csv", "origen": "fuente"},
            {"archivo": "puntuaciones_leads.csv", "necesidad": "Evaluación de calidad por cuenta.", "descarga": "data/archivos/cro/puntuaciones_leads.csv", "origen": "fuente"},
            {"archivo": "pagos.csv", "necesidad": "Pagos vinculados a las cuentas del funnel.", "descarga": None, "origen": "fuente"},
            {"archivo": "ganados.csv", "necesidad": "Cierres Won con fecha de entrada y de cierre.", "descarga": None, "origen": "derivada", "derivacion": "Vista calculada vw_ganados desde fact_etapas y dim_cuentas; no prueba de primer pago."},
        ],
    },
    "puente": "Con estos datos se construyó la demostración. A partir de aquí continúa el recorrido existente: crecimiento de New, conversión comparable, calidad, niveles, capacidad y acciones.",
}

CFO = {
    "pregunta": "¿La política de descuentos mejora o deteriora el ingreso recurrente neto y el valor económico de los clientes durante el horizonte evaluado?",
    "proposito": "Evaluar ingreso recurrente neto y valor del cliente para mantener, ajustar o comprobar condiciones de descuento.",
    "resumen": "Cliente + mes + monto no separa causas: la demostración usa datos sintéticos del escenario principal, con frente a sin política, y el recorrido analiza MRR y recuperación.",
    "originales": originales_cfo(),
    "nota_originales": "Archivos recibidos al inicio; se describen sin descarga en la web. Ninguno alimenta los cálculos de la demostración: esta usa datos sintéticos independientes. El desarrollo completo del modelo actual está en las secciones S02 y S03 del recorrido.",
    "enlaces_recorrido": [
        {"ancla": "S02", "texto": "Ver en S02 qué puede y qué no puede responder el modelo actual"},
        {"ancla": "S03", "texto": "Ver en S03 las nueve tablas del modelo propuesto"},
    ],
    "faltante": [
        {"tema": "Suscripciones y componentes", "detalle": "Contratos por cliente y servicios o partidas por suscripción."},
        {"tema": "Cantidades o uso", "detalle": "Cantidad por componente y mes para valorar el bruto."},
        {"tema": "Tarifas con vigencias", "detalle": "Precio por componente con inicio y fin de vigencia."},
        {"tema": "Descuentos con inicio y fin", "detalle": "Monto, porcentaje equivalente, vigencia, duración y objetivo comercial."},
        {"tema": "Estados contractuales", "detalle": "Estado por suscripción y mes (activo, baja, inactivo)."},
        {"tema": "Pagos y conciliación", "detalle": "Cobro vinculado al neto, con pendientes y cargos no recurrentes identificables."},
    ],
    "sinteticos": {
        "etiqueta": "Datos sintéticos de demostración",
        "escenario": "Escenario principal del notebook CFO vigente, con dos alternativas pareadas: con_descuento y sin_descuento.",
        "nota": "Tablas independientes de los archivos recibidos; cubren las necesidades listadas arriba. No se suman alternativas ni sensibilidades: la vista principal compara con frente a sin política; positivo, negativo y compensado quedan como respaldo citado.",
        "tablas": [
            {"archivo": "con_descuento/clientes.csv", "necesidad": "Clientes: tipo y elegibilidad para el descuento.", "descarga": "data/archivos/cfo/con_descuento/clientes.csv", "origen": "fuente"},
            {"archivo": "con_descuento/suscripciones.csv", "necesidad": "Suscripciones con inicio y fin.", "descarga": "data/archivos/cfo/con_descuento/suscripciones.csv", "origen": "fuente"},
            {"archivo": "con_descuento/componentes.csv", "necesidad": "Servicios o partidas por suscripción.", "descarga": None, "origen": "fuente"},
            {"archivo": "con_descuento/precios.csv", "necesidad": "Tarifas con vigencia.", "descarga": "data/archivos/cfo/con_descuento/precios.csv", "origen": "fuente"},
            {"archivo": "con_descuento/descuentos.csv", "necesidad": "Descuentos temporales con inicio, fin y objetivo.", "descarga": "data/archivos/cfo/con_descuento/descuentos.csv", "origen": "fuente"},
            {"archivo": "sin_descuento/descuentos.csv", "necesidad": "Referencia sin política: archivo vacío que ilustra la ausencia de descuentos.", "descarga": "data/archivos/cfo/sin_descuento/descuentos.csv", "origen": "fuente"},
            {"archivo": "con_descuento/estados.csv", "necesidad": "Estados por suscripción y mes.", "descarga": None, "origen": "fuente"},
            {"archivo": "con_descuento/componentes_mes.csv", "necesidad": "Valoración mensual: cantidad × tarifa menos descuento.", "descarga": None, "origen": "derivada", "derivacion": "Calculada desde componentes, precios y descuentos vigentes."},
            {"archivo": "con_descuento/pagos.csv", "necesidad": "Cobros con pendientes y cargos no recurrentes.", "descarga": None, "origen": "fuente"},
            {"archivo": "con_descuento/movimientos.csv", "necesidad": "Agregado por cliente y mes.", "descarga": None, "origen": "derivada", "derivacion": "Agregado de componentes_mes y pagos por cliente y mes."},
        ],
    },
    "puente": "Con estos datos se construyó la demostración. A partir de aquí continúa el recorrido existente: respuestas a las tres preguntas del CFO, evolución del MRR, recuperación, explicación y cierre con acción.",
}

for caso, dato in (("cro", CRO), ("cfo", CFO)):
    p = RAIZ / f"src/content/{caso}.json"
    c = json.loads(p.read_text(encoding="utf-8"))
    assert dato["pregunta"] == c["recorrido"]["pregunta_principal"], f"pregunta diverge en {caso}"
    assert dato["proposito"] == c["recorrido"]["proposito"], f"propósito diverge en {caso}"
    assert len(dato["originales"]) == 3
    c["construccion"] = dato
    p.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{caso}: construccion lista ({len(dato['faltante'])} faltantes, {len(dato['sinteticos']['tablas'])} tablas)")
