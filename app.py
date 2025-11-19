import streamlit as st
import requests
import pandas as pd
from collections import Counter

# 1. Configuração da Página
st.set_page_config(
page_title="Monitor Legislativo",
page_icon="⚖️",
layout="wide"
)

# 2. Barra Lateral (Sidebar) para Filtros
st.sidebar.header("Filtros de Pesquisa")
st.sidebar.info("Defina os parâmetros da sua busca jurídica.")

# Filtro de Ano
ano_atual = 2025
ano_selecionado = st.sidebar.slider("Ano de apresentação:", 2000, ano_atual, 2024)

# Quantidade de resultados
qtd_resultados = st.sidebar.number_input("Máximo de projetos:", min_value=5, max_value=50, value=10)

# 3. Título e Cabeçalho Principal
st.title("🏛️ Monitor Legislativo + Jurimetria")
st.markdown(f"""
Bem-vindo ao sistema de inteligência legislativa.
Pesquise abaixo para identificar projetos e analisar **quais partidos** estão legislando sobre o tema.
""")

st.divider()

# 4. Entrada de Dados (MÉTODO SIMPLIFICADO)
col1, col2 = st.columns([3, 1])

# Aqui usamos direto o objeto da coluna, sem precisar de indentação complicada
tema = col1.text_input("Digite o tema (ex: Direito Digital, Ambiental, Penal):")

# Botão na segunda coluna
col2.write("") # Espaço para alinhar
col2.write("")
botao_buscar = col2.button("🔍 Pesquisar", use_container_width=True)

# 5. Lógica da Pesquisa
if botao_buscar and tema:
with st.
