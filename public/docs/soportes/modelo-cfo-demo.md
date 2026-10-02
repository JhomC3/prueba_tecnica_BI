# CFO — datos, indicadores y controles

Modelo sintético reproducible, cierre con escenario principal 2026-10-01. No usa ni modifica `inputs/`; no acredita resultados de Finora. Lectura principal: [notebook CFO](../../notebooks/03_modelo_cfo.ipynb).

## Diseño

110 clientes por alternativa: 100 existentes, cinco altas en julio y cinco reactivaciones en septiembre. Diez existentes tienen dos suscripciones. Cada escenario compara los mismos clientes con/sin política; no sumar grupos ni escenarios. Bajas de cinco clientes en octubre y diez en enero, iguales entre alternativas. Diez clientes reciben un aumento de tarifa en diciembre, también igual entre alternativas.

Enero 2025–marzo 2026: seis meses previos (enero–junio), descuento julio–septiembre y seis posteriores (octubre–marzo). 50 existentes elegibles (C000–C049, activos antes de la política, IDs fijos en ambas alternativas); se mantienen activos durante el seguimiento. Primera fotografía es saldo de apertura, no adquisición. Escenario principal más tres sensibilidades, sin azar. Configuración única en `scripts/cfo_model.py:CONFIG`; sin tendencia diferencial (no se descuenta 5% arbitrario):

| Escenario | Bruto antes → después | Descuento por mes | Resultado esperado, nueve meses, 50 clientes |
| --- | --- | --- | --- |
| Principal (hilo ejecutivo) | 100 → 110 UM | 40 UM durante tres meses | −1.500 UM (no recuperado; umbral 30 UM) |
| Positivo (respaldo) | 100 → 130 UM | 30 UM durante tres meses | +9.000 UM |
| Negativo (respaldo) | 100 → 100 UM | 20 UM durante tres meses | −3.000 UM |
| Compensado (respaldo) | 100 → 110 UM | 30 UM durante tres meses | 0 UM |

La comparación aísla ampliación/descuento con objetivo `ampliacion` (negativo: `descuento_sin_ampliacion`); no impone beneficio de retención ni adquisición y no denomina retención a cambiar solo precio o cantidades. La referencia sin descuento conserva bruto 100 por decisión del generador; es una alternativa programada, no el contrafactual conocido ni quitar el descuento conservando servicios. Seis meses posteriores permiten comprobar recuperación a seis meses del vencimiento, sin representar toda la vida del cliente.

## Tablas y relaciones

`clientes` → `suscripciones` → `componentes` → `precios` y `descuentos`. `estados`: suscripción × mes. `componentes_mes`: componente × mes activo, cantidad/tarifa/bruto/descuento/neto. `movimientos`: cliente × mes tras agregar todas sus suscripciones. `pagos`: suscripción × mes, con pendiente y cargo no recurrente separados. `grupo` integra todas las claves para evitar mezclar alternativas.

Tarifas y descuentos tienen vigencia con fin exclusivo. Descuentos fijos; porcentaje equivalente calculado sobre bruto, no un descuento adicional. Cantidad y tarifa representan contratos simulados. Fotografías al inicio del mes, sin prorrateo intramensual ni impuestos. Importes enteros en centavos de UM ilustrativas; no COP históricos.

## Indicadores

- MRR neto = bruto − descuentos; crecimiento mensual = (neto / neto previo − 1) × 100; ARR = neto × 12; ARPU = neto / clientes activos.
- Puente: apertura + nuevo negocio + reactivación + churn bruto + expansión/contracción subyacente + pricing − Δdescuento = neto final. Cantidad a precio anterior y después precio a cantidad actual. Nuevos componentes a precio actual; retirados a anterior.
- Retención: clientes de enero activos sin interrupción / clientes iniciales. NRR: su neto actual / neto inicial. GRR: limitar neto de cada retenido a su neto inicial. Altas/reactivaciones posteriores fuera del denominador inicial.
- Churn: bajas totales / activos al inicio del mes. LTV de ingreso = ARPU / churn mensual, estimación estacionaria; no estimable con churn cero. No es utilidad ni vida observada.
- Permanencia: meses activos observados y censura al corte; no vida media de supervivientes. Ingreso acumulado: neto julio–marzo por cohorte común; resultado incremental = neto con política menos referencia enlazada por cliente/mes. Primer mes de recuperación = primer corte con acumulado no negativo (equilibrio vs positivo; advertir si recae; si no: «no recuperado al corte»). Identidad de comprobación para ampliación constante: H × aumento − meses_desc × dto. Costos, margen y CAC no calculables con esta demo.

