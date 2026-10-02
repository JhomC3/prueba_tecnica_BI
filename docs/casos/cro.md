# Caso CRO — formulación

**En curso · 2026-09-30.** Lectura del candidato organizada con IA. Decisión inferida, todavía en discusión; no confirmada por un CRO entrevistado ni respaldada por hallazgos comerciales.

## Requerimiento original

Fuente: [reto técnico](../fuentes/reto-tecnico.md).

> Aumentamos bastante el volumen en las primeras etapas del funnel, especialmente en New, pero los clientes nuevos no están creciendo al mismo ritmo. Marketing dice que está trayendo más demanda. Sales dice que la calidad bajó. Otros creen que atendemos lento o que el problema está después de SQL. Además, hay usuarios que pagan directamente desde producto, otros entran casi directo a SQL y otros pueden durar semanas en una etapa. Hoy vemos volúmenes y conversiones, pero no tenemos una lectura suficientemente clara de dónde estamos perdiendo crecimiento ni por qué.

## Pregunta principal y recorrido — 2026-10-01

**Calidad — decisión 2026-10-01:** comprobar primero si existe una puntuación de leads. Si existe y es comparable, evaluar su media mensual en New, global y por canal. Si no existe, continuar con la información disponible y proponer implementar la medición. Para demostrar el análisis generamos puntuaciones aleatorias de 0 a 100, sin diseñar criterios de scoring ni usarlas como evidencia de una causa real. La pregunta de referencia se conserva.

**¿La tasa de conversión de New a Won aumentó o disminuyó después del aumento de New?**

Recorrido acordado: confirmar el aumento de New y sus canales → comparar conversión → revisar calidad de New → localizar transiciones afectadas → investigar atención/tiempos y otras hipótesis → conectar hallazgos con acciones y seguimiento.

La comparación antes/después y el filtrado conjunto New/canal están pendientes de consolidar. Las vistas existentes de calidad y algunas etapas mezclan tipos de entrada; no atribuir sus resultados a New sin separarlos. Las caídas a 30 días no prueban menor conversión final ni causas. Entrar directamente a SQL no acredita calidad; se analiza desde SQL, por separado. Producto se conserva para explicar crecimiento total, fuera de New → Won.

Las preguntas registradas abajo se conservan. El notebook cambia su orden y numeración; los bloques complementarios quedan disponibles sin obligar a recorrerlos todos.

## 1. Quién decide

El CRO. Revisar primero datos y definiciones; preguntar solo lo que cambie la decisión y no pueda resolverse con evidencia.

## 2. Decisión y éxito — propuesta

**Decidir qué acciones priorizar y en qué etapas o rutas intervenir para mejorar la conversión a nuevos clientes pagadores.**

La intervención concreta se elegirá después del diagnóstico. «Tomar medidas necesarias» es demasiado general; tampoco asumimos problemas en todas las etapas: pueden influir mezcla de rutas o maduración.

- **Objetivo:** mejorar el crecimiento de nuevos pagadores.
- **Necesidad:** saber dónde se limita ese crecimiento y por qué.
- **Éxito inicial:** elegir una intervención fundamentada, con responsable y seguimiento. Meta, horizonte y restricciones pendientes de evidencia.

## 3. Necesidad real

**Comprobar cómo se compara el crecimiento de New y Won; distinguir menor conversión, mayor tiempo hasta el cierre y cambios en las entradas que originan los cierres.** Después localizar etapas/segmentos afectados y revisar calidad y atención. Todavía no sabemos si cayó la conversión.

Necesitamos comprobar si existe una definición de calidad y si se registra. Si falta, proponer criterios observables —ajuste al cliente objetivo, necesidad e intención de compra— como supuestos pendientes de validación. No definir baja calidad únicamente por no convertir. Las métricas corresponden al componente 5.

## 4. Preguntas analíticas — propuesta para revisar

**Enfoque acordado con el candidato: desempeño por etapa, periodo y segmento.** IDs/eventos individuales sirven para calcular tasas y tiempos; no construiremos historias individuales como análisis principal. New → Won y formas de entrada aportan contexto al resultado global.

