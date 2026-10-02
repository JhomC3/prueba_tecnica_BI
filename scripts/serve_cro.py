"""Vista local: solo sirve datos y resultados CRO, sin exponer el resto del repo."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = [ROOT / p for p in ("datos/sinteticos/cro", "datos/bases/cro", "resultados/cro")]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def translate_path(self, path):
        candidate = Path(super().translate_path(path)).resolve()
        if any(candidate == base or base in candidate.parents for base in ALLOWED):
            return str(candidate)
        return str(ROOT / ".ruta_cro_no_disponible")


if __name__ == "__main__":
    print("Tablas: http://127.0.0.1:8790/resultados/cro/tablas.html", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8790), Handler).serve_forever()
