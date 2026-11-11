---
title: Defectos y condiciones de fallo legacy
role: Hallazgos estáticos del autor, con correcciones auditadas pendientes de revisión.
retrieve_when: Caracterizar un defecto B- antes de capturarlo o cambiar su comportamiento.
read_scope: La fila B-, sus condiciones y el estado de verificación.
authority: Investigación estática del autor; no demuestra ejecución, paridad ni validez científica.
verify: Contrastar símbolos y condiciones con legacy; consultar la cobertura canónica para capturas e implementación actuales.
review_status: '#to-review'
---

# 06 — Lo que está roto

> Trece hallazgos del autor contrastados estáticamente, con condiciones revisadas abajo. Ninguno
> se ejecutó en esta auditoría. `B-09` es una hipótesis dependiente del dtype, no una excepción
> probada en todas las ramas. La fuente original `docs/13-bugs-y-soluciones.md` pertenece al repo
> de análisis y no está suministrada aquí. #to-review

| `B-` | Hallazgo y condición | Línea | Efecto previsto | Corrección propuesta, no aplicada |
|---|---|---|---|---|
| `B-01` | 4 ramas `Seleccion` quedan fuera de la guarda de año, dentro del recorrido de datos; requiere entradas no vacías | panel `5662, 5735, 5808, 5881` | puede devolver un par anterior al año elegido | caracterizar la rama y después revisar indentación. #to-review |
| `B-02` | 7 `tableC2` usan `Placa/resume` en vez de `Placa2/resume2`; llamadas CI2 también pasan `df` en vez de `df2` | panel `5456, 5535, 5611, 5684, 5757, 5830, 5903` y ramas CI2 | tabla 2 usa entrada del módulo 1; impacto de `df` depende de contenido/mutaciones | capturar ambos módulos; revisar argumentos. #to-review |
| `B-03` | `any()` itera caracteres de la etiqueta seleccionada; espacios/dígitos compartidos pueden aceptar otros años | panel `5428-5431`, `2477-2480` | filtro ineficaz para etiquetas habituales; no tautología para cualquier cadena | comparar etiquetas completas e identificar año/resolución. #to-review |
| `B-04` | índices de extremos `Voc_F`, pero valores de `Vmax_F` (Sandia lee `Voc_S`) | módulo `3128-3129` | la tabla publica otra magnitud como Voc en la rama afectada | conservar referencia y evaluar cambio de columna. #to-review |
| `B-05` | condiciones de voltaje máximo rotuladas temperatura mínima en `resume_IV`: 10 `minima` + 1 `Minima` | módulo `4759` y otros 10 sitios | interpretación incorrecta de la condición de curva | capturar orden/condiciones y corregir etiquetas aparte. #to-review |
| `B-06` | `Placa_Prueba` descarta los 11 valores suministrados y devuelve 250 W; `INSERT` la reutiliza | módulo `982-1015`; panel p. ej. `1188` | entrada manual ignorada; el preset `SELEC` sí muestra 250 W | distinguir preset de entrada manual antes de cambiar. #to-review |
| `B-07` | `round(d, 2)` sobre un dict en `[2]`/`[3]`, si se alcanza tras construirlo | módulo `3267, 3524` | `TypeError` en esa operación | capturar fallo; definir redondeo explícito por separado. #to-review |
| `B-08` | el operando `'NOCT'` es verdadero; la guarda aún requiere `Tsandia` y `TFeinman` | módulo `1663` | acceso a NOCT ausente si están ambas otras columnas; no fallo universal | probar columna faltante y revisar pertenencia. #to-review |
| `B-09` | resta escalar medido/lista en 7 ramas; el escalar proviene de pandas sin conversión a `float` Python | módulo `6790-6848` | `numpy.float64` sí admite la resta; `float` Python no. Fallo pendiente de dtype/captura | recuperar libro y dtypes antes de proponer conversión. #to-review |
| `B-10` | 32 lecturas de CSV sin productor activo; las rutas son alcanzables | panel `4344-5937`; módulo `913-930` comentado | `FileNotFoundError` si no existe un CSV externo | fijar y capturar el contrato de medición antes de cambiar lector. #to-review |
| `B-11` | `IV_Corrct` inicializa resultados locales a 0 y puede publicarlos por guardas; los stores no declaran `data` inicial | panel `3794-3797` y retornos de guarda | una selección posterior puede enviar 0 a tabla/bootstrap; secuencia sin capturar | distinguir ausencia de resultado y tabla/curva válida. #to-review |
| `B-12` | claves `style` dentro del valor de la propiedad `style` en 5 retornos de `Tabla_R_Boots` | panel `4092, 4100, 4110, 4119, 4127` | forma de estilo incorrecta; efecto visual depende de Dash/navegador | capturar UI y corregir clave `display` aparte. #to-review |
| `B-13` | fallback de `toggle_inputs` devuelve un dict para 13 salidas con selección vacía/no reconocida; valor inicial `SELEC` | panel `689`, control `143` | contrato de salidas inválido en fallback; no fallo normal de arranque demostrado | caracterizar selección vacía y devolver salida completa. #to-review |