Recapitulación de la lectura del candidato; la última pregunta conecta el análisis con la prioridad de intervención.

| Pregunta | Evidencia necesaria |
| --- | --- |
| ¿Cómo compara el CRO New y Won: totales del mismo mes o seguimiento de las mismas entradas? | Definiciones, fechas, periodo base y regla de comparación. Los Won del mes pueden proceder de entradas anteriores. |
| ¿Cuánto creció New, frente a qué periodo y en qué segmentos? | Volúmenes; canal, producto y región disponibles. |
| ¿Cambió la conversión y, si cayó, en qué transición? | Entradas y avances por cohorte/ruta, con igual ventana de seguimiento. |
| ¿Marketing trae más demanda frente al histórico? | ID, fecha de entrada y origen/canal/campaña. Primer pago no es necesario para verificar esta afirmación. |
| ¿Cambió la calidad de los leads o el criterio para calificarlos? | Perfil, calificación y motivos de descalificación. |
| ¿Cambió la rapidez o cobertura de atención y seguimiento? | Entrada, asignación, contactos, interacciones y plazo acordado. |
| ¿Se deterioró el avance después de SQL? | Conversiones, pendientes, cierres y motivos de pérdida por transición. |
| ¿Cómo contribuye cada ruta al crecimiento total? | Punto de entrada, secuencia y pago; self-serve y entradas directas. |
| ¿Se acumulan casos lentos o todavía no tuvieron tiempo de avanzar? | Permanencia, antigüedad de abiertos y madurez, por segmento. |
| ¿Se convierten menos o tardan más? ¿Los cierres vienen de entradas antiguas acumuladas? | Vincular New y Won de las mismas entidades; conversión acumulada por tiempo transcurrido, pendientes y mes de entrada de cada cierre. |
| ¿Qué freno tiene mayor impacto potencial en nuevos pagadores? | Volumen afectado, brecha comparable y vínculo con pago; estimación condicionada, no causalidad probada. |

## Precisiones del análisis

- **Recorridos — precisión de IA:** medir cada etapa solo con quienes la recorren. Quien paga desde producto cuenta como nuevo pagador, pero no como pérdida de Demo o Proposal si nunca pasó por ellas. Quien entra directamente a SQL se analiza desde esa entrada. Después reunir los resultados de todos los recorridos para explicar el crecimiento total.
- **Conversión y tiempo — aporte del candidato:** New +10% no exige Won +10%. Antes de diagnosticar, comprobar cómo se comparan: los cierres del mes pueden venir de entradas antiguas. Seguir las mismas entradas permite distinguir menor proporción convertida de mayor tiempo hasta el cierre. Si aumenta el tiempo, disminuye la rapidez; un pendiente no es una pérdida. Comparar también rutas/perfiles.
- **Evidencia — precisión de IA:** separar hechos, supuestos e hipótesis; no simular respuestas del CRO como evidencia. El enunciado dice **New**, no MQL.

## 5. Definiciones y métricas — selección aceptada

El candidato aceptó estas métricas el 2026-09-30. Para la demo se fijaron unidad, ventanas, plazo y criterios ilustrativos en [modelo CRO](../datos/modelo-cro-demo.md); las reglas reales siguen sin confirmar.

**Medir resultados, tiempos y atención; comparar histórico y poblaciones equivalentes.**

