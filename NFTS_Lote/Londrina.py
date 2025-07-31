import pandas as pd

df = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo v1.1.xlsx',
                   dtype=str, sheet_name='Livro SAP')

#Alterar tipo de dado da coluna.
df = df.astype({
    'CNPJ': str,
    'Nota': str,
    'ISS': float,
    'Valor': float,
})

#Seleção Filial e filtros.
df = df.loc[df['Centro'] == '0107']
df = df.loc[df['Cidade'] != 'LONDRINA']
df = df[df['CFOP'].isin(['1933/AA' , '2933/AA'])]

df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
df['Valor'] = df['Valor'].str.replace('.', ',')
df['LC 116'] = df['LC 116'].str.replace('.', '')
df['Data documento'] = pd.to_datetime(df['Data documento'])
df['dia'] = df['Data documento'].dt.day

df.loc[df['ISS'] > 0, 'situacaoNF'] = 'tt'
df.loc[df['ISS'] == 0, 'situacaoNF'] = 'nt'

df.insert(1, 'sep', ';')
df.insert(2, 'serie', 'E')
df.insert(4, 'CMC', '2899183')
df.insert(5, 'T_documento', 'T')
df.insert(6, 'L_concluido', 'C')
df.insert(7, 'CC', '1')

layout = pd.DataFrame()
layout = pd.concat([df['CNPJ'], df['sep'], df['Nota'], df['sep'], df['serie'], df['sep'], df['sep'], df['dia'], df['sep'],
                    df['LC 116'], df['sep'], df['situacaoNF'], df['sep'], df['Valor'], df['sep'], df['CMC'],
                    df['sep'], df['T_documento'], df['sep'], df['sep'], df['L_concluido'], df['sep'],df['Valor'],df['sep'], 
                    df['CC'], df['sep'], df['sep']],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

layout.to_csv('C:\\Users\\logger\\Downloads\\NFTS\\NFTS_PR.txt', index=False, header=False)
