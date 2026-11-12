---
title: Decisiones pendientes del modelo y los contratos
role: Opciones propuestas por el autor para discrepancias y cambios de comportamiento.
retrieve_when: Se pretende corregir o seleccionar una ecuación, unidad, rejilla, lectura o control estadístico.
read_scope: La decisión D pertinente, su función citada y el registro de supuestos vigente.
authority: Propuestas abiertas; ninguna recomendación equivale a un valor científico o contrato aprobado.
verify: Conservar la referencia observada y revisar formulación, unidades, fuentes y consecuencias del cambio.
---

# 10 — Decisiones pendientes

> **Esto no lo puede decidir el refactor.** Son cuestiones donde el código hace algo, el informe dice
> otra cosa o no dice nada, y elegir mal significa reescribir limpio un resultado incorrecto.
>
> Cada una lleva dos opciones y su consecuencia. La decisión es de las personas; aquí solo se deja el
> terreno preparado.

---

## `D-01` · El factor de irradiancia anual: `1000/G` o `G/1000`

**Qué pasa hoy.** `PE` (`1508`) calcula `Pmax=Vmp*Imp`. La función alternativa
de `Parametros_Electricos` (`185-186`, `219-220`) divide otra fórmula por
`1000/POA`. La síntesis suministrada reporta un factor impreso `1000/G`; el
informe original y la cadena completa requieren contraste.

| Opción | Consecuencia |
|---|---|
| **A** — multiplicar por `G/1000` | es igual a dividir por `1000/G`, para G distinto de cero. No identifica por sí solo la fórmula completa. |
| **B** — dividir por `1000/G` | no invierte el factor respecto a A; el término que se multiplica también debe compararse. |

**Por qué importa:** `PE` ya incluye `G/1000` en `Imax` y calcula `Vmax*Imax`;
la función alternativa traslada directamente la potencia de ficha. No se ha
establecido una diferencia máxima del 20% ni la equivalencia de ambas fórmulas.
Hay que comparar la cadena completa, sin añadir otro factor a `PE`. #to-review
**Recomendación:** fijar la formulación primaria (De Soto 2006 o el texto de referencia del informe) y
comprobar tres puntos a mano antes de tocar el código.

---

## `D-02` · Significado y unidades de `alpha` y `beta`

**Qué pasa hoy.** Se guardan como porcentaje (`0.04`, `−0.25`). `PE` divide entre 100 para el ajuste
CEC (`1386-1387`) y **no** divide para De Soto (`1400`). El informe deja las unidades de `gamma`
abiertas.

| Opción | Consecuencia |
|---|---|
| **A** — definir unidades explícitas en el contrato del modelo corregido | no basta dividir entre 100: el ajuste CEC requiere alpha en A/°C y beta en V/°C; De Soto consume alpha absoluto. |
| **B** — preservar valores y conversiones actuales en compatibilidad | permite medir el comportamiento observado; mantiene la inconsistencia documentada. |

**Propuesta del autor:** normalizar la interpretación para un modelo corregido.
Debe conservarse el registro fuente y asignarse un único propietario de cada
conversión. No se aplica silenciosamente a una referencia de compatibilidad. #to-review

---

## `D-03` · La forma del método 2 normalizado

**Qué pasa hoy.** El término al cuadrado de `7513-7524` pertenece a
`correction_IV`, no a `correction_IV_s`. Ambas funciones admiten M2 y M2N y
usan el término cuadrático, pero ajustan parámetros de forma distinta para
curvas medidas y simuladas. Existe `get_corrected_IV_P2` (`7537-7607`) sin
llamadas directas en el panel/módulo inspeccionados. El informe reconoce
ambigüedad logarítmica; ver el [mapa de métodos y orígenes](08-tesis-a-codigo.md).

| Opción | Consecuencia |
|---|---|
| **A** — implementar una formulación contrastada de IEC 60891 | requiere identificar edición, ecuaciones y condiciones, y evaluar sus diferencias con cada variante actual. |
| **B** — conservar cada forma implementada como variante | puede establecer paridad con el código seleccionado; no demuestra por sí sola paridad con la tesis ni distancia de una norma no contrastada. |

**Propuesta del autor:** conservar primero las variantes. Identificar edición y
ecuaciones de la norma antes de afirmar conformidad o desviación; preservar
capturas separadas de M2/M2N y de los ajustes medidos/simulados. #to-review

---

## `D-04` · La rejilla de puntos de la curva