| Métrica | Cómo medirla |
| --- | --- |
| Entradas | Usuarios, cuentas u oportunidades únicos que entran a una etapa en el periodo; elegir una unidad consistente. |
| Conversión de etapa | De los que entraron, porcentaje que alcanza la etapa objetivo dentro de una ventana definida. Separar transición siguiente y saltos. |
| Pérdidas y pendientes | De esa misma cohorte, porcentaje perdido y porcentaje todavía abierto al corte; distinguir quienes avanzaron. |
| Primer contacto | Tiempo desde entrada hasta primer intento; separar espera de asignación y atención posterior. Mostrar mediana y percentil 90, con porcentaje sin intento. |
| Cobertura y puntualidad | Porcentaje con intento y porcentaje atendido dentro del plazo acordado. No inventar el plazo; usar casos elegibles cuyo plazo ya venció. |
| Contacto efectivo | Porcentaje de intentados con intercambio real; definir respuesta o conversación. Un correo enviado no es contacto efectivo. |
| Permanencia y antigüedad | Tiempo entre entrada y salida por etapa; para abiertos, tiempo desde entrada hasta el corte. Mediana/percentil 90 por separado. |
| Calidad de entrada | De los leads evaluados, porcentaje que cumple el perfil definido. Cobertura: porcentaje del total que evaluamos. El perfil está pendiente; no comprar no implica por sí solo baja calidad. |
| Motivos de pérdida | Distribución de motivos entre perdidos/descalificados; informar porcentaje sin motivo registrado. |
| Nuevos pagadores | Entidades cuyo primer pago válido ocurre en el periodo; tiempo desde entrada hasta pago. Primer pago observado no prueba adquisición si falta historia previa. |
| Tiempo New → Won | Tiempo entre entrada a New y cierre Won de la misma entidad; complementar con porcentaje acumulado convertido según tiempo desde entrada, incluyendo pendientes. No aplicar a rutas que omiten New; definir Won y su relación con el pago. |
| Conversión New → Won por cohorte | Para quienes entraron juntos a New: porcentaje convertido tras ventanas ilustrativas de 30, 60 y 90 días, ajustables al ciclo histórico. Denominador: todas las entradas de esa cohorte con seguimiento suficiente para la ventana; no solo los ganados. |
| Origen temporal de los cierres | Distribuir los Won de cada mes según mes de entrada y ruta. Detecta si un aumento anterior provino de casos acumulados; no convierte ese aumento en una tasa de conversión. |

**Comparación correcta**

- Comparar cohortes de entrada con la misma ventana de seguimiento y suficiente maduración. Registrar periodo base y fecha de corte.
- **Lectura prioritaria:** mismo porcentaje a una ventana larga comparable, pero menor a una corta, es compatible con demora; menor porcentaje también a la larga puede indicar deterioro. No llamar «conversión final» a una ventana arbitraria ni inferirla solo de los ganados. Mostrar cuántos siguen abiertos.
- Mantener definiciones, unidad, reglas de elegibilidad y tratamiento de duplicados/reingresos. Si cambian, señalar la ruptura de comparación.
- Mostrar numerador y denominador junto al porcentaje. Ejemplo: 6% → 3% = −3 puntos porcentuales y −50% relativo; valorar tamaño de muestra antes de interpretar.
- Segmentar primero por ruta y etapa; después canal y perfil de cliente. Añadir producto/geografía si existen datos y una pregunta relevante, evitando grupos demasiado pequeños.
- Mostrar total y segmentos: un cambio en su composición puede reducir la conversión total sin deteriorar cada segmento.

**Interacciones:** tipo, fecha y resultado ayudan a explicar atención/avance. Más llamadas o correos no equivalen a mejor gestión. Los saltos, reingresos, unidad, ventanas y criterios de calidad requieren definición antes del cálculo.

**Límite:** faltan eventos CRM, rutas y contactos en los CSV. Podemos proponer medición/modelo y ejemplos ilustrativos; no demostrar una causa histórica.

