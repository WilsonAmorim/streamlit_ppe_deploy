import streamlit as st
from data.loader import carregar_dados, carregar_resumo_ativos, carregar_resumo_generos
from charts.lotes import mostrar_graficos_lotes
from charts.sexo import  mostrar_grafico_sexo
from charts.ativos import mostrar_grafico_ativos
from data.loader import carregar_lotacao
from charts.lotacao import exibir_hierarquia_lotacao

import plotly.express as px
import os

st.set_page_config(
    page_title="Dashboard PPE",
    layout="wide",
    page_icon="📊"
)

with open("styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])  # 1 parte imagem / 4 partes título

with col1:
    st.image("imagens/logo.png", width=80)

with col2:
    st.markdown(
        "<h1 style='margin-top: 10px;'>PPE – BI Beneficiários</h1>",
        unsafe_allow_html=True
    )

# Carrega dados
df_resumo_ativos = carregar_resumo_ativos()
# Verifica se há dados
if df_resumo_ativos.empty:
    st.warning("Nenhum dado disponível para o Beneficiários.")
    # st.stop()

df = carregar_dados()
# Verifica se há dados
if df.empty:
    st.warning("Nenhum dado disponível para o Beneficiários.")
    # st.stop()

df_resumo_generos = carregar_resumo_generos()

if df_resumo_generos.empty:
    st.warning("Nenhum dado disponível para o Beneficiários. Genero")


df_lotacao = carregar_lotacao()
if df_lotacao.empty:
    st.warning("Nenhum dado disponível para o Beneficiários. Lotação")



mostrar_grafico_ativos(df_resumo_ativos)
mostrar_graficos_lotes(df)
mostrar_grafico_sexo(df_resumo_generos)
exibir_hierarquia_lotacao(df_lotacao)

