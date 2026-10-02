# Qué queremos demostrar

**Revisión: 2026-09-30.** Orientación de evaluación; alcance vigente en la [spec aprobada](../../specs/001-solucion-analitica-finora/spec.md).

Resolver CRO y CFO y mostrar cómo el candidato estructura ambigüedad, analiza, valida IA y convierte evidencia en decisiones. **No conocemos una rúbrica oficial ni su ponderación:** estas demostraciones son propuestas.

## Capacidades y evidencia

| Capacidad indicada en oferta/reto | Cómo demostrarla |
| --- | --- |
| Estructurar problemas | Decisión, preguntas, definiciones e hipótesis comprobables. |
| Tratar datos incompletos | Calidad, supuestos, sensibilidad útil y evidencia faltante. |
| Profundidad analítica | Segmentos/cohortes, mezcla y maduración; distinguir asociación y causa. |
| Modelado y métricas SaaS | Grano, claves, vigencias y diccionario; separar suscripción, precio, descuento y pago. |
| SQL y autonomía | Transformaciones/controles reproducibles; explicar decisiones de consulta. |
| Uso crítico de IA | Ejemplos reales: delegación, resultado, revisión, corrección y validación. |
| Autoservicio y agentes | Definiciones consistentes, exploración guiada y respuestas trazables con límites. |
| Ownership e impacto | Acción, responsable propuesto, cadencia, indicador y criterio de revisión. |
| Comunicación | Lectura ejecutiva breve, gráficos útiles y respaldo técnico accesible. |
| Creatividad aplicada | Interacciones que aclaren decisiones; por ejemplo comparar explicaciones del mismo pago. |

La prueba demuestra trabajo actual, no años de experiencia, uso previo de CRM, inglés ni despliegues anteriores. Esas afirmaciones requieren experiencia real del candidato.

## Reglas para ejecutar y presentar

1. **Decisión antes de métricas.** CRO: demanda, calidad, atención, rutas y maduración. CFO: suscripción, precio, descuento y pago.
2. **Brechas con salida.** Qué puede medirse, supuestos, efecto de otra interpretación y datos necesarios. Cero pagado no demuestra churn contractual.
3. **Juicio visible.** Registrar elecciones, alternativas y correcciones; atribuir al candidato solo decisiones revisadas y asumidas por él.
4. **Herramientas con propósito.** Justificar utilidad, competencia demostrada, acceso, reproducibilidad, mantenimiento y tiempo. El formato libre no elimina SQL/modelado.
5. **IA verificable.** Episodios realizados: hipótesis, joins/unidades, descuentos o visualizaciones. La cantidad de herramientas/prompts no tiene ponderación publicada.
6. **Lectura por profundidad.** Primero situación, hallazgo o límite, implicación, decisión y acción; después exploración, evidencia, operación y proceso con IA. Definiciones consistentes.
7. **Impacto comprobable.** Indicador, población, ventana, comparación, éxito y efectos secundarios. No atribuir impacto real inexistente; etiquetar escenarios y ejemplos.

## Procedencia

Se trabajó sobre el enunciado aportado (documento privado, no incluido). La copia pública conserva preguntas, cifras, gráficas y soportes sintéticos.

Elegir herramientas y una entrega impactante son prioridades expresas del candidato. Creatividad/autoservicio son oportunidades de demostración, no requisitos oficiales añadidos.

## Evolución del alcance

La [conversación paralela](../fuentes/conversacion-paralela.txt) propuso web pública, preguntas naturales, archivos y método reutilizable. La preparación evaluó Pages/Functions y Workers/Static Assets, un agente, CSV y sesión temporal. Estas propuestas se resolvieron después en entrevista, spec y plan; no eran aprobaciones iniciales.

**Decisiones vigentes:** $0, Cloudflare gratuito, web sin login, un agente acotado, CSV y sesión temporal con descarga. Casos accesibles aunque falle IA. Credenciales fuera del navegador. «Grok» se interpretó como Groq por `gpt-oss-120b`: confirmar al integrar, junto con modelos gratuitos de Google AI Studio.

**Antes de integrar/publicar:** verificar cuentas/cuotas, seguridad, modelos gratuitos, límites de archivos/uso y rendimiento representativo. Se consultaron [Static Assets](https://developers.cloudflare.com/workers/static-assets/), [tarifas](https://developers.cloudflare.com/workers/platform/pricing/) y [límites](https://developers.cloudflare.com/workers/platform/limits/). Referencias de preparación: Workers Free, 100.000 solicitudes/día y 10 ms CPU/invocación; [Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/), 10.000 Neurons/día y algunos modelos con método de pago. Workers AI fue evaluado, no seleccionado. Estas cifras no garantizan vigencia ni capacidad suficiente para el análisis.

Constitución/spec aprobadas el 2026-09-30; entrevista completada, plan/tareas preparados. Implementación pendiente. Plazo/entregables: [contexto](../contexto.md). Historial/validaciones: [bitácora](../proceso/proceso-ia.md).
