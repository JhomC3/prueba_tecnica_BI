"""Gráficas y lecturas CRO para notebook y futura web, desde métricas revisables.

No modifica fuentes. Ratios agregados se reconstruyen desde numerador/denominador;
las medianas y P90 se leen del SQL a su grano original, nunca se promedian.
"""
from pathlib import Path
import math
import sqlite3
from contextlib import closing
import pandas as pd
import plotly.graph_objects as go
from scripts.cro_charts import CONFIG, MONTHS

STAGES=['New','Working','Engaged','SQL','Demo','Proposal']
NEXT=dict(zip(STAGES,['Working','Engaged','SQL','Demo','Proposal','Won']))
COLORS={'Marketing pago':'#2563eb','Orgánico':'#0d9488','Referidos':'#c76a12',
        'New':'#2563eb','SQL':'#0d9488','Producto':'#c76a12',
        '30 días':'#2563eb','60 días':'#0d9488','90 días':'#c76a12'}
PALETTE=['#2563eb','#0d9488','#c76a12','#64748b','#9333ea']
FULL_MONTHS=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']


def load(folder,name,dimension='total',**filters):
    df=pd.read_csv(Path(folder)/f'{name}.csv')
    df=df.loc[df.dimension.eq(dimension)].copy()
    for key,value in filters.items():
        df=df.loc[df[key].eq(value)]
    if df.empty:
        raise ValueError(f'Sin registros: {name}, {dimension}, {filters}')
    return df


def mature(df,total_column,date_column):
    """Omitir meses completos si cualquier grupo no tiene la ventana completa."""
    complete=df.groupby(date_column)['elegibles'].sum().eq(df.groupby(date_column)[total_column].sum())
    return df.loc[df[date_column].isin(complete[complete].index)].copy()


def weighted_rate(df,keys,numerator,denominator,output):
    out=df.groupby(keys,as_index=False)[[numerator,denominator]].sum()
    out[output]=100*out[numerator]/out[denominator].replace(0,float('nan'))
    return out


def check_ratio(df,column,numerator,denominator):
    expected=100*df[numerator]/df[denominator].replace(0,float('nan'))
    valid=expected.notna()
    if not df.loc[valid,column].sub(expected[valid]).abs().lt(1e-7).all():
        raise ValueError(f'No concilia {column} = {numerator}/{denominator}')
    if df.loc[~valid,column].notna().any():
        raise ValueError(f'{column}: denominador cero debe quedar sin resultado')


def long_series(df,date,metrics,group=None,selector=None):
    """Una fila por punto; conserva filtros y bases en columnas de hover."""
    rows=[]
    for column,label in metrics.items():
        for _,r in df.iterrows():
            row={'mes':r[date],'serie':str(r[group]) if group else label,
                 'valor':r[column],'selector':str(r[selector]) if selector else 'Todos'}
            bases={
                'conversion_pct':('avances_siguiente','elegibles','Avances','Entradas seguidas'),
                'conversion_new_won_pct':('ganados_ventana','elegibles','Won en el plazo','Entradas a New'),
                'conversion_pago_pct':('nuevos_pagadores_ventana','elegibles','Primeros pagos','Captados sin pago previo'),
                'calidad_pct':('calificados','evaluados','Calificados','Evaluados'),
                'cobertura_evaluacion_pct':('evaluados','prospectos','Evaluados','Prospectos'),
                'cobertura_intento_pct':('visitas_con_intento','visitas','Con intento','Visitas'),
                'contacto_efectivo_pct':('visitas_contacto_efectivo','visitas_con_intento','Contacto efectivo','Con intento'),
                'puntualidad_pct':('atendidos_en_plazo','elegibles_plazo','Atendidos en plazo','Visitas con seguimiento'),
                'perdida_pct':('perdidos','elegibles','Perdidos','Entradas seguidas'),
                'sin_avance_pct':('sin_avance_ventana','elegibles','Sin avance','Entradas seguidas'),
                'abiertos_corte_pct':('abiertos_corte','cuentas_entrada','Abiertos al corte','Entradas')}
            num,den,num_label,den_label=bases.get(column,('','',label,''))
            row['base']=r.get(den,float('nan'));row['casos']=r.get(num,float('nan'))
            row['numerador']=num_label;row['denominador']=den_label
            rows.append(row)
    return pd.DataFrame(rows)


