import pandas as pd

df = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo v1.1.xlsx', dtype=str, sheet_name='Livro SAP')

competencia = input('Informe a competência (AAAA/MM): ')
im = input('Informe a IM: ')

#Alterar tipo de dado da coluna.
df = df.astype({
    'CNPJ': str,
    'Nota': str,
    'ISS': float,
    'Valor': float,
    'Logradouro': str
})

#Seleção Filial e filtros.
df = df.loc[df['Centro'] == '0054']
df = df.loc[df['Cidade'] != 'CAMACARI']
df = df[df['CFOP'].isin(['1933/AA' , '2933/AA'])]
df['%ISS'] = df['%ISS'].str.rstrip('%').astype(float)

#Criação das colunas personalizadas, parâmetros conforme manual.
df.insert(1, 'T_RegistroD1', '2')
df.insert(2, 'T_RegistroD2', '3')
df.insert(3, 'Especie', '01')
df.insert(4, 'S_Documento', '01')
df.insert(5, 'Serie', 'UNICA')
df.insert(6, 'T_Entidade', '9')
df.insert(7, 'QI_Serviço', '1')
df.insert(8, 'S_Registro', '000001')
df.insert(9, 'BrancoD2', ' ')
df.insert(10, 'Observacoes', ' ')

df['Tributacao'] = df.apply(lambda row: '1' if row['ISS'] > 0 else '2', axis=1)

df['Data documento'] = pd.to_datetime(df['Data documento'])
df['Data documento'] = df['Data documento'].dt.strftime('%Y/%m/%d')
df['Data documento'] = df['Data documento'].str.replace('/', '')
df['LC 116'] = df['LC 116'].str.replace('.', '')

#Criação das colunas conforme regra do valor.
df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
df['ISS'] = df['ISS'].apply(lambda x: format(round(x, 2), '.2f'))
df['%ISS'] = df['%ISS'].apply(lambda x: format(round(x, 2), '.2f'))

#Parametrização das colunas utilizando 'PAD'
df['Nota'] = df['Nota'].str.pad(width=10, side='left', fillchar='0')
df['Serie'] = df['Serie'].str.pad(width=20, side='left', fillchar=' ')
df['QI_Serviço'] = df['QI_Serviço'].str.pad(width=3, side='left', fillchar='0')
df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
df['LC 116'] = df['LC 116'].str.pad(width=6, side='left', fillchar='0')
df['Razão Social'] = df['Razão Social'].str.pad(width=100, side='left', fillchar=' ')
df['Observacoes'] = df['Observacoes'].str.pad(width=500, side='right', fillchar=' ')
df['BrancoD2'] = df['BrancoD2'].str.pad(width=683, side='right', fillchar=' ')

df['Valor'] = df['Valor'].str.replace('.', '')
df['Base ISS'] = df['Base ISS'].str.replace('.', '')
df['%ISS'] = df['%ISS'].str.replace('.', '')
df['ISS'] = df['ISS'].str.replace('.', '')

df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(5))
df['ISS'] = df['ISS'].apply(lambda x: str(x).zfill(15))
df['Valor'] = df['Valor'].apply(lambda x: str(x).zfill(15))
df['Base ISS'] = df['Base ISS'].apply(lambda x: str(x).zfill(15))

num_linhas = len(df)
linhas_formatted = f'{num_linhas:0>6}'

cabecalho = [f'10{competencia}{im}V01.2{linhas_formatted}{' ' * 697}000001']
Header = pd.DataFrame(columns=cabecalho)

rodape = [f'4{' ' * 724}000000']
Trailer = pd.DataFrame(columns=rodape)

Detalhe1 = pd.DataFrame()
Detalhe1 = pd.concat([df['T_RegistroD1'], df['Especie'], df['S_Documento'], df['Serie'], df['T_Entidade'],
                       df['CNPJ'], df['Razão Social'], df['Nota'], df['Nota'], df['Data documento'], df['Data documento'],
                       df['Valor'], df['Valor'], df['ISS'], df['Tributacao'], df['Observacoes'], df['QI_Serviço'],
                       df['S_Registro']],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

Detalhe2 = pd.DataFrame()
Detalhe2 = pd.concat([df['T_RegistroD2'], df['LC 116'], df['Valor'], df['ISS'], df['%ISS'], df['BrancoD2'], df['S_Registro']],
                     axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

interleaved_dfs = []

for i in range(len(Detalhe1)):
    interleaved_dfs.append(Detalhe1.iloc[i])
    interleaved_dfs.append(Detalhe2.iloc[i])

result = pd.DataFrame(interleaved_dfs)

# Escrever linha por linha no arquivo de texto
with open('C:\\Users\\logger\\Downloads\\NFTS\\NFTS_BA.txt', 'w', encoding='ISO-8859-1') as file:
    # Iterar sobre todos os DataFrames (df1, df2, df3) dinamicamente
    for df_name in ['Header', 'result', 'Trailer']:
        df = globals()[df_name]  # Obtém o DataFrame pelo nome da variável
        df.to_csv(file, index=False, sep='\t')  # Escreve o DataFrame no arquivo
