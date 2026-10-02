"""Verificación reproducible de artefactos CFO, sin regenerar ni alterar fuentes."""
import hashlib
import csv
import json
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def run():
    manifest=json.loads((ROOT/'resultados/cfo/manifest.json').read_text())
    for name,digest in manifest['hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    expected={'positivo':900000,'negativo':-300000,'compensado':0}
    route_hashes={}
    for name,summary in manifest['escenarios'].items():
        assert summary['delta_previo']==0
        assert summary['delta_acumulado']==expected[name]
        with closing(sqlite3.connect(ROOT/f'datos/bases/cfo/{name}/modelo.sqlite')) as db:
            assert not db.execute('PRAGMA foreign_key_check').fetchall()
            assert db.execute('SELECT MAX(ABS(residuo)) FROM puente_mensual').fetchone()[0]==0
        htmls=list((ROOT/f'resultados/cfo/graficas/{name}').glob('*.html'))
        assert len(htmls)==9
        assert (ROOT/f'resultados/cfo/graficas/{name}/plotly.min.js').exists()
        focus_path=ROOT/f'resultados/cfo/metricas/{name}/focos.csv'
        route_path=ROOT/f'resultados/cfo/metricas/{name}/recorrido.json'
        if focus_path.exists() and route_path.exists():
            with focus_path.open() as f:focus=list(csv.DictReader(f))
            assert sum(int(r['diferencia_neta']) for r in focus)==expected[name]
            assert all(int(r['diferencia_neta'])==0 for r in focus if r['poblacion']=='Resto' or r['fase']=='previo')
            assert json.loads(route_path.read_text())['delta']==expected[name]
            for p in [focus_path,route_path]:route_hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    notebook=json.loads((ROOT/'notebooks/03_modelo_cfo.ipynb').read_text())
    codes=[c for c in notebook['cells'] if c['cell_type']=='code']
    assert all(c['execution_count'] is not None for c in codes)
    assert all(not any(o['output_type']=='error' for o in c['outputs']) for c in codes)
    tests=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_cfo*.py'],
                         cwd=ROOT,text=True,capture_output=True)
    assert tests.returncode==0,tests.stdout+tests.stderr
    evidence=dict(validacion='correcta',pruebas_cfo=tests.stderr.strip(),
        csv_con_hash=len(manifest['hashes']),graficas_html=27,
        celdas_ejecutadas=len(codes),residuo_puente=0,
        recorrido_verificado=bool(route_hashes),hashes_recorrido=route_hashes,
        fuente_original_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'inputs').rglob('*')) if p.is_file()},
        limites=['Demo sintética; no efecto causal histórico ni utilidad.',
                 'LTV estacionario no estimable cuando churn cero.',
                 'Revisión visual y de conclusiones por el candidato pendiente.'])
    (ROOT/'resultados/cfo/validacion.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in evidence.items() if k not in ('pruebas_cfo','fuente_original_sha256','limites')},ensure_ascii=False))
    return evidence


if __name__=='__main__':run()
