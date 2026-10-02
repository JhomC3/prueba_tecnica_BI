"""Localizar transiciones y acotar el análisis a cuentas que entraron por New."""
from pathlib import Path
from contextlib import closing
import sqlite3
import json
import pandas as pd
from scripts.cro_demo import Median,P90
from scripts.cro_analysis import STAGES,NEXT,stage_lines,trend,long_series,mature,check_ratio


def stages_for_new(folder):
    folder=Path(folder)
    root=Path(__file__).resolve().parents[1]
    cutoff=json.loads((root/'resultados/cro/manifest.json').read_text())['config']['cutoff']
    text=(root/'sql/cro/completas.sql').read_text()
    sql=text.split('-- @consulta etapas\n',1)[1].split('-- @consulta perdidas',1)[0]
    sql=sql.replace("e.id_etapa<>'Won'","e.id_etapa<>'Won' AND c.tipo_entrada='New'")
    database=root/'datos/bases/cro'/folder.name/'modelo.sqlite'
    frames=[]
    with closing(sqlite3.connect(f'file:{database}?mode=ro',uri=True)) as connection:
        connection.create_aggregate('mediana',1,Median)
        connection.create_aggregate('p90',1,P90)
        for dim,segment in [('total',"'Todos'"),('canal','c.canal')]:
            frame=pd.read_sql_query(sql.replace('__SEGMENTO__',segment),connection,params={'corte':cutoff})
            frame['dimension']=dim
            frames.append(frame)
    return pd.concat(frames,ignore_index=True)


def analyze_stage_focus(folder,month_of_increase,focus_limit=2):
    data=stages_for_new(folder)
    baseline=(pd.Period(month_of_increase,freq='M')-1).strftime('%Y-%m')
    data=data.loc[data['ventana'].eq(30)&data['mes'].ge(baseline)].copy()
    total=mature(data.loc[data['dimension'].eq('total')],'cuentas_entrada','mes')
    channels=mature(data.loc[data['dimension'].eq('canal')],'cuentas_entrada','mes')
    check_ratio(total,'conversion_pct','avances_siguiente','elegibles')
    check_ratio(channels,'conversion_pct','avances_siguiente','elegibles')
    table=total.pivot(index='etapa',columns='mes',values='conversion_pct')
    if baseline not in table or month_of_increase not in table:
        raise ValueError('Faltan meses comparables para localizar etapas')
    drops=(table[month_of_increase]-table[baseline]).dropna().sort_values()
    focus=drops.loc[drops.lt(0)].head(focus_limit).index.tolist()
    months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    label=lambda date:months[pd.Period(date,freq='M').month-1]
    fmt=lambda value:f'{value:.1f}'.replace('.',',')
    lines=[]
    for stage in STAGES:
        if stage not in focus:
            continue
        old=table.loc[stage,baseline];new=table.loc[stage,month_of_increase]
        lines.append(f'• {stage} → {NEXT[stage]}: {fmt(old)}% → {fmt(new)}%.')
    conclusion=(f'De {label(baseline)} a {label(month_of_increase)}:\n\n'+'\n'.join(lines))
    if focus:
        conclusion+='\n\nPriorizamos las mayores caídas. Las demás etapas quedan fuera del siguiente análisis.'
    else:
        conclusion+='\n\nNo se identificaron caídas en esta comparación; revisar otras explicaciones antes de fijar un foco.'
    bundles=[]
    for stage in focus:
        subset=channels.loc[channels['etapa'].eq(stage)]
        fig=trend(long_series(subset,'mes',{'conversion_pct':'Conversión'},group='segmento'),
            f'{stage} → {NEXT[stage]} por canal','%','Mes de entrada')
        rows=[]
        for channel,group in subset.groupby('segmento',sort=True):
            values=group.set_index('mes')['conversion_pct']
            if baseline in values and month_of_increase in values:
                rows.append(f'{channel}: {fmt(values[baseline])}% → {fmt(values[month_of_increase])}%')
        reading='; '.join(rows)+'.'
        after=total.loc[total['etapa'].eq(stage)&total['mes'].ge(month_of_increase)]
        if after['conversion_pct'].lt(table.loc[stage,baseline]).all():
            reading+=' El global se mantuvo por debajo de '+label(baseline)+' en todos los meses posteriores.'
        else:
            reading+=' La evolución posterior incluye recuperaciones; la caída no fue continua.'
        reading+=' Investigamos atención y tiempos en esta transición; todavía no conocemos la causa.'
        bundles.append({'stage':stage,'figure':fig,'reading':reading})
    return {'global_figure':stage_lines(total),'global_reading':conclusion,'focus':focus,
            'focused':bundles,'metrics':data,'baseline':baseline}
