"""Contratos sintéticos CFO -> CSV/SQLite -> indicadores, sin leer inputs reales."""
import csv
import hashlib
import json
import sqlite3
from collections import defaultdict
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONTHS = [f'{2025 + i//12}-{i%12+1:02d}-01' for i in range(15)]
SCENARIOS = {'positivo': (13, 3000), 'negativo': (10, 2000), 'compensado': (11, 3000)}
GROUPS = ('sin_descuento', 'con_descuento')


def bridge(previous, current, discount_before=0, discount_now=0):
    """Componentes {id: (cantidad, precio_centavos)}; cross-term a pricing."""
    underlying = pricing = 0
    for key in previous.keys() | current.keys():
        q0, p0 = previous.get(key, (0, 0))
        q1, p1 = current.get(key, (0, 0))
        if key not in previous:
            underlying += q1*p1
        elif key not in current:
            underlying -= q0*p0
        else:
            underlying += (q1-q0)*p0
            pricing += q1*(p1-p0)
    gross0 = sum(q*p for q, p in previous.values())
    gross1 = sum(q*p for q, p in current.values())
    return dict(subyacente=underlying, pricing=pricing,
                delta_descuento=discount_now-discount_before,
                neto_anterior=gross0-discount_before, neto=gross1-discount_now,
                delta_neto=gross1-discount_now-gross0+discount_before)


def generate(scenario):
    if scenario not in SCENARIOS:
        raise ValueError('Escenario desconocido')
    quantity, discount = SCENARIOS[scenario]
    tables = {n: [] for n in ('clientes', 'suscripciones', 'componentes', 'precios',
                              'descuentos', 'estados', 'componentes_mes', 'pagos', 'movimientos')}
    for group in GROUPS:
        for i in range(110):
            customer = f'C{i:03}'
            kind = 'existente' if i < 100 else ('nuevo' if i < 105 else 'reactivado')
            start = 0 if i < 100 else (6 if i < 105 else 8)
            eligible = i < 50
            # Bajas iguales entre grupos: octubre y enero; aislamos precio/descuento.
            end = 9 if 55 <= i < 60 else (12 if 80 <= i < 90 else 15)
            tables['clientes'].append(dict(grupo=group, cliente=customer, tipo=kind,
                                          segmento='Comercio' if i%2 else 'Servicios',
                                          elegible=int(eligible)))
            for k in range(2 if 90 <= i < 100 else 1):
                subscription = f'S{i:03}-{k}'
                component = f'{subscription}-base'
                tables['suscripciones'].append(dict(grupo=group, suscripcion=subscription,
                    cliente=customer, inicio=MONTHS[start], fin=MONTHS[end] if end < 15 else '',
                    historia_previa=int(kind == 'reactivado')))
                tables['componentes'].append(dict(grupo=group, componente=component,
                    suscripcion=subscription, servicio='Asientos' if k==0 else 'Modulo adicional',
                    unidad='licencia', inicio=MONTHS[start], fin=MONTHS[end] if end < 15 else ''))
                price = 1000 if k == 0 else 2000
                price_key = f'{component}-P1'
                tables['precios'].append(dict(grupo=group, precio_id=price_key, componente=component,
                    tarifa=price, inicio=MONTHS[start], fin='2025-12-01' if 70<=i<80 else ''))
                if 70 <= i < 80:
                    tables['precios'].append(dict(grupo=group, precio_id=f'{component}-P2',
                        componente=component, tarifa=price+100, inicio='2025-12-01', fin=''))
                if eligible and group == 'con_descuento' and k == 0:
                    tables['descuentos'].append(dict(grupo=group, descuento_id=f'D{i:03}',
                        suscripcion=subscription, componente=component, tipo='fijo', valor=discount,
                        porcentaje_equivalente=discount/(quantity*price)*100,
                        inicio=MONTHS[6], fin=MONTHS[9], duracion_meses=3,
                        objetivo='ampliacion_retencion' if scenario=='positivo' else 'ampliacion' if scenario=='compensado' else 'retencion',
                        responsable='Comercial (supuesto)'))
                for m, month in enumerate(MONTHS):
                    active = start <= m < end
                    state = 'activo' if active else ('baja' if m>=end else 'inactivo')
                    tables['estados'].append(dict(grupo=group, cliente=customer,
                        suscripcion=subscription, mes=month, estado=state))
                    if not active:
                        continue
                    q = (quantity if eligible and group=='con_descuento' and m>=6 else 10) if k==0 else 1
                    p = price + (100 if 70<=i<80 and m>=11 else 0)
                    d = discount if eligible and group=='con_descuento' and 6<=m<9 and k==0 else 0
                    gross = q*p
                    tables['componentes_mes'].append(dict(grupo=group, cliente=customer,
                        suscripcion=subscription, componente=component, mes=month,
                        cantidad=q, precio_id=f'{component}-P2' if p!=price else price_key,
                        tarifa=p, bruto=gross, descuento=d, neto=gross-d))
                    # Cobro sintético con un atraso y un cargo no recurrente explícitos.
                    lag = 1000 if i==0 and m==6 else (-1000 if i==0 and m==7 else 0)
                    extra = 500 if i==1 and m==6 else 0
                    tables['pagos'].append(dict(grupo=group, pago=f'{subscription}-{m}',
                        suscripcion=subscription, mes=month, mrr_neto=gross-d,
                        pendiente=lag, cargo_no_recurrente=extra, pagado=gross-d-lag+extra))
            prev = {}
            prev_discount = 0
            for m, month in enumerate(MONTHS):
                entries = [r for r in tables['componentes_mes'] if r['grupo']==group and r['cliente']==customer and r['mes']==month]
                current = {r['componente']: (r['cantidad'], r['tarifa']) for r in entries}
                d = sum(r['descuento'] for r in entries)
                result = bridge(prev, current, prev_discount, d)
                status = 'inicio' if m==0 else ('reactivacion' if current and not prev and kind=='reactivado' else 'nuevo' if current and not prev else 'churn' if prev and not current else 'continuo')
                tables['movimientos'].append(dict(grupo=group, cliente=customer, mes=month,
                    estado=status, activo=int(bool(current)), activo_anterior=int(bool(prev)),
                    bruto=sum(r['bruto'] for r in entries), descuento=d, **result))
                prev, prev_discount = current, d
    return tables


