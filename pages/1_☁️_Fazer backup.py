import streamlit as st
import pandas as pd
from io import StringIO
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io

# Função para autenticar e obter o serviço do Google Drive
def authenticate_google_drive():
    """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    if "google_drive_service" not in st.session_state:
        st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
        st.stop()
        
    return st.session_state["google_drive_service"]

def list_folders(service, folder_id=None, shared=False):
    """Lista apenas as pastas do Google Drive, incluindo pastas compartilhadas"""
    try:
        # Se shared=True, vamos listar arquivos compartilhados com o usuário
        if shared:
            query = "sharedWithMe = true and mimeType = 'application/vnd.google-apps.folder'"
        else:
            # Caso contrário, listamos pastas dentro de uma pasta específica ou todas as pastas não excluídas
            query = f"'{folder_id}' in parents and trashed = false and mimeType = 'application/vnd.google-apps.folder'" if folder_id else "trashed = false and mimeType = 'application/vnd.google-apps.folder'"

        # Realiza a busca usando a API
        results = service.files().list(q=query, pageSize=10, fields="files(id, name)").execute()
        items = results.get('files', [])
        
        # Retorna apenas as pastas
        return items

    except Exception as e:
        st.error(f"Erro ao listar pastas: {e}")
        return []

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

# Função principal que encapsula a lógica de exibição
def main():
    # Sidebar para navegação e autenticação
    with st.sidebar:
        st.header("Índice")
        
        # Authentication for Google Drive
        service = authenticate_google_drive()

        # Seletor para exibir arquivos compartilhados ou não
        show_shared = st.sidebar.checkbox("Exibir arquivos compartilhados", value=False)

        # Listar arquivos e pastas a partir da raiz ou compartilhados
        items = list_folders(service, shared=show_shared)

        # Separar pastas e arquivos
        folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
        files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']

        # Mostrar pastas na sidebar
        selected_folder_name = st.sidebar.selectbox("Escolha uma pasta", [folder['name'] for folder in folders] if folders else ["Sem pastas"])
        selected_folder = next((folder for folder in folders if folder['name'] == selected_folder_name), None)
        
        # Mostrar arquivos na sidebar
        if selected_folder:
            selected_folder_id = selected_folder['id']
            folder_files = list_files(service, folder_id=selected_folder_id, shared=show_shared)
            selected_file_name = st.sidebar.selectbox("Escolha um arquivo dentro da pasta", [file['name'] for file in folder_files])
        else:
            selected_file_name = st.sidebar.selectbox("Escolha um arquivo na raiz", [file['name'] for file in files])

        # Fetch the selected file
        if selected_file_name:
            if selected_folder:
                selected_file = next(file for file in folder_files if file['name'] == selected_file_name)
            else:
                selected_file = next(file for file in files if file['name'] == selected_file_name)

            file_id = selected_file['id']

            # Download the file from Google Drive
            # Código para download do arquivo (caso precise)

    # Upload de novo arquivo
    st.title("Faça upload para o drive")
    uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])

    # Verifique se um arquivo foi carregado antes de tentar fazer upload
    if uploaded_file is not None:
        upload_to_drive(uploaded_file.name, uploaded_file, folder_id=selected_folder_id)
    # Footer with custom background color and fixed to the bottom of the page
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)
    
# Chama a função main() para exibir o conteúdo
if __name__ == "__main__":
    main()
