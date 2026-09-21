# Proyecto de Grafos - Inglaterra Qatar 2022

## Objetivo

Analizar la red de pases de la selección de Inglaterra en cada uno de sus tres partidos de la fase de grupos del Mundial Qatar 2022, utilizando un grafo dirigido y ponderado por partido, para interpretar su estilo de juego y ver cómo cambió según el rival.

El objetivo principal del proyecto no es únicamente construir los grafos, sino interpretar qué muestra su estructura sobre la forma en que Inglaterra circuló el balón.

## Datos utilizados

Se utilizó el archivo `pases_inglaterra.csv`, que contiene los pases de Inglaterra durante el Mundial. Se filtraron únicamente los partidos de fase de grupos:

| Partido                    | Fecha      | Resultado* |
| -------------------------- | ---------- | ---------- |
| Inglaterra vs Iran         | 2022-11-21 | 6 - 2      |
| Inglaterra vs United States | 2022-11-25 | 0 - 0      |
| Inglaterra vs Wales        | 2022-11-29 | 3 - 0      |

\* El marcador no viene en el CSV; se agrega como contexto para la interpretación.

Solo se utilizaron los pases con resultado `Complete`, ya que representan pases que sí llegaron al receptor.

## Limpieza de datos

1. Se conservaron únicamente los registros donde `fase` es `Group Stage`.
2. Se conservaron únicamente los registros donde `resultado` es `Complete`.
3. Se seleccionaron solo las columnas necesarias: `match_id`, `fecha`, `oponente`, `jugador_nombre` y `receptor_nombre`. Se descartó `longitud_pase` porque el peso de las aristas no depende de ella.

De los 2,058 pases de la fase de grupos quedaron 1,799 pases completados.

## Modelo de grafo

Se construyó **un grafo dirigido y ponderado por partido**.

* Los nodos representan jugadores.
* Las aristas representan pases completados de un jugador (emisor) a otro (receptor).
* El peso de la arista es la cantidad de pases completados entre ese par de jugadores en el partido.

Decisiones y justificación:

* **Dirigido:** un pase tiene emisor y receptor, y las dos direcciones no son iguales. Por ejemplo, contra Estados Unidos Maguire le dio 35 pases a Stones, pero Stones le dio 21 a Maguire. Un grafo no dirigido perdería esa asimetría.
* **Ponderado:** entre dos jugadores hay muchos pases; el peso mide la fuerza de la conexión.
* **Un grafo por partido:** un grafo consolidado promedia los tres partidos y esconde diferencias. Con un grafo por partido se puede ver si el estilo cambió según el rival y el marcador.
* **Solo pases completados:** son los que construyen circulación real de balón entre jugadores.

| Partido             | Pases completos | Nodos | Aristas |
| ------------------- | --------------: | ----: | ------: |
| vs Iran             |             746 |    16 |     142 |
| vs United States    |             500 |    14 |     113 |
| vs Wales            |             553 |    16 |     138 |

## Métricas utilizadas

Se calcularon para cada jugador en cada partido (`metricas_por_partido.csv`):

| Métrica               | Descripción                                                           |
| --------------------- | --------------------------------------------------------------------- |
| `pases_dados`         | Pases completados realizados por el jugador                           |
| `pases_recibidos`     | Pases completados recibidos por el jugador                            |
| `total_participacion` | Suma de pases dados y recibidos                                       |
| `conexiones_salida`   | Jugadores distintos a los que el jugador le pasó el balón             |
| `conexiones_entrada`  | Jugadores distintos de los que el jugador recibió pases               |

## Visualizaciones

Se genera una imagen por partido:

* `grafo_inglaterra_vs_iran.png`
* `grafo_inglaterra_vs_united_states.png`
* `grafo_inglaterra_vs_wales.png`

Cada grafo completo tiene más de 110 aristas y no se lee bien, por lo que en la imagen solo se dibujan las conexiones con **10 o más pases completados** (23 en Irán, 15 contra Estados Unidos y 12 contra Gales). El umbral es menor que el que se usaría para los tres partidos juntos porque cada partido tiene menos pases: con un umbral de 20, contra Gales quedaría una sola arista (el máximo es 21). El grosor de la flecha es proporcional al peso y cada flecha muestra su valor.

## Resultados por partido

### Inglaterra vs Iran

| Jugador         | Pases dados | Pases recibidos | Participación total |
| --------------- | ----------: | --------------: | ------------------: |
| John Stones     |         117 |             112 |                 229 |
| Luke Shaw       |         104 |              97 |                 201 |
| Jude Bellingham |          94 |              86 |                 180 |
| Declan Rice     |          92 |              85 |                 177 |
| Kieran Trippier |          84 |              74 |                 158 |

Conexiones más fuertes: Trippier -> Stones (29), Rice -> Stones (28), Stones -> Maguire (19), Stones -> Trippier (19), Maguire <-> Shaw (18 en cada sentido).

### Inglaterra vs United States

