-- Una fila por cliente, mes y grupo. Importes enteros en centavos de UM.
-- Movimientos de cada componente se calculan con la convención cantidad -> tarifa.
CREATE VIEW puente_mensual AS
SELECT grupo, mes,
       SUM(neto_anterior) AS saldo_inicial,
       SUM(neto) AS saldo_final,
       SUM(subyacente) AS subyacente,
       SUM(pricing) AS pricing,
       SUM(delta_descuento) AS delta_descuento,
       SUM(neto-neto_anterior) AS delta_neto,
       SUM(neto-neto_anterior-subyacente-pricing+delta_descuento) AS residuo
FROM movimientos GROUP BY grupo, mes;
