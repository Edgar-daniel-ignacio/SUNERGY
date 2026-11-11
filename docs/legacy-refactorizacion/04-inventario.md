---
title: Inventario de funciones legacy
role: Localizador AST del autor, con comprobación de rangos y correcciones de alcance pendientes de revisión.
retrieve_when: Resolver un identificador F- o localizar funciones de un estado.
read_scope: La fila requerida; index.json permite la misma consulta sin leer el inventario completo.
authority: Investigación estática del autor; no demuestra ejecución, paridad ni validez científica.
verify: Contrastar símbolos y condiciones con legacy; consultar la cobertura canónica para capturas e implementación actuales.
---

# 04 — Inventario: las 109 funciones y en qué estado viven

> Inventario AST del autor. Se contrastaron las 109 filas de [`index.json`](index.json): nombre,
> fichero, inicio, fin y longitud coinciden con los dos ficheros principales; no faltan funciones
> de nivel superior. Los estados son anotaciones estáticas, no resultados de ejecución.

| Estado | Funciones | Líneas |
|---|---:|---:|
| S0 | 29 | 813 |
| S1 | 3 | 136 |
| S2 | 0 | 0 |
| S3 | 3 | 35 |
| S4 | 16 | 1814 |
| S5 | 2 | 1979 |
| S6 | 14 | 1231 |
| S7 | 18 | 2596 |
| S8 | 24 | 4912 |
| **total** | **109** | **13516** |

Las 13.516 líneas suman los rangos de funciones, no las 14.896 líneas brutas. S8 contiene
24 funciones: 23 callbacks decorados y `parse_contents`, auxiliar. El grafo estático desde
23 callbacks y 22 factorías del layout alcanza 103/109; las seis restantes coinciden con las
filas «muerta». Alcanzable no equivale a ejecutable ni verificada.

Las etiquetas originales se conservan para enlazar `index.json`. En particular, `IV_CI2`
(`F-064`) no falla necesariamente al restar escalar/lista: depende del dtype (B-09);
`df_creator_1` (`F-043`) tiene cinco ramas problemáticas que las llamadas actuales no seleccionan. #to-review

## S0 (29 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-001` | `table` | `Input_File_DIV_Mac_Informe.py:29-37` | 9 | viva | — |
| `F-002` | `table_module` | `Input_File_DIV_Mac_Informe.py:41-69` | 29 | viva | — |
| `F-003` | `table_module_b` | `Input_File_DIV_Mac_Informe.py:73-100` | 28 | viva | — |
| `F-004` | `table_module_b2` | `Input_File_DIV_Mac_Informe.py:102-129` | 28 | viva | — |
| `F-005` | `lat` | `Input_File_DIV_Mac_Informe.py:132-145` | 14 | viva | — |
| `F-006` | `lon` | `Input_File_DIV_Mac_Informe.py:148-161` | 14 | viva | — |
| `F-007` | `type_year` | `Input_File_DIV_Mac_Informe.py:277-294` | 18 | viva | — |
| `F-008` | `year_time` | `Input_File_DIV_Mac_Informe.py:296-314` | 19 | viva | — |
| `F-009` | `Pos_modulo` | `Input_File_DIV_Mac_Informe.py:316-343` | 28 | viva | — |
| `F-010` | `tilt` | `Input_File_DIV_Mac_Informe.py:345-353` | 9 | viva | — |
| `F-011` | `Azimuth` | `Input_File_DIV_Mac_Informe.py:356-364` | 9 | viva | — |
| `F-012` | `time_range` | `Input_File_DIV_Mac_Informe.py:367-383` | 17 | viva | — |
| `F-013` | `Dropdown_1` | `Input_File_DIV_Mac_Informe.py:387-405` | 19 | viva | — |
| `F-014` | `Dropdown_2` | `Input_File_DIV_Mac_Informe.py:407-425` | 19 | viva | — |
| `F-015` | `Dropdown_3` | `Input_File_DIV_Mac_Informe.py:427-446` | 20 | viva | — |
| `F-016` | `Dropdown_4` | `Input_File_DIV_Mac_Informe.py:448-467` | 20 | viva | — |
| `F-017` | `Data_filter` | `Input_File_DIV_Mac_Informe.py:474-527` | 54 | viva | — |
| `F-018` | `filter_selector` | `Input_File_DIV_Mac_Informe.py:532-565` | 34 | viva | — |
| `F-019` | `creador_de_filtros` | `Input_File_DIV_Mac_Informe.py:568-661` | 94 | viva | — |
| `F-020` | `tabla_modulos_base` | `Input_File_DIV_Mac_Informe.py:663-705` | 43 | viva | — |
| `F-021` | `temperature_items` | `Input_File_DIV_Mac_Informe.py:707-721` | 15 | viva | — |
| `F-022` | `Feinman_options` | `Input_File_DIV_Mac_Informe.py:723-742` | 20 | viva | — |
| `F-023` | `NOCT_In` | `Input_File_DIV_Mac_Informe.py:745-760` | 16 | viva | — |
| `F-024` | `Sandia_options` | `Input_File_DIV_Mac_Informe.py:762-783` | 22 | viva | — |
| `F-025` | `Year_tabla` | `Input_File_DIV_Mac_Informe.py:2880-2896` | 17 | muerta | — |
| `F-026` | `column_Pe` | `Input_File_DIV_Mac_Informe.py:2898-2939` | 42 | viva | — |
| `F-027` | `column_Pe_CEC` | `Input_File_DIV_Mac_Informe.py:2942-3031` | 90 | viva | — |
| `F-028` | `M_IV` | `Input_File_DIV_Mac_Informe.py:3033-3085` | 53 | viva | — |
| `F-029` | `correcion_IV` | `Input_File_DIV_Mac_Informe.py:7065-7077` | 13 | viva | — |

