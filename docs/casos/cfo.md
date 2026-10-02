# Caso CFO — formulación

**Modelo sintético implementado · 2026-10-01.** [Notebook: datos, indicadores, gráficas y respuestas](../../notebooks/03_modelo_cfo.ipynb). Escenarios ilustrativos; sin efectos reales de descuentos comprobados.

## Requerimiento original

Fuente: [reto técnico](../fuentes/reto-tecnico.md), caso 2.

El CFO pregunta:

> "Si un cliente pagaba 100 y ahora paga 80, ¿contrajo 20 o recibió un descuento? ¿Qué pasa si su suscripción creció de 100 a 130, pero tiene un descuento de 30 y sigue pagando 100? ¿Y cuando desaparezca el descuento, eso cuenta como expansión? Quiero saber qué está pasando con el negocio subyacente y cuánto revenue estamos dejando de capturar por decisiones comerciales."

Finora cobra suscripciones mensuales cuyo valor puede cambiar con el uso y características de cada cliente. Hoy existe un histórico con cliente + mes + monto pagado, y los cambios entre meses se usan para clasificar movimientos como crecimiento, contracción, churn o reactivación. Ahora Finora quiere introducir descuentos temporales.

Tu reto: evalúa si el modelo actual permite responder bien estas preguntas. Si no, muéstranos cómo debería evolucionar. Puedes modificar la estructura de datos, crear nuevas definiciones o proponer otro modelo.

Preguntas a responder:

1. ¿Qué puede y qué no puede responder el modelo actual (cliente + mes + monto pagado)?
2. ¿Cómo separarías el valor de la suscripción del precio efectivamente pagado? ¿Qué campos, tablas o definiciones agregarías?
3. ¿Cómo clasificarías el inicio y el fin de un descuento para que no se confundan con contracción o expansión reales?

Al final queremos poder responder consistentemente: ¿Por qué cambió nuestro MRR? y ¿cuánto del cambio corresponde al comportamiento del cliente y cuánto a pricing o descuentos?

## 1. Quién decide

El CFO. Finanzas y quienes autorizan precios/descuentos participarían; no asumir que la decisión pertenece a Marketing.

## 2. Decisión y éxito — propuesta

**Evaluar si la política de descuentos mejora o deteriora el ingreso recurrente neto y el valor económico de los clientes, explicando cuánto del cambio corresponde al negocio subyacente, a precios o a descuentos.** Para el histórico: explicar cambios observados cuando los datos lo permitan. Para descuentos futuros: evaluar escenarios o seguimiento; no afirmar de antemano que aumentarán el MRR.

La decisión propuesta es cómo medir esos movimientos y qué descuentos mantener, ajustar o limitar. Éxito inicial: saldo inicial + movimientos = saldo final, sin doble conteo, con causas identificables y límites explícitos. La diferencia entre bruto y neto cuantifica descuento aplicado; no demuestra por sí sola pérdida económica frente a no ofrecerlo.

## 3. Necesidad real y aclaración previa del alcance

**Separar servicio/uso, precio, descuento y pago**, y comprobar si menor ingreso inmediato se compensa con permanencia, ampliación o adquisición. **«¿Los descuentos contribuyen a un crecimiento económico sostenible mediante más clientes, mayor permanencia o ampliación de servicios?»**.

**Antes de desarrollar el caso, reconocer estas aclaraciones:**

- ¿Aumentar MRR es el objetivo final o un medio para aumentar ingresos, rentabilidad, liquidez o cuota de mercado?
- ¿Qué busca la política: ampliación, retención, adquisición o, si aplica, reactivación? ¿A quién se dirige? Los ejemplos sobre existentes no prueban exclusividad.
- ¿Qué horizonte, criterio de éxito y restricciones comerciales/financieras corresponden?

Las prioridades empresariales alternativas son hipótesis de contexto, **sin desarrollar un estudio estratégico o de cuota de mercado en este alcance**. Las métricas relacionadas con ingreso, permanencia y valor del cliente sí se crearán y evaluarán para complementar la respuesta CFO, con definiciones, datos o supuestos explícitos. No asumir respuestas ni dejar que su ausencia bloquee el modelo que exige el reto. Presupuesto de Marketing y tratamiento contable siguen pendientes. MRR, ingreso, utilidad y efectivo son resultados diferentes; más clientes o ARR anualizado no demuestran mayor LTV por cliente.

