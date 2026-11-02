# 03 — Contratos: qué entra y qué sale en cada frontera

> Las fronteras donde el sistema cambia de manos. Cada contrato lleva un identificador `C-###`
> para que se pueda citar sin ambigüedad. **medido** salvo donde se indique.

Un contrato aquí no es una promesa del código: es **lo que el código asume**. Donde la asunción no
está declarada en ningún sitio, se dice.

---

## C-01 · `NDH` — el diccionario de clima (en memoria)

| Campo | Valor |
|---|---|
| Productor | `Primer_Funcion_Clima.Clima` (`L64-183`), vía callback `clima` |
| Consumidores | `Clima_Car.clc`, `Posicion_Solar.Solar_pos(_e)`, `Temperature_*`, `table_e`, `TMY`, `creador_csv_clima` |
| Claves | la **longitud** de la serie como número: `8760.0`, `17520.0`, `35040.0`, `105120.0` |
| Valores | lista de DataFrames, índice `DatetimeIndex` con zona horaria |
| Columnas mínimas | `temp_air`, `wind_speed`, `ghi`, `dni`, `dhi`, `albedo`, `Year`, `Month`, `Day`, `Hour`, `Minute` |
| Columnas añadidas | `Poa_global`, `Poa_direct`, `Poa_diffuse`, `Poa_sky_diffuse`, `Poa_ground_diffuse` (S2) y `TFeinman`, `Tsandia`, `NOCT` (S3) |

**Lo que no garantiza.** Que el número de filas coincida con su clave: si no coincide, el DataFrame
se queda fuera de todos los bucles `if len(df) == n` y desaparece **sin aviso**. Y el nombre de su
índice es `None` (pvlib no lo nombra), lo que determina la cabecera del CSV siguiente.

---

## C-02 · `g_{año}_{n}.csv` — el bus climático

| Campo | Valor |
|---|---|
| Productor | `creador_csv_clima` (`módulo 828-855`) |
| Consumidores | `df_creator` (`1059-1129`), `use_ndh` (panel `1105-1116`) |
| Nombre | `g_{Year}_{n}.csv`, con `n` en `[8760, 17520, 35040, 105120]` |
| Índice | **cabecera vacía** → `pd.read_csv` la lee como `Unnamed: 0` |
| `index=` | `True` |
| Destructivo | borra `g_*.csv` antes de escribir |

**Riesgo `R-01`:** en un directorio de trabajo compartido, cualquier corrida borra los ficheros de
otra. Dos pestañas abiertas = `FileNotFoundError` a media corrida.

---

## C-03 · `PE_{año}_{n}.csv` y `PE2_{año}_{n}.csv` — el bus eléctrico

| Campo | Valor |
|---|---|
| Productor | `creador_csv_PE` (`859-884`) y `creador_csv_PE2` (`886-911`) |
| Consumidores | `df_creator_1` (`1207-1287`), 19 llamadas en 5 callbacks |
| Nombre | `PE_{Year}_{n}.csv` / `PE2_{Year}_{n}.csv` |
| Índice | **`Time`** — heredado del DataFrame que produce el motor `PE*` |
| Columnas | `Poa_global`, `Year`, `Month` + por modelo activo: `Gamma_*`, `Isc0_*`, `Voc_*`, `Imax_*`, `Vmax_*`, `Pmax_*`, `T_*` |
| Sufijos | `_F` Feinman · `_S` Sandia · `_NOCT` |

**Por qué el índice se llama `Time` y no `Unnamed: 0`.** Porque este DataFrame sí pasó por
`df_creator`, que hace `l.index.names = ['Time']` (`1067`). No es una decisión del escritor: es una
consecuencia de la procedencia.

**Riesgo `R-02`:** `df_creator_1` tiene cinco ramas que buscan `Unnamed: 0` en este fichero. Nunca
se ejecutan porque las 19 llamadas pasan `[1]` cableado. Si un refactor pasa la `Seleccion` real,
esas ramas lanzan `KeyError`.

---

## C-04 · `dcc.Store` — el bus de estado del navegador

