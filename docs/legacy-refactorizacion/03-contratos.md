---
title: Contratos implícitos del sistema legacy
role: Contratos recuperados por el autor, con correcciones auditadas pendientes de revisión.
retrieve_when: Reproducir una frontera de datos legacy o diagnosticar sus supuestos.
read_scope: El contrato C- correspondiente y sus funciones citadas.
authority: Investigación estática del autor; no demuestra ejecución, paridad ni validez científica.
verify: Contrastar símbolos y condiciones con legacy; consultar la cobertura canónica para capturas e implementación actuales.
---

# 03 — Contratos: qué entra y qué sale en cada frontera

> Las fronteras donde el sistema cambia de manos. Cada contrato lleva un identificador `C-###`
> para que se pueda citar sin ambigüedad. Son contratos implícitos recuperados del código, no
> contratos validados ni promesas del backend moderno.

Un contrato aquí no es una promesa del código: es **lo que el código asume**. Donde la asunción no
está declarada en ningún sitio, se dice.

---

## C-01 · `NDH` — el diccionario de clima (en memoria)

| Campo | Valor |
|---|---|
| Productor | `Primer_Funcion_Clima.Clima` (`L64-183`), vía callback `clima` |
| Consumidores | `Clima_Car.clc`, `Posicion_Solar.Solar_pos(_e)`, `Temperature_*`, `table_e`, `TMY`, `creador_csv_clima` |
| Claves | longitud de serie como `float`; inicializa `8760.0`, `17520.0`, `35040.0`, `105120.0` y admite claves adicionales si la descarga tiene otra longitud (`118-121`, `173-175`). |
| Valores | lista de DataFrames; `SmartNDH` también guarda `.df/.metadata` de la última respuesta y su iteración devuelve esos dos valores, no las claves (`43-56`, `183`). El panel usa `.items()`. |
| Columnas mínimas | `temp_air`, `wind_speed`, `ghi`, `dni`, `dhi`, `albedo`, `Year`, `Month`, `Day`, `Hour`, `Minute` |
| Columnas añadidas | `Poa_global`, `Poa_direct`, `Poa_diffuse`, `Poa_sky_diffuse`, `Poa_ground_diffuse` (S2) y `TFeinman`, `Tsandia`, `NOCT` (S3) |

**Límites.** `Clima` sí agrupa por la longitud recibida; no garantiza las cuatro resoluciones ni
valida integridad temporal. TMY fija 60 minutos. Los filtros por las cuatro longitudes están en
consumidores posteriores, no en la adquisición. El índice se hereda de la respuesta; el escritor
no fija su nombre y el lector exige `Unnamed: 0`. No se conservan metadatos por cada respuesta. #to-review

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
otra. Dos sesiones pueden interferir mediante borrado o sobrescritura; `FileNotFoundError`
depende de la secuencia de escritura/lectura, aún sin captura concurrente. #to-review

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

**Observación de diseño:** el bus es mixto. Los stores de series guardan rutas, mientras
`Tabla_Info*` transportan dicts de tablas y `Tablarm/Tablars` colecciones de curvas. Los doce
stores no declaran `data` inicial; algunos retornos de `IV_Corrct` publican ceros, riesgo B-11. #to-review

---

## C-05 · `Uploaded_.xlsx` — el libro de mediciones

| Campo | Valor |
|---|---|
| Productor | `guardar_archivo` (`módulo 962-980`), invocado desde `parse_contents` (panel `5976-6026`) |
| Consumidores | `IV_CI`, `IV_CI2`, `IV_CI_cor`, `IV_sim`, `IV_Corrct`, `electric_parameters@4182` |
| Escritura | decodifica la subida, lee todas las hojas y reescribe `Uploaded_.xlsx` con `index=False`, nombres/orden de hoja y borrado previo; no preserva bytes originales, formatos ni evidencia de fórmulas (`962-980`). #to-review |
| Hojas | `IV1…IVn` con columnas `Volts`, `Amps`, `Watts`, **y `Info` al final** |
| Hoja `Info` | `CurveID, Normalized, Date/Time, Power, Isc, Voc, Ipeak, Vpeak, Fill Factor, Irrad1, Temp1, Temp2` |
| Columnas usadas | en la extracción inicial de `IV_CI_cor`, **4 de 12**: `Voc`, `Irrad1`, `Temp1`, `Temp2`; no significa que `Voc` se descarte ni describe todos los lectores posibles. |

