"""Conclusiones descriptivas reproducibles sobre métricas guardadas."""
import pandas as pd

MONTHS=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']


def conclusion_new(csv_path):
    df=pd.read_csv(csv_path)
    df=df.loc[df['dimension'].eq('total')].copy()
    df['fecha']=pd.to_datetime(df['mes'],format='%Y-%m')
    df=df.sort_values('fecha').reset_index(drop=True)
    if df.empty or df['mes'].duplicated().any():
        raise ValueError('Se requiere una serie mensual única')
    positive=df.loc[df['crecimiento_new_pct'].gt(0)]
    if positive.empty:
        text=('No se registraron aumentos en las comparaciones mensuales disponibles.'
              if df['crecimiento_new_pct'].notna().any() else
              'No hay comparaciones mensuales calculables para concluir si New aumentó.')
        return {'texto':text,'criterio':'Solo variaciones mensuales calculables; no inferir causas.'}
    selected=positive.loc[positive['crecimiento_new_pct'].idxmax()]
    month=MONTHS[selected['fecha'].month-1]
    before=MONTHS[(selected['fecha'].month-2)%12]
    change=f"{selected['crecimiento_new_pct']:.1f}".replace('.',',')
    text=(f"El mayor aumento mensual de New ocurrió entre {before} y {month}: "
          f"pasó de {int(selected['new_anterior'])} a {int(selected['entradas_new'])} entradas (+{change}%).")
    later=df.loc[df['fecha']>=selected['fecha']]
    if len(later)>1:
        end=MONTHS[later.iloc[-1]['fecha'].month-1]
        text+=f" Entre {month} y {end}, las entradas oscilaron entre {int(later['entradas_new'].min())} y {int(later['entradas_new'].max())} por mes."
    return {'texto':text,'criterio':'Mayor variación mensual positiva y rango observado desde ese mes; no atribuye causas.',
            'evidencia':{'mes':selected['mes'],'anterior':int(selected['new_anterior']),
                         'actual':int(selected['entradas_new']),'variacion_pct':float(selected['crecimiento_new_pct']),
                         'minimo_posterior':int(later['entradas_new'].min()),'maximo_posterior':int(later['entradas_new'].max())}}


