# Bitácora del trabajo con IA

Inicio: 2026-09-29. Actualización: 2026-09-30. Registro de preparación, todavía sin solución implementada.

Lectura principal para evaluadores: [Cómo abordé la prueba](como-aborde-la-prueba.md). Respaldo de interacciones: [Conversación de preparación](conversacion-preparacion.md). Esta bitácora conserva estados históricos; las menciones de aprobaciones pendientes describen su momento, no el estado actual.

1. Codex leyó los dos documentos aportados y revisó la estructura y contenidos de los tres CSV. Se contrastaron requisitos de entrega, preguntas de los dos casos y expectativas de la oferta.
2. El agente interpretó inicialmente “kit SDD” como GitHub Spec Kit e instaló su CLI local. El usuario corrigió esa interpretación: debía usarse el kit personal ya disponible en Proyectos. No se inicializaron plantillas de GitHub Spec Kit.
3. Se leyó el kit personal 0.11.0 y la norma de Proyectos. Se instaló mediante su script, sin modificar el origen, y se copió su protocolo y plantillas al proyecto.
4. La instalación equivocada y el script exploratorio se retiraron del proyecto a `(ruta temporal retirada)`. Antes de localizar la norma del directorio padre, se había escrito ese script de perfil sin constitución aprobada. Se retiró para volver al flujo del kit. Se conserva el resultado inicial en `docs/datos/data_profile.json` como evidencia exploratoria, con SHA-256 de las fuentes, no como pipeline entregable.
5. Se documentaron las limitaciones: no hay eventos de funnel ni descuentos, hay ceros de significado desconocido, los IDs de Industry requieren una correspondencia y S&M no tiene unidad confirmada.
6. Se propuso la constitución y se dejó pendiente de aprobación. No se generó spec ni se eligió stack para la solución.

Validación inicial: conteos completos, campos vacíos, duplicados por clave, periodos, importes negativos/cero y cobertura técnica del join candidato. Los originales no se modificaron. Esto no demuestra causas de pérdida de crecimiento ni separa cambios reales de suscripción y descuentos.

Para el video de proceso deberán agregarse las decisiones posteriores, los cálculos reproducibles, casos de prueba, conciliaciones, revisiones humanas y límites finales. Este registro no es todavía el guion definitivo del video.

## Revisión del objetivo de evaluación

El usuario corrigió el peso del enfoque inicial: además de resolver los casos, la entrega debe demostrar su proceso de análisis, tratamiento de ambigüedad, uso de IA, elección de herramientas, creatividad y comunicación.

Se releyeron los dos documentos íntegros y se consultó la oferta en su página original. El dashboard del reto requiere acceso; se utilizó la copia local de nueve páginas. Se añadió `docs/metodo/enfoque-evaluacion.md`, distinguiendo declaraciones de las fuentes, inferencias y propuestas de demostración. Se actualizaron contexto, README y constitución propuesta. La constitución sigue pendiente de aprobación y no se inició la spec ni código de solución.

Esta corrección es un ejemplo real de revisión del trabajo de IA por el candidato. Su efecto fue cambiar el objetivo del proyecto y los criterios para preparar la entrega, antes de elegir herramientas o implementar.

## Definición del marco de trabajo — 2026-09-30

El candidato distinguió cuatro frentes: organizar el trabajo, resolver los casos, automatizar y presentar. Después propuso un marco analítico de 13 componentes y pidió una evaluación crítica, objetiva y constructiva.

La revisión identificó cinco ajustes: situar la comprobación de hipótesis antes del diagnóstico, explicitar la calidad de datos, distinguir intervención de negocio y solución analítica, establecer criterios de éxito desde el inicio y documentar la ejecución y el uso de IA.

El candidato indicó realizar la modificación. Se guardó el marco ajustado en `docs/metodo/marco-de-trabajo.md`, conservando los 13 componentes y añadiendo resultado esperado y criterio de avance para cada uno. Se incorporó la evaluación del impacto cuando exista ejecución real. No se aprobó la constitución ni se inició implementación.

El candidato estableció el pragmatismo como máxima del proyecto: una solución simple, eficiente y eficaz, sin sobreingeniería y con prioridad al valor aportado dentro del tiempo disponible. Se incorporó a la constitución propuesta y al marco de trabajo, incluyendo profundidad proporcional, documentación breve y automatización acotada. La constitución sigue pendiente de aprobación.

## Conversación paralela sobre automatización — 2026-09-30

El usuario aportó una conversación sobre web pública, backend serverless y agentes. Se incorporó a `docs/metodo/enfoque-evaluacion.md` como propuesta pendiente: Workers + Static Assets, procesamiento temporal de CSV y un agente con herramientas.

Se verificó que Cloudflare recomienda Workers para proyectos nuevos y que permite desplegar código y archivos estáticos conjuntamente. También se comprobó el límite de CPU del plan gratuito: el número bajo de visitas no basta para garantizar costo cero al procesar los datos. Se separaron requisitos del usuario, opción técnica, objetivos de costo y aspectos aún por validar. No se aprobó el stack ni se inició implementación.

## Aprobación de la constitución e inicio de entrevista — 2026-09-30

El usuario aprobó explícitamente la constitución. Se actualizó su estado y los punteros del proyecto conservando los siete principios. Se inició la entrevista de alcance con `spec-generator`, una pregunta por vez y hasta seis, empezando por el plazo efectivo de entrega. Las respuestas se registrarán en `docs/sdd/entrevista-sdd.md`. La aprobación no cierra el stack ni habilita implementación antes de las fases restantes del kit.

Primera respuesta: límite antes del viernes 2026-10-02 a las 12:00 de Colombia, con objetivo de entregar hoy 2026-09-30 o mañana 2026-10-01. El candidato indicó que la rapidez también influye en la oportunidad de continuar el proceso. Se registró ese objetivo para priorizar alcance y tiempo sin excluir los entregables exigidos.

En la segunda pregunta, el candidato cuestionó que elegir otro caso concreto fuera suficiente para definir los criterios de la spec. Se reconoció su utilidad limitada como prueba y se prepararon ejemplos ilustrativos a partir de documentación oficial de Marketing, Growth y Finanzas. La entrevista se reorientó a delimitar comportamientos: estructurar preguntas abiertas, pedir evidencia, ejecutar operaciones soportadas y explicar análisis fuera de alcance. La propuesta permanece pendiente de confirmación.

El candidato confirmó ese alcance con «adelante». Se registró la segunda respuesta como cerrada y se continuó con el presupuesto de la demo, pendiente de definir. El stack y la contratación de servicios siguen sin aprobarse.

## Presupuesto y fuentes de IA — 2026-09-30

El candidato fijó un presupuesto total de $0, eligió Cloudflare gratuito e indicó que ya dispone de credenciales de Google AI Studio y del proveedor mencionado como Grok. Por el modelo descrito, se interpreta provisionalmente Groq con gpt-oss-120b. Se contrastó la disponibilidad de planes gratuitos con documentación oficial; las cuotas y el nivel de las cuentas se verificarán al integrar. Se cerró la tercera respuesta de la entrevista y se planteó la continuidad del trabajo como siguiente requisito. No se solicitaron secretos ni se inició implementación.

## Continuidad del trabajo — 2026-09-30

El candidato aceptó una sesión temporal con resumen descargable. Los casos preparados seguirán accesibles en la web; recuperar archivos o conversaciones otro día queda fuera del alcance inicial. Se cerró la cuarta respuesta de la entrevista y se planteó el comportamiento ante indisponibilidad de la IA.

## Disponibilidad de la entrega — 2026-09-30

El candidato aceptó que los casos preparados permanezcan disponibles cuando falle la IA o se agote su cuota gratuita. La exploración informará del fallo y conservará el trabajo de la sesión para reintentar o descargar resultados ya obtenidos. Se cerró la quinta respuesta y se planteó la última pregunta sobre los formatos de datos admitidos en la primera entrega.

## Cierre de entrevista y spec propuesta — 2026-09-30

El candidato indicó mantener CSV si Excel añadía complejidad innecesaria. Se justificó que hojas, fórmulas y tipos de celda amplían el alcance sin aportar una necesidad del reto y se cerró la sexta pregunta con CSV como único formato inicial. Se generó la spec 001 en EARS y su revisión, separando histórico observado, modelo propuesto y ejemplos ilustrativos. La spec queda pendiente de aprobación; no se escribió código de aplicación ni se ejecutaron pruebas de una solución todavía inexistente.

## Aprobación y plan — 2026-09-30

El candidato aprobó explícitamente la spec 001. Se preparó un plan con cálculo exploratorio en el navegador, Worker acotado para IA y casos disponibles sin LLM; se eligieron dependencias mínimas y tareas de 15–25 minutos. Se verificaron runtimes, tamaños, hashes y representación exacta en centavos COP del histórico. La revisión plan-evaluator cubre los 22 RF y deja reservas sobre cuotas reales, rendimiento y videos. No se instaló software, no se escribió aplicación ni se consumieron credenciales.

## Organización y control de versiones — 2026-09-30

El candidato pidió control de versiones y organización antes de desarrollar código. Git 2.55.0 ya estaba disponible; se inicializó un repositorio local en `main` y se guardó el estado previo mediante un primer commit. Se movieron CSV a `inputs/`, documentos extraídos a `docs/fuentes/` y documentación a subcarpetas de método, datos, proceso y SDD. Se actualizaron referencias y rutas del perfil sin cambiar su evidencia ni sus hashes. Las cinco fuentes conservan sus bytes, incluidos BOM y finales de línea; se configuró `.gitattributes` para evitar conversiones de Git. Un segundo commit registra la reorganización. No se creó remoto ni se publicó información.

Verificación: 36 enlaces Markdown locales válidos; hashes de las cinco fuentes idénticos antes y después del movimiento y CSV comprobados contra el perfil. Índice completo actualizado a las nuevas rutas. No se ejecutaron pruebas de una aplicación todavía inexistente.

## Documentación para evaluadores — 2026-09-30

El candidato pidió registrar todo el proceso desde su primera interacción, incluidos preguntas, definición de cuatro etapas y construcción del marco. Aclaró que la audiencia principal son personas evaluadoras. Se recuperaron todas las páginas disponibles del historial de este chat: 30 turnos, 31 mensajes del candidato y 62 mensajes públicos de la IA al corte, desde el 2026-09-29. Se generó un relato legible y un anexo de conversación, sin comandos, respuestas de herramientas ni razonamiento privado. La conversación paralela aportada se copió como fuente histórica, sin convertir sus recomendaciones iniciales en decisiones actuales.

Se documentaron también la petición de una explicación humana de la spec, la distinción entre perfil exploratorio y análisis final, la separación entre casos preparados y agente reutilizable, y el cierre de preparación. La fase 1 está definida; ninguna de las 34 tareas de ejecución se marca como terminada por este registro. La próxima etapa es resolver los casos, con preparación técnica y definición de datos al inicio.

En adelante cada decisión, corrección o resultado relevante se registrará con pregunta, intervención del candidato, contribución de IA, decisión y motivo, evidencia de validación y estado. La síntesis para evaluadores y el video deben mostrar hechos reales, no solo comandos o requisitos.

## Inicio de resolución y lectura del CRO — 2026-09-30

El candidato indicó conservar el requerimiento original en la web y desarrollar los 13 componentes paso a paso; aceptó esa disposición. Se precisó RF-02 y el plan para reflejarla, sin añadir pantallas obligatorias ni ampliar las operaciones del agente.