## S1 (3 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-030` | `table_e` | `Input_File_DIV_Mac_Informe.py:167-220` | 54 | viva | — |
| `F-031` | `TMY` | `Input_File_DIV_Mac_Informe.py:223-276` | 54 | viva | — |
| `F-032` | `creador_csv_clima` | `Input_File_DIV_Mac_Informe.py:828-855` | 28 | viva | C-02 |

## S3 (3 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-033` | `Temperature_sandia` | `Input_File_DIV_Mac_Informe.py:785-800` | 16 | viva | — |
| `F-034` | `Temperature_feinman` | `Input_File_DIV_Mac_Informe.py:805-814` | 10 | viva | — |
| `F-035` | `Temperature_NOCT` | `Input_File_DIV_Mac_Informe.py:817-825` | 9 | viva | — |

## S4 (16 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-036` | `creador_csv_PE` | `Input_File_DIV_Mac_Informe.py:859-884` | 26 | viva | C-03 |
| `F-037` | `creador_csv_PE2` | `Input_File_DIV_Mac_Informe.py:886-911` | 26 | viva | C-03 |
| `F-038` | `Placa_Prueba` | `Input_File_DIV_Mac_Informe.py:982-1015` | 34 | rota | C-06 |
| `F-039` | `Placa_D1` | `Input_File_DIV_Mac_Informe.py:1017-1036` | 20 | viva | C-06 |
| `F-040` | `Placa_D2` | `Input_File_DIV_Mac_Informe.py:1038-1057` | 20 | viva | C-06 |
| `F-041` | `df_creator` | `Input_File_DIV_Mac_Informe.py:1059-1129` | 71 | viva | C-02 |
| `F-042` | `df_creator_PE` | `Input_File_DIV_Mac_Informe.py:1131-1205` | 75 | muerta | C-03 |
| `F-043` | `df_creator_1` | `Input_File_DIV_Mac_Informe.py:1207-1287` | 81 | rota | C-03 |
| `F-044` | `Factor_Idealidad` | `Input_File_DIV_Mac_Informe.py:1291-1374` | 84 | viva | — |
| `F-045` | `PE` | `Input_File_DIV_Mac_Informe.py:1376-1519` | 144 | viva | — |
| `F-046` | `PE_NOCT` | `Input_File_DIV_Mac_Informe.py:1524-2011` | 488 | rota | — |
| `F-047` | `PE_t` | `Input_File_DIV_Mac_Informe.py:2013-2178` | 166 | viva | — |
| `F-048` | `PE_t_S` | `Input_File_DIV_Mac_Informe.py:2180-2318` | 139 | viva | — |
| `F-049` | `PE_t_S1` | `Input_File_DIV_Mac_Informe.py:2320-2457` | 138 | viva | — |
| `F-050` | `PE_1` | `Input_File_DIV_Mac_Informe.py:2459-2593` | 135 | viva | — |
| `F-051` | `PE_t1` | `Input_File_DIV_Mac_Informe.py:2595-2761` | 167 | viva | — |

## S5 (2 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-052` | `resume_df` | `Input_File_DIV_Mac_Informe.py:3100-4149` | 1050 | rota | — |
| `F-053` | `resume_IV` | `Input_File_DIV_Mac_Informe.py:4675-5603` | 929 | rota | — |

