---
title: El refactor propuesto por el autor
role: Diseño histórico para reducir duplicación y separar responsabilidades del sistema Dash.
retrieve_when: Se evalúa la intención de una separación o consolidación de funciones legacy.
read_scope: El estado pertinente y sus requisitos de preservación; los pseudocontratos no son APIs existentes.
authority: Propuesta del autor, no arquitectura aprobada ni cobertura ejecutada del backend moderno.
verify: Contrastar cada equivalencia con productores, consumidores, contratos y capturas; arquitectura actual en docs/architecture.md.
review_status: '#to-review'
---

# 09 — El refactor propuesto

> **Propuesta**, no diagnóstico. Lo que sigue no está implementado ni medido: es el diseño que se
> deriva de [02](02-historia-del-dato.md), [05](05-lo-que-no-sirve.md) y [06](06-lo-que-esta-roto.md).
> Alcance: **que el sistema corra limpio en Dash**. La migración a FastAPI/Next es fase posterior y
> queda fuera de este documento a propósito.

Este alcance histórico conserva la intención del autor. La arquitectura actual
se rige por [arquitectura](../architecture.md): Python/FastAPI y presentación
Next.js, con nueva funcionalidad frontend después de la reproducción del backend.
Las firmas siguientes son propuestas de diseño, no comandos ni interfaces
soportadas por su mera presencia aquí. #to-review

---

## 1. El principio

Hoy el sistema expresa cinco dimensiones (modelos térmicos, método de curva, origen de placa, número
de módulos, corrección sí/no) como **combinaciones escritas a mano**. El refactor las convierte en
**datos**: tablas de configuración que un solo motor recorre.

Esto permite revisar las dimensiones sin multiplicar copias. Un motor compartido
no demuestra que todos los caminos funcionen: necesita preservar las diferencias
y pasar los casos de cada contrato. #to-review

---

## 2. Tamaño: estimación de diseño

| Estado | Hoy | Objetivo | Qué desaparece |
|---|---:|---:|---|
| **S0** Arranque y UI de entrada | 29 | **5** | `table_module` ×3, cuatro `Dropdown_×`, `column_Pe`/`column_Pe_CEC`, `Year_tabla` |
| **S1** Clima | 5 | **3** | cliente NREL, normalizador al contrato, tabla |
| **S2** POA | 3 | **1** | `Solar_pos` y `Solar_pos_e` son la misma función con tilt/azimut |
| **S3** Térmica | 4 | **1** | tres modelos → un despachador con tabla |
| **S4** Eléctricos + bus | 17 | **4** | `PE`/`PE_1`, `PE_t`/`PE_t1`, `PE_t_S`/`PE_t_S1`, `Placa_D1`/`D2`, `creador_csv_PE`/`PE2`, `df_creator`/`df_creator_1` |
| **S5** Síntesis | 2 | **2** | se reescriben parametrizados: 1.979 → ~250 líneas |
| **S6** Curvas | 7 | **4** | `IV_R`/`R1`/`R2` → un motor; `IV_CI`/`CI2` → uno |
| **S7** Corrección + estadística | 18 | **8** | `minimos` ×4 → 1, `Bootstrap`/`Bootstrap2` → 1, dos muertas |
| **S8** Presentación | 31 | **12** | 24 callbacks → una función por pantalla; 7 constructores → 3 |
| **Suma de las filas** | **116** | **40** | No es un nuevo conteo del código; el total 120 anterior no coincidía con las filas. #to-review |

**Líneas: 14.896 → ~4.400** (estimación por diseño, no medida; sin tests ni contratos, que añaden ~800).

Reducir funciones no debería reducir producto. El objetivo de 40 y los umbrales
de tamaño/duplicación son preferencias de esta propuesta, no prueba de cobertura
ni criterios suficientes de reproducción. #to-review

---

## 3. La forma de cada estado

### S0 — Configuración declarativa
Un diccionario de layout y factorías parametrizadas (`module_table(mode)`, `dropdown(name, options)`),
en lugar de cuatro funciones casi idénticas. Los valores por defecto salen del módulo de prueba y se
declaran una vez.

### S1 — Clima
```
clima(site, years, resolution) -> WeatherSeries      # contrato C-01
tabla_clima(series) -> dash_table.DataTable
```
El descargador queda aislado detrás de una función que devuelve el contrato, no un `dict` con claves
por longitud.

### S2 — Irradiancia
```
poa(series, tilt, azimuth) -> Series                 # puro, sin mutar la entrada
```
Hoy las funciones mutan y no devuelven la serie; la propuesta devuelve otro
objeto. Un valor `tilt=None` necesitaría una regla nueva: la función actual usa
`float(tilt)` y falla con None. Su orientación coincide con `Solar_pos` al pasar
explícitamente tilt=lat y azimuth=180. El resultado de `clc` no se usa en el panel;
eliminarlo sigue siendo una decisión de refactor, no un cambio del original. #to-review

