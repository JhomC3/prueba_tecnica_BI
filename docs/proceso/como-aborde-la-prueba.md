# Cómo abordé la prueba técnica

**Escenario Finora · 29–30 de septiembre de 2026.**

Relato para evaluadores, redactado con apoyo de Codex a partir de mensajes públicos y documentos. Distingue decisiones del candidato y ejecuciones de IA. Casos aún sin resolver.

## 1. Entender la evaluación

Pedí iniciar el proyecto, instalar SDD, indexarlo y recuperar el contexto. Corregí a Codex: debía reutilizar mi kit personal. Retiró la instalación equivocada. También registró un perfil exploratorio elaborado antes de cerrar la preparación, sin presentarlo como solución.

Pedí releer oferta y reto: debía demostrar tanto resultados como mi forma de estructurar problemas, tratar ambigüedad, usar IA y elegir herramientas. Codex distinguió requisitos expresos y propuestas propias.

## 2. Organizar el trabajo

Hice una pausa ante la acumulación de información y propuse cuatro etapas:

| Etapa | Resultado | Estado al cerrar la preparación |
| --- | --- | --- |
| 1. Definir el abordaje | Método, preguntas, tareas, dependencias y prioridades. | Constitución/spec aprobadas. |
| 2. Resolver el reto | Respuestas a CRO/CFO con evidencia y límites. | Pendiente; después comenzó la formulación CRO. |
| 3. Automatizar | Reutilizar operaciones validadas. | Alcance acordado; implementación pendiente. |
| 4. Presentar | Web, soporte y videos comprensibles. | Definidos; producción pendiente. |

Separé organización del proyecto y análisis de cada caso. La presentación se prepara desde el análisis, sin esperar al final.

## 3. Construir y cuestionar el método

Propuse los 13 componentes y los relacioné con la oferta. Pedí una revisión crítica y acepté ajustes: calidad explícita, comprobación de hipótesis antes del diagnóstico, acción de negocio distinta de solución analítica y éxito definido desde el inicio.

El [marco](../metodo/marco-de-trabajo.md) conserva preguntas, resultados y criterios. Documentación y validación de IA atraviesan el método.

## 4. Acotar la solución

Fijé el pragmatismo: dedicar tiempo a lo que aporte valor. Propuse una web pública sencilla y aporté una [conversación paralela](../fuentes/conversacion-paralela.txt).

Cuestioné pedir un tercer caso para definir la spec. Codex reformuló: un ejemplo adicional demostrará reutilización, sin exigir tres casos nuevos.

| Decisión confirmada | Consecuencia |
| --- | --- |
| Antes del 2 de octubre, mediodía Colombia; objetivo 30 de septiembre/1 de octubre. | Entrega completa temprana. |
| $0 y Cloudflare gratuito. | Verificar cuotas; ningún paso automático a pago. |
| Credenciales existentes de IA. | «Grok» interpretado como Groq por el modelo; verificar al integrar. |
| Sesión temporal y resumen descargable. | Evitar cuentas e historial persistente. |
| Casos accesibles si falla IA. | Preservar la entrega principal. |
| Solo CSV si Excel añade complejidad innecesaria. | Acotar formatos. |

Revisé y aprobé constitución y spec. Codex preparó plan y 34 tareas con dependencias, tiempos estimados y cierre; no son tareas ejecutadas.

## 5. Comprender lo aprobado y proteger fuentes

Pregunté qué contenía la spec, qué se había hecho con los datos y por qué separar el agente. Se distinguieron enunciado, respuesta preparada y exploración de preguntas nuevas.

Codex inspeccionó filas, claves, vacíos, ceros, importes y cobertura. Faltan eventos comerciales/descuentos; ceros y unidad S&M siguen ambiguos. El perfil no prueba causas ni MRR contractual.

Pedí Git y organización. Codex inició el repositorio, preservó el estado y movió CSV a `inputs/` y fuentes a `docs/fuentes/`. Verificó cinco fuentes idénticas y 36 enlaces válidos. Commits de respaldo: `22b8dce` y `4af0e86`.

## 6. Iniciar CRO — 2026-09-30

Definí la presentación: requerimiento original seguido de 13 componentes. Leí el caso frase por frase y cuestioné periodos, alcance, calidad, tiempos, rutas y conversiones, evitando bombardear al CRO.

Propuse medir cada etapa. Codex distinguió objetivo, necesidad y decisión; añadió rutas, resultado global y maduración. Self-serve contribuye al crecimiento, aunque no recorra etapas comerciales.

La [formulación CRO](../casos/cro.md) distingue mis aportaciones y propuestas de IA, todavía en discusión. No simula respuestas ni presenta hipótesis como hallazgos.

## Autoría, estado y respaldo