Después leyó el caso completo, cuestionó expresiones ambiguas y propuso conversiones por etapa: comparadores, alcance, demanda, calidad, atención, post-SQL, entradas directas y duración. Codex organizó esa aportación en `docs/casos/cro.md` y propuso distinguir objetivo, necesidad y decisión, incorporar rutas y resultado global, separar pendientes de pérdidas y comparar cohortes con seguimiento equivalente. No se simularon respuestas de un CRO como evidencia.

La decisión y las métricas son propuestas para revisar, no decisiones confirmadas por el usuario ni hallazgos. Los datos CRM necesarios no están en los CSV. Se conserva la conversación pública en `conversacion-resolucion.md`; el último turno se capturó en curso. No se modificaron fuentes, no se ejecutaron análisis nuevos ni se cerraron tareas de implementación.

## Revisión concisa y avance del marco — 2026-09-30

Por petición del candidato, un subagente abrevió CRO, marco, enfoque y relato; Codex revisó los cambios. Se conservaron fuentes, conversaciones literales y documentos formales. El candidato precisó que una caída requiere histórico comparable y que debemos comprobar si la calidad se define y mide. Se actualizó el punto 3 y se organizaron sus preguntas en el punto 4. A continuación pidió estructurar el punto 5: se añadieron fórmulas, ventanas, denominadores, segmentación y límites; sigue como borrador para revisión. Referencia oficial consultada: analítica de ventas de HubSpot, enlazada en CRO; aporta criterios de medición, no evidencia del caso.

El candidato pidió aclarar el tratamiento de rutas y recordó que ya había cuestionado la equivalencia entre crecimiento de New y Won. Se corrigió esa atribución y se incorporó su pregunta sobre el desfase entre entrada y cierre: seguir las mismas entidades a lo largo del tiempo, con pendientes y rutas explícitos. No hay eventos disponibles para calcularlo todavía.

El candidato aceptó la selección de métricas, incluida la pregunta New → Won. Se registró la aprobación manteniendo pendientes sus parámetros y se añadió el inventario inicial de datos requeridos/disponibles (6–7). Se discutió Jupyter; Codex propuso Python con informe HTML por simplicidad. No se instaló Jupyter ni se ejecutó todavía el pipeline.

## Evidencia ejecutable solicitada — 2026-09-30

El candidato cuestionó que no pudiera ver cómo se obtuvo el inventario ni comprobar errores de IA. Se añadió T00 como inspección técnica previa, sin cerrar contratos o tareas del pipeline. Codex creó y ejecutó un script visible, un informe HTML/JSON y registro con comando, fecha, versiones y hashes. Se reprodujeron 22 controles del perfil anterior y pasaron tres pruebas de lectura; fuentes intactas. Informe abierto y presentación revisada por Codex. La revisión del candidato sigue pendiente: no se afirma supervisión retrospectiva ni ausencia absoluta de alucinaciones. Evidencia: [inspección](../datos/inspeccion.md).

El candidato formuló una comprobación prioritaria: cómo se compara New con Won, distinguiendo proporción convertida, duración y cierres de entradas anteriores acumuladas. Se corrigieron preguntas que ya suponían una caída; se añadieron cohortes, ventanas comparables y origen temporal de los cierres. Las ventanas 30/60/90 son ilustrativas, no plazos acordados. Falta CRM para contrastar estas explicaciones.

El candidato pidió auditar el cumplimiento del plan porque no entendía las tareas. Se añadió una lectura humana con estados reales: T00 ejecutada, formulación CRO en curso y tareas restantes sin cierre. Se corrigió el encabezado obsoleto y se señalaron dependencias demasiado rígidas para revisión; no se rediseñó el alcance ni se dieron por aprobados nuevos órdenes. Las estimaciones no son tiempos validados.

El candidato inició la revisión conceptual del resumen: cuestionó significado de IDs, utilidad para CRO y categorías de S&M; pidió conservar ideas sin ejecutarlas. Codex contrastó el enunciado: ambas tablas se refieren a clientes, no a IDs de industria; pagos no prueban Won/entrada/salida, y las categorías de gasto no prueban atribución. Se guardaron preguntas para después. No se registró verificación humana de filas/controles ni se ejecutaron transformaciones.

El candidato corrigió la pregunta de Marketing: comprobar aumento de demanda no necesita primer pago. Después pidió planificar datos sintéticos coherentes y aleatoriedad controlada para distintos diagnósticos. Se propusieron cuatro tablas y tres escenarios (referencia, caída de conversión y demora), con semilla reproducible y corte temporal. Plan de demostración, no generación ejecutada ni evidencia histórica; ampliación e integración web pendientes de decisión.

El candidato exigió verificar datos contra el sistema de origen. Se hizo explícito en el componente 7, RF-03, plan y T03: procedencia/extracción, mismo alcance y corte, conciliación y tratamiento de discrepancias. No hay acceso al sistema original; verificación pendiente. Integridad de archivo y consistencia con origen no garantizan veracidad absoluta. Para sintéticos, referencia es generador/configuración; no se validan como datos reales. Solo cambios documentales.

El candidato pidió desglosar cada afirmación en preguntas, métricas, datos y tablas; señaló confusión con «ruta/recorrido» y repetición de la etiqueta sintética. Se reorganizó el plan con cuatro tablas nombradas por su contenido y conexiones por ID, explicitando una cuenta/una oportunidad como límite de la primera demo. Las métricas tienen campos trazables; generación todavía pendiente. Se distinguió demostrar la solución con un escenario creado de probar una causa histórica sin CRM real.

El candidato corrigió el enfoque: analizar etapas, no historias individuales. Codex distinguió unidad de presentación (etapa/periodo/segmento) y registros de soporte (IDs/eventos). Se priorizó conversión por transición, manteniendo New–Won como contexto, y se vinculó atención con visitas de etapa. Solo revisión documental del modelo; datos y generador siguen pendientes.

El candidato solicitó investigar si el modelo propuesto corresponde a fuentes reales de CRM. Codex consultó documentación oficial de Salesforce y HubSpot: exportaciones, historial de oportunidades/propiedades, actividades, pagos y puntuación de calidad. Se documentaron equivalencias y límites en `docs/casos/cro-datos-sinteticos.md`: tablas analíticas derivadas, IDs de objetos separados, historial limitado y campos configurados. No se accedió a un CRM ni se confirmó disponibilidad en Finora; no se generaron datos.

## Primera construcción de datos CRO — 2026-09-30

El candidato autorizó conservar como pendiente la distinción Won/pago y avanzar. Codex lo conservó como pendiente, usó Won para cierres comerciales y construyó `analisis.html` sobre resultados SQL existentes: conversión a 30 días y mediana de salidas por etapa, periodos comparables y selector de tres escenarios. No generó pagos ni eliminó métricas propuestas. Verificó las nueve pruebas, lectura visual y cambio a escenario demora. La revisión del candidato sigue pendiente; se completa solo el bloque técnico T09a, no el caso entero.

Actualización posterior: el candidato detectó que no veía Proposal → Won y pidió identificar ganados/nuevos clientes. La transición y los eventos ya existían; el HTML solo mostraba cinco filas del catálogo. Codex corrigió la vista a siete filas y creó `vw_ganados`/`ganados.csv` desde los datos existentes, con primera entrada, fecha Won y tiempo hasta cierre; agregó conteos por mes de cierre y conversión Proposal → Won. Aclaró que primer Won observado no acredita primer pago ni adquisición real sin historia suficiente. Quince CSV, tres SQLite, nueve pruebas en verde; notebook ampliado a nueve celdas. No se declara todo el caso completo.

El candidato cuestionó campos de calidad y métricas de atención, solicitando explicación. Codex interpretó inicialmente esas dudas como eliminación de métricas; el candidato corrigió esa interpretación. Se registró que siguen propuestas, pendientes de definición. Antes de la interrupción se habían creado generador, esquema SQL, métricas y cuatro pruebas, con datos solo en memoria; no CSV persistidos. El candidato pidió precisar ese estado y después autorizó explícitamente construir CSV, tablas y datos.

Codex corrigió el guardado (dependencia de plantilla HTML inexistente y cierre de conexiones SQLite), añadió una prueba de exportación y ejecutó la generación: tres escenarios con 1.800 cuentas y siete etapas cada uno, 12 CSV y tres bases SQLite. Preparó vista HTML con tablas/columnas y notebook ejecutado desde kernel nuevo, siete celdas sin errores. La restricción inicial de puertos locales de Jupyter se resolvió mediante ejecución autorizada fuera del sandbox. Ocho pruebas pasan; archivos/tablas concilian y hashes de los tres originales siguen iguales. Abrió el modelo/tablas en el panel y comprobó visualmente su lectura. Evidencia: `docs/datos/modelo-cro-demo.md` y `artifacts/cro_demo/validacion.json`. Revisión humana y gráficos pendientes; no se declara el caso ni la web terminados.

## Organización accesible de datos y resultados — 2026-09-30

El candidato cuestionó que los CSV y SQLite estuvieran en `artifacts`, porque esa ubicación no era intuitiva, y aprobó reorganizarlos. Codex trasladó CSV a `datos/sinteticos/cro/`, bases a `datos/bases/cro/` y salidas a `resultados/cro/`; actualizó generador, notebook, enlaces y documentación. Se conservaron los bytes de los 15 CSV y los tres originales. Nueve pruebas pasan y el notebook se ejecutó desde un kernel nuevo sin errores. La vista de tablas se abrió en su nueva dirección local; se verificaron enlaces CSV/SQLite/métricas. Evidencia: `resultados/cro/migracion.json`. Las gráficas existentes siguen pendientes de rediseño según la valoración del candidato; no se crearon nuevas gráficas.

## Auditoría de cobertura CRO — 2026-09-30

El candidato recordó las cuatro tablas acordadas y pidió comprobar cobertura de todas las preguntas, datos y métricas. Codex contrastó formulación, propuesta, generador y SQL: la demo actual es parcial. Registró once preguntas y sus faltantes en `docs/datos/cobertura-cro.md`, incluyendo calidad, atención, pagos, self-serve, cohortes, segmentos y reglas de historia previa. Distinguió cuatro tablas de negocio del catálogo auxiliar y de ganados derivados. No se generaron nuevas tablas ni se declaró completado el caso.

## Preparación completa de datos CRO — 2026-09-30

El candidato autorizó completar la información para iniciar el análisis y reservó la definición de gráficas para trabajar una por una con él. Codex amplió la spec/tarea T09b, implementó cuatro tablas de negocio y catálogo, interacciones y pagos, criterios sintéticos de calidad/atención, compras desde producto, saltos y visitas adicionales. Calculó doce familias para cubrir las once preguntas, con segmentos, ventanas y denominadores. No generó ni actualizó gráficas. Regeneró tres escenarios: 57 CSV y tres SQLite. Trece pruebas pasan, incluidas tasas de fixtures independientes y exclusión de pagos inválidos/previos/repetidos; valores CSV/SQLite y segmentos concilian. Hashes originales intactos. Revisión humana, interpretación y gráficas pendientes; no se afirma resolución real del caso ni cierre de la web. Evidencia: `docs/datos/modelo-cro-demo.md`, `docs/datos/cobertura-cro.md`, `resultados/cro/validacion.json` y notebook ejecutado.

## Corrección de la lectura del notebook — 2026-09-30

