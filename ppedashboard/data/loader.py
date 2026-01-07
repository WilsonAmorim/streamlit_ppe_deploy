import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)  # Guarda os dados por 1 hora (3600 segundos)
def carregar_dados_csv():
    """Lê o arquivo físico e limpa os tipos de dados básicos."""
    caminho = "data/Convenios.csv"
    
    # Carregamento otimizado
    df = pd.read_csv(caminho, low_memory=False)
    
    # Limpeza global de nomes de colunas
    df.columns = [str(col).strip() for col in df.columns]
    
    # Pré-limpeza de ConvenioNome para evitar erros de tipo (float vs str)
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