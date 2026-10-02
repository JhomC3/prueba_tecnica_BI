"""Diagnóstico acotado a los focos y periodos seleccionados en 3.4."""
from pathlib import Path
from contextlib import closing
import sqlite3
import json
import pandas as pd
from scripts.cro_demo import Median,P90
from scripts.cro_stage_focus import stages_for_new
from scripts.cro_analysis import NEXT,trend,long_series,check_ratio

MONTHS=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']


def fmt(value):
    return 'sin medición' if pd.isna(value) else f'{value:.1f}'.replace('.',',')


def attention_for_new(folder):
    root=Path(__file__).resolve().parents[1]
    cutoff=json.loads((root/'resultados/cro/manifest.json').read_text())['config']['cutoff']
    text=(root/'sql/cro/completas.sql').read_text()
    sql=text.split('-- @consulta atencion\n',1)[1].split('-- @consulta etapas',1)[0]
    sql=sql.replace("f.id_etapa<>'Won'","f.id_etapa<>'Won' AND c.tipo_entrada='New'")
    path=root/'datos/bases/cro'/Path(folder).name/'modelo.sqlite'
    frames=[]
    with closing(sqlite3.connect(f'file:{path}?mode=ro',uri=True)) as connection:
        connection.create_aggregate('mediana',1,Median);connection.create_aggregate('p90',1,P90)
        for dimension,segment in [('total',"'Todos'"),('canal','c.canal')]:
            frame=pd.read_sql_query(sql.replace('__SEGMENTO__',segment),connection,
                                   params={'corte':cutoff,'plazo':2})
            frame['dimension']=dimension;frames.append(frame)
    return pd.concat(frames,ignore_index=True)


