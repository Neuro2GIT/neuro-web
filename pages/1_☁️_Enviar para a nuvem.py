import streamlit as st
import pandas as pd
from io import StringIO

# Se o usuário não estiver autenticado, pede o login
if not st.session_state.get("password_correct", False):
    st.title("Apenas usuários autorizados")
    st.write("Por favor, faça login para acessar o conteúdo.")

else:
    # Página protegida, acessada após login bem-sucedido

    def main():
        st.title("Nuvem de camundongos")
        st.write("Faça upload para o google drive do grupo.")

        uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "txt", "xlsx"])

        if uploaded_file is not None:
            # Para ler o arquivo como bytes:
            bytes_data = uploaded_file.getvalue()
            st.write(bytes_data)

            # Para converter para uma IO de string:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.write(stringio)

            # Para ler o arquivo como string:
            string_data = stringio.read()
            st.write(string_data)

            # Pode ser usado onde for aceito um objeto "file-like":
            try:
                dataframe = pd.read_csv(uploaded_file)
                st.write(dataframe)
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

    # Chama a função main() para exibir o conteúdo do upload
    main()
