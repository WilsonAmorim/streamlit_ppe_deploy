# import streamlit as st
# from datetime import datetime
# import pandas as pd



# st.set_page_config(
#     page_title="Dashboard PPE",
#     layout="wide",
#     page_icon="📊"
# )
# col1, col2 = st.columns([1, 5])

# with col1:
#     # Substitua 'logo.png' pelo caminho real da sua imagem (ex: 'assets/logo.png')
#     # Use use_container_width para o logo respeitar o tamanho da coluna
#     st.sidebar.image("imagens/logo.png", width=120)

# with col2:
#     st.title("Dashboard PPE - Projeto Primeiro Emprego")

# st.sidebar.markdown("SAEB/SGI/PPE")

# st.markdown(
#     """
#     O Aplicatico de Dashboard PPE visa fornecer insights valiosos sobre os convênios
#     firmados pelo PPE ao longo dos anos. Com uma interface interativa e visualizações
#     dinâmicas, este dashboard permite aos usuários explorar dados detalhados sobre os
#     convênios, facilitando a análise de tendências, desempenho e impacto dessas parcerias.
    
# """
# )

import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(
    page_title="Dashboard PPE",
    layout="wide",
    page_icon="📊"
)

# --- CONFIGURAÇÃO DO LOGO NO TOPO DO MENU ---
# O st.logo coloca a imagem automaticamente acima da lista de páginas
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_logo = os.path.join(diretorio_atual, "imagens", "logo.png",)
caminho_logo2 = os.path.join(diretorio_atual, "imagens", "logogov.png")

if os.path.exists(caminho_logo):
    st.logo(caminho_logo, icon_image=caminho_logo)
else:
    st.sidebar.warning("Logo não encontrado em: imagens/logo.png")

st.sidebar.image(caminho_logo2, width=400)
# --- CONTEÚDO DA BARRA LATERAL ---
col_esq, col_meio, col_dir = st.columns([1, 2, 1])

with col_meio:
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, width=400)
    else:
        st.error("Logo não encontrado.")
st.sidebar.markdown("\n**SAEB/SGI/PPE**")

# --- CONTEÚDO DA PÁGINA PRINCIPAL ---
st.title("Dashboard PPE - Projeto Primeiro Emprego")

st.markdown(
    """
    O Aplicativo de Dashboard PPE visa fornecer insights valiosos sobre os convênios
    firmados pelo PPE ao longo dos anos. Com uma interface interativa e visualizações
    dinâmicas, este dashboard permite aos usuários explorar dados detalhados sobre os
    convênios, facilitando a análise de tendências, desempenho e impacto dessas parcerias.
    """
)