| Store | Escribe | Lee | Transporta |
|---|---|---|---|
| `store-ndh` | `clima@853` | `use_ndh@1105`, `electric_parameters@1148`, `electric_parameters@4182` | lista de rutas `g_*.csv` |
| `Datos_PE` | `electric_parameters@1148` | 7 callbacks | lista de rutas `PE_*.csv` |
| `Datos_PE2` | `electric_parameters@1148` | los mismos 7 | lista de rutas `PE2_*.csv` |
| `Database1` / `Database2` | `render_content@969` | `electric_parameters@1148`, `IV_Corrct@3791`, `Tabla_R_Boots@4045`, `electric_parameters@4182` | 11 parámetros CEC del módulo |
| `Tabla_Info`, `Tabla_Info_m`, `Tabla_Info_s` | `IV_Corrct@3791` | `Tabla_select@3981` | dicts `.to_dict()` de las tablas |
| `Tablarm`, `Tablars` | `IV_Corrct@3791` | `Tabla_R_Boots@4045` | curvas para el bootstrap |
| `Prueba` | `toggle_inputs@675` | **nadie** | diccionario de la placa de prueba |
| `selected-rows-store` | **nadie** | **nadie** | nada |

**Observación de diseño:** ningún store transporta datos, solo **nombres de fichero** o parámetros
pequeños. El estado real vive en el disco, y el navegador solo guarda el índice de dónde mirar.

---

## C-05 · `Uploaded_.xlsx` — el libro de mediciones

| Campo | Valor |
|---|---|
| Productor | `guardar_archivo` (`módulo 962-980`), invocado desde `parse_contents` (panel `5976-6026`) |
| Consumidores | `IV_CI`, `IV_CI2`, `IV_CI_cor`, `IV_sim`, `IV_Corrct`, `electric_parameters@4182` |
| Escritura | `index=False`, una hoja por hoja del libro subido |
| Hojas | `IV1…IVn` con columnas `Volts`, `Amps`, `Watts`, **y `Info` al final** |
| Hoja `Info` | `CurveID, Normalized, Date/Time, Power, Isc, Voc, Ipeak, Vpeak, Fill Factor, Irrad1, Temp1, Temp2` |
| Columnas usadas | **4 de 12**: `Voc`, `Irrad1`, `Temp1`, `Temp2` |

**Riesgo `R-03` (el más silencioso del sistema):** el código lee las curvas **por posición**
(`sheet_name=i`). Si `Info` no es la última hoja, la curva 1 pasa a ser la hoja `Info` y todo se
desplaza sin lanzar un error.

**Riesgo `R-04`:** nada verifica que el libro corresponda al módulo simulado. `Power`, `Isc`, `Voc`
y `Fill Factor` están en el fichero y se descartan: son justo los que permitirían detectar que se
está comparando un módulo de 227 W con una simulación de 570 W.

**Nota sobre `Uploaded_.csv`:** 32 lecturas esperan un `.csv` cuyo escritor (`creador_uplouded`,
`módulo 913-930`) está **comentado**. Todo el camino «comparación sin corrección» falla con
`FileNotFoundError` salvo la única rama que lee el `.xlsx` (panel `4289`), que además **solo lee la
primera hoja**.

---

## C-06 · El diccionario de placa

| Campo | Valor |
|---|---|
| Productores | `Placa_Prueba` (`982-1015`), `Placa_D1` (`1017-1036`), `Placa_D2` (`1038-1057`), `Parametros_Electricos.Placa` (muerto) |
| Consumidores | todo el cálculo eléctrico (`PE*`, `IV_R*`, `IV_CI*`, `correction_*`) |
| Claves | `Pmax`, `Vmax60`, `Imax`, `Voc`, `Isc`, `alpha`, `beta`, `deltha`, `cells_in_series`, `temp_ref`, `cell_type`, `A`, `Boltzmann`, `Elementary_charge` |

**Trampa `B-06`:** `Placa_Prueba` recibe once argumentos y **los sobrescribe todos** con valores
fijos (`984-994`: 250 W, `polySi`, 60 celdas). Cualquier ruta que la use simula un módulo distinto
del que el usuario eligió, sin aviso.

**Nota de unidades:** `alpha` y `beta` se guardan en **porcentaje** (0.04, −0.25) y cada consumidor
decide si divide entre 100. `PE` divide para el ajuste CEC y **no** divide para De Soto (`1386` vs
`1400`). Es una de las decisiones abiertas de [10](10-decisiones-pendientes.md).

---

## C-07 · El contrato que falta

Lo que el sistema **no** tiene y que un refactor necesita:

1. Un **objeto de datos tipado** en lugar de rutas de fichero: serie anual con índice `Time`
   garantizado y columnas declaradas.
2. Un **nombre de índice explícito** al escribir (`index_label="Time"`), no heredado.
3. **Aislamiento por sesión o corrida**: ningún `glob` + `os.remove` sobre el directorio de trabajo.
4. **Validación de la medición contra el módulo simulado** antes de comparar nada.
5. **Orden declarado** entre S2 y S3: hoy la irradiancia se propaga por mutación, no por retorno.
