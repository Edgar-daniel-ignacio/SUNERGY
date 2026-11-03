# 10 — Decisiones pendientes

> **Esto no lo puede decidir el refactor.** Son cuestiones donde el código hace algo, el informe dice
> otra cosa o no dice nada, y elegir mal significa reescribir limpio un resultado incorrecto.
>
> Cada una lleva dos opciones y su consecuencia. La decisión es de las personas; aquí solo se deja el
> terreno preparado.

---

## `D-01` · El factor de irradiancia anual: `1000/G` o `G/1000`

**Qué pasa hoy.** En `PE` (`módulo:1508`) la `Pmax` se obtiene multiplicando `Vmp × Imp`. En el módulo
muerto `Parametros_Electricos` (`185-186`, `219-220`) se divide por `(1000/POA)`. El informe describe la
formulación con `× (G/1000)`.

| Opción | Consecuencia |
|---|---|
| **A** — multiplicar por `G/1000` (comportamiento del código vivo) | coherente con las otras magnitudes (`Isc`, `Voc`, `Imax`, `Vmax`) |
| **B** — dividir por `1000/G` (versión anterior) | es algebraicamente lo mismo **solo si** el término va en el numerador; si está en el denominador invierte el sentido |

**Por qué importa:** es una diferencia de hasta el 20 % en `Pmax` a 800 W/m². No es redondeo.
**Recomendación:** fijar la formulación primaria (De Soto 2006 o el texto de referencia del informe) y
comprobar tres puntos a mano antes de tocar el código.

---

## `D-02` · `alpha` y `beta` en porcentaje o en fracción

**Qué pasa hoy.** Se guardan como porcentaje (`0.04`, `−0.25`). `PE` divide entre 100 para el ajuste
CEC (`1386-1387`) y **no** divide para De Soto (`1400`). El informe deja las unidades de `gamma`
abiertas.

| Opción | Consecuencia |
|---|---|
| **A** — normalizar a fracción en la frontera (contrato de placa) | un solo sitio donde se divide; imposible equivocarse después |
| **B** — dejarlo como está y documentar cada consumidor | el próximo que añada una fórmula repetirá el error |

**Recomendación:** A. Es el cambio más barato del refactor y elimina una clase entera de bugs.

---

## `D-03` · La forma del método 2 normalizado

**Qué pasa hoy.** `correction_IV_s` (`7609-7800`) usa un término **al cuadrado** (`7513-7524`), y existe
`get_corrected_IV_P2` (`7537-7607`) con otra forma, sin llamadores. El informe reconoce términos
logarítmicos ambiguos.

| Opción | Consecuencia |
|---|---|
| **A** — adoptar IEC 60891 tal cual | la corrección deja de ser «la del informe» y hay que re-validar contra las 30 curvas |
| **B** — conservar la forma implementada y documentarla como variante | paridad con la tesis, pero se aleja de la norma |

**Recomendación:** B para la primera versión (paridad con lo defendido), con la norma citada al lado y
una nota de discrepancia.

---

## `D-04` · La rejilla de puntos de la curva

**Qué pasa hoy.** Tres rejillas distintas: 100 puntos (Lambert W en `IV_R*`), 250 puntos (en otras
rutas) y `len(df)` (en las de medición).

| Opción | Consecuencia |
|---|---|
| **A** — una sola rejilla (100) para todo | comparaciones homogéneas; puede cambiar valores interpolados |
| **B** — rejilla por método, declarada en el contrato | conserva el comportamiento actual |

**Recomendación:** A para simulación, `len(df)` para medición (ahí la rejilla la pone el trazador).

---

## `D-05` · Cómo se lee el libro de mediciones

**Qué pasa hoy.** Por posición (`sheet_name=i`), lo que exige que `Info` sea la última hoja.

| Opción | Consecuencia |
|---|---|
| **A** — leer por nombre (`IV1…IVn`) y localizar `Info` por nombre | robusto; deja de romperse si el usuario reordena |
| **B** — mantener posición y documentar el requisito | cero cambios, cero mejoras |

**Recomendación:** A, sin discusión. Es el riesgo silencioso `R-03`.

---

## `D-06` · La semilla del bootstrap

**Qué pasa hoy.** `np.random.choice` sin semilla (`8366-8388`): dos corridas dan curvas distintas.

| Opción | Consecuencia |
|---|---|
| **A** — fijar semilla y declararla en el resultado | reproducible; la curva representativa deja de variar entre corridas |
| **B** — dejarlo aleatorio | más «honesto» estadísticamente, imposible de congelar |

**Recomendación:** A. Sin semilla no hay paridad posible en S7, y sin paridad no hay refactor
verificable.

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

**Recomendación:** adoptarla y escribirla en el arnés. Una tolerancia global es una invitación a
esconder diferencias.

---

## `D-08` · Qué se hace con `Placa_Prueba`

Hoy sobrescribe sus argumentos con 250 W fijos (`984-994`), y de ahí cuelga todo el modo «módulo de
prueba».

| Opción | Consecuencia |
|---|---|
| **A** — conservarla como módulo de prueba **legítimo**, con sus valores fijos declarados | el modo sigue existiendo y deja de mentir |
| **B** — eliminarla y usar el modo manual con valores por defecto | menos código, cambia la pantalla inicial |

**Recomendación:** A, pero renombrada (`placa_de_prueba()`) y con los valores en una constante visible.

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

Sin `D-01`, `D-02` y `D-06` cerradas, el refactor no puede empezar S4 ni S7: se estaría reescribiendo
sin saber qué debe reproducir.
