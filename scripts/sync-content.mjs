// Sincroniza src/content/*.json -> public/content/*.json y actualiza el manifest.
// Sin fuente externa: solo copia y verifica. La usa `predev` y `prebuild`
// para que editar src/content nunca deje desactualizada la copia pública.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const raiz = new URL('..', import.meta.url).pathname;
const sha = (buf) => createHash('sha256').update(buf).digest('hex');

mkdirSync(join(raiz, 'public/content'), { recursive: true });
const contenidos = [];
for (const nombre of ['resumen.json', 'cro.json', 'cfo.json']) {
  const origen = join(raiz, `src/content/${nombre}`);
  const destino = join(raiz, `public/content/${nombre}`);
  const txt = readFileSync(origen, 'utf8');
  JSON.parse(txt);
  writeFileSync(destino, txt);
  contenidos.push({ archivo: `content/${nombre}`, sha256: sha(readFileSync(destino)) });
}

const rutaManifest = join(raiz, 'public/data/manifest.json');
if (existsSync(rutaManifest)) {
  const m = JSON.parse(readFileSync(rutaManifest, 'utf8'));
  m.contenidos = contenidos;
  writeFileSync(rutaManifest, JSON.stringify(m, null, 2) + '\n');
}
console.log('sync-content OK:', contenidos.map((c) => c.archivo).join(', '));
