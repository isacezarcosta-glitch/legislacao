import streamlit as st
import requests
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="Monitor Legislativo",
    page_icon="⚖️",
    layout="centered"
)

# 2. Título e Cabeçalho
st.title("🏛️ Monitor Legislativo")
st.markdown("""
Bem-vindo ao buscador de **Proposições Legislativas**. 
Digite um tema jurídico abaixo para ver o que está tramitando na Câmara dos Deputados.
""")

st.divider() 

# 3. Entrada de Dados
tema = st.text_input("Digite uma palavra-chave (ex: Criptomoedas, Divórcio, IA):")
botao_buscar = st.button("Pesquisar Projetos")

# 4. Lógica da Pesquisa
if botao_buscar and tema:
    with st.spinner('Consultando a base de dados da Câmara...'):
        # URL base
        url_base = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
        
        parametros = {
            "keywords": tema,
            "ordem": "DESC",
            "ordenarPor": "id",
            "itens": 10 
        }
        
        try:
            resposta = requests.get(url_base, params=parametros)
            
            if resposta.status_code == 200:
                dados = resposta.json()['dados']
                
                if len(dados) > 0:
                    st.success(f"Encontramos {len(dados)} projetos recentes sobre '{tema}':")
                    
                    for projeto in dados:
                        # --- NOVA LÓGICA AQUI ---
                        # Para cada projeto, vamos buscar os autores
                        try:
                            url_autores = f"{url_base}/{projeto['id']}/autores"
                            resp_autores = requests.get(url_autores)
                            lista_autores = resp_autores.json()['dados']
                            
                            # Pega o primeiro nome da lista ou define como desconhecido
                            if lista_autores:
                                nome_autor = lista_autores[0]['nome']
                                # A API de autores as vezes não traz o partido direto nessa lista simples,
                                # então deixamos uma indicação padrão ou pegamos se disponível.
                                partido_autor = "Verificar no Link" 
                            else:
                                nome_autor = "Autor não identificado"
                                partido_autor = "-"
                                
                        except:
                            nome_autor = "Erro ao buscar autor"
                            partido_autor = "-"

                        # --- EXIBIÇÃO ATUALIZADA ---
                        with st.expander(f"📄 {projeto['siglaTipo']} {projeto['numero']}/{projeto['ano']}"):
                            # Usando markdown para formatar como você pediu
                            st.markdown(f"""
                            **Iniciador(a):** {nome_autor}  
                            **Partido:** {partido_autor}  
                            **Ementa:** {projeto['ementa']}  
                            """)
                            
                            link_camara = f"https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao={projeto['id']}"
                            st.markdown(f"**Link da tramitação:** [Clique aqui para acessar]({link_camara})")
                            
                else:
                    st.warning("Nenhum projeto encontrado com essa palavra-chave.")
            else:
                st.error("Erro ao conectar com a API da Câmara.")
                
        except Exception as e:
            st.error(f"Ocorreu um erro interno: {e}")

elif botao_buscar and not tema:
    st.warning("Por favor, digite um tema antes de pesquisar.")

st.markdown("---")
st.caption("Dados fornecidos pela API de Dados Abertos da Câmara dos Deputados.")
