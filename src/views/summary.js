const base = (import.meta.env?.BASE_URL) || './';

function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export async function renderResumen(el) {
  const r = await (await fetch(`${base}content/resumen.json`)).json();
  const m = r.metodo || {};
  const e = r.entrega || {};
  el.innerHTML = `
    <h1>${esc(r.titulo)}</h1>
    <p>${esc(r.descripcion)}</p>
    <p><strong>Método:</strong> ${esc(r.metodo_breve)}</p>
    ${(r.casos || []).map((c) => `
      <section aria-label="${esc(c.titulo)}">
        <h2>${esc(c.titulo)}</h2>
        <p><span class="nota">Decide: ${esc(c.decisor)}</span></p>
        <p><strong>Preocupación original:</strong> ${esc(c.preocupacion)}</p>
        <p><strong>Pregunta priorizada:</strong> ${esc(c.pregunta_priorizada)}</p>
        <p><strong>Resultado esencial:</strong> ${esc(c.resultado)}</p>
        <p><strong>Acción propuesta:</strong> ${esc(c.accion)}</p>
        <p><a href="#/${esc(c.caso_id)}">Abrir caso</a></p>
      </section>`).join('')}
    <p class="nota">${esc(r.nota_comun)}</p>
    <nav aria-label="Accesos de inicio"><ul>
      <li><a href="#/resumen/metodo">Método y uso de IA</a></li>
      <li><a href="#/resumen/entrega">Entrega y respaldo</a></li>
      <li><a href="#/explorar">Explorar</a></li>
    </ul></nav>
    <section id="metodo" aria-label="${esc(m.titulo || 'Método y uso de IA')}">
      <h2>${esc(m.titulo || 'Método y uso de IA')}</h2>
      <p>${esc(m.principio || '')}</p>
      <p><strong>Trabajo del candidato:</strong> ${esc(m.candidato || '')}</p>
      <p><strong>Trabajo asistido por IA:</strong> ${esc(m.ia || '')}</p>
      ${(m.episodios || []).map((p) => `<h3>${esc(p.titulo)}</h3><p>${esc(p.detalle)}</p>`).join('')}
      <p class="nota">${esc(m.controles || '')}</p>
    </section>
    <section id="entrega" aria-label="${esc(e.titulo || 'Entrega y respaldo')}">
      <h2>${esc(e.titulo || 'Entrega y respaldo')}</h2>
      <p><a href="${base}${esc(e.nota_corta || '')}" download>Descargar nota corta</a></p>
      <h3>Soportes publicados</h3>
      <ul>${(e.soportes || []).map((s) => `<li><a href="${base}${esc(s.archivo)}" download>${esc(s.archivo.split('/').pop())}</a> — ${esc(s.descripcion)}</li>`).join('')}</ul>
      <p class="nota">${esc(e.videos || '')}</p>
      <h3>Estado real</h3>
      <ul>${(e.estados || []).map((e2) => `<li><strong>${esc(e2.estado)}:</strong> ${esc(e2.situacion)}</li>`).join('')}</ul>
    </section>`;
}
