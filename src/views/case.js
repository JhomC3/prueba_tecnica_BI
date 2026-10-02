const base = (import.meta.env?.BASE_URL) || './';

function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

const ESTADO = { disponible: 'Disponible', en_revision: 'En revisión', pendiente: 'Pendiente' };
const EVIDENCIA = {
  datos_reto: 'Datos del reto',
  datos_sinteticos: 'Datos sintéticos',
  propuesta: 'Propuesta',
  hipotesis: 'Hipótesis'
};



function formatoCelda(valor, col) {
  if (valor === null || valor === undefined || valor === '') return esc(col.nulo || '—');
  if (col.formato === 'pct1') {
    const n = Number(valor);
    if (Number.isNaN(n)) return esc(String(valor));
    return esc(n.toFixed(1)) + ' %';
  }
  return esc(String(valor));
}

function tablaHTML(filas, tabla) {
  const cols = tabla.columnas || [];
  const thead = cols.map((c) => `<th scope="col">${esc(c.etiqueta || c.campo)}</th>`).join('');
  const cuerpo = (filas || []).map((f) => {
    const tds = cols.map((c, i) => {
      const v = formatoCelda(f[c.campo], c);
      const num = c.formato === 'entero' || c.formato === 'pct1' ? ' class="num"' : '';
      const th = i === 0 ? ` scope="row"` : '';
      const tag = i === 0 ? 'th' : 'td';
      return `<${tag}${th}${num}>${v}</${tag}>`;
    }).join('');
    return `<tr>${tds}</tr>`;
  }).join('');
  return `
    <div class="tabla-scroll" tabindex="0" role="region" aria-label="${esc(tabla.caption || 'Tabla de la figura')}">
    <table>
      <caption>${esc(tabla.caption || 'Tabla de la figura')}</caption>
      <thead><tr>${thead}</tr></thead>
      <tbody>${cuerpo}</tbody>
    </table>
    </div>`;
}

function metaHTML(d) {
  if (!d) return '';
  const partes = [];
  if (d.contexto) partes.push(`Contexto y supuestos fuera de la figura: ${esc(d.contexto)}.`);
  if (d.fuente) partes.push(`Fuente: ${esc(d.fuente)}.`);
  if (d.periodo) partes.push(`Periodo: ${esc(d.periodo)}.`);
  if (d.poblacion) partes.push(`Población: ${esc(d.poblacion)}.`);
  if (d.unidad) partes.push(`Unidad: ${esc(d.unidad)}.`);
  if (d.escenario) partes.push(`Escenario: ${esc(d.escenario)}.`);
  if (!partes.length) return '';
  return `<p class="nota">${partes.join(' ')}</p>`;
}

export async function renderFigura(figura) {
  if (!figura) return '';
  let datos = null;
  if (figura.datos_src) {
    const r = await fetch(`${base}${figura.datos_src}`);
    datos = await r.json();
  }
  const filas = datos?.valores || datos?.filas || figura.tabla?.filas || [];
  const etiqueta = datos?.nota_etiqueta ? ` · ${esc(datos.nota_etiqueta)}` : '';
  const iframe = figura.iframe_src ? `
      <div class="figura-marco">
        <iframe title="${esc(figura.titulo)} — figura interactiva existente"
          src="${base}${esc(figura.iframe_src)}" loading="lazy"></iframe>
      </div>` : '';
  const tabla = figura.tabla ? tablaHTML(filas, figura.tabla) : '';
  return `
    <figure>
      <figcaption><strong>${esc(figura.titulo)}</strong>${etiqueta}</figcaption>
      ${iframe}
      ${metaHTML(datos)}
    </figure>
    ${tabla}`;
}

