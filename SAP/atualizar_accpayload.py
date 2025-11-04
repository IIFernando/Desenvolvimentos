import requests
from time import sleep as slp
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd

df = pd.read_csv("/home/fernandoaraujo_logg/Desenvolvimentos/SAP/accpayload.csv", delimiter=',', dtype=str)

def is_nan_robusto(value):
    # Verifica se é NaN ou valor equivalente
    if pd.isna(value):
        return True
    if isinstance(value, str) and value.strip().lower() == 'nan':
        return True
    return False

def limpar_payload(payload):
    for chave, valor in payload.items():
        if is_nan_robusto(valor):
            payload[chave] = None
    return payload

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# URL da API
# url = "https://loggi-dev-qa.it-cpi003-rt.cfapps.us10.hana.ondemand.com/http/v1/update/repasse"
url = "https://loggi-prod.it-cpi008-rt.cfapps.br10.hana.ondemand.com/http/v1/update/repasse"

# Lendo as variáveis de ambiente
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

# Iterar pelas linhas do DataFrame
for index, row in df.iterrows():

    # Pegando os outros parâmetros
    param1 = row["LOGGI_ID"]
    param2 = row["CNPJ"]
    param3 = row["DATADOC"]
    param4 = row["DOCAMOUNT"]

    # Dados a serem enviados no corpo da requisição (JSON)
    payload = {
            "LOGGI_ID": param1, #Campo para a pesquisa do Payable
            "CNPJ": param2, #CNPJ do driver, CAMPO OPICIONAL.
            "DATADOC": param3, #Data de emissão (EX:YYYY-MM-DD), CAMPO OPICIONAL.
            "DOCAMOUNT": param4 #Campo de valor do documento, CAMPO OPICIONAL.
        }

    # Limpando o payload para remover valores NaN
    payload = limpar_payload(payload)
    
    # Enviando a requisição POST
    response = requests.put(
            url,
            json=payload,
            auth=HTTPBasicAuth(username, password)
        )

    # Exibindo o resultado
    print('Enviando payload:', payload)
    print("Status Code:", response.status_code)
    print("Resposta da API:", response.text)
    slp(5)
