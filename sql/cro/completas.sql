-- Consultas sobre datos observados al corte; __SEGMENTO__ es un identificador
-- de dimensión permitido por el código, nunca texto procedente del usuario.
-- @consulta demanda
WITH RECURSIVE meses(mes) AS (
 SELECT '2026-01' UNION ALL SELECT strftime('%Y-%m',date(mes||'-01','+1 month')) FROM meses WHERE mes<'2026-08'
), segmentos AS (SELECT DISTINCT __SEGMENTO__ segmento FROM dim_cuentas c WHERE c.fecha_captacion<=:corte), agregado AS (
 SELECT substr(c.fecha_captacion,1,7) mes,__SEGMENTO__ segmento,
 COUNT(*) captados,SUM(c.tipo_entrada='New') entradas_new,
 SUM(c.canal IN ('Marketing pago','Orgánico')) entradas_marketing
 FROM dim_cuentas c WHERE c.fecha_captacion<=:corte GROUP BY mes,segmento
), completo AS (
 SELECT m.mes,s.segmento,COALESCE(a.captados,0) captados,COALESCE(a.entradas_new,0) entradas_new,
 COALESCE(a.entradas_marketing,0) entradas_marketing
 FROM meses m CROSS JOIN segmentos s LEFT JOIN agregado a ON a.mes=m.mes AND a.segmento=s.segmento
 WHERE m.mes<=substr(:corte,1,7)
), anterior AS (
 SELECT *,lag(captados) OVER(PARTITION BY segmento ORDER BY mes) captados_anterior,
 lag(entradas_new) OVER(PARTITION BY segmento ORDER BY mes) new_anterior,
 lag(entradas_marketing) OVER(PARTITION BY segmento ORDER BY mes) marketing_anterior FROM completo
)
SELECT *,captados-captados_anterior diferencia_captados,
 100.0*(captados-captados_anterior)/NULLIF(captados_anterior,0) crecimiento_captados_pct,
 100.0*(entradas_new-new_anterior)/NULLIF(new_anterior,0) crecimiento_new_pct,
 100.0*(entradas_marketing-marketing_anterior)/NULLIF(marketing_anterior,0) crecimiento_marketing_pct
FROM anterior ORDER BY segmento,mes;
-- @consulta calidad
SELECT substr(c.fecha_captacion,1,7) mes,__SEGMENTO__ segmento,
 COALESCE(c.version_criterios,'v1') version_criterios,COUNT(*) prospectos,
 SUM(c.fecha_evaluacion IS NOT NULL AND c.fecha_evaluacion<=:corte) evaluados,
 SUM(CASE WHEN c.fecha_evaluacion<=:corte THEN c.calificado ELSE 0 END) calificados,
 100.0*SUM(c.fecha_evaluacion IS NOT NULL AND c.fecha_evaluacion<=:corte)/COUNT(*) cobertura_evaluacion_pct,
 100.0*SUM(CASE WHEN c.fecha_evaluacion<=:corte THEN c.calificado ELSE 0 END)/
 NULLIF(SUM(c.fecha_evaluacion IS NOT NULL AND c.fecha_evaluacion<=:corte),0) calidad_pct
FROM dim_cuentas c WHERE c.fecha_captacion<=:corte GROUP BY mes,segmento,COALESCE(c.version_criterios,'v1');
-- @consulta descalificaciones
SELECT substr(c.fecha_captacion,1,7) mes,__SEGMENTO__ segmento,
 c.version_criterios,COALESCE(c.motivo_descalificacion,'Sin motivo registrado') motivo,COUNT(*) descalificados
