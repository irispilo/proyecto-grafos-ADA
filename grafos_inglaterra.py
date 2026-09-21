import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Solo se dibujan las conexiones con al menos este número de pases completados
UMBRAL_CONEXION_FUERTE = 10
TAMANO_NODO = 1600

# Carga y limpieza: fase de grupos, pases completados y columnas necesarias
df = pd.read_csv("pases_inglaterra.csv")

df_grupos = df[df["fase"] == "Group Stage"]
df_limpio = df_grupos[df_grupos["resultado"] == "Complete"][
    ["match_id", "fecha", "oponente", "jugador_nombre", "receptor_nombre"]
]

print("Pases en fase de grupos:", len(df_grupos))
print("Pases completos:", len(df_limpio))

metricas_partidos = []

# Un grafo dirigido y ponderado por cada partido de la fase de grupos
for (match_id, oponente, fecha), pases in df_limpio.groupby(["match_id", "oponente", "fecha"]):
    # Peso de cada arista = cantidad de pases completados de un emisor a un receptor
    aristas = (
        pases
        .groupby(["jugador_nombre", "receptor_nombre"])
        .size()
        .reset_index(name="peso")
    )
    G = nx.from_pandas_edgelist(
        aristas,
        source="jugador_nombre",
        target="receptor_nombre",
        edge_attr="peso",
        create_using=nx.DiGraph
    )

    print(f"\nInglaterra vs {oponente} ({fecha})")
    print("Pases completos:", len(pases))
    print("Nodos:", G.number_of_nodes())
    print("Aristas:", G.number_of_edges())

    # Métricas por jugador en este partido
    for jugador in G.nodes():
        dados = G.out_degree(jugador, weight="peso")
        recibidos = G.in_degree(jugador, weight="peso")
        metricas_partidos.append({
            "oponente": oponente,
            "jugador": jugador,
            "pases_dados": dados,
            "pases_recibidos": recibidos,
            "total_participacion": dados + recibidos,
            "conexiones_salida": G.out_degree(jugador),
            "conexiones_entrada": G.in_degree(jugador)
        })

    # Subgrafo con las conexiones fuertes: es el que se dibuja para que se lea bien
    G_fuerte = G.edge_subgraph(
        [(u, v) for u, v, peso in G.edges(data="peso") if peso >= UMBRAL_CONEXION_FUERTE]
    )

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G_fuerte, seed=42, k=1.5)

    # Grosor de la flecha proporcional al peso; la punta indica la dirección del pase
    grosor = [peso / 8 + 1 for _, _, peso in G_fuerte.edges(data="peso")]

    nx.draw_networkx_nodes(G_fuerte, pos, node_size=TAMANO_NODO, node_color="lightgreen")
    # node_size hace que la flecha termine en el borde del nodo y no quede tapada por él
    nx.draw_networkx_edges(
        G_fuerte,
        pos,
        width=grosor,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=20,
        node_size=TAMANO_NODO,
        edge_color="dimgray",
        alpha=0.8,
        connectionstyle="arc3,rad=0.25"
    )
    nx.draw_networkx_labels(G_fuerte, pos, font_size=8, font_weight="bold")
    nx.draw_networkx_edge_labels(
        G_fuerte,
        pos,
        edge_labels=nx.get_edge_attributes(G_fuerte, "peso"),
        font_size=7,
        connectionstyle="arc3,rad=0.25"
    )

    plt.title(f"Conexiones de {UMBRAL_CONEXION_FUERTE}+ pases - Inglaterra vs {oponente} ({fecha})")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"grafo_inglaterra_vs_{oponente.lower().replace(' ', '_')}.png", dpi=300)
    plt.close()

# Métricas de los tres partidos en un solo archivo
df_metricas = pd.DataFrame(metricas_partidos).sort_values(
    ["oponente", "total_participacion"],
    ascending=[True, False]
)
df_metricas.to_csv("metricas_por_partido.csv", index=False)
