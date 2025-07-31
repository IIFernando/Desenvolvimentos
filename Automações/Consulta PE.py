import pandas as pd
from selenium import webdriver
from time import sleep as slp
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv

df = pd.read_excel('C:\\Users\\logger\\Downloads\\Termos\\TERMOS TRNE.xlsx', dtype=str)

#Firefox
servico = Service(GeckoDriverManager().install())
browser = webdriver.Firefox(service=servico)
browser.maximize_window()

# Abrir a página da web
slp(5)

# Abrir o arquivo CSV para escrita
filename = 'C:\\Users\\logger\\Downloads\\Termos\\Log_PE_TRNE.csv'
with open(filename, 'a', newline='', encoding='UTF-16') as arquivo:
    writer = csv.writer(arquivo)

    for row in df.itertuples():

        browser.get('https://efisco.sefaz.pe.gov.br/sfi_trb_gof/PRManterTermoFielDepositario')
        # t = row.Termo
        c =row.Termo
        # Preencher o campo de busca
        termo_input = browser.find_element(By.XPATH, '//*[@id="nuProtocoloTFD"]')
        termo_input.clear()
        termo_input.send_keys(c)
        
        try:
            # Clicar no botão de busca
            localizar_button = browser.find_element(By.XPATH, '//*[@id="btt_localizar"]')
            localizar_button.click()
            
            # Clica no registro pra garantir que seja selecionado caso apareça repetido.
            detalhar_button = browser.find_element(By.XPATH, '//*[@id="table_conteiner"]/tbody/tr[3]/td/div/div[1]/a[1]')
            detalhar_button.click()
            
            # Clicar no botão de detalhar
            detalhar_button = browser.find_element(By.XPATH, '//*[@id="btt_detalhar"]')
            detalhar_button.click()
            
            # Extrair os dados da tabela e escrever no arquivo CSV
            table_id = "table_tabeladados"  # substitua pelo ID real do elemento da tabela
            table_element = browser.find_element(By.ID, table_id)
            rows = table_element.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                row_data.insert(0, c)
                writer.writerow(row_data)
            browser.back()
            
        except:
            browser.get('https://efisco.sefaz.pe.gov.br/sfi_trb_cmt/PRConsultarTermoFielDepositario')
            # Preencher o campo de busca com o N° do termo
            termo_input = browser.find_element(By.XPATH, '//*[@id="nuTermoFielDepositario"]')
            termo_input.clear()
            termo_input.send_keys(c)
            
            # Clicar no botão de busca
            localizar_button = browser.find_element(By.XPATH, '//*[@id="btt_localizar"]')
            localizar_button.click()
            
            # Clicar no botão de detalhar
            detalhar_button = browser.find_element(By.XPATH, '//*[@id="btt_detalhar"]')
            detalhar_button.click()
            
            # Extrair os dados da tabela e escrever no arquivo CSV
            table_id = "table_tabeladados"  # substitua pelo ID real do elemento da tabela
            table_element = browser.find_element(By.ID, table_id)
            rows = table_element.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                row_data.insert(0, c)
                writer.writerow(row_data)
            browser.back()
# Fechar o navegador
browser.quit()
