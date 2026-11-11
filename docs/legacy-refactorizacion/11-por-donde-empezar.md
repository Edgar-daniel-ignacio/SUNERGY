---
title: Por dónde empezar según la propuesta del autor
role: Secuencia histórica de captura y refactorización con sus dependencias.
retrieve_when: Se elige el siguiente flujo legacy que caracterizar o se recupera el orden propuesto.
read_scope: El paso pertinente; contrastar sus prerrequisitos con cobertura y comandos actuales.
authority: Propuesta de secuencia, no estado vigente ni receta de ejecución aprobada.
verify: Confirmar artefactos, importaciones, efectos de llamada y capturas existentes antes de ejecutar.
review_status: '#to-review'
---

# 11 — Por dónde empezar

> El orden que minimiza riesgo. **Propuesta** con las dependencias reales del sistema: cada paso dice
> qué desbloquea y qué lo bloquea.

El congelado sigue siendo la prioridad. Esta propuesta antecede a las capturas
parciales actuales; [cobertura](../legacy_backend_coverage.md) mantiene sus límites,
el [README del proyecto](../../README.md) los comandos soportados y el plan activo
el progreso de una tarea. No se ejecuta un pseudoflujo solo por aparecer aquí. #to-review

---

## Paso 0 — El congelado (y por qué va antes que todo)

**Qué es.** Ejecutar el sistema actual sobre casos fijos y guardar sus salidas numéricas. Ese archivo
es el juez de todos los pasos siguientes: un módulo refactorizado entra solo si reproduce esos números.

**Por qué va primero.** Sin él, cualquier refactor es una opinión. Con él, cada paso es comprobable en
segundos y los defectos de [06](06-lo-que-esta-roto.md) pasan de deducciones a hechos.

**Dependencias de cada ruta**, no bloqueos de todo arnés: #to-review

| Bloqueo | Qué falta | Cómo se resuelve |
|---|---|---|
| `NREL_API_KEY` + `NREL_API_EMAIL` | credenciales para adquisición en vivo | bloquean esa adquisición; un snapshot o entradas sintéticas permiten otras caracterizaciones. #to-review |
| `Libro1.xlsx` | catálogo del selector `CEC`, sin edición/origen confirmados | afecta ese modo; el módulo manual evita esa dependencia. #to-review |
| Entorno histórico | versiones originales no establecidas | seleccionar y registrar un entorno reconstruido no prueba identidad histórica; las capturas actuales ya tienen locks propios. #to-review |

**El arnés propuesto.** Importar el helper completo sí requiere Dash y otras
dependencias UI/científicas. Su nivel superior contiene importaciones y funciones,
no borrados; los efectos de ficheros aparecen al llamar determinados helpers.
Las capturas actuales seleccionan AST inspeccionado en procesos aislados. La
lista siguiente es el alcance de un futuro flujo completo, no una rutina ya
implementada: #to-review

1. construya un `NDH` de prueba (o cargue uno guardado);
2. llame a `df_creator`, `PE*`, `resume_df`, `resume_IV`, `IV_R`, `IV_CI_cor`;
3. conserve salidas crudas y un manifiesto con fuente/wrapper, entorno incluido
   PySAM/SSC para ajuste CEC, entradas efectivas, unidades, rejillas, RNG y hashes;
   no basta registrar solo pvlib/pandas. #to-review

**Los tres casos mínimos:**

| Caso | Qué ejercita | Por qué ese |
|---|---|---|
| 1 módulo, `[1]`, método `PE` | S4 → S5 → S6 | el camino más usado |
| 2 módulos, `[1,2]`, `CEC`, método `PE` | `B-02`, `B-03`, S8 | donde están los bugs que rompen dato |
| corrección con el libro de 30 curvas | S7 completo | es lo que valida la tesis |

**Criterio de este piloto propuesto:** los tres casos corren sin interfaz y dejan
referencias con procedencia verificable. No es por sí solo el cierre de todas las
capacidades del backend ni una validación científica. #to-review
**Si no corren:** ese es el primer trabajo real, y probablemente el más largo. Vale la pena saberlo
antes de prometer un refactor.

---

## Paso 1 — Cerrar tres decisiones

`D-01`, `D-02` y `D-06` condicionan formulaciones corregidas y controles nuevos.
No impiden capturar el comportamiento actual, sus fallos o un estado RNG original
controlado. Ver [10](10-decisiones-pendientes.md); no se estima su resolución como
«una conversación» ni se detiene trabajo independiente por estas decisiones. #to-review

---

## Paso 2 — Contratos antes que código

Escribir `C-01`…`C-06` como **tipos y validaciones**, no como documentación: un `WeatherSeries`, un
`AnnualSeries` con índice `Time` garantizado, una `Placa` con unidades normalizadas, una
`MeasurementBook` que localiza `Info` por nombre.

Los tipos deben formalizar las fronteras que se implementen, distinguiendo los
contratos observados de propuestas como lectura por nombre o coeficientes corregidos.
No se necesitan esquemas especulativos de rutas aún no implementadas. #to-review

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
| Reescribir sin preservar fuente y referencias | se pierde la posibilidad de medir compatibilidad; la validez física necesita evidencia separada. #to-review |
| Anteponer nueva UI a la reproducción | la arquitectura actual usa Python/FastAPI/Next, pero la funcionalidad nueva del frontend espera al backend; no se exige reconstruir Dash. #to-review |
| Arreglar los 13 defectos antes del congelado | sin juez, no se puede demostrar que el arreglo no rompió otra cosa |
| Borrar el código muerto como primer paso | ahorra 6 % y no cambia nada estructural |
| Parametrizar sin casos de prueba | es la forma más rápida de cambiar resultados sin darse cuenta |
| Confiar en la interfaz para probar | no hay forma de ejecutar un caso sin teclear |

---

## Orden orientativo, sin promesa de plazo

1. Revisar los entornos/capturas existentes y registrar el entorno de la ruta siguiente. #to-review
2. Recuperar credenciales o fuentes solo para las rutas que las necesiten. #to-review
3. Caracterizar el caso completo seleccionado, partiendo de límites ya capturados. #to-review
4. Preservar manifiesto, referencias y diferencias antes de reemplazar ese comportamiento. #to-review
5. Repetir para módulos, fuentes y correcciones que tengan sus entradas disponibles. #to-review
6. Resolver decisiones corregidas cuando una implementación dependa de ellas. #to-review
7. Formalizar contratos de las fronteras que se implementen y comprobar consumidores. #to-review

El alcance y los siguientes pasos se ajustan con resultados ejecutados y huecos
concretos, no con los plazos de esta propuesta histórica. #to-review
