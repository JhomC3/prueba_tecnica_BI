# Inspección visible de fuentes

**2026-09-30, última ejecución 13:43 Colombia.** Ejecutó Codex; revisión del candidato pendiente. Esta ejecución reconstruye parte del inventario previo; no demuestra supervisión humana retrospectiva.

## Qué se ejecutó

[Script](../../scripts/inspect_sources.py): lectura CSV UTF-8 con coma, conteos, campos vacíos, repetidos, claves, muestras localizables, SHA-256 antes/después y contraste con el perfil preliminar. Decimal para importes originales; sin conversión de unidades, limpieza ni joins.

Desde la raíz del proyecto, último comando utilizado (Python 3.13.3; también comprobado con el runtime 3.12.14):

```bash
python3 scripts/inspect_sources.py
```

Resultados regenerables: [informe HTML](../../artifacts/inspeccion/informe.html), [detalle JSON](../../artifacts/inspeccion/resultado.json), [registro de ejecución](../../artifacts/inspeccion/ejecucion.txt). Permanecen fuera de Git; el script y esta síntesis se versionan.

## Resultado observado

| Fuente | Registros sin encabezado | Campos | Vacíos completos |
| --- | ---: | ---: | ---: |
| Transactions | 66.674 | 3 | 0 |
| Industry | 1.962 | 2 | 1 |
| S&M_spend | 34 | 8 | 0 |

22 controles coinciden con el perfil anterior. Las tres fuentes conservaron sus bytes. Tres pruebas pasaron: BOM/comillas/vacíos, registros defectuosos/importes no finitos y escape HTML. Esto no valida significado comercial ni ausencia de todo error posible.

**Conciliación con sistema de origen: pendiente.** Solo recibimos CSV; no contrastamos contra CRM, facturación u otro sistema fuente. El perfil anterior y los hashes no sustituyen ese control.

## Qué revisar tú

1. Contrastar muestras con el registro/línea indicado en el CSV original.
2. Revisar las reglas del script y los controles desplegables.
3. Señalar correcciones o confirmar qué verificaste; solo entonces registrar esa revisión humana.
