import streamlit as st
from PIL import Image
import os
from cnn_model import classificar_imagem
from recommender import get_index_by_class, get_nutritional_info, get_top_similar, insa_df

st.set_page_config(
    page_title="Classificação e Recomendações",
    page_icon="🔍",
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

# --- Estado para forçar reset do uploader ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

st.title("Upload de Imagem e Recomendações Nutricionais")

st.markdown("""
**📸 Boas práticas para envio da imagem:**
- Use **fundo branco ou uniforme**, sem objetos extras  
- Fotografe **apenas um alimento** por vez  
- Evite sombras fortes ou iluminação irregular  
- Centralize o alimento na imagem  
- Utilize imagens **nítidas** e bem focadas  
""")

uploaded_file = st.file_uploader(
    "Arraste e solte sua imagem aqui ou clique para selecionar",
    type=["jpg", "jpeg", "png"],
    key=f"uploader_{st.session_state.uploader_key}"
)

classe_detetada = None

if uploaded_file is not None:
    try:
        # tenta abrir a imagem
        img = Image.open(uploaded_file)
        st.image(img, caption="Imagem enviada", use_container_width=True)

        # --- bloco de classificação ---
        with st.spinner("🔍 Classificando imagem..."):
            classe_detetada = classificar_imagem(img)

        index = get_index_by_class(classe_detetada)
        info = get_nutritional_info(index)

        st.markdown("### 📋 Informações nutricionais do alimento detetado:")
        st.dataframe(info.to_frame().T, use_container_width=True)

        st.markdown("---")
        st.subheader("Alimentos mais similares nutricionalmente")

        top_n = st.slider("Quantos alimentos semelhantes deseja visualizar?", 1, 10, 3)

        similares = get_top_similar(index, top_n=top_n)

        st.dataframe(similares.reset_index(drop=True), use_container_width=True)

    except Exception:
        # Mensagem de erro
        st.error("❌ A imagem enviada não é compatível ou está corrompida.")

    # --- Botão de reset, sempre visível após mensagem ou classificação ---
    if st.button("🔄 Fazer nova classificação"):
        for k in ["classe_detetada", "index", "info", "similares"]:
            st.session_state.pop(k, None)
        st.session_state.uploader_key += 1
        st.rerun()

st.markdown("Fonte: Tabela da Composição de Alimentos. Instituto Nacional de Saúde Doutor Ricardo Jorge, I. P.- INSA. v 6.0 - 2023")