**Oportunidad de profundización — fuera del análisis actual:** investigar si una reducción de costos y gastos permite ofrecer descuentos. Como hipótesis, el MRR podría disminuir sin deteriorar el margen de utilidad si los ahorros compensan la reducción del ingreso; esto no garantiza mantener la utilidad total. Ampliar el análisis permitiría evaluar ese equilibrio y sus efectos en retención y captación de mercado.

## 4. Preguntas analíticas

**Pregunta principal:** ¿La política de descuentos mejora o deteriora el ingreso recurrente neto y el valor económico de los clientes durante el horizonte evaluado?

Para concluir sobre utilidad, incorporar costos y margen.

| Pregunta | Acción y evidencia necesaria |
| --- | --- |
| **1. «Si un cliente pagaba 100 y ahora paga 80, ¿contrajo 20 o recibió un descuento?»** | Agregar descuentos: tipo fijo/porcentual, valor, porcentaje con base de cálculo y fechas de inicio/fin para determinar duración. Vincularlos a suscripción y componentes; conservar bruto, descuento y neto separados. El pago aislado no identifica la causa. |
| **2. «¿Qué pasa si su suscripción creció de 100 a 130, pero tiene un descuento de 30 y sigue pagando 100? ¿Y cuando desaparezca el descuento, eso cuenta como expansión?»** | Expansión de MRR es un aumento del ingreso recurrente mensual de un cliente existente. De bruto 100 a 130 con descuento 30, el neto sigue en 100: no hay expansión neta. Si el aumento proviene de más servicios/uso, hay expansión subyacente +30; si proviene de la tarifa, es pricing. Al vencer el descuento, el neto sube a 130: expansión neta +30 por fin del descuento, sin nueva expansión subyacente. |
| **3. «Quiero saber qué está pasando con el negocio subyacente»** | MRR bruto/neto total y promedio por cliente; ARR; retención/churn, permanencia, NRR/GRR, LTV e ingreso neto acumulado por cohorte. Cambios de servicios/uso separados de tarifas y descuentos; comparación antes/durante/después, tendencia previa y grupo comparable sin descuento cuando exista. |
| **4. «¿Y cuánto revenue estamos dejando de capturar por decisiones comerciales?»** | Cuantificar descuentos aplicados por mes y acumulados: bruto menos neto. Evaluar si permanencia, adquisición o ampliación compensan esa reducción durante el horizonte. Para estimar ingreso incremental, comparar con lo esperado sin descuento; para utilidad, agregar costos/margen. |
| **5. ¿Qué puede y qué no puede responder el modelo actual, y cómo debe evolucionar?** | Auditar cliente + mes + monto pagado; agregar suscripción, componentes/uso, precios, estados y descuentos con historia. Conciliar saldo inicial + movimientos = saldo final, separando cliente, pricing y descuentos. Validar los tres ejemplos del CFO. |

## 5. Definiciones y métricas — propuestas

**Reglas de clasificación del caso:**

- **Expansión/contracción subyacente:** aumento/disminución del valor recurrente por cambios de plan, servicios, cantidades o uso monetizable de un cliente que permanece activo, excluyendo cambios de tarifa y descuentos. Más servicios sin mayor valor se registra como cambio de servicio, sin expansión monetaria.
- **Pricing:** efecto de cambiar la tarifa para los mismos servicios/uso. Si cantidad y tarifa cambian a la vez, valorar primero la cantidad a tarifa anterior y después la tarifa sobre la cantidad actual. Componentes nuevos: precio actual; eliminados: precio anterior.
- **Descuento:** reducción comercial respecto del bruto. Su inicio/ampliación reduce el neto; su reducción/vencimiento aumenta el neto. Nunca se clasifica como ampliación o reducción subyacente.
- **Momento y estado:** reconocer el cambio cuando entra en vigor, independientemente del cobro. Primera activación, baja total y retorno tras baja se clasifican como nuevo negocio, churn y reactivación; no como expansión/contracción de clientes que continúan activos.

