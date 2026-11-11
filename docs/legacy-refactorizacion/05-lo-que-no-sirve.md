---
title: Duplicación y desconexiones legacy
role: Diagnóstico del autor de duplicación y alcanzabilidad, con correcciones auditadas pendientes de revisión.
retrieve_when: Evaluar una posible simplificación sin confundir duplicación con equivalencia.
read_scope: El patrón afectado y sus llamadores; no usar ahorros estimados como requisito.
authority: Investigación estática del autor; no demuestra ejecución, paridad ni validez científica.
verify: Contrastar símbolos y condiciones con legacy; consultar la cobertura canónica para capturas e implementación actuales.
review_status: '#to-review'
---

# 05 — Lo que no sirve

> Separar duplicación, ausencia de un camino estático, ramas no seleccionadas y resultados
> descartados. Repetir código no demuestra que funcione ni que sus variantes sean equivalentes.
> Las métricas de similitud son reportadas por el autor; sus scripts no están disponibles. #to-review

---

## 1. Concentración de código y duplicación reportada

| Función | Líneas | Qué se repite | Ahorro estimado |
|---|---:|---|---|
| `electric_parameters@4182` | 1.774 | el autor reporta 44 grupos, 166 bloques y **1.619 líneas = 91 %**; método no reproducido | ~1.650, estimación del autor #to-review |
| `Voltaje_Corriente_Selector@1742` | 1.942 | ramas de 1/2 módulos; 692/1.206 líneas y 73 % de similitud reportados, sin método disponible | ~1.865, estimación del autor #to-review |
| `resume_df` | 1.050 | siete ramas; 73 % de similitud y 12 bloques normalizados reportados, sin método disponible | ~1.010, estimación del autor #to-review |
| `resume_IV` | 929 | siete ramas con retorno; semejanza estructural, no prueba de equivalencia numérica | ~884, estimación del autor #to-review |
| `IV_CI_cor` | 830 | reapertura de Excel por hoja; 158 líneas no consumidas reportadas, sin análisis original disponible | ~690, estimación del autor #to-review |
| `PE_NOCT` | 488 | repite operaciones por combinación térmica; las siete funciones `PE*` suman 1.377 líneas, no 1.521 | no estimado por separado #to-review |

**Total de las seis funciones: 7.013 líneas**, el 51,9 % de las 13.516 líneas de funciones o
47,1 % de las 14.896 líneas brutas. Las longitudes se contrastaron por AST; los porcentajes de
duplicación y ahorros no se han reproducido. #to-review

### Los pares que son la misma función

Estos pares orientan la inspección de código repetido. Antes de unificarlos hay que comparar
firmas, conversiones, mutaciones, grillas y comportamiento de fallo; `IV_CI/IV_CI2` ya tienen
una diferencia de operación señalada en B-09. No son equivalencias demostradas. #to-review

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

El grafo estático reconstruido desde 45 raíces (23 callbacks + 22 factorías del `layout`)
alcanza **103 de 109** funciones. Se siguieron llamadas directas locales y `input.*`, conservando
las dos definiciones de cada nombre duplicado. No cubre consumidores externos ni despacho
dinámico; la métrica no prueba ejecución exitosa. Las seis desconectadas coinciden con el índice. #to-review

| Función | Líneas | Similitud con una viva | Comentario |
|---|---:|---|---|
| `IV_CI_Corr` | 216 | 0,99 con `IV_CI2` | residual |
| `minimos2` | 102 | 0,84 con `minimos_s` | residual |
| `minimos_s2` | 83 | 0,96 con `minimos_s` | residual |
| `df_creator_PE` | 75 | 0,98 con `df_creator_1` | residual |
| `Year_tabla` | 17 | 0,82 con `Dropdown_1` | residual |
| `get_corrected_IV_P2` | 71 | 0,75, **sin gemela** | la única que merece lectura antes de borrar |

