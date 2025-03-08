import pandas as pd
import streamlit as st
from io import BytesIO

# Função para criar a planilha Excel com os dados
def criar_planilha(num_animais_ct, num_animais_dt, num_dias):
    # Dados para a Tabela de Peso dos Animais
    animais_ct = list(range(1, num_animais_ct + 1))  # ID dos animais da classe CT
    animais_dt = list(range(num_animais_ct + 1, num_animais_ct + num_animais_dt + 1))  # ID dos animais da classe DT
    animais = animais_ct + animais_dt  # Unir ambos os grupos de animais
    classes = ['CT'] * num_animais_ct + ['DT'] * num_animais_dt  # Classes (CT e DT)

    # Inicializando as colunas de pesos (dias de 1 até num_dias)
    colunas_peso = ['ID do Animal', 'Classe do Animal'] + [f'Peso no Dia {i} (g)' for i in range(1, num_dias + 1)]

    # Tabela de peso dos animais
    dados_peso = {
        'ID do Animal': animais,
        'Classe do Animal': classes
    }

    # Inicializando o peso de cada dia (todos começam como None)
    for dia in range(1, num_dias + 1):
        dados_peso[f'Peso no Dia {dia} (g)'] = [None] * (num_animais_ct + num_animais_dt)  # Nenhum valor de peso, somente a estrutura

    df_peso = pd.DataFrame(dados_peso, columns=colunas_peso)

    # Dados para a Tabela de Consumo de Ração
    num_caixas = 2  # Apenas duas caixas (CT e DT)
    caixas = [1, 2]  # ID das caixas
    classes_caixas = ['CT', 'DT']  # Classes das caixas

    # Inicializando as colunas de consumo de ração (dias de 1 até num_dias)
    colunas_racao = ['ID da Caixa', 'Classe da Caixa'] + [f'Consumo no Dia {i} (g)' for i in range(1, num_dias + 1)]

    # Tabela de consumo de ração
    dados_racao = {
        'ID da Caixa': caixas,
        'Classe da Caixa': classes_caixas
    }

    # Inicializando o consumo de cada dia (todos começam como None)
    for dia in range(1, num_dias + 1):
        dados_racao[f'Consumo no Dia {dia} (g)'] = [None] * num_caixas  # Nenhum valor de consumo, somente a estrutura

    df_racao = pd.DataFrame(dados_racao, columns=colunas_racao)

    # Criar um arquivo Excel em memória
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            # Escrever as tabelas no Excel
            df_peso.to_excel(writer, sheet_name='Pesagem de Animais', index=False)
            df_racao.to_excel(writer, sheet_name='Consumo de Ração', index=False)

            # Obter o objeto do workbook e worksheet
            workbook  = writer.book
            worksheet_peso = writer.sheets['Pesagem de Animais']
            worksheet_racao = writer.sheets['Consumo de Ração']

            # Estilo de alinhamento centralizado
            center_alignment = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

            # Ajustar a largura das colunas da planilha de pesagem
            for i, col in enumerate(df_peso.columns):
                max_len = df_peso[col].apply(lambda x: len(str(x)) if x is not None else 0).max()
                max_len = max(max_len, len(col))  # Considera o tamanho do cabeçalho também
                worksheet_peso.set_column(i, i, max_len + 2, center_alignment)  # +2 para garantir um pouco de espaço extra

            # Ajustar a largura das colunas da planilha de consumo de ração
            for i, col in enumerate(df_racao.columns):
                max_len = df_racao[col].apply(lambda x: len(str(x)) if x is not None else 0).max()
                max_len = max(max_len, len(col))  # Considera o tamanho do cabeçalho também
                worksheet_racao.set_column(i, i, max_len + 2, center_alignment)  # +2 para garantir um pouco de espaço extra

        b.seek(0)
        return b.read()

# Configuração do Streamlit
st.title("Peso dos animais e consumo de ração")

# Widgets para o número de animais e dias do experimento
num_animais_ct = st.number_input("Número de animais na classe CT:", min_value=1, value=5, step=1)
num_animais_dt = st.number_input("Número de animais na classe DT:", min_value=1, value=5, step=1)
num_dias = st.number_input("Número de dias do experimento:", min_value=1, value=16, step=1)

# Botão para gerar o arquivo Excel e permitir o download
if st.button("Gerar Planilha"):
    excel_file = criar_planilha(num_animais_ct, num_animais_dt, num_dias)
    
    st.download_button(
        label="Baixar Planilha Excel",
        data=excel_file,
        file_name="dados_experimento.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