def conclusion_new_por_canal(csv_path):
    base=conclusion_new(csv_path)
    if 'evidencia' not in base:
        return {'texto':base['texto']}
    df=pd.read_csv(csv_path)
    month=base['evidencia']['mes']
    series=df.loc[df['dimension'].eq('canal')].sort_values('mes').copy()
    if series.duplicated(['mes','segmento']).any():
        raise ValueError('Se requiere una serie mensual única por canal')
    channels=series.loc[series['mes'].eq(month)].copy()
    if channels.empty or channels['new_anterior'].isna().any():
        return {'texto':'No hay comparación completa por canal para ese mes.'}
    # Comprobar cobertura antes de contextualizar: ninguna fecha/canal omitido.
    totals=df.loc[df['dimension'].eq('total')].set_index('mes')['entradas_new']
    expected=pd.MultiIndex.from_product([totals.index,series['segmento'].unique()])
    observed=pd.MultiIndex.from_frame(series[['mes','segmento']])
    if set(expected)!=set(observed):
        raise ValueError('Faltan meses o canales para contextualizar la serie completa')
    sums=series.groupby('mes')['entradas_new'].sum().reindex(totals.index)
    if not sums.eq(totals).all():
        raise ValueError('La serie por canales no concilia con el total')
    channels['aumento']=channels['entradas_new']-channels['new_anterior']
    total_delta=base['evidencia']['actual']-base['evidencia']['anterior']
    if int(channels['aumento'].sum())!=total_delta:
        raise ValueError('El incremento por canales no concilia con el total')
    top=channels.loc[channels['aumento'].idxmax()]
    share=f"{100*top['aumento']/total_delta:.1f}".replace('.',',')
    date=pd.Timestamp(month+'-01')
    before=MONTHS[(date.month-2)%12]
    current=MONTHS[date.month-1]
    intro=(f"De {before} a {current}, {top['segmento']} aportó {int(top['aumento'])} "
           f"de las {total_delta} entradas adicionales ({share}%). El contexto por canal es:")
    paragraphs=[]
    evidence=[]
    for _, row in channels.sort_values('aumento',ascending=False).iterrows():
        history=series.loc[series['segmento'].eq(row['segmento'])]
        prior=history.loc[history['mes']<month]
        peak=prior.loc[prior['entradas_new'].idxmax()]
        peak_count=int(peak['entradas_new'])
        previous=int(row['new_anterior'])
        actual=int(row['entradas_new'])
        peak_month=MONTHS[pd.Timestamp(peak['mes']+'-01').month-1]
        def percent(value, baseline):
            if baseline==0:
                return 'porcentaje no calculable desde cero'
            return f"{100*(value/baseline-1):+.1f}%".replace('.',',')
        prefix=f"{row['segmento']}: "
        if previous<peak_count:
            prefix+=(f"había bajado de {peak_count} en {peak_month} a {previous} en {before} "
                     f"({percent(previous,peak_count)}). ")
        prefix+=(f"En {current} alcanzó {actual} ({percent(actual,previous)} frente a {before}; "
                 f"{percent(actual,peak_count)} frente al máximo previo de {peak_count}).")
        later=history.loc[history['mes']>month]
        if not later.empty:
            last=later.iloc[-1]
            end=MONTHS[pd.Timestamp(last['mes']+'-01').month-1]
            prefix+=(f" Después osciló entre {int(later['entradas_new'].min())} y "
                     f"{int(later['entradas_new'].max())}; terminó en {int(last['entradas_new'])} en {end}.")
            if (later['entradas_new']>peak_count).all():
                prefix+=' Todos esos meses superaron el máximo previo.'
            elif (later['entradas_new']<=peak_count).any():
                prefix+=' No permaneció por encima del máximo previo en todos esos meses.'
        paragraphs.append(prefix)
        evidence.append({'canal':str(row['segmento']),'maximo_previo':peak_count,
                         'mes_maximo_previo':peak['mes'],'anterior':previous,'actual':actual,
                         'serie':history[['mes','entradas_new']].to_dict('records')})
    if channels['aumento'].gt(0).all():
        changes='; '.join(
            f"{row['segmento']} +{float(row['crecimiento_new_pct']):.1f}%".replace('.',',')
            if pd.notna(row['crecimiento_new_pct']) else
            f"{row['segmento']} de {int(row['new_anterior'])} a {int(row['entradas_new'])}"
            for _, row in channels.iterrows())
        summary=(f"De {before} a {current}, las entradas a New aumentaron en todos los canales "
                 f"({changes}). Este aumento fue compartido; por ese criterio, "
                 "no hay motivo para excluir ningún canal del análisis de conversión.")
    else:
        increased=channels.loc[channels['aumento'].gt(0),'segmento'].astype(str).tolist()
        other=channels.loc[channels['aumento'].le(0),'segmento'].astype(str).tolist()
        summary=(f"De {before} a {current}, New aumentó en {', '.join(increased) or 'ningún canal'}; "
                 f"no aumentó en {', '.join(other)}. "
                 "El aumento de captación no fue compartido por todos los canales.")
    return {'texto':summary,'texto_detallado':intro+'\n\n'+'\n\n'.join(paragraphs),
            'criterio':'Salto mensual, máximo anterior y todos los meses posteriores; sin inferir causas ni tendencia sostenida.',
            'mes':month,'canal_principal':str(top['segmento']),'contexto':evidence,
            'detalle':channels[['segmento','new_anterior','entradas_new','aumento','crecimiento_new_pct']].to_dict('records')}


