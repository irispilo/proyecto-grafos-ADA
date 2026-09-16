# Proyecto de Grafos - Inglaterra Qatar 2022

## Objetivo

Analizar la red de pases de la selección de Inglaterra durante la fase de grupos del Mundial Qatar 2022, utilizando grafos dirigidos y ponderados para interpretar su estilo de juego.

El objetivo principal del proyecto no es únicamente construir el grafo, sino interpretar qué muestra la estructura de la red sobre la forma en que Inglaterra circuló el balón.

## Datos utilizados

Se utilizó el archivo `pases_inglaterra.csv`, que contiene registros de pases realizados por Inglaterra durante el Mundial Qatar 2022.

Para este análisis se filtraron únicamente los partidos de fase de grupos:

* Inglaterra vs Iran
* Inglaterra vs United States
* Inglaterra vs Wales

También se utilizaron únicamente los pases con resultado `Complete`, ya que estos representan pases que sí llegaron correctamente al receptor.

## Limpieza de datos

A partir del archivo original, se aplicaron los siguientes filtros:

1. Se conservaron únicamente los registros donde la columna `fase` fuera igual a `Group Stage`.
2. Se conservaron únicamente los registros donde la columna `resultado` fuera igual a `Complete`.
3. Se seleccionaron las columnas necesarias para construir el grafo:

* `match_id`
* `fecha`
* `oponente`
* `jugador_nombre`
* `receptor_nombre`
* `longitud_pase`

Después del filtrado, se obtuvo una base de datos con los pases completados de Inglaterra durante sus tres partidos de fase de grupos.

## Modelo de grafo

El grafo construido es un grafo dirigido y ponderado.

* Los nodos representan jugadores.
* Las aristas representan pases completados entre jugadores.
* La dirección de la arista indica quién hizo el pase y quién lo recibió.
* El peso de la arista representa la cantidad de pases completados entre dos jugadores.

Se eligió un grafo dirigido porque un pase tiene dirección. Por ejemplo, un pase de John Stones a Luke Shaw no representa lo mismo que un pase de Luke Shaw a John Stones.

Se eligió un grafo ponderado porque entre dos jugadores puede haber múltiples pases. El peso permite representar la fuerza de esa conexión dentro de la red.

## Construcción del grafo

Primero se agruparon los pases por jugador emisor y jugador receptor. Luego se contó cuántas veces ocurrió cada conexión.

Por ejemplo, si John Stones le pasó el balón varias veces a Harry Maguire, esa relación se representa como una sola arista con un peso igual al número total de pases completados entre ambos.

```text
John Stones -> Harry Maguire
peso = cantidad de pases completados
```

El grafo final contiene:

* 20 nodos
* 240 aristas

## Métricas utilizadas

Se calcularon las siguientes métricas para cada jugador:

| Métrica               | Descripción                                                           |
| --------------------- | --------------------------------------------------------------------- |
| `pases_dados`         | Cantidad de pases completados realizados por el jugador               |
| `pases_recibidos`     | Cantidad de pases completados recibidos por el jugador                |
| `total_participacion` | Suma de pases dados y pases recibidos                                 |
| `conexiones_salida`   | Cantidad de jugadores distintos a los que el jugador le pasó el balón |
| `conexiones_entrada`  | Cantidad de jugadores distintos de los que el jugador recibió pases   |

Estas métricas permiten identificar qué jugadores participaron más en la circulación del balón y qué tan conectados estuvieron dentro de la red.

## Resultados principales

Los jugadores con mayor participación total en la red fueron:

| Jugador                | Pases dados | Pases recibidos | Participación total |
| ---------------------- | ----------: | --------------: | ------------------: |
| John Stones            |         278 |             269 |                 547 |
| Luke Shaw              |         224 |             210 |                 434 |
| Harry Maguire          |         211 |             203 |                 414 |
| Declan Rice            |         193 |             168 |                 361 |
| Jude Bellingham        |         174 |             170 |                 344 |
| Kieran Trippier        |         165 |             135 |                 300 |
| Jordan Pickford        |          68 |              64 |                 132 |
| Mason Mount            |          59 |              69 |                 128 |
| Jordan Brian Henderson |          59 |              63 |                 122 |
| Marcus Rashford        |          40 |              61 |                 101 |

