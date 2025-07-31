import os
import pandas as pd

# Obtém o diretório onde o script está sendo executado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Caminho para a planilha
caminho_planilha = os.path.join(diretorio_atual, 'SAP Novo v1.1.xlsx')
# Lê a planilha
df = pd.read_excel(caminho_planilha, dtype=str , sheet_name='Livro SAP')
cod_sp = pd.read_excel(caminho_planilha, '')

def nfts_SP():
#   df = pd.read_excel('/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/SAP Novo v1.1.xlsx',
#                     dtype=str, sheet_name='Livro SAP')
  cod_sp = pd.read_excel('/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos/CODSP.xlsx',
                        dtype=str)

  dtint = input('Data inicio: ')
  dtfim = input('Data fim: ')
  inMunicipal = input('Informar IM: ')
  filial = input('Informe código da filial: ')

  #Alterar tipo de dado da coluna.
  df = df.astype({
      'CNPJ': str,
      'Nota': str,
      'ISS': float,
      'Valor': float
  })

  df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand=True)

  #Seleção Filial e filtros.
  df = df.loc[df['Centro'] == filial]
  df = df.loc[df['Cidade'] != 'SAO PAULO']
  df = df[df['CFOP'].isin(['1933/AA', '2933/AA'])]
  df['%ISS'] = df['%ISS'].str.rstrip('%').astype(float)

  #Criação das colunas personalizadas, parâmetros conforme manual.
  df.insert(3, 'T_Registro', '4')
  df.insert(4, 'T_Documento', '02')
  df.insert(5, 'Serie', '    E')
  df.insert(6, 'SNFTS', 'N')
  df.insert(7, 'Tributação', 'T')
  df.insert(11, 'vDeducao', '000000000000000')
  df.insert(4, 'Ind_CNPJ', '2')
  df.insert(8, 'Regime_T', '0')
  df.insert(11, 'Tipo_End', 'END')
  df.insert(9, 'Complemento', ' ')
  df.insert(12, 'CCM', '00000000')
  df.insert(13, 'T_NFTS', '1')
  df.insert(14, 'C_INSS', '0')
  df.insert(15, 'N_OBRA', '0')
  df.insert(15, 'C_RESERVADO', ' ')
  df.insert(16, 'Data_PGTO', ' ')
  df.insert(16, 'Descrição do Serviço', 'Contratação de Serviços')

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
          return '2'
      # Retorne outros valores de acordo com suas necessidades
      else:
          return np.NAN  # Valor padrão para linhas sem 'ISS' > 0 ou 'ISS' == 0

  df['ISS Retido'] = df.apply(definir_iss_retido, axis=1)  # Aplicar a função a cada linha
  df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
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

  #Parametrização das colunas utilizando 'PAD'
  df['Nota'] = df['Nota'].str.pad(width=12, side='left', fillchar='0')
  df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
  df['Valor'] = df['Valor'].str.pad(width=15, side='left', fillchar='0')
  df['CÓDIGO'] = df['CÓDIGO'].str.pad(width=5, side='left', fillchar='0')
  df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(4))
  df['Razão Social'] = df['Razão Social'].str.pad(width=75, side='left', fillchar=' ')
  df['Logradouro'] = df['Logradouro'].str.pad(width=50, side='right', fillchar=' ')
  df['Número'] = df['Número'].str.pad(width=10, side='right', fillchar=' ')
  df['Complemento'] = df['Complemento'].str.pad(width=30, side='right', fillchar=' ')
  df['Bairro'] = df['Bairro'].str.pad(width=30, side='right', fillchar=' ')
  df['Cidade'] = df['Cidade'].str.pad(width=50, side='right', fillchar=' ')
  df['E-mail'] = df['E-mail'].astype(str).apply(lambda x: x.ljust(75))
  df['C_INSS'] = df['C_INSS'].str.pad(width=12, side='right', fillchar='0')
  df['N_OBRA'] = df['N_OBRA'].str.pad(width=12, side='right', fillchar='0')
  df['C_RESERVADO'] = df['C_RESERVADO'].str.pad(width=200, side='right', fillchar=' ')
  df['Descrição do Serviço'] = df['Descrição do Serviço'].str.pad(width=200, side='right', fillchar=' ')
  df['Data_PGTO'] = df['Data_PGTO'].str.pad(width=8, side='right', fillchar=' ')
  df['UF'] = df['UF'].str.pad(width=2, side='right', fillchar=' ')
  df['CEP'] = df['CEP'].str.pad(width=8, side='right', fillchar='0')

  cabecalho = [f'1002{inMunicipal}{dtint}{dtfim}']
  Header = pd.DataFrame(columns=cabecalho)

  registros = pd.DataFrame()
  registros = pd.concat([df['T_Registro'], df['T_Documento'], df['Serie'], df['Nota'], df['Data documento'], df['SNFTS'],
                        df['Tributação'], df['Valor'], df['vDeducao'], df['CÓDIGO'], df['LC 116'], df['%ISS'],
                        df['ISS Retido'], df['Ind_CNPJ'], df['CNPJ'], df['CCM'], df['Razão Social'], df['Tipo_End'],
                        df['Logradouro'],df['Número'], df['Complemento'], df['Bairro'], df['Cidade'], df['UF'], df['CEP'],
                        df['E-mail'],df['T_NFTS'], df['Regime_T'], df['Data_PGTO'], df['C_INSS'], df['N_OBRA'], df['C_RESERVADO'],
                        df['Descrição do Serviço']],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

  df = df.astype({'Valor': int, })
  num_linhas = len(registros)
  num_linhas_formatted = f'{num_linhas:0>6}'
  Total = df['Valor'].sum()
  Total = str(Total)
  TotalZ = Total.zfill(15)

  radape = ['90' + num_linhas_formatted + TotalZ + '000000000000000']
  footer = pd.DataFrame(columns=radape)

  #Escrever linha por linha no arquivo de texto
  with open(f'/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos TXT/{filial}.txt', 'w', encoding='utf-8') as file:
      #Iterar sobre todos os DataFrames (df1, df2, df3) dinamicamente
      for df_name in ['Header', 'registros', 'footer']:
          df = locals()[df_name]  #Obtém o DataFrame pelo nome da variável
          df.to_csv(file, index=False, sep='\t')  #Escreve o DataFrame no arquivo

def main():
    print('Selecione a Prefeitura\n' +
      '1 - São Paulo \n' +
      '2 - Recife \n' +
      '3 - Cajamar \n'+
      '4 - Camaçari \n'+
      '5 - Gravatai - SC \n'+
      '6 - Invoice SP \n'+
      '7 - Londrina \n'+
      '8 - Rio de Janeiro \n'+
      '9 - São José - SC \n')

    op = int(input('Digite a opção: '))

    if(op == 1):
        nfts_SP()