import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_grafico_contratacoes_ano(df):
    # No CSV a coluna se chama 'ConvenioNome', na API era 'lote'
    col_lote = "ConvenioNome"
    
    if col_lote not in df.columns:
        st.error(f"Coluna '{col_lote}' não encontrada no arquivo.")
        return

    st.subheader("📦 Contratações por Ano")
    
    # 1. Tratamento das Datas (Importante para bater com o histórico)
    df_c = df.copy()
    df_c['DataAdmissao'] = pd.to_datetime(df_c['DataAdmissao'], errors='coerce', dayfirst=True)
    df_c['ano'] = df_c['DataAdmissao'].dt.year
    
    # 2. Pegar os lotes únicos
    lotes = sorted(df_c[col_lote].dropna().unique().tolist())
    abas = st.tabs(lotes)

    for tab, lote in zip(abas, lotes):
        with tab:
            # Filtrar dados do lote
            df_lote = df_c[df_c[col_lote] == lote].copy()
            
            if not df_lote.empty:
                # DIFERENÇA AQUI: No CSV contamos as linhas (.size()), 
                # na API você somava a coluna 'quantidade'.
                df_ano = df_lote.groupby("ano").size().reset_index(name="quantidade")

                # Filtra o valor 0 e anos inválidos
                df_ano = df_ano[df_ano["ano"] > 0]
                
                # TRANSFORMA EM TEXTO (Como na sua API)
                df_ano["ano"] = df_ano["ano"].astype(int).astype(str)
                
                # Ordenar para garantir a sequência correta
                df_ano = df_ano.sort_values("ano")

                if not df_ano.empty:
                    fig = px.bar(
                        df_ano,
                        x="ano",
                        y="quantidade",
                        title=f"Total por Ano – {lote}",
                        text="quantidade",
                        color_discrete_sequence=["#003366"]
                    )
                    
                    # Configurações idênticas à sua API
                    fig.update_xaxes(type='category', categoryorder='category ascending')
                    fig.update_traces(textposition="outside")
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis_title="quantidade",
                        xaxis_title="ano"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Não há anos válidos registrados para este lote.")