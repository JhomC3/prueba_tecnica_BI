# CFO — datos, indicadores y controles

Modelo sintético reproducible, 2026-10-01. No usa ni modifica `inputs/`; no acredita resultados de Finora. Lectura principal: [notebook CFO](../../notebooks/03_modelo_cfo.ipynb).

## Diseño

110 clientes por alternativa: 100 existentes, cinco altas en julio y cinco reactivaciones en septiembre. Diez existentes tienen dos suscripciones. Cada escenario compara los mismos clientes con/sin política; no sumar grupos ni escenarios. Bajas de cinco clientes en octubre y diez en enero, iguales entre alternativas. Diez clientes reciben un aumento de tarifa en diciembre, también igual entre alternativas.

Enero 2025–marzo 2026: seis meses previos, descuento julio–septiembre y seis meses posteriores. 50 existentes elegibles; se mantienen activos durante el seguimiento. Primera fotografía es saldo de apertura, no adquisición. Tres escenarios parametrizados, sin azar:

| Escenario | Bruto antes → después | Descuento por mes | Resultado esperado, nueve meses, 50 clientes |
| --- | --- | --- | --- |
| Positivo | 100 → 130 UM | 30 UM durante tres meses | +9.000 UM |
| Negativo | 100 → 100 UM | 20 UM durante tres meses | −3.000 UM |
| Compensado | 100 → 110 UM | 30 UM durante tres meses | 0 UM |

La comparación aísla ampliación/descuento. No impone beneficio de retención ni adquisición. La referencia sin descuento es una alternativa programada, no el contrafactual conocido del negocio real. Seis meses posteriores permiten observar recuperación, sin representar toda la vida del cliente.

## Tablas y relaciones

`clientes` → `suscripciones` → `componentes` → `precios` y `descuentos`. `estados`: suscripción × mes. `componentes_mes`: componente × mes activo, cantidad/tarifa/bruto/descuento/neto. `movimientos`: cliente × mes tras agregar todas sus suscripciones. `pagos`: suscripción × mes, con pendiente y cargo no recurrente separados. `grupo` integra todas las claves para evitar mezclar alternativas.

Tarifas y descuentos tienen vigencia con fin exclusivo. Descuentos fijos; porcentaje equivalente calculado sobre bruto, no un descuento adicional. Cantidad y tarifa representan contratos simulados. Fotografías al inicio del mes, sin prorrateo intramensual ni impuestos. Importes enteros en centavos de UM ilustrativas; no COP históricos.

## Indicadores

- MRR neto = bruto − descuentos; crecimiento mensual = (neto / neto previo − 1) × 100; ARR = neto × 12; ARPU = neto / clientes activos.
- Puente: apertura + nuevo negocio + reactivación + churn bruto + expansión/contracción subyacente + pricing − Δdescuento = neto final. Cantidad a precio anterior y después precio a cantidad actual. Nuevos componentes a precio actual; retirados a anterior.
- Retención: clientes de enero activos sin interrupción / clientes iniciales. NRR: su neto actual / neto inicial. GRR: limitar neto de cada retenido a su neto inicial. Altas/reactivaciones posteriores fuera del denominador inicial.
- Churn: bajas totales / activos al inicio del mes. LTV de ingreso = ARPU / churn mensual, estimación estacionaria; no estimable con churn cero. No es utilidad ni vida observada.
- Permanencia: meses activos observados y censura al corte; no vida completa de clientes existentes. Ingreso acumulado: neto julio–marzo; resultado: acumulado con política menos referencia. Costos, margen y CAC no calculables con esta demo.

## Reproducir

```bash
.venv/bin/python scripts/cfo_model.py
.venv/bin/python scripts/cfo_present.py
.venv/bin/python scripts/validate_cfo.py
.venv/bin/jupyter nbconvert --to notebook --execute notebooks/03_modelo_cfo.ipynb --inplace
```

CSV: `datos/sinteticos/cfo/{escenario}/{grupo}/`; SQLite: `datos/bases/cfo/{escenario}/modelo.sqlite`; métricas, ejemplos, manifiesto, gráficas y conclusiones: `resultados/cfo/`. SQL: `sql/cfo/puente.sql`. Código de generación, cálculo y presentación separado del notebook. Parámetro `ESCENARIO` selecciona la lectura; las gráficas HTML permiten revisar las tres alternativas.

Controles: claves/relaciones, vigencias, descuentos válidos, cantidades/precios, pagos conciliados y residuo cero del puente. Fixtures independientes cubren ejemplos CFO, cambio de cantidad/precio simultáneo, altas/bajas/reactivación, múltiples suscripciones, denominadores, LTV no estimable, resultado acumulado y presentación. Evidencia de ejecución: `resultados/cfo/validacion.json`.

## Recorrido por hallazgos

El notebook empieza por pregunta/decisión y resultado acumulado; localiza diferencias por elegibilidad y fase, explica ingreso bruto/descuentos y movimientos, propone acción según signo y define evaluación. `scripts/cfo_present.py --recorrido` deriva `focos.csv` y `recorrido.json` sin modificar fuente, métricas ni gráficas previas. En equilibrio se comprueban compensaciones temporales; sin diferencia no se fuerza un foco. Complementos de retención y valor quedan disponibles en respaldo plegado. No actualiza el marco general ni acredita impacto real.
