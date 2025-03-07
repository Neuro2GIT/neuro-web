import pandas as pd
import streamlit as st
from io import BytesIO

# Função para criar a planilha Excel com os dados
def criar_planilha():
    # Dados para a Tabela de Peso dos Animais (sem valores fictícios, apenas estrutura com 16 dias)
    animais = list(range(1, 11))  # ID dos animais 1 a 10
    classes = ['CT', 'CT', 'CT', 'CT', 'CT', 'DT', 'DT', 'DT', 'DT', 'DT']  # Classes (CT e DT)

    # Inicializando as colunas de pesos (dias de 1 a 16)
    colunas_peso = ['ID do Animal', 'Classe'] + [f'Peso no Dia {i}' for i in range(1, 17)]

    # Tabela de peso dos animais
    dados_peso = {
        'ID do Animal': animais,
        'Classe': classes
    }

    for dia in range(1, 17):
        dados_peso[f'Peso no Dia {dia}'] = [None] * 10  # Nenhum valor de peso, somente a estrutura

    df_peso = pd.DataFrame(dados_peso, columns=colunas_peso)

    # Dados para a Tabela de Consumo de Ração (somente estrutura)
    caixas = [1, 2]  # ID das caixas
    classes_caixas = ['CT', 'DT']  # Classes das caixas

    # Inicializando as colunas de consumo de ração (dias de 1 a 16)
    colunas_racao = ['ID da Caixa', 'Classe da Caixa'] + [f'Consumo no Dia {i}' for i in range(1, 17)]

    # Tabela de consumo de ração
    dados_racao = {
        'ID da Caixa': caixas,
        'Classe da Caixa': classes_caixas
    }

    for dia in range(1, 17):
        dados_racao[f'Consumo no Dia {dia}'] = [None] * 2  # Nenhum valor de consumo, somente a estrutura

    df_racao = pd.DataFrame(dados_racao, columns=colunas_racao)

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
