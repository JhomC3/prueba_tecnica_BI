# Datos del proyecto

- `sinteticos/cro/{referencia,conversion,demora}/`: cuentas, etapas, registros y ganados en CSV.
- `bases/cro/{referencia,conversion,demora}/modelo.sqlite`: las mismas tablas y vista de ganados en SQLite.
- Originales del reto: `../inputs/`. Resultados: `../resultados/cro/`.

Regenerar desde la raíz con `python3 scripts/cro_demo.py`. Son escenarios de demostración, no hechos de Finora. Los datos generados se excluyen de Git; se versionan código, SQL, pruebas y documentación.

Versión 2 CRO: cuatro tablas de negocio (`dim_cuentas`, `fact_etapas`, `interacciones`, `pagos`), catálogo `dim_etapas` y salida derivada `ganados`. Definiciones y controles en [modelo CRO](../docs/datos/modelo-cro-demo.md).