## S6 (14 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-054` | `table_PE1` | `Input_File_DIV_Mac_Informe.py:2764-2821` | 58 | viva | — |
| `F-055` | `table_PE2` | `Input_File_DIV_Mac_Informe.py:2823-2878` | 56 | viva | — |
| `F-056` | `table_IV` | `Input_File_DIV_Mac_Informe.py:4161-4212` | 52 | viva | — |
| `F-057` | `table_IV2` | `Input_File_DIV_Mac_Informe.py:4214-4265` | 52 | viva | — |
| `F-058` | `IV_R` | `Input_File_DIV_Mac_Informe.py:4268-4368` | 101 | viva | — |
| `F-059` | `IV_R1` | `Input_File_DIV_Mac_Informe.py:4372-4468` | 97 | viva | — |
| `F-060` | `IV_R2` | `Input_File_DIV_Mac_Informe.py:4471-4564` | 94 | viva | — |
| `F-061` | `IV_R_VE` | `Input_File_DIV_Mac_Informe.py:4566-4671` | 106 | viva | — |
| `F-062` | `IV_CI` | `Input_File_DIV_Mac_Informe.py:5607-5768` | 162 | viva | C-05 |
| `F-063` | `IV_sim` | `Input_File_DIV_Mac_Informe.py:5771-5815` | 45 | viva | C-05 |
| `F-064` | `IV_CI2` | `Input_File_DIV_Mac_Informe.py:6651-6866` | 216 | rota | C-05 |
| `F-065` | `table_final_IV` | `Input_File_DIV_Mac_Informe.py:6869-6932` | 64 | viva | — |
| `F-066` | `table_final_IVM` | `Input_File_DIV_Mac_Informe.py:6934-6997` | 64 | viva | — |
| `F-067` | `table_final_IVS` | `Input_File_DIV_Mac_Informe.py:6999-7062` | 64 | viva | — |

## S7 (18 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-068` | `eliminar_archivo_anterior` | `Input_File_DIV_Mac_Informe.py:955-958` | 4 | viva | — |
| `F-069` | `guardar_archivo` | `Input_File_DIV_Mac_Informe.py:962-980` | 19 | viva | C-05 |
| `F-070` | `IV_CI_cor` | `Input_File_DIV_Mac_Informe.py:5819-6648` | 830 | viva | C-05 |
| `F-071` | `Rs_e` | `Input_File_DIV_Mac_Informe.py:7080-7174` | 95 | viva | — |
| `F-072` | `find_k_sweep` | `Input_File_DIV_Mac_Informe.py:7177-7208` | 32 | viva | — |
| `F-073` | `Temperature_coeffs` | `Input_File_DIV_Mac_Informe.py:7214-7292` | 79 | viva | — |
| `F-074` | `linear_fit` | `Input_File_DIV_Mac_Informe.py:7294-7301` | 8 | viva | — |
| `F-075` | `correction_IV` | `Input_File_DIV_Mac_Informe.py:7304-7534` | 231 | viva | — |
| `F-076` | `get_corrected_IV_P2` | `Input_File_DIV_Mac_Informe.py:7537-7607` | 71 | muerta | — |
| `F-077` | `correction_IV_s` | `Input_File_DIV_Mac_Informe.py:7609-7800` | 192 | viva | — |
| `F-078` | `minimos` | `Input_File_DIV_Mac_Informe.py:7803-7868` | 66 | viva | — |
| `F-079` | `minimos2` | `Input_File_DIV_Mac_Informe.py:7870-7971` | 102 | muerta | — |
| `F-080` | `minimos_s` | `Input_File_DIV_Mac_Informe.py:7974-8052` | 79 | viva | — |
| `F-081` | `minimos_s2` | `Input_File_DIV_Mac_Informe.py:8054-8136` | 83 | muerta | — |
| `F-082` | `IV_CI_Corr` | `Input_File_DIV_Mac_Informe.py:8140-8355` | 216 | muerta | — |
| `F-083` | `Bootstrap` | `Input_File_DIV_Mac_Informe.py:8358-8562` | 205 | viva | — |
| `F-084` | `Bootstrap2` | `Input_File_DIV_Mac_Informe.py:8565-8761` | 197 | viva | — |
| `F-085` | `Comprobacion` | `Input_File_DIV_Mac_Informe.py:8764-8850` | 87 | viva | — |

## S8 (24 funciones)

