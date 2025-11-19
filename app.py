import streamlit as st
import requests
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="Monitor Legislativo",
    page_icon="",
    layout="centered"
)

# 2. Título e Cabeçalho
st.title("Monitor Legislativo")
st.markdown("""
Bem-vindo ao buscador de **Proposições Legislativas**. 
Digite um tema jurídico abaixo para ver os temas de Projetos de Lei que estão tramitando na Câmara dos Deputados.
""")

st.divider() # Linha divisória visual

# 3. Entrada de Dados (Input do Usuário)
tema = st.text_input("Digite uma palavra-chave (ex: Criptomoedas, Divórcio, IA):")
botao_buscar = st.button("Pesquisar Projetos")

# 4. Lógica da Pesquisa (Conexão com a API)
if botao_buscar and tema:
    with st.spinner('Consultando a base de dados da Câmara...'):
        # URL oficial da API da Câmara dos Deputados
        url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
        
        # Parâmetros para filtrar a busca
        parametros = {
            "keywords": tema,
            "ordem": "DESC",
            "ordenarPor": "id",
            "itens": 10  # Traz apenas os 10 resultados mais recentes
        }
        
        try:
            # Fazendo a requisição (o "pedido" para a API)
            resposta = requests.get(url, params=parametros)
            
            if resposta.status_code == 200:
                dados = resposta.json()['dados']
                
                if len(dados) > 0:
                    st.success(f"Encontramos {len(dados)} projetos recentes sobre '{tema}':")
                    
                    # 5. Exibição dos Resultados
                    for projeto in dados:
                        # Cria um cartão expansível para cada lei
                        with st.expander(f"📄 {projeto['siglaTipo']} {projeto['numero']}/{projeto['ano']}"):
                            st.markdown(f"**Ementa (Resumo):**")
                            st.write(projeto['ementa'])
                            
                            # Verifica se existe link para o inteiro teor
                            # A API as vezes retorna apenas a uri, então montamos o link da câmara
                            link_camara = f"https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao={projeto['id']}"
                            st.markdown(f"[🔗 Ver Tramitação Completa na Câmara]({link_camara})")
                else:
                    st.warning("Nenhum projeto encontrado com essa palavra-chave.")
            else:
                st.error("Erro ao conectar com a API da Câmara.")
                
        except Exception as e:
            st.error(f"Ocorreu um erro interno: {e}")

elif botao_buscar and not tema:
    st.warning("Por favor, digite um tema antes de pesquisar.")

# 6. Rodapé
st.markdown("---")
st.caption("Dados fornecidos pela API de Dados Abertos da Câmara dos Deputados.")
