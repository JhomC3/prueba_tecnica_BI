"""Población, periodos y seguimiento del diagnóstico acotado."""
import unittest
from pathlib import Path
import pandas as pd
from scripts.cro_stage_focus import analyze_stage_focus
from scripts.cro_focused_diagnosis import focused_diagnosis

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'resultados/cro/metricas/referencia'


class FocusedDiagnosisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focus=analyze_stage_focus(FOLDER,'2026-05')
        cls.result=focused_diagnosis(FOLDER,cls.focus,'2026-05')

    def test_scope_is_only_selected_stages_and_reference_period(self):
        for name in ['attention_metrics','stage_metrics']:
            data=self.result[name]
            self.assertEqual(set(data.etapa),{'Demo','Proposal'})
            self.assertTrue(data.mes.between('2026-04','2026-08').all())
        self.assertEqual({x['stage'] for x in self.result['findings']},{'Demo','Proposal'})

    def test_attention_count_reconciles_with_raw_new_visits(self):
        base=ROOT/'datos/sinteticos/cro/referencia'
        accounts=pd.read_csv(base/'dim_cuentas.csv')
        events=pd.read_csv(base/'fact_etapas.csv')
        new_ids=set(accounts.loc[accounts.tipo_entrada.eq('New'),'id_cuenta'])
        expected=events.loc[events.id_cuenta.isin(new_ids)&events.id_etapa.eq('Demo')&
                            events.entrada.str.startswith('2026-04')].shape[0]
        d=self.result['attention_metrics']
        actual=d.loc[d.etapa.eq('Demo')&d.mes.eq('2026-04')&d.dimension.eq('total'),'visitas'].iloc[0]
        self.assertEqual(actual,expected)

    def test_longer_windows_use_same_fully_observed_months(self):
        for block in self.result['windows']:
            traces=block['figure'].data
            self.assertEqual(len(traces),3)
            self.assertTrue(all(list(t.x)==list(traces[0].x) for t in traces))
            self.assertTrue(all(str(x)<'2026-07' for t in traces for x in t.x))

    def test_each_chart_has_a_conclusion_and_only_selected_stage(self):
        for family in ['attention','duration','windows']:
            for block in self.result[family]:
                self.assertIn(block['stage'],self.focus['focus'])
                self.assertTrue(block['reading'])
                self.assertFalse(block['figure'].layout.updatemenus)
                for trace in block['figure'].data:
                    self.assertEqual(len(trace.x),len(trace.y))


if __name__=='__main__':
    unittest.main()
