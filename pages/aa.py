import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


# Função para carregar e processar os dados do arquivo Excel
def carregar_e_processar_excel(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Pesagem de Animais")
    df_racao = pd.read_excel(uploaded_file, sheet_name="Consumo de Ração")

    # Separar dados de peso por classe
    df_ct = df[df['Classe do Animal'] == 'CT']
    df_dt = df[df['Classe do Animal'] == 'DT']

    # Calculo da média do peso e erro padrão para animais CT
    medias_peso_ct = df_ct.iloc[:, 2:].mean()
    erro_padrao_peso_ct = df_ct.iloc[:, 2:].std() / np.sqrt(df_ct.shape[0])

    # Calculo da média do peso e erro padrão para animais DT
    medias_peso_dt = df_dt.iloc[:, 2:].mean()
    erro_padrao_peso_dt = df_dt.iloc[:, 2:].std() / np.sqrt(df_dt.shape[0])

    # Dicionário com o resultado dos dados processados
    return {
        "medias_peso_ct": medias_peso_ct,
        "erro_padrao_peso_ct": erro_padrao_peso_ct,
        "df_ct": df_ct,
        "medias_peso_dt": medias_peso_dt,
        "erro_padrao_peso_dt": erro_padrao_peso_dt,
        "df_dt": df_dt,
    }

def gerar_df_medias(medias_peso_ct, medias_peso_dt):
    # Criar um DataFrame para as médias de peso de CT e DT
    dias = medias_peso_ct.index  # Assumindo que as colunas de peso são os dias
    df_medias = pd.DataFrame({
        'Dia': dias,
        'Média Peso CT': medias_peso_ct.values,
        'Média Peso DT': medias_peso_dt.values
    })

    # Transformar para formato longo (long format) para facilitar a visualização com Altair
    df_long = pd.melt(df_medias, id_vars=['Dia'], value_vars=['Média Peso CT', 'Média Peso DT'], 
                      var_name='Classe', value_name='Média Peso')
    
    return df_long

def exibir_grafico(medias_peso_ct, medias_peso_dt):
    # Gerar o DataFrame no formato longo para visualização
    df_medias_long = gerar_df_medias(medias_peso_ct, medias_peso_dt)
    
    # Criar gráfico com Altair
    chart = alt.Chart(df_medias_long).mark_line().encode(
        x='Dia:T',  # A variável 'Dia' no eixo x
        y='Média Peso:Q',  # As médias de peso no eixo y
        color='Classe:N',  # Diferenciar as classes CT e DT com cores diferentes
        tooltip=['Dia', 'Classe', 'Média Peso']  # Adicionar tooltip
    ).properties(
        title='Média de Peso por Dia e Classe'
    )

    # Exibir o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)

# Função principal do Streamlit
def main():
    uploaded_file = st.file_uploader("Carregue o arquivo Excel", type="xlsx")
    
    if uploaded_file is not None:
        # Carregar e processar os dados
        dados = carregar_e_processar_excel(uploaded_file)
        
        # Exibir as médias de peso por classe com Altair
        exibir_grafico(dados["medias_peso_ct"], dados["medias_peso_dt"])

if __name__ == "__main__":
    main()
