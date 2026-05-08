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
            encoding='latin-1'
        )
        
        # Limpeza de nomes de colunas
        df.columns = [str(col).strip() for col in df.columns]
        
        # TRATAMENTO DE DATAS (CRÍTICO PARA OS REGISTROS DE 2026)
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

def carregar_resumo_fesfsus_ativo():
    df = obter_dados_sessao()
    if df.empty:
        return df
    lote = "Fesfsus Lote 01"
    situacoes_ativas = ["ATIVO", "Ativo", "FÉRIAS", "LICENÇA MATERNIDADE"]
    if 'Situacao' in df.columns and 'ConvenioNome' in df.columns:
        return df[df['Situacao'].isin(situacoes_ativas) & (df['ConvenioNome'] == lote)].copy()
    return df.copy()

def carregar_resumo_flem2_ativo():
    df = obter_dados_sessao()
    if df.empty:
        return df

    lote2 = "Flem Lote 02"
    situacoes_ativas = ["ATIVO", "FÉRIAS", "LICENÇA MATERNIDADE"]

    # No seu loader ou na função do Lote 02
    situacoes = ["ATIVO", "FÉRIAS", "LICENÇA MATERNIDADE"]
    mask = (df['ConvenioNome'].str.strip() == 'Flem Lote 02') & \
        (df['Situacao'].str.strip().str.upper().isin(situacoes))
    return df[mask].copy()
    
    # return pd.DataFrame()

def carregar_resumo_flem3_ativo():
    df = obter_dados_sessao()
    if df.empty:
        return df
    lote3 = "Flem Lote 03"
    situacoes_ativas = ["ATIVO", "FÉRIAS", "LICENÇA MATERNIDADE"]
    if 'Situacao' in df.columns and 'ConvenioNome' in df.columns:
        return df[df['Situacao'].isin(situacoes_ativas) & (df['ConvenioNome'] == lote3)].copy()
    return df.copy()

def carregar_fesfsus_ativo():
    df_ativos = carregar_resumo_fesfsus_ativo()
    if df_ativos.empty:
        return 0
    return int(df_ativos.shape[0])

def carregar_flem2_ativo():
    df_ativos = carregar_resumo_flem2_ativo()
    if df_ativos.empty:
        return 0
    return int(df_ativos.shape[0])

def carregar_flem3_ativo():
    df_ativos = carregar_resumo_flem3_ativo()
    if df_ativos.empty:
        return 0
    return int(df_ativos.shape[0])

def carregar_resumo_finalizados():
    df = obter_dados_sessao()
    if df.empty:
        return df
    categorias_fim = ["DESLIGADO", "Demitido"]
    if 'Categoria' in df.columns:
        return df[df['Categoria'].isin(categorias_fim)].copy()
    return df.copy()

def carregar_resumo_afastados():
    df = obter_dados_sessao()
    if df.empty:
        return df
    situacoes_ativas = ["Afastado", "AFASTADO INSS"]
    if 'Situacao' in df.columns:
        return df[df['Situacao'].isin(situacoes_ativas)].copy()
    return df.copy()

def carregar_finalizados():
    df_ativos = carregar_resumo_finalizados()
    if df_ativos.empty:
        return 0
    return int(df_ativos.shape[0])

def carregar_afastados():
    df_ativos = carregar_resumo_afastados()
    if df_ativos.empty:
        return 0
    return int(df_ativos.shape[0])


def gerar_relatorio_lotes_2026():
    df = obter_dados_sessao()
    if df.empty:
        return pd.DataFrame()

    # 1. Filtrar apenas registros de 2026 baseado na Data de Admissão
    df_2026 = df[df['DataAdmissao'].dt.year == 2026].copy()
    df_afastado = df[df['DataAdmissao'].dt.year == 2026].copy()
    
    # 2. Definir os grupos de situação
    situacoes_ativas = ["ATIVO", "Ativo", "FÉRIAS", "LICENÇA MATERNIDADE"]
    situacoes_afastadas = ["AFASTADO", "Afastado", "AFASTADO INSS"] # Ajuste conforme seu CSV
    situacoes_desligadas = ["DESLIGADO", "Demitido"] # Ajuste conforme seu CSV

    # 3. Criar colunas de categoria para facilitar a contagem
    def categorizar(status):
        if status in situacoes_ativas: return "Ativos"
        if status in situacoes_afastadas: return "Afastados"
        return "Desligados"

    df_2026['Categoria'] = df['Situacao'].apply(categorizar)

    # 4. Agrupar por Lote (ConvenioNome) e Categoria
    relatorio = df_2026.groupby(['ConvenioNome', 'Categoria']).size().unstack(fill_value=0)
    
    # Garantir que todas as colunas existam mesmo que o valor seja zero
    for col in ["Ativos", "Afastados", "Desligados"]:
        if col not in relatorio.columns:
            relatorio[col] = 0
            
    # 5. Calcular o Total por Lote
    relatorio['Total Geral'] = relatorio.sum(axis=1)
    
    return relatorio

def gerar_relatorio_lotes_2026_v2():
    df = obter_dados_sessao()
    if df.empty:
        return pd.DataFrame()

    # --- 1. DEFINIÇÃO DAS SITUAÇÕES ---
    situacoes_ativas = ["ATIVO", "Ativo", "FÉRIAS", "LICENÇA MATERNIDADE"]
    situacoes_afastadas = ["AFASTADO", "Afastado", "AFASTADO INSS"] # Ajuste conforme seu CSV
    situacoes_desligadas = ["DESLIGADO", "Demitido"] # Ajuste conforme seu CSV

    # --- 2. FILTROS POR CATEGORIA ---
    
    # Ativos apenas de 2026 (pela Data de Admissão)
    mask_ativos_2026 = (df['Situacao'].isin(situacoes_ativas)) & (df['DataAdmissao'].dt.year == 2026)
    df_ativos = df[mask_ativos_2026].groupby('ConvenioNome').size().rename("Ativos (2026)")

    # Desligados apenas de 2026
    mask_desligados_2026 = (df['Situacao'].isin(situacoes_desligadas))
    df_desligados = df[mask_desligados_2026].groupby('ConvenioNome').size().rename("Desligados (2026)")

    # Afastados SEM FILTRO DE ANO (Estoque Total)
    mask_afastados_total = df['Situacao'].isin(situacoes_afastadas)
    df_afastados = df[mask_afastados_total].groupby('ConvenioNome').size().rename("Afastados (Total)")

    # --- 3. CONSOLIDAÇÃO ---
    # Unimos os três contadores pelo nome do Lote (ConvenioNome)
    relatorio = pd.concat([df_ativos, df_afastados, df_desligados], axis=1).fillna(0).astype(int)
    
    # Cálculo do Total Geral da linha
    relatorio['Movimentação Total'] = relatorio.sum(axis=1)
    
    # Ordenar por nome de lote para ficar organizado
    return relatorio.sort_index()