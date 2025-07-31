import pandas as pd
from datetime import datetime
import numpy as np

df = pd.read_excel(
    'G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo v1.1.xlsx', 
    dtype=str, sheet_name='Livro SAP')

# Variaveis de instância para o script atenda todas as filiais.
imMunicipal = str(input('Inscrição Municipal: '))
mesCompetencia = input('Mês de Competência: ')
anoCompetencia = input('Ano de Competência: ')
empresa = 'L4B LOGISTICA LTDA'
dataHora = datetime.now()
data_hora_formatada = dataHora.strftime("%H:%M %d/%m/%Y")

df = df.astype({
    'CNPJ': str,
    'Nota': str,
    'ISS': float,
    'Valor': float,
    '%ISS': float,
    'vLiquido': float
})

# Seleção Filial e filtros.
df = df.loc[df['Centro'] == '0046']
df = df.loc[df['Cidade'] != 'BRASILIA']

# Converter a coluna para datetime (se não estiver no formato datetime) e formatar
df['Data documento'] = pd.to_datetime(df['Data documento']).dt.strftime("%d/%m/%Y")
df['Data documento'] = df['Data documento'].str.replace('/', '')

# Parametrizando colunas de valor com 2 casas decimais após o .
df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
df['vLiquido'] = df['vLiquido'].apply(lambda x: format(round(x, 2), '.2f'))
df['%ISS'] = df['%ISS'].apply(lambda x: format(round(x, 1), '.1f'))

def definir_iss_retido(row):
    if row['ISS'] > 0:
        return '1'
    elif row['ISS'] == 0:
        return '0'

# Header do arquivo
cabecalho = [f'{imMunicipal};{mesCompetencia};{anoCompetencia};{data_hora_formatada}{empresa};1;EXPORTACAO DECLARACAO ELETRONICA-ONLINE-NOTA CONTROL;']
Header = pd.DataFrame(columns=cabecalho)

df.insert(1, 'T_Documento', '4') # Conforme manual o modelo do documento para NFTS é 5
df.insert(2, 'IM_Prestador', '') # Teste de IM do prestador
df.insert(3, 'CódigoArea', '')
df.insert(4, 'uEconomica', '0')
df['ISS Retido'] = df.apply(definir_iss_retido, axis=1)  # Aplicar a função a cada linha
df['LC 116'] = df['LC 116'].str.replace('.', '')
df['CEP'] = df['CEP'].str.replace('.', '')
df['CEP'] = df['CEP'].str.replace('-', '')

registros = pd.DataFrame()
registros = pd.concat([df['T_Documento'] + ";" +  df['Nota'] + ";" + df['Valor'] + ";" + df['vLiquido'] +
                       ";" + df['%ISS'] + ";" + df['Data documento'] + ";" + df['Data documento'] + ";" +
                       df['CNPJ'] + ";" + df['Razão Social'] + ";" + df['IM_Prestador'] + ";" + df['ISS Retido'] + ";" + 
                       df['CEP'] + ";" + df['Logradouro'] + ";" + df['Número'] + ";" + df['Bairro'] + ";" + df['Cidade'] + ";" + 
                       df['UF'] + ";" + df['DDD'] + ";" + df['ISS Retido'] + ";" + df['LC 116'] + ";" + '1' + ";"
                       ],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

# Escrever linha por linha no arquivo de texto
with open('C:\\Users\\logger\\Downloads\\NFTS\\NFTS_DF.txt', 'w', encoding='utf-8') as file:
    
    #Iterar sobre todos os DataFrames (df1, df2) dinamicamente
    for df_name in ['Header', 'registros']:
        df = globals()[df_name]  #Obtém o DataFrame pelo nome da variável
        df.to_csv(file, index=False, sep='\t')  #Escreve o DataFrame no arquivo
