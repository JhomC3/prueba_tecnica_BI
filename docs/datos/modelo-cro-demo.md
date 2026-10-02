# CRO — datos y métricas preparados

2026-09-30. **Modelo sintético ampliado para comenzar el análisis de las once preguntas.** Las definiciones son supuestos visibles de demostración; no hallazgos de Finora. No se crearon ni actualizaron gráficas en esta ampliación.

## Dónde verlo

- `notebooks/02_modelo_cro.ipynb`: tablas, controles y muestras de métricas ejecutados.
- `resultados/cro/tablas.html`: modelo con columnas en filas, muestras y enlaces CSV.
- CSV: `datos/sinteticos/cro/{escenario}/`.
- SQLite: `datos/bases/cro/{escenario}/modelo.sqlite`.
- Métricas: `resultados/cro/metricas/{escenario}/`.

## Cuatro tablas de negocio

| Tabla/CSV | Contenido |
| --- | --- |
| `dim_cuentas` — prospectos | Captación, tipo de entrada, canal/campaña, industria, perfil, producto, región, asignación y evaluación de calidad. Historia previa de pagos declarada. |
| `fact_etapas` | Una fila por visita; etapa, cuenta, fechas, destino, resultado, motivo de pérdida y asignación. |
| `interacciones` | Intentos y contactos efectivos, vinculados a la cuenta y visita. |
| `pagos` | Eventos válidos y fallidos, incluidos pagos previos y repetidos. |

`dim_etapas` es el catálogo auxiliar de siete etapas. `ganados.csv` es una vista derivada de Won, no una quinta fuente de negocio. SQLite incluye además vistas de primera entrada/último resultado por cuenta y etapa y de primer pago válido.

| Escenario | Cuentas | Visitas | Interacciones | Pagos | Won |
| --- | ---: | ---: | ---: | ---: | ---: |
| Referencia | 1.800 | 6.740 | 8.635 | 2.440 | 595 |
| Menor conversión | 1.800 | 6.004 | 7.677 | 2.211 | 502 |
| Mayor demora | 1.800 | 6.503 | 8.614 | 2.265 | 530 |

Escenarios alternativos de las mismas cuentas: no sumarlos entre sí. La versión 2 amplía y regenera la primera demo; sus cantidades sustituyen las anteriores. Originales en `inputs/` intactos.

## Reglas de la simulación

- Semilla 42; 180 captaciones/mes enero–abril y 270 mayo–agosto; corte 2026-09-30. Cuenta = una oportunidad.
- Núcleo comercial: probabilidades de avance 94/82/85/80/78/85%, tiempos 2–8 días. Caída: −35 puntos de probabilidad en Working desde mayo. Demora: +28 días, sin cambiar la probabilidad programada. No son benchmarks.
- Una parte de cuentas compra desde producto sin etapas comerciales. Se conservan entradas directas a SQL; se incluyen saltos SQL → Proposal y visitas adicionales a Working.
- Calidad v1: micro/pequeña empresa, necesidad cubierta e intención de evaluar compra en 90 días. Los tres criterios deben cumplirse. Se incluyen no evaluados; la calidad no se deriva de Won.
- Atención: plazo ilustrativo de 2 días desde entrada a una visita; efectivo significa intercambio registrado, no envío. Se incluyen visitas sin intento. El plazo no es un SLA confirmado.
- Historia de pagos completa desde 2025-01-01 para estas cuentas sintéticas: algunos ya pagaban antes de captación. Primer válido tras captación cuenta como nuevo pagador solo sin pago previo. Fallos y pagos repetidos no cuentan como adquisición.
- Tasas por etapa: cuenta única y primera entrada; reingresos no duplican denominadores. Saltos separados de avances a la siguiente. Permanencia calendario desde primera entrada hasta última salida; en esta demo los reingresos son inmediatos. Atención se mide por visita.
- Cohortes a 30/60/90 días: solo entradas con seguimiento suficiente. Abiertos al corte y sin avance dentro de una ventana son conceptos diferentes. Mediana/P90 de ganados o salidas no describe los casos todavía abiertos.

Reglas ejecutables en `scripts/cro_complete.py` y `resultados/cro/manifest.json`. Configuración v1 de calidad y plazo ilustrativo pueden revisarse con el candidato antes de interpretar.

## Resultados reutilizables

Doce familias: resultado global, demanda, calidad, descalificación, atención, etapas, pérdidas, cohortes New → Won, origen temporal de cierres, nuevos pagadores, captación → pago y prioridad. Cada CSV incluye total y segmentación separada por tipo de entrada, canal, industria, perfil, producto, región y campaña; **no sumar dimensiones entre sí**.

Las cohortes y etapas incluyen ventanas y denominadores. `prioridad.csv` muestra brecha de conversión frente al periodo base y avances ilustrativos asociados a esa brecha; no ingresos garantizados ni efecto causal. No sumar brechas de etapas como si fueran clientes distintos.

## Reproducción y evidencia

- Generar: `.venv/bin/python scripts/cro_demo.py`.
- Comprobar: `.venv/bin/python -m unittest discover -s tests`.
- Notebook: `.venv/bin/jupyter nbconvert --to notebook --execute notebooks/02_modelo_cro.ipynb --inplace`.

Consultas reutilizables en `sql/cro/completas.sql`; métricas base en `sql/cro/metricas.sql`. Trece pruebas, con fixtures independientes para calidad/cobertura, contactos, plazos, saltos/reingresos, conversión, madurez, primer pago y conciliación por segmentos. Manifiesto con hashes de 57 CSV: 18 de datos/vistas y 39 de métricas. Tres SQLite. Evidencia en `resultados/cro/validacion.json`.

Gráficas anteriores conservadas como resultado histórico rechazado por el candidato; no corresponden a esta versión y no deben usarse para analizarla. Las siguientes se definirán una por una con él.

**Límite real:** con estos datos podemos demostrar el análisis. Para concluir qué pasó en Finora siguen faltando CRM, definiciones confirmadas y conciliación contra origen.

## Diagnóstico acotado desde 3.5 — 2026-10-01

`atencion_focos_new.csv` y `etapas_focos_new.csv`, en cada carpeta de métricas, contienen exclusivamente cuentas con entrada New, transiciones seleccionadas por 3.4 y periodo de referencia/seguimiento. SQL de solo lectura sobre la base del escenario; conserva mediana/P90 originales, sin promediar medianas por canal. Comando: `.venv/bin/python -m scripts.cro_focused_diagnosis`. Ventanas 30/60/90 se comparan solo en meses completos comunes. El notebook principal muestra la historia acotada; las vistas generales anteriores están en `notebooks/archivo/02_modelo_cro_respaldo.ipynb`.
