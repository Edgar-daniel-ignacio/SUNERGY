# 00 — Convenciones, unidades y nombres

> Sin esta página, la mitad de los defectos del sistema parecen errores distintos y son el mismo
> problema de vocabulario. Borradores: **verificado** salvo donde se marque.

---

## 1. Los ficheros, y por qué los nombres no coinciden

El código importa `Input_File_DIV_Mac_Informe as input`, así que la documentación antigua habla
de «input» para referirse a ese módulo. Son el mismo objeto.

| Nombre en este informe | Fichero real en `legacy/` | Líneas |
|---|---|---|
| **el panel** | `GIU_Final_Presetacion.py` | 6.043 |
| **el módulo** | `Input_File_DIV_Mac_Informe.py` | 8.853 |
| clima | `Primer_Funcion_Clima.py` | 183 |
| radiación | `Posicion_Solar.py` | 204 |
| caracterización meteorológica | `Clima_Car.py` | 39 |
| **muerto** | `Parametros_Electricos.py` | 240 |
| **muerto** | `CurvaIV.py` | 99 |

`Parametros_Electricos` y `CurvaIV` se importan en el panel (`L4` y `L7`) y **no se llaman nunca**:
son una generación anterior del mismo cálculo, copiada después dentro del módulo. Cualquier
afirmación sobre «el modelo de un diodo» que se apoye en ellos está describiendo código muerto.

---

## 2. Las cinco dimensiones del problema

Todo el sistema es el producto de estas cinco decisiones. Entenderlo es entender por qué hay 84
bloques de cálculo.

| Dimensión | Valores | Dónde vive |
|---|---|---|
| **Modelos térmicos** (`Seleccion`) | `[1]` Feinman · `[2]` Sandia · `[3]` NOCT, y sus 4 combinaciones | `checklist-input` |
| **Método de curva** (`Metodo`) | `PE` puntos estadísticos · `VE` valores específicos · `CI` comparación con medición | `IV-Method` |
| **Origen de la placa** (`Method`) | `SELEC` prueba · `INSERT` manual · `CEC` catálogo | `selection-dropdown` |
| **Módulos** | 1 o 2 | `Table_modulos_base` |
| **Corrección** | sí (`correction == [1]`) o no | `correction` |

`1` = Feinman, `2` = Sandia, `3` = NOCT. `[1, 3]` significa «Feinman y NOCT activos a la vez».

---

## 3. Los nombres de índice del CSV (aquí se pierden las tardes)

El sistema usa el **directorio de trabajo como bus de datos**. Los CSV llevan su índice como
columna, y el nombre de esa columna **no lo pone quien escribe**: lo hereda del DataFrame.

| Fichero | Columna de índice | Por qué | Quién la lee |
|---|---|---|---|
| `g_{año}_{n}.csv` | vacía → `Unnamed: 0` | viene de pvlib, cuyo índice no tiene nombre | `df_creator` |
| `PE_{año}_{n}.csv` | `Time` | viene de `df_creator`, que renombra el índice a `['Time']` | `df_creator_1` rama `[1]` |
| `PE2_{año}_{n}.csv` | `Time` | igual | igual |
| `Uploaded_.xlsx` | sin índice (`index=False`) | lo escribe `guardar_archivo` | `IV_CI`, `IV_CI_cor`, `IV_sim` |

Consecuencia práctica: **si cambias quién produce un CSV, cambias el nombre de su índice.** Y
`df_creator_1` tiene cinco ramas que esperan `Unnamed: 0` en un fichero que siempre trae `Time`;
hoy no se alcanzan porque los 19 puntos de llamada pasan `[1]` cableado.

`use_ndh` usa un tercer nombre, `Tiempo`, y no devuelve nada. Es código sin efecto.

---

## 4. Unidades y rejillas

- Temperatura en **°C**; irradiancia en **W/m²**; corriente en **A**; tensión en **V**; potencia en **W**.
- El año se trocea en cuatro resoluciones, y las longitudes son las claves del diccionario `NDH`:
  **8760** (1 h) · **17520** (30 min) · **35040** (15 min) · **105120** (5 min).
- El código filtra por `len(df) == n`, no por la resolución pedida: si un año trae un número
  distinto de filas (bisiesto, hueco de datos), **no entra en ninguna rejilla y desaparece sin aviso**.
- El índice temporal es `DatetimeIndex` con zona horaria (`Etc/GMT±N` en la ruta de pvlib).

---

## 5. Los rótulos que mienten

| Rótulo en pantalla | Lo que realmente contiene | Dónde |
|---|---|---|
| `"Temperatura minima"` (fila 2 de las tablas de extremos) | valores de **voltaje** | 10 sitios; llega a la leyenda de `IV_R` |
| `"Año … [Horas: …]"` | formato de 1 módulo | `4245`, `1789` |
| `"Year … [Hours: …]"` | formato de 2 módulos; **no coincide** con las opciones del desplegable | `5428`, `2477` |
| `"Voc"` en la tabla de Feinman | es **`Vmax_F`**, no `Voc_F` (`3128-3129`) | `resume_df` |

El tercero no es cosmético: el filtro compara etiquetas, y con el idioma cambiado la pantalla
queda vacía sin lanzar error.

---

## 6. Variables globales de módulo

Once en el panel (`Pot`, `Vm`, `Im`, `Voc`, `Isc`, `alpha`, `beta`, `gamma`, `Numero_celda`,
`Tempref`, `Tc`, en `GIU_Final_Presetacion.py:92-102`) y cinco mutables en el módulo (`tables`,
`l`, `name`, `tablespe`, `Tabla_Promedio_s`). Las globales del panel **no son un defecto**: son los
valores por defecto del módulo de prueba, y por eso la línea `678` de `toggle_inputs` no falla
(aunque no haga nada útil).

---

## 7. Estados de una función

| Estado | Significado | Cómo se reconoce |
|---|---|---|
| **viva** | se ejecuta en algún flujo real | alcanzable desde los 23 callbacks o el layout |
| **muerta** | nadie la llama | alcanzabilidad = 0 |
| **muerta-hoy** | existe y es coherente, pero ningún llamador puede alcanzarla con los argumentos actuales | p. ej. las 5 ramas de `df_creator_1` |
| **rota** | se ejecuta y falla o corrompe el dato | ver `06-lo-que-esta-roto.md` |
| **nunca conectada** | escrita y nunca invocada | `df_creator_PE`, `Year_tabla`, `minimos2`, `minimos_s2`, `IV_CI_Corr`, `get_corrected_IV_P2` |
