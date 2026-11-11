---
title: Lo que falta en el sistema legacy
role: Inventario del autor de rutas incompletas, desconectadas y ausentes.
retrieve_when: Una capacidad legacy parece ausente, rota o no conectada.
read_scope: La fila de la capacidad y sus productores, consumidores y defectos enlazados.
authority: Investigación estática del autor; no demuestra ejecución ni describe por sí sola el backend actual.
verify: Contrastar función y llamadas actuales; consultar cobertura para implementaciones y capturas modernas.
review_status: '#to-review'
---

# 07 — Lo que falta: lo que se escribió y nunca llegó a funcionar

> Este capítulo es el que responde a «muchas partes no funcionan porque eran muchas combinaciones».
> Se separan tres cosas: lo **escrito y nunca conectado**, los **caminos que existen y no llegan**, y
> lo que **no existe en absoluto**. **verificado** contra el código; lo que no se puede saber se marca.

El alcance de esas ausencias es la aplicación legacy. El backend actual ya tiene
algunas funciones invocables, pruebas y capturas; su estado se mantiene en
[cobertura](../legacy_backend_coverage.md), no en este inventario histórico. #to-review

---

## 1. Escrito y nunca conectado

| Qué | Dónde | Qué habría hecho | Por qué no funciona |
|---|---|---|---|
| 5 ramas de `df_creator_1` | módulo `1230-1286` | leer el CSV eléctrico con la `Seleccion` real del usuario | las 19 llamadas pasan `[1]` cableado |
| `get_corrected_IV_P2` | módulo `7537-7607` | versión alternativa del método de corrección | 0 llamadores; sin gemela (similitud 0,75) |
| `minimos2`, `minimos_s2` | módulo `7870-7971`, `8054-8136` | extrapolación para el segundo módulo | 0 llamadas directas en el panel y módulo inspeccionados. #to-review |
| `IV_CI_Corr` | módulo `8140-8357` | corrección de curvas | 0 llamadores; 0,99 de similitud con `IV_CI2` |
| `Parametros_Electricos.py` | módulo completo, 240 líneas | motor eléctrico y de temperatura | importado y nunca llamado |
| `CurvaIV.py` | módulo completo, 99 líneas | curvas I-V con 6 condiciones fijas | importado y nunca llamado |
| `creador_uplouded` | módulo `913-930` | escribir `Uploaded_.csv` | **comentado**; 32 lecturas dependen de él |
| `use_ndh` | panel `1105-1116` | mostrar el clima leído | no tiene `return`: devuelve `None` |
| `clc` | `Clima_Car.py:3-40` | caracterización de mínimos y máximos por hora | se llama, se calcula y el resultado se descarta |

---

## 2. Caminos que existen y no llegan

Aquí no falta código: falta que alguien pueda entrar por ahí.

| Camino | Estado | Qué haría falta |
|---|---|---|
| **Comparación I-V sin corrección** (32 ramas) | roto: `FileNotFoundError` | unificar en el `.xlsx` y decidir qué hoja se lee |
| **Modo `CEC` con `Seleccion == [1, 3]` y 1 módulo** | calcula con 250 W fijos (`B-06`) | usar `Placa_D1` con los datos del catálogo |
| **Dos módulos con años múltiples** | el filtro no filtra (`B-01`, `B-03`) | corregir indentación y comparación |
| **Año con número de filas fuera de la rejilla** | algunas rutas filtran por longitud; no todas las funciones térmicas lo hacen | identificar el propietario del filtro y capturar su efecto antes de cambiarlo. #to-review |
| **Mediciones con `Info` no al final** | la lectura de curvas por posición puede desalinearse o fallar, según la rama | capturar la selección actual y evaluar lectura por nombre como cambio explícito. #to-review |
| **Mediciones de otro módulo** | se comparan igual, sin aviso | validar `Power`/`Voc` contra la placa activa |

---

## 3. Lo que no existe en absoluto

| Falta | Consecuencia | Coste de añadirlo |
|---|---|---|
| **Punto de entrada programático completo** | hay helpers invocables, pero no un caso completo desacoplado del panel y sus ficheros | extraer flujos S4–S7 con contratos; las funciones modernas ya existentes se registran en cobertura. #to-review |
| **Captura de salidas (congelado)** | la investigación original no suministró referencias ejecutadas | completar las rutas pendientes a partir de las capturas actuales; ver [reproducción](../reproduction.md). #to-review |
| **Pruebas automatizadas** | no se identificaron en el sistema legacy investigado | el backend moderno tiene pruebas; no transfieren cobertura a ramas legacy no capturadas. #to-review |
| **Aislamiento por sesión** | dos pestañas se borran los CSV | bajo: carpeta por corrida |
| **Validación de la medición** | se compara cualquier módulo con cualquier simulación | bajo |
| **Exportación de resultados anuales** | las tablas finales de I-V exportan a `.xlsx`, las series anuales no | bajo |
| **Mensajes de error de usuario** | todo falla como excepción de Python en la consola | medio |

---

## 4. La razón de fondo

Estos huecos no son descuido: son el resultado de un programa que creció combinando casos a mano.

Cada vez que aparecía una combinación nueva (otro modelo térmico, el segundo módulo, la corrección,
dos años), la respuesta fue **añadir una rama**. Con cinco dimensiones eso son decenas de ramas, y en
algún punto dejó de ser posible cubrirlas todas: se conectó el camino que se probaba y los demás
quedaron escritos, pareciendo que funcionaban.

Por eso el refactor no se limita a «arreglar trece bugs». La propuesta es **expresar
las combinaciones como datos** y reducir copias. Compartir un motor no garantiza
que todos los caminos funcionen: cada combinación y sus diferencias necesitan
contratos y comparación ejecutada. #to-review
