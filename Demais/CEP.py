import requests
import json

cep = str(input('Informe o CEP: '))

browser = requests.get(f'https://viacep.com.br/ws/{cep}/json/', verify=False)

resp = json.loads(browser.text)

zip = resp['cep']
adress = resp['logradouro']
bairro = resp['bairro']
estado = resp['estado']
uf = resp['uf']
ibge = resp['ibge']

print(f'{zip}; {adress}; {bairro}; {estado}; {uf}; {uf} {ibge}')