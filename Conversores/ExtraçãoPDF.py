import tabula
import pandas as pd

# Função para abrir o arquivo PDF e extrair a primeira tabela
def extract_and_display_table(pdf_file):
    tables = tabula.read_pdf(pdf_file, pages=1, multiple_tables=True)
    if tables:
        df = tables[0]
        pd.set_option('display.max_columns', None)  # Mostrar todas as colunas
        pd.set_option('display.expand_frame_repr', False)  # Impedir que as colunas sejam truncadas
        print(df)
    else:
        print("Nenhuma tabela encontrada na primeira página.")

# Função principal
def main():
    pdf_file = input("Digite o caminho do arquivo PDF: ")
    extract_and_display_table(pdf_file)

if __name__ == "__main__":
    main()
