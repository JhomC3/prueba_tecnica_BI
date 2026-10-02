# Prueba técnica — Finora

Dos casos de Business Intelligence con datos sintéticos: localizar dónde se frena el funnel comercial (**CRO**) y separar suscripción, descuentos y cobro para explicar el ingreso recurrente (**CFO**).

**Empieza por los análisis:** [CRO](notebooks/02_modelo_cro.ipynb) · [CFO](notebooks/03_modelo_cfo.ipynb). Cada uno conecta pregunta, evidencia, conclusión y acción propuesta. Los escenarios son sintéticos.

| Quiero… | Dónde empezar |
| --- | --- |
| Ver los resultados y decisiones | Notebooks [CRO](notebooks/02_modelo_cro.ipynb) y [CFO](notebooks/03_modelo_cfo.ipynb). |
| Comprobar los datos y reproducir el trabajo | [Guía de ejecución](notebooks/README.md), modelos [CRO](docs/datos/modelo-cro-demo.md) / [CFO](docs/datos/modelo-cfo-demo.md). |
| Entender el criterio y el método | [Contexto](docs/contexto.md) y [cómo se abordó la prueba](docs/proceso/como-aborde-la-prueba.md). |
| Explorar la demo web | [Guion ejecutivo](public/docs/guion-video-ejecutivo.md) y [nota corta](public/docs/nota-corta.md). |

## Abrir la web local

Con Node.js y pnpm disponibles (ver `.node-version` y `packageManager` en `package.json`):

```bash
pnpm install --frozen-lockfile
pnpm test
pnpm run check:coherence
pnpm run build
pnpm run dev
```

La reproducción analítica y el entorno Python están en la [guía](notebooks/README.md). Esta copia pública no incluye CSV originales, oferta laboral, enunciado privado ni historial Git original.
