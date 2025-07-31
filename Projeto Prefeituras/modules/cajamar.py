import pandas as pd

def nfts_Cajamar(template_file, data, cnpj):
    # Ler o arquivo Excel do template
    df = pd.read_excel(template_file, dtype=str)

    # Alterar tipo de dado da coluna
    df = df.astype({
        'CNPJ': str,
        'ISS': float,
        'Valor': float
    })

    # Separar data e hora
    df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand=True)

    # Criação das colunas personalizadas
    df.insert(1, 'CNPJ_Filial', cnpj)
    df.insert(2, 'D_Lançamento', data)
    df.loc[df['ISS'] > 0, 'ISS Retido'] = 'T'
    df.loc[df['ISS'] == 0, 'ISS Retido'] = 'R'

    # Criação das colunas conforme regra do valor
    df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))

    # Limpeza e preparação dos dados
    df.drop(['HORA'], axis=1, inplace=True)

    # Formatação das colunas
    df['Data documento'] = df['Data documento'].str.replace('-', '')
    df['LC 116'] = df['LC 116'].str.replace('.', '')
    df['Valor'] = df['Valor'].str.replace('.', '')

    # Parametrização das colunas utilizando 'PAD'
    df['Serie'] = df['Serie'].str.slice(0, 2).str.pad(width=2, side='left', fillchar=' ')
    df['Nota'] = df['Nota'].str.slice(0, 6).str.pad(width=6, side='left', fillchar='0')
    df['T_NFTS'] = df['T_NFTS'].str.slice(0, 5).str.pad(width=5, side='left', fillchar='0')
    df['LC 116'] = df['LC 116'].str.slice(0, 4).str.pad(width=4, side='left', fillchar='0')
    df['Valor'] = df['Valor'].str.pad(width=14, side='left', fillchar='0')
    df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
    df['Municipio_T'] = df['Municipio_T'].str.pad(width=50, side='right', fillchar=' ')

    # Criação da série de NFTS
    dfNFTS = pd.Series(df['CNPJ_Filial'] + df['T_NFTS'] + df['Serie'] + df['Nota'] + df['LC 116'] + df['ISS Retido'] +
                       df['Data documento'] + df['Valor'] + df['Valor'] + df['CNPJ'] + df['Municipio_T'] + df['D_Lançamento'])

    # Criar uma string para armazenar o conteúdo
    content = ''
    
    # Adicionar os registros
    for registro in dfNFTS:
        content += registro + '\n'
    
    # Retornar o conteúdo como string
    return content