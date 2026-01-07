import streamlit as st

def exibir_hierarquia_lotacao(df):
    st.markdown("---")
    st.subheader("📍 Tabela por Lote, Município e  Posto de Trabalho")

    if df.empty:
        st.info("Nenhum dado de lotação disponível.")
        return

    # Padronização de nomes das colunas (baseado no seu C#)
    col_lote = 'lote'
    col_mun = 'lotacao'
    col_posto = 'posto'
    col_qtd = 'quantidade'

    # 1º NÍVEL: Agrupamento por Lote
    lotes = sorted(df[col_lote].unique())

    for lote in lotes:
        df_lote = df[df[col_lote] == lote]
        total_lote = df_lote[col_qtd].sum()
        
        # Expander do Lote (Nível Pai)
        with st.expander(f"📦 {lote.upper()} (Total: {total_lote})"):
            
            # 2º NÍVEL: Agrupamento por Município dentro do Lote
            municipios = sorted(df_lote[col_mun].unique())
            
            for mun in municipios:
                df_mun = df_lote[df_lote[col_mun] == mun]
                total_mun = df_mun[col_qtd].sum()
                
                # Expander do Município (Nível Filho)
                # O parâmetro 'expanded=False' garante que ele comece fechado
                with st.expander(f"🏠 Município: {mun} (Total: {total_mun})"):
                    
                    # 3º NÍVEL: Lista de Postos de Trabalho
                    # Formatamos para uma visualização limpa
                    df_postos = df_mun[[col_posto, col_qtd]].sort_values(by=col_qtd, ascending=False)
                    
                    # Exibe a tabela final
                    st.dataframe(
                        df_postos,
                        column_config={
                            col_posto: "Posto de Trabalho",
                            col_qtd: st.column_config.NumberColumn("Qtd", format="%d")
                        },
                        use_container_width=True,
                        hide_index=True
                    )