**MRR neto = MRR bruto − descuentos.** Por tanto, **ΔMRR neto = movimientos subyacentes + efecto de pricing − Δdescuentos**. Facturación y cobro no equivalen automáticamente a MRR. Sin evidencia de la causa, clasificar como cambio no identificado.

| Medida | Definición propuesta |
| --- | --- |
| MRR bruto, descuentos y MRR neto | Sumar componentes recurrentes al grano mensual; conciliar bruto menos descuento con neto. |
| MRR neto total y promedio | Total y total dividido por clientes activos; definir actividad contractual. |
| Retención y churn | Seguimiento de clientes activos al inicio; permanencia sin baja y bajas sobre esa población, en igual periodo. Reactivaciones separadas. |
| Permanencia | Duración observada y retención a plazos fijos; clientes aún activos no tienen vida completa conocida. |
| Ingreso neto acumulado | Suma por cliente/cohorte en horizonte común; permite evaluar compensación del descuento, no rentabilidad sin costos. |
| Desviación frente a tendencia | MRR observado menos esperado según crecimiento previo; referencia hipotética, no efecto causal demostrado. |

**Comparación correcta:** antes/durante/después, incluyendo vencimiento; cohortes con igual seguimiento. Separar existentes, nuevos, reactivados y con/sin descuento. Justificar ventanas con duración, ciclo e historia disponible; la demo usa seis meses previos, tres de descuento y seis posteriores; no es un plazo universal. Tendencia supone continuidad: revisar estacionalidad y acumular crecimiento al proyectar varios meses. ARR complementará la escala mensual; LTV estimará valor durante la relación con supuestos explícitos. Cada resultado indicará población, periodo y segmentos cubiertos.