FROM dim_cuentas c WHERE c.calificado=0 AND c.fecha_evaluacion<=:corte
GROUP BY mes,segmento,c.version_criterios,motivo;
-- @consulta atencion
WITH contactos AS (
 SELECT id_registro,MIN(fecha) primer_intento,COUNT(*) intentos,
 MAX(resultado='intercambio_efectivo') efectivo
 FROM interacciones WHERE fecha<=:corte GROUP BY id_registro
), base AS (
 SELECT f.*,c.canal,c.tipo_entrada,c.industria,c.perfil,c.producto,c.region,c.campana,
 i.primer_intento,COALESCE(i.intentos,0) intentos,COALESCE(i.efectivo,0) efectivo
 FROM fact_etapas f JOIN dim_cuentas c USING(id_cuenta) LEFT JOIN contactos i USING(id_registro)
 WHERE f.entrada<=:corte AND f.id_etapa<>'Won'
)
SELECT c.id_etapa etapa,substr(c.entrada,1,7) mes,__SEGMENTO__ segmento,
 COUNT(*) visitas,SUM(c.intentos>0) visitas_con_intento,SUM(c.intentos=0) visitas_sin_intento,
 SUM(c.intentos) intentos,SUM(c.efectivo) visitas_contacto_efectivo,
 100.0*SUM(c.intentos>0)/COUNT(*) cobertura_intento_pct,
 100.0*SUM(c.efectivo)/NULLIF(SUM(c.intentos>0),0) contacto_efectivo_pct,
 mediana(julianday(c.fecha_asignacion_etapa)-julianday(c.entrada)) mediana_espera_asignacion,
 mediana(julianday(c.primer_intento)-julianday(c.entrada)) mediana_primer_intento,
 p90(julianday(c.primer_intento)-julianday(c.entrada)) p90_primer_intento,
 mediana(julianday(c.primer_intento)-julianday(c.fecha_asignacion_etapa)) mediana_atencion_tras_asignacion,
 SUM(julianday(:corte)-julianday(c.entrada)>=:plazo) elegibles_plazo,
 SUM(CASE WHEN julianday(:corte)-julianday(c.entrada)>=:plazo AND julianday(c.primer_intento)-julianday(c.entrada)<=:plazo THEN 1 ELSE 0 END) atendidos_en_plazo,
 100.0*SUM(CASE WHEN julianday(:corte)-julianday(c.entrada)>=:plazo AND julianday(c.primer_intento)-julianday(c.entrada)<=:plazo THEN 1 ELSE 0 END)/
 NULLIF(SUM(julianday(:corte)-julianday(c.entrada)>=:plazo),0) puntualidad_pct
FROM base c GROUP BY etapa,mes,segmento;
-- @consulta etapas
WITH base AS (
 SELECT e.*,d.siguiente,c.canal,c.tipo_entrada,c.industria,c.perfil,c.producto,c.region,c.campana
 FROM vw_etapas_cuenta e JOIN dim_cuentas c USING(id_cuenta) JOIN dim_etapas d USING(id_etapa)
 WHERE e.entrada<=:corte AND e.id_etapa<>'Won'
), ventanas(dias) AS (VALUES(30),(60),(90))
SELECT c.id_etapa etapa,substr(c.entrada,1,7) mes,__SEGMENTO__ segmento,v.dias ventana,
 COUNT(*) cuentas_entrada,SUM(c.visitas) visitas,
 SUM(julianday(:corte)-julianday(c.entrada)>=v.dias) elegibles,
 SUM(CASE WHEN julianday(:corte)-julianday(c.entrada)>=v.dias AND julianday(c.salida)-julianday(c.entrada)<=v.dias AND c.estado='avance' AND c.id_etapa_destino=c.siguiente THEN 1 ELSE 0 END) avances_siguiente,
 SUM(CASE WHEN julianday(:corte)-julianday(c.entrada)>=v.dias AND julianday(c.salida)-julianday(c.entrada)<=v.dias AND c.estado='avance' AND c.id_etapa_destino<>c.siguiente THEN 1 ELSE 0 END) saltos,
 SUM(CASE WHEN julianday(:corte)-julianday(c.entrada)>=v.dias AND julianday(c.salida)-julianday(c.entrada)<=v.dias AND c.estado='perdido' THEN 1 ELSE 0 END) perdidos,
 100.0*SUM(CASE WHEN julianday(:corte)-julianday(c.entrada)>=v.dias AND julianday(c.salida)-julianday(c.entrada)<=v.dias AND c.estado='avance' AND c.id_etapa_destino=c.siguiente THEN 1 ELSE 0 END)/
 NULLIF(SUM(julianday(:corte)-julianday(c.entrada)>=v.dias),0) conversion_pct,
 SUM(c.estado='abierto') abiertos_corte,
 100.0*SUM(c.estado='abierto')/COUNT(*) abiertos_corte_pct,
 mediana(CASE WHEN c.salida<=:corte THEN julianday(c.salida)-julianday(c.entrada) END) mediana_permanencia,
 p90(CASE WHEN c.salida<=:corte THEN julianday(c.salida)-julianday(c.entrada) END) p90_permanencia,
 mediana(CASE WHEN c.estado='abierto' THEN julianday(:corte)-julianday(c.entrada) END) mediana_antiguedad_abiertos,
 p90(CASE WHEN c.estado='abierto' THEN julianday(:corte)-julianday(c.entrada) END) p90_antiguedad_abiertos
FROM base c CROSS JOIN ventanas v GROUP BY etapa,mes,segmento,v.dias;
-- @consulta perdidas
SELECT f.id_etapa etapa,substr(f.entrada,1,7) mes,__SEGMENTO__ segmento,
 COALESCE(f.motivo_perdida,'Sin motivo registrado') motivo,COUNT(*) perdidas
