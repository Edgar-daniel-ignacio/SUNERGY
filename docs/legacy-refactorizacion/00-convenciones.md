---
title: Convenciones del sistema legacy
role: Vocabulario y convenciones recuperados por el autor, con correcciones auditadas pendientes de revisión.
retrieve_when: Interpretar nombres, unidades, estados o índices de los archivos legacy.
read_scope: La convención y sus productores o consumidores citados.
authority: Investigación estática del autor; no demuestra ejecución, paridad ni validez científica.
verify: Contrastar símbolos y condiciones con legacy; consultar la cobertura canónica para capturas e implementación actuales.
---

# 00 — Convenciones, unidades y nombres

> Sin esta página, la mitad de los defectos del sistema parecen errores distintos y son el mismo
> problema de vocabulario. Convenciones contrastadas estáticamente; sus condiciones de aplicación
> no sustituyen una captura ni una validación científica.

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
| caracterización meteorológica | `Clima_Car.py` | 40 |
| **sin llamadas desde el panel trazado** | `Parametros_Electricos.py` | 240 |
| **sin llamadas desde el panel trazado** | `CurvaIV.py` | 99 |

`Parametros_Electricos` y `CurvaIV` se importan en el panel (`L4` y `L7`), sin llamadas a sus
alias `pe` e `iv` en ese fichero. Sus ecuaciones no prueban el comportamiento de los motores
activos en `Input_File_DIV_Mac_Informe.py`. No se ha descartado todo consumidor externo posible. #to-review

---

## 2. Las cinco dimensiones del problema

Estas cinco decisiones explican la repetición de ramas. Los 84 `if Metodo ==` pertenecen al
callback `electric_parameters@4182`; el conteo no acredita todas las combinaciones posibles.

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

`use_ndh` usa un tercer nombre, `Tiempo`, y devuelve `None` (`panel 1105-1115`): no publica
los datos que relee, aunque sí realiza I/O y puede fallar al leerlos. #to-review

---

## 4. Unidades y rejillas

- Temperatura en **°C**; irradiancia en **W/m²**; corriente en **A**; tensión en **V**; potencia en **W**.
- El año se trocea en cuatro resoluciones, y las longitudes son las claves del diccionario `NDH`:
  **8760** (1 h) · **17520** (30 min) · **35040** (15 min) · **105120** (5 min).
- `Clima` conserva longitudes distintas creando nuevas claves (`Primer_Funcion_Clima.py:118-121,
  173-175`). Son consumidores posteriores —posición solar, Sandia y escritores/tablas— los que
  filtran las cuatro longitudes reconocidas. La pérdida depende del consumidor, no de la descarga. #to-review
- El índice temporal es `DatetimeIndex` con zona horaria (`Etc/GMT±N` en la ruta de pvlib).

---

## 5. Los rótulos que mienten

| Rótulo en pantalla | Lo que realmente contiene | Dónde |
|---|---|---|
| `"Temperatura minima"` / `"Temperatura Minima"` en `resume_IV` | condiciones elegidas por **voltaje máximo**, no temperatura mínima | 10 rótulos con `minima` y uno con `Minima` (`4759`); llega a la leyenda de `IV_R`. |
| `"Año … [Horas: …]"` | formato de 1 módulo | `4245`, `1789` |
| `"Year … [Hours: …]"` | formato de 2 módulos; **no coincide** con las opciones del desplegable | `5428`, `2477` |
| `"Voc"` en la tabla de Feinman | es **`Vmax_F`**, no `Voc_F` (`3128-3129`) | `resume_df` |

La discrepancia `Año`/`Year` afecta las comparaciones de etiquetas. El resultado concreto
depende del filtro y la rama: varios filtros de dos módulos comparan caracteres (B-03), por lo
que tampoco se puede deducir una pantalla vacía universal sin ejecutar el caso. #to-review

---

## 6. Variables globales de módulo

Once en el panel (`Pot`, `Vm`, `Im`, `Voc`, `Isc`, `alpha`, `beta`, `gamma`, `Numero_celda`,
`Tempref`, `Tc`, en `GIU_Final_Presetacion.py:92-102`) y cinco mutables en el módulo (`tables`,
`l`, `name`, `tablespe`, `Tabla_Promedio_s`). Las globales del panel **no son un defecto**: son los
valores por defecto del módulo de prueba, y por eso la línea `678` de `toggle_inputs` no falla
(aunque no haga nada útil).

---

## 7. Estados de una función

#to-review — Las etiquetas viva, muerta y rota ahora delimitan análisis estático, no ejecución observada.

| Estado | Significado | Cómo se reconoce |
|---|---|---|
| **viva** | alcanzable en el grafo estático del panel | 23 callbacks o 22 factorías del layout; no demuestra que la rama se ejecute con datos válidos. |
| **muerta** | sin camino desde las raíces analizadas | alcanzabilidad estática = 0 en estos dos ficheros; comprobar consumidores externos antes de borrar. |
| **muerta-hoy** | existe y es coherente, pero ningún llamador puede alcanzarla con los argumentos actuales | p. ej. las 5 ramas de `df_creator_1` |
| **rota** | anotación original de defecto o riesgo de fallo | ver condiciones y límites en `06-lo-que-esta-roto.md`; no equivale a fallo observado. |
| **nunca conectada** | escrita y nunca invocada | `df_creator_PE`, `Year_tabla`, `minimos2`, `minimos_s2`, `IV_CI_Corr`, `get_corrected_IV_P2` |
