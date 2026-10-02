// Gate de vocabulario y coherencia: falla ante etiquetas o términos fuera del contrato.
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const raiz = new URL('..', import.meta.url).pathname;
const vocab = JSON.parse(readFileSync(join(raiz, 'src/vocabulary.json'), 'utf8'));
const errores = [];
const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');

// 1. Contenidos: 13 componentes en orden, estados válidos, preguntas literales no vacías.
for (const nombre of ['cro.json', 'cfo.json']) {
  const c = JSON.parse(readFileSync(join(raiz, `src/content/${nombre}`), 'utf8'));
  const nums = c.componentes.map((k) => k.numero);
  if (JSON.stringify(nums) !== JSON.stringify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])) {
    errores.push(`${nombre}: componentes fuera del orden 1–13`);
  }
  for (const k of c.componentes) {
    if (!['disponible', 'en_revision', 'pendiente'].includes(k.estado)) errores.push(`${nombre} comp ${k.numero}: estado inválido`);
    if (k.estado === 'pendiente' && k.respuesta) errores.push(`${nombre} comp ${k.numero}: pendiente con respuesta`);
    if (k.evidencia && !vocab.tipos_evidencia.includes(etiquetaEvidencia(k.evidencia.tipo))) {
      errores.push(`${nombre} comp ${k.numero}: tipo de evidencia fuera de vocabulario`);
    }
  }
  for (const p of c.preguntas) {
    if (!p.pregunta || !p.pregunta.trim()) errores.push(`${nombre} ${p.id}: pregunta vacía`);
    if (p.estado === 'disponible' && !p.que_medimos && !p.evidencia_necesaria) {
      errores.push(`${nombre} ${p.id}: disponible sin bloque de medida ni evidencia`);
    }
    if (p.figura) {
      if (!p.figura.id || !p.figura.titulo) errores.push(`${nombre} ${p.id}: figura sin id/titulo`);
      if (p.figura.tabla && !Array.isArray(p.figura.tabla.columnas)) {
        errores.push(`${nombre} ${p.id}: tabla sin columnas configuradas`);
      }
      if (p.figura.tabla) {
        for (const col of p.figura.tabla.columnas) {
          if (!col.campo || !col.etiqueta) errores.push(`${nombre} ${p.id}: columna sin campo/etiqueta`);
        }
      }
    }
  }
}
function etiquetaEvidencia(t) {
  return { datos_reto: 'Datos del reto', datos_sinteticos: 'Datos sintéticos', propuesta: 'Propuesta', hipotesis: 'Hipótesis' }[t];
}

// 2. Términos prohibidos fuera de contexto de límite (se permite negado: «no ...»).
const textos = readdirSync(join(raiz, 'src/content')).filter((f) => f.endsWith('.json'))
  .map((f) => readFileSync(join(raiz, 'src/content', f), 'utf8')).join('\n');
for (const t of vocab.terminos_prohibidos) {
  const rx = new RegExp(`(?<!no |No |sin |Sin |ni |Ni )${t}`, 'g');
  const m = textos.match(rx);
  if (m) errores.push(`término prohibido sin contexto de límite: «${t}» (${m.length} vez/veces)`);
}

