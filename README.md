🍎 NutriVisão — Guia Nutricional Inteligente

Visão Geral

NutriVisão é uma plataforma interativa desenvolvida em Streamlit, que combina Visão Computacional, IA Generativa e dados oficiais de composição nutricional (INSA - Instituto Nacional de Saúde Doutor Ricardo Jorge, Portugal) para promover educação alimentar de forma acessível, prática e personalizada.

O sistema permite:

- Classificar alimentos a partir de imagens usando um modelo de deep learning (CNN).

- Explorar a composição nutricional oficial da Tabela INSA.

- Conversar com um assistente nutricional inteligente baseado em IA (Google Gemini).

- Visualizar dados e comparações em uma tabela e dashboard interativos.

**Demonstração**
- [Acesse o app online:](https://nutrivisao.streamlit.app)

**Relatório Técnico (TCC)**

- Para conhecer os detalhes metodológicos, resultados e fundamentação teórica deste projeto, consulte o relatório completo do Trabalho de Conclusão de Curso (TCC):
- [Acesse o Relatório Completo do TCC (PDF)]([https://link-do-relatorio.com](https://drive.google.com/file/d/1OfltMipkMKdVfBWYgpwNlvyVPPWb-7vv/view?usp=drive_link))  
- (Instituto Superior Manuel Teixeira Gomes – Curso de Engenharia Informática, 2025)*

**Estrutura do Projeto**
NutriVisao/
│
├── modelos/
│   └── melhor_modelo.keras               # Modelo CNN treinado (baixado automaticamente via Google Drive)
│   └── class_indices.pkl                 # Mapeamento das classes
│
├── insa_db/                              # Base vetorial (Chroma) com embeddings nutricionais
│
├── pages/
│   ├── Classificação_de_Imagem_e_Recomendações.py
│   ├── Assistente_Nutricional.py
│   └── Tabela_e_Dashboard_Interativos.py
│
├── assistant.py                          # Lógica do assistente com Gemini e LangChain
├── cnn_model.py                          # Pipeline de classificação e pré-processamento de imagens
├── recommender.py                        # Geração de recomendações baseadas em similaridade nutricional
├── df_insa_reduced.csv                   # Versão reduzida da Tabela INSA
├── requirements.txt                      # Dependências
├── .streamlit/secrets.toml               # Configurações de chaves e variáveis
└── Página_Inicial.py                     # Página principal do app

**Funcionalidades em Detalhe**
1. Classificação de Alimentos
- Envie uma imagem de um alimento.
- O modelo CNN baseado em ResNet50 realiza a inferência e identifica o tipo de alimento.
- A partir da classe predita, o sistema recomenda alimentos semelhantes em composição nutricional.

2. Exploração de Dados Nutricionais
- A base é a Tabela de Composição de Alimentos do INSA (v6.0 - 2023).
- Você pode pesquisar, filtrar e visualizar nutrientes de diferentes alimentos.
- A ferramenta inclui um dashboard interativo para comparar grupos alimentares.

3. Assistente Nutricional com IA
- Integrado ao Google Gemini.
- Utiliza embeddings semânticos (all-MiniLM-L6-v2) para contextualizar as perguntas.
- O assistente responde com base em dados oficiais e promove educação nutricional responsável.

**Instalação Local**
1️. Clone o repositório
git clone https://github.com/ana0212/NutriVisao.git
cd NutriVisao

2️. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

3️. Instale as dependências
pip install -r requirements.txt

4️. Configure o arquivo .streamlit/secrets.toml
Crie a pasta e o arquivo:
mkdir .streamlit
nano .streamlit/secrets.toml

E adicione sua chave da API Gemini:
GEMINI_API_KEY = "sua_chave_aqui"

5️. Execute o app localmente
streamlit run Página_Inicial.py

**Autora**
Ana Luiza @ana0212
Cientista de Dados Jr.
Contato: [LinkedIn](https://www.linkedin.com/in/ana-luiza-miranda-ds/)


**Fonte de Dados**
Tabela da Composição de Alimentos (v6.0, 2023)
Instituto Nacional de Saúde Doutor Ricardo Jorge, I. P. (INSA)