def focused_diagnosis(folder,focus_result,month_of_increase):
    focus=focus_result['focus'];baseline=focus_result['baseline']
    end=focus_result['metrics'].loc[
        focus_result['metrics']['elegibles'].eq(focus_result['metrics']['cuentas_entrada']),'mes'].max()
    attention=attention_for_new(folder)
    stages=stages_for_new(folder)
    def narrow(data):
        return data.loc[data['etapa'].isin(focus)&data['mes'].between(baseline,end)].copy()
    attention=narrow(attention);stages=narrow(stages)
    attention_blocks=[];duration_blocks=[];window_blocks=[];findings=[]
    def pair(data,column):
        table=data.set_index('mes')
        if baseline not in table.index or month_of_increase not in table.index:
            return float('nan'),float('nan')
        return table.loc[baseline,column],table.loc[month_of_increase,column]
    comparison=f'{MONTHS[pd.Period(baseline).month-1]} → {MONTHS[pd.Period(month_of_increase).month-1]}'
    for stage in focus:
        label=f'{stage} → {NEXT[stage]}'
        a=attention.loc[attention['etapa'].eq(stage)]
        total=a.loc[a['dimension'].eq('total')]
        channels=a.loc[a['dimension'].eq('canal')]
        check_ratio(total,'cobertura_intento_pct','visitas_con_intento','visitas')
        old_time,new_time=pair(total,'mediana_primer_intento')
        old_coverage,new_coverage=pair(total,'cobertura_intento_pct')
        reading=(f'{comparison}: el primer intento pasó de {fmt(old_time)} a {fmt(new_time)} días; '
                 f'las visitas con intento, de {fmt(old_coverage)}% a {fmt(new_coverage)}%. ')
        if pd.isna(old_time) or pd.isna(new_time):
            reading+='No hay tiempos comparables; revisar el registro de atención.'
        elif new_time>old_time:
            reading+='La atención se demoró más; investigamos ese cambio, sin atribuirle todavía la caída.'
        else:
            reading+='El tiempo no aumentó en esta comparación; revisamos duración y cierre de la etapa.'
        attention_blocks.append({'stage':stage,'figure':trend(long_series(total,'mes',
            {'mediana_primer_intento':'Mediana'}),f'{label}: tiempo hasta el primer intento','Días','Mes de entrada'),
            'reading':reading})
        channel_lines=[]
        slower_channels=[]
        for channel,group in channels.groupby('segmento',sort=True):
            old,new=pair(group,'mediana_primer_intento')
            channel_lines.append(f'{channel}: {fmt(old)} → {fmt(new)} días')
            if pd.notna(old) and pd.notna(new) and new>old:
                slower_channels.append(channel)
        next_attention=('Revisamos el seguimiento en '+', '.join(slower_channels)+'.'
                        if slower_channels else 'No aumentó el tiempo en los canales comparables; avanzamos al tiempo en la etapa.')
        attention_blocks.append({'stage':stage,'figure':trend(long_series(channels,'mes',
            {'mediana_primer_intento':'Mediana'},group='segmento'),f'{label}: primer intento por canal','Días','Mes de entrada'),
            'reading':'; '.join(channel_lines)+'. '+next_attention})
        d=stages.loc[stages['etapa'].eq(stage)&stages['ventana'].eq(30)&
                     stages['elegibles'].eq(stages['cuentas_entrada'])]
        dt=d.loc[d['dimension'].eq('total')]
        old_duration,new_duration=pair(dt,'mediana_permanencia')
        open_count=int(dt['abiertos_corte'].sum())
        duration_reading=(f'{comparison}: la mediana de permanencia entre estancias terminadas '
            f'pasó de {fmt(old_duration)} a {fmt(new_duration)} días. ')
        if open_count==0:
            duration_reading+='No quedan casos abiertos de estos meses al corte; no hay acumulación pendiente en esta población.'
        else:
            ages=dt.loc[dt['abiertos_corte'].gt(0),'mediana_antiguedad_abiertos'].dropna()
            duration_reading+=f'Quedan {open_count} casos abiertos al corte; revisar su antigüedad por mes.'
            if not ages.empty:
                duration_reading+=f' Las medianas de antigüedad van de {fmt(ages.min())} a {fmt(ages.max())} días.'
        duration_blocks.append({'stage':stage,'figure':trend(long_series(dt,'mes',
            {'mediana_permanencia':'Mediana','p90_permanencia':'P90'}),f'{label}: tiempo en la etapa','Días','Mes de entrada'),
            'reading':duration_reading+' Contrastamos ahora el avance con más tiempo de seguimiento.'})
        dc=d.loc[d['dimension'].eq('canal')]
        channel_lines=[]
        for channel,group in dc.groupby('segmento',sort=True):
            old,new=pair(group,'mediana_permanencia');channel_lines.append(f'{channel}: {fmt(old)} → {fmt(new)} días')
        duration_blocks.append({'stage':stage,'figure':trend(long_series(dc,'mes',
            {'mediana_permanencia':'Mediana'},group='segmento'),f'{label}: permanencia por canal','Días','Mes de entrada'),
            'reading':'; '.join(channel_lines)+'. Son tiempos de estancias terminadas, incluidos avances y pérdidas.'})
        w=stages.loc[stages['etapa'].eq(stage)&stages['dimension'].eq('total')]
        complete=w.groupby('mes').apply(lambda g:set(g['ventana'])=={30,60,90} and
            g['elegibles'].eq(g['cuentas_entrada']).all(),include_groups=False)
        w=w.loc[w['mes'].isin(complete.loc[complete].index)].copy()
        if not w.empty:
            check_ratio(w,'conversion_pct','avances_siguiente','elegibles')
            w['plazo']=w['ventana'].astype(str)+' días'
            fig=trend(long_series(w,'mes',{'conversion_pct':'Conversión'},group='plazo'),
                f'{label}: avance a 30, 60 y 90 días','%','Mes de entrada')
            fig.update_layout(hovermode='x unified')
            values=w.pivot(index='mes',columns='ventana',values='conversion_pct')
            if baseline in values.index and month_of_increase in values.index:
                before=values.loc[baseline,90];recent=values.loc[month_of_increase,90]
                same=values[30].sub(values[90]).abs().lt(1e-9).all()
                reading=(f'Con meses comparables ({w["mes"].min()} a {w["mes"].max()}), '
                         f'el avance a 90 días pasó de {fmt(before)}% a {fmt(recent)}%. ')
                if same:
                    reading+='Las curvas a 30 y 90 días coinciden: dar más tiempo no recupera el avance en estos meses.'
                else:
                    gain=values.loc[month_of_increase,90]-values.loc[month_of_increase,30]
                    reading+=f'En el mes del aumento, esperar 90 días recupera {fmt(gain)} puntos frente a 30 días.'
                reading+=' El menor avance observado aún requiere explicar sus motivos.'
            else:
                reading='No hay seguimiento común suficiente para comparar ambos meses a 90 días; el diagnóstico de demora queda pendiente.'
            window_blocks.append({'stage':stage,'figure':fig,'reading':reading})
        old_conversion,new_conversion=pair(dt,'conversion_pct')
        if pd.notna(old_time) and pd.notna(new_time) and new_time>old_time:
            action='Revisar las visitas sin intento y el retraso de seguimiento; probar una mejora acotada de atención.'
        else:
            action='Revisar motivos de pérdida y decisiones comerciales de esta transición antes de elegir una intervención.'
        findings.append({'stage':stage,'hallazgo':f'{label}: conversión {fmt(old_conversion)}% → {fmt(new_conversion)}%; '
                         f'primer intento {fmt(old_time)} → {fmt(new_time)} días.',
                         'accion':action,'responsable':'Sales (propuesto)',
                         'seguimiento':'Comparar atención y conversión de nuevas entradas a esta etapa con igual seguimiento; acordar plazo y criterios de éxito.'})
    return {'attention':attention_blocks,'duration':duration_blocks,'windows':window_blocks,
            'findings':findings,'attention_metrics':attention,'stage_metrics':stages,
            'focus':focus,'baseline':baseline,'end':end}


if __name__=='__main__':
    from scripts.cro_stage_focus import analyze_stage_focus
    from scripts.cro_insights import conclusion_new
    root=Path(__file__).resolve().parents[1]
    for scenario in ('referencia','conversion','demora'):
        folder=root/'resultados/cro/metricas'/scenario
        month=conclusion_new(folder/'demanda.csv')['evidencia']['mes']
        focus=analyze_stage_focus(folder,month)
        result=focused_diagnosis(folder,focus,month)
        result['attention_metrics'].to_csv(folder/'atencion_focos_new.csv',index=False)
        result['stage_metrics'].to_csv(folder/'etapas_focos_new.csv',index=False)
        print(f'{scenario}: focos {result["focus"]}, periodo {result["baseline"]}–{result["end"]}.')
