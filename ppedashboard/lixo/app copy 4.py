import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import re

API_URL = "http://localhost:5271/api/convenios"

response = requests.get(API_URL)
json_data = response.json()

# Detectar estrutura JSON
if isinstance(json_data, list):
    data = json_data
else:
    data = json_data.get("conveiosCadastrados", [])

df = pd.DataFrame(data)
df.columns = df.columns.str.lower()

# Criar coluna Ano
df["ano"] = pd.to_datetime(df["dataadmissao"], errors="coerce").dt.year

# Extrair número do lote para ordenar
def extrair_numero_lote(nome):
    numeros = re.findall(r'\d+', nome)
    return int(numeros[-1]) if numeros else 0

df["numero_lote"] = df["convenionome"].apply(extrair_numero_lote)
df = df.sort_values(by="numero_lote")

# Lista de lotes em ordem
lotes = df["convenionome"].dropna().astype(str).unique().tolist()

st.title("Dashboard por Lote e Ano")

# Criar abas dinamicamente
tabs = st.tabs(lotes)

# Renderizar um gráfico por aba
for tab, lote in zip(tabs, lotes):
    with tab:
        df_lote = df[df["convenionome"] == lote]

        contagem = df_lote.groupby("ano").size().reset_index(name="quantidade")

        fig = px.bar(contagem, x="ano", y="quantidade",
                     title=f"Quantidade por Ano - {lote}", text="quantidade")

        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)
