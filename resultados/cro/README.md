# Resultados CRO

Datos y métricas preparados; las once preguntas tienen gráficas y lecturas iniciales en el notebook. Revisión humana y diagnóstico pendientes.

- `tablas.html`: modelo, muestras y enlaces a CSV; [vista local](http://127.0.0.1:8790/resultados/cro/tablas.html).
- `metricas/{escenario}/`: doce familias de métricas completas y resumen mensual base.
- `resultados.json`: resultados/controles y muestras por escenario.
- `manifest.json`: reglas y hashes reproducibles.
- `validacion.json`: evidencia de comprobación actual.
- `migracion.json`: registro histórico del traslado de la versión 1.
- `graficas/analisis.html`: gráfica histórica rechazada, anterior a esta versión; no usarla para analizar los datos actuales.

Detalle de preguntas y cálculos: [cobertura CRO](../../docs/datos/cobertura-cro.md).

Primera gráfica acordada: `graficas/01_new_tendencia.html`, misma figura interactiva del notebook. `scripts/cro_charts.py` contiene el código reutilizable.

## Revisión de las once preguntas

Abrir `notebooks/02_modelo_cro.ipynb` en VS Code. Contiene 36 figuras: cuatro anteriores y 32 para 3.3–3.11. Selectores de etapa mantienen las transiciones separadas.

- `scripts/cro_analysis.py`: funciones reutilizables para 3.3–3.11; sin modificar fuentes.
- `.venv/bin/python -m scripts.validate_cro_analysis`: valida ratios y conciliaciones; evidencia en `validacion_graficas.json`.
- `.venv/bin/python -m unittest discover -s tests`: comprobaciones del modelo y gráficas.
- `.venv/bin/jupyter nbconvert --to notebook --execute notebooks/02_modelo_cro.ipynb --inplace --ExecutePreprocessor.timeout=180`: regenerar las salidas.

La representación se comprobó estructuralmente; la revisión visual en VS Code quedó pendiente de permisos de pantalla. Plazos de atención, criterios de calidad y estimaciones de impacto siguen sujetos a revisión de negocio.
