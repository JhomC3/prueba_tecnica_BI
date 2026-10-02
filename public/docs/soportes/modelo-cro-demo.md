# CRO — datos y métricas preparados

2026-09-30. **Modelo sintético ampliado para comenzar el análisis de las once preguntas.** Las definiciones son supuestos visibles de demostración; no hallazgos de Finora. No se crearon ni actualizaron gráficas en esta ampliación.

**Cierre con capacidad — 2026-10-01:** escenario deliberado con más volumen en Demo/Proposal, personal constante, demora derivada de sobrecarga y menor conversión dentro del plazo. Desde 3.5 el notebook muestra solo carga por persona y demora hasta primer intento (dos gráficas), síntesis y acción con evaluación. Detalle en `specs/001-solucion-analitica-finora/encargo-cierre-cro.md`. Fuentes originales intactas; versión anterior en `notebooks/archivo/02_modelo_cro_antes_cierre_capacidad.ipynb`.

## Dónde verlo

- `notebooks/02_modelo_cro.ipynb`: tablas, controles y muestras de métricas ejecutados.
- `resultados/cro/tablas.html`: modelo con columnas en filas, muestras y enlaces CSV.
- CSV: `datos/sinteticos/cro/{escenario}/`.
- SQLite: `datos/bases/cro/{escenario}/modelo.sqlite`.
- Métricas: `resultados/cro/metricas/{escenario}/`.

## Cuatro tablas de negocio y capacidad auxiliar

| Tabla/CSV | Contenido |
| --- | --- |
| `dim_cuentas` — prospectos | Captación, tipo de entrada, canal/campaña, industria, perfil, producto, región, asignación y evaluación de calidad. Historia previa de pagos declarada. |
| `fact_etapas` | Una fila por visita; etapa, cuenta, fechas, destino, resultado, motivo de pérdida y asignación. |
| `interacciones` | Intentos y contactos efectivos, vinculados a la cuenta y visita. |
| `pagos` | Eventos válidos y fallidos, incluidos pagos previos y repetidos. |
| `dim_capacidad` — auxiliar | Personas disponibles por mes calendario y etapa foco (Demo 10 personas x 11 cuentas, Proposal 8 x 10, constantes enero–septiembre). Clave mes + etapa. |

`dim_etapas` es el catálogo auxiliar de siete etapas. `ganados.csv` es una vista derivada de Won, no una quinta fuente de negocio. SQLite incluye además vistas de primera entrada/último resultado por cuenta y etapa y de primer pago válido.

| Escenario | Cuentas | Visitas | Interacciones | Pagos | Won |
| --- | ---: | ---: | ---: | ---: | ---: |
| Referencia | 1.800 | 6.740 | 8.635 | 2.436 | 595 |
| Menor conversión | 1.800 | 6.004 | 7.677 | 2.211 | 502 |
| Mayor demora | 1.800 | 6.503 | 8.614 | 2.255 | 530 |

Escenarios alternativos de las mismas cuentas: no sumarlos entre sí. La versión 2 amplía y regenera la primera demo; sus cantidades sustituyen las anteriores. El cierre con capacidad regenera fechas de Demo/Proposal e interacciones por sobrecarga (pagos −4/−10 por corte); New y canales se conservan. Originales en `inputs/` intactos.

## Reglas de la simulación

- Semilla 42; 180 captaciones/mes enero–abril y 270 mayo–agosto; corte 2026-09-30. Cuenta = una oportunidad.
- Núcleo comercial: probabilidades de avance 94/82/85/80/78/85%, tiempos 2–8 días. Caída: −35 puntos de probabilidad en Working desde mayo (escenario conversión). Demora: +28 días en Working (escenario demora), sin cambiar la probabilidad programada. No son benchmarks.
- **Cierre con capacidad (referencia):** Demo 10 personas x 11 cuentas por persona y mes (110 total), Proposal 8 x 10 (80 total), constantes enero–septiembre. Si llegadas del mes superan la capacidad total, demora = techo((llegadas − capacidad total)/personal) hasta 4 días al primer intento y a la salida. La demora desplaza intentos y avances; la conversión se calcula desde esas fechas, sin caída porcentual programada aparte.
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

