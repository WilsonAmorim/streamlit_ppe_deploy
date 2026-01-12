import streamlit as st
import pandas as pd
import os

def exibir_tabelas_por_lote_csv(nome_arquivo="repasses.csv"):
    st.markdown("---")
    st.subheader("📋 Detalhamento Financeiro por Lote - Repasses")

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio_atual, "..", "data", nome_arquivo)
    
    if not os.path.exists(caminho):
        st.error(f"⚠️ Arquivo não encontrado: {caminho}")
        return

    try:
        # Lendo o CSV (tratando ponto como decimal)
        df = pd.read_csv(caminho, sep=',') 
        df.columns = [c.lower() for c in df.columns]

        # Converte para numérico garantindo que a soma seja matemática e não de texto
        df['valor'] = pd.to_numeric(df['valor'].astype(str).str.replace(',', '.'), errors='coerce')

        def formatar_moeda_br(val):
            try:
                return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return "R$ 0,00"

        col_lote = "nomelote"
        lotes_unicos = sorted(df[col_lote].unique())

        for lote in lotes_unicos:
            with st.expander(f"📦 {str(lote).upper()}", expanded=False):
                # Filtra o lote e remove duplicatas de ID para a soma
                df_lote = df[df[col_lote] == lote].drop_duplicates(subset=['id']).copy()
                
                # Cálculo do Total em destaque
                total_valor = df_lote['valor'].sum()
                st.write("Total Repassado")
                st.markdown(f"## {formatar_moeda_br(total_valor)}")

                # Formatações para a Tabela
                if 'datapagamento' in df_lote.columns:
                    df_lote['datapagamento'] = pd.to_datetime(df_lote['datapagamento'], errors='coerce')
                    df_lote['datapagamento'] = df_lote['datapagamento'].apply(
                        lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) and x.year > 1900 else "Pendente"
                    )

                df_lote['valor_exibicao'] = df_lote['valor'].apply(formatar_moeda_br)

                # REORDENAÇÃO E SELEÇÃO (Referência primeiro, remove ID e NomeLote)
                # Definimos a ordem exata das colunas que queremos mostrar
                ordem_colunas = [
                    'valorrepasse',  # Referência vem primeiro
                    'periodo', 
                    'valor_exibicao', 
                    'status', 
                    'delay', 
                    'datapagamento'
                ]
                
                # Filtra apenas as colunas que existem no DataFrame
                df_exibir = df_lote[[c for c in ordem_colunas if c in df_lote.columns or c == 'valor_exibicao']]
                
                st.dataframe(
                    df_exibir,
                    column_config={
                        "valorrepasse": "Referência",
                        "periodo": "Competência",
                        "valor_exibicao": "Valor",
                        "status": "Situação",
                        "delay": "Atraso",
                        "datapagamento": "Data de Pagto"
                    },
                    use_container_width=True,
                    hide_index=True
                )
    except Exception as e:
        st.error(f"Erro ao processar: {e}")