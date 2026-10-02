# CRO — cobertura de preguntas y métricas

Revisión 2026-09-30. Contrastados: preguntas y métricas aceptadas en `docs/casos/cro.md`, propuesta de cuatro tablas, generador, esquema SQLite y consulta de métricas actuales. **Datos y cálculos ampliados ejecutados.** La revisión inicial detectó faltantes; la implementación posterior los cubre bajo supuestos sintéticos. No acredita causas reales.

## Preguntas registradas y cálculos disponibles

Preguntas conservadas con la redacción registrada en `docs/casos/cro.md`; no son transcripciones literales de toda la conversación. Tener un cálculo disponible no equivale a haber respondido toda la pregunta. La primera gráfica y conclusión cubren solo total general y comparación mensual; falta desarrollar los segmentos.

Actualización: el bloque de datos y cálculos ya está construido; diagnóstico, decisiones y gráficas se revisarán con el candidato. CSV en `resultados/cro/metricas/{escenario}/`.

| Pregunta | Cálculo disponible |
| --- | --- |
| ¿Cómo compara el CRO New y Won: totales del mismo mes o seguimiento de las mismas entradas? | `resultado_global.csv`: entradas/cierres/pagadores y crecimientos mensuales; `origen_cierres.csv`: mes de entrada de los cierres. La regla histórica usada por el CRO real permanece desconocida. |
| ¿Cuánto creció New, frente a qué periodo y en qué segmentos? | `demanda.csv`: volumen, diferencia y crecimiento; segmentación por canal, perfil, industria, producto, región y campaña. |
| ¿Cambió la conversión y, si cayó, en qué transición? | `etapas.csv`: denominadores, avances, saltos, pérdidas y sin avance a 30/60/90 días. |
| ¿Marketing trae más demanda frente al histórico? | `demanda.csv`: captaciones atribuidas al origen Marketing de la simulación y crecimiento mensual. Sin requerir pagos. |
| ¿Cambió la calidad de los leads o el criterio para calificarlos? | `calidad.csv` y `descalificaciones.csv`: cobertura, calificados/evaluados y motivos; versión v1 documentada. |
| ¿Cambió la rapidez o cobertura de atención y seguimiento? | `atencion.csv`: espera, primer intento, cobertura, puntualidad, contacto efectivo; visitas sin intento incluidas. |
| ¿Se deterioró el avance después de SQL? | `etapas.csv`, `perdidas.csv` y `prioridad.csv`, filtrando SQL/Demo/Proposal. |
| ¿Cómo contribuye cada ruta al crecimiento total? | `resultado_global.csv`, `pagadores.csv` y `captacion_pago.csv`, por tipo de entrada. Producto sin etapas comerciales. |
| ¿Se acumulan casos lentos o todavía no tuvieron tiempo de avanzar? | `etapas.csv`: mediana/P90 de permanencia y antigüedad de abiertos; seguimiento y ventanas explícitos. |
| ¿Se convierten menos o tardan más? ¿Los cierres vienen de entradas antiguas acumuladas? | `cohortes.csv`: New → Won a 30/60/90 días, mediana/P90 de tiempos y abiertos; `origen_cierres.csv`. |
| ¿Qué freno tiene mayor impacto potencial en nuevos pagadores? | `prioridad.csv`: volumen, brecha respecto al histórico y vínculo descriptivo con pago. La intervención y su efecto siguen por analizar, no se deducen causalmente de una tasa. |

## Modelo suficiente: cuatro tablas de negocio y un catálogo

1. **Prospectos — ampliar `dim_cuentas`.** ID, fecha de captación, tipo de entrada, canal/campaña, industria, producto, región; fecha/responsable de asignación; criterios de calidad observables, resultado de evaluación, fecha, versión y motivo de descalificación.
2. **Registros de etapas — ampliar `fact_etapas`.** ID de visita, cuenta, etapa, entrada, salida, destino, resultado; motivo de pérdida, responsable y asignación por etapa. Permitir varias visitas a la misma etapa y destinos que omitan etapas, sin convertirlos en pérdidas.
3. **Interacciones — crear.** ID, cuenta, visita cuando aplique, fecha, tipo, resultado y responsable. Distinguir intento de intercambio efectivo; un caso sin interacción permanece en el denominador.
4. **Pagos — crear.** ID, cuenta, fecha y estado válido/no válido. Para identificar nuevos pagadores: historial previo y comienzo de observación conocido. La simulación debe declarar explícitamente qué cuentas no tenían pagos previos; el primer pago observado por sí solo no basta.

**Catálogo `dim_etapas`:** nombres, orden y siguiente etapa. Es auxiliar; no reemplaza ninguna de las cuatro tablas. **Ganados y métricas son resultados derivados**, no fuentes adicionales. Mismos IDs y fechas compatibles entre las tablas; agregar interacciones/pagos antes de unirlos a etapas para no multiplicar registros.

## Reglas necesarias, sin más tablas de negocio

- Configuración: unidad cuenta = oportunidad para esta demo; fecha de corte, periodos comparados, ventanas, criterios/versiones de calidad y plazos por etapa. Supuestos sintéticos explícitos, sin atribuirlos al CRO.
- Nuevos pagadores: primer pago válido con historia suficiente; Won mide cierre comercial. Se permite Won sin pago y pago desde producto sin Won.
- Calidad: definir criterios antes de generar etiquetas; no derivar calidad de haber ganado. Descalificación de prospecto y pérdida comercial son conceptos distintos.
- Ventanas: mismo seguimiento para las poblaciones comparadas, numerador/denominador visibles, faltantes distintos de cero. «Sin avance a 30 días» no equivale a perdido ni necesariamente abierto al corte.
- Comparar por etapa y tipo de entrada, luego canal/perfil; usar producto/región cuando aporten al diagnóstico. La mezcla de segmentos puede cambiar el total.

## Criterio para declarar el bloque completo

Cada fila anterior cuenta con datos, cálculo reutilizable y resultado tabular; se ejecutaron controles de integridad y fixtures independientes para las familias de métricas. La revisión humana e interpretación siguen pendientes. Comprobar claves, relaciones, fechas, duplicados, saltos/reingresos, madurez, ausencia de evaluación/contacto, Won sin pago, compra directa y pagos inválidos. Conciliar totales con detalle. No basta contar archivos ni pasar las pruebas del modelo parcial.

Para datos reales sigue pendiente conciliar contra el sistema de origen. Datos sintéticos completos permiten demostrar el método, pero no probar qué pasó realmente ni determinar una causa solo con asociaciones.