Mis intervenciones fijaron objetivo, método, restricciones y aprobaciones; corregí y cuestioné propuestas. Codex leyó fuentes, revisó alternativas, formalizó y ejecutó verificaciones técnicas, registradas como trabajo de IA.

Sin aplicación, hallazgos finales, integración LLM, despliegue ni videos terminados. Cuotas/rendimiento pendientes. No se calcularon métricas CRM con datos inexistentes.

- [Preparación](conversacion-preparacion.md) y [resolución](conversacion-resolucion.md): mensajes públicos originales.
- [Bitácora](proceso-ia.md): acciones, errores y comprobaciones.
- [Entrevista](../sdd/entrevista-sdd.md), [spec](../../specs/001-solucion-analitica-finora/spec.md) y [tareas](../../specs/001-solucion-analitica-finora/tasks.md): alcance y trabajo pendiente.

Actualizaré solo decisiones, correcciones y resultados relevantes, con aportación humana/IA, motivo, validación y estado. Sin fabricar un proceso retrospectivo.

## 7. Continuidad e inicio CFO — 2026-09-30

Pedí recuperar el contexto completo y la conversación del proyecto para iniciar el segundo caso con el mismo método. Codex revisó constitución, spec/plan/tareas, fuentes, documentación y el historial del chat «Preparar contexto del proyecto». Recuperó las correcciones de CRO: notebook como hilo principal, tablas explicadas, cobertura de preguntas antes de gráficas y revisión de una pregunta/gráfica a la vez.

La base sintética CRO y la primera gráfica de New están preparadas; diagnóstico y acciones siguen pendientes. Codex volvió a ejecutar las trece pruebas y comprobó los hashes de los 57 CSV del manifiesto y de los tres originales. Inició el [documento CFO](../casos/cfo.md) con el requerimiento original y el decisor. La formulación de la decisión será el siguiente componente con el candidato; no se implementó el modelo CFO ni se adelantaron gráficas.

## 8. Planificar la web con el avance disponible — 2026-09-30

Solicité recuperar contexto, conversaciones y trabajo realizado para preparar una exploración y un plan detallado de la web. Codex contrastó la documentación, historial accesible y artefactos actuales; preparó [el plan de la primera web](../../specs/001-solucion-analitica-finora/plan-web.md). Propone requerimiento original y 13 componentes por caso, CRO con la figura New existente, CFO con su formulación inicial y pendientes visibles. Recomienda reutilizar Plotly y adelantar la base visual. La exploración con IA y la entrega completa conservan su alcance. No se implementó ni publicó la web en esta sesión.

## Comparar las lecturas CFO — 2026-10-01

Aporté mi primera lectura y realicé una segunda; pedí identificar preguntas omitidas/nuevas y sintetizarlas para revisión. Codex distinguió preguntas compartidas, definición explícita nueva de expansión y cambio hacia descuentos solo para ampliación. Recuperó retención/churn, métricas alternativas y necesidad real planteadas antes. Contrastó la clasificación de descuentos con documentación oficial de ChartMogul y dejó las interpretaciones y la síntesis separadas del texto de referencia. No se aprobaron políticas ni se implementó CFO.

## Objetivo comercial de descuentos — 2026-10-01

El candidato separó la intención comercial de aplicar descuentos de la necesidad inmediata del CFO y propuso ampliación, retención y adquisición. Codex evaluó cada objetivo y propuso reactivación solo si aplica; precisó población/periodo para relacionar retención y churn. No se confirmó una política de Finora.

## Alcance de descuentos — 2026-10-01

El candidato preguntó «si los descuentos únicamente son para clientes antiguos, existentes o para clientes nuevos», a partir de los ejemplos del CFO. Codex distinguió ejemplos sobre clientes existentes de una política exclusiva: el enunciado no confirma esa restricción. Elegibilidad pendiente, vinculada al objetivo comercial; sin implementación.

## Prioridad propuesta de efectividad — 2026-10-01

Propuse priorizar «¿aplicar descuentos aumenta la facturación o aumenta el ingreso mensual recurrente?» y medir antes/después según monto, porcentaje y duración. Codex conservó la pregunta y distinguió descripción temporal de efecto atribuible al descuento; señaló que retención puede evitar una caída y que facturación/MRR requieren definiciones separadas. La pregunta de efectividad complementa las exigencias del CFO; no hay resultados calculados.

## Aproximación mediante tendencias y retención — 2026-10-01

El candidato propuso permanencia media, churn y MRR promedio y tendencias antes/después del descuento, con ejemplos hipotéticos de tres a seis meses y de 30 a 40. Codex reconoció la hipótesis de compensación por permanencia/base activa; precisó seguimiento comparable, clientes aún activos, total frente a promedio y separación de adquisición. Propuso ingreso neto acumulado en horizonte común y mantuvo límites de datos/causalidad. Ejemplos sin calcular, no hallazgos ni supuestos numéricos aprobados.

