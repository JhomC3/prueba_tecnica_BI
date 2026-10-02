import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');

// fetch local: sirve public/ y src/content como el servidor estático.
globalThis.fetch = async (url) => {
  const rel = String(url).replace(/^\.\//, '').replace(/^content\//, 'content/').replace(/^data\//, 'data/').replace(/^charts\//, 'charts/');
  const candidatos = [join(raiz, 'public', rel), join(raiz, 'src', rel), join(raiz, rel)];
  for (const c of candidatos) {
    try {
      const txt = readFileSync(c, 'utf8');
      if (rel.endsWith('.json')) return { json: async () => JSON.parse(txt), text: async () => txt };
      return { json: async () => JSON.parse(txt), text: async () => txt };
    } catch { /* siguiente */ }
  }
  throw new Error('no encontrado: ' + url);
};

function elemento() {
  const slots = {};
  return {
    innerHTML: '',
    querySelector(sel) {
      return (slots[sel] ??= { set innerHTML(v) { this.html = v; }, html: '' });
    },
    _slots: slots,
  };
}

describe('renderizado sin errores', () => {
  it('resumen menciona ambos casos sin hallazgos inventados', async () => {
    const { renderResumen } = await import('../../src/views/summary.js');
    const el = elemento();
    await renderResumen(el);
    assert.ok(el.innerHTML.includes('Caso CRO'));
    assert.ok(el.innerHTML.includes('Caso CFO'));
  });
  it('caso cro: apertura, 6 escenas y respaldo de 3 grupos', async () => {
    const { renderCaso } = await import('../../src/views/case.js');
    const el = elemento();
    await renderCaso(el, 'cro');
    assert.ok(el.innerHTML.includes('Preocupación del directivo'), 'apertura con cita literal');
    assert.equal((el.innerHTML.match(/class="escena"/g) || []).length, 6);
    assert.ok(el.innerHTML.includes('Fuentes, método y respuestas al reto'), 'respaldo único');
    assert.ok(el.innerHTML.includes('Definiciones y límites'));
    assert.ok(el.innerHTML.includes('Fuentes y material de soporte'));
    assert.ok(!el.innerHTML.includes('class="componente"'), 'sin fichas históricas en la web');
    assert.ok(!el.innerHTML.includes('Pendiente de desarrollar'), 'sin estados obsoletos en la web');
    const c = JSON.parse(leer('src/content/cro.json'));
    assert.equal(c.componentes.length, 13, 'componentes conservados en la fuente');
    assert.equal(c.preguntas.length, 11, 'preguntas conservadas en la fuente');
  });
  it('figura genérica: otras columnas y rutas sin cambiar el renderizador', async () => {
    const { renderFigura } = await import('../../src/views/case.js');
    const html = await renderFigura({
      id: 'prueba-config',
      titulo: 'Tabla de prueba configurable',
      datos_src: 'data/new_serie_referencia.json',
      tabla: {
        caption: 'Solo meses y entradas (config de prueba)',
        columnas: [
          { campo: 'mes', etiqueta: 'Mes prueba' },
          { campo: 'entradas_new', etiqueta: 'Entradas prueba', formato: 'entero' },
        ],
      },
    });
    assert.ok(html.includes('Solo meses y entradas (config de prueba)'));
    assert.ok(html.includes('Mes prueba') && html.includes('Entradas prueba'));
    assert.ok(!html.includes('Variación mensual'), 'las columnas vienen del contrato');
    assert.ok(!html.includes('<iframe'), 'sin iframe cuando no se declara');
  });
  it('caso cfo: apertura simétrica, f-modelo y respaldo útil', async () => {
    const { renderCaso } = await import('../../src/views/case.js');
    const el = elemento();
    await renderCaso(el, 'cfo');
    assert.ok(el.innerHTML.includes('Pregunta a priorizar'));
    assert.ok(el.innerHTML.includes('Ejemplos de clasificación'));
    assert.ok(!el.innerHTML.includes('class="componente"'), 'sin fichas históricas en la web');
    assert.ok(!el.innerHTML.includes('Pendiente de desarrollar'), 'sin estados obsoletos en la web');
    const c = JSON.parse(leer('src/content/cfo.json'));
    assert.equal(c.componentes.length, 13, 'componentes conservados en la fuente');
    assert.equal(c.preguntas.length, 14, 'preguntas conservadas en la fuente');
  });
  it('explorar: aviso sin controles funcionales', async () => {
    const { renderExplorar } = await import('../../src/views/explore.js');
    const el = elemento();
    await renderExplorar(el);
    assert.ok(el.innerHTML.includes('Pendiente de integración'));
    assert.ok(!/<button|<form|<input/.test(el.innerHTML));
  });
});
