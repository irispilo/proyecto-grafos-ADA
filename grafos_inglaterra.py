import pandas as pd

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