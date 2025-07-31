import pandas as pd
import numpy as np

dataFrame = pd.read_excel('G:\\Drives compartilhados\\Finance 3.0\\1. Tax\\Fiscal Indiretos\\FILIAL L4B 0001 SP - ATIVA\\DMS\\Importação em lote planilha\\SAP Novo v1.1.xlsx', 
                          sheet_name='Livro SAP', dtype=str)

filial = str(input('Informe a filial: '))
im = str(input('Informe a Incrição Municipal: '))

dataFrame = dataFrame[dataFrame['CFOP'].isin(['1933/AA', '2933/AA'])]
dataFrame = dataFrame[dataFrame['Centro'].isin([filial])]
dataFrame = dataFrame.loc[dataFrame['Cidade'] != 'FORTALEZA']
dataFrame['Data documento'] = pd.to_datetime(dataFrame['Data documento'])
dataFrame['%ISS'] = dataFrame['%ISS'].str.rstrip('%').astype(float)

nfts = pd.DataFrame()
nfts.insert(0, 'CNPJ', dataFrame['CNPJ'])
nfts.insert(1, 'vLayout', '2.0')
nfts.insert(2, 'tipoServico', 2)
nfts.insert(3, 'tipoPrestador', 2)
nfts.insert(4, 'Prestador', dataFrame['Razão Social'])
nfts.insert(5, 'cPais', '1058')
nfts.insert(6, 'cUF', dataFrame['UF'])
nfts.insert(7, 'IBGE', dataFrame['IBGE'])
nfts.insert(8, 'CEP', dataFrame['CEP'])
nfts.insert(9, 'Logradouro', dataFrame['Logradouro'])
nfts.insert(10, 'Número', dataFrame['Número'])
nfts.insert(11, 'Complemento', 'Sem Complemento')
nfts.insert(12, 'Bairro', dataFrame['Bairro'])
nfts.insert(13, 'Telefone', '11958697364')
nfts.insert(14, 'Email', dataFrame['E-mail'])
nfts.insert(15, 'Nota', dataFrame['Nota'])
nfts.insert(16, 'Serie', 'E')
nfts.insert(17, 'DtEmissao', dataFrame['Data documento'].dt.strftime("%d/%m/%Y"))
nfts.insert(18, 'situacaoDoc', '1')
nfts.insert(19, 'cnae', dataFrame['CNAE'])
nfts.insert(20, '%iss', dataFrame['%ISS'])
nfts.insert(21, 'descricao', 'Contratação de serviço')
nfts.insert(22, 'Cart', '')
nfts.insert(23, 'Cobra', '')
nfts.insert(24, 'vServico', dataFrame['Valor'])
nfts.insert(25, 'vDeducao', '')
nfts.insert(26, 'vDescIncond', '')
nfts.insert(27, 'vDescCond', '')
nfts.insert(28, 'vORetencao', '')
nfts.insert(29, 'vIR', '')
nfts.insert(30, 'vPIS', '')
nfts.insert(31, 'vCofins', '')
nfts.insert(32, 'vCsll', '')
nfts.insert(33, 'vINSS', '')
nfts.insert(34, 'nEspelho', '')
nfts.insert(35, 'indicaISSR', '')
nfts.insert(36, 'tTributadoT', '')
nfts.insert(37, 'Imunicipal', '')
nfts.insert(38, 'ImunicipalP', im)
nfts.insert(39, 'TDocumento', '7')
nfts.insert(40, 'Mes', dataFrame['Data documento'].dt.strftime("%m"))
nfts.insert(41, 'Ano', dataFrame['Data documento'].dt.strftime("%Y"))
nfts.insert(42, 'sep', ';')
nfts.insert(43, 'vISS', dataFrame['ISS'])

nfts = nfts.astype({
    'vISS': float,
    'vServico': float,
    'Nota': int
})

def definir_iss_retido(row):
    if row['vISS'] > 0:
        return '1'
    elif row['vISS'] == 0:
        return '2'
    else:
        return np.NAN

nfts['ISS Retido'] = nfts.apply(definir_iss_retido, axis=1)  # Aplicar a função a cada linha
nfts['vServico'] = nfts['vServico'].apply(lambda x: format(round(x, 2), '.2f'))

# Converter a coluna para datetime (se não estiver no formato datetime) e formatar
nfts['CEP'] = nfts['CEP'].str.replace('.', '')
nfts['CEP'] = nfts['CEP'].str.replace('-', '')
nfts['%iss'] = (nfts['%iss'] * 100).round().astype(int)
nfts['%iss'] = nfts['%iss'].apply(lambda x: str(x).zfill(3))
nfts['vServico'] = nfts['vServico'].astype(str).str.replace('.', '')

layout = pd.DataFrame()
layout = pd.concat([nfts['vLayout'], nfts['sep'], nfts['tipoServico'], nfts['sep'], nfts['tipoPrestador'], nfts['sep'], nfts['CNPJ'], nfts['sep'], nfts['Prestador'], 
                    nfts['sep'], nfts['Imunicipal'], nfts['sep'], nfts['cPais'], nfts['sep'], nfts['cUF'], nfts['sep'], nfts['IBGE'], nfts['sep'], nfts['CEP'], nfts['sep'],
                    nfts['Logradouro'], nfts['sep'], nfts['Número'], nfts['sep'], nfts['Complemento'], nfts['sep'], nfts['Bairro'], nfts['sep'], nfts['Telefone'], nfts['sep'],
                    nfts['Email'], nfts['sep'], nfts['TDocumento'], nfts['sep'], nfts['Nota'], nfts['sep'], nfts['Serie'], nfts['sep'], nfts['DtEmissao'], nfts['sep'], 
                    nfts['situacaoDoc'], nfts['sep'], nfts['Mes'], nfts['sep'], nfts['Ano'], nfts['sep'], nfts['cnae'], nfts['sep'], nfts['%iss'], nfts['sep'], nfts['descricao'], nfts['sep'],
                    nfts['cPais'], nfts['sep'], nfts['cUF'], nfts['sep'], nfts['IBGE'], nfts['sep'], nfts['ISS Retido'], nfts['sep'], nfts['Cart'], nfts['sep'], nfts['Cobra'], nfts['sep'],
                    nfts['vServico'], nfts['sep'], nfts['vDeducao'], nfts['sep'], nfts['vDescIncond'], nfts['sep'], nfts['vDescCond'], nfts['sep'], nfts['vORetencao'], nfts['sep'],
                    nfts['vIR'], nfts['sep'], nfts['vPIS'], nfts['sep'], nfts['vCofins'], nfts['sep'], nfts['vCsll'], nfts['sep'], nfts['vINSS'], nfts['sep'], nfts['nEspelho'], nfts['sep'],
                    nfts['indicaISSR'], nfts['sep'], nfts['tTributadoT'], nfts['sep'], nfts['ImunicipalP']], axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

layout.to_csv(f'C:\\Users\\logger\\Downloads\\NFTS\\{filial}.txt', index=False, header=False)
