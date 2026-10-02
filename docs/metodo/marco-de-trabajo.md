# Marco de trabajo analítico

**Versión consolidada: 2026-10-01.** Guía para responder solicitudes de cualquier área directiva. Conserva los 13 componentes propuestos por el candidato y sus criterios expresados públicamente. El recorrido y la ficha son una síntesis operativa de IA; no representan acceso a su pensamiento privado ni garantizan resolver cualquier pregunta. Las propuestas permanecen separadas de las decisiones confirmadas. Este documento guía el trabajo; la spec activa sigue definiendo el alcance de implementación.

## Regla principal: pragmatismo

Elegir la solución más simple que responda la pregunta y permita decidir. Cada análisis, métrica, tarea o herramienta debe aportar a ese propósito. Añadir complejidad únicamente cuando una necesidad comprobada la justifique. Reutilizar decisiones confirmadas y preguntar solo lo que cambie el alcance, la medición o la decisión.

## Recorrido práctico

**Enfocar → comprobar → localizar → explicar → actuar → evaluar.** Cada resultado determina el siguiente análisis; el recorrido se adapta a la solicitud y puede retroceder cuando cambia la evidencia.

1. **Enfocar.** Conservar la solicitud y las preguntas originales. Identificar quién decide, qué necesita elegir, la pregunta principal y cómo reconocer una respuesta útil. Separar preguntas derivadas y propuestas de reformulación.
2. **Comprobar.** Verificar la premisa antes de explicar sus causas: qué sucede, desde cuándo y frente a qué referencia. Definir conceptos, población, periodo, métricas y datos disponibles. Si la premisa no se sostiene, corregir el planteamiento.
3. **Localizar.** Ir de lo general a lo específico: encontrar el foco y acotar la población de los siguientes análisis. Mantener referencias comparables; ampliar de nuevo si la evidencia lo exige. Priorizar cuando existan varios focos. Localizar un problema todavía no demuestra su causa.
4. **Explicar.** Contrastar explicaciones alternativas en el foco encontrado. Distinguir observaciones, asociaciones, explicaciones sustentadas e hipótesis pendientes. Buscar la comprobación que permita discriminar entre ellas.
5. **Actuar.** Vincular el hallazgo con una intervención o una siguiente comprobación. Proponer responsable, condiciones, plazo y resultado esperado. Diferenciar la acción del negocio de la herramienta que la apoya.
6. **Evaluar.** Verificar si se respondió la pregunta y si la solución permite decidir. Medir impacto cuando se ejecute la acción; mientras tanto, dejar el plan de medición. Incorporar aprendizajes y corregir el alcance cuando corresponda.

El recorrido sirve también para iniciativas, pronósticos, diseño o documentación: no obliga a buscar una caída ni una causa donde la solicitud no lo requiere. Los componentes siguientes comprueban cobertura; no son trece preguntas que deban formularse siempre ni trece entregables separados.

## Los 13 componentes

| Componente | Pregunta | Resultado y criterio para avanzar |
| --- | --- | --- |
| **1. Quién decide** | ¿Quién usa el análisis y ejecuta la decisión? | Decisor, usuarios y responsabilidades claros. |
| **2. Decisión y éxito** | ¿Qué decide y cómo sabremos si fue útil? | Alternativas, alcance, restricciones y éxito inicial definidos. |
| **3. Necesidad real** | ¿Qué necesita saber para elegir? | Incertidumbres relevantes para la decisión. |
| **4. Preguntas analíticas** | ¿Qué responder con datos? | Preguntas priorizadas y comprobables; población, segmento y periodo delimitados. |
| **5. Definiciones y métricas** | ¿Cómo medir cada concepto? | Fórmulas, grano, población, denominadores, ventanas, interpretación y línea base reproducibles. |
| **6. Datos necesarios** | ¿Qué información hace falta? | Campos, fuentes, claves, relaciones y periodos vinculados a preguntas. |
| **7. Disponibilidad, calidad y modelo** | ¿Qué responden los datos actuales y coinciden con el origen? | Procedencia, extracción, cobertura, unidades, claves y joins revisados; conciliación con origen o falta de acceso explícita; preguntas respondibles, condicionadas o pendientes. |
| **8. Hipótesis y comprobación** | ¿Qué explicaciones contrastar? | Alternativas priorizadas con prueba, evidencia necesaria o limitación explícita. |
| **9. Análisis** | ¿Qué ocurre, dónde, a quién y desde cuándo? | Comparaciones y contrastes reproducibles, conciliados con fuentes y poblaciones/periodos comparables. |
| **10. Diagnóstico** | ¿Qué explica los hallazgos? | Distinguir observación, asociación, explicación sustentada e hipótesis pendiente. Causalidad solo con evidencia suficiente. |
| **11. Acción de negocio** | ¿Qué hacer y cómo comprobar su efecto? | Intervención priorizada, responsable propuesto, condiciones, plazo y seguimiento/experimento ligados al diagnóstico. |
| **12. Solución analítica** | ¿Qué herramienta apoya la decisión y acción? | Modelo, métrica, dashboard, reporte o automatización justificados, con alcance y aceptación. |
| **13. Evaluación y aprendizaje** | ¿Permite decidir y qué debemos ajustar? | Comprobar utilidad/funcionamiento; impacto solo cuando haya ejecución. Si falta, dejar plan de medición. |

