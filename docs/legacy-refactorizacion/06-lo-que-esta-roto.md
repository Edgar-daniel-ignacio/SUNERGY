# 06 — Lo que está roto

> Trece defectos verificados contra el código. **Ninguno se ha observado en ejecución**: son
> deducciones del código, y esa es la diferencia entre esta lista y un informe de pruebas.
> Detalle completo con síntoma, parche y comprobación: `docs/13-bugs-y-soluciones.md` del repo de
> análisis (fuente de esta tabla).

| `B-` | Defecto | Línea | Gravedad | Parche |
|---|---|---|---|---|
| `B-01` | Indentación a 20 espacios: 4 ramas `Seleccion` quedan fuera del filtro de año | panel `5662, 5735, 5808, 5881` | **rompe dato** | indentar +4 |
| `B-02` | `tableC2` se calcula con la placa del módulo 1 (7 líneas) y en 2 módulos pasa `df` en vez de `df2` (9 líneas) | panel `5456…5903` | **rompe dato** | cambiar a `Placa2`/`resume2`/`df2` |
| `B-03` | Filtro de año de 2 módulos compara **carácter a carácter**: siempre verdadero | panel `5428-5431`, `2477-2480` | **rompe dato** | comparar cadenas completas y unificar rótulo |
| `B-04` | `VocMaxF`/`VocMinF` leen `Vmax_F` en vez de `Voc_F` (Sandia sí lee `Voc_S`) | módulo `3128-3129` | **rompe dato** | cambiar la columna |
| `B-05` | Rótulo `"Temperatura minima"` sobre valores de voltaje, 10 sitios; llega a la leyenda | módulo (10 sitios) | cosmético con efecto | renombrar |
| `B-06` | `Placa_Prueba` sobrescribe sus 11 argumentos con 250 W fijos | módulo `984-994` | **rompe dato** | respetar argumentos |
| `B-07` | `round(d, 2)` sobre un dict en `resume_df` ramas `[2]` y `[3]` | módulo `3267, 3524` | excepción | `data=d` y redondear después |
| `B-08` | `and 'NOCT':` evalúa un literal siempre verdadero | módulo `1663` | excepción | `'NOCT' in datos` |
| `B-09` | `IV_CI2` resta `float − list` en sus 7 ramas | módulo `6790-6848` | excepción | convertir a `np.array` |
| `B-10` | 32 lecturas de `Uploaded_.csv`, cuyo escritor está comentado | panel `4344-5937` | excepción | leer el `.xlsx` con `sheet_name` |
| `B-11` | Stores de resultados inicializados a `0` → `pd.DataFrame(0)` y `Bootstrap(0)` | panel `3794-3795` | excepción | inicializar a `{}` + guardas con `or` |
| `B-12` | `{"style": ...}` donde Dash espera `{"display": ...}` en 3 ramas | panel `4092, 4100, 4110` | pantalla en blanco | cambiar la clave |
| `B-13` | `toggle_inputs` devuelve 1 valor para 13 salidas al arrancar | panel `689` | excepción | devolver la tupla completa |

---

## Los cuatro que rompen el dato

Son los únicos que justifican parar y arreglar antes de cualquier otra cosa, porque **dan resultados
equivocados sin avisar**:

1. **`B-01`** — con dos módulos y años múltiples, cambiar de año no cambia nada: siempre se pinta el
   primero. El usuario cree que está comparando años distintos.
2. **`B-02`** — la tabla del módulo 2 sale con los números del módulo 1. La comparación de dos módulos,
   que es una función central del programa, es falsa.
3. **`B-03`** — el filtro de año es un `any()` sobre caracteres: `'2'`, `'0'` y `' '` están en cualquier
   etiqueta, así que siempre entra. Combinado con `B-01`, el filtro temporal no existe en el modo de
   dos módulos.
4. **`B-04`** — la fila de `Voc` de Feinman es en realidad `Vmax`. Toda tabla de extremos de Feinman
   publica un Voc incorrecto.
5. **`B-06`** — cualquier ruta que use `Placa_Prueba` simula 250 W fijos, aunque el usuario haya elegido
   otro módulo. Sin aviso.

---

## Los que dan pantalla vacía sin error

Los peores de diagnosticar, porque no dejan rastro:

- `B-03` y `B-01` (arriba): la gráfica simplemente no aparece.
- `B-12`: los paneles de la curva representativa no se muestran porque la clave del estilo está mal.
- `B-05`: la leyenda dice «Temperatura minima» cuando muestra voltajes; el usuario lee mal el gráfico.

---

## Lo que NO está en esta lista

- **El «NameError» de `toggle_inputs`**: era falso. Las once variables son globales del módulo
  (`panel 92-102`) y la línea `678` no falla. Se corrigió tras la auditoría adversarial.
- **Nada de rendimiento**: la lentitud es real (relecturas, doble cálculo de curvas) pero es
  consecuencia del diseño, no un defecto con parche. Está en [05](05-lo-que-no-sirve.md) §4.
- **Nada de ciencia**: que `1000/G` o `G/1000` sea lo correcto no es un defecto del código, es una
  decisión pendiente. Está en [10](10-decisiones-pendientes.md).

---

## Estado de la verificación

| Nivel | Defectos |
|---|---|
| Confirmado dos veces (lectura + auditoría adversaria) | `B-01`, `B-02`, `B-03`, `B-04`, `B-06`, `B-07`, `B-08`, `B-09`, `B-11` |
| Confirmado una vez, con la línea abierta | `B-05`, `B-10`, `B-12`, `B-13` |
| Observado en ejecución | **ninguno** |

Ese último renglón es el que hay que cerrar antes de tocar código: un arnés de ejecución convierte
trece deducciones en trece hechos.
