import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');

describe('navegación y accesibilidad', () => {
  it('cuatro rutas con enlace directo (hash, recargable sin servidor)', () => {
    const app = leer('src/app.js');
    for (const r of ['resumen', 'cro', 'cfo', 'explorar']) {
      assert.ok(app.includes(r), `ruta ${r}`);
    }
    const html = leer('index.html');
    for (const r of ['resumen', 'cro', 'cfo', 'explorar']) {
      assert.ok(html.includes(`#/${r}`), `enlace #/${r}`);
    }
  });
  it('documento accesible: idioma, salto, aria-current, foco visible', () => {
    const html = leer('index.html');
    assert.ok(html.includes('lang="es"'));
    assert.ok(html.includes('Saltar al contenido'));
    assert.ok(leer('src/app.js').includes('aria-current'));
    assert.ok(leer('src/styles.css').includes(':focus-visible'));
  });
  it('sin controles de formulario: lectura sin Adjuntar ni envíos', () => {
    const vistas = leer('src/app.js') + leer('src/views/summary.js') + leer('src/views/case.js') + leer('src/views/explore.js');
    assert.ok(!/onclick|onkeydown|<form|<input|<button|Adjuntar/.test(vistas), 'sin formularios, botones ni adjuntos');
    assert.ok(leer('src/views/case.js').includes('<details>'), 'cálculos plegados con details');
    assert.ok(leer('src/views/case.js').includes('title='), 'iframe con título accesible');
    assert.ok(leer('src/views/case.js').includes('loading="lazy"'), 'figura con carga diferida');
  });
  it('adaptación móvil: viewport y breakpoint', () => {
    assert.ok(leer('index.html').includes('name="viewport"'));
    assert.ok(leer('src/styles.css').includes('@media'));
  });
});
