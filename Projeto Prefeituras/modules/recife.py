import pandas as pd

def nfts_Recife(template_file, dtinicio, dtfim,inMunicipal, cnpj):
  df = pd.read_excel(template_file, dtype=str)

  # Converter colunas para numérico para evitar erro de comparação
  df['ISS Retido'] = pd.to_numeric(df['ISS Retido'], errors='coerce').fillna(0)
  df['ISS'] = pd.to_numeric(df['ISS'], errors='coerce').fillna(0)

  df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand=True)

  #Seleção Filial e filtros.
  df = df.loc[df['Cidade'] != 'RECIFE']

  #Criação das colunas personalizadas, parâmetros conforme manual.
  df.insert(12, 'C_RESERVADO1', '')
  df.insert(13, 'C_RESERVADO2', '')
  df.insert(14, 'C_RESERVADO3', '')

  #Criação das colunas conforme regra do valor.
  def definir_iss_retido(row):
      """
      """
      if row['ISS Retido'] > 0:
          return '1'
      elif row['ISS Retido'] == 0:
          return '0'

  def t_tributacao(row):
      """
      """
      if row['ISS'] > 0:
          return '01'
      else:
          return '02' 

  df['Tributacao'] = df.apply(t_tributacao, axis=1)  # Aplicar a função a cada linha
  df['ISS'] = df.apply(definir_iss_retido, axis=1)  # Aplicar a função a cada linha

  # Converter para float antes de aplicar round e format
  for col in ['Valor', '%ISS']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

  df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
  df['%ISS'] = (df['%ISS'] * 100).round().astype(int)

  df['Data documento'] = df['Data documento'].str.replace('-', '')
  df['LC 116'] = df['LC 116'].str.replace('.', '')
  df['CEP'] = df['CEP'].str.replace('.', '')
  df['CEP'] = df['CEP'].str.replace('-', '')
  df['Valor'] = df['Valor'].astype(str).str.replace('.', '')
  df['ISS Retido'] = df['ISS Retido'].astype(str).str.replace('.', '')

  df['Telefone'] = df['Telefone'].str.replace('-', '')
  df['Telefone'] = df['Telefone'].str.replace(' ', '')
  df['Telefone'] = df['Telefone'].str.replace('(', '')
  df['Telefone'] = df['Telefone'].str.replace(')', '')
  df['Telefone'] = df['Telefone'].str.replace('/', '')
  
  df['CNAE'] = df['CNAE'].str.replace('.', '')
  df['CNAE'] = df['CNAE'].str.replace('-', '')

# Preencher NaN com string vazia para campos que precisam ser espaços
  for col in ['N_OBRA', 'Anotacao_Tecnica', 'Descrição do Serviço', 'C_RESERVADO1', 'C_RESERVADO2', 'C_RESERVADO3', 'Complemento']:
    df[col] = df[col].fillna('')

