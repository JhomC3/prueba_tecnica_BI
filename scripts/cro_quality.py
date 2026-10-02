"""Puntuaciones aleatorias para demostrar el análisis, sin modelo de calificación."""
from pathlib import Path
import csv
import random
import pandas as pd
import plotly.graph_objects as go


def generate_scores(accounts_path, output_path, seed=20261001):
    """Una puntuación por cuenta New; no depende de Won ni de su conversión."""
    with open(accounts_path, encoding='utf-8', newline='') as source:
        accounts=sorted((row for row in csv.DictReader(source) if row['tipo_entrada']=='New'),
                        key=lambda row:row['id_cuenta'])
    rng=random.Random(seed)
    rows=[{'id_cuenta':row['id_cuenta'],'puntuacion_calidad':rng.randint(0,100)} for row in accounts]
    output_path=Path(output_path)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open('w',encoding='utf-8',newline='') as target:
        writer=csv.DictWriter(target,fieldnames=['id_cuenta','puntuacion_calidad'])
        writer.writeheader();writer.writerows(rows)
    return len(rows)


def analyze_scores(accounts_path, scores_path, month_of_increase=None):
    accounts=pd.read_csv(accounts_path)
    accounts=accounts.loc[accounts['tipo_entrada'].eq('New')].copy()
    if not Path(scores_path).exists():
        return {'figures':[], 'reading':'No disponemos de puntuaciones de calidad. No atribuimos la caída a calidad; proponemos implementar su medición y avanzamos con el análisis de etapas.'}
    scores=pd.read_csv(scores_path)
    if scores['id_cuenta'].duplicated().any() or accounts['id_cuenta'].duplicated().any():
        raise ValueError('La puntuación debe ser única por cuenta')
    if not set(scores['id_cuenta']).issubset(set(accounts['id_cuenta'])):
        raise ValueError('Hay puntuaciones de cuentas fuera de las entradas New')
    values=pd.to_numeric(scores['puntuacion_calidad'],errors='raise')
    if not values.dropna().between(0,100).all():
        raise ValueError('Las puntuaciones deben estar entre 0 y 100')
    scores['puntuacion_calidad']=values
    data=accounts.merge(scores,on='id_cuenta',how='left',validate='one_to_one')
    if not data['puntuacion_calidad'].notna().any():
        return {'figures':[], 'reading':'No disponemos de puntuaciones de calidad. Proponemos implementar su medición y avanzamos con el análisis de etapas.'}
    data['mes']=pd.to_datetime(data['fecha_captacion']).dt.to_period('M').astype(str)
    def aggregate(group):
        return data.groupby(group,as_index=False).agg(
            puntuacion_media=('puntuacion_calidad','mean'),
            puntuados=('puntuacion_calidad','count'),entradas_new=('id_cuenta','size'))
    total=aggregate('mes');channels=aggregate(['mes','canal'])
    figures=[]
    years=sorted(pd.to_datetime(data['fecha_captacion']).dt.year.unique())
    period=str(years[0]) if len(years)==1 else f'{years[0]}–{years[-1]}'
    for title,frame,by_channel in [(f'Puntuación media de los New · {period}',total,False),
                                   (f'Puntuación media de los New por canal · {period}',channels,True)]:
        fig=go.Figure()
        groups=frame.groupby('canal',sort=True) if by_channel else [('Global',frame)]
        colors={'Global':'#2563eb','Marketing pago':'#2563eb','Orgánico':'#0d9488','Referidos':'#c76a12'}
        for name,group in groups:
            fig.add_trace(go.Scatter(x=group['mes'],y=group['puntuacion_media'],name=name,
                mode='lines+markers',line=dict(color=colors.get(name,'#64748b'),width=3),
                customdata=group[['puntuados','entradas_new']].to_numpy(),
                hovertemplate='%{x}<br>Puntuación media: %{y:.1f}/100<br>Puntuados: %{customdata[0]} de %{customdata[1]}<extra>%{fullData.name}</extra>'))
        fig.update_layout(title=title,template='plotly_white',height=420,
            font=dict(family='Arial, sans-serif',size=14),margin=dict(l=65,r=30,t=65,b=90),
            xaxis_title='Mes de entrada a New',yaxis_title='Puntuación media (0–100)',
            showlegend=by_channel,legend=dict(orientation='h',y=-.25))
        figures.append(fig)
    reading='No hay una comparación mensual disponible para el periodo del aumento de New.'
    if month_of_increase:
        previous=(pd.Period(month_of_increase,freq='M')-1).strftime('%Y-%m')
        indexed=total.set_index('mes')
        if previous in indexed.index and month_of_increase in indexed.index:
            a=indexed.loc[previous,'puntuacion_media'];b=indexed.loc[month_of_increase,'puntuacion_media']
            if pd.notna(a) and pd.notna(b):
                change='bajó' if b<a else 'subió' if b>a else 'se mantuvo'
                months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
                label=lambda date:months[pd.Period(date,freq='M').month-1]
                fmt=lambda value:f'{value:.1f}'.replace('.',',')
                reading=(f'De {label(previous)} a {label(month_of_increase)}, la puntuación media {change} '
                         f'de {fmt(a)} a {fmt(b)} sobre 100. ')
                reading+=(f'Las medias mensuales oscilan entre {fmt(total["puntuacion_media"].min())} '
                          f'y {fmt(total["puntuacion_media"].max())}. ')
                reading+='Son puntuaciones aleatorias: no permiten atribuir la caída de conversión a calidad. Revisamos las etapas.'
    if total['puntuados'].lt(total['entradas_new']).any():
        reading+=' Hay New sin puntuación; la media describe únicamente los puntuados.'
    return {'figures':figures,'reading':reading,'total':total,'channels':channels}


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    for scenario in ('referencia','conversion','demora'):
        source=root/'datos/sinteticos/cro'/scenario
        count=generate_scores(source/'dim_cuentas.csv',source/'puntuaciones_leads.csv')
        result=analyze_scores(source/'dim_cuentas.csv',source/'puntuaciones_leads.csv')
        target=root/'resultados/cro/metricas'/scenario
        result['total'].to_csv(target/'puntuacion_leads_mensual.csv',index=False)
        result['channels'].to_csv(target/'puntuacion_leads_por_canal.csv',index=False)
        print(f'{scenario}: {count} puntuaciones aleatorias generadas y conciliadas con New.')
