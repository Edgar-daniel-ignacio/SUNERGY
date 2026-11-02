# 05 — Lo que no sirve

> Tres cosas distintas que conviene no confundir: lo que se **duplica** (funciona, pero está escrito
> varias veces), lo que **no se ejecuta nunca** (muerto) y lo que es **inalcanzable hoy** (vivo, pero
> ningún llamador puede llegar a él). **medido**.

---

## 1. Duplicación: el 52 % del código

| Función | Líneas | Qué se repite | Ahorro estimado |
|---|---:|---|---|
| `electric_parameters@4182` | 1.774 | 44 grupos de bloques idénticos, 166 bloques, **1.619 líneas = 91 %** | ~1.650 |
| `Voltaje_Corriente_Selector@1742` | 1.942 | dos ramas gemelas de 692 y 1.206 líneas, 73 % similares (1 vs 2 módulos) | ~1.865 |
| `resume_df` | 1.050 | siete ramas `if Seleccion ==`, 73 % de similitud media; el bloque por modelo aparece **12 veces** al normalizar sufijos | ~1.010 |
| `resume_IV` | 929 | idéntico patrón: siete ramas, cada una con su `return` | ~884 |
| `IV_CI_cor` | 830 | 158 líneas muertas + reapertura del Excel por hoja | ~690 |
| `PE_NOCT` + familia `PE*` | 1.521 | siete funciones para el mismo cálculo con distinto conjunto de modelos | ~1.200 |

**Total en las seis monstruos: 7.013 líneas (52 % del sistema).**

### Los pares que son la misma función

Ninguno es una abstracción pendiente: son copias con el sufijo cambiado.

| Par | Diferencia real |
|---|---|
| `PE` / `PE_1` | módulo 1 contra módulo 2 |
| `PE_t` / `PE_t1` | idem |
| `PE_t_S` / `PE_t_S1` | idem |
| `Placa_D1` / `Placa_D2` | idem |
| `creador_csv_PE` / `creador_csv_PE2` | prefijo del fichero |
| `table_PE1` / `table_PE2`, `table_IV` / `table_IV2` | idem |
| `IV_R` / `IV_R1` / `IV_R2` | módulo |
| `IV_CI` / `IV_CI2` | módulo |
| `Bootstrap` / `Bootstrap2` | módulo |
| `minimos` / `minimos2` / `minimos_s` / `minimos_s2` | módulo y variante |
| `df_creator` / `df_creator_PE` / `df_creator_1` | similitud 0,98 entre las dos últimas |

---

## 2. Código muerto: 4,2 %

Alcanzabilidad determinista desde 45 raíces (23 callbacks + 22 factorías del `layout`): **103 de 109
funciones son alcanzables**. Las seis desconectadas:

| Función | Líneas | Similitud con una viva | Comentario |
|---|---:|---|---|
| `IV_CI_Corr` | 216 | 0,99 con `IV_CI2` | residual |
| `minimos2` | 102 | 0,84 con `minimos_s` | residual |
| `minimos_s2` | 83 | 0,96 con `minimos_s` | residual |
| `df_creator_PE` | 75 | 0,98 con `df_creator_1` | residual |
| `Year_tabla` | 17 | 0,82 con `Dropdown_1` | residual |
| `get_corrected_IV_P2` | 71 | 0,75, **sin gemela** | la única que merece lectura antes de borrar |

Y dos módulos completos muertos: `Parametros_Electricos.py` (240 líneas) y `CurvaIV.py` (99), importados
en el panel (`L4`, `L7`) y **nunca invocados**. Son una generación anterior del mismo cálculo, que
después se copió dentro del módulo grande.

**No son el problema.** 564 + 339 líneas de 14.896: menos del 6 %. Borrarlas no arregla nada, pero
tampoco cuesta.

---

## 3. Lo que está vivo y no se puede alcanzar

Esto es lo que no aparece en ningún análisis de código muerto y sí explica por qué el sistema
«solo funcionaba con cierto patrón de entrada»:

| Qué | Dónde | Por qué es inalcanzable |
|---|---|---|
| 5 ramas de `df_creator_1` (`[2]`, `[3]`, `[1,3]`, `[2,3]`, `[1,2,3]`) | módulo `1230-1286` | las 19 llamadas pasan `[1]` cableado |
| 32 lecturas de `Uploaded_.csv` | panel `4344-5937` | el escritor de ese `.csv` está comentado (`módulo 913-930`) |
| `use_ndh` completo | panel `1105-1116` | lee, filtra y devuelve `None`: no produce nada |
| `clc` completo | `Clima_Car.py:3-40` | su resultado se descarta en las dos ramas (panel `906`, `910`) |
| `Effective_irradiance` | panel `907`, `911` | recibe `None` porque `Solar_pos` no devuelve nada |

---

## 4. Cálculo que se hace y se tira

| Qué | Cuánto | Dónde |
|---|---|---|
| Asignaciones que nunca se leen en `resume_IV` | **132** | 6 en `[1]`, 28 en `[1,2]`, 42 en `[1,2,3]`, 28 en `[1,3]`, 28 en `[2,3]` |
| Motores de curva invocados dos veces seguidas | 35 ramas | `fig = IV_R(...)[0]` y `IV_R(...)[1]` en la línea siguiente |
| Reaperturas del `.xlsx` de mediciones | 31 por pasada | una por hoja, más la de `Info` |
| Reaperturas de `Libro1.xlsx` | 4 por selección | `Data_filter`, `creador_de_filtros` (3 veces) y `data_handler` |
| Relecturas del CSV eléctrico por cambio de filtro | 19 puntos de llamada | ver `C-03` |

El segundo es el más caro: `fit_cec_sam` + `calcparams_desoto` + `singlediode` son las tres llamadas
más pesadas del sistema y se ejecutan dos veces por rama para obtener figura y tabla de la misma
curva.

---

## 5. Lo que esto significa para el refactor

- **Borrar el código muerto no ahorra casi nada** (6 %) y no cambia el comportamiento. Es limpieza, no
  refactor.
- **Desduplicar los seis monstruos ahorra ~6.300 líneas** y sí cambia la mantenibilidad, pero solo es
  seguro si cada rama se sustituye por una parametrizada que **reproduzca los mismos números**.
- **Las ramas inalcanzables son la deuda más engañosa**: parecen funcionalidad y no lo son. Un refactor
  que las «arregle» sin decidir antes qué debe hacer el sistema está inventando producto, no
  restaurando código.
