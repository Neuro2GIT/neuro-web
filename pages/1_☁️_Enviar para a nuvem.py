import streamlit as st
import pandas as pd
from io import StringIO
from googleapiclient.http import MediaIoBaseUpload

# Se o usuário não estiver autenticado, pede o login
if not st.session_state.get("password_correct", False):
    st.title("Apenas usuários autorizados")
    st.write("Por favor, faça login para acessar o conteúdo.")

else:
    # Página protegida, acessada após login bem-sucedido
    def authenticate_google_drive():
        """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
        if "google_drive_service" not in st.session_state:
            st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
            st.stop()
        return st.session_state["google_drive_service"]

    def upload_to_drive(file_name, file_data):
        """Faz o upload do arquivo para o Google Drive"""
        try:
            # Conectar à API do Google Drive
            service = authenticate_google_drive()
            
            # Cria o arquivo no Google Drive
            file_metadata = {'name': file_name}
            media = MediaIoBaseUpload(file_data, mimetype='text/csv')  # Ajuste o mimetype conforme o tipo de arquivo

            # Faz o upload para a pasta raiz do Google Drive
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            st.success(f"Arquivo '{file_name}' carregado com sucesso para o Google Drive! ID do arquivo: {file['id']}")
        
        except Exception as e:
            st.error(f"Erro ao fazer upload para o Google Drive: {e}")

    def main():
        st.title("Nuvem de camundongos")
        st.write("Faça upload para o Google Drive do grupo.")

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

            # Chama a função de upload para o Google Drive
            upload_to_drive(uploaded_file.name, uploaded_file)

    # Chama a função main() para exibir o conteúdo do upload
    main()
