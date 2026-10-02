-- Una fila de origen = una entrada de una cuenta a una etapa.
-- Ventana ilustrativa parametrizada; no es un SLA de atención.
-- El filtro se aplica antes de agrupar: no se promedian porcentajes de segmentos.
WITH observados AS (
  SELECT f.*, c.canal, c.tipo_entrada,
    julianday(:corte)-julianday(f.entrada) AS antiguedad,
    CASE WHEN f.salida <= :corte THEN julianday(f.salida)-julianday(f.entrada) END AS duracion,
    CASE WHEN f.id_etapa <> 'Won' AND
      julianday(:corte)-julianday(f.entrada) >= :ventana THEN 1 ELSE 0 END AS elegible,
    CASE WHEN f.salida <= :corte THEN f.estado
         WHEN f.estado='ganado' THEN 'ganado' ELSE 'abierto' END AS estado_corte
  FROM vw_etapas_cuenta f JOIN dim_cuentas c USING(id_cuenta)
  WHERE f.entrada <= :corte
    AND (:canal='' OR c.canal=:canal)
    AND (:tipo='' OR c.tipo_entrada=:tipo)
), calculados AS (
  SELECT *,
    CASE WHEN elegible=1 AND duracion <= :ventana AND estado_corte='avance' AND id_etapa_destino=(SELECT siguiente FROM dim_etapas d WHERE d.id_etapa=observados.id_etapa)
      THEN 1 ELSE 0 END AS avance_ventana,
    CASE WHEN elegible=1 AND duracion <= :ventana AND estado_corte='perdido'
      THEN 1 ELSE 0 END AS perdida_ventana
  FROM observados
)
SELECT id_etapa AS etapa, __GRUPO__ AS grupo,
  COUNT(*) AS entradas,
  SUM(elegible) AS elegibles,
  SUM(avance_ventana) AS avances,
  SUM(perdida_ventana) AS perdidos,
  SUM(elegible)-SUM(avance_ventana)-SUM(perdida_ventana) AS sin_avance,
  100.0*SUM(avance_ventana)/NULLIF(SUM(elegible),0) AS conversion,
  SUM(CASE WHEN estado_corte='abierto' THEN 1 ELSE 0 END) AS abiertos,
  SUM(CASE WHEN duracion IS NOT NULL AND id_etapa<>'Won' THEN 1 ELSE 0 END) AS cerrados,
  mediana(CASE WHEN id_etapa<>'Won' THEN duracion END) AS mediana_cerrados,
  p90(CASE WHEN id_etapa<>'Won' THEN duracion END) AS p90_cerrados,
  mediana(CASE WHEN estado_corte='abierto' THEN antiguedad END) AS mediana_abiertos,
  p90(CASE WHEN estado_corte='abierto' THEN antiguedad END) AS p90_abiertos
FROM calculados
__FILTRO_PERIODO__
GROUP BY id_etapa, grupo
ORDER BY (SELECT orden FROM dim_etapas s WHERE s.id_etapa=calculados.id_etapa), grupo;
