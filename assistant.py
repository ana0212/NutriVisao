import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- Configuração da API Gemini ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Funções auxiliares ---
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def linha_para_texto(row):
    return "\n".join([f"{col}: {row[col]}" for col in row.index])

# --- Carregar DataFrame e gerar lista de documentos (sempre disponível) ---
df = pd.read_csv("df_insa_reduced.csv")
docs = [
    Document(page_content=linha_para_texto(row), metadata={"alimento": row["Nome do alimento"]})
    for _, row in df.iterrows()
]

# --- Criar ou carregar o banco vetorial ---
try:
    db = Chroma(persist_directory="insa_db", embedding_function=embedding_function)
    _ = db.similarity_search("teste", k=1)
except Exception:
    db = Chroma.from_documents(docs, embedding=embedding_function, persist_directory="insa_db")
    db.persist()

def detectar_alimentos_na_pergunta(pergunta):
    encontrados = []
    for doc in docs:
        nome_alimento = doc.metadata.get("alimento", "").lower()
        if nome_alimento and nome_alimento in pergunta.lower():
            encontrados.append(nome_alimento)
    return list(set(encontrados))  # remove duplicados

def buscar_contexto_similar_com_foco(pergunta, k=6):
    embedding_pergunta = embedding_function.embed_query(pergunta)
    docs_similares = db.similarity_search_by_vector(embedding_pergunta, k=k)

    alimentos_mencionados = detectar_alimentos_na_pergunta(pergunta)

    # adiciona cada alimento mencionado ao contexto
    for alimento in alimentos_mencionados:
        doc_alvo = next(
            (doc for doc in docs if alimento in doc.metadata.get("alimento", "").lower()),
            None
        )
        if doc_alvo and doc_alvo not in docs_similares:
            docs_similares.insert(0, doc_alvo)

    return "\n\n".join([doc.page_content for doc in docs_similares])

# --- Consulta à Gemini ---
def gerar_resposta_gemini_com_foco(pergunta):
    contexto = buscar_contexto_similar_com_foco(pergunta)
    prompt = f"""
Você é um assistente nutricional com acesso à Tabela INSA de composição de alimentos.

Abaixo estão os dados nutricionais de alimentos relevantes da Tabela INSA:
{contexto}

Com base apenas nessas informações, responda de forma clara e educativa à seguinte pergunta:
{pergunta}

Cada valor nutricional corresponde ao mg por 100 g de parte edível com exceção do grupo Bebidas alcoólicas (nível 1) cujos valores são expressos por 100 ml de parte edível.
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
