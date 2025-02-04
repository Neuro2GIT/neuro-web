import streamlit as st
import pandas as pd
from io import StringIO
from googleapiclient.http import MediaIoBaseUpload

# Função para autenticar e obter o serviço do Google Drive
def authenticate_google_drive():
    """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    if "google_drive_service" not in st.session_state:
        st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
        st.stop()
    return st.session_state["google_drive_service"]

# Função para listar arquivos e pastas do Google Drive
def list_files(service):
    """Lista arquivos e pastas do Google Drive"""
    results = service.files().list(
        q="'root' in parents", fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

# Função para upload de arquivo para o Google Drive
def upload_to_drive(file_name, file_data, folder_id=None):
    """Faz o upload do arquivo para o Google Drive"""
    try:
        # Conectar à API do Google Drive
        service = authenticate_google_drive()
        
        # Cria o arquivo no Google Drive
        file_metadata = {'name': file_name}
        
        # Se uma pasta foi escolhida, o arquivo será enviado para essa pasta
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaIoBaseUpload(file_data, mimetype='text/csv')  # Ajuste o mimetype conforme o tipo de arquivo

        # Faz o upload para o Google Drive
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        st.success(f"Arquivo '{file_name}' carregado com sucesso para o Google Drive! ID do arquivo: {file['id']}")
    
    except Exception as e:
        st.error(f"Erro ao fazer upload para o Google Drive: {e}")

# Função principal da página secundária (upload)
def main():
    # Verifica se o usuário está autenticado
    if not st.session_state.get("password_correct", False):
        st.title("Apenas usuários autorizados")
        st.write("Por favor, faça login para acessar o conteúdo.")
        return

    st.title("Nuvem de camundongos")
    st.write("Faça upload para o Google Drive do grupo.")

    # Conecta ao Google Drive
    service = authenticate_google_drive()

    # Lista arquivos e pastas do Google Drive
    items = list_files(service)

    # Separa pastas e arquivos
    folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
    files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']

    # Exibe as pastas no sidebar
    selected_folder_name = st.sidebar.selectbox("Escolha uma pasta", 
                                                [folder['name'] for folder in folders] if folders else ["Sem pastas"])
    
    # Identifica a pasta selecionada
    selected_folder = next((folder for folder in folders if folder['name'] == selected_folder_name), None)
    selected_folder_id = selected_folder['id'] if selected_folder else None

    # Upload de arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "txt", "xlsx"])

    if uploaded_file is not None:
        # Lê o arquivo como bytes
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # Converte para uma IO de string
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # Lê o arquivo como string
        string_data = stringio.read()
        st.write(string_data)

        # Exibe o DataFrame (caso o arquivo seja um CSV)
        try:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

        # Chama a função para fazer upload para o Google Drive
        upload_to_drive(uploaded_file.name, uploaded_file, folder_id=selected_folder_id)

# Chama a função main() para exibir o conteúdo do upload
main()
