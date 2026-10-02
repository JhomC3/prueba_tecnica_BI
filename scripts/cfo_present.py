"""Figuras y lecturas descriptivas CFO; todas las cifras vienen de resultados."""
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

ROOT=Path(__file__).resolve().parents[1]
LABELS={'positivo':'Positivo','negativo':'Negativo','compensado':'Compensado'}
CONFIG={'displaylogo':False, 'responsive':True}


def frame(scenario, name='mensual'):
    return pd.read_csv(ROOT/f'resultados/cfo/metricas/{scenario}/{name}.csv')


def localize(scenario):
    """Vista pareada por elegibilidad y fase; no cambia datos/indicadores previos."""
    folder=ROOT/f'datos/sinteticos/cfo/{scenario}'
    sources=[pd.read_csv(folder/g/'movimientos.csv') for g in ('con_descuento','sin_descuento')]
    a,b=sources
    joined=a.merge(b,on=['cliente','mes'],suffixes=('_con','_sin'),validate='one_to_one')
    clients=pd.read_csv(folder/'con_descuento/clientes.csv')[['cliente','elegible']]
    joined=joined.merge(clients,on='cliente',validate='many_to_one')
    joined['poblacion']=joined.elegible.map({1:'Elegibles',0:'Resto'})
    joined['fase']=joined.mes.map(lambda m:'previo' if m<'2025-07-01' else 'durante' if m<'2025-10-01' else 'posterior')
    joined['cliente_activo']=joined.cliente.where((joined.activo_con==1)|(joined.activo_sin==1))
    for source,target in [('neto','diferencia_neta'),('bruto','diferencia_bruta'),('descuento','diferencia_descuento'),
                          ('subyacente','variacion_mrr_servicio'),('pricing','variacion_mrr_tarifa')]:
        joined[target]=joined[f'{source}_con']-joined[f'{source}_sin']
    focus=joined.groupby(['poblacion','fase'],as_index=False).agg(
        clientes=('cliente_activo','nunique'),diferencia_neta=('diferencia_neta','sum'),
        diferencia_bruta=('diferencia_bruta','sum'),diferencia_descuento=('diferencia_descuento','sum'),
        variacion_mrr_servicio=('variacion_mrr_servicio','sum'),variacion_mrr_tarifa=('variacion_mrr_tarifa','sum'))
    assert (focus.diferencia_neta==focus.diferencia_bruta-focus.diferencia_descuento).all()
    assert focus.diferencia_neta.sum()==frame(scenario,'comparacion').diferencia.sum()
    return focus


def reasoning(scenario):
    """Cada diferencia elige foco, explicación y acción; equilibrio no es pérdida."""
    focus=localize(scenario)
    comparison=frame(scenario,'comparacion')
    selected=comparison[comparison.mes>='2025-07-01']
    delta=int(selected.diferencia.sum())
    result='aumento' if delta>0 else 'reduccion' if delta<0 else 'equilibrio'
    scores=focus.groupby('poblacion').diferencia_neta.apply(lambda s:s.abs().sum())
    location=scores.idxmax() if scores.max()>0 else 'Sin diferencia localizada'
    gross=int(focus.diferencia_bruta.sum());discount=int(focus.diferencia_descuento.sum())
    c=frame(scenario,'cohortes')
    ca=c[c.grupo=='con_descuento'].retencion.to_numpy()
    cb=c[c.grupo=='sin_descuento'].retencion.to_numpy()
    same_retention=bool((ca==cb).all())
    folder=ROOT/f'datos/sinteticos/cfo/{scenario}'
    a=pd.read_csv(folder/'con_descuento/movimientos.csv')
    b=pd.read_csv(folder/'sin_descuento/movimientos.csv')
    paired=a[['cliente','mes','activo']].merge(b[['cliente','mes','activo']],on=['cliente','mes'],suffixes=('_con','_sin'),validate='one_to_one')
    same_activity=bool((paired.activo_con==paired.activo_sin).all())
    service=int(focus.variacion_mrr_servicio.sum());price=int(focus.variacion_mrr_tarifa.sum())
    actions={
        'aumento':'Validar la combinación en un piloto acotado antes de extenderla; el beneficio de ingreso observado en la demo no acredita rentabilidad real.',
        'reduccion':'Revisar monto o duración y exigir evidencia de ampliación o permanencia que compense la reducción antes de extender la política.',
        'equilibrio':'Si el objetivo es aumentar ingreso acumulado, esta combinación no lo logra en el horizonte; revisar condiciones. Si se busca retención, comprobar ese beneficio antes de justificarla.'}
    next_step=('Localizar qué meses y clientes compensan la reducción inicial.' if result=='equilibrio' else
               'Localizar qué clientes y periodos aportan a la diferencia frente a la referencia.')
    if location=='Sin diferencia localizada':
        next_step='No hay diferencia de ingreso localizada; comprobar si existe otro objetivo comercial declarado antes de abrir más análisis.'
    return dict(resultado=result,delta=delta,foco=location,
        comprobar=f'Julio 2025–marzo 2026: diferencia acumulada {delta/100:+,.0f} UM frente a la referencia sin descuento; resultado: {"reducción" if result=="reduccion" else result}.',
        siguiente=next_step,
        explicar=f'Diferencia de ingreso bruto acumulado {gross/100:+,.0f} UM menos diferencia de descuentos {discount/100:+,.0f} UM = {delta/100:+,.0f} UM netas. En el puente pareado, variación adicional de MRR por servicios/uso: {service/100:+,.0f} UM; por tarifa: {price/100:+,.0f} UM. Estas variaciones de MRR no se suman directamente como ingreso acumulado.',
        retencion_igual=same_retention,
        actividad_igual_por_cliente=same_activity,
        accion=actions[result],
        evaluacion='Finanzas y Comercial (responsables propuestos): antes del piloto, registrar contratos, objetivo y grupo comparable; revisar mensualmente neto/puente y cerrar tras la vigencia más seguimiento posterior. Evaluar ingreso acumulado frente a referencia, retención y margen cuando haya costos. Hoy solo se verificó el modelo; impacto real pendiente.')


