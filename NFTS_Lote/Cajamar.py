import pandas as pd

df = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo.xlsx', dtype=str, sheet_name='Livro SAP')

#Alterar tipo de dado da coluna.
df = df.astype({
    'CNPJ': str,
    'ISS': float,
    'Valor_Serv': float
})

df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand= True)

filial = input('Informe a filial: ')
data = input('Informar data de importação (aaaammdd): ')

if filial == '0001':
    cnpj = '24217653000608'
    
elif filial == '0099':
    cnpj = '24217653010077'

#Seleção Filial e filtros.
df = df.loc[df['Centro'] == filial]
df = df.loc[df['Cidade'] != 'CAJAMAR']
df = df[df['CFOP'].isin(['1933/AA' , '2933/AA'])]

#Criação das colunas personalizadas, parâmetros conforme manual.
df.insert(13, 'T_NFTS', 'NFSE ')
df.insert(13, 'Serie', 'E ')
df.insert(13, 'Municipio_T', 'Cajamar')
df.insert(13, 'CNPJ_Filial', cnpj)
df.insert(13, 'D_Lançamento', data)
df.loc[df['ISS'] > 0, 'ISS Retido'] = 'T'
df.loc[df['ISS'] == 0, 'ISS Retido'] = 'R'

#Criação das colunas conforme regra do valor.
df['Valor_Serv'] = df['Valor_Serv'].apply(lambda x: format(round(x, 2), '.2f'))

df.drop(['HORA'], axis= 1, inplace= True)
df.drop_duplicates(['Documento MIRO'], inplace=True)

df['Data documento'] = df['Data documento'].str.replace('-', '')
df['LC 116/2003'] = df['LC 116/2003'].str.replace('.', '')
df['Valor_Serv'] = df['Valor_Serv'].str.replace('.', '')

#Parametrização das colunas utilizando 'PAD'
df['Nota'] = df['Nota'].str.pad(width=6, side='left', fillchar='0')
df['Valor_Serv'] = df['Valor_Serv'].str.pad(width=14, side='left', fillchar='0')
df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
df['Municipio_T'] = df['Municipio_T'].str.pad(width=50, side='right', fillchar=' ')

dfNFTS = pd.Series(df['CNPJ_Filial'] + df['T_NFTS'] + df['Serie'] + df['Nota'] + df['LC 116/2003'] + df['ISS Retido'] +
                    df['Data documento'] + df['Valor_Serv'] + df['Valor_Serv'] + df['CNPJ'] + df['Municipio_T'] + df['D_Lançamento'])

dfNFTS.to_csv('NFTS_Cajamar.txt', index=False, header=False)
