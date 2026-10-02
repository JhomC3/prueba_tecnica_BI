"""Comprobación reproducible de las gráficas preparadas y sus denominadores."""
from pathlib import Path
import hashlib
import json
import pandas as pd
from scripts.cro_analysis import build_question, check_ratio

ROOT=Path(__file__).resolve().parents[1]
RATES={
 'etapas':[('conversion_pct','avances_siguiente','elegibles'),('perdida_pct','perdidos','elegibles'),('sin_avance_pct','sin_avance_ventana','elegibles'),('abiertos_corte_pct','abiertos_corte','cuentas_entrada')],
 'cohortes':[('conversion_new_won_pct','ganados_ventana','elegibles')],
 'calidad':[('calidad_pct','calificados','evaluados'),('cobertura_evaluacion_pct','evaluados','prospectos')],
 'atencion':[('cobertura_intento_pct','visitas_con_intento','visitas'),('contacto_efectivo_pct','visitas_contacto_efectivo','visitas_con_intento'),('puntualidad_pct','atendidos_en_plazo','elegibles_plazo')],
 'captacion_pago':[('conversion_pago_pct','nuevos_pagadores_ventana','elegibles')],
 'prioridad':[('conversion_base_pct','avances_base','elegibles_base'),('conversion_reciente_pct','avances_reciente','elegibles_reciente')]}
COUNTS={
 'demanda':(['mes'],['captados','entradas_new','entradas_marketing']),
 'etapas':(['etapa','mes','ventana'],['cuentas_entrada','elegibles','avances_siguiente','saltos','perdidos']),
 'atencion':(['etapa','mes'],['visitas','visitas_con_intento','visitas_contacto_efectivo','elegibles_plazo','atendidos_en_plazo']),
 'calidad':(['mes','version_criterios'],['prospectos','evaluados','calificados']),
 'cohortes':(['mes_entrada','ventana'],['entradas_new','elegibles','ganados_ventana']),
 'pagadores':(['mes_pago'],['nuevos_pagadores']),
 'captacion_pago':(['mes_entrada','ventana'],['captados_sin_pago_previo','elegibles','nuevos_pagadores_ventana']),
 'prioridad':(['etapa'],['elegibles_base','elegibles_reciente','avances_base','avances_reciente'])}


def validate():
    report={'escenarios':{},'revision_visual':'Pendiente en VS Code; sin permisos de pantalla.',
            'revision_humana':'Pendiente; lecturas descriptivas iniciales, sin causalidad.'}
    for scenario in ['referencia','conversion','demora']:
        folder=ROOT/'resultados/cro/metricas'/scenario
        stats={'ratios':0,'grupos_conciliados':0,'preguntas':{}}
        for name,rates in RATES.items():
            df=pd.read_csv(folder/f'{name}.csv')
            for column,num,den in rates:
                check_ratio(df,column,num,den);stats['ratios']+=len(df)
        for name,(keys,columns) in COUNTS.items():
            df=pd.read_csv(folder/f'{name}.csv')
            total=df[df.dimension.eq('total')].groupby(keys)[columns].sum().sort_index()
            channels=df[df.dimension.eq('canal')].groupby(keys)[columns].sum().reindex(total.index).fillna(0)
            if not total.eq(channels).all().all():
                raise AssertionError(f'No concilia por canal: {scenario}/{name}')
            stats['grupos_conciliados']+=len(total)
        for question in range(3,12):
            b=build_question(folder,question)
            for figure in b['figures']:
                if figure.layout.annotations:
                    raise AssertionError('Texto accesorio dentro de una figura')
                for menu in figure.layout.updatemenus:
                    for button in menu.buttons:
                        assert len(button.args[0]['visible'])==len(figure.data)
            stats['preguntas'][str(question)]={'figuras':len(b['figures']),'lectura':b['reading'],'evidencia':b['evidence']}
        report['escenarios'][scenario]=stats
    hashes={
     'Transactions.csv':'2dcbe59e9ac497c441f3c019963b11e9848ce4916e5773d257a36f83d953ae95',
     'S&M_spend.csv':'41fbb6499f2b0ad4565ccc0e96ec490c72599e15fd46d64086fd98e3443c4c13',
     'Industry.csv':'b4330fc6d7df60429849b3b176746f5389c65931f281308eb8224c8efd440ff5'}
    for name,expected in hashes.items():
        actual=hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()
        assert actual==expected,name
    report['originales_intactos']=True
    return report


if __name__=='__main__':
    report=validate()
    output=ROOT/'resultados/cro/validacion_graficas.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verificación completa: tres escenarios, nueve preguntas, ratios y cantidades conciliados; originales intactos.')
