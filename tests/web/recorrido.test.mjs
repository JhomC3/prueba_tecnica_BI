import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');

describe('contrato de recorrido CRO', () => {
  it('recorrido C01–C05 + cierre con bloques figura→conclusion→motivo', () => {
    const c = JSON.parse(leer('src/content/cro.json'));
    assert.ok(c.recorrido && c.recorrido.capitulos && c.recorrido.cierre);
    assert.deepEqual(c.recorrido.capitulos.map((k) => k.id), ['C01', 'C02', 'C03', 'C04', 'C05']);
    assert.ok(c.recorrido.pregunta_principal && c.recorrido.proposito && c.recorrido.alcance);
    assert.ok(c.recorrido.cierre.sintesis && c.recorrido.cierre.acciones.tabla);
    for (const cap of c.recorrido.capitulos) {
      assert.ok(cap.pregunta_literal && cap.que_medimos && cap.alcance && cap.metrica_formula && cap.datos);
      assert.ok(Array.isArray(cap.bloques) && cap.bloques.length >= 1);
      for (const b of cap.bloques) {
        assert.ok(b.conclusion && b.siguiente_analisis, `bloque ${b.id} con conclusion y motivo`);
        assert.ok(b.visibilidad);
        if (b.figura) assert.ok(b.figura.titulo && b.figura.iframe_src);
      }
    }
  });
  it('cierre CRO: criterios comunes una vez, sin duplicados', () => {
    const c = JSON.parse(leer('src/content/cro.json'));
    const acc = c.recorrido.cierre.acciones;
    assert.ok(acc.evaluacion_comun && acc.evaluacion_comun.includes('octubre–noviembre de 2026'));
    assert.deepEqual(acc.tabla.columnas.map((col) => col.campo), ['hallazgo', 'accion', 'responsable']);
    for (const f of acc.tabla.filas) assert.ok(!('evaluacion' in f), 'sin evaluación repetida por fila');
    assert.ok(!acc.conclusion.includes('No se han ejecutado intervenciones'), 'aviso único en la nota');
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('evaluacion_comun'), 'criterios comunes tras la tabla');
  });
  it('conclusiones sin prefijos duplicados', () => {
    const c = JSON.parse(leer('src/content/cro.json'));
    const textos = [];
    for (const cap of c.recorrido.capitulos) for (const b of cap.bloques) textos.push([b.id, b.conclusion]);
    textos.push(['cierre', c.recorrido.cierre.sintesis], ['acciones', c.recorrido.cierre.acciones.conclusion]);
    for (const [id, t] of textos) {
      assert.ok(!/^(Conclusión|Resultado|Conclusión final)\s*:/.test(t.trim()), `bloque ${id} sin prefijo duplicado`);
    }
  });
  it('seleccion primaria trazada y preguntas de referencia intactas', () => {
    const mapa = JSON.parse(leer('docs/web/cro-mapa.json'));
    assert.equal(mapa.seleccion_primaria.length, 7);
    const c = JSON.parse(leer('src/content/cro.json'));
    assert.equal(c.preguntas.length, 11);
    assert.equal(c.componentes.length, 13);
  });
  it('renderizador sin cifras, rutas ni notas internas visibles', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('bloqueHTML') && vista.includes('escenaHTML') && vista.includes('respaldoHTML'));
    assert.ok(!vista.includes('133') && !vista.includes('179'), 'sin cifras fijadas en vistas');
    assert.ok(!vista.includes('charts/cro-story/'), 'sin rutas de historia fijadas en renderizador');
    assert.ok(!vista.includes('21,1'), 'sin tasas fijadas');
    assert.ok(!vista.includes('Procedencia') && !vista.includes('celdas'), 'sin notas internas visibles');
  });
  it('indice con anclas por ruta', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('#/${ruta}/'), 'indice conserva la ruta del caso');
    const app = leer('src/app.js');
    assert.ok(app.includes("split('/')"), 'router separa ruta y ancla');
    assert.ok(app.includes('rutaVista'), 'router re-renderiza al cambiar de caso aunque el ancla coincida');
  });
  it('CFO usa el mismo contrato de recorrido con su respaldo', () => {
    const cfo = JSON.parse(leer('src/content/cfo.json'));
    assert.ok(cfo.recorrido && cfo.recorrido.capitulos);
    assert.equal(cfo.componentes.length, 13);
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes("aperturaHTML(c.ejecutiva.apertura"), 'apertura con preocupación literal');
  });
});
