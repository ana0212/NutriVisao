import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import textwrap

st.set_page_config(
    page_title="Tabela e Dashboard Interativos",
    page_icon="📊",
    layout="wide",
)

# Barra Lateral - Largura
st.markdown(
    """
    <style>
        /* Reduz a largura da barra lateral */
        [data-testid="stSidebar"] {
            min-width: 370px;
            max-width: 370px;
        }

        /* Ajusta o conteúdo para ocupar mais espaço */
        [data-testid="stAppViewContainer"] {
            padding-left: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== Tabela Interativa ==================
@st.cache_data
def load_data():
    return pd.read_csv("df_insa_reduced.csv")

st.title("Filtro Interativo da Tabela INSA")
df = load_data()
df_filtrado = df.copy()

st.markdown("### Aplique filtros na tabela:")
df = load_data()
df_filtrado = df.copy()

# --- Filtro Nome do alimento (multiselect com opções filtradas) ---
nome_opcoes = sorted(df_filtrado["Nome do alimento"].dropna().unique())
nome_selecionados = st.multiselect("Nome do alimento", nome_opcoes)
if nome_selecionados:
    df_filtrado = df_filtrado[df_filtrado["Nome do alimento"].isin(nome_selecionados)]

# --- Filtro Nível 1 ---
nivel_1_opcoes = sorted(df["Nível 1"].dropna().unique())
nivel_1_selecionados = st.multiselect("Nível 1", nivel_1_opcoes)

if nivel_1_selecionados:
    df_filtrado = df_filtrado[df_filtrado["Nível 1"].isin(nivel_1_selecionados)]
    # Nível 2 limitado pelo Nível 1
    nivel_2_opcoes = sorted(df_filtrado["Nível 2"].dropna().unique())
else:
    nivel_2_opcoes = sorted(df["Nível 2"].dropna().unique())

# --- Filtro Nível 2 ---
nivel_2_selecionados = st.multiselect("Nível 2", nivel_2_opcoes)

if nivel_2_selecionados:
    df_filtrado = df_filtrado[df_filtrado["Nível 2"].isin(nivel_2_selecionados)]
    # Nível 3 limitado pelo Nível 2 (e Nível 1, pois já filtramos)
    nivel_3_opcoes = sorted(df_filtrado["Nível 3"].dropna().unique())
else:
    nivel_3_opcoes = sorted(df_filtrado["Nível 3"].dropna().unique())

# --- Filtro Nível 3 ---
nivel_3_selecionados = st.multiselect("Nível 3", nivel_3_opcoes)
if nivel_3_selecionados:
    df_filtrado = df_filtrado[df_filtrado["Nível 3"].isin(nivel_3_selecionados)]

# --- Filtro Energia [kcal] ---
min_kcal = float(df["Energia [kcal]"].min())
max_kcal = float(df["Energia [kcal]"].max())
faixa_kcal = st.slider("Energia [kcal]", min_value=min_kcal, max_value=max_kcal, value=(min_kcal, max_kcal))
df_filtrado = df_filtrado[df_filtrado["Energia [kcal]"].between(faixa_kcal[0], faixa_kcal[1])]

st.markdown("### Resultado filtrado:")
st.dataframe(df_filtrado, use_container_width=True)

# ================== Dashboard ==================
st.title("Dashboard Interativo")

# ================== Gráfico 1: Distribuição de Energia ==================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df_filtrado,
        x="Energia [kcal]",
        nbins=20,
        histfunc='count',
        title="Distribuição de Energia [kcal]",
        color_discrete_sequence=["#FF9800"]
    )
    fig1.update_layout(yaxis_title="Contagem") 
    st.plotly_chart(fig1, use_container_width=True)

# ================== Gráfico 2: Energia vs Proteína ==================
with col2:
    df_prot = df_filtrado.dropna(subset=["Energia [kcal]", "Proteínas  [g]"])
    if len(df_prot) >= 2:
        fig2 = px.scatter(
            df_prot,
            x="Energia [kcal]",
            y="Proteínas  [g]",
            hover_name="Nome do alimento",
            title="Energia vs Proteína",
            labels={
                "Energia [kcal]": "Energia (kcal)",
                "Proteínas  [g]": "Proteína (g)"
            },
            color="Proteínas  [g]",
            color_continuous_scale="Inferno"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ================== Gráfico 3: Contagem por Categoria ==================
def wrap_labels(labels, width=20):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

if "Nível 1" in df_filtrado.columns:
    categoria_counts = df_filtrado["Nível 1"].value_counts().reset_index()
    categoria_counts.columns = ["Categoria", "Quantidade"]

    # Quebra nomes longos
    categoria_counts["Categoria_wrapped"] = wrap_labels(categoria_counts["Categoria"], width=20)

    fig3 = px.bar(
        categoria_counts,
        x="Quantidade",
        y="Categoria_wrapped",
        orientation="h",
        title="Quantidade de Alimentos por Categoria (Nível 1)",
        labels={"Categoria_wrapped": "Categoria", "Quantidade": "Contagem"},
        color_discrete_sequence=["#4CAF50"],
        height=700  # aumentar altura para melhor leitura
    )
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