function respuestasHTML(lista, ruta) {
  if (!lista || !lista.length) return '';
  return (lista || []).map((r) => `
    <details id="${esc(r.id)}"><summary>${esc(r.pregunta)}</summary>
      <p>${esc(r.respuesta)}</p>
      <ul>${(r.evidencia || []).map((e) => `<li><a href="#/${ruta}/${esc(e.ancla)}">${esc(e.texto)}</a></li>`).join('')}</ul>
    </details>`).join('');
}

function respaldoHTML(c, ruta) {
  const r = c.respaldo || {};
  const def = r.definiciones || {};
  const fue = r.fuentes || {};
  return `
    <details id="respaldo"><summary>${esc(r.etiqueta || 'Fuentes, método y respuestas al reto')}</summary>
    <section aria-label="${esc(def.titulo || 'Definiciones y límites')}">
      <h3>${esc(def.titulo || 'Definiciones y límites')}</h3>
      <dl>${((def.items) || []).map((i) => `<dt><strong>${esc(i.termino)}</strong></dt><dd>${esc(i.definicion)}</dd>`).join('')}</dl>
    </section>
    <section aria-label="${esc(fue.titulo || 'Fuentes y material de soporte')}">
      <h3>${esc(fue.titulo || 'Fuentes y material de soporte')}</h3>
      <p><strong>Recibidas:</strong> ${esc(fue.recibidas || '')}</p>
      <p><strong>Sintéticos:</strong> ${esc(fue.sinteticos || '')}</p>
      <p><strong>Derivadas:</strong> ${esc(fue.derivadas || '')}</p>
      <ul>${((fue.descargas) || []).map((d) => `<li><a href="${base}${esc(d.ruta)}" download>${esc(d.archivo)}</a> — ${esc(d.descripcion)}</li>`).join('')}</ul>
      <p class="nota">${esc(fue.nota || '')} <a href="#/resumen/entrega">Soportes completos en la entrega</a>.</p>
    </section>
    <section aria-label="Respuestas al reto" id="respuestas">
      <h3>Respuestas al reto</h3>
      ${respuestasHTML(c.respuestas_reto, ruta)}
    </section>
    </details>`;
}

function mapaBloques(recorrido) {
  const m = new Map();
  for (const cap of recorrido.capitulos || []) for (const b of cap.bloques || []) m.set(b.id, { cap, b });
  return m;
}

function figuraHTML(figura, sinCabecera) {
  if (!figura) return '';
  return `
    <figure>
      ${sinCabecera ? '' : `<figcaption><strong>${esc(figura.titulo)}</strong></figcaption>`}
      <div class="figura-marco">
        <iframe title="${esc(figura.titulo)} — figura interactiva"
          src="${base}${esc(figura.iframe_src)}" loading="lazy"></iframe>
      </div>
    </figure>`;
}

function detalleHTML(cap, b, resumido) {
  const tabla = b.tabla ? tablaHTML(b.tabla.filas, b.tabla) : '';
  const lista = b.lista ? `<ul>${b.lista.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>` : '';
  return `
      <details><summary>Ver detalle del análisis</summary>
        ${resumido ? `<p><strong>Conclusión original:</strong> ${esc(b.conclusion)}</p>` : ''}
        <p><strong>Qué medimos:</strong> ${esc(cap.que_medimos)}</p>
        <p><strong>Alcance mostrado:</strong> ${esc(cap.alcance)}</p>
        <p><strong>Métrica/fórmula:</strong> ${esc(cap.metrica_formula)}</p>
        <p><strong>Datos:</strong> ${esc(cap.datos)}</p>
        ${lista}
        ${tabla}
        <p><strong>Motivo técnico del análisis:</strong> ${esc(b.siguiente_analisis)}</p>
      </details>`;
}

function bloqueEjecutivoHTML(entrada, resumido, sinCabecera) {
  const { cap, b } = entrada;
  return `
    <div class="bloque" data-bloque="${esc(b.id)}">
      ${figuraHTML(b.figura, sinCabecera)}
      ${resumido ? '' : `<p><strong>Conclusión:</strong> ${esc(b.conclusion)}</p>`}
      ${detalleHTML(cap, b, resumido)}
    </div>`;
}

