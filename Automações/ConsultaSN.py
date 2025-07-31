from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep as slp

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/aplicacoes.aspx?id=21')

cnpj = driver.find_element(By.XPATH, '//*[@id="Cnpj"]')
cnpj.clear()
cnpj.send_keys('24217653000195')

consulta = driver.find_element(By.XPATH, '//*[@id="consultarForm"]/button')
consulta.click()

slp(5)