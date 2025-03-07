import pandas as pd
import streamlit as st
from io import BytesIO

# Função para criar a planilha Excel com os dados
def criar_planilha():
    # Dados para a Tabela de Peso dos Animais
    dados_peso = {
        'ID do Animal': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Classe': ['CT', 'CT', 'CT', 'CT', 'CT', 'DT', 'DT', 'DT', 'DT', 'DT'],
        'Peso no Dia 1': [2.5, 2.7, 2.6, 2.8, 2.9, 3.0, 3.2, 3.1, 3.4, 3.3],
        'Peso no Dia 2': [2.6, 2.8, 2.7, 2.9, 3.0, 3.1, 3.3, 3.2, 3.5, 3.4],
        'Peso no Dia 3': [2.7, 2.9, 2.8, 3.0, 3.1, 3.2, 3.4, 3.3, 3.6, 3.5],
        # Adicione os dados dos outros dias até o Dia 16
        'Peso no Dia 16': [3.0, 3.2, 3.1, 3.3, 3.4, 3.5, 3.7, 3.6, 3.9, 3.8]
    }

    # Dados para a Tabela de Consumo de Ração
    dados_racao = {
        'ID da Caixa': [1, 2],
        'Classe da Caixa': ['CT', 'DT'],
        'Consumo no Dia 1': [1.2, 1.5],
        'Consumo no Dia 2': [1.25, 1.6],
        'Consumo no Dia 3': [1.3, 1.7],
        # Adicione os dados dos outros dias até o Dia 16
        'Consumo no Dia 16': [1.5, 1.9]
    }

    # Criar DataFrames com os dados
    df_peso = pd.DataFrame(dados_peso)
    df_racao = pd.DataFrame(dados_racao)

    # Criar um arquivo Excel em memória
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df_peso.to_excel(writer, sheet_name='Pesagem de Animais', index=False)
            df_racao.to_excel(writer, sheet_name='Consumo de Ração', index=False)
        b.seek(0)
        return b.read()

# Configuração do Streamlit
st.title("Gerar Planilha de Dados de Experimento")

# Botão para gerar o arquivo Excel e permitir o download
excel_file = criar_planilha()

st.download_button(
    label="Baixar Planilha Excel",
    data=excel_file,
    file_name="dados_experimento.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