**Riesgo `R-03`:** el código lee curvas **por posición** (`sheet_name=i`) e `Info` por nombre.
Si `Info` queda dentro del recorrido, se interpreta como curva y puede fallar por forma/columnas
antes de calcular. El libro de 30 curvas es evidencia reportada por el autor, ausente aquí;
no se capturó el fallo ni se verificó ese artefacto en esta revisión.

**Riesgo `R-04`:** no hay validación de identidad que asocie el libro con la placa simulada.
`Voc` sí se usa en el cálculo; su presencia y la de otros campos no impiden comparar módulos
distintos. Los valores 227 W/570 W son el ejemplo reportado, no un caso reproducido aquí.

#to-review — R-03/R-04 distinguen fallo posicional, uso de Voc y ausencia de validación de identidad.

**Nota sobre `Uploaded_.csv`:** 32 lecturas esperan un archivo sin productor activo
(`creador_uplouded`, módulo `913-930`, comentado). Es una dependencia ausente de rutas alcanzables:
si no existe un CSV externo, fallan al leer. La rama del panel `4289` usa `.xlsx` y solo lee la
primera hoja; no se ha demostrado su éxito completo.

---

## C-06 · El diccionario de placa

| Campo | Valor |
|---|---|
| Productores | `Placa_Prueba` (`982-1015`), `Placa_D1` (`1017-1036`), `Placa_D2` (`1038-1057`); `Parametros_Electricos.Placa` no es llamado desde el panel trazado. |
| Consumidores | todo el cálculo eléctrico (`PE*`, `IV_R*`, `IV_CI*`, `correction_*`) |
| Claves | `Pmax`, `Vmax60`, `Imax`, `Voc`, `Isc`, `alpha`, `beta`, `deltha`, `cells_in_series`, `temp_ref`, `cell_type`, `A`, `Boltzmann`, `Elementary_charge` |

**Trampa `B-06`:** `Placa_Prueba` descarta los once valores de entrada y devuelve el preset
250 W, `polySi`, 60 celdas (`982-1015`). El defecto afecta los llamadores que pretenden respetar
entradas manuales, como `INSERT`; el preset `SELEC` ya muestra 250 W. De las 14 claves del dict,
`A=1.33`, `Boltzmann` y `Elementary_charge` se agregan en código: no son mediciones de ficha. #to-review

**Nota de unidades:** `PE` divide `alpha/beta` por 100 al ajustar CEC, pero pasa `alpha` sin
dividir a De Soto (`1386`, `1400`). Las semánticas y conversiones dependen de la fuente y no
pueden imponerse uniformemente desde los nombres. Véanse [10](10-decisiones-pendientes.md) y
[las suposiciones canónicas](../assumptions.md).

**Discrepancia de significado:** el catálogo coloca `Average NOCT` en el campo 10 de
`Database1/2` (índice 9; panel `1014`, `1047`, `1075`). `Placa_D1/D2` lo guarda como `temp_ref`,
que `PE` usa como referencia del ajuste CEC (`1390`), mientras `IV_R` fija 25 °C. NOCT y
temperatura de referencia no son intercambiables: conservar esta ruta para medir compatibilidad
y revisar una corrección por separado. #to-review

---

## C-07 · El contrato que falta

Esta lista conserva necesidades propuestas por el autor, no un contrato aprobado. La frontera
moderna y su cobertura se mantienen en [arquitectura](../architecture.md) y
[cobertura](../legacy_backend_coverage.md).

1. Un **objeto de datos tipado** en lugar de rutas de fichero: serie anual con índice `Time`
   garantizado y columnas declaradas.
2. Un **nombre de índice explícito** al escribir (`index_label="Time"`), no heredado.
3. **Aislamiento por sesión o corrida**: ningún `glob` + `os.remove` sobre el directorio de trabajo.
4. **Validación de la medición contra el módulo simulado** antes de comparar nada.
5. **Orden declarado** entre S2 y S3: hoy la irradiancia se propaga por mutación, no por retorno.
