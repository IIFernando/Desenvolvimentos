import pandas as pd
import requests
import json
from time import sleep as slp

df = pd.read_excel('C:\\Users\\logger\\Downloads\\Consulta.xltx', dtype=str)

df['CNPJ'] = df['CNPJ'].str.replace('.', '').str.replace('/', '').str.replace('-', '')

print('Consultando...')

with open('C:\\Users\\logger\\Downloads\\consulta_cnpj.csv', 'a', newline='',
          encoding='ISO-8859-1') as arquivo:
    
    for c in df['CNPJ']:

        if len(c) > 11:

            browser = requests.get('https://www.receitaws.com.br/v1/cnpj/' + c, verify=False)

            slp(3)
            
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

            arquivo.write(
                c + '|' + str(nome) + '|' + str(porte) + '|' + str(cep) + '|' + str(logradouro) + '|' + 
                str(numero) + '|' + str(bairro) + '|' + str(municipio) + '|' + str(uf) + '|' + str(cnae)
                + '|' + email + '|' + situacao + '|' + data + '|' + motivo_situacao + '|' + str(simples))
            arquivo.write(str('\n'))

            slp(20)
            
        else:
            arquivo.write(c + '|' + 'O número não é um CNPJ válido')
            arquivo.write(str('\n'))
            
print('Finalizado.')