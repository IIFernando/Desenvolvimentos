import requests
import json
import pandas as pd
from time import sleep as slp

# Se você tiver uma chave de API para autorização, defina aqui:
Loggi_api_key = '88e11e45-4dde-4098-b8e6-aced3f872fb5-e3280b0b-c0b2-4ffd-b08d-73e87a5c0038'
# Teste_api_key = '81ea0df2-094a-440b-9049-8d4defb054c3-2b2589e2-2539-4b76-a83d-2cfd56489b92'

# Carregar o DataFrame a partir do arquivo Excel
df = pd.read_excel(r'C:\Users\logger\Downloads\2023 e 2024_3.xlsx', dtype=str)

print('Consultando.')

# Abrir o arquivo CSV para escrever os logs
with open(r'C:\Users\logger\Downloads\LogSaidaConsultaSN.csv', 'a', newline='', encoding='ISO-8859-1') as arquivo:
    for c in df['CNPJ']:
        print(c)

        url = 'https://api.cnpja.com/office/'+ c +'?simples=true&simplesHistory=true'
        headers = { 'Authorization': Loggi_api_key }

        try:
            # Fazer a requisição GET com um timeout de 10 segundos
            response = requests.request("GET", url, headers=headers, timeout=120)
            response.raise_for_status()  # Lança uma exceção para códigos de status HTTP diferentes de 2xx

            resp = json.loads(response.text)

            # Extrair os dados desejados do JSON de resposta
            update = resp['updated']
            name = resp['company']['name']
            founded = resp['founded']

            acronym = resp['company']['size']['acronym']
            text = resp['company']['size']['text']

            # simei = resp['company']['simei']['optant']
            # dtsimei = resp['company']['simei']['since']
            # smeihis = resp['company']['simei']['history']

            simples = resp['company']['simples']['optant']
            dtsm = resp['company']['simples']['since']
            smhis = resp['company']['simples']['history']

            # Escrever no arquivo CSV os dados obtidos
            arquivo.write(f"{c}_{update}_{name}_{founded}_{acronym}_{text}_{simples}_{dtsm}_{smhis}\n")

        except requests.exceptions.RequestException as e:
            # Em caso de erro na requisição HTTP (timeout, conexão recusada, etc.)
            print(f"Erro na requisição para CNPJ {c}: {e}")
            arquivo.write(f"{c}_Erro na consulta\n")

        except json.JSONDecodeError as e:
            # Em caso de erro ao decodificar a resposta JSON
            print(f"Erro ao decodificar JSON para CNPJ {c}: {e}")
            arquivo.write(f"{c}_Erro na decodificação JSON\n")

        slp(1)  # Aguardar 1 segundo antes da próxima consulta (rate limiting)

print('Consultas finalizadas.')
