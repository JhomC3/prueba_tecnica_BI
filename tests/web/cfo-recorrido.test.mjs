import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');

describe('contrato de recorrido CFO', () => {
  it('recorrido S01–S09 + cierre con bloques evidencia→conclusion→conexion', () => {
    const c = JSON.parse(leer('src/content/cfo.json'));
    assert.ok(c.recorrido && c.recorrido.capitulos && c.recorrido.cierre);
    assert.deepEqual(c.recorrido.capitulos.map((k) => k.id), ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S09']);
    assert.ok(c.recorrido.pregunta_principal && c.recorrido.proposito && c.recorrido.alcance);
    assert.ok(c.recorrido.cierre.sintesis && c.recorrido.cierre.acciones.tabla && c.recorrido.cierre.evaluacion);
    for (const cap of c.recorrido.capitulos) {
      assert.ok(cap.pregunta_literal && cap.que_medimos && cap.alcance && cap.metrica_formula && cap.datos);
      assert.ok(Array.isArray(cap.bloques) && cap.bloques.length >= 1);
      for (const b of cap.bloques) {
        assert.ok(b.conclusion && b.siguiente_analisis, `bloque ${b.id} con conclusion y conexion`);
        assert.ok(b.visibilidad);
        if (b.figura) assert.ok(b.figura.titulo && b.figura.iframe_src);
      }
    }
  });
  it('conclusiones sin prefijos duplicados', () => {
    const c = JSON.parse(leer('src/content/cfo.json'));
    const textos = [];
    for (const cap of c.recorrido.capitulos) for (const b of cap.bloques) textos.push([b.id, b.conclusion]);
    textos.push(['cierre', c.recorrido.cierre.sintesis], ['acciones', c.recorrido.cierre.acciones.conclusion]);
    for (const [id, t] of textos) {
      assert.ok(!/^(Conclusión|Resultado|Conclusión final)\s*:/.test(t.trim()), `bloque ${id} sin prefijo duplicado`);
    }
  });
  it('seleccion primaria trazada y preguntas de referencia intactas', () => {
    const mapa = JSON.parse(leer('docs/web/cfo-mapa.json'));
    assert.equal(mapa.seleccion_primaria.length, 2);
    const c = JSON.parse(leer('src/content/cfo.json'));
    assert.equal(c.preguntas.length, 14);
    assert.equal(c.componentes.length, 13);
  });
  it('indice CFO con anclas por ruta', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes("#/${ruta}/"), 'indice conserva la ruta del caso');
    assert.ok(vista.includes("escenaHTML(e, lookup, ruta)"), 'escenas ejecutivas sobre bloques existentes');
    assert.ok(vista.includes('id="respaldo"'), 'respaldo plegado con ancla propia');
  });
  it('figuras CFO exportadas y manifiesto coherente', () => {
    const m = JSON.parse(leer('public/data/cfo-story-manifest.json'));
    assert.equal(m.figuras.length, 2);
    assert.ok(m.validaciones.bruto_menos_descuento_igual_neto);
    assert.equal(m.validaciones.diferencia_acumulada, -1500.0);
  });
});