| Jugador         | Pases dados | Pases recibidos | Participación total |
| --------------- | ----------: | --------------: | ------------------: |
| John Stones     |          86 |              85 |                 171 |
| Harry Maguire   |          70 |              64 |                 134 |
| Luke Shaw       |          69 |              62 |                 131 |
| Kieran Trippier |          64 |              51 |                 115 |
| Declan Rice     |          56 |              47 |                 103 |

Conexiones más fuertes: Maguire -> Stones (35), Stones -> Maguire (21), Shaw -> Maguire (19), Rice -> Stones (16), Stones <-> Trippier (15 en cada sentido).

### Inglaterra vs Wales

| Jugador                | Pases dados | Pases recibidos | Participación total |
| ---------------------- | ----------: | --------------: | ------------------: |
| Harry Maguire          |          77 |              82 |                 159 |
| John Stones            |          75 |              72 |                 147 |
| Jordan Brian Henderson |          50 |              52 |                 102 |
| Luke Shaw              |          51 |              51 |                 102 |
| Jude Bellingham        |          47 |              48 |                  95 |

Conexiones más fuertes: Maguire -> Stones (21), Stones -> Maguire (19), Maguire -> Shaw (18), Stones -> Henderson (15), Pickford -> Maguire (15), Stones -> Walker (13).

## Interpretación

**El eje de la circulación fue muy parecido en los tres partidos.** John Stones es el primero o el segundo en participación en los tres partidos, Luke Shaw está en el top 5 de los tres, y Harry Maguire lidera contra Gales y es segundo contra Estados Unidos. Ningún delantero entra en el top 5 de ningún partido. Esto indica que Inglaterra construía desde atrás: los centrales y el lateral izquierdo sostenían la posesión y no solo defendían. La conexión Maguire-Stones, en ambos sentidos, aparece entre las conexiones fuertes de los tres grafos.

**Contra Irán (6-2) el juego fue más coral y más profundo en el mediocampo.** Fue el partido con más pases completados (746) y con más conexiones fuertes (23). Rice, Bellingham y Trippier están entre los cinco con más participación, y las dos conexiones más fuertes (Trippier -> Stones y Rice -> Stones) llegan a Stones desde el lateral y desde el pivote. El grafo muestra una red densa entre seis jugadores, típica de un equipo que domina el balón y tiene varias salidas por cada pase. Es compatible con un partido en el que Inglaterra dominó la posesión y ganó con holgura. Maguire, en cambio, participó menos que en los otros dos partidos (121).

**Contra Estados Unidos (0-0) la circulación se concentró entre los centrales.** Fue el partido con menos pases (500), menos nodos (14) y menos conexiones fuertes que Irán (15), y tiene la arista más pesada de todo el análisis: Maguire -> Stones con 35 pases. Bellingham sale del top 5 y Rice cae al quinto lugar con 103 de participación. La lectura futbolística es que Inglaterra mantuvo la pelota, pero le costó progresar por el centro: el balón se movió mucho entre los defensas y menos hacia los mediocampistas y delanteros, algo consistente con un 0-0 ante un rival ordenado y cerrado.

**Contra Gales (3-0) apareció el arquero y cambió la banda derecha.** Maguire pasa a ser el jugador con más participación (159), por encima de Stones, y Pickford -> Maguire (15) y Pickford -> Stones (11) entran entre las conexiones fuertes, señal de salida de balón desde el arquero. Kyle Walker y Henderson aparecen en las conexiones fuertes de este partido (Stones <-> Walker con 13 en cada sentido, Stones -> Henderson con 15), mientras que Trippier apenas participó (17 pases dados). Es el partido con menos conexiones fuertes (12) y una red menos densa en el mediocampo, con más peso en la línea defensiva.

**En conjunto**, el estilo de Inglaterra fue de posesión y salida ordenada desde atrás, con Stones y Maguire como eje. Lo que cambió entre partidos fue cuánto participó el mediocampo: mucho contra Irán, poco contra Estados Unidos, y con otra composición contra Gales. Ver los partidos por separado permite notar esto, cosa que un grafo consolidado promedia.

## Limitaciones del análisis

* Solo se consideraron pases completados; no se analizaron los incompletos, la posición de los jugadores, goles, tiros ni la presión del rival.
* El peso mide la cantidad de pases, no su longitud ni su importancia táctica.
* En cada imagen solo se muestran las conexiones de 10 o más pases, por lo que las relaciones ocasionales no se ven, aunque sí están en el grafo.
* Con solo tres partidos, las diferencias entre ellos pueden deberse al rival, a la alineación o al marcador, y no necesariamente a un cambio de estilo.

## Cómo ejecutar el proyecto

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el script:

```bash
python grafos_inglaterra.py
```

## Archivos generados

```text
grafo_inglaterra_vs_iran.png
grafo_inglaterra_vs_united_states.png
grafo_inglaterra_vs_wales.png
metricas_por_partido.csv
```

## Conclusión

Los grafos por partido muestran un equipo de posesión, con salida ordenada desde una línea defensiva muy participativa y con Stones y Maguire como eje de la circulación. El mediocampo tuvo un papel distinto en cada partido: fue protagonista contra Irán, quedó más aislado contra Estados Unidos y compartió peso con la defensa y el arquero contra Gales.
