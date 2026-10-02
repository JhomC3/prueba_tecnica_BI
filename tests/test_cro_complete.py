"""Fixtures independientes: denominadores, reingresos, pagos y madurez."""
import unittest
from contextlib import closing
from scripts.cro_demo import generate, database
from scripts.cro_complete import generate_full, complete_metrics, validate_full


def account(key,kind='New',captured='2026-01-01',qualified=None,prior=0):
    return dict(id_cuenta=key,canal='Referidos',industria='Comercio',tipo_entrada=kind,
                fecha_captacion=captured,perfil='micro',producto='Facturacion',region='Colombia',campana=None,
                inicio_historia_pagos='2025-01-01',pagador_previo=prior,
                ajuste_perfil=None if qualified is None else 1,necesidad=None if qualified is None else 1,
                intencion=qualified,calificado=qualified,
                fecha_evaluacion=None if qualified is None else '2026-01-02',
                version_criterios=None if qualified is None else 'v1',
                motivo_descalificacion='sin_intencion' if qualified==0 else None)


def visit(key,c,stage,start,end=None,state='abierto',target=None):
    return dict(id_registro=key,id_cuenta=c,id_etapa=stage,entrada=start,salida=end,
                estado=state,id_etapa_destino=target,fecha_asignacion_etapa=start,
                responsable_etapa='V1',motivo_perdida=None)


