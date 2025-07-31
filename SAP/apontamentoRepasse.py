import requests
import google.generativeai as genai
from time import sleep as slp
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd
from pathlib import Path

# Configura exibição do pandas
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', None)

# Carregar variáveis do arquivo .env
env_path = Path(__file__).resolve().parent.parent / 'auth' / '.env'
load_dotenv(dotenv_path=env_path)

# Configura chave da API do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API KEY do Gemini não encontrada no .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# Datas da consulta
dtinicio = '20250527'
dtfim = '20250527'

# URL da API
url = f"https://loggi-prod.it-cpi008-rt.cfapps.br10.hana.ondemand.com/http/v1/read/drivtransf?DATE_START={dtinicio}&DATE_END={dtfim}"

# Autenticação da API
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

if not username or not password:
    raise ValueError("Usuário ou senha da API não encontrados no .env")

# Chamada da API
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Verifica a resposta da API
if response.status_code == 200:
    dados_json = response.json()
    df = pd.DataFrame(dados_json)

    # Seleciona apenas colunas desejadas (e existentes)
    colunas_desejadas = ['LOGGI_ID', 'DOCTYPE', 'BP_NUMBER', 'AMOUT', 'PERIOD_START', 'PERIOD_END', 'MSG']
    colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
    if not colunas_existentes:
        raise ValueError("Nenhuma das colunas esperadas foi encontrada na resposta da API.")

    df_filtrado = df[colunas_existentes]

    # Instruções para o Gemini
    instrucoes = (
        "Analise a mensagem de erro abaixo e diga qual é a provável causa e como resolver, tambem seja breve na explicação. "
        "Erro comum: 'BP_NUMBER' → O BP não está cadastrado no SAP e precisa ser reenviado. "
        "'Divergencias de valores' → Seja direto e aponte o valor da diferença entre SAP e Loggi Web. E cuidado com valores negativos, o SAP pode gerar essa diferença o que deixa o saldo negativo."
        "Erros relacionandos a 'Fornecedor XXXX LTEC não existe na empresa' → É necessário solicitar ao time de cadastro que amplie a empresa do BP. "
        "Responda sempre de forma objetiva, em no máximo 1 linhas."
    )

    # Geração de sugestões com Gemini
    sugestoes = []

    for msg in df_filtrado['MSG']:
        try:
            if not msg:
                sugestoes.append("Mensagem vazia.")
                continue
            resposta = model.generate_content(f"{instrucoes}{msg}")
            sugestoes.append(resposta.text)
            slp(1)
        except Exception as e:
            sugestoes.append(f"Erro ao processar: {str(e)}")

    # Adiciona a coluna com as sugestões
    df_filtrado['sugestao_gemini'] = sugestoes

    # Exibe o resultado completo
    print(df_filtrado)

else:
    print(f"Erro ao consultar API: {response.status_code}")
    print(response.text)
