"""Gráficas CRO reutilizables sobre métricas SQL guardadas."""
from pathlib import Path
import math
import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
MONTHS = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
CONFIG = {'displayModeBar': False, 'displaylogo': False, 'responsive': True}


def grafica_new(csv_path, escenario='referencia'):
    """Entradas a New y variación mensual en hover; no recalcula métricas."""
    df = pd.read_csv(csv_path)
    df = df.loc[df['dimension'].eq('total')].copy()
    df['fecha'] = pd.to_datetime(df['mes'], format='%Y-%m')
    df = df.sort_values('fecha')
    if df.empty or df['mes'].duplicated().any() or (df['entradas_new'] < 0).any():
        raise ValueError('La serie mensual de New debe ser única y no negativa')
    labels = [f'{MONTHS[d.month-1]} {d.year}' for d in df['fecha']]
    variations = ['—' if pd.isna(v) else f'{v:+.1f}%'.replace('.',',')
                  for v in df['crecimiento_new_pct']]
    minimo, maximo = float(df['entradas_new'].min()), float(df['entradas_new'].max())
    margen = max(5, (maximo-minimo)*.12)
    paso = 20
    inicio_y = max(0, math.floor((minimo-margen)/paso)*paso)
    limite_y = max(inicio_y+paso, math.ceil((maximo+margen)/paso)*paso)
    fig = go.Figure(go.Scatter(
        x=[d.isoformat() for d in df['fecha']], y=[int(v) for v in df['entradas_new']], mode='lines+markers+text',
        text=[str(int(v)) for v in df['entradas_new']], textposition='top center',
        textfont={'size':12,'color':'#334155'},
        line={'color':'#2563eb','width':2.5}, marker={'size':6},
        customdata=list(zip(labels, variations)),
        hovertemplate='<b>%{customdata[0]}</b><br>Entradas a New: %{y:.0f}<br>Variación mensual: %{customdata[1]}<extra></extra>',
        name='Entradas a New',
    ))
    fig.update_layout(
        title={'text':'¿Cuánto aumentó New?','font':{'size':24},'x':.04},
        template='plotly_white', height=390, margin={'l':65,'r':35,'t':60,'b':60},
        font={'family':'Arial, sans-serif','size':14,'color':'#243247'},
        xaxis={'title':'Mes · 2026','type':'date','tickmode':'array','tickvals':df['fecha'].tolist(),
               'ticktext':[MONTHS[d.month-1] for d in df['fecha']], 'fixedrange':True,'showgrid':False},
        yaxis={'title':'Entradas a New','range':[inicio_y,limite_y],'tickmode':'linear','tick0':inicio_y,'dtick':paso,'fixedrange':True,'gridcolor':'#edf1f5','zeroline':False},
        hovermode='closest', dragmode=False,
        showlegend=False,
    )
    return fig


def guardar_new(escenario='referencia'):
    source=ROOT/'resultados/cro/metricas'/escenario/'demanda.csv'
    target=ROOT/'resultados/cro/graficas/01_new_tendencia.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    fig=grafica_new(source,escenario)
    fig.write_html(target,include_plotlyjs=True,config=CONFIG)
    return target


if __name__=='__main__':
    print(guardar_new())