El candidato solicitó explicar las tablas, corregir textos obsoletos y unificar el recorrido de lectura del notebook y HTML. Codex reconoció el error de presentación y reorganizó el notebook como recorrido principal: explicación y muestra breve de cada tabla, catálogo auxiliar, controles y solo la primera pregunta sobre crecimiento de New. Las demás métricas permanecen guardadas, sin desplegarse en bloque. No cambió datos/cálculos ni creó gráficas; revisión humana pendiente.

El candidato precisó que la primera pregunta debe mostrar la evolución de New mes a mes y pidió una lectura breve. Se simplificó el bloque del notebook a objetivo, fórmula y datos, con encabezados humanos: Mes, Entradas a New y Variación mensual (%). Sin cambiar cálculos ni generar gráficas.

## Primera gráfica acordada — 2026-09-30

El candidato propuso una tendencia temporal de New y aprobó una línea de cantidades con variación mensual al pasar el cursor. Codex instaló pandas/Plotly en el entorno y registró versiones; creó `scripts/cro_charts.py` para leer las métricas SQL sin recalcularlas y reutilizar la figura en notebook y HTML. Ocho meses comprobados contra el CSV; cursor en mayo muestra 179 entradas y +34,6%. Notebook ejecutado sin errores, archivos de datos/métricas conservan hashes. Revisión visual técnica realizada; evaluación de la gráfica con el candidato pendiente. No se crearon otras gráficas.

## Recuperación de contexto e inicio CFO — 2026-09-30

- **Solicitud humana:** iniciar caso dos con el método del caso uno y recuperar contexto/conversación del proyecto.
- **Trabajo de Codex:** lectura del historial accesible de «Preparar contexto del proyecto», constitución, fuentes, marco, spec, plan/tareas/revisión y documentación CRO; comprobación del notebook, manifiesto y estado Git. Reindexación MCP sin cambiar fuentes.
- **Estado contrastado:** cuatro tablas CRO más catálogo, tres escenarios, métricas calculadas y primera gráfica New; diagnóstico CRO pendiente. Modelo CFO diseñado en el plan, todavía sin implementación. Hay cambios previos sin commit: se conservaron.
- **Validación de esta sesión:** `.venv/bin/python -m unittest discover -s tests`: 13 pruebas OK. Hashes de los 57 CSV del manifiesto CRO y tres fuentes coinciden. Notebook guardado: diez celdas de código, sin salidas de error; no se reejecutó ni se efectuó una nueva revisión visual de la figura.
- **Resultado:** `docs/casos/cfo.md` conserva el caso original, establece CFO como decisor y deja decisión/éxito y componentes restantes pendientes de desarrollo con el candidato. Mapa y relato actualizados. No se atribuye al candidato una decisión de negocio aún no formulada.

El candidato revisó la primera gráfica en VS Code y señaló que el eje Y no mostraba una marca superior a los valores de mayo–agosto. Se fijó la escala desde cero hasta el siguiente múltiplo de 50 que cubre el máximo (200 en referencia), con marcas explícitas. Se actualizó el notebook sin cambiar datos ni abrir otra vista HTML.

El candidato pidió disponer de las once preguntas en el notebook para planear las siguientes gráficas. Se añadieron bloques de qué se mide, métricas y datos, conservando el cálculo/gráfica de New y sin desplegar nuevas tablas ni crear otras gráficas.

## Exploración y plan de la web de resultados — 2026-09-30

- **Solicitud humana:** recuperar contexto y conversaciones, explorar lo existente y preparar un plan detallado de la web para mostrar el avance disponible.
- **Trabajo de Codex:** lectura de constitución, fuentes/contexto, marco, entrevista, spec, plan/tareas/revisión, documentos de proceso y artefactos CRO. Recuperación de turnos accesibles de «Preparar contexto del proyecto», «Propuesta de alojamiento web» y «Marco de análisis completo»; lectura del estado de «Preparar el segundo caso», sin mensajería. «Registros de etapas» no devolvió turnos. Grafo reindexado; función `grafica_new` inspeccionada. Consulta de documentación oficial Cloudflare/Vite/Plotly.
- **Comprobaciones ejecutadas:** `.venv/bin/python -m unittest discover -s tests`: 13 OK; 57 CSV CRO coinciden con hashes del manifiesto; tres fuentes CSV coinciden con perfil. Serie total New enero–agosto comprobada; HTML de figura 4.825.011 bytes. Frontend/manifiesto npm/configuración hosting inexistentes. No se reejecutó notebook ni se hizo nueva validación visual.
- **Resultado:** `plan-web.md`, con cuatro destinos, 13 componentes por caso, avance/pending, tareas W01–W12, contratos, controles y continuidad del alcance final. Propuesta técnica de reutilizar Plotly y adelantar shell respecto a T13, pendiente de formalizar antes de código. Mapas y punteros actualizados.
- **Autoría/estado:** el candidato fijó la prioridad de mostrar lo existente; Codex elaboró inventario y propuesta de ejecución. No se atribuye aprobación humana al diseño detallado, ni implementación, integración IA o publicación. Se conservaron cambios previos de otros chats y fuentes originales.

El candidato revisó la estructura del notebook: las preguntas pertenecen al mismo bloque de análisis. Se corrigió la numeración a 3.1–3.11 dentro de «Preguntas y análisis»; se mantuvo la evidencia de validación con su resultado plegado, sin cambiar ni repetir cálculos.

Se corrigió el formato de salida de la primera gráfica: Plotly nativo para notebook, en lugar de HTML con JavaScript incrustado. Ocho puntos y escala 0–200 verificados en la salida guardada; ejecución sin errores. Datos y cálculos sin cambios.

