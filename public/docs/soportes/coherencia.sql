-- Una cuenta, una cohorte (primera entrada a New), un reloj para todo el funnel.
WITH primera_new AS (
 SELECT id_cuenta, MIN(entrada) fecha_new
 FROM fact_etapas WHERE id_etapa='New' GROUP BY id_cuenta
), cohortes AS (
 SELECT c.id_cuenta,c.canal,n.fecha_new
 FROM dim_cuentas c JOIN primera_new n USING(id_cuenta)
 WHERE c.tipo_entrada='New' AND n.fecha_new<=:corte
), ventanas(dias) AS (VALUES(30),(60),(90))
SELECT c.id_cuenta,c.canal,c.fecha_new,substr(c.fecha_new,1,7) mes,
 v.dias ventana,date(c.fecha_new,'+'||v.dias||' days') limite,
 CASE WHEN julianday(:corte)-julianday(c.fecha_new)>=v.dias THEN 1 ELSE 0 END maduro,
 MAX(d.orden) max_orden,
 MAX(CASE WHEN f.id_etapa='Won' AND f.estado='ganado' THEN 1 ELSE 0 END) won,
 GROUP_CONCAT(DISTINCT f.id_etapa) etapas_visitadas
FROM cohortes c CROSS JOIN ventanas v
LEFT JOIN fact_etapas f ON f.id_cuenta=c.id_cuenta
 AND f.entrada>=c.fecha_new AND f.entrada<=:corte
 AND julianday(f.entrada)-julianday(c.fecha_new)<=v.dias
LEFT JOIN dim_etapas d ON d.id_etapa=f.id_etapa
GROUP BY c.id_cuenta,c.canal,c.fecha_new,v.dias;