def layout(fig,title,unit='UM',time=True):
    fig.update_layout(template='plotly_white',title=title,height=420,
        font=dict(family='Arial, sans-serif',size=14,color='#243247'),
        margin=dict(l=65,r=25,t=65,b=60),legend=dict(orientation='h',y=-.2),
        xaxis_title='Mes · enero 2025–marzo 2026' if time else '',
        yaxis_title=unit,hovermode='x unified')
    return fig


def lines(df, fields, title, divisor=100,unit='UM'):
    fig=go.Figure()
    for field,label in fields:
        fig.add_trace(go.Scatter(x=df['mes'],y=df[field]/divisor,name=label,mode='lines+markers'))
    return layout(fig,title,unit)


def figures(scenario):
    monthly=frame(scenario)
    treatment=monthly[monthly.grupo=='con_descuento']
    reference=monthly[monthly.grupo=='sin_descuento']
    movement=pd.read_csv(ROOT/f'datos/sinteticos/cfo/{scenario}/con_descuento/movimientos.csv')
    customer=movement[movement.cliente=='C000']
    # C000 siempre activo; su historia muestra bruto y neto sin mezclar caja.
    customer=customer.rename(columns={'descuento':'descuentos'})
    examples=pd.read_csv(ROOT/'resultados/cfo/ejemplos.csv').iloc[:2]
    fig=go.Figure()
    for field,label in [('bruto','Valor bruto'),('neto','Ingreso neto')]:
        fig.add_trace(go.Bar(x=['Contracción de servicios','Descuento aplicado'],y=examples[field]/100,name=label))
    fig.update_layout(barmode='group')
    out={'01_valor_descuento':layout(fig,'Dos causas distintas para pasar de 100 a 80',time=False)}
    july=customer[customer.mes=='2025-07-01'].iloc[0]
    october=customer[customer.mes=='2025-10-01'].iloc[0]
    out['02_movimientos']=layout(go.Figure(go.Waterfall(
        x=['Antes','Servicio/uso','Tarifa','Inicio descuento','Durante','Fin descuento','Después'],
        measure=['absolute','relative','relative','relative','total','relative','total'],
        y=[july.neto_anterior/100,july.subyacente/100,july.pricing/100,-july.delta_descuento/100,0,
           -october.delta_descuento/100,0],connector={'line':{'color':'#94a3b8'}})),
        '¿Por qué cambió el ingreso del cliente?',time=False)
    fig=go.Figure()
    for df,field,label in [(treatment,'bruto','Bruto con política'),(treatment,'neto','Neto con política'),(reference,'neto','Sin descuento')]:
        fig.add_trace(go.Scatter(x=df.mes,y=df[field]/100,name=label,mode='lines+markers'))
    out['03_mrr']=layout(fig,'Evolución del ingreso recurrente')
    cohort=frame(scenario,'cohortes')
    out['04_retencion']=lines(cohort[cohort.grupo=='con_descuento'],
        [('retencion','Clientes retenidos'),('nrr','NRR'),('grr','GRR')],
        'Retención de clientes e ingresos',divisor=.01,unit='%')
    out['05_churn']=lines(treatment,[('churn','Churn mensual')],'Bajas de clientes',divisor=.01,unit='%')
    out['06_arpu_ltv']=lines(treatment,[('arpu','MRR promedio por cliente'),('ltv_ingreso','LTV estimado de ingreso')],
        'Ingreso por cliente y estimación de LTV')
    fig=go.Figure()
    for group,label in [('con_descuento','Con política'),('sin_descuento','Sin descuento')]:
        df=monthly[(monthly.grupo==group)&(monthly.mes>='2025-07-01')].copy()
        fig.add_trace(go.Scatter(x=df.mes,y=df.neto.cumsum()/100,name=label,mode='lines+markers'))
    out['07_acumulado']=layout(fig,'Ingreso acumulado desde el inicio del descuento')
    fig=go.Figure()
    for name,label in LABELS.items():
        df=frame(name);a=df[(df.grupo=='con_descuento')&(df.mes>='2025-07-01')]
        b=df[(df.grupo=='sin_descuento')&(df.mes>='2025-07-01')]
        fig.add_trace(go.Scatter(x=a.mes,y=(a.neto.to_numpy()-b.neto.to_numpy()).cumsum()/100,
                                 name=label,mode='lines+markers'))
    out['08_comparacion']=layout(fig,'Diferencia acumulada frente a no ofrecer descuento')
    residual=treatment.neto-treatment.saldo_inicial-treatment.apertura_mrr-treatment.nuevo_mrr-treatment.reactivacion_mrr-treatment.churn_bruto-treatment.expansion_subyacente-treatment.contraccion_subyacente-treatment.pricing+treatment.delta_descuento
    out['09_conciliacion']=layout(go.Figure(go.Bar(x=treatment.mes,y=residual/100,name='Residuo')),
                                 'Diferencia sin explicar en el puente de MRR')
    return out


