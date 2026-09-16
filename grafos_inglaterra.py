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

print(aristas.head(10))

G = nx.DiGraph()

for _, fila in aristas.iterrows():
    G.add_edge(
        fila["jugador_nombre"],
        fila["receptor_nombre"],
        weight=fila["peso"]
    )

print("Nodos:", G.number_of_nodes())
print("Aristas:", G.number_of_edges())

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
plt.show()