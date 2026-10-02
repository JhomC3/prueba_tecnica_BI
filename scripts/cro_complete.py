"""Extensión CRO: datos coherentes y métricas SQL, sin gráficas ni APIs."""
import random
from datetime import date, timedelta

ACCOUNT_EXTRA = {
    'fecha_captacion': ('Fecha', 'Primera captación observada en la simulación'),
    'campana': ('Texto opcional', 'Campaña de captación; no aplica a todos los canales'),
    'producto': ('Texto', 'Producto de interés'),
    'region': ('Texto', 'Región ilustrativa'),
    'perfil': ('Texto', 'Tamaño de empresa ilustrativo'),
    'responsable': ('Texto opcional', 'Responsable inicial'),
    'fecha_asignacion': ('Fecha opcional', 'Asignación inicial'),
    'ajuste_perfil': ('Entero opcional 0/1', 'Cumple tamaño de empresa objetivo de esta demo'),
    'necesidad': ('Entero opcional 0/1', 'Declara una necesidad cubierta por el producto'),
    'intencion': ('Entero opcional 0/1', 'Declara intención de evaluar compra en 90 días'),
    'fecha_evaluacion': ('Fecha opcional', 'Fecha de evaluación observada'),
    'version_criterios': ('Texto opcional', 'Versión de criterios aplicada'),
    'calificado': ('Entero opcional 0/1', 'Cumple los tres criterios; vacío si no evaluado'),
    'motivo_descalificacion': ('Texto opcional', 'Criterio no cumplido; no implica pérdida comercial'),
    'inicio_historia_pagos': ('Fecha', 'Inicio de historia de pagos completa en la simulación'),
    'pagador_previo': ('Entero 0/1', 'Existe un pago válido anterior a la captación'),
}
EVENT_EXTRA = {
    'motivo_perdida': ('Texto opcional', 'Motivo registrado de pérdida, no causa demostrada'),
    'responsable_etapa': ('Texto opcional', 'Responsable de la visita'),
    'fecha_asignacion_etapa': ('Fecha opcional', 'Asignación durante la visita'),
}
INTERACTIONS = {
    'id_interaccion': ('Texto · clave', 'Identificador de interacción'),
    'id_cuenta': ('Texto · relación', 'Cuenta atendida'),
    'id_registro': ('Texto · relación', 'Visita de etapa atendida'),
    'fecha': ('Fecha', 'Fecha del intento'),
    'tipo': ('Texto', 'Llamada o correo'),
    'resultado': ('Texto', 'Sin respuesta o intercambio efectivo'),
    'responsable': ('Texto', 'Responsable de la interacción'),
}
PAYMENTS = {
    'id_pago': ('Texto · clave', 'Identificador de pago'),
    'id_cuenta': ('Texto · relación', 'Cuenta pagadora'),
    'fecha_pago': ('Fecha', 'Fecha del evento de pago'),
    'estado_pago': ('Texto', 'Valido o fallido; solo valido cuenta'),
}
RULES = {
    'unidad': 'cuenta = una oportunidad en esta demostración',
    'periodo_base': ['2026-01-01', '2026-05-01'],
    'periodo_reciente': ['2026-05-01', '2026-09-01'],
    'ventanas_cohorte_dias': [30, 60, 90],
    'calidad_v1': 'ajuste_perfil=1 AND necesidad=1 AND intencion=1; no inferida de Won',
    'perfil_objetivo': 'micro o pequena empresa',
    'plazo_primer_intento_dias': 2,
    'plazo_naturaleza': 'supuesto ilustrativo uniforme, no SLA real',
    'contacto_efectivo': 'interacción registrada como intercambio_efectivo',
    'marketing': ['Marketing pago', 'Orgánico'],
    'historia_pagos_desde': '2025-01-01',
    'historia_pagos': 'completa desde el inicio declarado para estas cuentas sintéticas',
    'percentil': 'rango más próximo ceil(0.9*n)',
    'reingresos': 'tasas por cuenta y primera visita a cada etapa; visitas adicionales separadas',
    'saltos': 'separados del avance a etapa siguiente; nunca contados como pérdidas',
    'advertencia': 'Supuestos de demostración; no benchmarks ni datos observados de Finora',
}