## Ajuste por crecimiento previo — 2026-10-01

El candidato propuso descontar una tendencia media de crecimiento (5% como ejemplo) para observar un cambio ajustado y preguntó si sería sobreingeniería. Codex lo evaluó como línea base sencilla y condicionada: observado menos esperado, continuidad de tendencia explícita, horizonte/población comparables; diferencia de tasas en puntos porcentuales y sin atribución causal automática. Sin cálculos ni cambio de implementación.

## Síntesis breve CFO — 2026-10-01

Pedí condensar lo discutido en un documento organizado, breve y completo. Codex preparó `docs/casos/cfo-sintesis.md` con pregunta original, objetivos/elegibilidad, definiciones, métricas, comparación por periodos/cohortes y tendencia, datos/modelo y pendientes. Conservó las referencias originales y separó hipótesis de resultados; no ejecutó análisis.

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

## Extraer el patrón de razonamiento — 2026-10-01

El candidato pidió revisar todas las conversaciones del proyecto y amplió el encargo a todos los archivos del directorio para capturar su forma de preguntar, analizar y ejercer pensamiento crítico. Codex recuperó 151 turnos y 154 mensajes del candidato de seis chats con contenido, registró un chat relacionado sin mensajes recuperables e inspeccionó 188 archivos de trabajo. Elaboró el [patrón de razonamiento](../metodo/marco-de-trabajo.md), instrucciones reutilizables y treinta extractos literales cotejados. Conservó los 13 componentes y separó aportes del candidato, precisiones de IA e interpretaciones nuevas. La síntesis documental está preparada para contraste humano; no acredita un agente general implementado ni nuevas conclusiones de negocio.

## Corrección de primera pregunta CFO — 2026-10-01

El candidato corrigió expresamente la primera pregunta: retirar facturación y centrarse en ingreso mensual recurrente. Pregunta vigente: «¿aplicar descuentos aumenta el ingreso mensual recurrente?». Codex actualizó pregunta y evidencia de la primera fila en sección 4. Redacción previa conservada únicamente como referencia histórica; sin cálculos ni modificación de otras preguntas.

## Continuidad incremental del marco — 2026-10-01

El candidato pidió que los documentos del patrón evolucionen cuando solicite nuevas revisiones, examinando solo los cambios posteriores al último corte. Codex registró protocolo, marcadores de conversaciones y versiones de referencia. No repitió la revisión analítica ni incorporó como revisados mensajes nuevos de otros chats.

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

## Implementación analítica CFO autorizada — 2026-10-01

El candidato solicitó preparar datos, métricas y presentación siguiendo el caso CRO; pidió primero propuesta y detener creación hasta su autorización. Tras revisar la propuesta de tres escenarios y ventana seis meses previos/tres de descuento/seis posteriores, autorizó: «Bien, comencemos con la implementación y la creación de los datos, de las métricas, de todo, gráficas, todo».

Codex actualizó spec/plan/tareas antes de implementar. Creó `scripts/cfo_model.py`, puente SQL, pruebas independientes, `scripts/cfo_present.py`, `scripts/validate_cfo.py` y notebook `03_modelo_cfo.ipynb`. CSV y SQLite por escenario y grupo pareado; componentes/precios/descuentos/estados separados del pago. Reutilizó entorno y presentación CRO: qué medimos, alcance, fórmula/datos y cálculos plegados. Implementó MRR bruto/neto/descuentos, crecimiento, ARR/ARPU, retención/churn, NRR/GRR, LTV estacionario, permanencia observada y acumulados. Costos/CAC/margen no inventados.

Las pruebas iniciales detectaron que bajas de clientes elegibles impedían el equilibrio esperado del escenario compensado. Se corrigió la simulación para aislar ampliación/descuento; bajas y adquisición iguales entre grupos. No se atribuye mejora de retención a esa política. Julio 2025–marzo 2026: positivo +9.000 UM, negativo −3.000 UM, compensado 0 UM frente a referencias sin descuento; son resultados simulados, no efectos reales ni utilidad.

Validación: 11 pruebas CFO pasan y suite completa de 34 pruebas pasa. La versión final del notebook ejecutó todas sus celdas desde kernel nuevo; Jupyter requirió ejecución autorizada fuera del sandbox para abrir sus puertos locales. Tres bases concilian sin residuo y validan relaciones; 66 CSV con hashes y 27 figuras HTML generadas. Fuentes `inputs/` intactas respecto de hashes previos. Ver `resultados/cfo/validacion.json` y `docs/datos/modelo-cfo-demo.md`. Revisión visual del navegador local no realizada por restricción de acceso a archivos; revisión humana de figuras y conclusiones pendiente. No se publica web ni se autoriza política comercial ni se declara la prueba completa entregada.


### Reorientar el análisis hacia la decisión

