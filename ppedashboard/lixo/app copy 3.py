import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://localhost:5271/api/convenios"

response = requests.get(API_URL)
json_data = response.json()

# Detecta estrutura do JSON
if isinstance(json_data, list):
    data = json_data
else:
    data = json_data.get("conveiosCadastrados", [])

df = pd.DataFrame(data)

# Normalizar nomes
df.columns = df.columns.str.lower()

# Criar coluna de Ano
df["ano"] = pd.to_datetime(df["datadmissao"], errors="coerce").dt.year
df = df.dropna(subset=["ano"])

# Lotes ordenados numericamente
lotes = sorted(df["convenionome"].unique(), key=lambda x: x.split()[-1].zfill(2))

st.title("Dashboard de Convênios por Lote e Ano")

# Criar abas para cada lote
tabs = st.tabs(lotes)

for tab, lote in zip(tabs, lotes):
    with tab:
        df_lote = df[df["convenionome"] == lote]

        if df_lote.empty:
            st.warning("Nenhum dado disponível para este lote.")
            continue

        # Agrupar por ano e contar
        contagem = df_lote.groupby("ano").size().reset_index(name="quantidade")

        # Gráfico de barras
        fig = px.bar(
            contagem,
            x="ano",
            y="quantidade",
            title=f"Quantidade por Ano - {lote}",
            text="quantidade"
        )

        fig.update_layout(xaxis_title="Ano", yaxis_title="Quantidade")
        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)
