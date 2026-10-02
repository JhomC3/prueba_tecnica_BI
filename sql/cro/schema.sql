PRAGMA foreign_keys = ON;
CREATE TABLE dim_cuentas (
  id_cuenta TEXT PRIMARY KEY,
  canal TEXT NOT NULL,
  industria TEXT NOT NULL,
  tipo_entrada TEXT NOT NULL CHECK(tipo_entrada IN ('New','SQL','Producto')),
  fecha_captacion TEXT,
  campana TEXT,
  producto TEXT,
  region TEXT,
  perfil TEXT,
  responsable TEXT,
  fecha_asignacion TEXT,
  ajuste_perfil INTEGER CHECK(ajuste_perfil IN (0,1)),
  necesidad INTEGER CHECK(necesidad IN (0,1)),
  intencion INTEGER CHECK(intencion IN (0,1)),
  fecha_evaluacion TEXT,
  version_criterios TEXT,
  calificado INTEGER CHECK(calificado IN (0,1)),
  motivo_descalificacion TEXT,
  inicio_historia_pagos TEXT,
  pagador_previo INTEGER CHECK(pagador_previo IN (0,1))
);
CREATE TABLE dim_etapas (
  id_etapa TEXT PRIMARY KEY,
  orden INTEGER NOT NULL UNIQUE,
  siguiente TEXT REFERENCES dim_etapas(id_etapa)
);
CREATE TABLE fact_etapas (
  id_registro TEXT PRIMARY KEY,
  id_cuenta TEXT NOT NULL REFERENCES dim_cuentas(id_cuenta),
  id_etapa TEXT NOT NULL REFERENCES dim_etapas(id_etapa),
  entrada TEXT NOT NULL,
  salida TEXT,
  estado TEXT NOT NULL CHECK(estado IN ('avance','perdido','abierto','ganado')),
  id_etapa_destino TEXT REFERENCES dim_etapas(id_etapa),
  motivo_perdida TEXT,
  responsable_etapa TEXT,
  fecha_asignacion_etapa TEXT,
  CHECK(salida IS NULL OR salida >= entrada)
);

-- Vista derivada: no es otra fuente ni requiere generar cierres independientes.
-- En esta demo cuenta = oportunidad; en producción comprobar historia previa.
CREATE VIEW vw_ganados AS
WITH primera_entrada AS (
  SELECT id_cuenta, MIN(entrada) AS fecha_entrada_inicial
  FROM fact_etapas GROUP BY id_cuenta
), primer_won AS (
  SELECT id_cuenta, MIN(entrada) AS fecha_won
  FROM fact_etapas WHERE id_etapa='Won' AND estado='ganado'
  GROUP BY id_cuenta
)
SELECT c.id_cuenta, c.canal, c.industria, c.tipo_entrada,
       e.fecha_entrada_inicial, w.fecha_won,
       CAST(julianday(w.fecha_won)-julianday(e.fecha_entrada_inicial) AS INTEGER) AS dias_hasta_won
FROM primer_won w JOIN dim_cuentas c USING(id_cuenta)
JOIN primera_entrada e USING(id_cuenta);

CREATE TABLE interacciones (
 id_interaccion TEXT PRIMARY KEY,
 id_cuenta TEXT NOT NULL REFERENCES dim_cuentas(id_cuenta),
 id_registro TEXT NOT NULL REFERENCES fact_etapas(id_registro),
 fecha TEXT NOT NULL,
 tipo TEXT NOT NULL CHECK(tipo IN ('llamada','correo')),
 resultado TEXT NOT NULL CHECK(resultado IN ('sin_respuesta','intercambio_efectivo')),
 responsable TEXT NOT NULL
);
CREATE TABLE pagos (
 id_pago TEXT PRIMARY KEY,
 id_cuenta TEXT NOT NULL REFERENCES dim_cuentas(id_cuenta),
 fecha_pago TEXT NOT NULL,
 estado_pago TEXT NOT NULL CHECK(estado_pago IN ('valido','fallido'))
);
-- Una cuenta/etapa: primera entrada y resultado de la última visita observada.
-- La generación contiene reingresos inmediatos; si hay intervalos fuera de etapa,
-- duración de visitas se obtiene sumando las visitas, separada del tiempo calendario.
CREATE VIEW vw_etapas_cuenta AS
WITH ordenados AS (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY id_cuenta,id_etapa ORDER BY entrada DESC,id_registro DESC) rn
 FROM fact_etapas
), primera AS (
 SELECT id_cuenta,id_etapa,MIN(entrada) entrada,COUNT(*) visitas
 FROM fact_etapas GROUP BY id_cuenta,id_etapa
)
SELECT o.id_registro,p.id_cuenta,p.id_etapa,p.entrada,o.salida,o.estado,o.id_etapa_destino,p.visitas
FROM primera p JOIN ordenados o USING(id_cuenta,id_etapa) WHERE o.rn=1;
CREATE VIEW vw_primer_pago AS
SELECT p.id_cuenta, MIN(p.fecha_pago) fecha_primer_pago
FROM pagos p WHERE p.estado_pago='valido' GROUP BY p.id_cuenta;
CREATE INDEX idx_etapas_cuenta ON fact_etapas(id_cuenta,entrada);
CREATE INDEX idx_interacciones_visita ON interacciones(id_registro,fecha);
CREATE INDEX idx_pagos_cuenta ON pagos(id_cuenta,fecha_pago);