**Métricas complementarias:** crear y evaluar MRR/ARR, LTV, retención/churn, permanencia, NRR/GRR e ingreso acumulado para interpretar evolución y escenarios de descuentos. Definir variantes, cohortes y horizonte antes de calcular; no inferir LTV automáticamente de mayor MRR. ARR = MRR × 12 bajo esa convención, no ingreso anual realizado. LTV es estimación de ingreso o margen por cliente, no dato observado completo. NRR/GRR distinguen retención de ingresos con/sin ampliaciones. CAC/recuperación y margen se evaluarán según intención comercial y disponibilidad de costos; faltantes explícitos. Si datos reales no permiten una métrica, demostrarla mediante ejemplo sintético separado y documentar lo necesario para calcularla realmente. Esto no convierte escenarios en pronósticos verificados. [ARR, Stripe](https://support.stripe.com/questions/understanding-monthly-recurring-revenue-%28mrr%29-and-annual-recurring-revenue-%28arr%29); [métricas, ChartMogul](https://chartmogul.com/saas-metrics/).

## 6. Datos necesarios — inventario inicial

Cliente y suscripciones/estados/fechas; producto, cantidad/uso y precios con vigencias; descuentos con monto fijo o porcentaje, inicio/fin, alcance, objetivo, motivo y autorización; facturas y pagos vinculados. Mantener historia y distinguir varias suscripciones por cliente. Para LTV: ingreso neto, permanencia/churn, cohortes y supuestos de evolución; costos/margen si se estima contribución. Para CAC/recuperación: unidades de gasto y adquisición atribuible verificadas.

## 7. Datos disponibles y calidad

Transactions aporta cliente, mes y monto pagado: permite describir pagos/cambios, no identificar contratos, descuentos ni causas. Cero no prueba churn; primer pago observado no prueba adquisición. Industry permitiría segmentar tras validar identidad; S&M no identifica descuentos y sus unidades requieren aclaración.

Reutilizar [inspección de fuentes](../datos/inspeccion.md); validar grano, claves, vigencias, importes y relaciones antes de calcular. Conciliación contra origen y definiciones comerciales pendientes; hashes solo prueban integridad. Con lo disponible no hay evaluación real de descuentos ni MRR contractual demostrado.

## 8. Hipótesis y comprobación — propuestas

Mayor permanencia, ampliación o adquisición podrían compensar menor ingreso inmediato. Contrastar con las medidas del componente 5 según objetivo, cohortes y plazo. Usar el crecimiento previo como línea base.

Antes/después y tendencia mejoran la descripción, pero selección de clientes, precios u otros cambios pueden explicarla. Comparación con clientes similares sin descuento o experimento, cuando viable, fortalecería atribución. Bruto menos neto mide descuento aplicado, no ventas que habrían ocurrido sin él; vencer el descuento no demuestra éxito.

## 9. Análisis — implementado en la demo

**Pregunta y decisión:** evaluar ingreso recurrente neto y valor del cliente para mantener, ajustar o comprobar condiciones de descuento.

**Procedimiento aplicado:**

1. **Comprobar:** verificar datos, seis meses previos comparables y puente; comparar ingreso acumulado con la referencia sin descuento. El histórico real no permite identificar el efecto; la respuesta actual es una demo.
2. **Localizar:** separar elegibles del resto y periodos previo/durante/posterior. Si hay diferencia, concentrar el detalle en su aporte; si el total es cero, comprobar compensaciones temporales. Sin diferencia localizada, no inventar un problema.
3. **Explicar:** conciliar diferencia bruta menos descuentos y comprobar en componentes/movimientos qué cambió en servicios, tarifas o vigencias. Revisar retención solo si la evidencia lo requiere; estabilidad agregada no descarta todas las hipótesis.
4. **Actuar:** según resultado y objetivo, proponer piloto acotado, revisión de condiciones o comprobación de otro beneficio. Finanzas y Comercial como responsables propuestos; no aprobar política real por la simulación.
5. **Evaluar:** revisar mensualmente neto/puente y cerrar tras vigencia más seguimiento equivalente. Comparar acumulado y retención frente a referencia; margen cuando haya costos. Modelo validado e impacto real son comprobaciones distintas.

ARR, ARPU, LTV, NRR/GRR, churn y permanencia permanecen disponibles como respaldo; cada hallazgo determina qué complemento revisar. [Focos y recorrido aplicado](../../notebooks/03_modelo_cfo.ipynb).

## 10. Diagnóstico — demo

Julio 2025–marzo 2026: positivo +9.000 UM; negativo −3.000 UM; compensado 0 UM frente a referencias sin descuento. La diferencia se concentra en 50 elegibles; el resto aporta 0. En el compensado, −3.000 UM durante descuento y +3.000 UM después explican el equilibrio. Bajas y actividad coinciden por cliente entre alternativas; no se observa beneficio de retención en esta demo. Causalidad real y rentabilidad siguen abiertas.

## 11. Acción de negocio — propuestas condicionadas

- **Resultado positivo:** validar condiciones en piloto acotado antes de extender; comprobar costos/margen.
- **Negativo:** revisar monto/duración y evidencia de ampliación o permanencia que compense la reducción.
- **Equilibrio:** si el objetivo es aumentar ingreso acumulado, revisar condiciones; si es retención, comprobar ese beneficio.

Finanzas y Comercial: registrar objetivo, contratos y grupo comparable antes del piloto; revisión mensual y cierre tras descuento más seguimiento. Responsables propuestos, sin intervención real ejecutada.

## 12. Solución analítica — implementación local

El modelo implementa suscripciones, componentes/precios y descuentos con vigencias, separados de pagos. Derivar vistas mensuales bruto/descuento/neto y puente: saldo inicial + movimientos = saldo final; agregar al grano correcto antes de joins y conciliar pagos cuando difieran del MRR. Validar los tres ejemplos del reto y cambios simultáneos sin doble conteo. RF-05, RF-08, RF-09 y RF-11. [Tablas, contratos y reproducción](../datos/modelo-cfo-demo.md).

## 13. Evaluación y aprendizaje — validación automatizada; revisión humana pendiente

Los ejemplos, el puente y las métricas se contrastan con fixtures independientes. La revisión humana de las respuestas sigue pendiente. Verificar si cada hallazgo justifica el siguiente análisis y aporta a la pregunta principal. Efectividad comercial requiere piloto y seguimiento frente a referencia; todavía no hay impacto real medido.

## Presentación y respaldo

Notebook: qué medimos, alcance mostrado ahora y justificación del plazo, métrica/fórmula y datos; cálculos plegados. Una pregunta/gráfica a la vez, usando código reutilizable y contexto fuera de figuras.

Respaldo: [registro de lecturas](../proceso/cfo-comparacion-lecturas.md) e [inventario de preguntas](../proceso/cfo-inventario-preguntas.md).