def validate(tables):
    components = {(r['grupo'],r['componente']) for r in tables['componentes']}
    prices = {(r['grupo'],r['precio_id']):r for r in tables['precios']}
    intervals = defaultdict(list)
    for r in tables['precios']:
        if r['fin'] and r['inicio'] >= r['fin']:
            raise ValueError('Vigencia inválida')
        intervals[r['grupo'],r['componente']].append((r['inicio'],r['fin'] or '9999'))
    for versions in intervals.values():
        ordered = sorted(versions)
        if any(b[0] < a[1] for a,b in zip(ordered,ordered[1:])):
            raise ValueError('Precios con vigencias solapadas')
    keys = set()
    for r in tables['componentes_mes']:
        key = (r['grupo'], r['componente'], r['mes'])
        if key in keys or key[:2] not in components:
            raise ValueError('Clave duplicada o relación inválida')
        keys.add(key)
        price = prices.get((r['grupo'],r['precio_id']))
        if not price or price['componente']!=r['componente'] or price['tarifa']!=r['tarifa'] or not price['inicio']<=r['mes']<(price['fin'] or '9999'):
            raise ValueError('Precio no vigente')
        if r['bruto']!=r['cantidad']*r['tarifa'] or not 0<=r['descuento']<=r['bruto'] or r['neto']!=r['bruto']-r['descuento']:
            raise ValueError('Importes inválidos')
        expected=sum(d['valor'] for d in tables['descuentos'] if d['grupo']==r['grupo'] and d['componente']==r['componente'] and d['inicio']<=r['mes']<d['fin'])
        if r['descuento']!=expected:
            raise ValueError('Descuento no corresponde a vigencia/alcance')
    for r in tables['movimientos']:
        if r['delta_neto'] != r['subyacente']+r['pricing']-r['delta_descuento']:
            raise ValueError('Puente no conciliado')
    for r in tables['pagos']:
        if r['pagado']+r['pendiente']-r['cargo_no_recurrente']!=r['mrr_neto']:
            raise ValueError('Pago no conciliado')