def grafica_new_won(csv_path, escenario='referencia', ventana=30):
    """Porcentaje de los New de cada mes que llega a Won en un plazo fijo."""
    df=pd.read_csv(csv_path)
    df=df.loc[df['dimension'].eq('total') & df['ventana'].eq(ventana)].copy()
    # Comparar meses completos, sin excluir solo las entradas más recientes.
    df=df.loc[df['elegibles'].eq(df['entradas_new']) & df['entradas_new'].gt(0)]
    df['fecha']=pd.to_datetime(df['mes_entrada'],format='%Y-%m')
    df=df.sort_values('fecha')
    if df.empty or df['mes_entrada'].duplicated().any():
        raise ValueError('No hay meses completos y únicos para este plazo')
    counts=df['ganados_ventana']
    if ((counts<0) | (counts>df['entradas_new'])).any():
        raise ValueError('Los ganados deben estar entre cero y las entradas a New')
    calculated=100*counts/df['entradas_new']
    if not ((calculated-df['conversion_new_won_pct']).abs()<1e-8).all():
        raise ValueError('El porcentaje no coincide con ganados / entradas a New')
    x=[d.isoformat() for d in df['fecha']]
    months=[f'{MONTHS[d.month-1]} {d.year}' for d in df['fecha']]
    values=[float(v) for v in df['conversion_new_won_pct']]
    custom=[[m,int(n),int(w)] for m,n,w in zip(months,df['entradas_new'],counts)]
    fig=go.Figure(go.Scatter(
        x=x,y=values,mode='lines+markers+text',
        text=[f'{v:.1f}%'.replace('.',',') for v in values],textposition='top center',
        line={'color':'#2563eb','width':2.5},marker={'size':6},textfont={'size':12},
        customdata=custom,
        hovertemplate=(f'<b>%{{customdata[0]}}</b><br>Entraron a New: %{{customdata[1]}}'
                       f'<br>De ellos, Won en {ventana} días: %{{customdata[2]}}'
                       '<br>Porcentaje: %{y:.1f}%<extra></extra>')))
    step=5
    pad=max(2,(max(values)-min(values))*.15)
    low=max(0,math.floor((min(values)-pad)/step)*step)
    high=min(100,max(low+step,math.ceil((max(values)+pad)/step)*step))
    years=sorted(df['fecha'].dt.year.unique())
    period=str(years[0]) if len(years)==1 else f'{years[0]}–{years[-1]}'
    fig.update_layout(
        title={'text':f'¿Qué porcentaje de New llegó a Won en {ventana} días?',
               'font':{'size':22},'x':.04},
        template='plotly_white',height=390,margin={'l':65,'r':35,'t':65,'b':60},
        font={'family':'Arial, sans-serif','size':14,'color':'#243247'},
        xaxis={'title':f'Mes de entrada a New · {period}','type':'date','tickmode':'array',
               'tickvals':x,'ticktext':[MONTHS[d.month-1] for d in df['fecha']],
               'fixedrange':True,'showgrid':False},
        yaxis={'title':'New que llegó a Won (%)','range':[low,high],'tickmode':'linear',
               'tick0':low,'dtick':step,'ticksuffix':'%','fixedrange':True,
               'gridcolor':'#edf1f5','zeroline':False},
        hovermode='closest',dragmode=False,showlegend=False)
    return fig


def grafica_new_por_canal(csv_path):
    df=pd.read_csv(csv_path)
    df=df.loc[df['dimension'].eq('canal')].copy()
    df['fecha']=pd.to_datetime(df['mes'],format='%Y-%m')
    if df.empty or df.duplicated(['mes','segmento']).any():
        raise ValueError('Serie de canales vacía o duplicada')
    colors={'Marketing pago':'#2563eb','Orgánico':'#0d9488','Referidos':'#c76a12'}
    fig=go.Figure()
    for channel,group in df.groupby('segmento',sort=True):
        group=group.sort_values('fecha')
        custom=[[f'{MONTHS[d.month-1]} {d.year}', '—' if pd.isna(v) else f'{v:+.1f}%'.replace('.',',')]
                for d,v in zip(group['fecha'],group['crecimiento_new_pct'])]
        fig.add_trace(go.Scatter(x=[d.isoformat() for d in group['fecha']],y=[int(v) for v in group['entradas_new']],
            name=channel,mode='lines+markers',line={'color':colors.get(channel),'width':2.5},marker={'size':6},
            customdata=custom,hovertemplate=f'<b>{channel}</b> · %{{customdata[0]}}<br>Entradas a New: %{{y:.0f}}<br>Variación mensual: %{{customdata[1]}}<extra></extra>'))
    low,max_value=float(df['entradas_new'].min()),float(df['entradas_new'].max())
    pad=max(5,(max_value-low)*.12)
    minimum=max(0,math.floor((low-pad)/10)*10);maximum=math.ceil((max_value+pad)/10)*10
    dates=sorted(df['fecha'].unique())
    fig.update_layout(title={'text':'New por canal','font':{'size':22},'x':.04},template='plotly_white',height=420,
        margin={'l':65,'r':30,'t':55,'b':105},font={'family':'Arial, sans-serif','size':13,'color':'#243247'},
        xaxis={'title':'Mes · 2026','type':'date','tickmode':'array','tickvals':[pd.Timestamp(d).isoformat() for d in dates],
               'ticktext':[MONTHS[pd.Timestamp(d).month-1] for d in dates],'showgrid':False,'fixedrange':True},
        yaxis={'title':'Entradas a New','range':[minimum,maximum],'tickmode':'linear','tick0':minimum,'dtick':10,
               'fixedrange':True,'gridcolor':'#edf1f5','zeroline':False},
        legend={'orientation':'h','x':0,'y':-.3,'xanchor':'left','yanchor':'top'},
        hovermode='closest',dragmode=False)
    return fig