def trend(data,title,unit,date_label='Mes',selector_labels=None,range_fixed=None):
    """Una figura por unidad. Selectores de etapa cambian solo la serie visible."""
    if data.empty:
        raise ValueError(f'Figura sin registros: {title}')
    if data.duplicated(['mes','serie','selector']).any():
        raise ValueError(f'Puntos repetidos en {title}')
    data=data.copy()
    data['fecha']=pd.to_datetime(data.mes,format='%Y-%m')
    options=list(data.selector.unique())
    if selector_labels:
        options=[k for k in selector_labels if k in options]
    valid_options=[k for k in options if data.loc[data.selector.eq(k),'valor'].notna().any()]
    active=valid_options[0] if valid_options else options[0]
    fig=go.Figure(); trace_selectors=[]
    for option in options:
        subset=data.loc[data.selector.eq(option)]
        for number,(series,group) in enumerate(subset.groupby('serie',sort=False)):
            group=group.sort_values('fecha')
            custom=[]
            for _,r in group.iterrows():
                d=r.fecha
                custom.append([f'{MONTHS[d.month-1]} {d.year}',
                               '—' if pd.isna(r.base) else str(int(r.base)),
                               '—' if pd.isna(r.casos) else str(int(r.casos)),r.denominador,r.numerador])
            hover=f'<b>{series}</b> · %{{customdata[0]}}<br>%{{y:.1f}} {unit}'
            if unit=='%':
                hover+='<br>%{customdata[3]}: %{customdata[1]}<br>%{customdata[4]}: %{customdata[2]}'
            fig.add_trace(go.Scatter(
                x=[d.isoformat() for d in group.fecha],
                y=[None if pd.isna(v) else float(v) for v in group.valor],name=series,
                mode='lines+markers',visible=option==active,connectgaps=False,
                line={'color':COLORS.get(series,PALETTE[number%len(PALETTE)]),'width':2.5,
                      'dash':'dot' if 'P90' in series else 'solid'},marker={'size':6},
                customdata=custom,hovertemplate=hover+'<extra></extra>'))
            trace_selectors.append(option)
    dates=sorted(data.fecha.unique());years=sorted(data.fecha.dt.year.unique())
    period=str(years[0]) if len(years)==1 else f'{years[0]}–{years[-1]}'
    # Misma escala entre opciones: el selector no exagera cambios entre etapas.
    values=data.valor.dropna()
    if range_fixed is not None:
        limits=range_fixed
    elif len(values):
        low,high=float(values.min()),float(values.max())
        step=5 if unit=='%' else (20 if high>100 else (5 if high>10 else 1))
        pad=max(step*.6,(high-low)*.12)
        limits=[max(0,math.floor((low-pad)/step)*step),math.ceil((high+pad)/step)*step]
        if unit=='%': limits[1]=min(100,limits[1])
        if limits[0]==limits[1]: limits[1]+=step
    else:
        limits=[0,1]
    multiple=data.serie.nunique()>1
    menus=[]
    current_title=title
    if len(options)>1:
        labels=selector_labels or {k:k for k in options}
        current_title=title
        buttons=[{'label':labels[k],'method':'update','args':[
            {'visible':[v==k for v in trace_selectors]},
            {'title':{'text':title,'font':{'size':20},'x':.04}}]} for k in options]
        menus=[{'buttons':buttons,'direction':'down','x':0,'y':1.18,'xanchor':'left','yanchor':'top','showactive':True}]
    fig.update_layout(
        title={'text':current_title,'font':{'size':20},'x':.04},template='plotly_white',
        height=440 if len(options)>1 or multiple else 390,
        margin={'l':70,'r':35,'t':110 if len(options)>1 else 65,'b':105 if multiple else 60},
        font={'family':'Arial, sans-serif','size':14,'color':'#243247'},
        xaxis={'title':f'{date_label} · {period}','type':'date','tickmode':'array',
               'tickvals':[pd.Timestamp(d).isoformat() for d in dates],
               'ticktext':[MONTHS[pd.Timestamp(d).month-1] for d in dates],'showgrid':False,'fixedrange':True},
        yaxis={'title':unit if unit!='%' else 'Porcentaje','range':limits,
               'ticksuffix':'%' if unit=='%' else '', 'fixedrange':True,
               'gridcolor':'#edf1f5','zeroline':False},
        showlegend=multiple,legend={'orientation':'h','x':0,'y':-.3,'yanchor':'top'},
        updatemenus=menus,hovermode='closest',dragmode=False)
    return fig


