# Contexto de la prueba y la postulación

Revisión de fuentes: 2026-09-29; rutas organizadas el 2026-09-30. Fuente de requisitos: el enunciado del reto (documento privado, no incluido). Los CSV originales están excluidos de esta copia pública; la demo usa datos sintéticos en `public/data/archivos/`. Este documento reúne contexto y observaciones iniciales; no es la spec de la solución.

## Objetivo y lectura de la evaluación

El proyecto debe resolver los casos y hacer visible cómo el candidato estructura el problema, procesa datos ambiguos, elige herramientas, usa y valida IA, comunica resultados y propone acciones medibles. La entrega y el proceso son evidencia de sus capacidades.

La introducción del reto declara ese interés en el pensamiento y la toma de decisiones. El rol de referencia agrega capacidades de modelado, SQL, BI, colaboración entre dominios, autoservicio y seguimiento al impacto. La libertad creativa permite elegir una forma de demostrarlas. No se conoce una rúbrica oficial ni su ponderación.

La lectura detallada, la distinción entre declaraciones e inferencias y la estrategia de demostración están en [Enfoque de la evaluación](metodo/enfoque-evaluacion.md). Ese documento orienta la especificación.

El [Marco de trabajo analítico](metodo/marco-de-trabajo.md), actualizado el 2026-09-30 a partir de la propuesta del candidato, guía la resolución de los casos y servirá para organizar tareas, dependencias, tiempos y evidencias de cierre.

## Rol de referencia

El rol de referencia conecta problemas ambiguos de Growth, Sales, Product y Finance con modelos de datos, métricas, análisis, decisiones y seguimiento al impacto. El dashboard es una parte de ese ciclo.

La oferta pide más de tres años de experiencia en áreas analíticas afines, SQL avanzado, herramientas de BI, experiencia con CRM, métricas SaaS, uso habitual de IA, comunicación con stakeholders e inglés B2. Python, experimentación y herramientas llevadas a producción son deseables. Estas son exigencias del rol de referencia, no afirmaciones sobre la experiencia del candidato.

Para esta prueba debemos demostrar: definición rigurosa del problema, ownership analítico, modelado, criterio sobre límites de los datos, comunicación ejecutiva y una solución que sirva para operar decisiones recurrentes. No basta mostrar gráficos o código generado.

(Detalle de la oferta privada retirado de la copia pública.)

## Escenario y plazo

Finora es la compañía SaaS colombiana del escenario de la prueba, con software financiero y operativo para PyMEs. Su modelo combina adquisición y pago desde producto con procesos comerciales asistidos. Se espera uso natural de IA y explicación del proceso.

El enunciado fija **cuatro días**. El usuario confirmó el 2026-09-30 un límite efectivo de entrega **antes del viernes 2026-10-02 a las 12:00, horario de Colombia**. Su objetivo es entregar el 2026-09-30 o el 2026-10-01 con calidad suficiente. Según lo comunicado al candidato, el proceso puede cerrarse antes si otro candidato entrega una solución convincente; se prioriza una entrega completa temprana.

(Enunciado completo privado, no incluido en la copia pública.)

## Caso 1: CRO y funnel comercial

Problema declarado: aumentan los leads, especialmente en New, y los clientes nuevos no crecen al mismo ritmo. Marketing señala más demanda; Sales plantea menor calidad; otras hipótesis son lentitud de atención o conversión después de SQL. Son hipótesis del escenario, todavía sin evidencia en los CSV.

Etapas: **New, Working, Engaged, SQL, Demo, Proposal y Won**. Hay usuarios que pagan desde producto, entradas directas a SQL y permanencias de semanas. Una conversión entre etapas no puede asumir que todos recorrieron el mismo camino ni que cohortes recientes ya tuvieron tiempo de convertir.

| Pregunta exigida | Evidencia o propuesta necesaria |
| --- | --- |
| ¿Cómo definir y medir recorridos distintos? | Definir rutas, unidad de análisis, cohortes, ventanas de conversión y tratamiento de saltos, reingresos y oportunidades aún abiertas. |
| ¿Dónde se concentra la pérdida de crecimiento? | Descomponer cambios por volumen, mix, conversión y tiempo en segmentos con denominadores comparables. |
| ¿Qué hipótesis lo explican? | Separar demanda, calidad, velocidad y conversión post-SQL; identificar datos y pruebas para validar cada una. |
| ¿Qué construir para operar el funnel? | Vista recurrente con decisiones, responsables, cadencia, métricas de seguimiento y detalle operativo. |

**Límite comprobado:** no se entregaron eventos del CRM, leads, oportunidades, rutas de adquisición, responsables ni timestamps de etapas. Los pagos permiten describir clientes pagadores observados, no identificar una etapa comercial responsable de la pérdida. Una demo con datos sintéticos debe etiquetarlos claramente y mantenerlos separados del histórico real.

## Caso 2: CFO y cambios del MRR

Modelo actual descrito: cliente, mes y monto pagado. El CFO pregunta si un cambio refleja la suscripción subyacente o un descuento temporal.

