def separar_grupo_subgrupo(df, grupo, subgrupo):
    """
    Função para filtrar o DataFrame com base no grupo e subgrupo.
    
    :param df: DataFrame original
    :param grupo: Valor do grupo ('M' ou 'F')
    :param subgrupo: Valor do subgrupo ('CT' ou 'DT')
    :return: DataFrame filtrado
    """
    return df[(df['Classe do animal'] == subgrupo) & (df['Grupo'] == grupo)]

def calcular_indices(df):
    # Usar a função para separar os dados por grupo e subgrupo
    df_m_ct = separar_grupo_subgrupo(df, 'M', 'CT')  # Machos - CT
    df_m_dt = separar_grupo_subgrupo(df, 'M', 'DT')  # Machos - DT
    df_f_ct = separar_grupo_subgrupo(df, 'F', 'CT')  # Fêmeas - CT
    df_f_dt = separar_grupo_subgrupo(df, 'F', 'DT')  # Fêmeas - DT
    
    # Calcular discriminação absoluta para os subgrupos M-CT, M-DT, F-CT, F-DT
    df_m_ct["Discriminação absoluta"] = df_m_ct["Tempo no objeto novo"] - df_m_ct["Tempo no objeto familiar"]
    df_m_dt["Discriminação absoluta"] = df_m_dt["Tempo no objeto novo"] - df_m_dt["Tempo no objeto familiar"]
    df_f_ct["Discriminação absoluta"] = df_f_ct["Tempo no objeto novo"] - df_f_ct["Tempo no objeto familiar"]
    df_f_dt["Discriminação absoluta"] = df_f_dt["Tempo no objeto novo"] - df_f_dt["Tempo no objeto familiar"]
    
    # Calcular Índice de Discriminação para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de discriminação"] = df_m_ct["Discriminação absoluta"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])
    df_m_dt["Índice de discriminação"] = df_m_dt["Discriminação absoluta"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])
    df_f_ct["Índice de discriminação"] = df_f_ct["Discriminação absoluta"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])
    df_f_dt["Índice de discriminação"] = df_f_dt["Discriminação absoluta"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])
    
    # Calcular Índice de Preferência para M-CT, M-DT, F-CT, F-DT
    df_m_ct["Índice de preferência"] = (df_m_ct["Tempo no objeto novo"] / (df_m_ct["Tempo no objeto novo"] + df_m_ct["Tempo no objeto familiar"])) * 100
    df_m_dt["Índice de preferência"] = (df_m_dt["Tempo no objeto novo"] / (df_m_dt["Tempo no objeto novo"] + df_m_dt["Tempo no objeto familiar"])) * 100
    df_f_ct["Índice de preferência"] = (df_f_ct["Tempo no objeto novo"] / (df_f_ct["Tempo no objeto novo"] + df_f_ct["Tempo no objeto familiar"])) * 100
    df_f_dt["Índice de preferência"] = (df_f_dt["Tempo no objeto novo"] / (df_f_dt["Tempo no objeto novo"] + df_f_dt["Tempo no objeto familiar"])) * 100

    # Unir os dataframes de 'M-CT', 'M-DT', 'F-CT' e 'F-DT' novamente
    df = pd.concat([df_m_ct, df_m_dt, df_f_ct, df_f_dt])
    
    # Calcular a média dos índices de discriminação
    df["Média dos índices de discriminação"] = df["Índice de discriminação"].mean()
    
    return df

# Streamlit: Interface do usuário
st.title("Cálculo de Índices de Discriminação e Preferência")

# Carregar um arquivo CSV de exemplo ou coletar os dados de outra maneira
uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])

if uploaded_file is not None:
    # Carregar os dados do arquivo CSV
    df = pd.read_csv(uploaded_file)
    
    # Verificar se as colunas necessárias existem
    if 'Classe do animal' in df.columns and 'Grupo' in df.columns and 'Tempo no objeto novo' in df.columns and 'Tempo no objeto familiar' in df.columns:
        
        # Calcular os índices
        df_calculado = calcular_indices(df)
        
        # Exibir a tabela de resultados
        st.subheader("Resultados")
        st.dataframe(df_calculado)  # Exibe o DataFrame resultante
        
        # Exibir algumas métricas (opcional)
        st.subheader("Média dos Índices de Discriminação")
        st.write(f"Média dos Índices de Discriminação: {df_calculado['Média dos índices de discriminação'].iloc[0]:.2f}")
        
        # Adicionar gráficos para visualização, por exemplo:
        st.subheader("Gráfico de Índice de Preferência")
        st.line_chart(df_calculado[['Índice de preferência']])
        
        st.subheader("Gráfico de Discriminação Absoluta")
        st.line_chart(df_calculado[['Discriminação absoluta']])

    else:
        st.error("O arquivo CSV não contém as colunas necessárias.")
