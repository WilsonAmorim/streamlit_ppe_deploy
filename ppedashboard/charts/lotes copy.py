import streamlit as st
import plotly.express as px
# from data.loader import carregar_dados

def mostrar_graficos_lotes(df):

    if "convenionome" not in df.columns:
        st.error("Coluna 'convenioNome' não encontrada.")
        return

    lotes = sorted(df["convenionome"].dropna().unique().tolist())

    if not lotes:
        st.warning("Nenhum lote encontrado.")
        return

    st.subheader("📦 Gráficos por Lote")

    abas = st.tabs(lotes)

    for tab, lote in zip(abas, lotes):
        with tab:
            df_lote = df[df["convenionome"] == lote]

            if df_lote.empty:
                st.write("Sem dados para este lote.")
                continue

            contagem = df_lote.groupby("ano").size().reset_index(name="quantidade")

            fig = px.bar(
                contagem,
                x="ano",
                y="quantidade",
                title=f"Quantidade por Ano – {lote}",
                text="quantidade"
            )

            fig.update_layout(xaxis_title="Ano", yaxis_title="Quantidade")
            fig.update_traces(textposition="outside")

            st.plotly_chart(fig, use_container_width=True)
    
         