class CompleteTests(unittest.TestCase):
    def fixture(self):
        accounts=[account('A',qualified=1),account('B',qualified=0,prior=1),account('C'),
                  account('D',captured='2026-02-28'),account('E','Producto',qualified=1)]
        rows=[visit('A1','A','New','2026-01-01','2026-01-03','avance','Working'),
              visit('A2','A','Working','2026-01-03','2026-01-05','avance','Working'),
              visit('A3','A','Working','2026-01-05','2026-01-11','avance','Won'),
              visit('A4','A','Won','2026-01-11',state='ganado'),
              visit('B1','B','New','2026-01-01','2026-01-05','perdido'),
              visit('C1','C','New','2026-01-01'),visit('D1','D','New','2026-02-28')]
        contacts=[dict(id_interaccion='i1',id_cuenta='A',id_registro='A1',fecha='2026-01-02',tipo='correo',resultado='sin_respuesta',responsable='V1'),
                  dict(id_interaccion='i2',id_cuenta='A',id_registro='A1',fecha='2026-01-03',tipo='llamada',resultado='intercambio_efectivo',responsable='V1'),
                  dict(id_interaccion='i3',id_cuenta='B',id_registro='B1',fecha='2026-01-04',tipo='correo',resultado='sin_respuesta',responsable='V1')]
        pays=[dict(id_pago=k,id_cuenta=c,fecha_pago=d,estado_pago=s) for k,c,d,s in [
            ('p0','B','2025-12-15','valido'),('p1','A','2026-01-05','fallido'),
            ('p2','A','2026-01-12','valido'),('p3','A','2026-02-12','valido'),
            ('p4','E','2026-01-02','valido'),('p5','B','2026-01-06','valido')]]
        return accounts,rows,contacts,pays

    def test_independent_rates_payments_and_maturity(self):
        with closing(database(*self.fixture())) as con:
            validate_full(con,'2026-03-01')
            metrics=complete_metrics(con,'2026-03-01')
        total=lambda name:[r for r in metrics[name] if r['dimension']=='total']
        quality=next(r for r in total('calidad') if r['mes']=='2026-01')
        self.assertEqual((quality['prospectos'],quality['evaluados'],quality['calificados']),(4,3,2))
        self.assertEqual(quality['cobertura_evaluacion_pct'],75)
        self.assertAlmostEqual(quality['calidad_pct'],200/3)
        new=next(r for r in total('etapas') if r['etapa']=='New' and r['mes']=='2026-01' and r['ventana']==30)
        self.assertEqual((new['elegibles'],new['avances_siguiente'],new['perdidos']),(3,1,1))
        self.assertAlmostEqual(new['conversion_pct'],100/3)
        working=next(r for r in total('etapas') if r['etapa']=='Working' and r['ventana']==30)
        self.assertEqual((working['cuentas_entrada'],working['visitas'],working['avances_siguiente'],working['saltos']),(1,2,0,1))
        self.assertEqual(working['mediana_permanencia'],8)
        jan=next(r for r in total('atencion') if r['etapa']=='New' and r['mes']=='2026-01')
        self.assertEqual((jan['visitas'],jan['visitas_con_intento'],jan['intentos']),(3,2,3))
        self.assertAlmostEqual(jan['cobertura_intento_pct'],200/3)
        self.assertEqual(jan['contacto_efectivo_pct'],50)
        self.assertAlmostEqual(jan['puntualidad_pct'],100/3)
        fresh=next(r for r in total('atencion') if r['etapa']=='New' and r['mes']=='2026-02')
        self.assertEqual(fresh['elegibles_plazo'],0)
        self.assertIsNone(fresh['puntualidad_pct'])
        cohort=next(r for r in total('cohortes') if r['mes_entrada']=='2026-01' and r['ventana']==30)
        self.assertEqual((cohort['elegibles'],cohort['ganados_ventana']),(3,1))
        self.assertEqual(cohort['mediana_dias_new_won'],10)
        immature=next(r for r in total('cohortes') if r['mes_entrada']=='2026-01' and r['ventana']==60)
        self.assertEqual(immature['elegibles'],0)
        self.assertIsNone(immature['conversion_new_won_pct'])
        pay=total('pagadores')
        self.assertEqual(sum(r['nuevos_pagadores'] for r in pay),2)
        self.assertEqual(sum(r['compras_desde_producto'] for r in pay),1)
        self.assertEqual(sum(r['ganados'] for r in total('origen_cierres')),1)
        jan_demand=next(r for r in total('demanda') if r['mes']=='2026-01')
        self.assertEqual(jan_demand['captados'],4)
        self.assertIsNone(jan_demand['crecimiento_captados_pct'])

    def test_full_generation_controls_reproducibility_and_segments(self):
        for scenario in ('referencia','conversion','demora'):
            raw=generate_full(generate,scenario,seed=42,size=90)
            self.assertEqual(raw,generate_full(generate,scenario,seed=42,size=90))
            with closing(database(*raw)) as con:
                self.assertTrue(all(v==0 for v in validate_full(con,'2026-09-30').values()))
                m=complete_metrics(con,'2026-09-30')
                # Each segmentation reconciles to the total, not the sum of all dimensions.
                for name,value in [('demanda','captados'),('pagadores','nuevos_pagadores'),('origen_cierres','ganados')]:
                    total=sum(r[value] for r in m[name] if r['dimension']=='total')
                    for dimension in ('canal','tipo_entrada','industria','producto','region','perfil','campana'):
                        self.assertEqual(sum(r[value] for r in m[name] if r['dimension']==dimension),total)
                self.assertGreater(con.execute("SELECT COUNT(*) FROM dim_cuentas WHERE tipo_entrada='Producto'").fetchone()[0],0)
                self.assertGreater(con.execute("SELECT COUNT(*) FROM vw_etapas_cuenta WHERE visitas>1").fetchone()[0],0)
                self.assertGreater(con.execute("SELECT COUNT(*) FROM vw_ganados w LEFT JOIN vw_primer_pago p USING(id_cuenta) WHERE p.id_cuenta IS NULL").fetchone()[0],0)
                self.assertGreater(con.execute("SELECT COUNT(*) FROM pagos WHERE estado_pago='fallido'").fetchone()[0],0)
                con.execute("UPDATE interacciones SET fecha='2030-01-01' WHERE id_interaccion=(SELECT MIN(id_interaccion) FROM interacciones)")
                with self.assertRaises(ValueError):
                    validate_full(con,'2026-09-30')

    def test_priority_is_a_descriptive_gap_with_independent_counts(self):
        accounts=[account('A'),account('B'),account('C',captured='2026-05-01'),account('D',captured='2026-05-01')]
        events=[visit('A1','A','New','2026-01-01','2026-01-02','avance','Working'),
                visit('A2','A','Working','2026-01-02','2026-01-03','perdido'),
                visit('B1','B','New','2026-01-01','2026-01-02','perdido'),
                visit('C1','C','New','2026-05-01','2026-05-02','perdido'),
                visit('D1','D','New','2026-05-01','2026-05-02','perdido')]
        with closing(database(accounts,events)) as con:
            validate_full(con,'2026-09-30')
            m=complete_metrics(con,'2026-09-30')
        r=next(r for r in m['prioridad'] if r['dimension']=='total' and r['etapa']=='New')
        self.assertEqual((r['elegibles_base'],r['elegibles_reciente']),(2,2))
        self.assertEqual((r['conversion_base_pct'],r['conversion_reciente_pct'],r['brecha_pp']),(50,0,-50))
        self.assertEqual(r['avances_brecha_ilustrativa'],1)
        may=next(r for r in m['resultado_global'] if r['dimension']=='total' and r['mes']=='2026-05')
        self.assertEqual(may['new_anterior'],0)
        self.assertIsNone(may['crecimiento_new_pct'])

    def test_missing_month_is_zero_and_does_not_skip_baseline(self):
        accounts=[account('A'),account('B',captured='2026-03-01')]
        with closing(database(accounts,[])) as con:
            rows=[r for r in complete_metrics(con,'2026-04-01')['demanda'] if r['dimension']=='total']
        march=next(r for r in rows if r['mes']=='2026-03')
        self.assertEqual(march['captados_anterior'],0)
        self.assertIsNone(march['crecimiento_captados_pct'])
