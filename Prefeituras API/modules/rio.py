def nfts_Rio():
  df = pd.read_excel('/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/SAP Novo v1.1.xlsx', dtype=str, sheet_name='Livro SAP')
  cod_rj = pd.read_excel('/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos/CODRJ.xlsx', dtype=str)

  dtint = input('Data inicio: ')
  dtfim = input('Data fim: ')
  inMunicial = input('Informar IM: ')
  cnpj = input('Informar CNPJ: ')
  filial = input('Informe a filial: ')

  inMunicipal_formatted = f'{inMunicial:0>15}'

  # Alterar tipo de dado da coluna.
  df = df.astype({
      'CNPJ': str,
      'Nota': str,
      'ISS': float,
      'Valor': float
  })

  df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand=True)

  # Seleção Filial e filtros.
  df = df.loc[df['Centro'] == filial]
  df = df.loc[(df['Cidade'] != 'RIO DE JANEIRO') & (df['Cidade'] != 'MARICA')]
  df = df[df['CFOP'].isin(['1933/AA', '2933/AA'])]
  df['%ISS'] = df['%ISS'].str.rstrip('%').astype(float)

  # Criação das colunas personalizadas, parâmetros conforme manual.
  df.insert(1, 'T_Registro', '40')  # Tipo de Registro
  df.insert(2, 'T_Documento', '01')  # Tipo da Nota Convencional
  df.insert(3, 'Serie', '    E')  # Série da Nota Convencional
  df.insert(4, 'SNFTS', '1')  # Status da Nota Convencional
  df.insert(5, 'Ind_CNPJ', '2')  # Identificação de CPF ou CNPJ do Prestador
  df.insert(6, 'IM', '000000000000000')  # Inscrição Municipal do Prestador
  df.insert(7, 'IE', '000000000000000')  # Inscrição Estadual do Prestador
  df.insert(10, 'Tipo_End', 'END')  # Tipo do Endereço do Prestador.
  df.insert(12, 'Telefone', '           ')  # Telefone de Contato do Prestador.
  df.insert(13, 'o_Simples', '0')  # Opção Pelo Simples
  df.insert(14, 'Anotacao', ' ')  # Anotação de Responsabilidade Técnica para serviços de construção civil.
  df.insert(15, 'vDeducao', '000000000000000')
  df.insert(16, 'Complemento', ' ')
  df.insert(17, 'Beneficio', '000')
  df.insert(18, 'N_OBRA', ' ')
  df.insert(19, 'C_RESERVADO23', ' ')  # Reservado
  df.insert(20, 'C_RESERVADO30', ' ')  # Reservado
  df.insert(21, 'C_RESERVADO26', ' ')  # Reservado
  df.insert(22, 'Descrição do Serviço', 'Contratação de Serviços')

  # Tributação de Serviços da Nota conforme regra do valor de ISS
  df.loc[df['ISS'] > 0, 'T_tributacao'] = '01'
  df.loc[df['ISS'] == 0, 'T_tributacao'] = '02'
  df.loc[df['ISS'] > 0, 'T_ISS'] = '1'
  df.loc[df['ISS'] == 0, 'T_ISS'] = '0'
  df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
  df['%ISS'] = (df['%ISS'] * 100).round().astype(int)

  # União das planilha base, trazendo os dados cadastrais do Prestador.
  df = pd.merge(df, cod_rj, on='LC 116', how='inner')

  df.drop_duplicates(['Documento MIRO'], inplace=True)

  df['Data documento'] = df['Data documento'].str.replace('-', '')
  df['LC 116'] = df['LC 116'].str.replace('.', '')
  df['CEP'] = df['CEP'].str.replace('.', '')
  df['CEP'] = df['CEP'].str.replace('-', '')
  df['Valor'] = df['Valor'].str.replace('.', '')
  df['CÓDIGO'] = df['CÓDIGO'].str.replace('.', '')

  df.loc[(df['LC 116'] == '0705') | (df['LC 116'] == '0702'), 'N_OBRA'] = 'CO1'

  df = df.astype({
      'ISS': str,
  })

  df['ISS'] = df['ISS'].str.replace('.', '')

  # Parametrização das colunas utilizando 'PAD'
  df['Nota'] = df['Nota'].str.pad(width=15, side='left', fillchar='0')
  df['CNPJ'] = df['CNPJ'].str.pad(width=14, side='left', fillchar='0')
  df['Valor'] = df['Valor'].str.pad(width=15, side='left', fillchar='0')
  df['ISS'] = df['ISS'].str.pad(width=15, side='left', fillchar='0')
  df['LC 116'] = df['LC 116'].str.pad(width=4, side='left', fillchar='0')
  df['CÓDIGO'] = df['CÓDIGO'].str.pad(width=5, side='left', fillchar='0')
  df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(5))
  df['Razão Social'] = df['Razão Social'].str.pad(width=115, side='left', fillchar=' ')
  df['Logradouro'] = df['Logradouro'].str.pad(width=125, side='right', fillchar=' ')
  df['Número'] = df['Número'].str.pad(width=10, side='right', fillchar=' ')
  df['Complemento'] = df['Complemento'].str.pad(width=60, side='right', fillchar=' ')
  df['Bairro'] = df['Bairro'].str.pad(width=72, side='right', fillchar=' ')
  df['Cidade'] = df['Cidade'].str.pad(width=50, side='right', fillchar=' ')
  df['E-mail'] = df['E-mail'].astype(str).apply(lambda x: x.ljust(80))
  df['Anotacao'] = df['Anotacao'].str.pad(width=15, side='right', fillchar=' ')
  df['N_OBRA'] = df['N_OBRA'].str.pad(width=15, side='left', fillchar=' ')
  df['C_RESERVADO23'] = df['C_RESERVADO23'].str.pad(width=54, side='right', fillchar=' ')
  df['C_RESERVADO30'] = df['C_RESERVADO30'].str.pad(width=30, side='right', fillchar=' ')
  df['C_RESERVADO26'] = df['C_RESERVADO26'].str.pad(width=11, side='right', fillchar=' ')
  df['Descrição do Serviço'] = df['Descrição do Serviço'].str.pad(width=100, side='right', fillchar=' ')
  df['UF'] = df['UF'].str.pad(width=2, side='right', fillchar=' ')
  df['CEP'] = df['CEP'].str.pad(width=8, side='right', fillchar='0')

  cabecalho = [f'100032{cnpj}{inMunicipal_formatted}{dtint}{dtfim}']
  Header = pd.DataFrame(columns=cabecalho)

  registros = pd.DataFrame()
  registros = pd.concat([df['T_Registro'], df['T_Documento'], df['Serie'], df['Nota'], df['Data documento'],
                        df['SNFTS'], df['Ind_CNPJ'], df['CNPJ'], df['IM'], df['IE'], df['Razão Social'],
                        df['Tipo_End'], df['Logradouro'], df['Número'], df['Complemento'], df['Bairro'],
                        df['Cidade'], df['UF'], df['CEP'], df['Telefone'], df['E-mail'], df['T_tributacao'],
                        df['C_RESERVADO23'], df['o_Simples'], df['LC 116'], df['C_RESERVADO26'],
                        df['Beneficio'], df['CÓDIGO'], df['%ISS'], df['Valor'], df['vDeducao'],
                        df['C_RESERVADO30'], df['ISS'], df['T_ISS'], df['Data documento'],df['N_OBRA'],
                        df['Anotacao'], df['Descrição do Serviço']],axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

  df = df.astype({'Valor': int, })

  num_linhas = len(registros)
  num_linhas = str(num_linhas)
  num_linhas_formatted = f'{num_linhas:0>8}'
  Total = df['Valor'].sum()
  Total = str(Total)
  # TotalZ = Total.zfill(15)
  Total_formatted = f'{Total:0>15}'

  radape = ['90' + num_linhas_formatted + Total_formatted + '000000000000000']
  footer = pd.DataFrame(columns=radape)

  # Escrever linha por linha no arquivo de texto
  with open(f'/content/drive/Shareddrives/Finance 3.0/1. Tax/Fiscal Indiretos/FILIAL L4B 0001 SP - ATIVA/DMS/Importação em lote planilha/Arquivos TXT/{filial}.txt', 'w', encoding='utf-8') as file:
      # Iterar sobre todos os DataFrames (df1, df2, df3) dinamicamente
      for df_name in ['Header', 'registros', 'footer']:
          df = locals()[df_name]  # Obtém o DataFrame pelo nome da variável
          df.to_csv(file, index=False, sep='\t')  # Escreve o DataFrame no arquivo
          