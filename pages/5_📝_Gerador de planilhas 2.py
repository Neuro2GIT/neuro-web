import pandas as pd
import streamlit as st
from io import BytesIO

def criar_planilha(num_animais_ct, num_animais_dt):
    # Criando os dados para a planilha "Animais CT"
    animais_ct = list(range(1, num_animais_ct + 1))  # IDs dos animais CT
    dados_ct = {
        "ID do animal": animais_ct,
        "Classe do animal": ["CT"] * num_animais_ct,
        "Tempo no objeto novo": [None] * num_animais_ct,
        "Tempo no objeto familiar": [None] * num_animais_ct
    }
    df_ct = pd.DataFrame(dados_ct)

    # Criando os dados para a planilha "Animais DT"
    animais_dt = list(range(1, num_animais_dt + 1))  # IDs dos animais DT
    dados_dt = {
        "ID do animal": animais_dt,
        "Classe do animal": ["DT"] * num_animais_dt,
        "Tempo no objeto novo": [None] * num_animais_dt,
        "Tempo no objeto familiar": [None] * num_animais_dt
    }
    df_dt = pd.DataFrame(dados_dt)

    # Criando o arquivo Excel em memória
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df_ct.to_excel(writer, sheet_name='Animais CT', index=False)
            df_dt.to_excel(writer, sheet_name='Animais DT', index=False)

            # Obter o objeto do workbook e worksheets
            workbook = writer.book
            worksheet_ct = writer.sheets['Animais CT']
            worksheet_dt = writer.sheets['Animais DT']

            # Estilo de alinhamento centralizado
            center_alignment = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

            # Ajustar a largura das colunas da planilha "Animais CT"
            for i, col in enumerate(df_ct.columns):
                max_len = df_ct[col].astype(str).map(len).max()
                max_len = max(max_len, len(col))  # Considera o tamanho do cabeçalho também
                worksheet_ct.set_column(i, i, max_len + 2, center_alignment)

            # Ajustar a largura das colunas da planilha "Animais DT"
            for i, col in enumerate(df_dt.columns):
                max_len = df_dt[col].astype(str).map(len).max()
                max_len = max(max_len, len(col))  # Considera o tamanho do cabeçalho também
                worksheet_dt.set_column(i, i, max_len + 2, center_alignment)
        
        b.seek(0)
        return b.read()

# Configuração do Streamlit
st.title("Planilha para o TRO")

st.markdown("---")

with st.expander("Como funciona?"):
    st.write("O gerador criará um arquivo excel contendo duas planilhas, uma para inserir os tempos de exploração para os animais CT e a outra os animais DT.")

with st.container(border=True):
    num_animais_ct = st.number_input("Número de animais na classe CT:", min_value=1, value=5, step=1)
    num_animais_dt = st.number_input("Número de animais na classe DT:", min_value=1, value=5, step=1)

# Botão para gerar o arquivo Excel e permitir o download
if st.button("Gerar Planilha"):
    excel_file = criar_planilha(num_animais_ct, num_animais_dt)
    
    st.download_button(
        label="Baixar Planilha Excel",
        data=excel_file,
        file_name="experimento_tro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
