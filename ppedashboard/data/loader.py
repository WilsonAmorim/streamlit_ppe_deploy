import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def carregar_dados_csv():
    """Lê o arquivo físico tratando erros de linhas mal formadas e datas."""
    caminho = "data/Convenios.csv"
    
    # 1. on_bad_lines='skip' evita que o código trave, mas pula registros.
    # Se possível, limpe o CSV original. Aqui garantimos a leitura do máximo possível.
    df = pd.read_csv(
        caminho, 
        low_memory=False, 
        on_bad_lines='skip', 
        encoding='utf-8'
    )
    
    # Limpeza de nomes de colunas
    df.columns = [str(col).strip() for col in df.columns]
    
    # TRATAMENTO DE DATAS (CRÍTICO PARA OS 346 REGISTROS)
    # Removemos o 'dayfirst' fixo para o Pandas detectar o formato ISO do seu CSV
    if 'DataAdmissao' in df.columns:
        df['DataAdmissao'] = pd.to_datetime(df['DataAdmissao'], errors='coerce')

    # Pré-limpeza de ConvenioNome
    if 'ConvenioNome' in df.columns:
        df['ConvenioNome'] = df['ConvenioNome'].fillna('NÃO INFORMADO').astype(str).str.strip()
        
    return df

def obter_dados_sessao():
    """Gerencia os dados no Session State para persistência na navegação."""
    if "data" not in st.session_state:
        st.session_state["data"] = carregar_dados_csv()
    return st.session_state["data"]

def carregar_resumo_geral():
    """Retorna o histórico completo (Admissões totais)."""
    return obter_dados_sessao()

def carregar_resumo_ativo():
    """Retorna apenas quem está na ativa hoje."""
    df = obter_dados_sessao()
    situacoes_ativas = ["ATIVO", "Ativo", "FÉRIAS", "LICENÇA MATERNIDADE"]
    
    if 'Situacao' in df.columns:
        return df[df['Situacao'].isin(situacoes_ativas)].copy()
    return df.copy()