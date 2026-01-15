import streamlit as st
import pandas as pd
import os

@st.cache_data(ttl=3600)
def carregar_dados_csv():
    """Lê o arquivo físico tratando erros de localização, linhas mal formadas e datas."""
    
    # --- AJUSTE DE CAMINHO PARA STREAMLIT CLOUD ---
    # Busca o diretório onde este arquivo loader.py está
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # Monta o caminho subindo uma pasta e entrando em 'data'
    caminho = os.path.join(diretorio_atual, "..", "data", "Convenios.csv")
    
    # Verifica se o arquivo realmente existe antes de tentar ler
    if not os.path.exists(caminho):
        st.error(f"⚠️ Arquivo não encontrado: {caminho}")
        return pd.DataFrame()

    try:
        # 1. on_bad_lines='skip' evita que o código trave nas linhas com vírgulas extras
        df = pd.read_csv(
            caminho, 
            low_memory=False, 
            on_bad_lines='skip', 
            encoding='utf-8'
        )
        
        # Limpeza de nomes de colunas
        df.columns = [str(col).strip() for col in df.columns]
        
        # TRATAMENTO DE DATAS (CRÍTICO PARA OS REGISTROS DE 2025)
        if 'DataAdmissao' in df.columns:
            df['DataAdmissao'] = pd.to_datetime(df['DataAdmissao'], errors='coerce')

        # Pré-limpeza de ConvenioNome
        if 'ConvenioNome' in df.columns:
            df['ConvenioNome'] = df['ConvenioNome'].fillna('NÃO INFORMADO').astype(str).str.strip()
            
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao processar o CSV: {e}")
        return pd.DataFrame()

def obter_dados_sessao():
    if "data" not in st.session_state:
        st.session_state["data"] = carregar_dados_csv()
    return st.session_state["data"]

def carregar_resumo_geral():
    return obter_dados_sessao()

def carregar_resumo_ativo():
    df = obter_dados_sessao()
    if df.empty:
        return df
    
    situacoes_ativas = ["ATIVO", "Ativo", "FÉRIAS", "LICENÇA MATERNIDADE"]
    if 'Situacao' in df.columns:
        return df[df['Situacao'].isin(situacoes_ativas)].copy()
    return df.copy()

def obter_total_ativos():
    df_ativos = carregar_resumo_ativo()
    if df_ativos.empty:
        return 0
    return int(df_ativos.shape[0]) # Retorna apenas a contagem de linhas