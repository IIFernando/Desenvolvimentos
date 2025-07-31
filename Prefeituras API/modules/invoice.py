def invoice():
  # 1. Escopo de acesso ao Google Sheets e Drive
  scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

  # 2. Caminho para o arquivo da conta de serviço
  creds = ServiceAccountCredentials.from_json_keyfile_name("/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos/SK_GoogleSheet.json", scope)

  # 3. Autentica e inicializa o cliente
  client = gspread.authorize(creds)

  # 4. Abre a planilha (verifique o nome exato e se a conta de serviço tem acesso)
  spreadsheet = client.open("Fechamento Municipal - 2025")

  # 5. Seleciona a aba (worksheet) — pode usar o nome ou índice
  worksheet = spreadsheet.worksheet("Importações")  # ou .get_worksheet(0)

  # 6. Converte os dados em DataFrame
  data = worksheet.get_all_records()  # retorna como lista de dicionários
  df = pd.DataFrame(data)

  # Datas em formato americano.
  dtint = input('Data inicio: ')
  dtfim = input('Data fim: ')
  inMunicial = input('Informar IM: ')
  filial = input('Informe código da filial: ')

  # Filtros
  df = df.loc[df['Empresa'] == filial]
  df = df[df['NFTS SP'].isnull()]

  df.insert(3, 'T_Registro', '4')
  df.insert(4, 'T_Documento', '01')
  df.insert(5, 'Serie', 'INV')
  df.insert(6, 'SNFTS', 'N')
  df.insert(7, 'Tributação', 'T')
  df.insert(11, 'vDeducao', '000000000000000')
  df.insert(4, 'Ind_CNPJ', '3')
  df.insert(8, 'Regime_T', '0')
  df.insert(11, 'Tipo_End', ' ')
  df.insert(9, 'Complemento', ' ')
  df.insert(12, 'CCM', '00000000')
  df.insert(13, 'T_NFTS', '1')
  df.insert(14, 'C_INSS', '0')
  df.insert(15, 'N_OBRA', '0')
  df.insert(15, 'C_RESERVADO', ' ')
  df.insert(16, 'Data_PGTO', ' ')
  df.insert(17, 'ISS Retido', '1')
  df.insert(18, 'CNPJ', '0')
  df.insert(18, 'LOGRADOURO', 'EUA')
  df.insert(18, 'NÚMERO', ' ')
  df.insert(18, 'BAIRRO', ' ')
  df.insert(18, 'CIDADE', ' ')
  df.insert(18, 'UF', ' ')
  df.insert(18, 'CEP', '0')
  df.insert(18, 'EMAIL', ' ')
  df.insert(18, 'Descrição do Serviço', 'Prestação de serviços do exterior.')

  df['Valor R$'] = df['Valor R$'].apply(lambda x: format(round(x, 2), '.2f'))
  df['%ISS'] = (df['%ISS'] * 100).round().astype(int)

  df = df.astype({
      'Valor R$': str,
  })

  # df['%ISS'] = df['%ISS'].str.replace(',', '').str.replace('%', '')
  df['Valor R$'] = df['Valor R$'].str.replace('.', '').str.replace(',', '').str.replace('R$', '')
  df['Data Fechamento'] = df['Data Fechamento'].str.replace('/', '')
  df['Cód. ISS'] = df['Cód. ISS'].str.replace('.', '')
  df['Data Fechamento'] = pd.to_datetime(df['Data Fechamento'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y %m %d')
  # df['Data Fechamento'] = pd.to_datetime(df['Data Fechamento'], format='%d%m%Y').dt.strftime('%Y %m %d')
  df['Data Fechamento'] = df['Data Fechamento'].str.replace(' ', '')

  # Parametrização das colunas utilizando 'PAD'
  df['Invoice'] = df['Invoice'].str.pad(width=12, side='left', fillchar='0')
  df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
  df['Valor R$'] = df['Valor R$'].str.pad(width=15, side='left', fillchar='0')
  df['SUBITEM'] = df['SUBITEM'].str.pad(width=5, side='left', fillchar='0')
  df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(4))
  df['Fornecedor'] = df['Fornecedor'].astype(str).str.rjust(75)
  df['LOGRADOURO'] = df['LOGRADOURO'].astype(str).str.rjust(50)
  df['Serie'] = df['Serie'].astype(str).str.rjust(5)
  df['NÚMERO'] = df['NÚMERO'].astype(str).str.rjust(12)
  df['Complemento'] = df['Complemento'].astype(str).str.rjust(30)
  df['BAIRRO'] = df['BAIRRO'].astype(str).str.rjust(30)
  df['CIDADE'] = df['CIDADE'].astype(str).str.rjust(50)
  df['EMAIL'] = df['EMAIL'].astype(str).str.rjust(75)
  df['C_INSS'] = df['C_INSS'].str.pad(width=12, side='right', fillchar='0')
  df['N_OBRA'] = df['N_OBRA'].str.pad(width=12, side='right', fillchar='0')
  df['C_RESERVADO'] = df['C_RESERVADO'].astype(str).str.rjust(200)
  df['Descrição do Serviço'] = df['Descrição do Serviço'].astype(str).str.rjust(200)
  df['Data_PGTO'] = df['Data_PGTO'].str.pad(width=8, side='right', fillchar=' ')
  df['UF'] = df['UF'].str.pad(width=2, side='right', fillchar=' ')
  df['CEP'] = df['CEP'].str.pad(width=8, side='right', fillchar='0')

  dfNFTS = pd.DataFrame()

  dfNFTS[f'100259871091{dtint}{dtfim}'] = pd.concat(
      [df['T_Registro'], df['T_Documento'], df['Serie'], df['Invoice'], df['Data Fechamento'], df['SNFTS'],
      df['Tributação'], df['Valor R$'], df['vDeducao'], df['SUBITEM'], df['Cód. ISS'], df['%ISS'],
      df['ISS Retido'], df['Ind_CNPJ'], df['CNPJ'], df['CCM'], df['Fornecedor'], df['Tipo_End'], df['LOGRADOURO'],
      df['NÚMERO'], df['Complemento'], df['BAIRRO'], df['CIDADE'], df['UF'], df['CEP'], df['EMAIL'],
      df['T_NFTS'], df['Regime_T'], df['Data_PGTO'], df['C_INSS'], df['N_OBRA'], df['C_RESERVADO'],
      df['Descrição do Serviço']],
      axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

  cabecalho = [f'1002{inMunicial}{dtint}{dtfim}']
  Header = pd.DataFrame(columns=cabecalho)

  df = df.astype({'Valor R$': int, })
  num_linhas = len(dfNFTS)
  num_linhas_formatted = f'{num_linhas:0>7}'
  Total = df['Valor R$'].sum()
  Total = str(Total)
  TotalZ = Total.zfill(15)

  radape = ['90' + num_linhas_formatted + TotalZ + '000000000000000']
  footer = pd.DataFrame(columns=radape)

  # Escrever linha por linha no arquivo de texto
  file_path = f'/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos TXT/{filial}.txt'
  with open(file_path, 'w', encoding='utf-8') as file:
      # Iterar sobre todos os DataFrames (df1, df2, df3) dinamicamente
      for df_name in ['Header', 'dfNFTS', 'footer']:
          df = locals()[df_name]  # Obtém o DataFrame pelo nome da variável
          df.to_csv(file, index=False, sep='\t')  # Escreve o DataFrame no arquivo