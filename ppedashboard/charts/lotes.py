import streamlit as st
import plotly.express as px

def mostrar_graficos_lotes(df):
    col_lote = "lote"
    
    if col_lote not in df.columns:
        st.error(f"Coluna '{col_lote}' não encontrada.")
        return

    lotes = sorted(df[col_lote].dropna().unique().tolist())
    st.subheader("📦 Contratações por Ano")
    
    abas = st.tabs(lotes)

    for tab, lote in zip(abas, lotes):
        with tab:
            df_lote = df[df[col_lote] == lote].copy()
            
            if not df_lote.empty:
                # Agrupa e soma as quantidades por ano
                df_ano = df_lote.groupby("ano")["quantidade"].sum().reset_index()

                # Filtra o valor 0 que estava causando erro nas imagens
                df_ano = df_ano[df_ano["ano"] > 0]
                
                # TRANSFORMA EM TEXTO (Resolve o problema do eixo -0.4, 0, 0.4)
                df_ano["ano"] = df_ano["ano"].astype(str)

                if not df_ano.empty:
                    fig = px.bar(
                        df_ano,
                        x="ano",
                        y="quantidade",
                        title=f"Total por Ano – {lote}",
                        text="quantidade",
                        color_discrete_sequence=["#003366"]
                    )
                    
                    # Força o Plotly a tratar o eixo X como categorias individuais
                    fig.update_xaxes(type='category', categoryorder='category ascending')
                    fig.update_traces(textposition="outside")
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Não há anos válidos registrados para este lote.")