Las conexiones con mayor peso fueron:

| Conexión                       | Peso |
| ------------------------------ | ---: |
| Harry Maguire -> John Stones   |   73 |
| John Stones -> Harry Maguire   |   59 |
| Harry Maguire -> Luke Shaw     |   50 |
| Declan Rice -> John Stones     |   49 |
| Luke Shaw -> Harry Maguire     |   49 |
| Kieran Trippier -> John Stones |   44 |
| John Stones -> Kieran Trippier |   34 |
| Declan Rice -> Luke Shaw       |   30 |
| John Stones -> Declan Rice     |   30 |
| Jude Bellingham -> Luke Shaw   |   30 |

## Visualizaciones

El proyecto genera dos visualizaciones:

* `grafo_inglaterra.png`: grafo completo de pases.
* `grafo_inglaterra_conexiones_fuertes.png`: grafo filtrado con las conexiones más fuertes.

El grafo completo muestra todas las conexiones de pases completados entre jugadores. Sin embargo, debido a que contiene muchas aristas, puede verse saturado.

Por esa razón, también se generó una segunda visualización filtrada, mostrando únicamente las conexiones con peso mayor o igual a 20 pases completados. Este umbral se eligió porque deja únicamente las relaciones más repetidas de la red (por encima del rango típico de conexiones ocasionales), facilitando identificar las relaciones principales dentro de la red de pases.

## Interpretación

El grafo muestra que Inglaterra concentró gran parte de la circulación del balón en jugadores defensivos y mediocampistas. John Stones fue el jugador con mayor participación total, seguido por Luke Shaw, Harry Maguire, Declan Rice y Jude Bellingham.

La presencia de John Stones, Harry Maguire, Luke Shaw y Kieran Trippier entre los jugadores más participativos sugiere que Inglaterra construía frecuentemente desde la zona defensiva. Esto indica una intención de iniciar el juego desde atrás, utilizando a los defensas centrales y laterales como base para la circulación del balón.

Las conexiones más fuertes se dieron principalmente entre defensas centrales, laterales y mediocampistas. Destaca especialmente la relación entre Harry Maguire y John Stones, que fue la conexión más repetida en la red. También aparecen conexiones importantes entre Maguire y Luke Shaw, Declan Rice y John Stones, y Kieran Trippier y John Stones.

Desde el punto de vista futbolístico, esto puede interpretarse como un estilo de juego basado en la posesión, la salida ordenada desde atrás y la progresión controlada. Inglaterra no parece depender únicamente de pases directos hacia los delanteros, sino que mueve el balón por medio de sus defensas y mediocampistas antes de avanzar.

Declan Rice y Jude Bellingham también tuvieron una alta participación, lo que muestra que el mediocampo fue importante para conectar la defensa con zonas más adelantadas. Esto refuerza la idea de un equipo que busca mantener control del balón y avanzar mediante asociaciones entre jugadores cercanos.

En conjunto, el grafo sugiere que Inglaterra tuvo una estructura de circulación organizada, con fuerte participación de la línea defensiva y del mediocampo.

## Limitaciones del análisis

Este análisis se basa únicamente en pases completados durante la fase de grupos. No se consideraron pases incompletos, posiciones exactas de los jugadores durante todo el partido, contexto táctico detallado, goles, tiros o presión del rival.

Además, el peso de las aristas se calculó usando la cantidad de pases completados, no la longitud del pase ni la importancia táctica de cada acción.

A pesar de estas limitaciones, el grafo permite observar patrones generales de circulación del balón y detectar qué jugadores fueron más importantes dentro de la red de pases.

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

Al ejecutar el programa se generan los siguientes archivos:

```text
metricas_jugadores.csv
grafo_inglaterra.png
grafo_inglaterra_conexiones_fuertes.png
```

## Conclusión

La red de pases de Inglaterra en la fase de grupos del Mundial Qatar 2022 muestra un equipo con circulación ordenada, fuerte participación de defensas y mediocampistas, y una construcción frecuente desde atrás.

Los jugadores más importantes en la red fueron John Stones, Luke Shaw, Harry Maguire, Declan Rice y Jude Bellingham. La estructura del grafo sugiere un estilo basado en posesión, control y progresión gradual del balón.