#Parametrização das colunas utilizando 'PAD'
  df['Nota'] = df['Nota'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
  df['T_Serie'] = df['T_Serie'].str.slice(0, 5).str.pad(width=5, side='left', fillchar=' ')
  df['CNPJ'] = df['CNPJ'].str.slice(0, 14).str.pad(width=14, side='left', fillchar='0')
  df['Valor'] = df['Valor'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
  df['vDeducao'] = df['vDeducao'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
  df['ISS Retido'] = df['ISS Retido'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
  df['CNAE'] = df['CNAE'].str.slice(0, 20).str.pad(width=20, side='left', fillchar='0')
  df['Telefone'] = df['Telefone'].str.slice(0, 11).str.pad(width=11, side='left', fillchar='0')
  df['LC 116'] = df['LC 116'].str.slice(0, 4).str.pad(width=4, side='left', fillchar='0')
  df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(5))
  df['Razão Social'] = df['Razão Social'].str.slice(0, 115).str.pad(width=115, side='left', fillchar=' ')
  df['Logradouro'] = df['Logradouro'].str.slice(0, 125).str.pad(width=125, side='right', fillchar=' ')
  df['Número'] = df['Número'].str.slice(0, 10).str.pad(width=10, side='right', fillchar=' ')
  df['Complemento'] = df['Complemento'].str.slice(0, 60).str.pad(width=60, side='right', fillchar=' ')
  df['Bairro'] = df['Bairro'].str.slice(0, 72).str.pad(width=72, side='right', fillchar=' ')
  df['Cidade'] = df['Cidade'].str.slice(0, 50).str.pad(width=50, side='right', fillchar=' ')
  df['E-mail'] = df['E-mail'].str.slice(0, 80).str.pad(width=80, side='right', fillchar=' ')
  df['Anotacao_Tecnica'] = df['Anotacao_Tecnica'].str.slice(0, 15).str.pad(width=15, side='right', fillchar=' ')
  df['N_OBRA'] = df['N_OBRA'].str.slice(0, 15).str.pad(width=15, side='right', fillchar=' ')
  df['C_RESERVADO1'] = df['C_RESERVADO1'].str.slice(0, 54).str.pad(width=54, side='right', fillchar=' ')
  df['C_RESERVADO2'] = df['C_RESERVADO2'].str.slice(0, 30).str.pad(width=30, side='right', fillchar=' ')
  df['C_RESERVADO3'] = df['C_RESERVADO3'].str.slice(0, 30).str.pad(width=30, side='right', fillchar=' ')
  df['Descrição do Serviço'] = df['Descrição do Serviço'].str.slice(0, 100).str.pad(width=100, side='right', fillchar=' ')
  df['UF'] = df['UF'].str.slice(0, 2).str.pad(width=2, side='right', fillchar=' ')
  df['CEP'] = df['CEP'].str.slice(0, 8).str.pad(width=8, side='right', fillchar='0')

  cabecalho = [f'100032{cnpj}{inMunicipal}{dtinicio}{dtfim}']
  Header = pd.DataFrame(columns=cabecalho)

  registros = pd.DataFrame()
  registros = pd.concat([df['T_Registro'], df['T_Documento'], df['T_Serie'], df['Nota'], df['Data documento'],
                        df['SNFTS'], df['Ind_CNPJ'], df['CNPJ'], df['CCM'], df['IE'], df['Razão Social'],
                        df['Tipo_End'], df['Logradouro'], df['Número'], df['Complemento'], df['Bairro'], df['Cidade'],
                        df['UF'], df['CEP'], df['Telefone'], df['E-mail'], df['Tributacao'], df['C_RESERVADO1'],
                        df['OP_Simples'], df['LC 116'], df['CNAE'], df['%ISS'], df['Valor'], df['vDeducao'],
                        df['C_RESERVADO2'], df['ISS Retido'], df['ISS'], df['Data documento'], df['N_OBRA'],
                        df['Anotacao_Tecnica'], df['Descrição do Serviço']
                        ],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

  df = df.astype({'Valor': float})
  df = df.astype({'vDeducao': float})
        
  num_linhas = len(registros)
  num_linhas_formatted = f'{num_linhas:0>8}'
  Total = df['Valor'].sum()
  TotalDeducao = df['vDeducao'].sum()
        
  Total = str(Total)
  TotalDeducao = str(TotalDeducao)
        
  Total = Total.replace('.', '')
  TotalDeducao = TotalDeducao.replace('.', '')
  TotalZ = Total.zfill(16)
  TotalDeducaoZ = TotalDeducao.zfill(15)

  radape = ['90' + num_linhas_formatted + TotalZ + TotalDeducaoZ]
  footer = pd.DataFrame(columns=radape)

  # Construir string final igual São Paulo
  content = ''
  content += Header.columns[0] + '\n'
  for registro in registros:
      content += registro + '\n'
  content += footer.columns[0] + '\n'
  return content
