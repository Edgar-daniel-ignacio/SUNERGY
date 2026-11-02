# 11 — Por dónde empezar

> El orden que minimiza riesgo. **Propuesta** con las dependencias reales del sistema: cada paso dice
> qué desbloquea y qué lo bloquea.

---

## Paso 0 — El congelado (y por qué va antes que todo)

**Qué es.** Ejecutar el sistema actual sobre casos fijos y guardar sus salidas numéricas. Ese archivo
es el juez de todos los pasos siguientes: un módulo refactorizado entra solo si reproduce esos números.

**Por qué va primero.** Sin él, cualquier refactor es una opinión. Con él, cada paso es comprobable en
segundos y los defectos de [06](06-lo-que-esta-roto.md) pasan de deducciones a hechos.

**Los tres bloqueos reales** (hay que resolverlos antes de escribir el arnés):

| Bloqueo | Qué falta | Cómo se resuelve |
|---|---|---|
| `NREL_API_KEY` + `NREL_API_EMAIL` | credenciales en `.env` | sin ellas S1 no corre; se puede congelar desde S4 con un `NDH` guardado |
| `Libro1.xlsx` | el catálogo CEC | solo afecta al modo `CEC`; se puede empezar con placa manual |
| Versión de `pvlib` | no está fijada | fijar la que se use y anotarla en el manifiesto |

**El arnés mínimo.** No hace falta `Dash`: se importan los módulos y se llaman las funciones
directamente. Un script que:

1. construya un `NDH` de prueba (o cargue uno guardado);
2. llame a `df_creator`, `PE*`, `resume_df`, `resume_IV`, `IV_R`, `IV_CI_cor`;
3. guarde cada salida como CSV + un `manifest.json` con versión de Python, `pvlib`, `pandas`, hash de
   entradas y de salidas.

**Los tres casos mínimos:**

| Caso | Qué ejercita | Por qué ese |
|---|---|---|
| 1 módulo, `[1]`, método `PE` | S4 → S5 → S6 | el camino más usado |
| 2 módulos, `[1,2]`, `CEC`, método `PE` | `B-02`, `B-03`, S8 | donde están los bugs que rompen dato |
| corrección con el libro de 30 curvas | S7 completo | es lo que valida la tesis |

**Criterio de éxito:** los tres corren sin abrir la interfaz y dejan salidas con hash.
**Si no corren:** ese es el primer trabajo real, y probablemente el más largo. Vale la pena saberlo
antes de prometer un refactor.

---

## Paso 1 — Cerrar tres decisiones

`D-01` (factor de irradiancia), `D-02` (unidades de los coeficientes) y `D-06` (semilla del bootstrap).
Sin ellas, S4 y S7 no tienen qué reproducir. Ver [10](10-decisiones-pendientes.md).

Coste: una conversación. Bloquea: S4, S7.

---

## Paso 2 — Contratos antes que código

Escribir `C-01`…`C-06` como **tipos y validaciones**, no como documentación: un `WeatherSeries`, un
`AnnualSeries` con índice `Time` garantizado, una `Placa` con unidades normalizadas, una
`MeasurementBook` que localiza `Info` por nombre.

Coste: bajo. Desbloquea: todo lo demás. Es el paso que impide que el refactor herede los contratos
implícitos.

---

## Paso 3 — S4 y S5 (el 60 % del ahorro)

Es donde está la duplicación más grande y donde el diseño nuevo rinde de inmediato:

- `serie_electrica(series, placa, modelos)` sustituye a siete funciones `PE*`.
- `extremos(serie, modelos)` y `casos_curva(serie, modelos)` sustituyen 1.979 líneas.
- Eliminar `PE_1`, `PE_t1`, `PE_t_S1`, `df_creator_PE`, `minimos2`, `minimos_s2`.

Cada reemplazo se acepta solo si reproduce el caso 1 del congelado.
Riesgo: los `B-01`…`B-06` viven aquí. **Decidir antes** si se reproduce el comportamiento o se corrige
(ver [09](09-refactor-propuesto.md) §5).

---

## Paso 4 — S6 y S7

`curva_iv()` con tres métodos y `corregir()` con M2/M2N. Aquí es donde el congelado del tercer caso
(corrección con las 30 curvas) se vuelve indispensable: sin él no hay forma de saber si la corrección
sigue siendo la misma.

---

## Paso 5 — S8 y S0

Al final, no al principio. Cuando S1–S7 devuelven objetos y no rutas de fichero, los callbacks se
adelgazan solos: dejan de releer del disco y de manipular estilo.

Aquí desaparecen las clases enteras de defectos de presentación: `B-03`, `B-12`, `B-13`.

---

## Lo que no hay que hacer

| Tentación | Por qué no |
|---|---|
| Reescribir desde cero en otro repo | se pierde la física validada y los números de la tesis |
| Migrar a FastAPI/Next ahora | duplica el trabajo sobre un sistema que aún no corre limpio |
| Arreglar los 13 defectos antes del congelado | sin juez, no se puede demostrar que el arreglo no rompió otra cosa |
| Borrar el código muerto como primer paso | ahorra 6 % y no cambia nada estructural |
| Parametrizar sin casos de prueba | es la forma más rápida de cambiar resultados sin darse cuenta |
| Confiar en la interfaz para probar | no hay forma de ejecutar un caso sin teclear |

---

## Primera semana, en concreto

1. Fijar `pvlib` y `pandas`, documentar versiones. *(1 h)*
2. Resolver credenciales y localizar `Libro1.xlsx`. *(variable)*
3. Escribir el arnés mínimo con el caso 1. *(1 día)*
4. Congelar caso 1 y guardar el manifiesto. *(2 h)*
5. Repetir con los casos 2 y 3. *(1–2 días según el libro de mediciones)*
6. Cerrar `D-01`, `D-02`, `D-06`. *(una conversación)*
7. Definir los tipos de contrato de S1–S3. *(1 día)*

Al final de esa semana se sabe, con datos, si el refactor es de semanas o de meses. Eso es lo que hoy
no se sabe.
