"""Fixtures independientes de generación para definiciones CFO."""
import unittest
from scripts.cfo_model import bridge, generate, metrics, validate


class CFOTests(unittest.TestCase):
    def test_discount_examples(self):
        old = {'base': (10, 1000)}
        self.assertEqual(bridge(old, old, 0, 2000)['delta_neto'], -2000)
        r = bridge(old, {'base': (13, 1000)}, 0, 3000)
        self.assertEqual((r['subyacente'], r['pricing'], r['delta_neto']), (3000, 0, 0))
        r = bridge({'base': (13, 1000)}, {'base': (13, 1000)}, 3000, 0)
        self.assertEqual((r['subyacente'], r['delta_neto']), (0, 3000))

    def test_price_quantity_and_components(self):
        r = bridge({'a': (10, 1000), 'b': (1, 2000)},
                   {'a': (12, 1100), 'c': (1, 500)}, 1000, 2000)
        self.assertEqual((r['subyacente'], r['pricing'], r['delta_neto']), (500, 1200, 700))

    def test_scenarios_and_cohort(self):
        for name, sign in [('positivo', 1), ('negativo', -1), ('compensado', 0)]:
            rows = generate(name)
            validate(rows)
            monthly, cohort, summary = metrics(rows)
            self.assertEqual(len(monthly), 30)
            d = summary['delta_acumulado']
            self.assertEqual((d > 0) - (d < 0), sign)
            self.assertEqual(summary['delta_previo'], 0)
            # Adquisiciones/reactivaciones no entran al denominador inicial.
            self.assertTrue(all(c['clientes_iniciales'] == 100 for c in cohort))
            self.assertTrue(all(c['grr'] <= 1 for c in cohort))

    def test_known_month_and_zero_denominators(self):
        monthly, cohort, summary = metrics(generate('compensado'))
        july = next(r for r in monthly if r['grupo'] == 'con_descuento' and r['mes'] == '2025-07-01')
        self.assertEqual(july['nuevos'], 5)
        self.assertEqual(july['expansion_subyacente'], 50000)
        self.assertEqual(july['descuentos'], 150000)
        jan = next(r for r in monthly if r['mes'] == '2025-01-01')
        self.assertIsNone(jan['ltv_ingreso'])
        self.assertIsNone(jan['churn'])
        self.assertIsNone(jan['crecimiento_mrr_pct'])
        self.assertAlmostEqual(july['crecimiento_mrr_pct'],(9700/10200-1)*100)
        self.assertEqual(summary['delta_acumulado'], 0)

    def test_initial_churn_cohort_cannot_reenter(self):
        monthly, cohort, _ = metrics(generate('positivo'))
        march = next(r for r in cohort if r['grupo'] == 'sin_descuento' and r['mes'] == '2026-03-01')
        self.assertEqual(march['clientes_retenidos'], 85)
        self.assertEqual(march['retencion'], .85)

    def test_independent_retention_income_denominators(self):
        monthly, cohort, _ = metrics(generate('compensado'))
        july = next(r for r in cohort if r['grupo']=='con_descuento' and r['mes']=='2025-07-01')
        # 100 clientes iniciales: 100*100 UM + 10 módulos de 20 UM.
        # 50 amplían 10 UM y reciben 30 UM; nuevas adquisiciones no entran a NRR.
        self.assertEqual(july['retencion'], 1)
        self.assertAlmostEqual(july['nrr'], 9200/10200)
        self.assertAlmostEqual(july['grr'], 9200/10200)
        october=next(r for r in monthly if r['grupo']=='con_descuento' and r['mes']=='2025-10-01')
        self.assertEqual(october['bajas'],5)
        self.assertAlmostEqual(october['churn'],5/110)

    def test_overlapping_prices_rejected(self):
        rows=generate('positivo')
        rows['precios'].append(dict(rows['precios'][0],precio_id='Duplicado'))
        with self.assertRaises(ValueError):validate(rows)

    def test_invalid_discount_rejected(self):
        rows = generate('positivo')
        rows['componentes_mes'][0]['descuento'] = rows['componentes_mes'][0]['bruto'] + 1
        with self.assertRaises(ValueError):
            validate(rows)


if __name__ == '__main__':
    unittest.main()
