import pandas as pd
import numpy as np

df = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo v1.1.xlsx', dtype=str, sheet_name='Livro SAP')
cod_sp = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\DMS\\Importação em lote planilha\\Arquivos\\CODSP.xlsx', dtype=str)

#Alterar tipo de dado da coluna.
df = df.astype({
    'CNPJ': str,
    'Nota': str,
    'ISS': float,
    'Valor': float
})

# dtint = input('Data inicio: ')
# dtfim = input('Data fim: ')
# inMunicipal = input('Informar IM: ')
# filial = input('Informe código da filial: ')

dtint = '20240101'
dtfim = '20240731'
inMunicipal = '000000007261993'
filial = '0129'
cnpj = '24217653012959'

df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand=True)

#Seleção Filial e filtros.
df = df.loc[df['Centro'] == filial]
df = df.loc[df['Cidade'] != 'RECIFE']
df = df[df['CFOP'].isin(['1933/AA', '2933/AA'])]
df['%ISS'] = df['%ISS'].str.rstrip('%').astype(float)

#Criação das colunas personalizadas, parâmetros conforme manual.
df.insert(1, 'T_Registro', '40')
df.insert(2, 'T_Documento', '01')
df.insert(3, 'T_Serie', '    E')
df.insert(4, 'S_Documento', '1')
df.insert(5, 'I_CNPJ', '2')
df.insert(6, 'IM', '000000000000000')
df.insert(7, 'IE', '000000000000000')
df.insert(8, 'T_end', 'Rua')
df.insert(9, 'Complemento', '')
df.insert(10, 'Telefone', '           ')
df.insert(11, 'Deduções', '000000000000000')
df.insert(12, 'C_RESERVADO1', '')
df.insert(13, 'C_RESERVADO2', '')
df.insert(14, 'C_RESERVADO3', '')
df.insert(15, 'N_OBRA', '')
df.insert(16, 'Anotação', '')
df.insert(17, 'Descrição do Serviço', 'Prestação de serviço')

#Criação das colunas conforme regra do valor.
def definir_iss_retido(row):
    """
        Define o valor do 'ISS Retido' para uma linha. Args:
        row (pandas.Series): Uma linha do DataFrame. Returns:
        str: O valor do 'ISS Retido' para a linha.
    """
    if row['ISS'] > 0:
        return '1'
    elif row['ISS'] == 0:
        return '0'
    # Retorne outros valores de acordo com suas necessidades
    else:
        return np.NAN  # Valor padrão para linhas sem 'ISS' > 0 ou 'ISS' == 0
    
def op_simples(row):
    """
        Define o valor do 'ISS Retido' para uma linha. Args:
        row (pandas.Series): Uma linha do DataFrame. Returns:
        str: O valor do 'ISS Retido' para a linha.
    """
    if row['PORTE'] == 'DEMAIS':
        return '0'
    else:
        return '1'  # Valor padrão para linhas sem 'ISS' > 0 ou 'ISS' == 0
    
def t_tributacao(row):
    """
        Define o valor do 'ISS Retido' para uma linha. Args:
        row (pandas.Series): Uma linha do DataFrame. Returns:
        str: O valor do 'ISS Retido' para a linha.
    """
    if row['ISS'] > 0:
        return '01'
    else:
        return '02'  # Valor padrão para linhas sem 'ISS' > 0 ou 'ISS' == 0

df['tributação'] = df.apply(t_tributacao, axis=1)  # Aplicar a função a cada linha
df['E_porte'] = df.apply(op_simples, axis=1)  # Aplicar a função a cada linha
df['ISS Retido'] = df.apply(definir_iss_retido, axis=1)  # Aplicar a função a cada linha
df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
df['ISS'] = df['ISS'].apply(lambda x: format(round(x, 2), '.2f'))
df['%ISS'] = (df['%ISS'] * 100).round().astype(int)

#União das planilha base trazendo os subitens COD.
df = pd.merge(df, cod_sp, on='LC 116', how='inner')

df.drop(['HORA', 'DESCRIÇÃO'], axis=1, inplace=True)
df.drop_duplicates(['Documento MIRO'], inplace=True)

