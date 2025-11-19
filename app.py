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
ano_atual = 2025 # Atualizado para o ano corrente
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

# 4. Entrada de Dados (CORRIGIDO AQUI)
# Criamos as colunas e usamos o 'with' logo em seguida, garantindo a indentação correta
col1, col2 = st.columns([3, 1])

with col1:
tema = st.text_input("Digite o tema (ex: Direito Digital, Ambiental, Penal):")

with col2:
st.write("") # Espaço para alinhar verticalmente
st.write("")
botao_buscar = st.button("🔍 Pesquisar", use_container_width=True)

# 5. Lógica da Pesquisa
if botao_buscar and tema:
with st.spinner('Minerando dados do Congresso Nacional...'):
url_proposicoes = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"

parametros = {
"keywords": tema,
"ano": ano_selecionado,
"ordem": "DESC",
"ordenarPor": "id",
"itens": qtd_resultados
}

try:
resposta = requests.get