function aperturaHTML(a, c, ruta, caso) {
  const pregunta = a.pregunta_editorial || a.pregunta_despues;
  const preguntas = (a.preguntas || []).map((p) => `<li>${esc(p.texto)}${p.nota ? ` <span class="nota">${esc(p.nota)}</span>` : ''}</li>`).join('');
  const datos = (a.datos || []).map((t) => `<li>${esc(t)}</li>`).join('');
  return `
    <section class="apertura" id="intro" aria-label="Preocupación del directivo">
      <p class="cita-titular">«${esc(a.cita_titular)}»</p>
      <blockquote>${esc(a.cita_completa)}</blockquote>
      <p class="sintesis">${esc(a.sintesis_preocupacion || '')}</p>
      <p><strong>Pregunta a priorizar:</strong> ${esc(pregunta)}</p>
      <p>${esc(a.datos_intro || '')}</p>
      <ul>${datos}</ul>
      <p>${esc(a.insuficiencia || '')}</p>
      <p><strong>${esc(a.preguntas_rotulo || 'Preguntas que priorizamos para el análisis')}</strong></p>
      <ul class="preguntas-priorizadas">${preguntas}</ul>
      <p>${esc(a.necesidad_intro || '')} ${esc(a.necesidad || '')}</p>
      <p>${esc(a.sinteticos_frase || '')}</p>
    </section>`;
}

function escenaHTML(e, lookup, ruta) {
  const resumido = Boolean(e.sintesis);
  const entradas = (e.bloques || []).map((id) => lookup.get(id)).filter(Boolean);
  const figuras = entradas.map(({ b }) => figuraHTML(b.figura, resumido)).join('');
  const conclusiones = resumido ? '' : entradas.map(({ b }) => `<p><strong>Conclusión:</strong> ${esc(b.conclusion)}</p>`).join('');
  const detalles = entradas.map(({ cap, b }) => detalleHTML(cap, b, resumido)).join('');
  const det = e.detalle;
  const detBloques = det ? (det.bloques || []).map((id) => lookup.get(id)).filter(Boolean).map((en) => bloqueEjecutivoHTML(en, false, false)).join('') : '';
  return `
    <section class="escena" id="${esc(e.id)}" aria-label="${esc(e.titulo)}">
      <h2>${esc(e.titulo)}</h2>
      ${e.transicion ? `<p class="nota">${esc(e.transicion)}</p>` : ''}
      ${figuras}
      ${resumido ? `<p>${esc(e.sintesis)}</p>` : conclusiones}
      ${e.limite ? `<p class="nota">${esc(e.limite)}</p>` : ''}
      ${e.puente ? `<p class="puente">${esc(e.puente)}</p>` : ''}
      ${detalles}
      ${det ? `<details><summary>${esc(det.titulo)}</summary>${detBloques}</details>` : ''}
    </section>`;
}

function cierreEjecutivoHTML(cierre, etiquetaDetalle, ejCierre) {
  const resumen = ejCierre ? `
      <p><strong>Decisión:</strong> ${esc(ejCierre.decision)}</p>
      <p><strong>Responsable:</strong> ${esc(ejCierre.responsable)}</p>
      <p><strong>Medida de éxito:</strong> ${esc(ejCierre.exito)}</p>
      <p class="nota">${esc(ejCierre.supuestos)}</p>` : `
      <p>${esc(cierre.sintesis)}</p>
      <p><strong>Acciones:</strong> ${esc(cierre.acciones.conclusion)}</p>
      ${cierre.evaluacion ? `<p><strong>Evaluación:</strong> ${esc(cierre.evaluacion)}</p>` : ''}`;
  const detalleExtra = ejCierre ? `
      <p><strong>Explicación completa:</strong> ${esc(cierre.acciones.conclusion)}</p>
      ${cierre.evaluacion ? `<p><strong>Evaluación:</strong> ${esc(cierre.evaluacion)}</p>` : ''}` : '';
  return `
    <section aria-label="Cierre" id="cierre">
      <h2>${esc(cierre.titulo)}</h2>
      ${resumen}
      <details><summary>${esc(etiquetaDetalle)}</summary>
        ${tablaHTML(cierre.acciones.tabla.filas, cierre.acciones.tabla)}
        ${detalleExtra}
        ${cierre.acciones.evaluacion_comun ? `<p><strong>Evaluación común:</strong> ${esc(cierre.acciones.evaluacion_comun)}</p>` : ''}
      </details>
      <p class="nota">${esc(cierre.nota)}</p>
    </section>`;
}


