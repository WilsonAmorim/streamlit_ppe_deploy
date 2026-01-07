import streamlit as st
import pandas as pd

def exibir_tabelas_por_lote(df):
    st.markdown("---")
    st.subheader("📋 Detalhamento Financeiro por Lote - Repasses")

    if df.empty:
        st.warning("Nenhum dado de repasse disponível para exibição.")
        return

    # Padronização de nome da coluna de lote
    col_lote = "nomelote" if "nomelote" in df.columns else "lote"
    lotes = sorted(df[col_lote].unique())

    # Função para formatar moeda padrão brasileiro (R$ 1.234,56)
    def formatar_moeda_br(val):
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    for lote in lotes:
        with st.expander(f"📦 {lote.upper()}", expanded=False):
            # Filtra dados do lote atual
            df_lote = df[df[col_lote] == lote].copy()
            
            # 1. Métrica de Total (Formatada igual à tabela)
            total_valor = df_lote['valor'].sum()
            st.metric(label="Total Repassado", value=formatar_moeda_br(total_valor))

            # 2. Formatação da Data (Tratando o erro 1900-01-01)
            if 'datapagamento' in df_lote.columns:
                df_lote['datapagamento'] = pd.to_datetime(df_lote['datapagamento'], errors='coerce')
                df_lote['datapagamento'] = df_lote['datapagamento'].apply(
                    lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) and x.year > 1900 else "Pendente"
                )

            # 3. Formatação do Valor na Tabela
            if 'valor' in df_lote.columns:
                df_lote['valor'] = df_lote['valor'].apply(formatar_moeda_br)

            # 4. Seleção das colunas que queremos mostrar (sem deletar as que vamos usar)
            # Removemos apenas a coluna do Lote, pois ela já é o título do expander
            colunas_visiveis = [c for c in df_lote.columns if c != col_lote]
            df_exibir = df_lote[colunas_visiveis]
            
            st.dataframe(
                df_exibir,
                column_config={
                    "periodo": "Competência",
                    "valor": "Valor",
                    "status": "Situação",
                    "delay": "Atraso",
                    "datapagamento": "Data de Pagto",
                    "valorrepasse": "Referência"
                },
                use_container_width=True,
                hide_index=True
            )