"""Comprobación de presentación con resultados aislados regenerados."""
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts import cfo_model, cfo_present


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        (cls.root/'sql/cfo').mkdir(parents=True)
        shutil.copy(cfo_model.ROOT/'sql/cfo/puente.sql',cls.root/'sql/cfo/puente.sql')
        cls.old_model_root=cfo_model.ROOT
        cls.old_present_root=cfo_present.ROOT
        cfo_model.ROOT=cls.root
        cfo_present.ROOT=cls.root
        cfo_model.run()

    @classmethod
    def tearDownClass(cls):
        cfo_model.ROOT=cls.old_model_root
        cfo_present.ROOT=cls.old_present_root
        cls.temp.cleanup()

    def test_figures_and_positive_waterfall(self):
        figs=cfo_present.figures('positivo')
        self.assertEqual(len(figs),9)
        self.assertEqual(list(figs['02_movimientos'].data[0].y),[100,30,0,-30,0,30,0])
        self.assertTrue(all(float(v)==0 for v in figs['09_conciliacion'].data[0].y))
        for fig in figs.values():
            self.assertNotIn('sintético',fig.layout.title.text)

    def test_conclusions_change_with_results(self):
        a=cfo_present.conclusions('positivo')['4']
        b=cfo_present.conclusions('negativo')['4']
        c=cfo_present.conclusions('compensado')['4']
        self.assertIn('+9,000',a)
        self.assertIn('-3,000',b)
        self.assertIn('+0',c)
        self.assertNotEqual(a,b)

    def test_all_expected_results(self):
        import json
        manifest=json.loads((self.root/'resultados/cfo/manifest.json').read_text())
        self.assertEqual({k:v['delta_acumulado'] for k,v in manifest['escenarios'].items()},
                         {'positivo':900000,'negativo':-300000,'compensado':0})

    def test_focus_reconciles_and_excludes_unaffected_population(self):
        for scenario,total in [('positivo',900000),('negativo',-300000),('compensado',0)]:
            focus=cfo_present.localize(scenario)
            self.assertEqual(focus.diferencia_neta.sum(),total)
            self.assertTrue(focus[focus.poblacion=='Resto'].diferencia_neta.eq(0).all())
            self.assertTrue(focus[focus.fase=='previo'].diferencia_neta.eq(0).all())

    def test_compensation_requires_temporal_focus(self):
        focus=cfo_present.localize('compensado')
        eligible=focus[focus.poblacion=='Elegibles'].set_index('fase')
        self.assertEqual(eligible.loc['durante','diferencia_neta'],-300000)
        self.assertEqual(eligible.loc['posterior','diferencia_neta'],300000)
        result=cfo_present.reasoning('compensado')
        self.assertEqual(result['foco'],'Elegibles')
        self.assertEqual(result['resultado'],'equilibrio')

    def test_action_follows_result(self):
        results=[cfo_present.reasoning(s) for s in ('positivo','negativo','compensado')]
        self.assertEqual([r['resultado'] for r in results],['aumento','reduccion','equilibrio'])
        self.assertEqual(len({r['accion'] for r in results}),3)
        self.assertTrue(all('Finanzas' in r['evaluacion'] for r in results))

    def test_no_difference_does_not_invent_focus(self):
        folder=self.root/'datos/sinteticos/cfo/compensado'
        target=folder/'con_descuento/movimientos.csv'
        original=target.read_bytes()
        try:
            target.write_bytes((folder/'sin_descuento/movimientos.csv').read_bytes())
            route=cfo_present.reasoning('compensado')
            self.assertEqual(route['foco'],'Sin diferencia localizada')
            self.assertIn('antes de abrir más análisis',route['siguiente'])
        finally:
            target.write_bytes(original)


if __name__=='__main__':unittest.main()