def conclusions(scenario):
    manifest=json.loads((ROOT/'resultados/cfo/manifest.json').read_text())['escenarios'][scenario]
    monthly=frame(scenario);t=monthly[monthly.grupo=='con_descuento'];r=monthly[monthly.grupo=='sin_descuento']
    c=frame(scenario,'cohortes');last=c[(c.grupo=='con_descuento')].iloc[-1]
    customer=pd.read_csv(ROOT/f'datos/sinteticos/cfo/{scenario}/con_descuento/movimientos.csv')
    customer=customer[customer.cliente=='C000'];j=customer[customer.mes=='2025-07-01'].iloc[0];o=customer[customer.mes=='2025-10-01'].iloc[0]
    d=manifest['delta_acumulado']/100
    classification='mayor' if d>0 else 'menor' if d<0 else 'igual'
    route=reasoning(scenario)
    return {
        '1':"El mismo neto de 80 UM puede resultar de bruto 80 sin descuento o bruto 100 con descuento 20. El modelo distingue contracción subyacente de reducción comercial; cliente + mes + pago no identifica la causa.",
        '2':f"Al inicio, el cambio neto es {j.delta_neto/100:+,.0f} UM; al vencer el descuento es {o.delta_neto/100:+,.0f} UM. En el vencimiento la ampliación subyacente es {o.subyacente/100:,.0f} UM: el aumento procede de retirar el descuento.",
        '3':f"El MRR neto final es {t.iloc[-1].neto/100:,.0f} UM, frente a {r.iloc[-1].neto/100:,.0f} sin descuento. La cohorte inicial retiene {last.retencion*100:.1f}% de clientes; NRR {last.nrr*100:.1f}% y GRR {last.grr*100:.1f}%. Las bajas son iguales entre grupos: este escenario no demuestra un beneficio de retención. La evolución total incluye altas, reactivaciones y pricing; no se atribuye toda al descuento.",
        '4':f"Durante julio 2025–marzo 2026, el ingreso neto con política es {classification} al de la referencia: diferencia {d:+,.0f} UM. Descuentos aplicados: {manifest['descuentos_acumulados']/100:,.0f} UM. {route['siguiente']} La comparación es una respuesta de simulación pareada, no una estimación causal histórica ni utilidad.",
        '5':"El puente concilia sin residuo; estados, tarifas y descuentos se identifican por separado. Los pagos incorporan atraso y cargo no recurrente conciliables: no se fuerzan a igualar MRR. El histórico original no contiene esos contratos ni causas; las respuestas son demostraciones del modelo propuesto."
    }


def run():
    for scenario in LABELS:
        path=ROOT/f'resultados/cfo/graficas/{scenario}';path.mkdir(parents=True,exist_ok=True)
        for name,fig in figures(scenario).items():
            fig.write_html(path/f'{name}.html',include_plotlyjs='directory',config=CONFIG)
        (ROOT/f'resultados/cfo/metricas/{scenario}/conclusiones.json').write_text(
            json.dumps(conclusions(scenario),ensure_ascii=False,indent=2)+'\n')
    run_reasoning()
    print('27 figuras HTML y lecturas de cinco preguntas por escenario.')


def run_reasoning():
    for scenario in LABELS:
        target=ROOT/f'resultados/cfo/metricas/{scenario}'
        localize(scenario).to_csv(target/'focos.csv',index=False)
        (target/'recorrido.json').write_text(json.dumps(reasoning(scenario),ensure_ascii=False,indent=2)+'\n')
        (target/'conclusiones.json').write_text(json.dumps(conclusions(scenario),ensure_ascii=False,indent=2)+'\n')
    print('Focos y recorrido guardados; fuentes, indicadores y gráficas previas intactos.')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--recorrido',action='store_true')
    args=parser.parse_args()
    run_reasoning() if args.recorrido else run()
