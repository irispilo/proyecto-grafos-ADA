import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

df = pd.read_csv("pases_inglaterra.csv")

df_grupos = df[df["fase"] == "Group Stage"].copy()
df_completos = df_grupos[df_grupos["resultado"] == "Complete"].copy()

columnas = [
    "match_id",
    "fecha",
    "oponente",
    "jugador_nombre",
    "receptor_nombre",
    "longitud_pase"
]

df_limpio = df_completos[columnas].copy()

print("Pases en fase de grupos:", len(df_grupos))
print("Pases completos:", len(df_limpio))
print(df_limpio.head())

aristas = (
    df_limpio
    .groupby(["jugador_nombre", "receptor_nombre"])
    .size()
    .reset_index(name="peso")
    .sort_values("peso", ascending=False)
)

# para grafo 2
print(aristas.head(10))

aristas_fuertes = aristas[aristas["peso"] >= 20].copy()

print("\nConexiones fuertes:")
print(aristas_fuertes)


G = nx.DiGraph()

G_fuertes = nx.DiGraph()

for _, fila in aristas_fuertes.iterrows():
    G_fuertes.add_edge(
        fila["jugador_nombre"],
        fila["receptor_nombre"],
        weight=fila["peso"]
    )
#------


for _, fila in aristas.iterrows():
    G.add_edge(
        fila["jugador_nombre"],
        fila["receptor_nombre"],
        weight=fila["peso"]
    )

print("Nodos:", G.number_of_nodes())
print("Aristas:", G.number_of_edges())

metricas = []

for jugador in G.nodes():
    pases_dados = G.out_degree(jugador, weight="weight")
    pases_recibidos = G.in_degree(jugador, weight="weight")
    conexiones_salida = G.out_degree(jugador)
    conexiones_entrada = G.in_degree(jugador)

    metricas.append({
        "jugador": jugador,
        "pases_dados": pases_dados,
        "pases_recibidos": pases_recibidos,
        "total_participacion": pases_dados + pases_recibidos,
        "conexiones_salida": conexiones_salida,
        "conexiones_entrada": conexiones_entrada
    })

df_metricas = pd.DataFrame(metricas)

df_metricas = df_metricas.sort_values(
    "total_participacion",
    ascending=False
)

print("\nMetricas principales:")
print(df_metricas.head(10))


df_metricas.to_csv("metricas_jugadores.csv", index=False)

#visualización:

plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G, seed=42, k=0.7)

pesos = [G[u][v]["weight"] for u, v in G.edges()]
grosor_aristas = [peso / 5 for peso in pesos]

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=1200,
    node_color="lightblue"
)

nx.draw_networkx_edges(
    G,
    pos,
    width=grosor_aristas,
    arrows=True,
    arrowstyle="->",
    arrowsize=15,
    edge_color="gray",
    alpha=0.6
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=8,
    font_weight="bold"
)

plt.title("Grafo de pases completados - Inglaterra, fase de grupos")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafo_inglaterra.png", dpi=300)
plt.close()


#segunda visualización

plt.figure(figsize=(14, 10))

pos_fuertes = nx.spring_layout(G_fuertes, seed=42, k=0.9)

pesos_fuertes = [G_fuertes[u][v]["weight"] for u, v in G_fuertes.edges()]
grosor_fuertes = [peso / 8 for peso in pesos_fuertes]

nx.draw_networkx_nodes(
    G_fuertes,
    pos_fuertes,
    node_size=1600,
    node_color="lightcoral"
)

nx.draw_networkx_edges(
    G_fuertes,
    pos_fuertes,
    width=grosor_fuertes,
    arrows=True,
    arrowstyle="->",
    arrowsize=18,
    edge_color="gray",
    alpha=0.7
)

nx.draw_networkx_labels(
    G_fuertes,
    pos_fuertes,
    font_size=8,
    font_weight="bold"
)

etiquetas_aristas = nx.get_edge_attributes(G_fuertes, "weight")

nx.draw_networkx_edge_labels(
    G_fuertes,
    pos_fuertes,
    edge_labels=etiquetas_aristas,
    font_size=7
)

plt.title("Conexiones fuertes de pases - Inglaterra, fase de grupos")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafo_inglaterra_conexiones_fuertes.png", dpi=300)
plt.close()

