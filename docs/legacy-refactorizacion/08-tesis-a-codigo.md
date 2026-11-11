---
title: Del informe de licenciatura al código
role: Mapa conceptual del autor entre metodología reportada, funciones y campaña experimental.
retrieve_when: Se interpreta una afirmación de la tesis, una medición o una ruta de corrección y estadística.
read_scope: La modalidad o etapa pertinente; seguir el símbolo y la evidencia original citada.
authority: Atribución del autor y revisión estática; los resultados del libro e informe no son una reproducción local.
verify: Recuperar originales y versión; distinguir dato observado, cálculo implementado y validez científica.
review_status: '#to-review'
---

# 08 — Del informe de licenciatura al código

> Qué función produce cada cosa que el informe afirma. Sirve para dos cosas: defender el software
> (cada número debe tener su origen) y proponer el alcance de reproducción. Conservar
> el código actual no demuestra por sí solo conservar los resultados históricos validados. #to-review
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
| Modelos térmicos Faiman / Sandia SAPM / NOCT | `Temperature_feinman`, `Temperature_sandia`, `Temperature_NOCT` | `785-825`; Sandia empieza en 785. #to-review |
| Ecuaciones de traslación (`Isc`, `Voc`, `Imax`, `Vmax`, `Pmax`) | familia `PE*` | `1376-2761` |
| Parámetros De Soto y CEC/SAM | `fit_cec_sam` + `calcparams_desoto` (pvlib) dentro de las `PE*` | — |

**Correspondencia por comprobar:** las etapas coinciden por concepto. La igualdad
de ecuaciones y resultados requiere el informe original y su versión de código;
las discrepancias de coeficientes, potencia y estadística siguen abiertas.
La comparación manual con pvlib que relata el informe verifica consistencia,
no es una validación empírica independiente. #to-review

**Lo que el informe no puede sostener:** que la cadena anual esté validada experimentalmente. El
propio informe lo limita a la campaña de curvas I-V.

---

## 3. Corrección y comparación (el núcleo del trabajo)

| Paso | Función | Líneas |
|---|---|---|
| Lectura del libro de mediciones (hojas + `Info`) | `IV_CI_cor` | `5893-5960` |
| Temperaturas observada y efectiva | `IV_CI_cor`: usa la media de sensores, luego deriva otro `Tmod` desde Voc | `5957`, `5985-5989`; las correcciones reciben el Tmod derivado. #to-review |
| Corrección de curvas medidas, M2 o M2N | `correction_IV` | `7304-7534`; ambas ramas viven en esta función. #to-review |
| Corrección de curvas simuladas, M2 o M2N | `correction_IV_s` | `7609-7800`; el sufijo identifica el origen simulado, no el método normalizado. #to-review |
| Ajuste de `Rs` y coeficientes | `Rs_e`, `find_k_sweep`, `Temperature_coeffs`, `linear_fit` | `7080-7301` |
| Extrapolación a los ejes | `minimos`, `minimos_s` | `7803-8052` |
| Errores contra ficha STC o contra curva medida corregida | `IV_CI_cor`, según `Tipo_Analisis` | `6006-6008`, `6125-6127`, `6288-6290`; denominadores distintos. #to-review |
| Curva representativa | `Bootstrap`, `Bootstrap2` | `8358-8761` |
| Tabla rotulada IC95% y banda de ficha ±3% | `Comprobacion` | `8764-8850`; fija n=30 y usa el spread del bootstrap; validez estadística pendiente. #to-review |

M2 y M2N son etiquetas del código. La conformidad con una edición concreta de
IEC 60891 necesita revisión de las ecuaciones. Además, las ramas M2N medidas y
simuladas usan ajustes diferentes: `correction_IV` recalcula coeficientes,
simula G=400…1100 y optimiza k; `correction_IV_s` conserva los coeficientes,
simula G=200…1100 y usa `ri_2/100`. No deben unificarse por nombre. #to-review

La media de sensores queda en las tablas de temperatura, aunque corrección y
`IV_sim` usan el `Tmod` derivado. `T_Medicion == 'Promedio'` (`6427…`) resume
las tablas finales; no selecciona la temperatura de célula. #to-review

---

## 4. Las 30 mediciones reportadas por el autor

El autor declara haber contrastado el libro real. Los valores siguientes conservan
esa observación reportada; el libro, su hash y el informe original no están en los
artefactos disponibles para esta auditoría. No se presenta como una repetición
local de la campaña. #to-review

| Lo que afirma el informe | Lo que hay en el `.xlsx` | Estado |
|---|---|---|
| 30 curvas medidas | **30 hojas** `IV1…IV30` | coincide |
| Tomadas en una misma campaña | 11/08/2024, de 11:04 a 11:17 (13 minutos), según la revisión del autor | la duración no establece por sí sola homogeneidad. #to-review |
| Módulo policristalino de 60 celdas, según el informe | `Power` máx. 227,1 W; `Isc` 8,84 A; `Voc` 36,14 V, reportados del libro | esos máximos no identifican por sí solos tecnología, celdas o espécimen. #to-review |
| Corrección a STC y comparación | `correction_IV`, tablas, bootstrap | implementado |

Datos reportados del libro: irradiancia **860–1024 W/m²**, `Temp1`
**33,9–62,7 °C**, `Temp2` **34,6–63,8 °C**, `CurveID` de 1 a 37 con 30 filas.
Hay siete identificadores ausentes; no consta aquí si fueron curvas descartadas
ni con qué criterio. #to-review

**Campos reportados que `IV_CI_cor` no consume:** `Power`, `Isc`, `Ipeak`,
`Vpeak`, `Fill Factor`, `CurveID`, `Normalized`, `Date/Time`. Son ocho nombres.
Sí lee `Voc`, `Irrad1`, `Temp1` y `Temp2` (`5949-5952`); consumir esos campos
no equivale a validar la identidad del módulo, sensores o curva. #to-review

---

## 5. Alcance de reproducción propuesto

Estos cinco puntos organizan el trabajo; no son prueba suficiente de conservar
lo que la tesis validó. Falta enlazar informe, datos y revisión de código. #to-review

1. La curva de un módulo en condiciones dadas, con las tres modalidades.
2. Las ecuaciones de traslación anuales y sus combinaciones térmicas, separadas de la validación experimental del informe. #to-review
3. La corrección M2 y M2N a STC con las mismas tolerancias.
4. El error porcentual contra la medición.
5. La curva representativa y su intervalo, con el mismo estado/algoritmo RNG, orden de datos y reglas de alineación. #to-review

El bootstrap no fija semilla (`8366-8388`), pero una captura puede registrar y
reponer el estado RNG original sin cambiar la función. La síntesis suministrada
§4.10 reporta 4000 muestras de tamaño 15 y 255 posiciones; el código actual usa
3000×12 y trunca a la curva más corta. No está demostrada la identidad entre
esta revisión y el algoritmo de los resultados históricos. #to-review
