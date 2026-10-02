import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');
const sha = (p) => createHash('sha256').update(readFileSync(join(raiz, p))).digest('hex');

describe('inicio ejecutivo y entrega', () => {
  it('resumen con dos casos veraces y accesos', () => {
    const r = JSON.parse(leer('src/content/resumen.json'));
    assert.equal(r.casos.length, 2);
    for (const c of r.casos) {
      assert.ok(c.decisor && c.preocupacion && c.pregunta_priorizada && c.resultado && c.accion);
    }
    assert.ok(!JSON.stringify(r).includes('Sin modelo ejecutado'), 'sin estados obsoletos');
    assert.ok(!JSON.stringify(r).includes('Sin diagnóstico ni intervención elegida'), 'sin estados obsoletos');
    assert.ok(r.nota_comun && r.metodo && r.entrega);
  });
  it('respuestas al reto con preguntas literales y anclas', () => {
    for (const [caso, n] of [['cro', 4], ['cfo', 5]]) {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      assert.equal(c.respuestas_reto.length, n);
      for (const r of c.respuestas_reto) {
        assert.ok(r.pregunta && r.respuesta && r.evidencia.length >= 1);
      }
    }
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('respuestasHTML'), 'render de respuestas');
    assert.ok(vista.includes('id="respuestas"'), 'sección enlazable');
  });
  it('nota, guiones y soportes publicados con hash', () => {
    for (const d of ['public/docs/nota-corta.md', 'public/docs/guion-video-ejecutivo.md', 'public/docs/guion-video-proceso-ia.md']) {
      assert.ok(existsSync(join(raiz, d)), `existe ${d}`);
    }
    const man = JSON.parse(leer('public/data/soportes-manifiesto.json'));
    assert.equal(man.archivos.length, 8);
    for (const s of man.archivos) {
      assert.ok(existsSync(join(raiz, 'public', s.ruta)), `existe ${s.ruta}`);
      assert.equal(s.sha256, sha(join('public', s.ruta)));
    }
    const r = JSON.parse(leer('src/content/resumen.json'));
    for (const s of r.entrega.soportes) {
      assert.ok(man.archivos.some((m) => m.ruta === s.archivo), `soporte en manifiesto: ${s.archivo}`);
    }
    assert.equal(r.entrega.nota_corta, 'docs/nota-corta.md');
  });
  it('figuras activas sin CDN con biblioteca local compartida', () => {
    const lib = join(raiz, 'public/charts/plotly.min.js');
    assert.ok(existsSync(lib), 'biblioteca compartida existe');
    assert.ok(readFileSync(lib, 'utf8').includes('plotly.js v4.1.1'), 'versión requerida conservada');
    const activas = [];
    for (const caso of ['cro', 'cfo']) {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      for (const cap of c.recorrido.capitulos) for (const b of cap.bloques) {
        if (b.figura && b.figura.iframe_src) activas.push(b.figura.iframe_src);
      }
    }
    assert.ok(activas.length >= 14, `figuras activas localizadas (${activas.length})`);
    for (const a of activas) {
      const html = leer(`public/${a}`);
      assert.ok(!/src="https:\/\/cdn\.|href="https:\/\/cdn\./.test(html), `sin CDN: ${a}`);
      assert.ok(html.includes('../plotly.min.js'), `cargador local: ${a}`);
    }
    for (const m of ['public/data/cro-story-manifest.json', 'public/data/cfo-story-manifest.json']) {
      assert.ok(JSON.parse(leer(m)).plotly_lib, `manifiesto con biblioteca: ${m}`);
    }
  });
});