| Pregunta exigida | Evidencia o propuesta necesaria |
| --- | --- |
| ¿Qué responde el modelo actual? | Comparaciones de monto observado, con límites explícitos sobre actividad contractual, descuentos y razones de cambio. |
| ¿Cómo separar suscripción y precio pagado? | Proponer suscripciones, componentes de valor, pricing, descuentos con vigencias y estados; definir grano y relaciones. |
| ¿Cómo tratar inicio y fin de descuento? | Movimientos comerciales separados de contracción/expansión subyacentes y conciliación entre capas. |
| ¿Por qué cambió MRR y cuánto es comercial? | Puente reconciliado de MRR que explique cambios sin duplicarlos. |

Los tres ejemplos obligan a distinguir capas: 100 a 80 puede ser contracción o descuento; valor de suscripción de 100 a 130 con descuento de 30 puede dejar el pago en 100; el fin de ese descuento no demuestra expansión subyacente.

**Límite comprobado:** Transactions no tiene valor contractual, descuentos, plan, precio, uso ni estado de suscripción. Cero pagado no prueba churn contractual. El primer pago del histórico no prueba adquisición nueva cuando existe historia previa no observada. El importe mensual es una aproximación al MRR bajo supuestos a documentar, no una equivalencia demostrada entre caja y revenue recurrente.

## Fuentes entregadas y perfil observado

Perfil completo: `docs/datos/data_profile.json`. Conteos excluyen encabezados.

| Fuente | Estructura y volumen | Observación |
| --- | --- | --- |
| Transactions.csv | 66.674 filas, ID/month/amount, 1.961 clientes, 34 meses de enero de 2022 a octubre de 2024 | Una fila por cliente y mes; sin duplicados de esa clave ni campos vacíos. 33.703 importes son cero y ninguno es negativo. El enunciado exige multiplicar amount por 10.000 para COP. |
| Industry.csv | 1.962 filas leídas, ID/Industria | 1.961 clientes y una fila completamente vacía. IDs con formato `Cliente N`; requieren una regla de correspondencia con ID `N` en Transactions. |
| S&M_spend.csv | 34 filas, Month y siete categorías de gasto | Cobertura mensual coincide con Transactions y no hay meses duplicados. Valores como `$1.040` y `$0.120` tienen moneda, escala y separador sin confirmar. |

Industry contiene seis industrias: Restaurantes (529 clientes), Producción (454), Retail (428), Tecnología (241), Servicios profesionales (165) y Salud (144).

Al extraer N de `Cliente N`, la cobertura técnica de IDs es completa en ambas direcciones y las claves son únicas. El join literal da cero coincidencias. Esto valida la compatibilidad del formato, no la identidad de negocio; se debe registrar el supuesto antes del join analítico.

Los 1.961 clientes aparecen en cada uno de los 34 meses. Se observa un panel balanceado de montos con muchos ceros. Debemos investigar la semántica de esos ceros antes de usarlos como estados de vida de una suscripción.

No hay evidencia suficiente para confirmar unidad de gasto, atribución de adquisición, CAC por canal, LTV o causas comerciales. No aplicar a S&M el factor de Transactions sin confirmación. La ausencia de datos forma parte explícita de la prueba.

## Entregables literales

| Entregable | Condición |
| --- | --- |
| Video ejecutivo | Máximo cinco minutos, dirigido a CEO, CRO y CFO; situación, hallazgo, implicación, decisión y acción; argumento de negocio y técnico. |
| Demo y video del proceso con IA | Demo accesible por link y video de máximo cinco minutos que explique herramientas, pasos y uso de IA. |
| Material de soporte | Formato libre: modelos, SQL, notebooks, dashboards, HTML, spreadsheets, visualizaciones o prototipos según utilidad. |
| Nota corta | Preguntas priorizadas, supuestos, información faltante, cambios al modelo actual, uso de IA, validación y calidad de conclusiones. |
| Entrega | Links y archivos mediante formulario adjunto al correo del reto. No se ha aportado el formulario. |

## Prioridades para la especificación

1. Resolver ambos casos y hacer evaluable el criterio analítico y las competencias reales del candidato.
2. Formular decisiones de negocio, cuestionar premisas y documentar hipótesis y elecciones metodológicas.
3. Analizar el histórico de pagos y sus segmentos, con transformaciones y controles reproducibles que evidencien SQL y modelado.
4. Diseñar el modelo de descuentos y comprobar los ejemplos del CFO con casos claramente ilustrativos.
5. Proponer medición del funnel, datos necesarios e hipótesis accionables sin inventar hallazgos de CRM.
6. Justificar herramientas y visualizaciones por su utilidad, las capacidades que demuestran y la experiencia del evaluador.
7. Registrar desde el inicio ejemplos reales de uso de IA, revisión, corrección y validación.
8. Preparar una demo y narrativa con lectura ejecutiva, exploración, respaldo técnico y acciones con seguimiento del impacto.

Estas prioridades son una propuesta inicial. Stack, formato concreto, hosting, alcance del prototipo y secuencia de implementación se resuelven después de aprobar la constitución, durante entrevista, spec y plan.

## Pendientes de contexto

- Restricciones del formulario de entrega. Fecha/hora límite ya confirmadas en la entrevista.
- Definición de cero, monto pagado y actividad contractual.
- Unidad y formato numérico de S&M.
- Alcance elegido para la demo y datos de CRM/contratos adicionales, si existen.
- Requisitos de acceso al link de la demo.
- Capacidades y herramientas que domina el candidato y quiere evidenciar mediante esta prueba.

La entrevista SDD debe usar este contexto y preguntar únicamente lo que falta, de una pregunta a la vez y con un máximo de seis.