function bloqueHTML(b) {
  const figura = b.figura ? `
    <figure>
      <figcaption><strong>${esc(b.figura.titulo)}</strong></figcaption>
      <div class="figura-marco">
        <iframe title="${esc(b.figura.titulo)} — figura interactiva"
          src="${base}${esc(b.figura.iframe_src)}" loading="lazy"></iframe>
      </div>
    </figure>` : '';
  const tabla = b.tabla ? (
    b.tabla.plegada
      ? `<details><summary>${esc(b.tabla.resumen || b.tabla.caption)}</summary>${tablaHTML(b.tabla.filas, b.tabla)}</details>`
      : tablaHTML(b.tabla.filas, b.tabla)
  ) : '';
  const lista = b.lista ? `<ul>${b.lista.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>` : '';
  return `
    <div class="bloque" data-bloque="${esc(b.id)}">
      ${figura}
      <p><strong>Conclusión:</strong> ${esc(b.conclusion)}</p>
      <p><strong>Motivo del siguiente análisis:</strong> ${esc(b.siguiente_analisis)}</p>
      ${lista}
      ${tabla}
    </div>`;
}

export async function renderCaso(el, id) {
  const c = await (await fetch(`${base}content/${id}.json`)).json();
  if ((id === 'cro' || id === 'cfo') && c.recorrido && c.recorrido.capitulos && c.ejecutiva) {
    const ruta = id;
    const otro = id === 'cro' ? { ruta: 'cfo', texto: 'Seguir con el caso CFO' } : { ruta: 'cro', texto: 'Volver al caso CRO' };
    const lookup = mapaBloques(c.recorrido);
    const escenaDe = new Map();
    for (const e of c.ejecutiva.escenas || []) {
      for (const b of e.bloques || []) escenaDe.set(b, e);
      for (const b of ((e.detalle || {}).bloques || [])) escenaDe.set(b, e);
    }
    const etiquetaDetalle = id === 'cro' ? 'Umbrales y evaluación completa' : 'Sensibilidad y diseño completo';
    el.innerHTML = `
    <div class="ejecutiva">
    <h1>${esc(c.titulo)}</h1>
    ${aperturaHTML(c.ejecutiva.apertura, c, ruta, id)}
${(c.ejecutiva.escenas || []).map((e) => escenaHTML(e, lookup, ruta)).join('')}
    ${cierreEjecutivoHTML(c.recorrido.cierre, etiquetaDetalle, c.ejecutiva.cierre)}
    <p><a href="#/${ruta}/respaldo">Ver respaldo técnico</a> · <a href="#/${otro.ruta}">${esc(otro.texto)}</a></p>
    ${respaldoHTML(c, ruta)}
    </div>`;
    return;
  }
  el.innerHTML = `
    <h1>${esc(c.titulo)}</h1>
    <section class="requerimiento" aria-label="Requerimiento original">
      <h2>Requerimiento original</h2>
      <blockquote>${esc(c.requerimiento_original.texto)}</blockquote>
      <p class="nota">Fuente: ${esc(c.requerimiento_original.fuente)}</p>
    </section>
    <p class="nota">${esc(c.nota_cierre)}</p>`;
}
