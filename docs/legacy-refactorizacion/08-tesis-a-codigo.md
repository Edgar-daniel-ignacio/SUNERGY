# 08 — Del informe de licenciatura al código

> Qué función produce cada cosa que el informe afirma. Sirve para dos cosas: defender el software
> (cada número tiene su origen) y fijar el criterio de paridad (si el refactor conserva esto, conserva
> lo validado).
>
> **Nota:** el informe de licenciatura es
> *«Simulación, Corrección y Validación de Curvas I-V de Módulos Fotovoltaicos»* (UNAM, 2025). El mapeo
> está hecho por **concepto**; la numeración de figuras debe confirmarla el autor antes de publicarlo.

---

## 1. Las tres modalidades y su función

El informe describe tres formas de obtener una curva I-V. En el código son `Metodo`:

| Modalidad del informe | `Metodo` | Función | Qué hace |
|---|---|---|---|
| Prueba Estándar | `PE` | `IV_R`, `IV_R1`, `IV_R2` (módulo `4268-4564`) | resuelve la ecuación de un diodo en las condiciones extremas del año |
| Valores Específicos | `VE` | `IV_R_VE` (`4566-4671`) | evalúa los pares (irradiancia, temperatura) que fija el usuario |
| Comparación I-V | `CI` | `IV_CI`, `IV_CI2` (`5607-5768`, `6651-6866`) | compara con una curva medida; con `correct == [1]` pasa por `IV_Corrct` |

---

## 2. Cadena de simulación anual

| Lo que el informe afirma | Función | Líneas |
|---|---|---|
| Descarga de clima (TMY o año específico, 1998–2020) | `Primer_Funcion_Clima.Clima` | `64-183` |
| Cálculo de irradiancia en el plano (POA) | `Posicion_Solar.Solar_pos(_e)` | `36-192` |
| Modelos térmicos Faiman / Sandia SAPM / NOCT | `Temperature_feinman`, `Temperature_sandia`, `Temperature_NOCT` | `805-825` |
| Ecuaciones de traslación (`Isc`, `Voc`, `Imax`, `Vmax`, `Pmax`) | familia `PE*` | `1376-2761` |
| Parámetros De Soto y CEC/SAM | `fit_cec_sam` + `calcparams_desoto` (pvlib) dentro de las `PE*` | — |

**Lo que el informe dice y el código hace igual:** las ecuaciones de traslación son las mismas, y la
verificación manual de pvlib (Faiman, Sandia, NOCT) coincide con la que describe el texto.

**Lo que el informe no puede sostener:** que la cadena anual esté validada experimentalmente. El
propio informe lo limita a la campaña de curvas I-V.

---

## 3. Corrección y comparación (el núcleo del trabajo)

| Paso | Función | Líneas |
|---|---|---|
| Lectura del libro de mediciones (hojas + `Info`) | `IV_CI_cor` | `5893-5960` |
| Temperatura de célula medida como promedio de dos sensores | `IV_CI_cor`: `(T1 + T2)/2` | `5955` |
| Método 2 (IEC 60891) | `correction_IV` | `7304-7534` |
| Método 2 normalizado | `correction_IV_s` | `7609-7800` |
| Ajuste de `Rs` y coeficientes | `Rs_e`, `find_k_sweep`, `Temperature_coeffs`, `linear_fit` | `7080-7301` |
| Extrapolación a los ejes | `minimos`, `minimos_s` | `7803-8052` |
| Error porcentual contra lo medido | `IV_CI_cor`, tablas comparativas | `5893-6648` |
| Curva representativa | `Bootstrap`, `Bootstrap2` | `8358-8761` |
| Intervalo de confianza al 95 % y tolerancia ±3 % | `Comprobacion` | `8764-8850` |

---

## 4. Las 30 mediciones, verificadas con el libro real

| Lo que afirma el informe | Lo que hay en el `.xlsx` | Estado |
|---|---|---|
| 30 curvas medidas | **30 hojas** `IV1…IV30` | coincide |
| Tomadas en una misma campaña, condiciones homogéneas | 11/08/2024, de 11:04 a 11:17 (13 minutos) | coincide |
| Módulo policristalino de 60 celdas | `Power` máx. 227,1 W; `Isc` 8,84 A; `Voc` 36,14 V | compatible con un 250 W a ~1021 W/m² |
| Corrección a STC y comparación | `correction_IV`, tablas, bootstrap | implementado |

Datos reales del libro: irradiancia **860–1024 W/m²**, `Temp1` **33,9–62,7 °C**, `Temp2` **34,6–63,8 °C**,
`CurveID` de 1 a 37 con **30 filas** (7 curvas descartadas; el criterio no está documentado).

**Y lo que el código ignora del libro:** `Power`, `Isc`, `Voc`, `Ipeak`, `Vpeak`, `Fill Factor`,
`CurveID`, `Normalized`, `Date/Time`. Ocho de doce columnas. Son exactamente las que permitirían
comprobar que la medición corresponde al módulo simulado.

---

## 5. Criterio de paridad que se deriva de esto

Si el refactor conserva estos cinco puntos, conserva lo que la tesis validó:

1. La curva de un módulo en condiciones dadas, con las tres modalidades.
2. Las ecuaciones de traslación anuales, para cualquier combinación de modelos térmicos.
3. La corrección M2 y M2N a STC con las mismas tolerancias.
4. El error porcentual contra la medición.
5. La curva representativa y su intervalo, con la misma semilla y el mismo orden de datos.

El punto 5 tiene un problema conocido: **el bootstrap no fija semilla** (`módulo 8366-8388`). Dos
corridas dan curvas ligeramente distintas, así que la paridad exacta ahí no es posible sin decidir
primero si se fija (ver [10](10-decisiones-pendientes.md), `D-06`).
