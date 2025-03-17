import pandas as pd
import streamlit as st
from io import BytesIO

# Função para criar a planilha Excel com os dados dos animais
def criar_planilha(num_animais):
    
    # Gerar IDs para os animais
    ids = list(range(1, num_animais + 1))

    # Criando a tabela de dados (sem os valores preenchidos, exceto o ID)
    dados = {
        'ID do Animal': ids,
        'Classe do Animal': [''] * num_animais,  # A coluna de classe está vazia para ser preenchida depois
        'Tempo no Objeto Novo (segundos)': [None] * num_animais,  # Coluna de tempo vazia
        'Tempo no Objeto Familiar (segundos)': [None] * num_animais  # Coluna de tempo vazia
    }
    
    df = pd.DataFrame(dados)

    # Criar um arquivo Excel em memória
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            # Escrever a tabela de dados no Excel
            df.to_excel(writer, sheet_name='Dados dos Animais', index=False)

            # Obter o objeto do workbook e worksheet
            workbook = writer.book
            worksheet = writer.sheets['Dados dos Animais']

            # Estilo de alinhamento centralizado
            center_alignment = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

            # Ajustar a largura das colunas da planilha
            for i, col in enumerate(df.columns):
                max_len = df[col].apply(lambda x: len(str(x)) if x is not None else 0).max()
                max_len = max(max_len, len(col))  # Considera o tamanho do cabeçalho também
                worksheet.set_column(i, i, max_len + 2, center_alignment)  # +2 para garantir um pouco de espaço extra

        b.seek(0)
        return b.read()

# Configuração do Streamlit
st.title("Gerador de Planilha de Dados dos Animais")

with st.container(border=True):
    # Widget para o número de animais
    num_animais = st.number_input("Número de animais:", min_value=1, value=5, step=1)

# Botão para gerar o arquivo Excel e permitir o download
if st.button("Gerar Planilha"):
    excel_file = criar_planilha(num_animais)
    
    st.download_button(
        label="Baixar Planilha Excel",
        data=excel_file,
        file_name="dados_animais.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