| ID | Función | Fichero:líneas | L | Estado | Contrato |
|---|---|---|---:|---|---|
| `F-086` | `toggle_inputs` | `GIU_Final_Presetacion.py:675-689` | 15 | rota | — |
| `F-087` | `filter_data` | `GIU_Final_Presetacion.py:698-701` | 4 | viva | — |
| `F-088` | `shower_list` | `GIU_Final_Presetacion.py:725-730` | 6 | viva | — |
| `F-089` | `data_handler` | `GIU_Final_Presetacion.py:753-805` | 53 | viva | — |
| `F-090` | `angles_show` | `GIU_Final_Presetacion.py:816-823` | 8 | viva | — |
| `F-091` | `clima` | `GIU_Final_Presetacion.py:853-936` | 84 | viva | C-01 |
| `F-092` | `update_year_dropdown_visibility` | `GIU_Final_Presetacion.py:947-950` | 4 | viva | — |
| `F-093` | `render_content` | `GIU_Final_Presetacion.py:969-1080` | 112 | viva | — |
| `F-094` | `update_map_center` | `GIU_Final_Presetacion.py:1093-1096` | 4 | viva | — |
| `F-095` | `use_ndh` | `GIU_Final_Presetacion.py:1105-1115` | 11 | rota | C-02 |
| `F-096` | `electric_parameters` | `GIU_Final_Presetacion.py:1148-1441` | 294 | viva | C-04 |
| `F-097` | `Data_Base_selector` | `GIU_Final_Presetacion.py:1460-1478` | 19 | viva | — |
| `F-098` | `Graph_filter` | `GIU_Final_Presetacion.py:1494-1556` | 63 | viva | — |
| `F-099` | `update_graph` | `GIU_Final_Presetacion.py:1568-1712` | 145 | viva | — |
| `F-100` | `Voltaje_Corriente_Selector` | `GIU_Final_Presetacion.py:1723-1730` | 8 | viva | — |
| `F-101` | `Voltaje_Corriente_Selector` | `GIU_Final_Presetacion.py:1742-3683` | 1942 | viva | — |
| `F-102` | `Graph_filter_IV` | `GIU_Final_Presetacion.py:3699-3725` | 27 | viva | — |
| `F-103` | `IV_Corrct` | `GIU_Final_Presetacion.py:3791-3963` | 173 | viva | C-04 |
| `F-104` | `Tabla_select` | `GIU_Final_Presetacion.py:3981-4001` | 21 | rota | C-04 |
| `F-105` | `Tabla_R_Boots` | `GIU_Final_Presetacion.py:4045-4127` | 83 | rota | C-04 |
| `F-106` | `electric_parameters` | `GIU_Final_Presetacion.py:4182-5955` | 1774 | viva | C-04 |
| `F-107` | `add_row` | `GIU_Final_Presetacion.py:5964-5970` | 7 | viva | — |
| `F-108` | `parse_contents` | `GIU_Final_Presetacion.py:5976-6026` | 51 | viva | — |
| `F-109` | `update_output` | `GIU_Final_Presetacion.py:6035-6038` | 4 | viva | — |

## Funciones fuera de los dos ficheros (5 módulos)

S2 no aparece arriba porque **la irradiancia en el plano no vive en los dos ficheros grandes**:
está en `Posicion_Solar.py`. Los 11 localizadores externos también coinciden con la fuente:
son **10 funciones y una clase**. Estos símbolos no están incluidos en los totales de arriba.

| Estado | Fichero | Función | Líneas | Situación |
|---|---|---|---|---|
| S1 | `Primer_Funcion_Clima.py` | `Clima` | 64-183 | viva |
| S1 | `Primer_Funcion_Clima.py` | `obtener_utc_de_coordenadas` | 24-40 | viva |
| S1 | `Primer_Funcion_Clima.py` | `SmartNDH (clase)` | 43-56 | viva |
| S1 | `Clima_Car.py` | `clc` | 3-40 | viva (resultado descartado) |
| S2 | `Posicion_Solar.py` | `Solar_pos` | 36-112 | viva |
| S2 | `Posicion_Solar.py` | `Solar_pos_e` | 116-192 | viva |
| S2 | `Posicion_Solar.py` | `get_time_zone` | 24-33 | viva |
| — | `Parametros_Electricos.py` | `PE` | 56-232 | muerta |
| — | `Parametros_Electricos.py` | `Placa` | 34-54 | muerta |
| — | `Parametros_Electricos.py` | `temperaturas` | 6-30 | muerta (pide input() por teclado) |
| — | `CurvaIV.py` | `IV` | 14-98 | muerta |

Nota: `Parametros_Electricos.temperaturas` llama a `input()` (`L21`): una invocación interactiva
puede esperar datos; en un entorno sin stdin puede fallar. No hay llamadas a los alias `pe`/`iv`
en el panel analizado; «muerta» en estos módulos no acredita ausencia de consumidores externos.
