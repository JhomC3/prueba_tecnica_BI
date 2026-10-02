import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const raiz = new URL('../..', import.meta.url).pathname;
const leer = (p) => readFileSync(join(raiz, p), 'utf8');
const sha = (p) => createHash('sha256').update(readFileSync(join(raiz, p))).digest('hex');

describe('contrato de construccion CRO+CFO', () => {
  for (const caso of ['cro', 'cfo']) {
    it(`${caso}: pregunta literal sin duplicar recorrido`, () => {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      const d = c.construccion;
      assert.ok(d, 'construccion presente');
      assert.equal(d.pregunta, c.recorrido.pregunta_principal);
      assert.equal(d.proposito, c.recorrido.proposito);
      assert.ok(d.puente && d.puente.length > 20);
    });
    it(`${caso}: tres originales recibidos sin descarga`, () => {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      const nombres = c.construccion.originales.map((o) => o.nombre);
      assert.deepEqual(nombres, ['Transactions.csv', 'Industry.csv', 'S&M_spend.csv']);
      for (const o of c.construccion.originales) {
        assert.equal(o.estado, 'recibido');
        assert.ok(o.descripcion && o.aporta && o.limite);
        assert.equal(o.descarga, null);
      }
      assert.ok(c.construccion.nota_originales.includes('sintéticos'));
    });
    it(`${caso}: faltante y sinteticos con necesidades`, () => {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      assert.ok(c.construccion.resumen && c.construccion.resumen.length > 20, 'resumen visible');
      assert.equal(c.construccion.faltante.length, 6);
      assert.ok(c.construccion.sinteticos.etiqueta.includes('sintéticos'));
      assert.ok(c.construccion.sinteticos.tablas.length >= 8);
      for (const t of c.construccion.sinteticos.tablas) {
        assert.ok(t.archivo && t.necesidad);
        assert.ok(['fuente', 'derivada'].includes(t.origen), `origen válido en ${t.archivo}`);
        if (t.origen === 'derivada') assert.ok(t.derivacion, `derivación explicada en ${t.archivo}`);
      }
    });
    it(`${caso}: sin rutas locales como enlaces`, () => {
      const txt = leer(`src/content/${caso}.json`);
      assert.ok(!txt.includes('/Users/'), 'sin rutas del ordenador');
    });
  }
  it('cfo enlaza S02/S03 sin repetir tablas', () => {
    const c = JSON.parse(leer('src/content/cfo.json'));
    assert.deepEqual(c.construccion.enlaces_recorrido.map((e) => e.ancla), ['S02', 'S03']);
  });
  it('descargas apuntan a archivos reales con hash de manifiesto', () => {
    const man = JSON.parse(leer('public/data/archivos-manifiesto.json'));
    const porRuta = new Map(man.sinteticos.map((s) => [s.ruta, s]));
    for (const caso of ['cro', 'cfo']) {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      for (const t of c.construccion.sinteticos.tablas) {
        if (!t.descarga) continue;
        const pub = join('public', t.descarga);
        assert.ok(existsSync(join(raiz, pub)), `existe ${t.descarga}`);
        const e = porRuta.get(t.descarga);
        assert.ok(e, `manifiesto cubre ${t.descarga}`);
        assert.equal(e.sha256, sha(pub));
      }
    }
    for (const o of man.originales) assert.equal(o.descarga, null);
    for (const d of man.derivados) assert.ok(existsSync(join(raiz, 'public', d.ruta)));
  });
  it('derivadas distinguidas de fuentes', () => {
    const cro = JSON.parse(leer('src/content/cro.json')).construccion.sinteticos.tablas;
    const g = cro.find((t) => t.archivo === 'ganados.csv');
    assert.equal(g.origen, 'derivada');
    assert.ok(g.derivacion.includes('vw_ganados'));
    const cfo = JSON.parse(leer('src/content/cfo.json')).construccion.sinteticos.tablas;
    for (const a of ['con_descuento/componentes_mes.csv', 'con_descuento/movimientos.csv']) {
      const t = cfo.find((x) => x.archivo === a);
      assert.equal(t.origen, 'derivada');
    }
    assert.ok(cfo.filter((t) => t.origen === 'fuente').length >= 7);
  });
  it('apertura común A–F sin CSV ni estados', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('Pregunta a priorizar'), 'rótulo común');
    assert.ok(vista.includes('preguntas-priorizadas'), 'lista en cursiva');
    assert.ok(!vista.includes('Archivos recibidos'), 'sin rótulo de archivos en apertura');
    assert.ok(!vista.includes('.csv'), 'sin nombres CSV en el render de apertura');
  });
  it('respaldo de 3 grupos plegados, sin archivo histórico', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('Fuentes, método y respuestas al reto'), 'etiqueta única');
    assert.ok(vista.includes('Definiciones y límites'), 'grupo 1');
    assert.ok(vista.includes('Fuentes y material de soporte'), 'grupo 2');
    assert.ok(!vista.includes('class="componente"'), 'sin fichas en el render');
    assert.ok(!vista.includes('Pendiente de desarrollar'), 'sin estados obsoletos en el render');
    assert.ok(!vista.includes('preguntaHTML'), 'sin inventario renderizado');
    for (const caso of ['cro', 'cfo']) {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      assert.ok(c.respaldo && c.respaldo.definiciones.items.length >= 5, `${caso} con definiciones`);
      assert.ok(c.componentes.length === 13 && c.preguntas.length >= 11, `${caso} historial conservado en fuente`);
      for (const r of c.respuestas_reto) {
        for (const e of r.evidencia) {
          assert.ok(['respaldo', 'cierre', 'intro', 'e-new', 'e-plazo', 'e-conversion', 'e-calidad', 'e-transiciones', 'e-capacidad', 'f-modelo', 'f-politica', 'f-recupero'].includes(e.ancla), `${r.id} con destino útil ${e.ancla}`);
        }
      }
    }
  });
  it('widget de adjuntos retirado por completo', () => {
    const vista = leer('src/views/case.js');
    for (const s of ['adjuntosHTML', 'conectarAdjuntos', 'adjuntosSel', 'type="file"', 'Limpiar la selección', 'Seleccionado localmente', 'Adjuntar información']) {
      assert.ok(!vista.includes(s), `sin resto del widget: ${s}`);
    }
  });
  it('apertura común sin editor ni estados, sin adjuntos', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('sintesis_preocupacion'), 'síntesis diferenciada');
    assert.ok(vista.includes('Pregunta a priorizar'), 'rótulo común');
    assert.ok(vista.includes('preguntas-priorizadas'), 'lista en cursiva');
    assert.ok(!vista.includes('Editar pregunta'), 'sin botón de edición');
    assert.ok(!vista.includes('conectarPregunta') && !vista.includes('preguntaLocal'), 'sin conexiones del editor');
    assert.ok(vista.includes('preguntas-priorizadas'), 'lista en cursiva');
    assert.ok(!vista.includes('ver_tambien'), 'sin saltos al respaldo desde escenas');
    assert.ok(leer('src/styles.css').includes('.ejecutiva a'), 'enlaces con color coherente');
    assert.ok(!vista.includes('Archivos recibidos'), 'sin rótulo de archivos en apertura');
  });
  it('mediana con síntesis visible y original en detalle; f-modelo presente', () => {
    const cro = JSON.parse(leer('src/content/cro.json'));
    const plazo = cro.ejecutiva.escenas.find((e) => e.id === 'e-plazo');
    assert.ok(plazo.sintesis && plazo.sintesis.includes('Conservamos 30'));
    assert.ok(!plazo.transicion, 'sin cabecera duplicada');
    const cfo = JSON.parse(leer('src/content/cfo.json'));
    const mod = cfo.ejecutiva.escenas.find((e) => e.id === 'f-modelo');
    assert.ok(mod && mod.bloques.includes('S03-modelo'));
    assert.ok(mod.limite.includes('MRR neto'));
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('Conclusión original:'), 'original preservada en detalle');
  });
  it('superficie ejecutiva con respaldo plegado y anclas conservadas', () => {
    const vista = leer('src/views/case.js');
    assert.ok(vista.includes('aperturaHTML(c.ejecutiva.apertura'), 'apertura ejecutiva');
    assert.ok(vista.includes('escenaHTML(e, lookup, ruta)'), 'escenas sobre bloques');
    assert.ok(vista.includes('cierreEjecutivoHTML'), 'cierre ejecutivo');
    assert.ok(vista.includes('respaldoHTML(c, ruta)'), 'respaldo de 3 grupos');
    assert.ok(leer('src/app.js').includes('ANCLAS_ANTIGUAS'), 'anclas antiguas mapeadas');
    assert.ok(vista.includes('id="intro"'), 'apertura como destino de intro');
  });
  it('capa ejecutiva: apertura literal, escenas sobre bloques reales y límites', () => {
    const citas = [
      'Estamos generando más leads, pero no estamos vendiendo más',
      '¿Por qué cambió nuestro MRR?',
    ];
    for (const caso of ['cro', 'cfo']) {
      const c = JSON.parse(leer(`src/content/${caso}.json`));
      const ej = c.ejecutiva;
      assert.ok(ej && ej.apertura.cita_titular && ej.apertura.cita_completa);
      assert.ok(ej.apertura.pregunta_editorial || ej.apertura.pregunta_despues, 'pregunta a priorizar');
      if (caso === 'cfo') assert.equal(ej.apertura.pregunta_despues, c.recorrido.pregunta_principal);
      assert.ok(citas.includes(ej.apertura.cita_titular), `${caso}: titular literal del reto`);
      assert.ok(ej.apertura.cita_completa.length > ej.apertura.cita_titular.length);
      const bloqueIds = new Set();
      for (const cap of c.recorrido.capitulos) for (const b of cap.bloques) bloqueIds.add(b.id);
      assert.ok(ej.escenas.length >= 2);
      for (const e of ej.escenas) {
        assert.ok(e.titulo && e.puente !== undefined && e.limite !== undefined);
        for (const b of e.bloques || []) assert.ok(bloqueIds.has(b), `escena ${e.id} referencia bloque real ${b}`);
      }
      if (ej.cierre) {
        assert.ok(ej.cierre.decision && ej.cierre.responsable && ej.cierre.exito && ej.cierre.supuestos);
      }
      assert.ok(ej.apertura.sintesis_preocupacion && ej.apertura.sintesis_preocupacion.length > 20, 'síntesis diferenciada');
      if (caso === 'cfo') {
        assert.ok(!('s01_breve' in ej.apertura), 'ejemplos solo junto a f-modelo');
        const mod = ej.escenas.find((e) => e.id === 'f-modelo');
        assert.ok(mod.detalle && mod.detalle.titulo === 'Ejemplos de clasificación', 'detalle de ejemplos');
      }
      assert.ok(!ej.apertura.nota, 'sin instrucciones internas en apertura');
    }
    const superficie = leer('src/views/case.js');
    for (const f of ['Tensiones a introducir', 'Textos originales en S01', 'no sustituyen la pregunta inicial']) {
      assert.ok(!superficie.includes(f), `superficie sin frase interna: ${f}`);
    }
  });
});
