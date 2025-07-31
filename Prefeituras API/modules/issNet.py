def IssNet():
  df = pd.read_excel('/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/SAP Novo v1.1.xlsx', dtype=str, sheet_name='Livro SAP')

  def Municipio(filial):
    if filial == '0046':
      municipio = 'BRASILIA'
    elif filial == '0077':
      municipio = 'APARECIDA DE GOIANIA'
    return municipio

  def IMunicipal(filial):
    if filial == '0046':
      inscricao = '0795990700349'
    elif filial == '0077':
      inscricao = '14471871'
    return inscricao

  def CodNF(filial):
    if filial == '0046':
      codNF = '5'
    elif filial == '0077':
      codNF = '4'
    return codNF

  # Variaveis de instância para o script atenda todas as filiais.
  filial = str(input('Informe o código da filial: '))
  mesCompetencia = input('Mês de Competência: ')
  anoCompetencia = input('Ano de Competência: ')

  df = df.astype({
      'CNPJ': str,
      'Nota': str,
      'ISS': float,
      'Valor': float,
      'Base ISS': float,
      '%ISS': float,
      'vLiquido': float
  })

  # Filtra o DataFrame para pegar apenas as linhas com o mês específico
  df = df.loc[df['Centro'] == filial]
  df = df.loc[df['Cidade'] != Municipio(filial)]

  # Converter a coluna para datetime (se não estiver no formato datetime) e formatar
  df['Data documento'] = pd.to_datetime(df['Data documento']).dt.strftime("%d/%m/%Y")
  df['Data documento'] = df['Data documento'].str.replace('/', '')

  # Parametrizando colunas de valor com 2 casas decimais após o .
  df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
  df['vLiquido'] = df['vLiquido'].apply(lambda x: format(round(x, 2), '.2f'))
  df['Base ISS'] = df['Base ISS'].apply(lambda x: format(round(x, 2), '.2f'))
  df['%ISS'] = df['%ISS'].apply(lambda x: format(round(x, 1), '.1f'))

  def definir_iss_retido(row):
      if row['ISS'] > 0:
          return '1'
      elif row['ISS'] == 0:
          return '0'

  df = df.drop_duplicates(subset=['Documento MIRO'])

  # Header do arquivo
  dataHora = datetime.now()
  data_hora_formatada = dataHora.strftime("%H:%M %d/%m/%Y")
  cabecalho = [f'{IMunicipal(filial)};{mesCompetencia};{anoCompetencia};{data_hora_formatada}L4B LOGISTICA LTDA;1;EXPORTACAO DECLARACAO ELETRONICA-ONLINE-NOTA CONTROL;']
  Header = pd.DataFrame(columns=cabecalho)

  df.insert(1, 'T_Documento', CodNF(filial)) # Conforme manual o modelo
  df.insert(2, 'IM_Prestador', '') # Teste de IM do prestador
  df.insert(3, 'CódigoArea', '')
  df['ISS Retido'] = df.apply(definir_iss_retido, axis=1)  # Aplicar a função a cada linha
  df['LC 116'] = df['LC 116'].str.replace('.', '')
  df.insert(4, 'uEconomica', '0')
  df['CEP'] = df['CEP'].str.replace('.', '')
  df['CEP'] = df['CEP'].str.replace('-', '')

  registros = pd.DataFrame()
  registros = pd.concat([df['T_Documento'] + ";" +  df['Nota'] + ";" + df['Valor'] + ";" + df['vLiquido'] +
                        ";" + df['%ISS'] + ";" + df['Data documento'] + ";" + df['Data documento'] + ";" +
                        df['CNPJ'] + ";" + df['Razão Social'] + ";" + df['IM_Prestador'] + ";" + df['ISS Retido'] + ";" +
                        df['CEP'] + ";" + df['Logradouro'] + ";" + df['Número'] + ";" + df['Bairro'] + ";" + df['Cidade'] + ";" +
                        df['UF'] + ";" + df['DDD'] + ";" + df['ISS Retido'] + ";" + df['LC 116'] + ";" + df['uEconomica'] + ";"
                        ],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

  # Escrever linha por linha no arquivo de texto
  with open(f'/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos TXT/{filial}.txt', 'w', encoding='utf-8') as file:
      #Iterar sobre todos os DataFrames (df1, df2) dinamicamente
      for df_name in ['Header', 'registros']:
          df = locals()[df_name]  #Obtém o DataFrame pelo nome da variável
          df.to_csv(file, index=False, sep='\t')  #Escreve o DataFrame no arquivo
          