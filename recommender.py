import pandas as pd
import numpy as np
import pickle

# Carrega dados do INSA
insa_df = pd.read_csv("df_insa.csv")
insa_df_reduced = pd.read_csv("df_insa_reduced.csv")
insa_df = insa_df.fillna(0)

# Carrega matriz de similaridade já computada
with open("modelos/cosine_similarity.pkl", "rb") as f:
    sim_matrix = pickle.load(f)

# Mapeia classe detectada para índice no DataFrame
def get_index_by_class(class_name: str) -> int:
    mask = insa_df['Categorias do modelo'].str.contains(class_name, case=False, na=False)
    indices = insa_df[mask].index
    if len(indices) == 0:
        raise ValueError(f"Classe '{class_name}' não encontrada na coluna 'Categorias do alimento'")
    return indices[0] 

def get_nutritional_info(index: int) -> pd.Series:
    return insa_df_reduced.iloc[index]

def get_top_similar(index: int, top_n=3) -> pd.DataFrame:
    similarities = sim_matrix[index]
    similar_indices = np.argsort(similarities)[::-1]
    similar_indices = [i for i in similar_indices if i != index][:top_n]
    return insa_df_reduced.iloc[similar_indices]
