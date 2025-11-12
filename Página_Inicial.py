import streamlit as st

# ================== Configuração ==================
st.set_page_config(
    page_title="NutriVisão - Classificador de Alimentos",
    page_icon="🍎",
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

# ================== Cabeçalho ==================
st.title("NutriVisão")
st.subheader("Guia Nutricional Inteligente")

st.markdown("---")

# ================== Introdução ==================
st.markdown(
        """
        **NutriVisão** combina **inteligência artificial** e **dados nutricionais oficiais** para ajudar você a **reconhecer alimentos**, conhecer seus nutrientes e **descobrir opções semelhantes** para variar sua dieta de forma saudável.
        Além disso, oferece um **assistente nutricional inteligente**, uma **tabela interativa** para explorar a composição de alimentos e um **dashboard** visual para acompanhar e comparar informações de forma prática.

        ### O que você pode fazer aqui:
        - **Classificar alimentos** a partir de imagens e **Receber recomendações** de alimentos similares  
        - **Explorar informações nutricionais** com base na **Tabela INSA**  
        - **Conversar com um assistente** treinado para responder dúvidas sobre nutrição

        **Fonte oficial:**  
        [Fonte: Tabela da Composição de Alimentos. Instituto Nacional de Saúde Doutor Ricardo Jorge, I. P.- INSA. v 6.0 - 2023](https://portfir-insa.min-saude.pt/)
        """
    )

st.markdown("---")

# ================== Fluxo de uso ==================
st.header("Como usar")
st.markdown(
    """
    1. **Classifique um alimento** enviando uma imagem  e **Explore alimentos semelhantes** com base na composição 
    2. **Veja as informações nutricionais** detalhadas  
    3. **Converse com o assistente** para tirar dúvidas  
    """
)

st.markdown("---")
st.info("Use o menu ao lado para navegar entre as páginas da aplicação.")