**Qué pasa hoy.** Tres rejillas distintas: 100 puntos (Lambert W en `IV_R*`), 250 puntos (en otras
rutas) y `len(df)` (en las de medición).

| Opción | Consecuencia |
|---|---|
| **A** — una sola rejilla (100) para todo | comparaciones homogéneas; puede cambiar valores interpolados |
| **B** — rejilla por método, declarada en el contrato | conserva el comportamiento actual |

**Propuesta del autor:** A para un modelo posterior. La reproducción conserva la
rejilla de cada rama; unificarla requiere otro contrato y comparación explícita.
No se resamplean referencias para obtener un pase. #to-review

---

## `D-05` · Cómo se lee el libro de mediciones

**Qué pasa hoy.** Por posición (`sheet_name=i`), lo que exige que `Info` sea la última hoja.

| Opción | Consecuencia |
|---|---|
| **A** — leer por nombre (`IV1…IVn`) y localizar `Info` por nombre | robusto; deja de romperse si el usuario reordena |
| **B** — mantener posición y documentar el requisito | cero cambios, cero mejoras |

**Propuesta del autor:** A, asociada al riesgo `R-03`. La lectura por nombre es
un cambio respecto a la selección posicional actual y requiere preservar primero
el libro original y capturar fallos/desalineación por rama.

---

## `D-06` · La semilla del bootstrap

**Qué pasa hoy.** `np.random.choice` sin semilla (`8366-8388`): dos corridas dan curvas distintas.

| Opción | Consecuencia |
|---|---|
| **A** — fijar semilla y declararla en el resultado | propone un control explícito; debe identificar también generador, versión y orden de llamadas. |
| **B** — preservar el RNG global actual | puede capturarse su estado y reponerse para reproducir una corrida controlada; sin estado no se recupera una corrida histórica desconocida. |

**Propuesta del autor:** A para nuevas corridas controladas. La compatibilidad
también puede registrar estado RNG sin editar la función; cambiar semilla por
defecto, generador o reglas de muestreo es un cambio de comportamiento. #to-review

---

## `D-07` · Qué significa «igual» al comparar salidas

No existe una tolerancia única razonable.

| Magnitud | Tolerancia propuesta | Por qué |
|---|---|---|
| `Isc`, `Imax` | 1e-9 absoluto | operaciones deterministas |
| `Voc`, `Vmax` | 1e-6 absoluto | logaritmos y exponenciales |
| `Pmax` | 1e-6 relativo | producto de las anteriores |
| Curvas I-V | 1e-4 relativo en el punto | depende del solver |
| Bootstrap | igualdad exacta con semilla fija | si no, no se compara |
| Tablas de UI | igualdad de estructura, no de flotantes | es presentación |

**Estado:** estos números son una propuesta histórica, no tolerancias aprobadas.
Cada referencia necesita unidades, precisión, entorno, justificación y una prueba
que detecte diferencias relevantes. Los manifiestos de captura actuales son la
autoridad de su comparación; esta tabla no debe sustituirlos. #to-review

---

## `D-08` · Qué se hace con `Placa_Prueba`

Hoy sobrescribe sus argumentos con 250 W fijos (`984-994`), y de ahí cuelga todo el modo «módulo de
prueba».

| Opción | Consecuencia |
|---|---|
| **A** — conservarla como módulo de prueba **legítimo**, con sus valores fijos declarados | el modo sigue existiendo y deja de mentir |
| **B** — eliminarla y usar el modo manual con valores por defecto | menos código, cambia la pantalla inicial |

**Propuesta del autor:** A, con un nombre y valores explícitos. Hacer que el modo
manual respete argumentos antes descartados sigue siendo un cambio de conducta,
no una simple limpieza de nombre. #to-review

---

## Resumen para decidir

| ID | Decisión | Bloquea a |
|---|---|---|
| `D-01` | factor de irradiancia | S4 |
| `D-02` | unidades de coeficientes | S4, S6 |
| `D-03` | forma del M2N | S7 |
| `D-04` | rejilla de puntos | S6 |
| `D-05` | lectura del libro de mediciones | S7 |
| `D-06` | semilla del bootstrap | S7 |
| `D-07` | tolerancias de paridad | todas |
| `D-08` | placa de prueba | S0, S4 |

Estas decisiones bloquean las correcciones que dependan de ellas, no toda la
captura o refactorización estructural. Puede reproducirse el comportamiento
observado, incluidas sus inconsistencias y un estado RNG controlado, sin aprobar
todavía una formulación corregida. #to-review
