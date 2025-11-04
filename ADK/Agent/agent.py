from google.adk.agents import Agent
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

def consulta_cnpj(cnpj: str):
    """Esta função atende as requisições de consuta para CNPJ, 
    ela só é chamado quando o usuário digitar por cnpj"""
    
    browser = requests.get('https://www.receitaws.com.br/v1/cnpj/' + cnpj, verify=False)
    resp = json.loads(browser.text)
    nome = resp['nome']
    porte = resp['porte']
    cep = resp['cep']
    logradouro = resp['logradouro']
    numero = resp['numero']
    bairro = resp['bairro']
    municipio = resp['municipio']
    uf = resp['uf']
    cnae = resp['atividade_principal']
    email = resp['email']
    situacao = resp['situacao']
    data = resp['data_situacao']
    motivo_situacao = resp['motivo_situacao']
    simples = resp['simples']
    
    return (str(nome) + '|' + str(porte) + '|' + str(cep) + '|' + str(logradouro) + '|' + 
                    str(numero) + '|' + str(bairro) + '|' + str(municipio) + '|' + str(uf) + '|' + str(cnae)
                    + '|' + email + '|' + situacao + '|' + data + '|' + motivo_situacao + '|' + str(simples))

def alteraCusto(ccusto: str, aprov1: str, aprov2: str, aprov3: str):
    """Quando o usuário solicitar uma alteração de centro de custo executar essa tarefa ele devera passar no maximo
    4 users sendo o quarto não obrigatório"""
    
    filiais = ["L", "T", "X"]

    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv()

    # URL da API
    url = "https://loggi-prod.it-cpi008-rt.cfapps.br10.hana.ondemand.com/http/update/CentroCusto"

    # Lendo as variáveis de ambiente
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
            # Gerar os valores combinados (exemplo: L50150, T50150, X50150)
    for filial in filiais:
        combinado = filial + ccusto  # Junta a letra da filial com o número
        payload = {
                "IV_CENTRO_CUSTO": combinado,
                "IV_APROVADOR_NV1": aprov1,
                "IV_APROVADOR_NV2": aprov2,
                "IV_APROVADOR_NV3": aprov3,
                "IV_APROVADOR_NV4": "" #Paramêtro não obrigatório.
            }
    
        response = requests.get(
                url,
                json=payload,
                auth=HTTPBasicAuth(username, password)
            )

root_agent = Agent(
    name="agent",
    model="gemini-2.0-flash",
    description="Especialista no ERP SAP e na area tributária",
    instruction="""Você é um especialista no sistima SAP assim como tambem dominá o sistema tributário brasileiro
                fazendo pesquisas assim como consultas que sejam solicitadas.""",
                
    tools=[consulta_cnpj, alteraCusto]
)