def metrics(tables):
    monthly, cohorts = [], []
    clients = {(r['grupo'],r['cliente']): r for r in tables['clientes']}
    for group in GROUPS:
        initial = {r['cliente']:r['neto'] for r in tables['movimientos'] if r['grupo']==group and r['mes']==MONTHS[0] and r['activo']}
        initial_mrr = sum(initial.values())
        alive = set(initial)
        cumulative = cohort_cumulative = 0
        previous_net = None
        for month in MONTHS:
            rows = [r for r in tables['movimientos'] if r['grupo']==group and r['mes']==month]
            current = {r['cliente']:r for r in rows}
            active = sum(r['activo'] for r in rows)
            base = sum(r['activo_anterior'] for r in rows)
            churns = sum(r['estado']=='churn' for r in rows)
            net = sum(r['neto'] for r in rows)
            cumulative += net
            churn = churns/base if base else None
            arpu = net/active if active else None
            retained = {c for c in alive if current[c]['activo']}
            alive = retained  # no reingreso al numerador de retención ininterrumpida
            retained_net = sum(current[c]['neto'] for c in retained)
            cohort_cumulative += sum(current[c]['neto'] for c in initial)
            cohorts.append(dict(grupo=group, mes=month, clientes_iniciales=len(initial),
                clientes_retenidos=len(retained), retencion=len(retained)/len(initial),
                nrr=retained_net/initial_mrr,
                grr=sum(min(initial[c],current[c]['neto']) for c in retained)/initial_mrr,
                ingreso_cohorte_acumulado=cohort_cumulative))
            existing = [r for r in rows if r['estado']=='continuo' and r['activo'] and r['activo_anterior']]
            monthly.append(dict(grupo=group, mes=month,
                crecimiento_mrr_pct=(net/previous_net-1)*100 if previous_net else None,
                bruto=sum(r['bruto'] for r in rows),
                descuentos=sum(r['descuento'] for r in rows), neto=net, arr=net*12,
                clientes_activos=active, arpu=arpu, nuevos=sum(r['estado']=='nuevo' for r in rows),
                reactivados=sum(r['estado']=='reactivacion' for r in rows), bajas=churns,
                churn=churn, ltv_ingreso=arpu/churn if churn and arpu is not None else None,
                saldo_inicial=sum(r['neto_anterior'] for r in rows),
                nuevo_mrr=sum(r['subyacente'] for r in rows if r['estado']=='nuevo'),
                reactivacion_mrr=sum(r['subyacente'] for r in rows if r['estado']=='reactivacion'),
                churn_bruto=sum(r['subyacente'] for r in rows if r['estado']=='churn'),
                apertura_mrr=sum(r['subyacente'] for r in rows if r['estado']=='inicio'),
                expansion_subyacente=sum(max(0,r['subyacente']) for r in existing),
                contraccion_subyacente=sum(min(0,r['subyacente']) for r in existing),
                pricing=sum(r['pricing'] for r in rows),
                delta_descuento=sum(r['delta_descuento'] for r in rows),
                acumulado=cumulative))
            previous_net = net
    totals = {g:sum(r['neto'] for r in monthly if r['grupo']==g and r['mes']>=MONTHS[6]) for g in GROUPS}
    prev = {g:sum(r['neto'] for r in monthly if r['grupo']==g and r['mes']<MONTHS[6]) for g in GROUPS}
    # Permanencia restringida al periodo observable, no promedio de vidas completas.
    permanence = []
    for group in GROUPS:
        for customer in sorted(c for g,c in clients if g==group):
            rows=[r for r in tables['movimientos'] if r['grupo']==group and r['cliente']==customer]
            active_months=sum(r['activo'] for r in rows)
            permanence.append(dict(grupo=group,cliente=customer,meses_activos_observados=active_months,
                                   censurado=int(rows[-1]['activo']),tipo=clients[group,customer]['tipo']))
    return monthly, cohorts, dict(delta_acumulado=totals['con_descuento']-totals['sin_descuento'],
        delta_previo=prev['con_descuento']-prev['sin_descuento'], totales=totals,
        descuentos_acumulados=sum(r['descuento'] for r in tables['movimientos'] if r['grupo']=='con_descuento'),
        permanencia=permanence)


def write_csv(path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=fieldnames or list(rows[0]));writer.writeheader();writer.writerows(rows)


