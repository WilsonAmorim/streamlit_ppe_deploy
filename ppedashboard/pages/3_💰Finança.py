import streamlit as st
import pandas as pd
# Importamos a função que você já tem no arquivo de charts
from charts.repasses import exibir_tabelas_por_lote_csv

# 1. Configuração da página (Deve ser o primeiro comando se for página única)
# Se esta página for carregada via menu, verifique se o set_page_config já existe no main
# st.set_page_config(page_title="Gestão de Repasses", layout="wide")

# 2. Cabeçalho específico da página de Finanças
st.set_page_config(page_title="Painel de Beneficiários", layout="wide")

st.markdown("""
    <style>
    /* Esconde apenas os botões da direita (Share, Star, GitHub, etc.) */
    [data-testid="stToolbar"] {
        visibility: hidden;
        display: none;
    }

    /* Esconde especificamente o menu de 3 pontos (MainMenu) */
    #MainMenu {
        visibility: hidden;
    }

    /* Opcional: Remove o espaço vazio que fica no topo */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    /* Garante que o botão da barra lateral continue visível e funcional */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Beneficiários")

st.write("Acompanhamento detalhado dos repasses financeiros por lote e competência.")

# 3. Chamada da função que lê o seu CSV "Repasses.csv"
# Esta função já contém o st.expander e as métricas que configuramos
exibir_tabelas_por_lote_csv("Repasses.csv")