El candidato revisó las gráficas y volvió a la pregunta principal: «¿La tasa de conversión de New a Won aumentó o disminuyó después del aumento de New?». Propuso un recorrido: confirmar el aumento, comparar conversión por canal, revisar calidad, localizar etapas afectadas, investigar causas y definir acciones. Solicitó conservar el trabajo y reorganizarlo, dejando los análisis complementarios como apoyo. La IA aplicó ese orden, mantuvo preguntas/cálculos y señaló las comparaciones de población todavía pendientes.

## Aplicación del marco de razonamiento al análisis CFO — 2026-10-01

El candidato solicitó aplicar al análisis construido el recorrido formalizado: enfocar, comprobar, localizar, explicar, actuar y evaluar; cada hallazgo determina el siguiente análisis y cada análisis aporta a la pregunta principal. Codex leyó el patrón y ficha de aplicación; no modificó el marco ni avanzó sus marcadores de revisión.

Actualizó spec/plan/tareas y reorganizó notebook CFO: pregunta/decisión al inicio, resultado frente a referencia, focos por elegibilidad y fase, explicación de bruto/descuento y movimientos, acciones condicionadas y evaluación. Conservó las cinco preguntas de referencia y los 13 componentes. Retención/LTV y otros indicadores permanecen en respaldo plegado, disponibles según evidencia. No sustituyó preguntas ni eliminó métricas o figuras.

Añadió vistas derivadas `focos.csv` y `recorrido.json` y lectura automática por resultado: aumentar, reducir o equilibrar ingreso. Comprobó que el resto aporta cero y que la reducción/recuperación del compensado se cancelan (−3.000 y +3.000 UM). Verificó actividad igual por cliente; estabilidad agregada no se usa como descarte universal de causas. La acción y evaluación registran responsables propuestos, control mensual y cierre después de vigencia/seguimiento; no atribuyen piloto ni impacto real ejecutados.

Validaciones: 38 pruebas de proyecto pasan (15 CFO), incluidas conciliación de focos, compensación temporal, acciones distintas y no inventar foco si no hay diferencia. Ejecución desde kernel nuevo detectó una variable de ruta usada antes de su definición por el traslado de celdas; se corrigió su inicialización y el notebook completo pasó. Comparación SHA-256 confirma fuentes, bases, indicadores y 27 figuras previas intactos. Se actualizaron conclusiones y vistas de recorrido; revisión humana pendiente. Evidencia en `resultados/cfo/validacion.json`.

## Preparar el agente con mi método — 2026-10-01

Definí que el agente debe aproximarse a mis lineamientos analíticos ya documentados y poder evolucionar. Acepté una entrega estática con escenarios y resultados si la integración compromete el plazo o exige esfuerzo excesivo. Codex revisó el marco, patrón e instrucciones existentes y preparó [su aplicación al agente](../../specs/001-solucion-analitica-finora/plan-agente.md), sin implementar ni afirmar fidelidad demostrada. La referencia «Jeff» queda pendiente de identificar.

## Dos modos sobre la misma web — 2026-10-01

Propuse conservar el análisis preparado en una pestaña y reutilizarlo en otra con el agente añadido. Aclaré que el componente era Jev de TypeSafe y aporté los enlaces. Codex revisó documentación y registró su papel de decisión acotada, límites y condición de acceso gratuito; la conversación y los cálculos conservan sus módulos. Ambas pestañas compartirán contenido/componentes y el modo preparado seguirá disponible sin IA. Diseño registrado, implementación pendiente.

## Elegir tecnología por su aporte — 2026-10-01

Pedí evaluar Jev críticamente y usarlo solo donde aportara valor concreto sin comprometer la entrega. Codex propuso priorizar el asistente básico y, después, una clasificación opcional de intención con pruebas y fallback. La incorporación queda condicionada a acceso gratuito, utilidad observada y esfuerzo acotado; no se presenta como mejora analítica demostrada.

### 2026-10-01 — Preparación de una implementación delegable

El candidato delimitó esta sesión a planificación y reservó el código a otro agente. Se preparó un anexo dentro de la spec activa con tareas secuenciales, criterios verificables y puertas de continuación. La entrega preparada conserva prioridad; versiones parciales declaran lo pendiente y Jev solo se evalúa después del asistente básico. El paquete queda listo para revisión, sin desarrollo del módulo ni llamadas reales.


### Consolidación pragmática del método — 2026-10-01

El candidato pidió un único archivo práctico, sin redundancia ni complejidad innecesaria. La IA consolidó el recorrido, los 13 componentes conservados literalmente, criterios, ficha, evidencia esencial y mantenimiento en [el marco](../metodo/marco-de-trabajo.md). Las versiones previas y evidencias completas se archivaron preservando sus bytes. Se mantuvieron los cortes y pendientes de revisión; esta reorganización no equivale a una nueva revisión completa.
