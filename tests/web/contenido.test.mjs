import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');

describe('contrato de contenido', () => {
  for (const id of ['cro', 'cfo']) {
    it(`${id}: 13 componentes en orden con pregunta del marco`, () => {
      const c = JSON.parse(leer(`src/content/${id}.json`));
      assert.equal(c.componentes.length, 13);
      assert.deepEqual(c.componentes.map((k) => k.numero), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]);
      for (const k of c.componentes) assert.ok(k.pregunta_marco && k.nombre);
      assert.ok(c.requerimiento_original.texto.length > 50);
    });
  }
  it('cro: 11 preguntas literales con estándar 3.1', () => {
    const c = JSON.parse(leer('src/content/cro.json'));
    assert.equal(c.preguntas.length, 11);
    for (const p of c.preguntas) {
      assert.ok(p.pregunta);
      assert.ok(p.que_medimos && p.alcance && p.metrica_formula && p.datos);
    }
  });
  it('cfo: 14 preguntas con evidencia necesaria y origen marcado', () => {
    const c = JSON.parse(leer('src/content/cfo.json'));
    assert.equal(c.preguntas.length, 14);
    for (const p of c.preguntas) {
      assert.ok(p.evidencia_necesaria);
      assert.ok(['referencia', 'propuesta_desarrollo'].includes(p.origen));
    }
  });
  it('ningún pendiente aparece como disponible', () => {
    for (const id of ['cro', 'cfo']) {
      const c = JSON.parse(leer(`src/content/${id}.json`));
      for (const k of [...c.componentes, ...c.preguntas]) {
        if (k.estado === 'pendiente') assert.ok(!k.respuesta || !k.que_medimos);
      }
    }
  });
  it('figuras configurables por contrato (sin rutas fijas en el renderizador)', () => {
    const vista = leer('src/views/case.js');
    assert.ok(!vista.includes('new_serie_referencia.json'), 'el renderizador no fija la serie');
    assert.ok(!vista.includes('01_new_tendencia.html'), 'el renderizador no fija la figura');
    assert.ok(!vista.includes('new-serie') || vista.includes('p.figura'), 'sin id fijo salvo lectura del contrato');
    const c = JSON.parse(leer('src/content/cro.json'));
    const f = c.preguntas.find((p) => p.id === 'cro-3.1').figura;
    assert.ok(f.datos_src && f.iframe_src && f.tabla, 'cro-3.1 declara datos, figura y tabla');
    assert.ok(f.tabla.columnas.every((col) => col.campo && col.etiqueta));
  });
});

describe('exportación verificada sin valores fijados', () => {
  it('serie New: estructura válida y variación leída del CSV', () => {
    const s = JSON.parse(leer('public/data/new_serie_referencia.json'));
    assert.ok(s.valores.length >= 1);
    const meses = s.valores.map((v) => v.mes);
    assert.deepEqual(meses, [...meses].sort());
    assert.equal(new Set(meses).size, meses.length);
    assert.equal(s.valores[0].variacion_mensual_pct, null);
    assert.ok(!String(s.poblacion).includes('seguimiento de 30 días'), 'población sin ventana de conversión');
    assert.ok(String(s.contexto).includes('crecimiento_new_pct'), 'variación leída del CSV');
  });
  it('serie coherente con el manifest (meses y conteo, no valores fijos)', () => {
    const s = JSON.parse(leer('public/data/new_serie_referencia.json'));
    const m = JSON.parse(leer('public/data/manifest.json'));
    assert.deepEqual(m.serie.meses, s.valores.map((v) => v.mes));
    assert.equal(m.serie.n_meses, s.valores.length);
  });
  it('figura existente copiada en bytes', () => {
    assert.ok(existsSync(join(raiz, 'public/charts/01_new_tendencia.html')));
    const m = JSON.parse(leer('public/data/manifest.json'));
    assert.equal(m.figura.sha256, m.figura.origen_sha256);
  });
  it('contenido público sincronizado con la fuente', () => {
    const m = JSON.parse(leer('public/data/manifest.json'));
    for (const c of m.contenidos) {
      assert.equal(leer(`public/${c.archivo}`), leer(`src/${c.archivo}`));
    }
  });
});

describe('paquete público sin secretos ni internos', () => {
  it('sin .env, node_modules, .venv, .git ni inputs en public/', () => {
    for (const p of ['public/.env', 'public/.git', 'public/inputs', 'public/.venv']) {
      assert.ok(!existsSync(join(raiz, p)));
    }
    const html = leer('index.html');
    assert.ok(!/VITE_.*KEY|SECRET|TOKEN/.test(html));
  });
  it('vistas y estilos existen', () => {
    for (const p of ['src/app.js', 'src/views/summary.js', 'src/views/case.js', 'src/views/explore.js', 'src/styles.css', 'src/vocabulary.json', 'scripts/sync-content.mjs']) {
      assert.ok(existsSync(join(raiz, p)), p);
    }
  });
  it('build sincroniza contenido (prebuild)', () => {
    const pkg = JSON.parse(leer('package.json'));
    assert.ok(pkg.scripts.prebuild && pkg.scripts.prebuild.includes('sync-content'), 'prebuild sincroniza');
    assert.ok(pkg.scripts['sync:content'], 'comando sync:content existe');
  });
});
