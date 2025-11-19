import streamlit as st
import requests
import pandas as pd
from collections import Counter

# 1. Configuração da Página
st.set_page_config(
page_title="Monitor Legislativo",
page_icon="⚖️",
layout="wide" # Mudei para wide para caber o gráfico melhor
)

# 2. Barra Lateral (Sidebar) para Filtros
st.sidebar.header("Filtros de Pesquisa")
st.sidebar.info("Defina os parâmetros da sua busca jurídica.")

# Filtro de Ano
ano_atual = 2024 # Você pode atualizar isso conforme o ano
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

# 4. Entrada de Dados
col1, col2 = st.columns([3, 1]) # Cria colunas para ficar visualmente bonito
with col1:
tema = st.text_input("Digite o tema (ex: Direito Digital, Ambiental, Penal):")
with col2:
st.write("") # Espaço vazio para alinhar
st.write("")
botao_buscar = st.button("🔍 Pesquisar", use_container_width=True)

# 5. Lógica da Pesquisa
if botao_buscar and tema:
with st.spinner('Minerando dados do Congresso Nacional...'):
url_proposicoes = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"

# Agora os parâmetros usam as variáveis da barra lateral
parametros = {
"keywords": tema,
"ano": ano_selecionado,
"ordem": "DESC",
"ordenarPor": "id",
"itens": qtd_resultados
}

try:
resposta = requests.get(url_proposicoes, params=parametros)

if resposta.status_code == 200:
dados = resposta.json()['dados']

if len(dados) > 0:
st.success(f"Encontramos {len(dados)} projetos sobre '{tema}' em {ano_selecionado}.")

# Lista para guardar os partidos para o gráfico depois
lista_partidos = []

# Criação de Abas: Uma para a Lista, outra para o Gráfico
aba_lista, aba_grafico = st.tabs(["📜 Lista de Projetos", "📊 Análise Gráfica (Jurimetria)"])

with aba_lista:
for projeto in dados:
# --- LÓGICA DE AUTORES ---
nome_autor = "Autor não identificado"
partido_autor = "Outros" # Padrão para o gráfico não quebrar

try:
url_autores = f"{url_proposicoes}/{projeto['id']}/autores"
resp_autores = requests.get(url_autores)
lista_autores = resp_autores.json()['dados']

if lista_autores:
autor_principal = lista_autores[0]
nome_autor = autor_principal['nome']

if 'siglaPartido' in autor_principal and autor_principal['siglaPartido']:
partido_autor = autor_principal['siglaPartido']
elif 'uri' in autor_principal:
resp_deputado = requests.get(autor_principal['uri'])
dados_deputado = resp_deputado.json()['dados']
partido_autor = dados_deputado['ultimoStatus']['siglaPartido']
except:
partido_autor = "Não disponível"

# Adiciona o partido na lista para o gráfico
if partido_autor and partido_autor != "Não disponível":
lista_partidos.append(partido_autor)

# --- EXIBIÇÃO ---
with st.expander(f"📄 {projeto['siglaTipo']} {projeto['numero']}/{projeto['ano']} - {nome_autor} ({partido_autor})"):
st.markdown(f"**Ementa:** {projeto['ementa']}")
link_camara = f"https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao={projeto['id']}"
st.markdown(f"[🔗 Ver Tramitação Completa na Câmara]({link_camara})")

# --- ÁREA DO GRÁFICO ---
with aba_grafico:
st.markdown("### Distribuição Partidária")
st.write("Quais partidos estão propondo leis sobre esse assunto?")

if len(lista_partidos) > 0:
# Conta quantos projetos cada partido tem
contagem = pd.DataFrame.from_dict(Counter(lista_partidos), orient='index', columns=['Quantidade'])
st.bar_chart(contagem)
else:
st.info("Não foi possível identificar os partidos para gerar o gráfico.")

else:
st.warning(f"Nenhum projeto encontrado sobre '{tema}' no ano de {ano_selecionado}.")
else:
st.error("Erro ao conectar com a API da Câmara.")

except Exception as e:
st.error(f"Ocorreu um erro interno: {e}")

elif botao_buscar and not tema:
st.warning("Por favor, digite um tema antes de pesquisar.")

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para a disciplina de Programação para Advogados.")