def generate_full(base_generate, scenario='referencia', seed=42, size=180,
                  cutoff='2026-09-30', stage='Working'):
    accounts, events = base_generate(scenario, seed, size, cutoff, stage)
    cut = date.fromisoformat(cutoff)
    interactions, payments = [], []
    by_account = {}
    for e in events:
        by_account.setdefault(e['id_cuenta'], []).append(e)
    full_events = []
    for a in accounts:
        rng = random.Random(f'completo:{seed}:{a["id_cuenta"]}')
        rows = by_account[a['id_cuenta']]
        captured = date.fromisoformat(rows[0]['entrada'])
        selfserve = rng.random() < .12
        # Extensión estable entre escenarios: conserva el núcleo comercial programado.
        if selfserve:
            a['tipo_entrada'] = 'Producto'
            rows = []
        # Salto SQL -> Proposal: elimina Demo y conserva el tiempo y resultado terminal.
        elif rng.random() < .08:
            for i in range(len(rows)-2):
                if rows[i]['id_etapa']=='SQL' and rows[i+1]['id_etapa']=='Demo' and rows[i+2]['id_etapa']=='Proposal':
                    rows[i]['salida'] = rows[i+2]['entrada']
                    rows[i]['id_etapa_destino'] = 'Proposal'
                    rows.pop(i+1)
                    break
        # Una visita adicional a Working; dividir el tiempo, sin inventar tiempo negativo.
        if not selfserve and rng.random() < .1:
            for i, e in enumerate(rows):
                if e['id_etapa']=='Working' and e['salida']:
                    middle = date.fromisoformat(e['entrada'])+timedelta(days=1)
                    if middle.isoformat()<e['salida']:
                        rest = dict(e, id_registro=e['id_registro']+'-r', entrada=middle.isoformat())
                        e['salida'],e['estado'],e['id_etapa_destino'] = middle.isoformat(),'avance','Working'
                        rows.insert(i+1,rest)
                    break
        profile = rng.choice(['micro','pequena','mediana'])
        evaluation = captured + timedelta(days=rng.randint(0,3))
        evaluated = rng.random() < .85 and evaluation<=cut
        fit = int(profile in ('micro','pequena')) if evaluated else None
        need = int(rng.random()<.8) if evaluated else None
        intent = int(rng.random()<.7) if evaluated else None
        qualified = int(bool(fit and need and intent)) if evaluated else None
        reason = None if qualified or not evaluated else ('fuera_perfil' if not fit else 'sin_necesidad' if not need else 'sin_intencion')
        prior = rng.random()<.06
        assignment = captured+timedelta(days=rng.randint(0,2))
        a.update(fecha_captacion=captured.isoformat(),campana=rng.choice(['Busqueda','Contenido']) if a['canal']!='Referidos' else None,
                 producto=rng.choice(['Contabilidad','Facturacion']),region=rng.choice(['Colombia','Mexico']),perfil=profile,
                 responsable=None if selfserve else 'Ventas-'+str(rng.randint(1,4)),
                 fecha_asignacion=None if selfserve or assignment>cut else assignment.isoformat(),
                 ajuste_perfil=fit,necesidad=need,intencion=intent,fecha_evaluacion=evaluation.isoformat() if evaluated else None,
                 version_criterios='v1' if evaluated else None,calificado=qualified,motivo_descalificacion=reason,
                 inicio_historia_pagos='2025-01-01',pagador_previo=int(prior))
        if prior:
            payments.append(dict(id_pago=a['id_cuenta']+'-previo',id_cuenta=a['id_cuenta'],fecha_pago='2025-12-15',estado_pago='valido'))
        for e in rows:
            entered=date.fromisoformat(e['entrada'])
            end=date.fromisoformat(e['salida']) if e['salida'] else cut
            assigned=entered+timedelta(days=rng.randint(0,1))
            assigned=min(assigned,end)
            e.update(motivo_perdida=rng.choice(['sin_presupuesto','sin_prioridad','competidor',None]) if e['estado']=='perdido' else None,
                     responsable_etapa=a['responsable'] if e['id_etapa']!='Won' else None,
                     fecha_asignacion_etapa=assigned.isoformat() if e['id_etapa']!='Won' else None)
            if e['id_etapa']=='Won':
                continue
            if rng.random()<.88:
                first=assigned+timedelta(days=rng.randint(0,4))
                for n in range(rng.randint(1,3)):
                    when=first+timedelta(days=n)
                    if when>end or when>cut:
                        break
                    interactions.append(dict(id_interaccion=e['id_registro']+'-i'+str(n),id_cuenta=a['id_cuenta'],id_registro=e['id_registro'],
                                             fecha=when.isoformat(),tipo=rng.choice(['llamada','correo']),
                                             resultado='intercambio_efectivo' if rng.random()<.55 else 'sin_respuesta',responsable=a['responsable']))
        won=next((date.fromisoformat(e['entrada']) for e in rows if e['id_etapa']=='Won'),None)
        rng=random.Random(f'pago:{seed}:{a["id_cuenta"]}')
        pay_date=(captured+timedelta(days=rng.randint(0,3))) if selfserve else (won+timedelta(days=rng.randint(0,5)) if won else None)
        if pay_date and pay_date<=cut:
            # Incluye fallos, Won sin pago y pagos repetidos que no son nuevas adquisiciones.
            payments.append(dict(id_pago=a['id_cuenta']+'-fallido',id_cuenta=a['id_cuenta'],fecha_pago=pay_date.isoformat(),estado_pago='fallido'))
            if selfserve or rng.random()<.9:
                payments.append(dict(id_pago=a['id_cuenta']+'-p1',id_cuenta=a['id_cuenta'],fecha_pago=pay_date.isoformat(),estado_pago='valido'))
                later=pay_date+timedelta(days=30)
                if later<=cut:
                    payments.append(dict(id_pago=a['id_cuenta']+'-p2',id_cuenta=a['id_cuenta'],fecha_pago=later.isoformat(),estado_pago='valido'))
        full_events.extend(rows)
    return accounts,full_events,interactions,payments