def bars(df,category,value,title,unit,group=None):
    fig=go.Figure()
    categories=df[category].drop_duplicates().tolist()
    groups=list(df.groupby(group,sort=True)) if group else [(value,df)]
    for i,(label,g) in enumerate(groups):
        lookup=g.set_index(category)[value]
        values=[None if c not in lookup or pd.isna(lookup[c]) else float(lookup[c]) for c in categories]
        fig.add_trace(go.Bar(x=categories,y=values,name=str(label),marker_color=COLORS.get(label,PALETTE[i%len(PALETTE)]),
                            hovertemplate='%{x}<br>%{y:.1f} '+unit+'<extra>%{fullData.name}</extra>'))
    fig.update_layout(title={'text':title,'font':{'size':21},'x':.04},template='plotly_white',height=440,
        margin={'l':70,'r':35,'t':65,'b':125},font={'family':'Arial, sans-serif','size':14,'color':'#243247'},
        yaxis={'title':unit,'gridcolor':'#edf1f5','zeroline':False},
        xaxis={'tickangle':-15,'fixedrange':True},barmode='group',showlegend=bool(group),
        legend={'orientation':'h','x':0,'y':-.4},dragmode=False)
    return fig


def describe(df,date,column,label):
    """Extremos y cierre de toda la serie, sin deducir causalidad."""
    d=df.loc[df[column].notna()].sort_values(date)
    if d.empty: return f'{label}: sin observaciones suficientes.'
    low=d.loc[d[column].idxmin()];high=d.loc[d[column].idxmax()];last=d.iloc[-1]
    def point(r):
        month=FULL_MONTHS[pd.Timestamp(str(r[date])+'-01').month-1]
        return f"{r[column]:.1f} en {month}".replace('.',',')
    return f'{label}: rango de {point(low)} a {point(high)}; cierre de {point(last)}.'


def stage_lines(data,by_channel=False):
    """Todas las transiciones en un único plano, identificadas en la leyenda."""
    data=data.copy()
    data['_serie']=data['etapa'].map(lambda stage:f'{stage} → {NEXT[stage]}')
    if by_channel:
        data['_serie']+=' · '+data['segmento']
    fig=trend(long_series(data,'mes',{'conversion_pct':'Conversión'},group='_serie'),
        'Conversión por etapa en 30 días'+(' por canal' if by_channel else ''),
        '%','Mes de entrada')
    channels=sorted(data['segmento'].unique())
    dashes=['solid','dash','dot']
    for trace in fig.data:
        stage=next(stage for stage in STAGES if trace.name.startswith(stage+' →'))
        trace.line.color=PALETTE[STAGES.index(stage)%len(PALETTE)]
        if by_channel:
            channel=trace.name.split(' · ',1)[1]
            trace.line.dash=dashes[channels.index(channel)%len(dashes)]
    fig.update_layout(height=660 if by_channel else 490,
        margin=dict(l=70,r=35,t=65,b=235 if by_channel else 130),
        legend=dict(orientation='h',x=0,y=-.2,yanchor='top',font=dict(size=12)))
    return fig