// 3. Serie pública: estructura válida, sin valores fijados; coherente con el manifest.
const serie = JSON.parse(readFileSync(join(raiz, 'public/data/new_serie_referencia.json'), 'utf8'));
const vals = serie.valores || [];
if (!vals.length) errores.push('serie New vacía');
const meses = vals.map((v) => v.mes);
if (JSON.stringify(meses) !== JSON.stringify([...meses].sort())) errores.push('serie New sin orden por mes');
if (new Set(meses).size !== meses.length) errores.push('serie New con meses duplicados');
for (const v of vals) {
  if (!/^\d{4}-\d{2}$/.test(v.mes)) errores.push(`serie New mes inválido: ${v.mes}`);
  if (!Number.isInteger(v.entradas_new) || v.entradas_new < 0) errores.push(`serie New valor inválido en ${v.mes}`);
}
if (vals[0] && vals[0].variacion_mensual_pct !== null) errores.push('el primer mes debe ser «Sin comparación anterior» (null)');
if (String(serie.poblacion || '').includes('seguimiento de 30 días')) {
  errores.push('población de la serie New: el conteo no depende de una ventana de conversión');
}
const manifest = JSON.parse(readFileSync(join(raiz, 'public/data/manifest.json'), 'utf8'));
if (manifest.serie && JSON.stringify(manifest.serie.meses) !== JSON.stringify(meses)) {
  errores.push('manifest.serie.meses difiere de la serie pública');
}
if (manifest.serie && manifest.serie.n_meses !== vals.length) {
  errores.push('manifest.serie.n_meses difiere de la serie pública');
}
for (const c of manifest.contenidos || []) {
  const pub = join(raiz, 'public', c.archivo);
  const src = join(raiz, 'src', c.archivo);
  try {
    if (readFileSync(pub, 'utf8') !== readFileSync(src, 'utf8')) {
      errores.push(`contenido desactualizado: public/${c.archivo} difiere de src/${c.archivo} (falta sync)`);
    }
    if (sha(pub) !== c.sha256) errores.push(`manifest desactualizado para ${c.archivo}`);
  } catch {
    errores.push(`contenido faltante: ${c.archivo}`);
  }
}

if (errores.length) {
  console.error('COHERENCE-FAIL');
  for (const e of errores) console.error(' - ' + e);
  process.exit(1);
}

