"""Contexto temporal: recuperación, seguimiento y series incompletas."""
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from scripts.cro_insights import conclusion_new_por_canal


class ChannelContextTests(unittest.TestCase):
    def fixture(self, directory):
        rows=[]
        series={'Orgánico':[10,20,10,25,15], 'Marketing pago':[20,20,20,25,20],
                'Referidos':[10,10,10,15,15]}
        series['total']=[sum(values[i] for values in series.values()) for i in range(5)]
        for segment, values in series.items():
            for i, value in enumerate(values):
                previous=values[i-1] if i else None
                rows.append({'mes':f'2026-{i+1:02d}', 'dimension':'total' if segment=='total' else 'canal',
                             'segmento':segment,'entradas_new':value,'new_anterior':previous,
                             'crecimiento_new_pct':100*(value/previous-1) if previous else None})
        path=Path(directory)/'demanda.csv'
        pd.DataFrame(rows).to_csv(path,index=False)
        return path

    def test_recovery_does_not_hide_previous_peak_or_reversal(self):
        with tempfile.TemporaryDirectory() as directory:
            result=conclusion_new_por_canal(self.fixture(directory))
        self.assertEqual(result['mes'],'2026-04')
        self.assertIn('20 en febrero a 10 en marzo (-50,0%)',result['texto_detallado'])
        self.assertIn('+150,0% frente a marzo; +25,0% frente al máximo previo de 20',result['texto_detallado'])
        self.assertIn('terminó en 15 en mayo',result['texto_detallado'])
        self.assertIn('No permaneció por encima del máximo previo',result['texto_detallado'])
        self.assertEqual(len(result['contexto']),3)

    def test_missing_channel_month_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=self.fixture(directory)
            df=pd.read_csv(path)
            df.drop(df[df.segmento.eq('Orgánico') & df.mes.eq('2026-02')].index).to_csv(path,index=False)
            with self.assertRaisesRegex(ValueError,'Faltan meses'):
                conclusion_new_por_canal(path)

    def test_channel_totals_must_reconcile_for_every_month(self):
        with tempfile.TemporaryDirectory() as directory:
            path=self.fixture(directory)
            df=pd.read_csv(path)
            df.loc[df.segmento.eq('Orgánico') & df.mes.eq('2026-01'),'entradas_new']=99
            df.to_csv(path,index=False)
            with self.assertRaisesRegex(ValueError,'no concilia'):
                conclusion_new_por_canal(path)


if __name__=='__main__':
    unittest.main()