def run():
    manifest={'unidad':'UM ilustrativas, almacenadas en centavos; no COP históricos',
              'periodo': [MONTHS[0],MONTHS[-1]], 'descuento':['2025-07-01','2025-10-01'],
              'semilla':'determinista, sin azar', 'escenarios':{}, 'hashes':{}}
    examples=[]
    for name,old,new,d0,d1 in [
        ('Contraccion_100_80',{'base':(10,1000)},{'base':(8,1000)},0,0),
        ('Descuento_100_80',{'base':(10,1000)},{'base':(10,1000)},0,2000),
        ('Ampliacion_100_130',{'base':(10,1000)},{'base':(13,1000)},0,3000),
        ('Fin_descuento',{'base':(13,1000)},{'base':(13,1000)},3000,0)]:
        examples.append(dict(ejemplo=name,bruto=sum(q*p for q,p in new.values()),descuento=d1,
                             **bridge(old,new,d0,d1)))
    write_csv(ROOT/'resultados/cfo/ejemplos.csv',examples)
    for scenario in SCENARIOS:
        tables=generate(scenario);validate(tables)
        monthly, cohort, summary=metrics(tables)
        folder=ROOT/'resultados/cfo/metricas'/scenario
        write_csv(folder/'mensual.csv',monthly);write_csv(folder/'cohortes.csv',cohort)
        write_csv(folder/'permanencia.csv',summary.pop('permanencia'))
        comparison=[]
        accumulated=0
        for month in MONTHS:
            a=next(r for r in monthly if r['grupo']=='con_descuento' and r['mes']==month)
            b=next(r for r in monthly if r['grupo']=='sin_descuento' and r['mes']==month)
            difference=a['neto']-b['neto'];accumulated+=difference
            comparison.append(dict(mes=month,neto_con_descuento=a['neto'],
                esperado_sin_descuento=b['neto'],diferencia=difference,
                diferencia_acumulada=accumulated,descuentos=a['descuentos']))
        write_csv(folder/'comparacion.csv',comparison)
        for group in GROUPS:
            for name,rows in tables.items():
                selected=[r for r in rows if r['grupo']==group]
                write_csv(ROOT/'datos/sinteticos/cfo'/scenario/group/f'{name}.csv',selected,list(rows[0]))
        dbpath=ROOT/'datos/bases/cfo'/scenario/'modelo.sqlite';dbpath.parent.mkdir(parents=True,exist_ok=True)
        # Solo reconstruye su salida regenerable identificada.
        if dbpath.exists():dbpath.unlink()
        with closing(sqlite3.connect(dbpath)) as db, db:
            db.execute('PRAGMA foreign_keys = ON')
            primary = {'clientes':['grupo','cliente'], 'suscripciones':['grupo','suscripcion'],
                       'componentes':['grupo','componente'], 'precios':['grupo','precio_id'],
                       'descuentos':['grupo','descuento_id'], 'estados':['grupo','suscripcion','mes'],
                       'componentes_mes':['grupo','componente','mes'], 'pagos':['grupo','pago'],
                       'movimientos':['grupo','cliente','mes']}
            relations = {'suscripciones': [('cliente','clientes','cliente')],
                         'componentes':[('suscripcion','suscripciones','suscripcion')],
                         'precios':[('componente','componentes','componente')],
                         'descuentos':[('componente','componentes','componente'),('suscripcion','suscripciones','suscripcion')],
                         'estados':[('suscripcion','suscripciones','suscripcion')],
                         'componentes_mes':[('cliente','clientes','cliente'),('suscripcion','suscripciones','suscripcion'),('componente','componentes','componente'),('precio_id','precios','precio_id')],
                         'pagos':[('suscripcion','suscripciones','suscripcion')],
                         'movimientos':[('cliente','clientes','cliente')]}
            for name,rows in tables.items():
                keys=list(rows[0]);cols=[]
                for key in keys:
                    sample=next((r[key] for r in rows if r[key] is not None),None)
                    dtype='INTEGER' if isinstance(sample,int) else 'REAL' if isinstance(sample,float) else 'TEXT'
                    cols.append(f'"{key}" {dtype}')
                cols.append(f'PRIMARY KEY ({",".join(primary[name])})')
                for key,target,targetkey in relations.get(name,[]):
                    cols.append(f'FOREIGN KEY (grupo,{key}) REFERENCES {target}(grupo,{targetkey})')
                if name=='componentes_mes':
                    cols.extend(['CHECK(bruto=cantidad*tarifa)', 'CHECK(descuento>=0 AND descuento<=bruto)', 'CHECK(neto=bruto-descuento)'])
                db.execute(f'CREATE TABLE "{name}" ({",".join(cols)})')
                db.executemany(f'INSERT INTO "{name}" VALUES ({",".join("?" for _ in keys)})',
                               [tuple(r[k] for k in keys) for r in rows])
            db.executescript((ROOT/'sql/cfo/puente.sql').read_text())
            assert db.execute('SELECT MAX(ABS(residuo)) FROM puente_mensual').fetchone()[0]==0
            assert not db.execute('PRAGMA foreign_key_check').fetchall()
        summary['filas']={k:len(v) for k,v in tables.items()}
        manifest['escenarios'][scenario]=summary
    for root in [ROOT/'datos/sinteticos/cfo', ROOT/'resultados/cfo/metricas']:
        for p in sorted(root.rglob('*.csv')):
            manifest['hashes'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    out=ROOT/'resultados/cfo/manifest.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    return manifest


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v['delta_acumulado']/100 for k,v in result['escenarios'].items()},ensure_ascii=False))