df['Data documento'] = df['Data documento'].str.replace('-', '')
df['LC 116'] = df['LC 116'].str.replace('.', '')
df['CEP'] = df['CEP'].str.replace('.', '')
df['CEP'] = df['CEP'].str.replace('-', '')
df['Valor'] = df['Valor'].astype(str).str.replace('.', '')
df['ISS'] = df['ISS'].astype(str).str.replace('.', '')

#Parametrização das colunas utilizando 'PAD'
df['Nota'] = df['Nota'].str.pad(width=15, side='left', fillchar='0')
df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
df['Valor'] = df['Valor'].str.pad(width=15, side='left', fillchar='0')
df['ISS'] = df['ISS'].str.pad(width=15, side='left', fillchar='0')
df['CÓDIGO'] = df['CÓDIGO'].str.pad(width=5, side='left', fillchar='0')
df['CNAE'] = df['CNAE'].str.pad(width=20, side='left', fillchar='0')
df['LC 116'] = df['LC 116'].str.pad(width=4, side='left', fillchar='0')
df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(5))
df['Razão Social'] = df['Razão Social'].str.pad(width=115, side='left', fillchar=' ')
df['Logradouro'] = df['Logradouro'].str.pad(width=125, side='right', fillchar=' ')
df['Número'] = df['Número'].str.pad(width=10, side='right', fillchar=' ')
df['Complemento'] = df['Complemento'].str.pad(width=60, side='right', fillchar=' ')
df['Bairro'] = df['Bairro'].str.pad(width=72, side='right', fillchar=' ')
df['Cidade'] = df['Cidade'].str.pad(width=50, side='right', fillchar=' ')
df['E-mail'] = df['E-mail'].astype(str).apply(lambda x: x.ljust(80))
df['Anotação'] = df['Anotação'].str.pad(width=15, side='right', fillchar='0')
df['N_OBRA'] = df['N_OBRA'].str.pad(width=15, side='right', fillchar='0')
df['C_RESERVADO1'] = df['C_RESERVADO1'].str.pad(width=54, side='right', fillchar=' ')
df['C_RESERVADO2'] = df['C_RESERVADO2'].str.pad(width=30, side='right', fillchar=' ')
df['C_RESERVADO3'] = df['C_RESERVADO3'].str.pad(width=30, side='right', fillchar=' ')
df['Descrição do Serviço'] = df['Descrição do Serviço'].str.pad(width=100, side='right', fillchar=' ')
df['UF'] = df['UF'].str.pad(width=2, side='right', fillchar=' ')
df['CEP'] = df['CEP'].str.pad(width=8, side='right', fillchar='0')

cabecalho = [f'100032{cnpj}{inMunicipal}{dtint}{dtfim}']
Header = pd.DataFrame(columns=cabecalho)

registros = pd.DataFrame()
registros = pd.concat([df['T_Registro'], df['T_Documento'], df['T_Serie'], df['Nota'], df['Data documento'],
                       df['S_Documento'], df['I_CNPJ'], df['CNPJ'], df['IM'], df['IE'], df['Razão Social'],
                       df['T_end'], df['Logradouro'], df['Número'], df['Complemento'], df['Bairro'], df['Cidade'],
                       df['UF'], df['CEP'], df['Telefone'], df['E-mail'], df['tributação'], df['C_RESERVADO1'],
                       df['E_porte'], df['LC 116'], df['CNAE'], df['%ISS'], df['Valor'], df['Deduções'],
                       df['C_RESERVADO2'], df['ISS'], df['ISS Retido'], df['Data documento'], df['N_OBRA'],
                       df['Anotação'], df['Descrição do Serviço']
                       
                       
                       
                       ],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

df = df.astype({'Valor': int, })
num_linhas = len(registros)
num_linhas_formatted = f'{num_linhas:0>8}'
Total = df['Valor'].sum()
Total = str(Total)
TotalZ = Total.zfill(15)

radape = ['90' + num_linhas_formatted + TotalZ + '000000000000000']
footer = pd.DataFrame(columns=radape)

#Escrever linha por linha no arquivo de texto
with open('C:\\Users\\logger\\Downloads\\NFTS\\NFTS_PE.txt', 'w', encoding='utf-8') as file:
    #Iterar sobre todos os DataFrames (df1, df2, df3) dinamicamente
    for df_name in ['Header', 'registros', 'footer']:
        df = globals()[df_name]  #Obtém o DataFrame pelo nome da variável
        df.to_csv(file, index=False, sep='\t')  #Escreve o DataFrame no arquivo
