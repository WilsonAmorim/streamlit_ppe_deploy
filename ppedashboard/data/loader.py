import streamlit as st
import requests
import pandas as pd





@st.cache_data(ttl=300)
def carregar_dados():
    API_URL = "http://localhost:5271/api/Dashboard/dashboard-convenios"
    try:
        response = requests.get(API_URL, timeout=10)

        if response.status_code != 200:
            st.error(f"❌ Erro ao acessar API: {response.status_code}")
            st.stop()

        json_data = response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Falha ao conectar com API:\n{e}")
        st.stop()
    except ValueError:
        st.error("❌ Erro ao decodificar JSON retornado pela API!")
        st.stop()

    # -----------------------------
    # DETECTAR A ESTRUTURA DO JSON
    # -----------------------------
    if isinstance(json_data, list):
        data = json_data

    elif isinstance(json_data, dict):

        # busca por chaves conhecidas
        if "conveiosCadastrados" in json_data:
            data = json_data["conveiosCadastrados"]
        elif "convenios" in json_data:
            data = json_data["convenios"]

        # fallback: primeiro valor que seja lista
        else:
            data = next((v for v in json_data.values() if isinstance(v, list)), [])

    else:
        st.error("❌ Estrutura de JSON inesperada.")
        st.stop()

    # -----------------------------
    # MONTAR DATAFRAME
    # -----------------------------
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()

    if df.empty:
        st.warning("⚠ Nenhum dado retornado pela API.")
        return df

    # Limpa espaços e coloca tudo em minúsculo para evitar o KeyError
    df.columns = df.columns.str.strip().str.lower()

    # Verificar coluna dataadmissao
    if "ano" not in df.columns:
        if "dataadmissao" in df.columns:
            df["dataadmissao"] = pd.to_datetime(df["dataadmissao"], errors="coerce")
            df["ano"] = df["dataadmissao"].dt.year
        else:
            df["ano"] = 0

    return df


@st.cache_data(ttl=300)
def carregar_resumo_ativos():
    API_URL_ATIVOS = "http://localhost:5271/api/Dashboard/dashboard-convenios-ativos"
    try:
        response = requests.get(API_URL_ATIVOS, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame() # Retorna vazio em caso de erro

        data = response.json()
        df = pd.DataFrame(data)

        # Padroniza colunas para minúsculo para evitar erro de digitação
        df.columns = df.columns.str.lower()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar resumo de ativos: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def carregar_resumo_generos():
    # Verifique se esta URL abre no seu navegador
    API_URL_GENEROS = "http://localhost:5271/api/Dashboard/dashboard-convenios-genero"
    
    try:
        response = requests.get(API_URL_GENEROS, timeout=10)
        
        # Se a API retornar erro (Ex: 404 ou 500)
        if response.status_code != 200:
            return pd.DataFrame()

        data = response.json()
        
        # Se os dados vierem dentro de uma chave, extraímos ela
        if isinstance(data, dict):
            # Tenta pegar a primeira lista que encontrar no dicionário
            data = next((v for v in data.values() if isinstance(v, list)), [])

        df = pd.DataFrame(data)

        if not df.empty:
            # Padroniza nomes das colunas para minúsculo
            df.columns = df.columns.str.lower()
            
            # Se a API mandar 'convenionome', renomeamos para 'lote'
            if "convenionome" in df.columns:
                df = df.rename(columns={"convenionome": "lote"})
        
        return df

    except Exception as e:
        # Se der erro de conexão, ele avisa aqui
        print(f"Erro de conexão: {e}") 
        return pd.DataFrame()
    
@st.cache_data(ttl=300)
def carregar_repasses():
    API_URL_REPASSES = "http://localhost:5271/api/Dashboard/repasses"
    try:
        response = requests.get(API_URL_REPASSES, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extrai a lista de dentro da chave que sua API envia
            df = pd.DataFrame(data["repassesCadastrados"])
            
            # Padroniza colunas para minúsculo
            df.columns = df.columns.str.lower()
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao conectar com API de Repasses: {e}")
        return pd.DataFrame()
    

@st.cache_data(ttl=300)
def carregar_lotacao():
    API_URL = "http://localhost:5271/api/Dashboard/dashboard-convenios-lotacao"
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            # Padroniza nomes para minúsculo para evitar erros
            df.columns = df.columns.str.lower()
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar lotação: {e}")
        return pd.DataFrame()