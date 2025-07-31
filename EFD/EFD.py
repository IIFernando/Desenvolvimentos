import io

# Inicializa uma lista para armazenar as linhas filtradas
linhas_filtradas = []

# Lê o arquivo e filtra as linhas ao mesmo tempo
with io.open('EFD L4B 05_2022_14_09_2024v9.txt', 'r', encoding='ISO-8859-1') as file:
    for linha in file:
        if linha.startswith('|F100|'):
            linhas_filtradas.append(linha.strip())  # Adiciona a linha filtrada, removendo espaços em branco

# Exibe as linhas filtradas
for linha in linhas_filtradas:
    print(linha)