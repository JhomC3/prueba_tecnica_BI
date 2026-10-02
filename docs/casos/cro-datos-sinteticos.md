# CRO — preguntas, métricas, datos y tablas

**Modelo ampliado generado el 2026-09-30.** Ver [archivos, parámetros y controles](../datos/modelo-cro-demo.md). Calidad, atención y pagos incorporados con supuestos de demostración; definiciones comerciales reales no confirmadas. La propuesta de campos de abajo se implementa con nombres técnicos documentados en el modelo.

**Cobertura comprobada:** [preguntas, métricas y faltantes](../datos/cobertura-cro.md). Cuatro tablas de negocio y un catálogo auxiliar implementados; resultados tabulares listos, gráficas e interpretación pendientes.

## Enfoque central: desempeño de cada etapa

**Etapa × periodo de entrada × segmento.** Para cada etapa: entradas, conversión a la siguiente, pérdidas, pendientes, tiempos y atención; comparar histórico y poblaciones equivalentes.

No presentaremos historias individuales de clientes. IDs y fechas son soporte para saber quién entró, quién avanzó y cuánto tardó; no el objeto de la presentación. Los totales aislados de dos etapas pueden corresponder a poblaciones distintas.

New → Won y tipos de entrada quedan como contexto para relacionar el desempeño de las etapas con el crecimiento; no reemplazan el análisis por etapa.

## Tablas propuestas

1. **prospectos.csv — una fila por cuenta potencial.**
   - id_prospecto, id_oportunidad (vacío en compra desde producto), fecha_entrada, tipo_entrada, canal, campaña, industria, perfil, producto, región.
   - responsable, fecha_asignación.
   - ajuste_perfil, necesidad, intención, fecha_evaluación, versión_criterios, motivo_descalificación. Calidad se calcula con criterios acordados; no por haber comprado.
2. **registros_etapas.csv — una fila por visita a una etapa.**
   - id_visita, id_prospecto, etapa, fecha_entrada_etapa, fecha_salida_etapa, etapa_destino, resultado, motivo_pérdida, responsable_etapa, fecha_asignación_etapa.
   - Etapas del enunciado; resultado: avance, perdido, abierto o ganado. Nuevas visitas registran reingresos.
3. **interacciones.csv — una fila por interacción.**
   - id_interacción, id_prospecto, id_visita (cuando aplique), fecha, tipo, resultado, responsable. La visita vincula la interacción con la etapa correcta.
4. **pagos.csv — una fila por pago.**
   - id_pago, id_prospecto, fecha_pago, estado_pago. Solo pagos válidos cuentan.

**Relación:** id_prospecto conecta las cuatro tablas. La primera demo tendrá una cuenta por prospecto y como máximo una oportunidad por cuenta, sin reasignaciones; no representa toda la complejidad de un CRM. Contar visitas/interacciones como clientes produciría duplicados. Won y primer pago se registran por separado.

**Definiciones:** tipo_entrada distingue atención desde New, entrada directa a SQL y compra desde producto. Los registros de etapa aportan entradas, salidas y tiempos para calcular su desempeño. Fecha de corte, ventanas, plazos de atención y criterios de calidad van en configuración común; no se repiten por fila.

**Salida calculada:** resumen por etapa, periodo de entrada y segmento; entradas, avances, conversión, pérdidas, abiertos, duración y atención. Se deriva de las fuentes, no se inventa por separado. Las interacciones se agregan antes de unirlas a visitas para evitar duplicados.

## Viabilidad con fuentes reales — investigación 2026-09-30

**Las cuatro tablas son un modelo analítico propio, no cuatro exportaciones nativas idénticas.** La documentación confirma fuentes equivalentes; no confirma qué registra Finora ni qué licencias tiene.

