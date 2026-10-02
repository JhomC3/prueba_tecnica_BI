# AGENTS.md — Prueba técnica

- Contexto y método: `docs/contexto.md`, `docs/metodo/marco-de-trabajo.md`; estado: `README.md`.
- Español para documentación y comunicación.
- No reinterpretar ceros, unidades o descuentos sin una definición registrada en `docs/contexto.md`.
- Datos sintéticos versionados en `public/data/archivos/`; generadores en `scripts/`; modelos en `docs/datos/modelo-cro-demo.md` y `docs/datos/modelo-cfo-demo.md`.
- Web con pnpm: `pnpm install --frozen-lockfile`, `pnpm test`, `pnpm run check:coherence`, `pnpm run build`.
- Conservar las preguntas analíticas con su redacción; marcar resultados parciales sin presentar un total agregado como respuesta completa.
- Gráficas: título, unidades y periodo necesario; contexto y supuestos fuera de la figura.
- Cada gráfica del recorrido principal va seguida de su conclusión y la implicación para el siguiente análisis.
- Coherencia CRO: mismas cohortes por primera entrada a New y mismo reloj desde New; distinguir nivel alcanzado de visita real.