## Reproducir

```bash
.venv/bin/python scripts/cfo_model.py
.venv/bin/python scripts/cfo_present.py
.venv/bin/python scripts/cfo_notebook_build.py
.venv/bin/jupyter nbconvert --to notebook --execute notebooks/03_modelo_cfo.ipynb --inplace
.venv/bin/python scripts/validate_cfo.py
```

CSV: `datos/sinteticos/cfo/{escenario}/{grupo}/`; SQLite: `datos/bases/cfo/{escenario}/modelo.sqlite`; métricas (`mensual`, `cohortes`, `foco_cohorte`, `foco_comparacion`, `foco_resumen`, `comparacion`, `focos`, `recorrido`), ejemplos, manifiesto, gráficas y conclusiones: `resultados/cfo/`. SQL: `sql/cfo/puente.sql`. Código de generación, cálculo y presentación separado del notebook. `ESCENARIO=principal` en el hilo principal; las gráficas HTML permiten revisar sensibilidades como respaldo.

Controles: claves/relaciones, vigencias, descuentos válidos, cantidades/precios, pagos conciliados y residuo cero del puente; alteración de un importe persistido en copia temporal hace fallar el control. Fixtures independientes cubren ejemplos CFO, cambio de cantidad/precio simultáneo, altas/bajas/reactivación, múltiples suscripciones, cohorte de política, vigencias, acumulado, recuperación, umbral, ARPU/LTV separados y presentación. Evidencia de ejecución: `resultados/cfo/validacion.json`.

## Recorrido por hallazgos

El notebook presenta una evaluación breve del modelo actual y su evolución, dos muestras visibles (valor recurrente y cobro) y dos gráficas principales: evolución del MRR y compensación acumulada. Preguntas originales, método, otras siete tablas, validación y nota sobre supuestos/IA quedan desplegables en la misma presentación. Cierra con acción cuantificada, tabla de monto/duración y evaluación mediante dos grupos similares durante nueve meses (tres de descuento y seis posteriores). Visión ampliada desplegable en cuatro preguntas breves. El respaldo técnico permanece en archivos y en `notebooks/archivo/03_modelo_cfo_antes_simplificar_respaldo_2026-10-02.ipynb`. Generador: `scripts/cfo_notebook_build.py`.


## Corrección de presentación y conciliación — 2026-10-01

El CFO reutiliza la explicación individual de tablas, muestras y controles del CRO. Las respuestas literales se conservan desplegables al inicio; 3.1–3.2 cubren MRR, ingreso acumulado y explicación del resultado. `scripts/cfo_notebook_views.py` deriva las lecturas y `scripts/cfo_audit.py` reconstruye movimientos, compara CSV/SQLite y recalcula métricas. Las métricas complementarias y sensibilidades siguen disponibles fuera de la presentación.

La versión previa al cambio de estructura está en `notebooks/archivo/03_modelo_cfo_antes_espejo_cro.zip`. El notebook de presentación vigente tiene 23 celdas, ocho de código ejecutadas secuencialmente con IPython tras simplificar la lectura ejecutiva. Se conservan escenario, fuentes sintéticas y resultados económicos; CRO no se modifica.

**Ubicación de respaldos desde 2026-10-02:** las rutas históricas `notebooks/archivo/…` citadas en este documento son miembros de [organizacion-2026-10-02.zip](../proceso/archivo/organizacion-2026-10-02.zip). Consultar el [índice de recuperación](../proceso/archivo/README.md); ya no son archivos del recorrido activo.