def grafica_conversion_por_canal(csv_path, ventana=30):
    """Serie completa por canal: mismo plazo desde la entrada individual a New."""
    df=pd.read_csv(csv_path)
    df=df.loc[df['dimension'].eq('canal') & df['ventana'].eq(ventana)].copy()
    # Excluir el mes completo si alguno de sus canales tiene seguimiento parcial.
    complete=df.groupby('mes_entrada').apply(
        lambda group: group['elegibles'].eq(group['entradas_new']).all())
    df=df.loc[df['mes_entrada'].isin(complete[complete].index)]
    if df.empty or df.duplicated(['mes_entrada','segmento']).any():
        raise ValueError('La serie mensual por canal debe ser completa y única')
    df['fecha']=pd.to_datetime(df['mes_entrada'],format='%Y-%m')
    positive=df.loc[df['entradas_new'].gt(0)]
    expected=100*positive['ganados_ventana']/positive['entradas_new']
    if not (expected.sub(positive['conversion_new_won_pct']).abs()<1e-8).all():
        raise ValueError('La conversión por canal no coincide con ganados / entradas')
    colors={'Marketing pago':'#2563eb','Orgánico':'#0d9488','Referidos':'#c76a12'}
    fig=go.Figure()
    for channel,group in df.groupby('segmento',sort=True):
        group=group.sort_values('fecha')
        custom=[[f'{MONTHS[d.month-1]} {d.year}',int(n),int(w)]
                for d,n,w in zip(group['fecha'],group['entradas_new'],group['ganados_ventana'])]
        fig.add_trace(go.Scatter(
            x=[d.isoformat() for d in group['fecha']],
            y=[None if pd.isna(v) else float(v) for v in group['conversion_new_won_pct']],
            name=channel,mode='lines+markers',line={'color':colors.get(channel),'width':2.5},
            marker={'size':6},customdata=custom,connectgaps=False,
            hovertemplate=(f'<b>{channel}</b> · %{{customdata[0]}}'
                           '<br>Entraron a New: %{customdata[1]}'
                           f'<br>De ellos, Won en {ventana} días: %{{customdata[2]}}'
                           '<br>Conversión: %{y:.1f}%<extra></extra>')))
    values=positive['conversion_new_won_pct']
    low,high=float(values.min()),float(values.max())
    pad=max(2,(high-low)*.12)
    minimum=max(0,math.floor((low-pad)/5)*5)
    maximum=min(100,math.ceil((high+pad)/5)*5)
    dates=sorted(df['fecha'].unique())
    years=sorted(df['fecha'].dt.year.unique())
    period=str(years[0]) if len(years)==1 else f'{years[0]}–{years[-1]}'
    fig.update_layout(
        title={'text':f'New → Won en {ventana} días, por canal','font':{'size':22},'x':.04},
        template='plotly_white',height=420,margin={'l':65,'r':30,'t':55,'b':105},
        font={'family':'Arial, sans-serif','size':13,'color':'#243247'},
        xaxis={'title':f'Mes de entrada a New · {period}','type':'date','tickmode':'array',
               'tickvals':[pd.Timestamp(d).isoformat() for d in dates],
               'ticktext':[MONTHS[pd.Timestamp(d).month-1] for d in dates],
               'showgrid':False,'fixedrange':True},
        yaxis={'title':'New que llegó a Won (%)','range':[minimum,maximum],'tickmode':'linear',
               'tick0':minimum,'dtick':5,'ticksuffix':'%','fixedrange':True,
               'gridcolor':'#edf1f5','zeroline':False},
        legend={'orientation':'h','x':0,'y':-.3,'xanchor':'left','yanchor':'top'},
        hovermode='closest',dragmode=False)
    return fig
