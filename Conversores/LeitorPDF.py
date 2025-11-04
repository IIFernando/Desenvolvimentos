import PyPDF2
import tabula
import pandas as pd

file_path = 'C:\\Users\\ferna_5dwides\\Downloads\\Nova pasta\\Sefaz.pdf'
output_txt_path = 'C:\\Users\\ferna_5dwides\\Downloads\\Nova pasta\\Sefaz_output.txt'

# Abrir o arquivo PDF e contar o número de páginas
with open(file_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)

print(f"O PDF tem {num_pages} páginas.")

# Abrir o arquivo de saída para escrita
with open(output_txt_path, 'w', encoding='utf-16') as output_file:
    # Extrair tabelas de cada página e escrever no arquivo de texto
    for page in range(1, num_pages + 1):
        tables = tabula.read_pdf(file_path, pages=page, multiple_tables=True)
        page_content = ""
        for i, table in enumerate(tables):
            df = pd.DataFrame(table)
            page_content += df.to_string(index=False) + "\n\n"
        
        # Escrever o conteúdo da página no arquivo, cada página em uma linha
        output_file.write(f"Página {page}:\n{page_content}\n")

print(f"As informações foram extraídas e salvas em {output_txt_path}")