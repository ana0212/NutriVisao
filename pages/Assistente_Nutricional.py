import streamlit as st
import pandas as pd
import numpy as np
import time
from assistant import gerar_resposta_gemini_com_foco

st.set_page_config(
    page_title="Assistente",
    page_icon="🤖",
    layout="wide",
)

# --- Barra Lateral - Largura
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 370px;
            max-width: 370px;
        }
        [data-testid="stAppViewContainer"] {
            padding-left: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Conteúdo da página
st.title("Assistente Nutricional com IA")
st.subheader("💬 Tire suas dúvidas sobre alimentação e nutrição com base na Tabela INSA")

pergunta = st.text_area("Digite sua pergunta:")

if st.button("Responder") and pergunta:
    with st.spinner("Consultando o assistente..."):
        inicio = time.time()
        resposta = gerar_resposta_gemini_com_foco(pergunta)
        fim = time.time()
        tempo_resposta = fim - inicio

        st.success("Resposta:")
        st.markdown(f"💬 {resposta}")
        st.info(f"⏱️ Tempo de resposta: {tempo_resposta:.2f} segundos")

st.markdown(
    "Fonte: **Tabela da Composição de Alimentos. Instituto Nacional de Saúde Doutor Ricardo Jorge, I. P. - INSA. v 6.0 - 2023**"
)