- Generar: `.venv/bin/python scripts/cro_demo.py` (con capacidad y demora por sobrecarga).
- Focos y coherencia: `.venv/bin/python -m scripts.cro_focused_diagnosis`.
- Comprobar: `.venv/bin/python -m unittest discover -s tests -p 'test_cro*.py'` (32 pruebas CRO en verde).
- Notebook: `.venv/bin/python -m jupyter nbconvert --to notebook --execute notebooks/02_modelo_cro.ipynb --output 02_modelo_cro.ipynb` (kernel Python; salidas guardadas, 0 errores, 2 figuras desde 3.5).

Consultas reutilizables en `sql/cro/completas.sql` y `sql/cro/coherencia.sql`; métricas base en `sql/cro/metricas.sql`. Pruebas con fixtures independientes para calidad/cobertura, contactos, plazos, saltos/reingresos, conversión, madurez, primer pago, conciliación, capacidad constante/carga creciente/demora mayor y focos Demo/Proposal. Manifiesto con hashes de 81 CSV: 24 de datos (7 por escenario con capacidad + puntuaciones) y 57 de métricas (39 completas + 12 focos/coherencia + 6 puntuaciones). Tres SQLite. Controles en `control_coherencia.json` y `control_cohortes_new.csv`.

Gráficas anteriores conservadas como resultado histórico rechazado por el candidato; no corresponden a esta versión y no deben usarse para analizarla. El recorrido vigente ya contiene las figuras seleccionadas; su aceptación humana se registra separadamente.

**Límite real:** con estos datos podemos demostrar el análisis. Para concluir qué pasó en Finora siguen faltando CRM, definiciones confirmadas y conciliación contra origen.

## Diagnóstico acotado desde 3.5 — 2026-10-01

`atencion_focos_new.csv` y `etapas_focos_new.csv`, en cada carpeta de métricas, contienen exclusivamente cuentas con entrada New, transiciones seleccionadas por 3.4 y periodo de referencia/seguimiento. SQL de solo lectura sobre la base del escenario; conserva mediana/P90 originales, sin promediar medianas por canal. Comando: `.venv/bin/python -m scripts.cro_focused_diagnosis`. Ventanas 30/60/90 se comparan solo en meses completos comunes. El notebook principal muestra la historia acotada; las vistas generales anteriores están en `notebooks/archivo/02_modelo_cro_respaldo.ipynb`.

### Cierre con capacidad desde 3.5 — 2026-10-01

Referencia, abril frente a mayo, mismos New y ventana histórica 30 días (enero–abril 30 días, 178 cuentas; general 32 incluye demora May+). Carga usa mes calendario (cálculo y gráfica en llegadas finales): New 133→179; Demo 7,9→12,3 (79→123, 10 personas, supera 11 desde mayo) y Proposal 9,1→9,6 (73→77, 8 personas, aún bajo 80; supera en junio 106>80, 13,3 por persona, donde se atiende mayo 49/63; abril 16/32 en abril/mayo sin sobrecarga), personal constante; demora Demo 3,0→4,0 días (41/58→68/96; abril 26/32, mayo 51/45 en meses sobrecargados) y Proposal 2,0→4,0 (29/48→29/63; abril 16/32 sin sobrecarga, mayo 14/49 con junio sobrecargado); conversión Demo→Proposal 76,2%→61,8%, Proposal→Won 58,3%→19,0% y New→Won 21,1%→6,7% (28/133 y 12/179). Mediana New→Won 32 días (30 días como ventana común). Focos Demo y Proposal sin caída mayor oculta. Desde 3.5 solo dos gráficas (carga y demora), síntesis y acción (reforzar capacidad Demo/Proposal, Sales, prueba octubre–noviembre 2026). Duración/P90, canales y plazos 30/60/90 fuera del hilo principal, conservados en `notebooks/archivo/02_modelo_cro_antes_cierre_capacidad.ipynb`.


### Corrección de coherencia — 2026-10-01

El candidato identificó que las etapas cambiaban población y reloj respecto a New → Won. Se sustituyó esa base por cohortes de primera New y un plazo común desde New; se recalcularon 3.4–3.7. Las cifras/conclusiones anteriores de esos bloques quedan invalidadas, conservadas como historial. [Resultados, controles y reproducción](coherencia-cro.md). No se han probado causas ni ejecutado acciones.

**Ubicación de respaldos desde 2026-10-02:** las rutas históricas `notebooks/archivo/…` citadas en este documento son miembros de [organizacion-2026-10-02.zip](../proceso/archivo/organizacion-2026-10-02.zip). Consultar el [índice de recuperación](../proceso/archivo/README.md); ya no son archivos del recorrido activo.
