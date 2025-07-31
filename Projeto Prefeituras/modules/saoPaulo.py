import pandas as pd

def nfts_SP(template_file, dtint, dtfim, inMunicipal):
    try:
        # Ler o arquivo Excel do template
        df = pd.read_excel(template_file, dtype=str)

        # Verificar se as colunas necessárias existem
        required_columns = ['CNPJ', 'Nota', 'ISS', 'Valor', 'Data documento', '%ISS', 'Cidade']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"As seguintes colunas estão faltando no template: {', '.join(missing_columns)}")

        # Converter colunas para os tipos corretos
        df['CNPJ'] = df['CNPJ'].astype(str)
        df['Nota'] = df['Nota'].astype(str)
        df['ISS'] = pd.to_numeric(df['ISS'], errors='coerce')
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df['vDeducao'] = pd.to_numeric(df['vDeducao'], errors='coerce')
        
        # Tratar a coluna Data documento
        if 'Data documento' in df.columns:
            # Converter para string e limpar espaços
            df['Data documento'] = df['Data documento'].astype(str).str.strip()
            
            # Verificar se a coluna contém espaço para separar data e hora
            if df['Data documento'].str.contains(' ').any():
                df[['Data documento', 'HORA']] = df['Data documento'].str.split(' ', expand=True)
            else:
                # Se não houver hora, criar uma coluna vazia
                df['HORA'] = ''
        
        # Tratar a coluna %ISS
        if '%ISS' in df.columns:
            # Converter para string e limpar espaços
            df['%ISS'] = df['%ISS'].astype(str).str.strip()
            
            # Remover o símbolo % se existir
            df['%ISS'] = df['%ISS'].str.replace('%', '', regex=False)
            
            # Converter para float
            df['%ISS'] = pd.to_numeric(df['%ISS'], errors='coerce')

        # Seleção Filial e filtros.
        df = df.loc[df['Cidade'] != 'SAO PAULO']

        # Criação das colunas conforme regra do valor.
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

        df['ISS Retido'] = df.apply(definir_iss_retido, axis=1)
        df['Valor'] = df['Valor'].apply(lambda x: format(round(x, 2), '.2f'))
        df['vDeducao'] = df['vDeducao'].apply(lambda x: format(round(x, 2), '.2f'))
        df['%ISS'] = (df['%ISS'] * 100).round().astype(int)

        df.drop(['HORA'], axis=1, inplace=True)

        # Converter colunas para string antes de usar operações de string
        df['Data documento'] = df['Data documento'].astype(str).str.replace('-', '')
        df['Data_PGTO'] = df['Data_PGTO'].astype(str).str.replace('-', '')
        df['LC 116'] = df['LC 116'].astype(str).str.replace('.', '')
        df['CEP'] = df['CEP'].astype(str).str.replace('.', '')
        df['CEP'] = df['CEP'].astype(str).str.replace('-', '')
        df['Valor'] = df['Valor'].astype(str).str.replace('.', '')
        df['vDeducao'] = df['vDeducao'].astype(str).str.replace('.', '')

        # Parametrização das colunas utilizando 'PAD' e limitando o tamanho dos campos
        df['Nota'] = df['Nota'].str.slice(0, 12).str.pad(width=12, side='left', fillchar='0')
        df['Serie'] = df['Serie'].str.slice(0, 5).str.pad(width=5, side='left', fillchar=' ')
        df['CNPJ'] = df['CNPJ'].str.slice(0, 14).str.pad(width=14, side='left', fillchar='0')
        df['Valor'] = df['Valor'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
        df['Valor'] = df['Valor'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
        df['vDeducao'] = df['vDeducao'].str.slice(0, 15).str.pad(width=15, side='left', fillchar='0')
        df['SubCódigo'] = df['SubCódigo'].str.slice(0, 5).str.pad(width=5, side='left', fillchar='0')
        df['%ISS'] = df['%ISS'].apply(lambda x: str(x).zfill(4))
        df['Razão Social'] = df['Razão Social'].str.slice(0, 75).str.pad(width=75, side='left', fillchar=' ')
        df['Logradouro'] = df['Logradouro'].str.slice(0, 50).str.pad(width=50, side='right', fillchar=' ')
        df['Número'] = df['Número'].str.slice(0, 10).str.pad(width=10, side='right', fillchar=' ')
        df['Complemento'] = df['Complemento'].str.slice(0, 30).str.pad(width=30, side='right', fillchar=' ')
        df['Bairro'] = df['Bairro'].str.slice(0, 30).str.pad(width=30, side='right', fillchar=' ')
        df['Cidade'] = df['Cidade'].str.slice(0, 50).str.pad(width=50, side='right', fillchar=' ')
        df['E-mail'] = df['E-mail'].str.slice(0, 75).str.pad(width=75, side='left', fillchar=' ')
        df['C_INSS'] = df['C_INSS'].str.slice(0, 12).str.pad(width=12, side='right', fillchar='0')
        df['N_OBRA'] = df['N_OBRA'].str.slice(0, 12).str.pad(width=12, side='right', fillchar='0')
        
        # Garantir que C_RESERVADO sempre tenha 200 espaços, mesmo que seja NaN
        df['C_RESERVADO'] = df['C_RESERVADO'].fillna(' ').str.slice(0, 200).str.pad(width=200, side='right', fillchar=' ')
        df['Descrição do Serviço'] = df['Descrição do Serviço'].str.slice(0, 200).str.pad(width=200, side='right', fillchar=' ')
        df['Data_PGTO'] = df['Data_PGTO'].str.slice(0, 8).str.pad(width=8, side='right', fillchar=' ')
        df['UF'] = df['UF'].str.slice(0, 2).str.pad(width=2, side='right', fillchar=' ')
        df['CEP'] = df['CEP'].str.slice(0, 8).str.pad(width=8, side='right', fillchar='0')

        cabecalho = [f'1002{inMunicipal}{dtint}{dtfim}']
        Header = pd.DataFrame(columns=cabecalho)

        registros = pd.DataFrame()
        registros = pd.concat([
            df['T_Registro'], df['T_Documento'], df['Serie'], df['Nota'],
            df['Data documento'], df['SNFTS'], df['Tributação'], df['Valor'],
            df['vDeducao'], df['SubCódigo'], df['LC 116'], df['%ISS'],
            df['ISS Retido'], df['Ind_CNPJ'], df['CNPJ'], df['CCM'],
            df['Razão Social'], df['Tipo_End'], df['Logradouro'], df['Número'],
            df['Complemento'], df['Bairro'], df['Cidade'], df['UF'], df['CEP'],
            df['E-mail'], df['T_NFTS'], df['Regime_T'], df['Data_PGTO'],
            df['C_INSS'], df['N_OBRA'], df['C_RESERVADO'], df['Descrição do Serviço']
        ], axis=1, ignore_index=True).apply(lambda x: ''.join(str(val) for val in x), axis=1)

        df = df.astype({'Valor': float})
        df = df.astype({'vDeducao': float})
        
        num_linhas = len(registros)
        num_linhas_formatted = f'{num_linhas:0>6}'
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

        # Criar uma string para armazenar o conteúdo
        content = ''
        
        # Adicionar o header
        content += Header.columns[0] + '\n'
        
        # Adicionar os registros
        for registro in registros:
            content += registro + '\n'
        
        # Adicionar o footer
        content += footer.columns[0] + '\n'
        
        return content
    
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        raise