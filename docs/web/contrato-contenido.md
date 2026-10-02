# Contrato común de contenido (W03, revisado: figuras configurables + sync)

Los textos viven en `src/content/*.json`. Las vistas (`src/views/*.js`) solo renderizan; no contienen texto analítico ni rutas fijas de figuras.

## Caso (`cro.json`, `cfo.json`)

| Campo | Tipo | Regla |
| --- | --- | --- |
| `id` | `cro` \| `cfo` | Identificador estable |
| `titulo` | texto | Título del caso |
| `decisor` | texto | Quién decide (CRO / CFO) |
| `estado` | `disponible` \| `en_revision` \| `pendiente` | Estado del caso. Ambos casos: `en_revision` (formulación en curso, sin diagnóstico cerrado) |
| `requerimiento_original` | `{ texto, fuente }` | Cita literal del reto; `fuente` = referencia documental |
| `componentes` | 13 objetos en orden 1–13 | Orden del marco registrado |
| `componentes[].numero` | 1–13 | — |
| `componentes[].nombre` | texto | Nombre del marco (p. ej. «Quién decide») |
| `componentes[].pregunta_marco` | texto | Pregunta literal del marco |
| `componentes[].respuesta` | texto \| null | Respuesta breve o null si pendiente |
| `componentes[].estado` | `disponible` \| `en_revision` \| `pendiente` | — |
| `componentes[].evidencia` | `{ tipo, referencia, nota }` \| null | `tipo`: `datos_reto` \| `datos_sinteticos` \| `propuesta` \| `hipotesis`; `referencia`: ruta o documento |
| `preguntas` | array | Preguntas analíticas del candidato (literales) |
| `preguntas[].id` | texto (`cro-3.1`…) | — |
| `preguntas[].pregunta` | texto | Redacción literal registrada |
| `preguntas[].que_medimos` | texto \| null | Estándar 3.1; null = pendiente |
| `preguntas[].alcance` | texto \| null | Periodo/segmento parcial explícito |
| `preguntas[].metrica_formula` | texto \| null | Definición/fórmula |
| `preguntas[].datos` | texto \| null | Fuente y campos |
| `preguntas[].calculo` | `{ descripcion, fuente }` \| null | Cálculo plegado (`<details>`); null si no hay cálculo mostrado |
| `preguntas[].figura` | objeto figura \| null | Solo figuras acordadas; en otro caso null + `figura_pendiente: true` |
| `preguntas[].estado` | `disponible` \| `en_revision` \| `pendiente` | — |
| `preguntas[].lectura` | texto \| null | Lectura descriptiva breve con evidencia, sin causalidad |

Reglas: una pregunta sin `que_medimos` no se presenta como respondida; un `null` se renderiza como bloque «Pendiente»; ningún pendiente se etiqueta `disponible`.

## Figura configurable (sin tocar el renderizador)

`preguntas[].figura` admite nuevas figuras y tablas solo editando el JSON:

```json
{
  "id": "new-serie",
  "titulo": "Entradas a New por mes",
  "datos_src": "data/new_serie_referencia.json",
  "iframe_src": "charts/01_new_tendencia.html",
  "tabla": {
    "caption": "Entradas a New por mes de entrada (misma serie de la figura)",
    "columnas": [
      {"campo": "mes", "etiqueta": "Mes"},
      {"campo": "entradas_new", "etiqueta": "Entradas a New", "formato": "entero"},
      {"campo": "variacion_mensual_pct", "etiqueta": "Variación mensual", "formato": "pct1", "nulo": "Sin comparación anterior"}
    ]
  }
}
```

- `id`: estable; `titulo`: figcaption.
- `datos_src` (opcional): ruta bajo `public/` a un JSON con `{ valores|filas: [...], nota_etiqueta?, contexto?, fuente?, periodo?, poblacion?, unidad?, escenario? }`. El renderizador muestra los metadatos presentes sin fijarlos en código.
- `iframe_src` (opcional): ruta bajo `public/` a la figura HTML existente (carga diferida, con título accesible).
- `tabla` (opcional): `caption` + `columnas: [{ campo, etiqueta, formato?: texto|entero|pct1, nulo? }]`. `pct1` formatea `34.6` como `34,6 %`? No: muestra `34.6 %` con un decimal; `nulo` es el texto cuando el valor es null (p. ej. primer mes). También admite `tabla.filas` inline cuando no hay `datos_src`.
- Combinaciones válidas: solo iframe, solo tabla, o ambas. Sin `datos_src` ni `filas`, la tabla queda vacía.

El renderizador (`src/views/case.js: renderFigura`) no contiene ids, rutas ni columnas fijas. `scripts/check-coherence.mjs` valida que toda figura tenga `id/titulo` y que su tabla tenga `columnas` con `campo/etiqueta`.

## Resumen (`resumen.json`)

`{ titulo, descripcion, casos: [{ caso_id, pregunta, avance, siguiente }], metodo, datos, proceso }`. Solo avance real; sin hallazgos inventados.

## Vocabulario (`src/vocabulary.json`)

Fuente única de etiquetas: estados (`Disponible`, `En revisión`, `Pendiente`), tipos de evidencia (`Datos del reto`, `Datos sintéticos`, `Propuesta`, `Hipótesis`) y términos obligatorios (`importe observado`, `pagadores observados`, `modelo propuesto`, `ejemplo ilustrativo`, `hipótesis`, `pendiente de información`). `scripts/check-coherence.mjs` falla si el contenido usa etiquetas fuera del vocabulario o términos prohibidos (`MRR contractual`, `churn` aplicado a ceros, `adquisición demostrada` sin supuesto).

## Serie tabular (`public/data/new_serie_referencia.json`)

Generada por `scripts/export_web.py` desde `resultados/cro/metricas/referencia/demanda.csv` (segmento total). `{ escenario, periodo, unidad, poblacion, fuente, nota_etiqueta, contexto, valores: [{ mes, entradas_new, variacion_mensual_pct | null }] }`. La variación es la columna `crecimiento_new_pct` ya calculada, redondeada a un decimal; el primer mes es `null` («Sin comparación anterior»). `poblacion` es «cuentas que entraron por New, por mes de entrada» (sin ventana de conversión). Meses y valores no están fijados en código: se validan por estructura y contra el manifest (`n_meses`, `meses`, hashes).

## Sincronización (`src/content` → `public/content`)

`src/content/*.json` es la fuente editable. `public/content/*.json` es la copia servida. `scripts/sync-content.mjs` copia y actualiza el manifest; `predev` y `prebuild` lo ejecutan automáticamente, así que `npm run build` siempre incorpora el contenido actualizado sin exportación manual. `scripts/export_web.py` además sincroniza figura, serie y contenidos cuando hay acceso a la fuente original.