def build_question(folder,question):
    folder=Path(folder);figures=[];notes=[];evidence=[]
    stage_labels={s:f'{s} → {NEXT[s]}' for s in STAGES}
    def read(name,dimension='total',**filters):
        d=load(folder,name,dimension,**filters)
        evidence.append({'fuente':str(folder/f'{name}.csv'),'dimension':dimension,'filtros':filters,'filas':len(d)})
        return d
    def plot(d,date,metrics,title,unit,group=None,selector=None,labels=None,fixed=None):
        figures.append(trend(long_series(d,date,metrics,group,selector),title,unit,
                              'Mes de entrada' if date=='mes_entrada' else 'Mes',labels,fixed))
    if question==3:
        for dim in ['total','canal']:
            d=mature(read('etapas',dim,ventana=30),'cuentas_entrada','mes')
            check_ratio(d,'conversion_pct','avances_siguiente','elegibles')
            figures.append(stage_lines(d,by_channel=dim=='canal'))
        total=load(folder,'etapas','total',ventana=30)
        for stage in STAGES:
            g=mature(total[total.etapa.eq(stage)],'cuentas_entrada','mes')
            notes.append(describe(g,'mes','conversion_pct',stage_labels[stage]+' (%)'))
        notes.append('Una caída a 30 días puede reflejar demora. Comparar plazos mayores antes de atribuir pérdidas.')
    elif question==4:
        d=read('demanda');plot(d,'mes',{'entradas_marketing':'Captaciones de Marketing'},'Demanda de Marketing','Captaciones')
        c=read('demanda','canal');c=c[c.segmento.isin(['Marketing pago','Orgánico'])]
        plot(c,'mes',{'captados':'Captaciones'},'Demanda por canal de Marketing','Captaciones','segmento')
        campaigns=read('demanda','campana');campaigns=campaigns[campaigns.segmento.ne('No aplica')]
        plot(campaigns,'mes',{'entradas_marketing':'Captaciones'},'Demanda por campaña','Captaciones','segmento')
        notes.append(describe(d,'mes','entradas_marketing','Captaciones de Marketing'))
        for channel,g in c.groupby('segmento'): notes.append(describe(g,'mes','captados',channel))
    elif question==5:
        d=read('calidad');check_ratio(d,'calidad_pct','calificados','evaluados');check_ratio(d,'cobertura_evaluacion_pct','evaluados','prospectos')
        plot(d,'mes',{'calidad_pct':'Calificados entre evaluados'},'Prospectos que cumplen los criterios','%')
        coverage=d.rename(columns={'prospectos':'base','evaluados':'casos'})
        coverage['elegibles']=coverage.base;coverage['avances_siguiente']=coverage.casos
        plot(coverage,'mes',{'cobertura_evaluacion_pct':'Evaluados entre prospectos'},'Prospectos evaluados','%')
        c=read('calidad','canal');plot(c,'mes',{'calidad_pct':'Calificados'},'Calidad por canal','%','segmento')
        reasons=read('descalificaciones').groupby('motivo',as_index=False).descalificados.sum()
        reasons['motivo']=reasons.motivo.map({'fuera_perfil':'Fuera del perfil','sin_intencion':'Sin intención','sin_necesidad':'Sin necesidad'})
        figures.insert(2,bars(reasons,'motivo','descalificados','Motivos de descalificación','Prospectos'))
        notes.extend([describe(d,'mes','calidad_pct','Calificados entre evaluados (%)'),
                      describe(d,'mes','cobertura_evaluacion_pct','Evaluados (%)'),
                      'La definición v1 es ilustrativa. Una variación de evaluación no equivale por sí sola a peor calidad.'])
    elif question==6:
        labels={s:s for s in STAGES};d=read('atencion')
        plot(d,'mes',{'mediana_primer_intento':'Mediana','p90_primer_intento':'P90'},'Días hasta el primer intento de contacto','Días',selector='etapa',labels=labels)
        plot(d,'mes',{'mediana_espera_asignacion':'Mediana'},'Días hasta asignar un responsable','Días',selector='etapa',labels=labels)
        # Porcentajes con denominadores propios; selector evita mezclar conceptos.
        pieces=[]
        for col,label,num,den in [('cobertura_intento_pct','Con intento','visitas_con_intento','visitas'),
                                   ('contacto_efectivo_pct','Contacto efectivo','visitas_contacto_efectivo','visitas_con_intento'),
                                   ('puntualidad_pct','Atendidos en 2 días','atendidos_en_plazo','elegibles_plazo')]:
            check_ratio(d,col,num,den)
            part=d.copy();part['elegibles']=part[den];part['avances_siguiente']=part[num]
            long=long_series(part,'mes',{col:label},selector='etapa');pieces.append(long)
        figures.append(trend(pd.concat(pieces,ignore_index=True),'Atención y seguimiento','%',selector_labels=labels))
        c=read('atencion','canal');plot(c,'mes',{'mediana_primer_intento':'Mediana'},'Días hasta primer intento por canal','Días','segmento','etapa',labels)
        weighted=weighted_rate(d,['mes'],'visitas_con_intento','visitas','pct')
        notes.append(describe(weighted,'mes','pct','Visitas con intento de contacto (%)'))
        notes.append('El plazo de 2 días es ilustrativo. Los tiempos solo incluyen visitas con intento registrado; las no atendidas quedan en el porcentaje de cobertura.')
    elif question==7:
        labels={s:stage_labels[s] for s in STAGES[3:]}
        for dim in ['total','canal']:
            d=mature(read('etapas',dim,ventana=30),'cuentas_entrada','mes');d=d[d.etapa.isin(labels)]
            if dim=='total':
                plot(d,'mes',{'conversion_pct':'Avance siguiente'},'Conversión después de SQL en 30 días','%',selector='etapa',labels=labels)
                plot(d,'mes',{'perdida_pct':'Perdidos','sin_avance_pct':'Sin avance en el plazo'},'Pérdidas y casos sin avance en 30 días','%',selector='etapa',labels=labels)
                for stage in labels: notes.append(describe(d[d.etapa.eq(stage)],'mes','conversion_pct',labels[stage]+' (%)'))
            else:
                plot(d,'mes',{'conversion_pct':'Avance siguiente'},'Conversión después de SQL por canal','%','segmento','etapa',labels)
        notes.append('Los saltos a otras etapas se contabilizan aparte; no se consideran pérdidas.')
    elif question==8:
        d=read('resultado_global');plot(d,'mes',{'cierres_won':'Won','nuevos_pagadores':'Nuevos pagadores'},'Cierres y nuevos pagadores','Cuentas')
        for name,col,title,date in [('demanda','captados','Captaciones por tipo de entrada','mes'),
                                    ('pagadores','nuevos_pagadores','Nuevos pagadores por tipo de entrada','mes_pago')]:
            c=read(name,'tipo_entrada');plot(c,date,{col:'Cuentas'},title,'Cuentas','segmento')
        cierres=read('resultado_global','tipo_entrada')
        plot(cierres,'mes',{'cierres_won':'Won'},'Cierres Won por tipo de entrada','Cuentas','segmento')
        c=mature(read('captacion_pago','tipo_entrada',ventana=30),'captados_sin_pago_previo','mes_entrada')
        check_ratio(c,'conversion_pago_pct','nuevos_pagadores_ventana','elegibles')
        plot(c,'mes_entrada',{'conversion_pago_pct':'Primer pago'},'Conversión a primer pago en 30 días','%','segmento')
        totals=load(folder,'pagadores','tipo_entrada').groupby('segmento').nuevos_pagadores.sum()
        notes.append('Nuevos pagadores en el periodo: '+', '.join(f'{k}: {int(v)}' for k,v in totals.items())+'.')
        notes.append('Los pagos desde producto pueden ocurrir sin Won comercial. El conteo de cierres no sustituye el de pagadores.')
    elif question==9:
        d=read('etapas',ventana=30);labels={s:s for s in STAGES}
        plot(d,'mes',{'mediana_permanencia':'Mediana','p90_permanencia':'P90'},'Días en la etapa entre casos terminados','Días',selector='etapa',labels=labels)
        plot(d,'mes',{'abiertos_corte_pct':'Abiertos al corte'},'Casos abiertos por etapa','%',selector='etapa',labels=labels)
        opened=d.loc[d.abiertos_corte.gt(0)].copy()
        if not opened.empty:
            plot(opened,'mes',{'mediana_antiguedad_abiertos':'Mediana','p90_antiguedad_abiertos':'P90'},'Días acumulados de los casos abiertos','Días',selector='etapa',labels=labels)
        c=read('etapas','canal',ventana=30)
        plot(c,'mes',{'mediana_permanencia':'Mediana'},'Permanencia de casos terminados por canal','Días','segmento','etapa',labels)
        notes.append(f"Registros de cuenta-etapa abiertos al corte: {int(d.abiertos_corte.sum())}. Una cuenta puede aparecer en más de una etapa.")
        notes.append('La permanencia de terminados y la antigüedad de abiertos son poblaciones diferentes; no se mezclan sus medianas.')
    elif question==10:
        pieces=[]
        for window in [30,60,90]:
            d=mature(read('cohortes',ventana=window),'entradas_new','mes_entrada')
            check_ratio(d,'conversion_new_won_pct','ganados_ventana','elegibles')
            pieces.append(long_series(d,'mes_entrada',{'conversion_new_won_pct':f'{window} días'}))
        figures.append(trend(pd.concat(pieces,ignore_index=True),'New que llegó a Won según el plazo','%','Mes de entrada a New'))
        d=read('cohortes',ventana=30)
        plot(d,'mes_entrada',{'mediana_dias_new_won':'Mediana','p90_dias_new_won':'P90'},'Tiempo de New a Won entre ganados','Días')
        c=read('cohortes','canal');pieces=[]
        for window in [30,60,90]:
            part=mature(c[c.ventana.eq(window)],'entradas_new','mes_entrada').copy()
            part['plazo']=str(window)+' días'
            pieces.append(long_series(part,'mes_entrada',{'conversion_new_won_pct':'Conversión'},'segmento','plazo'))
        figures.append(trend(pd.concat(pieces,ignore_index=True),'New que llegó a Won por canal','%','Mes de entrada a New',
                             {f'{v} días':f'{v} días' for v in [30,60,90]}))
        # Consulta revisable sobre la misma SQLite: origen de cierres solo de New.
        scenario=folder.name;root=Path(__file__).resolve().parents[1]
        db=root/'datos/bases/cro'/scenario/'modelo.sqlite'
        with closing(sqlite3.connect(f'file:{db}?mode=ro',uri=True)) as con:
            origin=pd.read_sql_query("SELECT substr(fecha_entrada_inicial,1,7) mes_entrada, substr(fecha_won,1,7) mes_cierre, count(*) ganados FROM vw_ganados WHERE tipo_entrada='New' GROUP BY 1,2",con)
        evidence.append({'fuente':str(db),'consulta':'vw_ganados, tipo_entrada=New, meses de entrada y cierre','filas':len(origin)})
        matrix=origin.pivot(index='mes_entrada',columns='mes_cierre',values='ganados').fillna(0)
        heat=go.Figure(go.Heatmap(x=matrix.columns.tolist(),y=matrix.index.tolist(),z=matrix.to_numpy().tolist(),
            colorscale='Blues',hovertemplate='Entrada a New: %{y}<br>Cierre Won: %{x}<br>Cuentas: %{z}<extra></extra>',colorbar={'title':'Won'}))
        heat.update_layout(title={'text':'¿De qué mes de New vienen los cierres?','font':{'size':21},'x':.04},
            template='plotly_white',height=440,margin={'l':85,'r':60,'t':65,'b':65},
            font={'family':'Arial, sans-serif','size':14},xaxis={'title':'Mes de cierre','type':'category'},
            yaxis={'title':'Mes de entrada a New','type':'category','autorange':'reversed'},dragmode=False)
        figures.insert(2,heat)
        common=mature(load(folder,'cohortes',ventana=90),'entradas_new','mes_entrada').mes_entrada
        cohort=load(folder,'cohortes');cohort=cohort[cohort.mes_entrada.isin(common)]
        aggregate=weighted_rate(cohort,['ventana'],'ganados_ventana','elegibles','pct')
        notes.append('En los meses con 90 días completos, conversión ponderada: '+', '.join(f"{int(r.ventana)} días: {r.pct:.1f}%".replace('.',',') for _,r in aggregate.iterrows())+'.')
        notes.append('Las curvas a 60 y 90 días omiten meses que todavía no completan esos plazos. Comparar solo meses comunes; duración calculada entre ganados.')
    elif question==11:
        d=read('prioridad');d['transicion']=d.etapa.map(stage_labels)
        d['etapa']=pd.Categorical(d.etapa,STAGES,ordered=True);d=d.sort_values('etapa')
        figures.append(bars(d,'transicion','avances_brecha_ilustrativa','Avances asociados a la brecha de conversión','Avances estimados'))
        figures.append(bars(d,'transicion','brecha_pp','Cambio de conversión frente al periodo base','Puntos porcentuales'))
        c=read('prioridad','canal');c['transicion']=c.etapa.map(stage_labels)
        c['etapa']=pd.Categorical(c.etapa,STAGES,ordered=True);c=c.sort_values('etapa')
        figures.append(bars(c,'transicion','avances_brecha_ilustrativa','Brecha de avances por canal','Avances estimados','segmento'))
        top=d.loc[d.avances_brecha_ilustrativa.idxmax()]
        if top.avances_brecha_ilustrativa>0:
            estimate=f'{top.avances_brecha_ilustrativa:.1f}'.replace('.',',')
            gap=f'{top.brecha_pp:+.1f}'.replace('.',',')
            notes.append(f'Mayor brecha ilustrativa: {top.transicion}, {estimate} avances; cambio de {gap} puntos porcentuales.')
        else: notes.append('No se observa una brecha negativa de conversión en esta comparación.')
        notes.append('Comparación enero–abril frente a mayo–agosto. Los avances estimados no se suman entre etapas ni equivalen a nuevos pagadores; el impacto debe comprobarse.')
    else:
        raise ValueError(f'Pregunta no implementada: {question}')
    return {'figures':figures,'reading':'\n\n'.join(notes),'evidence':evidence,'question':question}
