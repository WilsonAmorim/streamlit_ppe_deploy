import streamlit as st
import plotly.express as px

def mostrar_grafico_ativos(df_resumo):
    st.markdown("---")
    st.subheader("🟢 Beneficários na Ativa por Lote")

    # Correção do erro: Usamos .empty para DataFrames
    if df_resumo is None or df_resumo.empty:
        st.info("Nenhum dado de ativos disponível para exibir.")
        return

    # Como a API manda dados separados por ANO, mas queremos o TOTAL POR LOTE:
    # Agrupamos novamente no Python para somar todos os anos
    df_agrupado_total = df_resumo.groupby(["lote"])["quantidade"].sum().reset_index()

    fig = px.bar(
        df_agrupado_total,
        x="lote",
        y="quantidade",
        title="Total de Ativos por Lote ",
        labels={"lote": "Lote/Convênio", "quantidade": "Total de Ativos"},
        text_auto=True,
        barmode="group", # Barras de M e F lado a lado
        color_discrete_map={"M": "#1f77b4", "F": "#e377c2", "N/I": "#7f7f7f"}
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)