## Criterios para preguntar y analizar

- **Comparación antes de interpretación.** Preguntar respecto de qué aumenta, cae o mejora algo. Revisar historia, segmentos y periodos comparables; crecimiento puede ser recuperación. Una cifra agregada no responde automáticamente por cada segmento.
- **Concepto antes de fórmula.** Precisar qué representa cada dato: demanda no equivale a ventas ganadas; un stock no equivale a un flujo. Registrar fórmula, unidad, población, denominador, grano y ventana. Justificar el plazo junto al alcance; una mediana entre ganadores no mide conversión final de toda una cohorte.
- **Origen antes de confianza.** Registrar extracción, filtros y corte; contrastar conteos, totales y registros por ID con el sistema de origen. Un hash prueba integridad del archivo, no veracidad. Sin acceso al origen, declarar la conciliación pendiente y limitar las conclusiones. Controlar también transformaciones, joins, métricas y gráficas.
- **Pregunta → métrica → datos → resultado → interpretación → decisión.** Mostrar cómo cada cálculo responde una parte de la pregunta. Usar tablas, campos y ejemplos concretos cuando hagan comprensible o comprobable el análisis. Automatizar operaciones validadas, manteniendo las conclusiones vinculadas a sus resultados.
- **Evidencia antes de causalidad.** Examinar alternativas; estabilidad de una métrica no demuestra calidad estable. Comparar antes y después no basta para atribuir un efecto. Diferenciar datos observados, simulación, supuestos y propuestas; una idea no equivale a ejecución.
- **Conservar antes de condensar.** No eliminar contenido porque resulte difícil de explicar. Mantener las preguntas del candidato con su redacción registrada; avisar antes de abreviarlas, fusionarlas, reformularlas o cambiar su alcance. Desarrollos de IA separados y atribución explícita de aportes y correcciones.

**No universalizar decisiones de un caso.** El orden de revisión de calidad y etapas del CRO, sus canales o ventanas pertenece a ese caso. SQL directo no garantiza calidad; autoservicio puede contribuir al resultado global fuera de las etapas comerciales. Una lectura de descuentos centrada en expansión se amplió a retención y adquisición: no reducirla a una política exclusiva. MRR/ARR agregados y LTV por cliente responden preguntas diferentes; una prioridad CFO propuesta requiere confirmación.

## Ficha mínima para una solicitud

Completar solo lo necesario; un mismo artefacto puede cubrir varios componentes:

- **Pregunta y decisión:** solicitud literal, decisor, objetivo y criterio de éxito.
- **Alcance:** foco, población, periodo, referencia de comparación, definiciones y límites.
- **Comprobación actual:** pregunta específica, métrica o criterio, datos y evidencia de cierre.
- **Resultado y siguiente paso:** hallazgo, interpretación, alternativas y pendiente que determina qué investigar después.
- **Acción y evaluación:** intervención o herramienta propuesta, responsable, condiciones, plazo y forma de medir utilidad/efecto.

Responder con conclusión sustentada, evidencia, alcance y límites, y acción o siguiente comprobación. Si falta información, precisar qué sí se responde, qué queda condicionado y qué dato cambiaría la decisión. No presentar cobertura parcial como respuesta completa.

