import requests
from time import sleep as slp
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd

df = pd.read_excel("/home/fernandoaraujo_logg/Desenvolvimentos/SAP/AlteraCentroCusto.xlsx")

filiais = ["L", "T", "X"]

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# URL da API
# url = "https://loggi-dev-qa.it-cpi003-rt.cfapps.us10.hana.ondemand.com/http/update/CentroCusto"
url = "https://loggi-prod.it-cpi008-rt.cfapps.br10.hana.ondemand.com/http/update/CentroCusto"

# Lendo as variáveis de ambiente
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

# Iterar pelas linhas do DataFrame
for index, row in df.iterrows():

    numero = str(row[0])  # Ajuste conforme a coluna que contém o valor desejado

    # Pegando os outros parâmetros (supondo que estão nas colunas 1, 2 e 3)
    param2 = row[1]  # Coluna 1: Param2
    param3 = row[2]  # Coluna 2: Param3
    param4 = row[3]  # Coluna 3: Param4

    # Gerar os valores combinados (exemplo: L50150, T50150, X50150)
    for filial in filiais:
        combinado = filial + numero  # Junta a letra da filial com o número
        print(f"Enviando para a API: {combinado}")

        # Dados a serem enviados no corpo da requisição (JSON)
        payload = {
            "IV_CENTRO_CUSTO": combinado,
            "IV_APROVADOR_NV1": param2,
            "IV_APROVADOR_NV2": param3,
            "IV_APROVADOR_NV3": param4,
            "IV_APROVADOR_NV4": "" #Paramêtro não obrigatório.
        }

        # Enviando a requisição POST
        response = requests.get(
            url,
            json=payload,
            auth=HTTPBasicAuth(username, password)
        )

        # Exibindo o resultado
        print("Status Code:", response.status_code)
        print("Resposta da API:", response.text)
        slp(5)