- **Prospectos:** HubSpot exporta contactos, empresas y negocios con propiedades y asociaciones. En producción conservaríamos sus IDs y relaciones separados; una cuenta puede tener varios contactos y oportunidades. [Exportación oficial](https://knowledge.hubspot.com/import-and-export/export-records).
- **Etapas:** Salesforce ofrece historial de oportunidades con etapa anterior, siguiente y fecha de modificación. HubSpot tiene fechas de entrada/salida y tiempos por etapa. Nuestra fila por visita se reconstruiría del historial disponible; el estado actual no basta para recuperar reingresos. HubSpot limita las revisiones conservadas por propiedad: 45 en contactos y 20 en empresas/negocios. [Salesforce](https://help.salesforce.com/s/articleView?id=analytics.reports_opp_history.htm&language=en_US&type=5), [propiedades de HubSpot](https://knowledge.hubspot.com/properties/hubspots-default-deal-properties), [historial y límites](https://knowledge.hubspot.com/properties/export-property-history).
- **Interacciones:** HubSpot permite obtener llamadas, notas y otras actividades por exportaciones específicas o API. Vincularlas a una visita de etapa sería una transformación nuestra mediante asociaciones y fechas; no asumimos que exista `id_visita` en el CRM. [Exportación de actividades](https://knowledge.hubspot.com/import-and-export/export-records).
- **Pagos:** HubSpot registra ID, fecha y estado cuando se utilizan sus opciones de procesamiento de pagos. Si no, necesitamos el sistema de cobros/facturación y una relación comprobada con la cuenta. Won no acredita un pago. [Propiedades de pagos](https://knowledge.hubspot.com/payments/hubspots-payments-and-subscriptions-properties).

**Campos no garantizados:** criterios/versiones de calidad, tipo de entrada y asignación por etapa requieren configuración, derivación o historial adicional. Las puntuaciones de calidad deben configurarse; no existe automáticamente nuestra definición. [Lead scoring de HubSpot](https://knowledge.hubspot.com/scoring/understand-the-lead-scoring-tool).

Antes de usar datos reales: confirmar significado de etapas/fechas, relaciones, historial conservado y licencia/permisos. No equiparar creación con entrada a New, ni fecha prevista de cierre con entrada efectiva a Won. Modelo viable; disponibilidad de cada campo pendiente de comprobar en el sistema concreto.

## Afirmación → preguntas → métricas → datos

1. **«Aumentamos el volumen, especialmente en New».**
   - **Pregunta:** ¿Cuánto, frente a qué periodo y en qué segmentos?
   - **Métrica:** entradas a New y crecimiento histórico.
     - **Datos:** registros_etapas: id_prospecto, etapa, fecha_entrada_etapa; prospectos: canal, campaña, industria/perfil, producto y región. Contar primera entrada, no reingresos.

2. **«Los clientes nuevos no crecen al mismo ritmo».**
   - **Pregunta:** ¿Cómo comparan New y Won? ¿Convierten menos, tardan más o cierran entradas antiguas?
   - **Métrica principal:** conversión de cada etapa a la siguiente, por grupo de entrada y ventana.
     - **Datos:** registros_etapas: ID, etapa, entrada/salida, destino y resultado; corte/ventana. Denominador: quienes entraron a esa etapa; incluir perdidos y pendientes, tratar saltos por separado.
   - **Métrica de contexto:** conversión/tiempo New → Won y procedencia temporal de los cierres.
     - **Datos:** entradas a New y Won de los mismos IDs y segmentos. Comparar ventanas iguales; el promedio de ganados no representa a los abiertos.
   - **Métrica:** nuevos pagadores.
     - **Datos:** pagos: ID, fecha y estado; historia previa suficiente para identificar primer pago.

3. **«Marketing trae más demanda».**
   - **Pregunta:** ¿Aumentaron las entradas atribuibles a Marketing?
   - **Métrica:** nuevas entradas de Marketing y crecimiento histórico.
     - **Datos:** prospectos: ID, fecha_entrada, canal/campaña; historial para confirmar entrada a New cuando corresponda. Sin primer pago.

4. **«Sales dice que la calidad bajó».**
   - **Pregunta:** ¿Existe un criterio, se evalúa y cambió la proporción que lo cumple?
   - **Métrica:** porcentaje calificado entre evaluados y cobertura sobre el total.
     - **Datos:** prospectos: criterios observables, fecha_evaluación, versión_criterios, ID, fecha_entrada y segmentos.
   - **Métrica:** motivos de descalificación.
     - **Datos:** prospectos: motivo_descalificación y evaluación. Distinguir motivo ausente de calidad baja.

5. **«Atendemos lento».**
   - **Pregunta:** ¿Cambió la espera, cobertura o respuesta efectiva?
   - **Métrica:** tiempo hasta primer intento y porcentaje dentro del plazo.
     - **Datos:** registros_etapas: entrada/asignación; interacciones: visita, fecha/tipo; plazo por etapa de configuración.
   - **Métrica:** cobertura de intentos y contacto efectivo.
     - **Datos:** todas las entradas de la etapa; interacciones vinculadas a la visita con fecha y resultado. Contacto efectivo requiere intercambio, no solo envío.

6. **«El problema está después de SQL».**
   - **Pregunta:** ¿Qué transición empeoró y por qué se registran pérdidas?
   - **Métrica:** conversión, pérdidas y pendientes por etapa.
     - **Datos:** registros_etapas: ID, etapa, fechas, resultado; ventana/corte común.
   - **Métrica:** distribución de motivos de pérdida.
     - **Datos:** registros_etapas: resultado y motivo_pérdida; informar motivos faltantes.

7. **«Pagan desde producto o entran directamente a SQL».**
   - **Pregunta:** ¿Cómo crece cada forma de entrada y qué etapas utiliza?
   - **Métrica:** entradas, conversión y nuevos pagadores por tipo de entrada.
     - **Datos:** prospectos: ID, tipo_entrada y fecha; historial: etapas/fechas; pagos: ID, fecha/estado. No exigir New o Demo a quienes los omitieron.

8. **«Pueden durar semanas en una etapa».**
   - **Pregunta:** ¿Aumentó la permanencia o solo hay entradas recientes?
   - **Métrica:** duración de visitas terminadas y antigüedad de abiertos, separadas.
     - **Datos:** registros_etapas: entrada/salida/resultado; corte común. Mediana y percentil 90; última interacción como contexto.
   - **Métrica:** conversión según tiempo transcurrido.
     - **Datos:** fechas de entrada y avances de los mismos IDs, segmento y ventanas comparables.

**Prioridad final:** volumen afectado y brecha comparable ayudan a priorizar intervenciones; no demuestran impacto causal. Se calculan con los datos anteriores.

## Generación y validación acotadas

- Tres escenarios: referencia sin deterioro, menor conversión en una etapa, mayor demora sin cambiar el resultado eventual programado.
- Parámetros: semilla, escenario, etapa, intensidad, tamaño/periodos y corte. Un script local, utilizable desde notebook.
- Misma configuración reproduce los datos. No exponer resultados futuros ni la respuesta esperada al analista/LLM.
- Verificar claves, fechas, relaciones, reingresos, conteos y patrón realmente generado; no asumir éxito por configurarlo.
- Datos reales: conciliar contra el sistema de origen. Esta demo: contrastar con generador/configuración.
- Guardar resultados aparte de inputs originales. Posponer selector web y combinaciones de problemas.
