import streamlit as st
import pandas as pd
# Importamos a função que você já tem no arquivo de charts
from charts.repasses import exibir_tabelas_por_lote_csv

# 1. Configuração da página (Deve ser o primeiro comando se for página única)
# Se esta página for carregada via menu, verifique se o set_page_config já existe no main
# st.set_page_config(page_title="Gestão de Repasses", layout="wide")

# 2. Cabeçalho específico da página de Finanças
st.set_page_config(page_title="Painel de Beneficiários", layout="wide")



st.title("📊 Painel de Beneficiários")

st.write("Acompanhamento detalhado dos repasses financeiros por lote e competência.")

# 3. Chamada da função que lê o seu CSV "Repasses.csv"
# Esta função já contém o st.expander e as métricas que configuramos
exibir_tabelas_por_lote_csv("Repasses.csv")

