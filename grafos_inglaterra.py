import pandas as pd
import networkx as nx

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