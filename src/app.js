import { renderResumen } from './views/summary.js';
import { renderCaso } from './views/case.js';
import { renderExplorar } from './views/explore.js';

const vista = document.getElementById('vista');
const enlaces = [...document.querySelectorAll('#nav a')];

const RUTAS = {
  resumen: { titulo: 'Resumen — Finora', render: renderResumen },
  cro: { titulo: 'Caso CRO — Finora', render: (el) => renderCaso(el, 'cro') },
  cfo: { titulo: 'Caso CFO — Finora', render: (el) => renderCaso(el, 'cfo') },
  explorar: { titulo: 'Explorar — Finora', render: renderExplorar }
};

function rutaVistaDeseada() {
  const h = window.location.hash.replace(/^#\/?/, '');
  const [ruta] = h.split('/');
  return RUTAS[ruta] ? ruta : 'resumen';
}

const ANCLAS_ANTIGUAS = {
  C01: 'e-new', C02: 'e-plazo', C03: 'e-calidad', C04: 'e-transiciones', C05: 'e-capacidad',
  S01: 'f-modelo', S02: 'f-modelo', S03: 'f-modelo', S04: 'f-politica', S05: 'f-politica',
  S06: 'f-recupero', S07: 'f-recupero', S09: 'respaldo',
  intro: 'intro', cierre: 'cierre', respuestas: 'respaldo',
  'adjuntos-cro': 'intro', 'adjuntos-cfo': 'intro', metodo: 'metodo', entrega: 'entrega',
};

function resolverAncla(ancla) {
  return (ancla && ANCLAS_ANTIGUAS[ancla]) || ancla;
}

let rutaVista = null;

function abrirRespaldo(dest) {
  let el = dest;
  while (el) {
    if (el.tagName === 'DETAILS' && !el.open) el.open = true;
    el = el.parentElement;
  }
}

async function mostrar() {
  const h = window.location.hash.replace(/^#\/?/, '');
  const [, ancla] = h.split('/');
  const rutaDeseada = rutaVistaDeseada();
  if (ancla && rutaVista === rutaDeseada) {
    const dest = document.getElementById(resolverAncla(ancla));
    if (dest) {
      abrirRespaldo(dest);
      dest.scrollIntoView();
      return;
    }
  }
  const ruta = rutaDeseada;
  enlaces.forEach((a) => {
    if (a.dataset.ruta === ruta) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
  vista.innerHTML = '<p>Cargando…</p>';
  try {
    await RUTAS[ruta].render(vista);
  } catch (e) {
    vista.innerHTML = '<p>No se pudo cargar esta vista. Comprueba tu conexión local e inténtalo de nuevo.</p>';
    console.error(e);
  }
  document.title = RUTAS[ruta].titulo;
  rutaVista = ruta;
  const pendiente = window.location.hash.replace(/^#\/?/, '').split('/')[1];
  if (pendiente) {
    const dest = document.getElementById(resolverAncla(pendiente));
    if (dest) {
      abrirRespaldo(dest);
      dest.scrollIntoView();
    }
  }
}

window.addEventListener('hashchange', mostrar);
mostrar();