def install_metadata(fields, dictionary):
    for table, extras in [('dim_cuentas',ACCOUNT_EXTRA),('fact_etapas',EVENT_EXTRA)]:
        fields[table] += list(extras)
        dictionary[table][2].update(extras)
    dictionary['dim_cuentas'][2]['tipo_entrada']=('Texto','Entrada por New, SQL o compra desde producto')
    for table,title,grain,cols in [('interacciones','Interacciones','Llamadas o correos realizados durante una visita de etapa; fecha y respuesta. Sirve para medir atención, no permanencia.',INTERACTIONS),
                                   ('pagos','Pagos','Intentos de pago y su resultado. Sirve para identificar primeros pagos válidos; varios pagos de una empresa no son varios clientes nuevos.',PAYMENTS)]:
        fields[table]=list(cols)
        dictionary[table]=(title,grain,cols)


def validate_full(con, cutoff):
    checks = {
        'relaciones': 'SELECT COUNT(*) FROM pragma_foreign_key_check',
        'interacciones_fuera_visita': '''SELECT COUNT(*) FROM interacciones i JOIN fact_etapas f USING(id_registro)
            WHERE i.id_cuenta<>f.id_cuenta OR i.fecha<f.entrada OR i.fecha>COALESCE(f.salida,:corte)
               OR i.fecha<f.fecha_asignacion_etapa OR f.id_etapa='Won' ''',
        'fechas_etapas': "SELECT COUNT(*) FROM fact_etapas WHERE entrada>:corte OR salida>:corte OR salida<entrada OR fecha_asignacion_etapa<entrada OR fecha_asignacion_etapa>COALESCE(salida,:corte)",
        'pagos_fuera_historia': 'SELECT COUNT(*) FROM pagos p JOIN dim_cuentas c USING(id_cuenta) WHERE p.fecha_pago>:corte OR p.fecha_pago<c.inicio_historia_pagos',
        'calidad': '''SELECT COUNT(*) FROM dim_cuentas WHERE
            (fecha_evaluacion IS NULL AND calificado IS NOT NULL) OR
            (fecha_evaluacion IS NOT NULL AND (calificado IS NULL OR calificado<>(ajuste_perfil AND necesidad AND intencion)))
            OR fecha_evaluacion>:corte OR fecha_evaluacion<fecha_captacion''',
        'captacion': 'SELECT COUNT(*) FROM dim_cuentas WHERE fecha_captacion>:corte OR fecha_asignacion<fecha_captacion OR fecha_asignacion>:corte',
        'producto_sin_etapas': "SELECT COUNT(*) FROM fact_etapas f JOIN dim_cuentas c USING(id_cuenta) WHERE c.tipo_entrada='Producto'",
        'historia_previa': '''SELECT COUNT(*) FROM dim_cuentas c WHERE c.pagador_previo <>
            EXISTS(SELECT 1 FROM pagos p WHERE p.id_cuenta=c.id_cuenta AND p.estado_pago='valido' AND p.fecha_pago<c.fecha_captacion)''',
        'estado_etapa': '''SELECT COUNT(*) FROM fact_etapas f WHERE
          (f.estado='avance' AND (f.salida IS NULL OR f.id_etapa_destino IS NULL OR
            (SELECT orden FROM dim_etapas WHERE id_etapa=f.id_etapa_destino)<(SELECT orden FROM dim_etapas WHERE id_etapa=f.id_etapa)))
          OR (f.estado<>'avance' AND f.id_etapa_destino IS NOT NULL)
          OR (f.estado='perdido' AND f.salida IS NULL)
          OR (f.estado IN ('ganado','abierto') AND f.salida IS NOT NULL)
          OR (f.estado='ganado')<>(f.id_etapa='Won')''',
        'entrada_inicial': '''SELECT COUNT(*) FROM dim_cuentas c WHERE c.tipo_entrada<>'Producto' AND
           NOT EXISTS(SELECT 1 FROM fact_etapas f WHERE f.id_cuenta=c.id_cuenta AND f.id_etapa=c.tipo_entrada AND f.entrada=c.fecha_captacion)''',
        'continuidad': '''WITH v AS (SELECT *, lead(entrada) OVER(PARTITION BY id_cuenta ORDER BY entrada,id_registro) siguiente_fecha,
             lead(id_etapa) OVER(PARTITION BY id_cuenta ORDER BY entrada,id_registro) siguiente_etapa FROM fact_etapas)
             SELECT COUNT(*) FROM v WHERE estado='avance' AND (siguiente_fecha IS NULL OR salida<>siguiente_fecha OR id_etapa_destino<>siguiente_etapa)
             OR estado<>'avance' AND siguiente_fecha IS NOT NULL''',
    }
    counts={k:con.execute(q,{'corte':cutoff}).fetchone()[0] for k,q in checks.items()}
    if any(counts.values()):
        raise ValueError(f'Controles del modelo completo: {counts}')
    if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
        raise ValueError('SQLite no íntegro')
    return counts


def complete_metrics(con,cutoff):
    """SQL revisable en sql/cro/completas.sql; no joins multiplicadores."""
    from pathlib import Path
    text=(Path(__file__).resolve().parents[1]/'sql/cro/completas.sql').read_text()
    queries={}
    for block in text.split('-- @consulta ')[1:]:
        name,sql=block.split('\n',1)
        queries[name.strip()]=sql
    output={name:[] for name in queries}
    dims=['total','tipo_entrada','canal','industria','perfil','producto','region','campana']
    params={'corte':cutoff,'plazo':RULES['plazo_primer_intento_dias']}
    for dim in dims:
        for name,sql in queries.items():
            rendered=sql.replace('__SEGMENTO__',"'Todos'" if dim=='total' else f"COALESCE(c.{dim},'No aplica')")
            rows=[dict(r,dimension=dim) for r in con.execute(rendered,params)]
            output[name].extend(rows)
    return output