Referencia de medición: [analítica de ventas de HubSpot](https://knowledge.hubspot.com/reports/create-sales-reports-in-the-sales-analytics-suite), revisada para conversión, saltos, duración y contactos; no constituye evidencia del caso.

## Presentación

**Requerimiento original → 13 componentes del [marco](../metodo/marco-de-trabajo.md).** Cada uno: pregunta, respuesta breve y evidencia o pendiente; detalle desplegable.

Las preguntas alimentan los componentes 3–7, no un interrogatorio al CRO. Hipótesis, análisis, diagnóstico, acciones, solución y evaluación pendientes.

## 6. Datos necesarios — inventario inicial

| Necesitamos | Disponibilidad inicial |
| --- | --- |
| Identidad y eventos de entrada/salida por etapa, incluido Won | No están en los CSV. |
| Ruta, canal, perfil y criterios de calidad | Industry aporta industria; faltan ruta, canal y calificación. |
| Asignación, contactos, interacciones y resultados | No están en los CSV. |
| Motivos de pérdida y descalificación | No están en los CSV. |
| Pagos vinculados a las mismas entidades | Transactions aporta ID, mes e importe; falta vínculo comprobado con CRM y definición de nuevo pagador. |

## 7. Datos disponibles y calidad — inspección técnica ejecutada, revisión humana pendiente

**Validación contra el origen:** identificar sistema, fecha de extracción, filtros y corte; comparar conteos, totales y registros por ID con la fuente para el mismo alcance. Hoy no tenemos acceso al sistema original: esa conciliación está pendiente. Los hashes solo comprueban integridad; tampoco una fuente conciliada garantiza ausencia de errores de captura.

| Archivo | Contenido | Qué revisar |
| --- | --- | --- |
| Transactions | Cliente, mes e importe | Periodos, ceros, claves y significado del pago. |
| Industry | Cliente e industria | Fila vacía y correspondencia de IDs con Transactions. |
| S&M_spend | Gastos por mes y categoría | Moneda, escala y formato antes de comparar importes. |

El [perfil preliminar](../datos/data_profile.json) se contrastó mediante una [inspección reproducible](../datos/inspeccion.md): muestras localizables, controles y registro de ejecución. Codex ejecutó Python y generó el informe HTML; revisión del candidato pendiente. No se validaron joins ni definiciones comerciales. Jupyter instalado; inspección y modelo sintético disponibles en notebooks ejecutados, sin equivaler a validación comercial.

### Observaciones del candidato — guardar, sin ejecutar

Al revisar el resumen, el candidato cuestionó significado de ID, utilidad para CRO, entradas/salidas y categorías de gasto. Es una revisión conceptual; todavía no una comprobación de filas o controles contra los originales.

- **Definición disponible:** el enunciado describe Transactions como ingresos mensuales por cliente e Industry como industria de cada cliente ([fuente](../fuentes/reto-tecnico.md)). ID identifica al cliente en ese contexto, no a la industria. La correspondencia concreta entre `N` y `Cliente N` sigue como supuesto por validar.
- **Límite CRO:** pagos no equivalen a eventos Won ni contienen fechas de ingreso al funnel. No inferir adquisición, salida o churn de ausencia/cero. El perfil inicial muestra los mismos IDs cada mes; aquí no hay desapariciones mensuales que permitan deducir salidas.
- **Utilidad acotada:** describir importes observados por mes y, tras validar el vínculo, por industria. No localizar causas de pérdida por etapa.
- **Gastos:** el enunciado confirma Sales & Marketing agregado, pero no moneda/escala ni atribución por equipo, canal o cliente. Payroll expenses significa gastos de nómina; Travel, Freelance, SoftwareTools y Team necesitan definición antes de asignarles una función comercial.
- **Para después:** pedir diccionario y claves; eventos CRM, rutas, calificación y estados; definición/unidad de gastos. Son preguntas registradas, no tareas nuevas aprobadas ni cálculos ejecutados.

## 8–13. Pendientes

8. Hipótesis · 9. Análisis · 10. Diagnóstico · 11. Acción · 12. Solución · 13. Evaluación. Se desarrollarán paso a paso; el límite de datos indicado arriba sigue vigente.

## Demostración sintética — planificación

El candidato autorizó completar todos los datos y cálculos antes de iniciar el análisis. Cuatro tablas de negocio más catálogo, escenarios y métricas ejecutados: [modelo y reglas](../datos/modelo-cro-demo.md), [cobertura de preguntas](../datos/cobertura-cro.md). Preparados para revisión; interpretación y gráficas se desarrollarán con el candidato. No acredita qué pasó realmente en Finora.
