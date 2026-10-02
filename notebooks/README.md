# Explorar los datos

**Recorrido CRO enfocado:** `02_modelo_cro.ipynb` continúa desde 3.5 únicamente en las transiciones priorizadas por 3.4, sobre entrada New y el periodo seleccionado. Cada gráfica tiene conclusión inmediata; termina en acciones propuestas.

Recrear los CSV del diagnóstico: `.venv/bin/python -m scripts.cro_focused_diagnosis`. Requiere los datos y métricas base existentes.

**Modelo CRO:** abrir `02_modelo_cro.ipynb`. CSV en `datos/sinteticos/cro/`, SQLite en `datos/bases/cro/` y métricas en `resultados/cro/metricas/`. Contiene modelo, tablas, controles y resultados mensuales. Ejecutado desde kernel nuevo; revisión humana pendiente. `resultados/cro/tablas.html` permite ver las tablas sin Jupyter. Detalle: `docs/datos/modelo-cro-demo.md`.

```bash
.venv/bin/jupyter notebook notebooks/02_modelo_cro.ipynb
```

Entorno aislado en `.venv/`; versiones instaladas en `requirements.lock.txt`. Para recrearlo:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r notebooks/requirements.lock.txt
.venv/bin/python -m ipykernel install --prefix .venv --name python3 --display-name "Python 3"
```

Los notebooks usan el kernel `python3`. La copia pública no incluye los CSV originales; la reproducción pública usa datos sintéticos (`public/data/archivos/`).

**Modelo CFO:** abrir [03_modelo_cfo.ipynb](03_modelo_cfo.ipynb). Tres escenarios, tablas, indicadores, nueve gráficas por escenario y conclusiones desde resultados. Seleccionar `ESCENARIO` y ejecutar todas las celdas. Modelo sintético separado del histórico; [definiciones y reproducción](../docs/datos/modelo-cfo-demo.md).