FROM fact_etapas f JOIN dim_cuentas c USING(id_cuenta)
WHERE f.estado='perdido' AND f.salida<=:corte GROUP BY etapa,mes,segmento,motivo;
-- @consulta cohortes
WITH ventanas(dias) AS (VALUES(30),(60),(90))
SELECT substr(c.fecha_captacion,1,7) mes_entrada,__SEGMENTO__ segmento,v.dias ventana,
 COUNT(*) entradas_new,SUM(julianday(:corte)-julianday(c.fecha_captacion)>=v.dias) elegibles,
 SUM(CASE WHEN julianday(:corte)-julianday(c.fecha_captacion)>=v.dias AND julianday(w.fecha_won)-julianday(c.fecha_captacion)<=v.dias THEN 1 ELSE 0 END) ganados_ventana,
 100.0*SUM(CASE WHEN julianday(:corte)-julianday(c.fecha_captacion)>=v.dias AND julianday(w.fecha_won)-julianday(c.fecha_captacion)<=v.dias THEN 1 ELSE 0 END)/
 NULLIF(SUM(julianday(:corte)-julianday(c.fecha_captacion)>=v.dias),0) conversion_new_won_pct,
 SUM(EXISTS(SELECT 1 FROM fact_etapas e WHERE e.id_cuenta=c.id_cuenta AND e.estado='abierto')) abiertos_corte,
 mediana(julianday(w.fecha_won)-julianday(c.fecha_captacion)) mediana_dias_new_won,
 p90(julianday(w.fecha_won)-julianday(c.fecha_captacion)) p90_dias_new_won
FROM dim_cuentas c LEFT JOIN vw_ganados w ON w.id_cuenta=c.id_cuenta AND w.fecha_won<=:corte CROSS JOIN ventanas v
WHERE c.tipo_entrada='New' AND c.fecha_captacion<=:corte GROUP BY mes_entrada,segmento,v.dias;
-- @consulta origen_cierres
SELECT substr(w.fecha_won,1,7) mes_cierre,substr(c.fecha_captacion,1,7) mes_entrada,
 __SEGMENTO__ segmento,COUNT(*) ganados
FROM vw_ganados w JOIN dim_cuentas c USING(id_cuenta) WHERE w.fecha_won<=:corte GROUP BY mes_cierre,mes_entrada,segmento;
-- @consulta pagadores
SELECT substr(p.fecha_primer_pago,1,7) mes_pago,__SEGMENTO__ segmento,COUNT(*) nuevos_pagadores,
 mediana(julianday(p.fecha_primer_pago)-julianday(c.fecha_captacion)) mediana_dias_hasta_pago,
 p90(julianday(p.fecha_primer_pago)-julianday(c.fecha_captacion)) p90_dias_hasta_pago,
 SUM(c.tipo_entrada='Producto') compras_desde_producto
FROM vw_primer_pago p JOIN dim_cuentas c USING(id_cuenta)
WHERE p.fecha_primer_pago<=:corte AND p.fecha_primer_pago>=c.fecha_captacion AND c.pagador_previo=0
 AND c.inicio_historia_pagos<=c.fecha_captacion GROUP BY mes_pago,segmento;
-- @consulta captacion_pago
WITH ventanas(dias) AS (VALUES(30),(60),(90))
SELECT substr(c.fecha_captacion,1,7) mes_entrada,__SEGMENTO__ segmento,v.dias ventana,
 COUNT(*) captados_sin_pago_previo,SUM(julianday(:corte)-julianday(c.fecha_captacion)>=v.dias) elegibles,
 SUM(CASE WHEN julianday(:corte)-julianday(c.fecha_captacion)>=v.dias AND julianday(p.fecha_primer_pago)-julianday(c.fecha_captacion)<=v.dias THEN 1 ELSE 0 END) nuevos_pagadores_ventana,
 100.0*SUM(CASE WHEN julianday(:corte)-julianday(c.fecha_captacion)>=v.dias AND julianday(p.fecha_primer_pago)-julianday(c.fecha_captacion)<=v.dias THEN 1 ELSE 0 END)/
 NULLIF(SUM(julianday(:corte)-julianday(c.fecha_captacion)>=v.dias),0) conversion_pago_pct