def conclusion_conversion(csv_path, ventana=30, mes_aumento=None):
    """Lectura de extremos y recuperaciones, sin inferir continuidad ni causas."""
    df=pd.read_csv(csv_path)
    df=df.loc[df['ventana'].eq(ventana) & df['dimension'].isin(['total','canal'])].copy()
    complete=df.groupby('mes_entrada')['elegibles'].sum().eq(
        df.groupby('mes_entrada')['entradas_new'].sum())
    df=df.loc[df['mes_entrada'].isin(complete[complete].index)]
    df=df.sort_values('mes_entrada')
    if df.empty or df.duplicated(['dimension','segmento','mes_entrada']).any():
        raise ValueError('La lectura requiere series completas y únicas')
    def point(row):
        month=MONTHS[pd.Timestamp(row['mes_entrada']+'-01').month-1]
        rate=f"{row['conversion_new_won_pct']:.1f}%".replace('.',',')
        return f'{rate} en {month}'
    paragraphs=[]
    evidence=[]
    groups=[('Global',df.loc[df['dimension'].eq('total')])]
    groups+=list(df.loc[df['dimension'].eq('canal')].groupby('segmento',sort=True))
    for label,group in groups:
        group=group.loc[group['conversion_new_won_pct'].notna()].copy()
        if group.empty:
            continue
        peak=group.loc[group['conversion_new_won_pct'].idxmax()]
        low=group.loc[group['conversion_new_won_pct'].idxmin()]
        last=group.iloc[-1]
        before=group.loc[group['mes_entrada']<peak['mes_entrada']]
        after_peak=group.loc[group['mes_entrada']>peak['mes_entrada']]
        if group['conversion_new_won_pct'].nunique()==1:
            text=f"{label}: conversión constante de {point(last)}."
        else:
            text=f"{label}: máximo de {point(peak)}."
            if not before.empty:
                earlier_low=before.loc[before['conversion_new_won_pct'].idxmin()]
                text+=f" Antes había registrado {point(earlier_low)}."
            if not after_peak.empty:
                later_low=after_peak.loc[after_peak['conversion_new_won_pct'].idxmin()]
                text+=f" Después bajó hasta {point(later_low)}."
                recovery=group.loc[group['mes_entrada']>later_low['mes_entrada']]
                if not recovery.empty:
                    rebound=recovery.loc[recovery['conversion_new_won_pct'].idxmax()]
                    text+=f" Recuperó hasta {point(rebound)}."
                    if rebound['mes_entrada']!=last['mes_entrada']:
                        text+=f" Terminó en {point(last)}."
        paragraphs.append(text)
        evidence.append({'serie':label,'valores':group[['mes_entrada','entradas_new','ganados_ventana','conversion_new_won_pct']].to_dict('records')})
    paragraphs.append('Las caídas no son continuas ni iguales entre canales. El siguiente paso es localizar las transiciones afectadas y comprobar si hay menos conversión final o más demora.')
    detailed='\n\n'.join(paragraphs)
    text=detailed
    if mes_aumento is not None:
        total=df.loc[df['dimension'].eq('total')].sort_values('mes_entrada')
        previous_month=(pd.Period(mes_aumento,freq='M')-1).strftime('%Y-%m')
        selected=total.loc[total['mes_entrada'].eq(mes_aumento)]
        previous=total.loc[total['mes_entrada'].eq(previous_month)]
        if selected.empty or previous.empty:
            raise ValueError('Falta un periodo comparable para el mes del aumento de New')
        old=float(previous.iloc[0]['conversion_new_won_pct'])
        new=float(selected.iloc[0]['conversion_new_won_pct'])
        old_label=MONTHS[pd.Timestamp(previous_month+'-01').month-1]
        new_label=MONTHS[pd.Timestamp(mes_aumento+'-01').month-1]
        direction='bajó' if new<old else 'subió' if new>old else 'se mantuvo'
        rate=lambda value:f'{value:.1f}%'.replace('.',',')
        changes=[]
        for channel,group in df.loc[df['dimension'].eq('canal')].groupby('segmento',sort=True):
            a=group.loc[group['mes_entrada'].eq(previous_month)]
            b=group.loc[group['mes_entrada'].eq(mes_aumento)]
            if not a.empty and not b.empty:
                x=float(a.iloc[0]['conversion_new_won_pct']);y=float(b.iloc[0]['conversion_new_won_pct'])
                changes.append(f'{channel}: {rate(x)} → {rate(y)}')
        later=total.loc[total['mes_entrada']>mes_aumento]
        followup=''
        if not later.empty:
            if new<old and later['conversion_new_won_pct'].lt(old).all():
                followup=' En los meses posteriores hubo variaciones, pero la conversión global permaneció por debajo de '+old_label+'.'
            else:
                followup=' La evolución posterior varía; la comparación de estos dos meses no demuestra una caída continua.'
        text=(f'De {old_label} a {new_label}, la conversión New → Won en {ventana} días {direction} de {rate(old)} a {rate(new)}. '
              +'; '.join(changes)+'.'+followup+'\n\n'
              +'Revisamos las etapas en todos los canales, manteniendo el desglose para localizar dónde cambió la conversión.')
    return {'texto':text,'texto_detallado':detailed,'evidencia':evidence,'ventana':ventana}