---

## Cinco hallazgos que afectan el significado del dato

Estos cinco requieren prioridad de caracterización. Primero conservar la referencia y sus
condiciones; cualquier corrección debe separarse de la compatibilidad. El código congelado no se
parchea para producir una referencia aparentemente correcta. #to-review

1. **`B-01`** — con dos módulos y varias series, las cuatro ramas pueden retornar antes de
   alcanzar el año elegido. Falta capturar una secuencia con entradas efectivas y orden conocidos. #to-review
2. **`B-02`** — las siete tablas del módulo 2 reciben los argumentos del módulo 1, mientras su
   figura recibe los del módulo 2. La discrepancia de argumentos está en fuente; falta comparación
   numérica con placas distintas. #to-review
3. **`B-03`** — los caracteres comunes de las etiquetas habituales invalidan la selección de
   año. Su interacción con B-01 y los rótulos `Año`/`Year` necesita un caso ejecutado. #to-review
4. **`B-04`** — la rama afectada publica `Vmax_F` como extremo de `Voc_F`; es una discrepancia
   de columna, independiente de que ambos valores coincidan accidentalmente en algún dato. #to-review
5. **`B-06`** — el preset fijo es visible en `SELEC`; la discrepancia está en usar la misma
   función para entradas manuales que prometen otra placa. #to-review

---

## Efectos de presentación pendientes de captura

El código permite identificar riesgos, pero no acredita un síntoma visual único en todos los
entornos. Estos casos requieren registrar controles, resultado del callback y versión de Dash. #to-review

- `B-03` y `B-01` pueden seleccionar otra serie o dejar una salida sin coincidencia, según la rama. #to-review
- `B-12` contiene una estructura de estilo incorrecta; la visibilidad resultante no se observó aquí. #to-review
- `B-05`: la leyenda dice «Temperatura minima» cuando muestra voltajes; el usuario lee mal el gráfico.

---

## Lo que NO está en esta lista

- **El «NameError» de `toggle_inputs`**: era falso. Las once variables son globales del módulo
  (`panel 92-102`) y la línea `678` no falla. Se corrigió tras la auditoría adversarial.
- **Rendimiento**: las relecturas y llamadas repetidas están en fuente; sin perfil no se ha medido
  aquí su coste relativo. Véase [05](05-lo-que-no-sirve.md) §4. #to-review
- **Ciencia**: las formulaciones completas de potencia anual, sus unidades y el uso de los
  términos de irradiancia requieren revisión; un factor aislado no demuestra una diferencia
  algebraica. D-01 se evalúa aparte en [10](10-decisiones-pendientes.md) y
  [suposiciones](../assumptions.md); no autoriza cambios durante el refactor. #to-review

---

## Estado de la verificación

| Nivel | Defectos |
|---|---|
| Fuente contrastada; efecto sujeto a las condiciones de cada fila | `B-01`–`B-08`, `B-10`–`B-13`. #to-review |
| Hipótesis de excepción no generalizable | `B-09`: la resta con escalar NumPy puede ser válida; requiere libro y dtype efectivos. #to-review |
| Observado ejecutando estos casos en esta auditoría | **ninguno**; las capturas parciales del backend no cubren esta lista completa. #to-review |

El arnés debe poder confirmar **o refutar** cada síntoma con entradas y entorno registrados.
Las prioridades y bloqueos de captura se mantienen en [cobertura](../legacy_backend_coverage.md),
no se deduce una prueba aprobada del número de hallazgos. #to-review