FROM dim_cuentas c LEFT JOIN vw_primer_pago p ON p.id_cuenta=c.id_cuenta AND p.fecha_primer_pago<=:corte CROSS JOIN ventanas v
WHERE c.fecha_captacion<=:corte AND c.pagador_previo=0 AND c.inicio_historia_pagos<=c.fecha_captacion
GROUP BY mes_entrada,segmento,v.dias;
-- @consulta prioridad
WITH base AS (
 SELECT e.*,d.siguiente,c.canal,c.tipo_entrada,c.industria,c.perfil,c.producto,c.region,c.campana FROM vw_etapas_cuenta e JOIN dim_etapas d USING(id_etapa) JOIN dim_cuentas c USING(id_cuenta)
 WHERE e.id_etapa<>'Won' AND e.entrada<'2026-09-01' AND julianday(:corte)-julianday(e.entrada)>=30
), resumen AS (
 SELECT c.id_etapa etapa,__SEGMENTO__ segmento,
 COUNT(CASE WHEN c.entrada<'2026-05-01' THEN 1 END) elegibles_base,
 COUNT(CASE WHEN c.entrada>='2026-05-01' THEN 1 END) elegibles_reciente,
 SUM(CASE WHEN c.entrada<'2026-05-01' AND c.estado='avance' AND c.id_etapa_destino=c.siguiente AND julianday(c.salida)-julianday(c.entrada)<=30 THEN 1 ELSE 0 END) avances_base,
 SUM(CASE WHEN c.entrada>='2026-05-01' AND c.estado='avance' AND c.id_etapa_destino=c.siguiente AND julianday(c.salida)-julianday(c.entrada)<=30 THEN 1 ELSE 0 END) avances_reciente,
 COUNT(CASE WHEN c.entrada>='2026-05-01' AND p.fecha_primer_pago>=a.fecha_captacion AND a.pagador_previo=0 AND p.fecha_primer_pago<=:corte THEN 1 END) nuevos_pagadores_de_entradas_recientes
 FROM base c JOIN dim_cuentas a USING(id_cuenta)
 LEFT JOIN vw_primer_pago p USING(id_cuenta)
 GROUP BY etapa,segmento
)
SELECT *,100.0*avances_base/NULLIF(elegibles_base,0) conversion_base_pct,
 100.0*avances_reciente/NULLIF(elegibles_reciente,0) conversion_reciente_pct,
 100.0*avances_reciente/NULLIF(elegibles_reciente,0)-100.0*avances_base/NULLIF(elegibles_base,0) brecha_pp,
 MAX(0,1.0*avances_base/NULLIF(elegibles_base,0)*elegibles_reciente-avances_reciente) avances_brecha_ilustrativa
FROM resumen;
-- @consulta resultado_global
WITH RECURSIVE eventos AS (
 SELECT substr(c.fecha_captacion,1,7) mes,__SEGMENTO__ segmento,
 CASE WHEN c.tipo_entrada='New' THEN 1 ELSE 0 END nuevos,0 ganados,0 pagadores
 FROM dim_cuentas c WHERE c.fecha_captacion<=:corte
 UNION ALL
 SELECT substr(w.fecha_won,1,7),__SEGMENTO__,0,1,0 FROM vw_ganados w JOIN dim_cuentas c USING(id_cuenta) WHERE w.fecha_won<=:corte
 UNION ALL
 SELECT substr(p.fecha_primer_pago,1,7),__SEGMENTO__,0,0,1 FROM vw_primer_pago p JOIN dim_cuentas c USING(id_cuenta)
 WHERE p.fecha_primer_pago>=c.fecha_captacion AND p.fecha_primer_pago<=:corte AND c.pagador_previo=0 AND c.inicio_historia_pagos<=c.fecha_captacion
), meses(mes) AS (
 SELECT '2026-01' UNION ALL SELECT strftime('%Y-%m',date(mes||'-01','+1 month')) FROM meses WHERE mes<(SELECT MAX(mes) FROM eventos)
), segmentos AS (SELECT DISTINCT segmento FROM eventos), agregado AS (
 SELECT mes,segmento,SUM(nuevos) entradas_new,SUM(ganados) cierres_won,SUM(pagadores) nuevos_pagadores FROM eventos GROUP BY mes,segmento
), completo AS (
 SELECT m.mes,s.segmento,COALESCE(a.entradas_new,0) entradas_new,COALESCE(a.cierres_won,0) cierres_won,COALESCE(a.nuevos_pagadores,0) nuevos_pagadores
 FROM meses m CROSS JOIN segmentos s LEFT JOIN agregado a ON a.mes=m.mes AND a.segmento=s.segmento
), anterior AS (
 SELECT *,LAG(entradas_new) OVER(PARTITION BY segmento ORDER BY mes) new_anterior,
 LAG(cierres_won) OVER(PARTITION BY segmento ORDER BY mes) won_anterior,
 LAG(nuevos_pagadores) OVER(PARTITION BY segmento ORDER BY mes) pagadores_anterior FROM completo
)
SELECT *,100.0*(entradas_new-new_anterior)/NULLIF(new_anterior,0) crecimiento_new_pct,
 100.0*(cierres_won-won_anterior)/NULLIF(won_anterior,0) crecimiento_won_pct,
 100.0*(nuevos_pagadores-pagadores_anterior)/NULLIF(pagadores_anterior,0) crecimiento_pagadores_pct
FROM anterior ORDER BY segmento,mes;
