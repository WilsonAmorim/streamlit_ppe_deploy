import requests

BASE_URL = "http://localhost:5271/api"  # ajuste conforme seu backend

def get_convenios(token=None):
    url = f"{BASE_URL}/convenios"

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    # 🔥 Agora aceita tanto lista quanto objeto com chave
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("conveiosCadastrados") or data.get("convenios") or []

    return []