`Parametros_Electricos.py` (240 líneas) y `CurvaIV.py` (99) se importan en el panel (`L4`, `L7`),
sin llamadas a sus alias en ese fichero. Quedan fuera de la ruta del panel trazada; no se
investigaron todos los consumidores externos posibles. #to-review

Las seis funciones suman 564 líneas (4,2 % de las líneas de funciones; 3,8 % del total bruto de
los dos ficheros). Los 339 renglones de los otros módulos están **fuera** de ese denominador.
Eliminar evidencia congelada no es parte del refactor; una retirada futura necesita verificar
consumidores y conservar trazabilidad. #to-review

---

## 3. Lo que está vivo y no se puede alcanzar

La tabla separa condiciones que el grafo de llamadas no distingue: ramas no seleccionadas,
dependencias de archivo ausentes y operaciones ejecutadas cuyo resultado se descarta. #to-review

| Qué | Dónde | Condición o efecto |
|---|---|---|
| 5 ramas de `df_creator_1` (`[2]`, `[3]`, `[1,3]`, `[2,3]`, `[1,2,3]`) | módulo `1230-1286` | las 19 llamadas pasan `[1]` cableado |
| 32 lecturas de `Uploaded_.csv` | panel `4344-5937` | alcanzables, pero sin productor activo (`módulo 913-930` comentado); requieren archivo externo y fallan si falta. #to-review |
| `use_ndh` completo | panel `1105-1115` | callback alcanzable: relee/filtra y retorna `None`; realiza I/O, aunque descarta datos. #to-review |
| `clc` completo | `Clima_Car.py:3-40` | se llama; su resultado se descarta en las dos ramas (panel `906`, `910`), sin mutar el NDH de entrada. #to-review |
| `Effective_irradiance` | panel `907`, `911` | asignación alcanzable que recibe `None`; el efecto útil es la mutación de NDH por `Solar_pos`. #to-review |

---

## 4. Cálculo que se hace y se tira

| Qué | Cuánto | Dónde |
|---|---|---|
| Asignaciones no consumidas en `resume_IV` | **132 reportadas** | 6/28/42/28/28 según el autor; suma comprobada, análisis de liveness original no disponible. #to-review |
| Invocaciones `IV_R/IV_R1/IV_R2` en el callback de curvas | 70 llamadas en 35 pares | 42/14/14 llamadas por AST; los pares obtienen figura y tabla por separado, sin medición de coste. #to-review |
| Reaperturas del `.xlsx` de mediciones | dependen del número de curvas y la rama | 31 es el caso de 30 curvas reportado por el autor; no un número universal ni una medición aquí. #to-review |
| Reaperturas de `Libro1.xlsx` | hasta 3 al crear filtros, más la lectura de `data_handler` | `creador_de_filtros` llama `Data_filter` una vez por dimensión seleccionada (`568-661`); no son siempre 4 por selección. #to-review |
| Relecturas del CSV eléctrico por cambio de filtro | 19 puntos de llamada | ver `C-03` |

Los pares repiten ajuste y cálculo para recuperar figura y tabla. Son un candidato de
simplificación, pero no hay perfil de tiempo disponible para ordenarlos como el mayor coste del
sistema. La equivalencia debe cubrir también errores y efectos laterales. #to-review

---

## 5. Lo que esto significa para el refactor

- La ausencia de un camino estático no autoriza borrar fuentes congeladas ni garantiza ausencia
  de uso externo. Cualquier retirada de implementación futura requiere comprobar sus consumidores. #to-review
- El ahorro de ~6.300 líneas es una estimación de diseño del autor, no una meta ni un resultado
  medido. Consolidar requiere reproducir estructura, valores, orden, unidades y fallos de cada ruta
  seleccionada, manteniendo aparte las correcciones intencionales. #to-review
- Una rama no seleccionada y una ruta con dependencia ausente tienen bloqueos distintos.
  Registrarlos en cobertura permite caracterizar cada una antes de decidir una corrección. #to-review
