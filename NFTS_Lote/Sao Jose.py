import pandas as pd

df = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo v1.1.xlsx', 
                   dtype=str, sheet_name='São José')

competencia = input('Informe a competência (MM/AAAA): ')
filialCnpj = input('Informe o CNPJ da Filial: ')
codFilial = input('Informe o Código da Filial: ') #Conforme livro do SAP

#Alterar tipo de dado da coluna.
df = df.astype({
    'CNPJ': str,
    'Nota': str,
    'ISS': float,
    'Valor_Serv': float,
    'Logradouro': str
})

if codFilial == '0048':
    cidade = 'GRAVATAI'
    docT = '10' 
elif codFilial == '0087':
    cidade = 'SAO JOSE'
    docT = '05'

#Seleção Filial e filtros.
df = df.loc[df['Centro'] == codFilial]
df = df.loc[df['Cidade'] !=cidade]
df = df[df['CFOP'].isin(['1933/AA', '2933/AA'])]
df['%ISS'] = df['%ISS'].str.rstrip('%').astype(float)

#Criação das colunas personalizadas, parâmetros conforme manual.
df.insert(1, 'T_Registro10', '10')
df.insert(2, 'T_Registro20', '20')
df.insert(2, 'T_Registro30', '30')
df.insert(3, 'T_Serviço', '2')
df.insert(4, 'T_Documento', docT)
df.insert(5, 'Competencia', competencia)
df.insert(6, 'T_PessoaP', 'J')
df.insert(7, 'T_PessoaT', 'J')
df.insert(8, 'Situaçao', 'E')
df.insert(9, 'CNPJT', filialCnpj)
df.insert(10, 'Simples', 'N')
df.insert(11, 'Sep', ';')
df.insert(12, 'C_RESERVADO', '')
df.insert(13, 'RISSOBRA', '0')
df.insert(13, 'Deducao', 0.00)
df.insert(14, 'TPrestador', 'N')
df.insert(15, 'T_Servico', '2')
df.insert(16, 'Complemento', ' ')
df.insert(17, 'Fone', ' ')
df.insert(16, 'Observacoes', ' ')

df['ISS Retido'] = df.apply(lambda row: '01' if row['ISS'] > 0 else '14', axis=1)

df['Data documento'] = df['Data documento'].str.replace('-', '/')
df['Data documento'] = pd.to_datetime(df['Data documento'])
df['Data documento'] = df['Data documento'].dt.strftime('%d/%m/%Y')
df['CEP'] = df['CEP'].str.replace('.', '')
df['CEP'] = df['CEP'].str.replace('-', '')
df['LC 116/2003'] = df['LC 116/2003'].str.replace('.', '')
df['%ISS'] = df['%ISS'].replace(0.00, 3.00)

#Criação das colunas conforme regra do valor.
df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
df['Deducao'] = df['Deducao'].apply(lambda x: format(round(x, 2), '.2f'))
df['ISS'] = df['ISS'].apply(lambda x: format(round(x, 2), '.2f'))
df['%ISS'] = df['%ISS'].apply(lambda x: format(round(x, 2), '.2f'))

#Parametrização das colunas utilizando 'PAD'
df['Nota'] = df['Nota'].str.pad(width=15, side='left', fillchar='0')
df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
df['Código municipios'] = df['Código municipios'].str.pad(width=7, side='left', fillchar='0')
df['RISSOBRA'] = df['RISSOBRA'].str.pad(width=10, side='left', fillchar='0')
df['LC 116/2003'] = df['LC 116/2003'].str.pad(width=7, side='left', fillchar='0')
df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(6))
df['ISS'] = df['ISS'].apply(lambda x: str(x).zfill(18))
df['Deducao'] = df['Deducao'].apply(lambda x: str(x).zfill(18))
df['Valor_Serv'] = df['Valor_Serv'].apply(lambda x: str(x).zfill(18))
df['Razão Social'] = df['Razão Social'].str.pad(width=40, side='left', fillchar=' ')
df['Logradouro'] = df['Logradouro'].str.pad(width=40, side='right', fillchar=' ')
df['Número'] = df['Número'].str.pad(width=6, side='right', fillchar=' ')
df['Bairro'] = df['Bairro'].str.pad(width=20, side='right', fillchar=' ')
df['Cidade'] = df['Cidade'].str.pad(width=30, side='left', fillchar=' ')
df['UF'] = df['UF'].str.pad(width=2, side='right', fillchar=' ')
df['CEP'] = df['CEP'].str.pad(width=8, side='right', fillchar='0')
df['Complemento'] = df['Complemento'].str.pad(width=20, side='right', fillchar=' ')
df['Observacoes'] = df['Observacoes'].str.pad(width=100, side='right', fillchar=' ')
df['Fone'] = df['Fone'].str.pad(width=12, side='right', fillchar=' ')

RG10 = pd.DataFrame()
RG10 = pd.concat([df['T_Registro10'], df['Sep'], df['T_Serviço'],df['Sep'], df['T_Documento'], df['Sep'], df['Nota'], df['Sep'], 
                    df['Competencia'], df['Sep'], df['T_PessoaP'], df['Sep'], df['CNPJ'], df['Sep'], df['T_PessoaT'], df['Sep'], 
                    df['CNPJT'], df['Sep'], df['Data documento'], df['Sep'], df['Valor_Serv'], df['Sep'], df['Situaçao'], df['Sep'], 
                    df['Observacoes'], df['Sep'], df['Simples'], df['Sep']], axis=1, 
                   ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

RG20 = pd.DataFrame()
RG20 = pd.concat([df['T_Registro20'], df['Sep'], df['T_Servico'], df['Sep'], df['T_Documento'], df['Sep'], df['Nota'], df['Sep'], df['Competencia'], df['Sep'],
                  df['T_PessoaP'], df['Sep'], df['CNPJ'], df['Sep'], df['T_PessoaT'], df['Sep'], df['CNPJT'], df['Sep'], 
                  df['LC 116/2003'], df['Sep'], df['%ISS'], df['Sep'], df['Valor_Serv'], df['Sep'], df['Deducao'], df['Sep'], 
                  df['ISS'], df['Sep'], df['Código municipios'], df['Sep'], df['ISS Retido'], df['Sep'], df['TPrestador'], df['Sep'], df['RISSOBRA'], df['Sep']],
                 axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

RG30 = pd.DataFrame()
RG30 = pd.concat([df['T_Registro30'], df['Sep'], df['T_PessoaP'], df['Sep'], df['CNPJ'], df['Sep'], 
                  df['Razão Social'], df['Sep'], df['Logradouro'], df['Sep'], df['Número'], df['Sep'],
                  df['Complemento'], df['Sep'], df['Bairro'], df['Sep'], df['Cidade'], df['Sep'],
                  df['UF'], df['Sep'], df['CEP'], df['Sep'], df['Fone'], df['Sep'], df['Fone'],df['Sep']],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

interleaved_dfs = []

for i in range(len(RG10)):
    interleaved_dfs.append(RG10.iloc[i])
    interleaved_dfs.append(RG20.iloc[i])
    interleaved_dfs.append(RG30.iloc[i])

result = pd.DataFrame(interleaved_dfs)

result.to_csv('C:\\Users\\logger\\Downloads\\NFTS\\NFTS_SJ.txt', index=False, header=False)
