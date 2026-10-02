"""Comprobar ratios, seguimiento y cobertura de las gráficas CRO."""
import unittest
from pathlib import Path
import pandas as pd
from scripts.cro_analysis import build_question, mature, weighted_rate, long_series

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'resultados/cro/metricas/referencia'

class AnalysisTests(unittest.TestCase):
    def test_weighted_rate_uses_counts_not_average_percentages(self):
        d=pd.DataFrame({'mes':['2026-01']*2,'n':[1,9],'d':[2,90]})
        result=weighted_rate(d,['mes'],'n','d','pct')
        self.assertAlmostEqual(result.iloc[0].pct,100*10/92)
        # 0/0 is unavailable, not a zero percent conversion.
        zero=weighted_rate(pd.DataFrame({'mes':['2026-01'],'n':[0],'d':[0]}),['mes'],'n','d','pct')
        self.assertTrue(pd.isna(zero.iloc[0].pct))

    def test_incomplete_month_not_partially_shown(self):
        d=pd.DataFrame({'mes':['2026-01','2026-01','2026-02','2026-02'],
                        'elegibles':[10,20,10,15],'cuentas_entrada':[10,20,10,20]})
        result=mature(d,'cuentas_entrada','mes')
        self.assertEqual(set(result.mes),{'2026-01'})

    def test_quality_hover_uses_evaluated_denominator(self):
        data=pd.DataFrame({'mes':['2026-01'],'prospectos':[100], 'evaluados':[20],
                           'calificados':[10],'calidad_pct':[50]})
        point=long_series(data,'mes',{'calidad_pct':'Calificados'}).iloc[0]
        self.assertEqual((point.casos,point.base),(10,20))
        self.assertEqual(point.denominador,'Evaluados')

    def test_every_question_has_figures_and_inspection_evidence(self):
        for question in range(3,12):
            with self.subTest(question=question):
                bundle=build_question(FOLDER,question)
                self.assertTrue(bundle['figures'])
                self.assertTrue(bundle['reading'])
                self.assertTrue(bundle['evidence'])
                for figure in bundle['figures']:
                    self.assertTrue(figure.data)
                    self.assertGreaterEqual(figure.layout.height,390)
                    if question!=3:
                        self.assertFalse(figure.layout.annotations)
                    for trace in figure.data:
                        if trace.type=='scatter':
                            self.assertEqual(len(trace.x),len(trace.y))
                    for menu in figure.layout.updatemenus:
                        for button in menu.buttons:
                            self.assertEqual(len(button.args[0]['visible']),len(figure.data))

    def test_stage_lines_show_all_six_transitions_without_selector(self):
        bundle=build_question(FOLDER,3)
        self.assertEqual(len(bundle['figures']),2)
        for fig in bundle['figures']:
            self.assertFalse(fig.layout.updatemenus)
            self.assertFalse(fig.layout.annotations)
            transitions={trace.name.split(' · ',1)[0] for trace in fig.data}
            self.assertEqual(len(transitions),6)
            self.assertIn('Proposal → Won',transitions)
            self.assertTrue(all(trace.visible is not False for trace in fig.data))
            self.assertEqual(len({trace.xaxis for trace in fig.data}),1)

    def test_cohort_90_day_trace_does_not_include_partial_july(self):
        bundle=build_question(FOLDER,10)
        figure=bundle['figures'][0]
        ninety=next(trace for trace in figure.data if trace.name=='90 días')
        self.assertEqual(len(ninety.x),6)
        self.assertTrue(all(str(x)<'2026-07' for x in ninety.x))

    def test_priority_not_added_across_stages(self):
        bundle=build_question(FOLDER,11)
        self.assertIn('no se suman',bundle['reading'])
        self.assertEqual(len(bundle['figures'][0].data[0].x),6)

if __name__=='__main__': unittest.main()