### S3 — Temperatura
```
MODELOS_TERMICOS = {
    "feinman": ("TFeinman", feinman),
    "sandia":  ("Tsandia",  sandia),
    "noct":    ("NOCT",     noct),
}
temperatura(series, modelos, params) -> Series
```

### S4 — El motor eléctrico y su bus
```
serie_electrica(series, placa, modelos) -> AnnualSeries   # columnas declaradas, índice Time
escribir_serie(serie, ruta)                               # index_label="Time"
leer_serie(ruta) -> AnnualSeries                          # índice Time garantizado
placa(origen, datos) -> Placa                             # prueba | manual | CEC
```
Una función por responsabilidad. La familia `PE*` es candidata a compartir
cálculos, pero no se presupone equivalencia de contratos, columnas, limpieza,
fallos o ramas. Cada variante debe caracterizarse antes de consolidarla. #to-review

### S5 — Síntesis
```
EXTREMOS = ["Pmax", "Imax", "Vmax", "Isc0", "Voc"]
extremos(serie, modelos) -> DataFrame        # 10 filas por modelo, no 7 ramas
casos_curva(serie, modelos) -> DataFrame     # 5/6/9 filas según modelos
```
La tabla se construye una vez y se filtra por modelo activo; no hay siete bloques con `return`.

### S6 — Curvas
```
curva_iv(placa, condiciones, metodo) -> (figura, tabla)
  metodo: "PE" | "VE" | "CI"
```
Un despachador puede evitar copias, conservando variantes explícitas: por ejemplo,
`IV_R_VE` fuerza gamma=-0.36 y devuelve parámetros, mientras `IV_R` usa deltha
y devuelve errores. El método PE/VE/CI no basta para declarar paridad. #to-review

### S7 — Corrección y estadística
```
corregir(curva, destino, metodo) -> Curva        # "M2" | "M2N"
curva_representativa(curvas, semilla) -> Resultado
comprobar(resultado, stc, tolerancia) -> Tabla
```
Se propone compartir mínimos y bootstrap donde sus contratos lo permitan.
Una semilla explícita, otro generador o una alineación nueva cambian controles
estadísticos; primero se capturan estado RNG, orden, truncamiento y retornos.
M2/M2N y origen medido/simulado son dimensiones distintas de la corrección. #to-review

### S8 — Presentación
Una función por pantalla, sin cálculo dentro. Los `dcc.Store` dejan de transportar rutas de fichero:
o transportan datos, o no existen (si S4–S7 se llaman en proceso).

---

## 4. Las cinco reglas que no se re-litigan

Si alguna de estas se rompe, el código vuelve a la forma actual en tres meses:

1. **Ningún cálculo lee ni escribe ficheros.** El disco es entrada/salida de usuario, no un bus.
2. **Las dimensiones son datos.** Un modelo térmico nuevo es una entrada en una tabla, no una rama.
3. **Contrato explícito en cada frontera**: índice `Time`, columnas declaradas, validación al entrar.
4. **La presentación no calcula** y no importa nada del dominio que no sea el resultado.
5. **Un módulo, una responsabilidad**: clima, física, dominio, UI. Sin excepciones por comodidad.

---

## 5. Lo que este refactor **no** hace

- No cambia la física. Las ecuaciones, pvlib y las tolerancias se conservan tal cual.
- No arregla silenciosamente los defectos de [06](06-lo-que-esta-roto.md): cada uno se decide antes
  (¿se reproduce el comportamiento actual o se corrige?). Reproducir un bug es legítimo para mantener
  paridad; corregirlo también, pero **explícito y documentado**.
- No migra a FastAPI/Next. Ese es el paso siguiente, y será barato si estos módulos no importan Dash.
- No elimina la interfaz ni cambia el flujo de pantallas.

---

## 6. Cómo se sabrá si funcionó

| Criterio | Umbral |
|---|---|
| Paridad numérica en los casos congelados | diferencia dentro de la tolerancia acordada por magnitud |
| Cobertura de combinaciones | ejecutar los contratos de cada combinación soportada, incluidos módulos, años, origen/método de corrección y fallos; el producto 7×3×3 no los enumera todos. #to-review |
| Funciones | ~40 y límite 200 líneas son objetivos de diseño propuestos, no evidencia numérica. #to-review |
| Duplicación | límite 30 líneas propuesto; compartir código no sustituye las comparaciones. #to-review |
| Acoplamiento | S1–S7 sin importar `dash` |
| Arranque | un comando ejecuta un caso completo sin abrir la interfaz |
