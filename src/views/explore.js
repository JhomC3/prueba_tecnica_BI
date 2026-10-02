export async function renderExplorar(el) {
  el.innerHTML = `
    <h1>Explorar</h1>
    <p><span class="pastilla pendiente">Pendiente de integración</span></p>
    <p>La exploración asistida (pregunta abierta, carga de CSV, operaciones verificables,
    sesión temporal y descarga) aún no está integrada. Esta página no analiza datos
    ni utiliza IA: cuando llegue, pedirá definiciones y archivos antes de calcular.</p>
    <h2>Qué incluirá</h2>
    <ul>
      <li>Pregunta de Marketing, Growth o Finanzas con decisor y decisión.</li>
      <li>Carga local de CSV con perfil y significado de columnas revisable.</li>
      <li>Operaciones soportadas (conteos, agregaciones, tendencias, comparaciones) con evidencia.</li>
      <li>Sesión temporal y síntesis descargable; sin recuperación al volver otro día.</li>
    </ul>
    <p class="nota">Alcance: RF-12 a RF-20 de la spec activa. Sin controles de demostración:
    no hay campos ni botones que aparenten funcionar.</p>`;
}