**Presentación analítica:** para cada pregunta, usar Markdown normal con **qué medimos, alcance mostrado ahora, métrica/fórmula y datos**. Justificar el plazo junto al alcance y mantener los cálculos plegados. Cada gráfica principal lleva inmediatamente su conclusión y la implicación para el siguiente análisis. En la figura, conservar título, unidades y periodo necesario; explicar supuestos y contexto fuera de ella.

Registrar decisiones con evidencia, supuesto/pendiente, elección y motivo, contribuciones humanas/IA, validación y estado. Organizar las [tareas](../../specs/001-solucion-analitica-finora/tasks.md) por dependencia, plazo y evidencia de cierre. No publicar razonamiento privado ni comentarios personales en la documentación para evaluadores.

## Evidencia y alcance de la síntesis

Extractos literales del candidato conservados como anclas; sus interpretaciones operativas aparecen arriba:

| Evidencia | Expresión registrada | Criterio observable |
| --- | --- | --- |
| E06 | «¿En base a qué estamos diciendo que aumenta? ¿En comparación a qué?» | Exigir una referencia. |
| E11 | «fracción de la pregunta, qué métrica necesitamos para esa fracción de la pregunta y qué data necesitamos para construir esa métrica» | Vincular pregunta, métrica y datos. |
| E13 | «tenemos que verificar la veracidad de la data, la calidad de la data, contra la fuente de origen.» | Conciliar con origen. |
| E18 | «No necesito que modifiques mis preguntas como las hice en un inicio; si las vas a modificar, necesito estar enterado.» | Preservar preguntas y comunicar cambios. |
| E31 | «cada análisis que hagamos, cada métrica que creemos, que mostremos, que evidenciemos, va a ser para responder a esta pregunta.» | Mantener el propósito. |
| E35 | «Ahora lo que necesitamos saber es qué acciones vamos a tomar para contrarrestar esto.» | Pasar de hallazgo a acción. |
| E36 | «Vamos desde lo más general a lo más específico buscando el problema, acotando, acotando, acotando la población de análisis.» | Acotar y profundizar. |

La revisión inicial cubrió 188 archivos y 151 turnos de seis conversaciones accesibles, con 154 mensajes del candidato. Después se incorporaron 13 turnos nuevos y una instrucción aislada, hasta E36. Una séptima conversación no devolvió contenido. Persisten archivos y tramos de conversaciones pendientes; la consolidación no declara revisado ese contenido.

Las 36 evidencias completas, sus fuentes y turnos, inventarios y versiones anteriores se conservan sin pérdida en el [archivo histórico](../proceso/archivo-marco-2026-10-01.zip). Los ejemplos sustentan patrones observables; no convierten cada propuesta de IA en una regla aprobada por el candidato.

## Actualización incremental

Actualizar **cuando el candidato lo solicite**:

1. Leer este marco y el [control de revisión](../proceso/seguimiento-marco/estado.json). Recuperar el último turno efectivamente analizado de cada conversación y los pendientes; una fecha de mantenimiento no sustituye esos cortes.
2. Revisar únicamente turnos nuevos, conversaciones nuevas pertinentes y archivos añadidos, modificados o retirados frente a sus huellas y la base textual. Consultar contenido anterior solo como contexto de un cambio o contradicción. No tratar artefactos regenerados como nueva evidencia del criterio humano.
3. Incorporar solo aportes que añadan, precisen o corrijan una regla. Contrastar con lo ya confirmado, conservar preguntas literales y separar evidencia humana de interpretación/propuesta de IA. Reemplazar duplicación por una formulación clara en este mismo documento.
4. Registrar brevemente qué cambió y por qué; actualizar únicamente los marcadores, huellas y fragmentos realmente revisados. Conservar vacíos, turnos aislados y fuentes inaccesibles como pendientes. No saltar sobre ellos por usar la fecha más reciente.

El control y la base textual comprimida son soporte técnico para comparar cambios, no documentos adicionales de consulta cotidiana. Los archivos históricos quedan fuera de la revisión rutinaria. No hay seguimiento automático ni nuevas revisiones completas implícitas.