El candidato solicitó un criterio de diseño que evitara espacio vacío y concentraciones de la línea en la parte superior. Se consultó la guía de gráficas de líneas de Datawrapper (https://www.datawrapper.de/academy/what-to-consider-when-creating-line-charts). Se ajustó el eje al rango observado más margen, indicando el intervalo visible; se añadieron etiquetas de valores y se redujo la altura. No cambian cifras ni métricas. Revisión del candidato pendiente.

## Segunda gráfica CRO — 2026-09-30

El candidato planteó medir el tiempo New → Won antes de comparar crecimiento y aceptó comparar las mismas entradas con igual seguimiento. Autorizó la gráfica. Codex reutilizó `cohortes.csv`: mediana de tiempo de ganados al corte y conversión a 60 días en dos paneles. Excluyó meses parcialmente maduros (agosto en referencia); enero–julio y siete tasas comprobadas contra numeradores/denominadores. La mediana no describe a quienes nunca ganaron ni garantiza cierres en un mes fijo. No se recalcularon ni modificaron métricas fuente. Revisión humana pendiente.

## Lectura automatizable de New — 2026-09-30

El candidato identificó el salto abril–mayo y el comportamiento posterior y propuso cerrar cada pregunta con una conclusión reutilizable. Codex registró su aportación, precisó +34,6% y creó un resumen generado desde las métricas: mayor variación mensual positiva y rango posterior. La conclusión de referencia muestra 133 → 179 y rango mayo–agosto 173–183. Sin atribución causal ni llamada LLM; reglas visibles en `scripts/cro_insights.py`, lectura en notebook y evidencia en `resultados/cro/conclusion_new.json`.

El candidato señaló que las abreviaciones de IA omitieron el periodo de comparación y los segmentos de sus preguntas. Se restituyó en cobertura y notebook la redacción registrada en `docs/casos/cro.md`, distinguiéndola de una transcripción literal. Se separó el desarrollo acordado de New → Won de la pregunta de referencia. La lectura de New se identifica como parcial: agregado mensual, pendiente análisis segmentado. Se fijó aviso previo a cambios de preguntas; datos y cálculos sin modificaciones.

El candidato revisó la jerarquía visual de la conclusión y pidió explicar la importación del script. Se priorizó el texto generado mediante un bloque de mayor tamaño, se retiró la nota introductoria y se plegó el código conservándolo disponible. La función importada genera texto desde métricas; no carga una conclusión fija. Se mejoró la redacción sin alterar cifras ni reglas.

El candidato pidió retirar texto accesorio de la primera gráfica. Se eliminaron la anotación de origen/escenario/rango y el espacio que ocupaba; se conservó el año 2026 en el eje temporal. Valores, escala y métricas sin cambios.

## Segmentación de New por canal — 2026-09-30

El candidato autorizó segmentar después de acordar conservar el total y empezar por canal. Codex añadió líneas por canal y conclusión automática al bloque 3.1, reutilizando demanda SQL. Comprobó conciliación de los ocho meses y del aumento abril–mayo: Marketing pago +5, Orgánico +29 y Referidos +12; total +46. Orgánico aporta 63,0% del incremento neto. No se modificó la pregunta original ni la gráfica 3.2; otras dimensiones pendientes por relevancia. Revisión humana pendiente.


### Contextualizar las conclusiones por canal — 2026-09-30

- **Contribución del candidato:** identificó que el salto de Orgánico desde abril ocultaba la caída desde febrero; pidió evitar conclusiones simplistas.
- **Corrección de IA:** conservar la contribución al salto como dato puntual y contextualizar cada canal con máximo anterior, caída previa y todos los meses posteriores. Figuras y preguntas sin cambios.
- **Evidencia:** Orgánico 52 en febrero → 34 en abril → 63 en mayo: −34,6%, luego +85,3%; mayo supera febrero un 21,2%. Junio baja a 51. Referidos permanece por encima de su máximo previo desde mayo; Marketing pago termina agosto en 50, por debajo del máximo anterior de 54. No inferir causas ni crecimiento sostenido.
- **Validación:** tres pruebas independientes para recuperación seguida de retroceso, ausencia de un mes/canal y conciliación completa; ejecución del notebook para actualizar las conclusiones visibles.


### Comparación New → Won a 30 días — 2026-09-30

- **Decisión del candidato:** seguir las entradas de cada mes a New y contar cuántas alcanzan Won en 30 días; simplificar la figura anterior.
- **Implementación:** una sola gráfica mensual de porcentaje, con entradas y ganados al pasar el cursor. Plazo desde la entrada individual; denominador de todas las entradas del mes cuando tienen seguimiento completo. Se conserva tiempo típico entre ganados como métrica independiente. Llegar después del plazo no implica pérdida.
- **Validación:** recomputar independientemente desde las primeras fechas de New y Won en registros de etapas; concilian entradas y ganados de los ocho meses con SQL. Verificar una sola serie, ocho puntos y ausencia de anotaciones accesorias; ejecutar notebook.


### Fundamento del plazo de conversión — 2026-09-30

- El candidato pidió justificar los 30 días con la mediana y eliminar texto accesorio.
- Cálculo: mediana de la diferencia entre primera entrada y primer Won para las 432 cuentas ganadas que entraron por New en referencia: 30 días. Se calcula de las fechas en el notebook, con código disponible y oculto inicialmente.
- Presentación: dos líneas, fundamento del plazo y definición de conversión; sin ejemplo. La ventana permanece fija al comparar escenarios.


### Estándar consistente entre preguntas — 2026-09-30

- El candidato definió el bloque 3.1 como referencia para la presentación de las demás preguntas.
- Ajuste de 3.2: qué medimos, alcance con mediana de 30 días, fórmula y datos en una celda Markdown, igual que 3.1. Se conserva el cálculo de mediana plegado y se verifica que coincide con el plazo justificado. Sin cambios en gráfica o métricas.
- Regla registrada en AGENTS.md para mantener este formato en próximas preguntas.


### Extensión del estándar a 3.3–3.11 — 2026-09-30

- Autorización del candidato: aplicar el mismo formato a todas las preguntas siguientes.
- Nueve bloques ajustados: qué medimos, alcance, fórmula y datos. Se conservaron literalmente las preguntas y las salidas de las gráficas anteriores.
- Fórmulas contrastadas con SQL: población con seguimiento completo, denominadores de calidad/atención, distinción entre cierres y pagos, permanencia de abiertos y brecha ilustrativa de avances. Se explicitan análisis y decisiones de alcance todavía pendientes. No se generaron gráficas ni se cambiaron cálculos.


### Conversión por canal en toda la serie — 2026-09-30

- El candidato pidió priorizar el desglose por canal y no restringir el análisis a abril–mayo.
- En 3.2 se muestra primero la conversión New → Won a 30 días por canal, enero–agosto; se conserva la figura global después. Colores consistentes con New; entradas y ganados disponibles al pasar el cursor.
- Precisión validada: abril–mayo, New 133→179, ganados dentro de 30 días 29→31 y conversión 21,8%→17,3%. Bajó el porcentaje, no la cantidad de ganados. Los cierres por mes calendario también pasaron de 62 a 63.
- Validación independiente: primeras fechas de New y Won por cuenta; concilian los 24 grupos mes/canal, porcentajes y sumas contra total. Figura con tres series de ocho meses, sin anotaciones accesorias. No se atribuyen causas con este desglose.


### Orden visual aclarado — 2026-09-30

- El candidato aclaró: primero gráfica global, después desglose por canal. Mantener enero–agosto completo.
- Se intercambiaron las celdas conservando sus salidas, cálculos y gráficas.


### Lectura conjunta de la conversión — 2026-09-30

- El candidato identificó descensos en Marketing pago y Orgánico y solicitó la interpretación de la gráfica.
- Se añadió lectura reproducible de enero–agosto, global y por canal: máximos, caídas posteriores y recuperaciones, conservando cifras/poblaciones para revisión. No se infieren causas ni deterioro continuo.
- Verificación: cuatro series de ocho meses; Marketing alcanza 34,0% en marzo, 13,3% en julio y 24,0% en agosto. Orgánico 27,5% en enero, 9,5% en mayo, 22,4% en julio y 16,1% en agosto. Notebook ejecutado sin errores.
- Siguiente análisis: transiciones por canal y distinción entre menor conversión final y mayor demora.


### Desarrollo de todas las gráficas CRO

- **Autorización del candidato:** desarrollar todas las gráficas de las preguntas restantes y preparar una revisión posterior, siguiendo el formato aprobado.
- **Trabajo de IA:** nueve bloques 3.3–3.11, 32 figuras nuevas, 36 guardadas en total; lecturas iniciales generadas desde métricas. Preguntas originales conservadas. Global antes de segmentos, colores coherentes, figuras separadas por unidad y selectores de etapa. Sin crear otra web ni modificar fuentes.
- **Criterios:** ventana inicial de 30 días para comparar transiciones; 60/90 en maduración. Criterios de calidad v1 y atención a 2 días ilustrativos. Ratios de grupos desde cantidades; no promediar medianas ni porcentajes. No sumar brechas entre etapas ni llamar impacto en pagadores a avances estimados.
- **Validación:** 23 pruebas; ejecución del notebook sin errores; generación de las nueve preguntas en referencia, conversión y demora. Verificación completa de ratios, conciliación total/canales y hashes de las tres fuentes originales; evidencia en `resultados/cro/validacion_graficas.json`. Proyecto reindexado.
- **Límite de verificación:** comprobación estructural de figuras y selectores realizada; inspección visual en VS Code pendiente de permisos de pantalla. Revisión humana, causalidad y decisiones de negocio pendientes. No se declara cerrada la resolución CRO.

## Comparación de lecturas CFO — 2026-10-01

Solicitud del candidato: comparar el adjunto de primera lectura con la segunda lectura del mensaje actual y sintetizar. Codex leyó ambos, distinguió coincidencias/omisiones/novedades y cambios de hipótesis; conservó las referencias y separó ocho preguntas propuestas. Revisó documentación oficial de ChartMogul sobre movimientos MRR y descuentos: el fin puede clasificarse como Expansion del neto; nuestro análisis requiere separar su causa de expansión subyacente. Señaló que Marketing como responsable y descuentos solo para ampliación no son hechos del reto; antes/después no prueba impacto incremental. Resultado en `docs/casos/cfo-comparacion-lecturas.md`; sin cálculos, gráficos ni implementación.

## Objetivo comercial de descuentos — 2026-10-01

Aporte humano: tres objetivos posibles de descuentos y solicitud de evaluación sin alternativas forzadas. IA: separó ampliación, retención, adquisición y reactivación opcional; distinguió cambio neto por vencimiento de crecimiento subyacente. Registro en comparación de lecturas CFO; sin cálculos ni cambios de implementación.

## Alcance de descuentos — 2026-10-01

El candidato preguntó «si los descuentos únicamente son para clientes antiguos, existentes o para clientes nuevos», a partir de los ejemplos del CFO. Codex distinguió ejemplos sobre clientes existentes de una política exclusiva: el enunciado no confirma esa restricción. Elegibilidad pendiente, vinculada al objetivo comercial; sin implementación.

## Prioridad propuesta de efectividad — 2026-10-01

Aporte humano: pregunta prioritaria sobre aumento de facturación/MRR por descuentos; variables monto, porcentaje y tiempo y comparación antes/después. IA: conservó redacción original; propuso distinguir facturación/MRR, incluir periodo durante promoción y comparación sin descuento para efecto incremental. Señaló criterio de éxito distinto para retención. Registro documental; sin cambio de spec ni implementación.

## Aproximación mediante tendencias y retención — 2026-10-01

El candidato propuso permanencia media, churn y MRR promedio y tendencias antes/después del descuento, con ejemplos hipotéticos de tres a seis meses y de 30 a 40. Codex reconoció la hipótesis de compensación por permanencia/base activa; precisó seguimiento comparable, clientes aún activos, total frente a promedio y separación de adquisición. Propuso ingreso neto acumulado en horizonte común y mantuvo límites de datos/causalidad. Ejemplos sin calcular, no hallazgos ni supuestos numéricos aprobados.

## Ajuste por crecimiento previo — 2026-10-01

El candidato propuso descontar una tendencia media de crecimiento (5% como ejemplo) para observar un cambio ajustado y preguntó si sería sobreingeniería. Codex lo evaluó como línea base sencilla y condicionada: observado menos esperado, continuidad de tendencia explícita, horizonte/población comparables; diferencia de tasas en puntos porcentuales y sin atribución causal automática. Sin cálculos ni cambio de implementación.

## Síntesis breve CFO — 2026-10-01

Solicitud humana: condensación clara, pragmática y completa de lo discutido. IA: revisó caso/registro y creó `docs/casos/cfo-sintesis.md`; enlazó documento en caso/mapa. Conserva pregunta original y propuestas separadas; incluye intención/elegibilidad, separación suscripción/precio/descuento/pago, métricas, comparación/tendencia, límites y datos faltantes. Sin implementación, gráficos ni resultados calculados.

## Coherencia documental CFO/CRO — 2026-10-01

El candidato solicitó limpiar documentos CFO y mantener el marco común con CRO. Codex consolidó `docs/casos/cfo.md` en requerimiento original y 13 componentes; conservó literalmente el requerimiento, las preguntas del candidato incluidas y las ocho preguntas propuestas de IA. Trasladó `docs/casos/cfo-comparacion-lecturas.md` a `docs/proceso/cfo-comparacion-lecturas.md` y archivó la síntesis anterior en `docs/proceso/archivo-cfo/cfo-sintesis-2026-10-01.md`. Las rutas antiguas citadas en registros anteriores son históricas. Actualizó mapa/enlaces; propuestas no se convierten en aprobaciones ni resultados. Sin cambios de código/datos.

## Objetivo empresarial y MRR — 2026-10-01

El candidato preguntó «¿Por qué es importante el ingreso mensual recurrente?» y «¿Cuál es el objetivo de la empresa?», vinculando más servicios/clientes con costos, utilidad, efectivo y mercados. Codex evaluó esta aclaración como pertinente en componentes 2–3, sin ampliar a estudio integral; consultó definición oficial Stripe sobre MRR y su diferencia de caja. Registró objetivo empresarial pendiente y preguntas originales separadas de propuestas. Sin análisis financiero ni objetivos de Finora confirmados.

## Exploración de métricas SaaS — 2026-10-01

El candidato propuso explorar ARR, LTV y otras métricas y cuestionó la prioridad del MRR. Codex consultó Stripe/ChartMogul y registró opciones en componente 5, vinculadas a decisión/datos; distinguió anualización de ingreso anual realizado y estimaciones LTV de resultados observados. NRR/GRR, CAC/recuperación y margen son candidatos; no nuevos requisitos aprobados ni cálculos ejecutados.

## Perspectiva CFO y condensación — 2026-10-01

El candidato planteó vender más a largo plazo, relaciones MRR/ARR/LTV y crecimiento de mercado con precios menores, y pidió condensar. Codex separó objetivo literal del CFO de intención inferida; volumen, ingreso, utilidad y caja; crecimiento agregado de valor por cliente. Registró síntesis en proceso y una precisión breve en componente 3; sin política confirmada ni cálculos.

## Delimitación del caso CFO — 2026-10-01

El candidato aceptó la pregunta condensada, priorizó aumento/cambio de MRR y efecto de decisiones comerciales y pidió reconocer objetivos estratégicos como posibles aclaraciones sin desarrollarlos en este alcance. Codex ajustó componentes 2–3 y marcó métricas complementarias fuera del desarrollo actual; distingue descuento aplicado de pérdida incremental. Conserva preguntas previas y requisitos del reto, sin implementación.

## Corrección de alcance de métricas CFO — 2026-10-01

El candidato corrigió la exclusión excesiva de métricas complementarias: MRR/ARR, LTV y las demás métricas vinculadas deben crearse/evaluarse para responder al caso. Objetivos estratégicos alternativos (priorizar mercado aunque caiga ingreso) quedan como hipótesis de contexto. Codex reconoció la interpretación errónea y corrigió componente 3/5/6, spec, plan y tareas T11a/T12a; mantiene límites de fuentes y simulación. Sin cálculos ejecutados ni cambio en preguntas originales.

## Inventario completo de preguntas CFO — 2026-10-01

Solicitud del candidato: comprobar todas las preguntas del adjunto/sesión en sección 4 y proponer selección/fusión/eliminación. Cotejo de primera lectura y 15 mensajes recuperados hasta esta solicitud: 53 formulaciones interrogativas distintas, incluyendo variantes, y 16 planteamientos técnicos literales. Excluidos únicamente muletillas y coordinación documental. Codex reconoce inventario previo incompleto, conserva referencias y ocho propuestas de IA, añade mapeo P1–P8 con cobertura total y recomendaciones sin borrar preguntas. Verificación de literalidad contra fuentes, conteos, asignación de cada ID y 13 componentes. Desarrollo/gráficas pendientes; fusiones aún propuestas para revisión.

Cierre del cotejo: 53 formulaciones humanas, 18 planteamientos técnicos (incluida cuota recaudada y restricción propuesta a ampliaciones), 27 variantes explícitas en respuestas públicas de IA, ocho propuestas documentales anteriores y preguntas literales del enunciado. Las cantidades cuentan formulaciones, no análisis independientes. Inventario y mapeo comprobados; no se borraron preguntas.

## Lectura breve de preguntas CFO — 2026-10-01

El candidato pidió simplificar nuevamente por exceso de texto. Codex redujo sección 4 a cuatro bloques y trasladó inventario íntegro a `docs/proceso/cfo-inventario-preguntas.md`, preservando preguntas y referencias. Propuesta: desarrollar modelo, cambio MRR y resultado de descuentos; contexto estratégico como aclaración. Sin eliminar preguntas ni métricas.

## Preguntas CFO con formato CRO — 2026-10-01

El candidato rechazó la reducción a cuatro bloques y pidió revisar CRO. Codex leyó sección 4 CRO (tabla pregunta/evidencia) y bloques 3.1–3.11 del notebook (qué medimos, alcance, fórmula y datos). Corrigió CFO a tabla de 14 preguntas concretas/evidencia; formulaciones de referencia separadas de propuestas de desarrollo, inventario completo conservado. Recomendación de selección/fusión pendiente de revisión; sin borrar preguntas ni métricas ni generar notebook/cálculos.

## Revisión de la base frontend delegada — 2026-10-01

- **Aporte externo comunicado por el candidato:** base web en worktree `prueba_tecnica_BI`, rama `codex/frontend-finora`, commit `1362549`; sin integración ni publicación.
- **Revisión de Codex:** comprobación de worktrees, entrega/contratos, contenido JSON y código mediante grafo MCP reindexado. Figura pública idéntica en bytes al archivo actual de origen; contenido src/public sincronizado. Las 11 preguntas CRO y 14 CFO se encuentran literalmente en documentos/notebook actuales; las propuestas CFO tienen origen diferenciado.
- **Validación ejecutada aquí:** `npm test` en el worktree frontend: 18 pruebas OK. No se reejecutó build ni se hizo revisión visual. Pruebas estáticas no acreditan navegación real, móvil ni accesibilidad completa.
- **Hallazgos:** `renderCaso` solo inserta figura con id `new-serie`; `figuraNew` fija rutas/columnas. Exportador fija ocho meses/valores y recalcula variación en vez de leer la métrica guardada; la etiqueta de población introduce seguimiento de 30 días en un conteo de entradas. `npm run build` no sincroniza contenido por sí mismo: requiere exportación previa para evitar publicar copias antiguas.
- **Recomendación:** encargar al agente frontend renderer declarativo mínimo para figuras/tablas, exportación configurable con controles y lectura de variación existente, etiquetas fieles y sincronización de contenido en el flujo de build. Después revisión real en navegador. Sin modificar código externo, fusionar ni publicar.

## Revisión del patrón de razonamiento — 2026-10-01

- **Solicitud humana:** recuperar la forma de razonar y preguntar a partir de todas las conversaciones y todos los archivos del directorio, para reutilizarla ante solicitudes de otros decisores.
- **Trabajo de Codex en esta sesión:** inventario y lectura/inspección de 188 archivos, recuperación paginada de 151 turnos de seis chats con contenido y lectura de respuestas públicas; un séptimo chat relacionado no devolvió mensajes. Se incorporó el turno frontend aparecido durante la revisión, atribuyendo su reporte y validaciones a aquella sesión.
- **Síntesis:** `docs/metodo/patron-de-razonamiento.md` e `instrucciones-para-aplicar-el-marco.md`; evidencia en `docs/proceso/evidencias-patron-razonamiento.md` y cobertura Markdown/JSON. Se mantienen los 13 componentes y las preguntas originales. Las reglas derivadas se identifican como interpretación/propuesta de IA.
- **Validación:** treinta extractos cotejados literalmente con mensajes del candidato; lectura/parseo del inventario sin errores; tres bases abiertas en solo lectura con integridad `ok`; comprobación de enlaces nuevos e integridad de fuentes. No se reejecutaron suite analítica, frontend ni despliegue.
- **Límites:** historial limitado a lo recuperable, exclusión de entornos/cachés y metadatos internos Git, sin inferencia psicológica ni razonamiento privado. Artefactos de IA no prueban autoría o supervisión humana. El marco documental permite estructurar preguntas nuevas; su ejecución general mediante un agente no se ha probado.

## Comprobación de los cinco ajustes frontend — 2026-10-01

- **Entrega externa comunicada:** commit `1b63c4f` en `codex/frontend-finora`, sin fusión ni publicación.
- **Revisión de Codex:** contrato/renderFigura genéricos, lectura de crecimiento_new_pct desde CSV, población sin ventana de conversión y predev/prebuild con sincronización de contenido comprobados en archivos.
- **Validación repetida:** `npm test`: 22 OK; `npm run check:coherence`: OK. No se repitió build ni prueba de navegador en esta sesión.
- **Evidencia externa:** `docs/web/ajustes-02.md` registra Chrome headless, cuatro rutas/recarga, móvil 390 px, teclado y ausencia de errores de consola/red; describe limitaciones y capturas temporales. Esa validación se atribuye al agente frontend.
- **Estado:** base técnica disponible para revisión humana de presentación y contenido. Incorporación final de análisis y assets pendiente; una figura nueva requiere preparar su archivo público y referencia en contenido. No se modificó código, fusionó ni publicó.

## Corrección de primera pregunta CFO — 2026-10-01

El candidato corrigió expresamente la primera pregunta: retirar facturación y centrarse en ingreso mensual recurrente. Pregunta vigente: «¿aplicar descuentos aumenta el ingreso mensual recurrente?». Codex actualizó pregunta y evidencia de la primera fila en sección 4. Redacción previa conservada únicamente como referencia histórica; sin cálculos ni modificación de otras preguntas.

## Preparación del seguimiento incremental — 2026-10-01

Solicitud humana: actualizar los documentos del patrón con novedades futuras cuando el candidato lo pida, sin repetir la revisión completa. Codex añadió protocolo en `docs/proceso/actualizacion-incremental-marco.md`, estado persistente por fuente y base textual para comparar versiones. Registró la regla en AGENTS.md y enlazó los documentos del marco. La captura de referencias es mantenimiento documental, no otra revisión sustantiva ni seguimiento automático; conserva pendientes y el corte de los chats ya analizados.

## Punto 4 CFO reorganizado por última lectura — 2026-10-01

El candidato autorizó sintetizar y ordenar siguiendo el enunciado, solicitando opinión crítica constructiva. Codex agrupó la sección 4 en cinco preguntas con acciones/evidencia; preservó referencias en el inventario y registró la lectura en [comparación CFO](cfo-comparacion-lecturas.md). Integró métricas complementarias, seguimiento antes/durante/después y tendencia. Precisó expansión subyacente frente a neta con fuentes oficiales; diferenció descuento aplicado, ingreso incremental y utilidad. Formulación preparada para avanzar, sin cálculos CFO ni modificación de fuentes originales.

## Oportunidad de profundización: descuentos y costos — 2026-10-01

El candidato planteó como hipótesis que menores costos y gastos podrían permitir descuentos, con efectos en MRR, retención y captación de mercado, sin necesariamente deteriorar los márgenes de utilidad. Solicitó únicamente agregar una apreciación concisa fuera del análisis actual, sin modificar lo acordado. Codex añadió la nota en componente 3 de CFO; precisó que preservar margen no garantiza preservar utilidad total. Sin ampliar preguntas, métricas, implementación ni alcance.

## Limpieza de anotaciones editoriales CFO — 2026-10-01

El candidato pidió eliminar aclaraciones sobre orden de lectura y proceso de edición por aportar volumen sin valor analítico. Codex retiró esas anotaciones del documento CFO, conservando preguntas, acciones, métricas, límites y la oportunidad de profundización. Trazabilidad mantenida en los registros de proceso.

## Definiciones investigadas de expansión — 2026-10-01

El candidato pidió sustituir «Definir expansión y separar servicio/uso, precio y descuento» por definiciones completas y reglas aplicables. Codex consultó documentación oficial de ChartMogul y Stripe: expansión de MRR es monetaria y puede incluir el vencimiento de descuentos; no demuestra por sí sola más servicios. Sustituyó la tarea pendiente en pregunta 2 por la clasificación de los importes y consolidó componente 5 con reglas de expansión/contracción subyacente, pricing, descuento, fecha efectiva y estados. Conservó la convención de descomposición ya registrada en el plan (cantidad a precio anterior, luego precio a cantidad actual) y la conciliación neta. Distinguió definición publicada de convención analítica local; causas desconocidas no se infieren del pago. Sin cálculos ni implementación CFO.

Fuentes verificadas: [movimientos ChartMogul](https://help.chartmogul.com/article/163-understanding-mrr-movements), [analítica Stripe](https://docs.stripe.com/billing/subscriptions/analytics).

## Precisión del procedimiento en pregunta 3 CFO — 2026-10-01

El candidato pidió aclarar «Aplicar la metodología siguiente». Codex sustituyó la referencia vaga en pregunta 3 por el procedimiento: cohortes por inicio del descuento, separación de existentes/nuevos/reactivados, comparación mensual antes/durante/después con seguimiento equivalente, descomposición de causas y contraste con tendencia/grupo similar sin descuento. Pregunta y métricas conservadas; sin fijar un plazo no acordado ni ejecutar análisis.

## Eliminación del bloque metodológico duplicado CFO — 2026-10-01

El candidato manifestó que los cuatro puntos metodológicos separados confundían su uso. Codex explicó su función y retiró el bloque duplicado de sección 4. Procedimiento conservado en pregunta 3, evaluación acumulada en pregunta 4, intención/elegibilidad en componente 3, definiciones de métricas en 5 y límites de atribución en 8. Precisó en pregunta 3 que el horizonte cubra vigencia y seguimiento posterior. Sin eliminar preguntas ni métricas ni ejecutar cálculos.

## Reubicación de metodología y procedimiento CFO — 2026-10-01

El candidato corrigió la eliminación del bloque: conservar contenido útil y ubicar metodología antes del procedimiento. Codex trasladó y consolidó metodología/procedimiento en componente 9, Análisis; mantuvo sección 4 centrada en preguntas y evidencia, sin cambiar las preguntas. Recuperó intención/responsable, cohortes/seguimiento, métricas/conciliación, tendencia/atribución, evaluación acumulada y límites de datos. No ejecutó cálculos.

## Definición de expansión integrada en respuesta 2 — 2026-10-01

El candidato pidió condensar la definición e incorporarla directamente a la respuesta del ejemplo 100→130 con descuento 30, sin fuentes visibles en ese bloque. Codex integró definición y respuesta en fila 2 y retiró el párrafo aislado: neto sin cambio durante ampliación compensada por descuento; aumento neto al vencer, causado por descuento; subyacente/precio separados. Pregunta conservada. Fuentes oficiales previamente verificadas permanecen en este respaldo: https://help.chartmogul.com/article/163-understanding-mrr-movements y https://docs.stripe.com/billing/subscriptions/analytics. Sin nueva investigación ni cálculos.


### Explicar el origen del modelo sintético — 2026-10-01

- El candidato pidió iniciar el notebook con la carencia de datos del funnel, la necesidad de generar datos sintéticos, las tablas a crear y sus datos.
- Se reorganizaron únicamente la introducción y el resumen inicial de tablas. Se enumeran las cuatro tablas de negocio y el catálogo; se distingue Ganados como resultado derivado.
- Verificación: todas las celdas de código y sus salidas permanecen idénticas. Sin regenerar datos, métricas ni gráficas.

## Implementación analítica CFO autorizada — 2026-10-01

El candidato solicitó preparar datos, métricas y presentación siguiendo el caso CRO; pidió primero propuesta y detener creación hasta su autorización. Tras revisar la propuesta de tres escenarios y ventana seis meses previos/tres de descuento/seis posteriores, autorizó: «Bien, comencemos con la implementación y la creación de los datos, de las métricas, de todo, gráficas, todo».

Codex actualizó spec/plan/tareas antes de implementar. Creó `scripts/cfo_model.py`, puente SQL, pruebas independientes, `scripts/cfo_present.py`, `scripts/validate_cfo.py` y notebook `03_modelo_cfo.ipynb`. CSV y SQLite por escenario y grupo pareado; componentes/precios/descuentos/estados separados del pago. Reutilizó entorno y presentación CRO: qué medimos, alcance, fórmula/datos y cálculos plegados. Implementó MRR bruto/neto/descuentos, crecimiento, ARR/ARPU, retención/churn, NRR/GRR, LTV estacionario, permanencia observada y acumulados. Costos/CAC/margen no inventados.

Las pruebas iniciales detectaron que bajas de clientes elegibles impedían el equilibrio esperado del escenario compensado. Se corrigió la simulación para aislar ampliación/descuento; bajas y adquisición iguales entre grupos. No se atribuye mejora de retención a esa política. Julio 2025–marzo 2026: positivo +9.000 UM, negativo −3.000 UM, compensado 0 UM frente a referencias sin descuento; son resultados simulados, no efectos reales ni utilidad.

Validación: 11 pruebas CFO pasan y suite completa de 34 pruebas pasa. La versión final del notebook ejecutó todas sus celdas desde kernel nuevo; Jupyter requirió ejecución autorizada fuera del sandbox para abrir sus puertos locales. Tres bases concilian sin residuo y validan relaciones; 66 CSV con hashes y 27 figuras HTML generadas. Fuentes `inputs/` intactas respecto de hashes previos. Ver `resultados/cfo/validacion.json` y `docs/datos/modelo-cfo-demo.md`. Revisión visual del navegador local no realizada por restricción de acceso a archivos; revisión humana de figuras y conclusiones pendiente. No se publica web ni se autoriza política comercial ni se declara la prueba completa entregada.


### Reorganización orientada a la pregunta principal — 2026-10-01

- **Contribución del candidato:** definir el hilo New → conversión → canal → calidad → etapas → causas → acciones; pidió reorganizar sin eliminar nada.
- **Trabajo de IA:** pregunta principal explícita al inicio de análisis, seis preguntas en recorrido principal, síntesis de hallazgos/acciones y cinco preguntas complementarias. Enunciados originales y 36 figuras conservados; se avisó del cambio de numeración. Acciones condicionadas con responsables propuestos y seguimiento, sin atribuir implementación.
- **Precisiones:** entrar a SQL no demuestra calidad; Producto queda fuera de New → Won pero disponible para crecimiento total. Algunas métricas de calidad/etapas mezclan tipos de entrada; filtrado New/canal y comparación antes/después pendientes. Menor conversión a 30 días puede reflejar demora.
- **Validación:** comparación exacta del conjunto de celdas de código y salidas antes/después; comparación exacta de los once enunciados. No se recalcularon ni alteraron métricas.
# Formalización del marco reutilizable — 2026-10-01

**Continuación enfocada desde 3.5:** el candidato autorizó completar los análisis posteriores con la población priorizada. IA creó `scripts/cro_focused_diagnosis.py` y CSV de atención/etapas de focos New; reescribió 3.5–3.7 y acciones. En referencia solo Demo y Proposal, abril–agosto; contraste 30/60/90 solo abril–junio con cuentas y meses comparables. Atención usa visitas; duración separa terminados de abiertos. Cada figura tiene conclusión inmediata. La versión anterior completa quedó en `notebooks/archivo/02_modelo_cro_respaldo.ipynb`, conservando preguntas y complementos; 3.1–3.4 permanecieron idénticos. Verificó tres escenarios y 14 pruebas de alcance, conciliación y gráficas. Ejecutó celdas nuevas con Python y guardó sus salidas; kernel completo y revisión visual humana pendientes. Hallazgos y acciones descriptivos/condicionados; no causalidad ni impacto ejecutado.

**Síntesis de focos:** el candidato pidió omitir de la conclusión las etapas no priorizadas. IA dejó únicamente Demo → Proposal y Proposal → Won, con sus cifras, y señaló que las demás etapas quedan fuera del siguiente análisis. No afirmó ausencia de variaciones ni eliminó sus datos.

**Conclusión y acotación por etapa:** el candidato pidió conclusión inmediata tras cada gráfica, abril como referencia y canal únicamente en las etapas de interés. IA filtró el SQL de etapas a cuentas con entrada New, mantuvo el mismo cálculo y priorizó las dos mayores caídas globales de abril a mayo: Demo → Proposal (86,4% → 77,1%) y Proposal → Won (94,4% → 81,4%). New → Working (95,5% → 93,3%) baja de prioridad; no descarta calidad. Creó `scripts/cro_stage_focus.py`, `etapas_new.csv` por escenario y actualizó 3.4: global/conclusión y una figura por foco con su conclusión. Conservó la vista completa anterior como respaldo. Conciliación de numeradores/denominadores por canal y periodos en tres escenarios; celdas nuevas ejecutadas con Python y salidas guardadas. Plazo por transición y causas siguen pendientes; filtro de atención a estos focos se realizará al revisar ese bloque.

**Corrección de visualización de etapas:** el candidato aclaró que quiere una gráfica con todas las transiciones como líneas etiquetadas, no paneles. IA sustituyó los paneles por un único plano global de seis líneas y conservó el desglose en otra figura con etiquetas de transición/canal. Color por transición y trazo por canal. Salidas verificadas en tres escenarios; siete pruebas correctas. Métricas conservadas.

**Etapas simultáneas:** el candidato pidió comparar todas las transiciones de un vistazo. IA sustituyó el selector de 3.4 por seis paneles globales y seis por canal, con escala común y denominadores en la información de cada punto. Conservó métricas, series y plazo. Comprobó las vistas en los tres escenarios y actualizó las salidas del notebook; las siete pruebas de análisis pasaron. Revisión visual humana pendiente.

**Inicio del análisis por etapas:** el candidato pidió introducir explícitamente la revisión de etapas en 3.4. IA añadió una frase que vincula la caída global con localizar la transición afectada, globalmente y por canal. Cambio de presentación; cálculos y gráficas conservados.

**Contexto de calidad:** el candidato propuso describir brevemente la estabilidad de las puntuaciones. IA incorporó el rango observado de medias mensuales (46,5–53,4) en la conclusión, sin deducir ausencia de tendencia del origen aleatorio. Cálculo desde datos; gráficas y puntuaciones conservadas.

**Puntuación de leads:** el candidato decidió comprobar primero si existe medición; si falta, avanzar y proponer implementarla. Autorizó puntuaciones aleatorias para el ejercicio sin desarrollar criterios. IA creó `scripts/cro_quality.py`, CSV `puntuaciones_leads.csv` y medias mensuales globales/por canal en los tres escenarios. Conservó cuentas originales, calificación booleana y sus gráficas como respaldo; 3.3 analiza exclusivamente New y distingue puntuación de probabilidad. Generación reproducible independiente de Won; el resultado simulado no identifica causas reales. Salidas de las celdas nuevas calculadas con Python; ejecución completa en kernel y revisión humana pendientes.

**Lectura de conversión y siguiente análisis:** el candidato propuso conservar todos los canales para revisar etapas y pidió una conclusión breve que explique esa decisión. IA comprobó abril/mayo: global 21,8% → 17,3%; Marketing pago 24,1% → 15,3%; Orgánico 20,6% → 9,5%; Referidos 20,0% → 28,1%. Precisó que hay variaciones posteriores, no caída continua; el global posterior sigue por debajo de abril. Condensó la salida del notebook desde las métricas y conservó la lectura detallada como respaldo.

**Medición de duración visible:** el candidato pidió evidenciar periodo, fuente y cálculo del fundamento de 30 días. IA incorporó antes de la conversión una pregunta específica, alcance enero–agosto de 2026 de entrada New, cierres observados hasta septiembre, cálculo desde fechas, tabla mensual y gráfica de medianas. La mediana general usa 432 ganados y no incluye pendientes ni constituye una referencia exclusiva anterior al aumento. Ejecutó los cálculos con Python y guardó la tabla y figura Plotly en el notebook, conservando las salidas de conversión. El kernel Jupyter no pudo iniciarse por restricción de puertos; ejecución completa desde kernel pendiente.

**Síntesis con valor por canal:** el candidato pidió conservar la interpretación y cifras útiles al condensar. IA añadió los crecimientos de abril a mayo (+85,3% Orgánico, +9,3% Marketing pago, +26,7% Referidos), vinculó ese aumento compartido con conservar todos los canales y distinguió captación de conversión. Actualizó conclusión y salida del notebook; tres pruebas existentes correctas.

**Claridad de 3.2:** el candidato propuso «¿Cómo entendemos la relación entre New y Won?» y pidió explicitar el fundamento del plazo. IA verificó una mediana de 30 días en las 432 cuentas de entrada New que llegaron a Won y reorganizó la explicación: duración observada primero, conversión a ese plazo después. Conservó cálculos, gráficas y pregunta original de referencia.

**Síntesis posterior de New por canal:** el candidato priorizó comprobar si todos los canales aumentaron y avanzar a conversión. IA condensó la conclusión visible y conservó el análisis histórico como respaldo; actualizó la salida correspondiente del notebook y verificó los tres controles existentes de contexto/conciliación. No cambió métricas ni gráficas.

El candidato pidió formalizar su estructura para otros trabajos y preguntas. Aporte humano: centrar cada análisis en una pregunta principal, acotar según hallazgos, conservar complementos y terminar en acciones. IA: organizó el recorrido en enfocar, comprobar, localizar, explicar, actuar y evaluar; conservó los 13 componentes y añadió una ficha de aplicación. Evidencias E31–E35 y cobertura incremental registradas. Verificación documental de extractos y enlaces; sin cambiar datos, cálculos ni gráficas. Aplicación general aún no probada mediante un agente.

## Aplicación del marco de razonamiento al análisis CFO — 2026-10-01

El candidato solicitó aplicar al análisis construido el recorrido formalizado: enfocar, comprobar, localizar, explicar, actuar y evaluar; cada hallazgo determina el siguiente análisis y cada análisis aporta a la pregunta principal. Codex leyó el patrón y ficha de aplicación; no modificó el marco ni avanzó sus marcadores de revisión.

Actualizó spec/plan/tareas y reorganizó notebook CFO: pregunta/decisión al inicio, resultado frente a referencia, focos por elegibilidad y fase, explicación de bruto/descuento y movimientos, acciones condicionadas y evaluación. Conservó las cinco preguntas de referencia y los 13 componentes. Retención/LTV y otros indicadores permanecen en respaldo plegado, disponibles según evidencia. No sustituyó preguntas ni eliminó métricas o figuras.

Añadió vistas derivadas `focos.csv` y `recorrido.json` y lectura automática por resultado: aumentar, reducir o equilibrar ingreso. Comprobó que el resto aporta cero y que la reducción/recuperación del compensado se cancelan (−3.000 y +3.000 UM). Verificó actividad igual por cliente; estabilidad agregada no se usa como descarte universal de causas. La acción y evaluación registran responsables propuestos, control mensual y cierre después de vigencia/seguimiento; no atribuyen piloto ni impacto real ejecutados.

Validaciones: 38 pruebas de proyecto pasan (15 CFO), incluidas conciliación de focos, compensación temporal, acciones distintas y no inventar foco si no hay diferencia. Ejecución desde kernel nuevo detectó una variable de ruta usada antes de su definición por el traslado de celdas; se corrigió su inicialización y el notebook completo pasó. Comparación SHA-256 confirma fuentes, bases, indicadores y 27 figuras previas intactos. Se actualizaron conclusiones y vistas de recorrido; revisión humana pendiente. Evidencia en `resultados/cfo/validacion.json`.

## Método del agente y alternativa estática — 2026-10-01

- **Decisión humana:** intentar una entrega con agente guiado por su método analítico; si fallos/esfuerzo comprometen entrega, aceptar web de escenarios/resultados preparados sin exploración asistida. Método actualizable; componente mencionado como «Jeff» solicitado.
- **Trabajo de Codex:** revisión del marco, patrón observado, instrucciones de aplicación, evidencias y protocolo incremental. Preparó `specs/001-solucion-analitica-finora/plan-agente.md` con política versionada, estado conversacional, resultados deterministas y evaluación mediante casos. Actualizó spec/plan para distinguir variante con agente y estática; no declaró RF omitidos cumplidos.
- **Límites:** síntesis observada incluye interpretaciones de IA, no pensamiento exacto del candidato. Fidelidad del agente todavía no probada. «Jeff» no identificado en documentos consultados; aclaración solicitada y pendiente. Sin llamadas a proveedores, código, despacho de agente externo ni cambios a marcadores/patrón metodológico.
- **Validación:** revisión documental y enlaces locales del plan; sin pruebas de agente implementado.

## Dos modos compartidos y revisión de Jev — 2026-10-01

- **Decisión humana:** pestañas de análisis preparado y análisis con agente, reutilizando la misma base; conservar entrega preparada independiente. Aclaración de «jev» con enlaces TypeSafe e introducción.
- **Revisión de Codex:** documentación oficial de introducción, primitivas, confianza, quickstart, modelos, estado, uso en agentes y limitaciones. Choice/Score/Noul confirmados; Noul es probabilidad 0–1, no null. Jev no conversa ni calcula métricas con precisión garantizada.
- **Resultado:** spec/plan-agente actualizados con dos modos, datos/componentes compartidos, carga diferida y aislamiento de fallos; Jev como servicio acotado de decisión, política versionada y validación determinista. Propuesta de siguiente paso vía Choice; otras primitivas condicionadas a utilidad/pruebas.
- **Costo/estado:** tarifas públicas USD 0,042 por millón de tokens de entrada; no se confirmó crédito gratuito de cuenta. Presupuesto $0 conservado, sin API ni instalación, implementación, publicación o nuevo agente despachado. Fidelidad y mejora frente a LLM/reglas pendientes de comprobar.

## Regla esencial de acotación — 2026-10-01

El candidato reiteró que el análisis debe ir de lo general a lo específico y limitar la investigación posterior a la etapa/población donde se localiza el problema. IA registró la regla en el marco de trabajo, patrón e instrucciones reutilizables, con foco y evidencia por tarea. E36 conserva el aporte literal. Actualización documental; filtros del notebook aún no modificados.

## Revisión pragmática del prefiltro Jev — 2026-10-01

- **Solicitud humana:** evaluar críticamente Jev como prefiltro de cada intervención LLM, elegir solo un uso con utilidad concreta y posponer experimentación; prioridad calidad y menor tiempo de entrega.
- **Revisión de Codex:** documentación oficial de intent-routing, confidence-routing, Choice, guardrails, límites del modelo y tarifas; contraste con catálogo/método/contrato del proyecto. La clasificación previa es técnicamente adecuada, pero no demuestra mejora analítica ni ahorro si todas las rutas llaman al mismo LLM.
- **Recomendación registrada en plan-agente:** priorizar asistente básico; Jev opcional limitado a Choice de intención para ruta preparada/nueva/corrección/no determinable. Reglas verifican datos/operaciones; LLM desarrolla preguntas abiertas. Scoring y evaluación de cada intervención pospuestos. Fallback a conversación básica ante ambigüedad/error, sin gate global que bloquee análisis válidos.
- **Condiciones:** acceso compatible con $0, evaluación breve en español y rutas efectivas frente al baseline, respeto del presupuesto de llamadas; límite propuesto de 45 minutos adicionales después del básico, sin garantía de completarlo. Sin pruebas de rendimiento/beneficio ejecutadas, implementación ni llamadas API.

### 2026-10-01 — Paquete de planificación del asistente

A solicitud del candidato, IA produjo anexo operativo de spec, clarificaciones, plan técnico, 33 tareas con dependencias y criterios de cierre, revisión documental y encargo para agente externo. Fuentes: constitución/spec activa, método documentado, decisiones de conversación y plan del agente. Separó entrega preparada, conversación parcial, catálogo completo y Jev opcional. Definió contratos, límites, costo $0, aislamiento de worktree y pruebas propuestas. No implementó código, no conectó proveedores ni autorizó ejecución; revisión/aprobación humana pendiente. La verificación realizada es documental, no pruebas de funcionalidades propuestas.


### 2026-10-01 — Un único marco de consulta

- **Decisión humana:** sintetizar los archivos del método, con pragmatismo y complejidad solo cuando sea necesaria.
- **Trabajo IA:** consolidación en `docs/metodo/marco-de-trabajo.md`; actualización de referencias; versiones anteriores en un único archivo ZIP, con manifiesto de integridad. Control incremental trasladado a `docs/proceso/seguimiento-marco/estado.json`.
- **Validación:** respaldo comparado byte a byte y 13 componentes conservados literalmente; cortes de conversaciones y pendientes preservados. Revisión limitada a documentos del método y referencias afectadas, sin ejecución de aplicación.

## Base web funcional Finora (W01–W10) — 2026-10-01

Encargo del coordinador: construir la primera estructura funcional de la web (Resumen, Caso CRO, Caso CFO, Explorar) en rama `codex/frontend-finora` y worktree propio, sin interferir con el análisis activo del checkout original. Contribución de IA: contraste del plan-web con el estado actual (ajustes en `docs/web/ajustes-w01.md`), contrato de contenido (`docs/web/contrato-contenido.md`), frontend Vite vanilla (HTML/CSS/JS, sin frameworks), plantilla común de casos, exportación seleccionada (`scripts/export_web.py`) y validación (18 pruebas `node --test`, gate `check:coherence`, `vite build`, dev y preview comprobados). Contenido provisional exclusivamente de documentos existentes: 11 preguntas CRO literales del notebook con estándar 3.1, 14 preguntas CFO de `docs/casos/cfo.md` con origen marcado, primera figura reutilizada en bytes más tabla accesible. Decisión técnica: aplazar Papa Parse/Chart.js/Plotly npm (innecesarios para casos preparados) y `worker/`/Wrangler (W11–W12 fuera del encargo). Validación: serie New verificada (127, 124, 132, 133, 179, 183, 182, 173; mayo +34,6 %), ningún pendiente etiquetado como disponible, paquete público sin secretos. Limitaciones: revisión visual en navegador y revisión humana del contenido pendientes; sin fusión ni publicación (decisión del dueño).

## Ajustes a la base web (5 puntos) — 2026-10-01

Encargo del coordinador en el mismo worktree (`codex/frontend-finora`), sin fusionar ni publicar; conservar alcance, preguntas y resultados analíticos. Contribución de IA: (1) renderizador genérico `renderFigura` por contrato (`datos_src`/`iframe_src`/`tabla.columnas`), sin ids/rutas fijos; (2) exportación sin valores fijados que lee `crecimiento_new_pct` del CSV y valida estructura, con manifest por `n_meses`/`meses`/hashes; (3) población de la serie New corregida a «cuentas que entraron por New, por mes de entrada»; (4) `scripts/sync-content.mjs` con `predev`/`prebuild` para que el build incorpore el contenido actualizado; (5) revisión real en Chrome headless sobre `preview :4179` (4 rutas + recarga, figura/tabla/details, móvil 390 sin desborde, teclado con skip link, sin errores de consola/red; favicon inline y `overflow-wrap` añadidos). Validación: `export_web` (8 meses derivados), `npm test` 22/22, `check:coherence` OK, `vite build` OK. Detalle en `docs/web/ajustes-02.md`. Preguntas CRO/CFO literales intactas; figuras 3.2–3.11, modelo CFO y publicación siguen fuera del encargo.

## Presentación CRO con notebook terminado (PC07–PC15) — 2026-10-02

Encargo del candidato: actualizar la presentación web con el notebook CRO terminado, en el worktree `codex/presentacion-cro`, sin fusionar ni publicar. Contribución de IA: (1) documentación actualizada antes de implementar — storyboard rev. 2 (C01–C07, 12 figuras), plan rev. 2, tareas rev. 2 (PC01–PC06 hechas, PC07–PC15 redefinidas) y spec P02/P06 al tramo terminado, con reestructuración avisada (3.5–3.7 extensos sustituidos por 3.5 capacidad/demora, 3.6 síntesis y 4 acción); preguntas literales intactas; (2) snapshot `22ffec72…` (55 celdas) con hashes y verificación figura↔CSV↔conclusión sin diferencias (New 133/179; 21,1→6,7%; focos 76,2→61,8 y 58,3→19,0; carga 7,9→12,3/9,1→9,6; demora 3,0→4,0/2,0→4,0); cero mutaciones del notebook; (3) historia C01–C05 + cierre con 7 figuras primarias, tablas de valores plegadas, síntesis calculada y tabla de acciones con responsable Sales propuesto y evaluación octubre–noviembre 2026; limpieza visible (sin notas internas ni prefijos duplicados); índice con anclas por ruta `#/cro/C01` y router que conserva CRO al pulsar, recargar y abrir directo; apertura con pregunta y propósito primero y requerimiento plegado. Validación: exportador offline, `pnpm test` 28/28, `check:coherence` OK, `vite build` OK, revisión en Chrome headless (escritorio y 390px, recarga byte-idéntica en ancla, sin desbordes, iframes lazy, cero IA). Entrega en `docs/web/cro-entrega.md` con capturas. Revisión humana de selección/densidad pendiente; sin merge/push/publicación.

## Presentación CFO estática (CF01–CF08) — 2026-10-02

Encargo del candidato: presentar el caso CFO en la web existente, con anexo de planificación, en el worktree `codex/presentacion-cro`, sin fusionar ni publicar. Contribución de IA: (1) paquete `presentacion-cfo/` con spec (F01–F08), storyboard (S01–S09), plan y tareas, reutilizando contrato `recorrido`, renderizadores, router con anclas y pruebas de CRO sin duplicarlos; (2) snapshot `d3154b8b…` (39 celdas, 2 Plotly) con verificación figura↔CSV↔conclusión sin diferencias (bruto−descuento=neto, trazas idénticas, cierre +500, acumulado −1.500, fases −4.500/+3.000, sensibilidad verificada); cero mutaciones; (3) exportador por copia exacta con Plotly local (funciona sin red) y manifiesto; historia S01–S09 + cierre con preguntas literales, tablas plegadas/abiertas, visión ampliada y respaldo intacto; índice `#/cfo/<seccion>` con recarga verificada byte-idéntica. Validación: `pnpm test` 33/33, `check:coherence` OK (una corrección de término sin contexto de límite), `vite build` OK, revisión en Chrome headless (escritorio y 390px, sin desbordes, iframes lazy, cero IA). Entrega en `docs/web/cfo-entrega.md` con capturas. Revisión humana de densidad y conexiones pendiente; sin merge/push/publicación ni impacto comercial atribuido.

## Introducción «cómo se construyó» CRO+CFO (IN01–IN08) — 2026-10-02

Encargo del candidato: intro pregunta→datos→faltantes→sintéticos→análisis en ambos casos, con adaptación visual ligera de una imagen de referencia que no llegó adjunta (se usó solo su descripción textual). Contribución de IA: (1) anexo `presentacion-intro/` con spec (I01–I07), plan y tareas; (2) sincronización CFO `d3154b8b…`→`b0a1d75c…` vía exportador existente (título S05 nuevo, cifras/trazas idénticas verificadas, cero mutaciones); CRO sin cambios; (3) bloque `construccion` en ambos contenidos con pregunta literal sin duplicar, 3 originales recibidos sin descarga, 6 faltantes y tablas sintéticas desde fuentes (CFO enlaza S02/S03); (4) 8 CSV pequeños copiados con bytes intactos + `archivos-manifiesto.json`; (5) render común, widget de adjuntos con estado por caso en sesión (sin contenido, sin red, sin ejecución) y CSS acotado azul/turquesa. Validación: `pnpm test` 45/45, coherence y build OK; navegador automatizado TODO-NAVEGADOR-OK (multiselección/retiro/limpieza/reselección, separación por caso, descarga real, 390px sin desborde, cero errores); descargas comprobadas desde el build. Entrega en `docs/web/intro-entrega.md` con capturas. Revisión humana de densidad y diseño pendiente; cuatro ajustes CRO reservados excluidos; sin merge/push/publicación ni impacto comercial atribuido.

## Correcciones a la intro (IN09) — 2026-10-02

Revisión del candidato con tres puntos concretos; los cuatro ajustes CRO reservados siguen excluidos. Contribución de IA: (1) B/C/D plegados con conteo, resumen visible junto a la pregunta y puente E visible (intro CRO 2.603→972 px en escritorio, móvil sin desborde); (2) etiqueta «Vista derivada» con explicación para `ganados.csv` (vista calculada `vw_ganados` en `scripts/cro_demo.py`), `componentes_mes.csv` y `movimientos.csv` (calculados en `scripts/cfo_model.py`), resto como «Dato sintético», con gate y pruebas; (3) `intro-entrega.md` con hash final y nota de descargas parciales (trazabilidad, no paquete reproducible). Validación: `pnpm test` 47/47, coherence y build OK, comprobación en navegador de plegados y derivadas. Sin merge/push/publicación.

## Presentación final CRO+CFO (PF01–PF12) — 2026-10-02

Encargo: ejecutar `presentacion-final/plan.md` con ambos notebooks finales y pestañas separadas. Contribución de IA: (1) PF01 línea base (HEAD 8fda6f3 limpio; CRO 987c30a9 53c/12p; CFO 298dbb74 23c/2p; cambios concurrentes en fuente no tocados); (2) PF02 anexo/spec/storyboard/tasks + matriz; (3) PF03 sync de LOS DOS casos vía exportadores (CRO: celdas y 9 conclusiones + cierre; CFO: celdas y S06/S07/cierre; trazas CFO idénticas; cero mutaciones); (4) PF04 inicio ejecutivo veraz con método/entrega; (5–6) bloques Respuestas al reto con preguntas verificadas literales contra el reto y notas obsoletas corregidas; (7) hito visual con capturas; (8–10) método con episodios, nota corta (409 palabras), 2 guiones y 8 soportes con hashes en el build; (11) §14 completa: 50/50 pruebas, coherence, build, navegador (recarga, figura→conclusión, descargas 13/13, 390px, cero errores), CDN de CRO declarado; (12) entrega final. Revisión humana, 4 ajustes CRO, Plotly local CRO, grabación/publicación/envío pendientes. Sin merge/push/publicación.

## Correcciones de cobertura (post-PF12) — 2026-10-02

Revisión del dueño con cinco puntos (PF07 aceptado como avance, cobertura no cerrada). Contribución de IA: (1) R-CRO1 ampliada con reglas documentadas de medición para self-serve, SQL directo y abiertos (docs/casos/cro.md, modelo-cro-demo.md), distinguiendo propuesta de análisis realizado; (2) R-CFO3 con la frase del notebook («reduce el MRR neto por descuento, sin contracción subyacente de servicios»); (3) nota corta: escenario 110 con política frente a 100 sin política, igualando solo cambios ajenos y permanencia; (4) 47→50 pruebas con ejecución indicada; (5) HEAD vigente en entrega-final. Hallazgo propio: el router no re-renderizaba al cambiar de caso con el mismo ancla (`#/cro/respuestas`→`#/cfo/respuestas`); simplificado a ruta deseada + `rutaVista`, con prueba. Validación: 50/50, coherence, build y navegador (ida y vuelta entre casos, nota descargada). Sin merge/push/publicación.

## Cierre local CL01–CL06 — 2026-10-02

Encargo CIERRE-LOCAL con los cuatro ajustes reservados incluidos. Contribución de IA: CL01 línea base (HEAD 0624981, notebooks iguales); CL02 cierre CRO recompuesto (síntesis 3.6 restituida —estaba solo en el mapa—, tabla por foco sin evaluación repetida, criterios comunes una vez, aviso único; contrato/render/exportador actualizados); CL03 respaldo rotulado histórico en ambos casos + comp9 CRO al estado real; CL04 Plotly local compartido v4.1.1 (exportadores reescriben el cargador con verificación, manifiestos con `plotly_lib`, 01_new_tendencia con biblioteca embebida documentada); CL05 cro-entrega reescrita (histórica vs actual), entrega-final/matriz/nota sin contradicciones, pendientes actualizados en fuente sin commit; CL06 53/53 pruebas, coherence (incluye ausencia de CDN), build, navegador con red bloqueada (13/13 CRO + 2/2 CFO, cierre/respaldo/adjuntos/descargas, 390px, cero errores). Hallazgo propio anterior conservado: router re-renderiza entre casos. Estados: presentación local validada; revisión humana, videos, publicación y envío pendientes. Sin merge/push/publicación.

## Superficie ejecutiva PE01–PE06 — 2026-10-02

Encargo PRESENTACION-EJECUTIVA: web como soporte del video de 5 min, casos separados. Contribución de IA: mapa editorial por escena; capa `ejecutiva` en contenidos (aperturas con citas literales, 7 escenas que referencian bloques por ID, puentes editoriales); render con apertura, escenas (figura+conclusión+detalle plegado), cierre con tablas plegadas y respaldo único (capítulos compactos sin duplicar figuras, respuestas, intro/adjuntos, históricos); tipografía 18/32px acotada; retirada de frases internas de superficie; auto-apertura del respaldo ante anclas antiguas; guion reescrito en orden visible con anclas. Validación: 54/54, coherence, build; navegador en orden de grabación con red verificada; hashes iguales. Sin grabar/publicar/fusionar/enviar.

## Ajustes pre-grabación ejecutiva — 2026-10-02

Revisión del candidato con tres puntos. Contribución de IA: retirar frases internas de superficie; CFO con apertura breve (pregunta + 3 ejemplos) y cierre en decisión/responsable/éxito con umbral supeditado visible; guion como narración oral (556 palabras, anclas exactas, ejemplo acotado, cierre en decisiones). Validación: 54/54, coherence, build y navegador (apertura/cierre CFO, CRO intacto). Sin grabar/publicar/fusionar/enviar.

## Apertura autosuficiente CRO+CFO — 2026-10-02

Ajuste puntual de presentación (datos, figuras y preguntas intactos). Contribución de IA: apertura con pregunta original, síntesis diferenciada, recibidos compactos, insuficiencia, priorizadas literales, faltante y demo etiquetada; pregunta editable como copia local con aviso y restauración; adjuntos integrados con grupos separados; enlaces en azul oscuro con foco visible, sin saltos al respaldo desde datos; respaldo único al final. Validación: 55/55, coherence, build y navegador (edición/restauración, adjuntos, móvil 390, cero errores). Sin refactorizaciones grandes ni cambios analíticos.

## Ajuste narrativa T1–T7 — 2026-10-02

Encargo AJUSTE-NARRATIVA (sustituye AJUSTE-CRO-APERTURA, marcado). Contribución de IA: apertura A–F con pregunta editorial CRO referenciada, 11 priorizadas con refs (oficiales solo en respaldo), sin editor/estados/CSV; tramo New→mediana→conversión con mediana visible y título editorial persistido en exportación (trazas intactas); 8+4 CRO y 2 CFO sin iframes duplicados; CFO con S04 visible y detalle local; guion con nuevas anclas. Validación: 55/55, coherence, build; navegador (apertura, orden, detalles, móvil, adjuntos, sin CDN, cero errores); hashes iguales. Sin merge/push/publicación.

## Ajustes post-revisión narrativa — 2026-10-02

Tres correcciones del candidato (T1–T7 no cerradas). Contribución de IA: escena f-modelo con identidad visible y tabla plegada; e-plazo con síntesis y original en detalle; guion con pasos de calidad/modelo, redacción acotada y cierre en decisión CFO (582 palabras). Validación: 56/56, coherence, build y navegador. Sin merge/push/publicación.

## Orden de mediana y tiempos de guion — 2026-10-02

Ajuste puntual post-revisión (sin reorganizar ni cambiar análisis). Contribución de IA: escena con figura → síntesis → límite → puente → detalle plegado (sin cabecera externa duplicada; título interno intacto); guion sin solapes (Focos 1:55–2:05, Recuperación 3:30–4:00). Validación: 56/56, coherence, build y navegador. Siguiente paso del candidato: ensayo cronometrado.

## Limpieza de superficie CRO+CFO — 2026-10-02

Ajuste puntual (figuras, conclusiones y datos intactos). Contribución de IA: widget de adjuntos eliminado con todas sus conexiones; puente de apertura retirado; priorizadas en cursiva sin enlaces; índice de escenas eliminado (primera pregunta tras datos sintéticos); respaldo único final con anclas vigentes. Validación: 56/56, coherence, build y navegador (aperturas, navegación, móvil 390, cero errores). Sin merge/push/publicación.

## Simetría y respaldo S1–S5 — 2026-10-02

Encargo SIMETRIA-Y-RESPALDO. Contribución de IA: apertura común A–F con pregunta editorial referenciada y 11 priorizadas con refs (oficiales solo en respaldo plegado); f-modelo con detalle de ejemplos; respaldo único de 3 grupos (definiciones, fuentes/descargas, respuestas plegadas con IDs); historial fuera del render pero conservado en fuentes; anclas antiguas mapeadas (S01/S03→f-modelo, etc.); título editorial persistido en exportación. Validación: 56/56, coherence, build; navegador (aperturas simétricas, 14 figuras con render real, respaldo, anclas, descargas, 390px, sin CDN ni errores); hashes iguales. Sin merge/push/publicación.

## Dos pendientes de simetría — 2026-10-02

Correcciones puntuales post-S1–S5 (sin reorganizar). Contribución de IA: ejemplos S01 fuera de la apertura CFO (solo en detalle f-modelo); definición CRO de Niveles con niveles alcanzados/superados y visitas reales. Validación: 56/56, coherence, build y navegador. Commit final para el agente de publicación.
