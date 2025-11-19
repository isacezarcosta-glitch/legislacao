import streamlit as st
import requests

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
Digite um tema jurídico abaixo para ver os temas de PL em tramitação na Câmara dos Deputados.
""")

st.divider() 

# 3. Entrada de Dados
tema = st.text_input("Digite uma palavra-chave (ex: Criptomoedas, Divórcio, IA):")
botao_buscar = st.button("Pesquisar Projetos")

# 4. Lógica da Pesquisa
if botao_buscar and tema:
    with st.spinner('Consultando a base de dados da Câmara...'):
        # URL base da API
        url_proposicoes = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
        
        parametros = {
            "keywords": tema,
            "ordem": "DESC",
            "ordenarPor": "id",
            "itens": 10 
        }
        
        try:
            resposta = requests.get(url_proposicoes, params=parametros)
            
            if resposta.status_code == 200:
                dados = resposta.json()['dados']
                
                if len(dados) > 0:
                    st.success(f"Encontramos {len(dados)} projetos recentes sobre '{tema}':")
                    
                    for projeto in dados:
                        # --- LÓGICA DE AUTORES (Mantida a correção do Partido) ---
                        nome_autor = "Autor não identificado"
                        partido_autor = "Não identificado" 
                        
                        try:
                            url_autores = f"{url_proposicoes}/{projeto['id']}/autores"
                            resp_autores = requests.get(url_autores)
                            lista_autores = resp_autores.json()['dados']
                            
                            if lista_autores:
                                autor_principal = lista_autores[0]
                                nome_autor = autor_principal['nome']
                                
                                # Tenta pegar a sigla direta ou busca na URI do deputado
                                if 'siglaPartido' in autor_principal and autor_principal['siglaPartido']:
                                    partido_autor = autor_principal['siglaPartido']
                                elif 'uri' in autor_principal:
                                    resp_deputado = requests.get(autor_principal['uri'])
                                    dados_deputado = resp_deputado.json()['dados']
                                    partido_autor = dados_deputado['ultimoStatus']['siglaPartido']
                        except:
                            partido_autor = "Não disponível"

                        # --- EXIBIÇÃO ---
                        with st.expander(f"📄 {projeto['siglaTipo']} {projeto['numero']}/{projeto['ano']}"):
                            st.markdown(f"""
                            **Iniciador(a):** {nome_autor}  
                            **Partido político:** {partido_autor}  
                            **Ementa:** {projeto['ementa']}
                            """)
                            
                            # --- AQUI ESTÁ A MUDANÇA QUE VOCÊ PEDIU ---
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

st.markdown("---")
st.caption("Dados fornecidos pela API de Dados Abertos da Câmara dos Deputados.")
