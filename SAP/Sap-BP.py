import requests
from time import sleep as slp
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd

# Ler planilha
df = pd.read_excel(r"C:\Users\ferna\Downloads\base_cadastros.xlsx", dtype=str)

# Carregar variáveis de ambiente
load_dotenv()

# URL da API
url = "https://loggi-dev-qa.it-cpi003-rt.cfapps.us10.hana.ondemand.com/http/s4/api/BPCustomer"

# Credenciais
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

# Iterar linha a linha da planilha
for index, row in df.iterrows():

    payload = {
        "partner": str(row["partner"]),
        "name_first": row["name_first"],
        "name_last": row["name_last"],
        "email_responsible": row["email_responsible"],
        "payment_method": "UMT",
        "payment_terms": "0001",
        "search_term_1": row["search_term_1"],
        "search_term_2": row["search_term_2"],
        "natural_person": "X",
        "company_code": [
            "L4B",
            "LTEC"
        ],
        "bp_group": "",
        "street": row["street"],
        "house_num_1": row["house_num_1"],
        "complement": row.get("complement", ""),
        "district": row["district"],
        "city_1": row["city_1"],
        "country": "BR",
        "state": row["state"],
        "postal_code_1": row["postal_code_1"],
        "telephone_default": str(row["telephone_default"]),
        "bp_type": "driver",
        "bank_data": {
            "country_bank": "BR",
            "bank_code": row["bank_code"],
            "bank_agency": row["bank_agency"],
            "bank_account": row["bank_account"],
            "bank_holder": row["bank_holder"],
            "bank_bp_number": str(row["bank_bp_number"])
        }
    }

    # Enviar requisição POST
    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(username, password),
        timeout=30
    )

    print(f"Linha {index + 1}")
    print("Status Code:", response.status_code)
    print("Resposta da API:", response.text)
    print("-" * 50)

    slp(5)