// 4. Introducción «cómo se construyó»: contrato y archivos precargados.
for (const nombre of ['cro.json', 'cfo.json']) {
  const c = JSON.parse(readFileSync(join(raiz, `src/content/${nombre}`), 'utf8'));
  const d = c.construccion;
  if (!d) errores.push(`${nombre}: falta bloque construccion`);
  else {
    if (d.pregunta !== c.recorrido.pregunta_principal) errores.push(`${nombre}: construccion.pregunta diverge del recorrido`);
    if ((d.originales || []).length !== 3) errores.push(`${nombre}: construccion sin los 3 originales`);
    if ((d.faltante || []).length < 6) errores.push(`${nombre}: construccion con faltante incompleto`);
    if ((d.sinteticos?.tablas || []).length < 8) errores.push(`${nombre}: construccion con tablas insuficientes`);
    for (const t of d.sinteticos?.tablas || []) {
      if (!['fuente', 'derivada'].includes(t.origen)) errores.push(`${nombre}: tabla sin origen válido ${t.archivo}`);
      if (t.origen === 'derivada' && !t.derivacion) errores.push(`${nombre}: derivada sin explicación ${t.archivo}`);
    }
    for (const t of d.sinteticos?.tablas || []) {
      if (t.descarga && !existsSyncPub(t.descarga)) errores.push(`${nombre}: descarga inexistente ${t.descarga}`);
    }
  }
}
function existsSyncPub(rel) {
  try {
    readFileSync(join(raiz, 'public', rel));
    return true;
  } catch {
    return false;
  }
}
try {
  const man = JSON.parse(readFileSync(join(raiz, 'public/data/archivos-manifiesto.json'), 'utf8'));
  for (const s of man.sinteticos || []) {
    const pub = join(raiz, 'public', s.ruta);
    try {
      if (sha(pub) !== s.sha256) errores.push(`archivos-manifiesto desactualizado: ${s.ruta}`);
    } catch {
      errores.push(`archivos-manifiesto sin archivo: ${s.ruta}`);
    }
  }
} catch {
  errores.push('archivos-manifiesto.json faltante o inválido');
}
try {
  const man = JSON.parse(readFileSync(join(raiz, 'public/data/soportes-manifiesto.json'), 'utf8'));
  for (const s of man.archivos || []) {
    const pub = join(raiz, 'public', s.ruta);
    try {
      if (sha(pub) !== s.sha256) errores.push(`soportes-manifiesto desactualizado: ${s.ruta}`);
    } catch {
      errores.push(`soportes-manifiesto sin archivo: ${s.ruta}`);
    }
  }
  const r = JSON.parse(readFileSync(join(raiz, 'src/content/resumen.json'), 'utf8'));
  for (const c of r.casos || []) {
    for (const k of ['decisor', 'preocupacion', 'pregunta_priorizada', 'resultado', 'accion']) {
      if (!c[k]) errores.push(`resumen ${c.caso_id}: sin ${k}`);
    }
  }
  const charts = join(raiz, 'public/charts');
  const sinCdn = [];
  const revisarHtml = (dir) => {
    for (const f of readdirSync(dir, { withFileTypes: true })) {
      const p = join(dir, f.name);
      if (f.isDirectory()) { revisarHtml(p); continue; }
      if (f.name.endsWith('.html')) {
        const html = readFileSync(p, 'utf8');
        if (/src="https:\/\/cdn\.|href="https:\/\/cdn\./.test(html)) sinCdn.push(p);
      }
    }
  };
  revisarHtml(charts);
  for (const p of sinCdn) errores.push(`figura con CDN: ${p}`);
  const ANCLAS = { C01: 'e-new', C02: 'e-plazo', C03: 'e-calidad', C04: 'e-transiciones', C05: 'e-capacidad', S01: 'f-modelo', S02: 'f-modelo', S03: 'f-modelo', S04: 'f-politica', S05: 'f-politica', S06: 'f-recupero', S07: 'f-recupero', S09: 'respaldo', intro: 'intro', cierre: 'cierre', respuestas: 'respaldo', 'adjuntos-cro': 'intro', 'adjuntos-cfo': 'intro', metodo: 'metodo', entrega: 'entrega' };
  const app = readFileSync(join(raiz, 'src/app.js'), 'utf8');
  for (const [a, d] of Object.entries(ANCLAS)) {
    if (!app.includes(`'${d}'`) || !app.includes(a)) errores.push(`ANCLAS sin ${a} → ${d}`);
  }
  for (const nombre of ['cro.json', 'cfo.json']) {
    const c = JSON.parse(readFileSync(join(raiz, `src/content/${nombre}`), 'utf8'));
    const ej = c.ejecutiva;
    if (!ej) errores.push(`${nombre}: falta capa ejecutiva`);
    else {
      const bloqueIds = new Set();
      const capIds = new Set();
      for (const cap of c.recorrido.capitulos) {
        capIds.add(cap.id);
        for (const b of cap.bloques) bloqueIds.add(b.id);
      }
      if (ej.apertura.pregunta_editorial && ej.apertura.pregunta_editorial === c.recorrido.pregunta_principal) {
        errores.push(`${nombre}: pregunta editorial idéntica a la original`);
      }
      for (const p of ej.apertura.preguntas || []) {
        if (!p.texto || !p.ref) errores.push(`${nombre}: pregunta sin texto/ref`);
        else if (!bloqueIds.has(p.ref) && !capIds.has(p.ref)) errores.push(`${nombre}: pregunta con ref inexistente ${p.ref}`);
      }
      for (const e of ej.escenas || []) {
        for (const b of e.bloques || []) {
          if (!bloqueIds.has(b)) errores.push(`${nombre}: escena ${e.id} sin bloque ${b}`);
        }
        for (const b of (e.detalle || {}).bloques || []) {
          if (!bloqueIds.has(b)) errores.push(`${nombre}: detalle ${e.id} sin bloque ${b}`);
        }
      }
    }
  }
} catch {
  errores.push('soportes-manifiesto.json faltante o inválido');
}

if (errores.length) {
  console.error('COHERENCE-FAIL');
  for (const e of errores) console.error(' - ' + e);
  process.exit(1);
}
console.log('COHERENCE-OK: 13+13 componentes, figuras configurables, serie estructurada y sincronizada.');
