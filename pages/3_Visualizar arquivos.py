import streamlit as st
import pandas as pd
from io import StringIO
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from docx import Document
import io


# Função para autenticar e obter o serviço do Google Drive
def authenticate_google_drive():
    """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    if "google_drive_service" not in st.session_state:
        st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
        st.stop()
    return st.session_state["google_drive_service"]

def list_files(service, folder_id=None):
    """Lista arquivos e pastas do Google Drive"""
    try:
        query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
        results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])
        return items

        # Verificando a estrutura da resposta
        if isinstance(results, dict):
            return results.get('files', [])
        else:
            st.error("A resposta da API não está no formato esperado. A resposta foi: " + str(results))
            return []
    
    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
        return []

# Função para baixar o arquivo do Google Drive
def download_file_from_drive(file_id, service):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO('modo_de_preparo.docx', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    return 'modo_de_preparo.docx'

# Função para ler o conteúdo do arquivo .docx
def read_docx_file(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Função principal
def main():
    st.title("🐁Listagem dos arquivos disponiveis no drive")
    with st.sidebar:
        st.header("Índice")
        
        # Autenticação para o Google Drive
        service = authenticate_google_drive()

        # Seletor para exibir arquivos compartilhados ou não
        show_shared = st.sidebar.checkbox("Exibir arquivos compartilhados", value=False)

        # Listar arquivos e pastas a partir da raiz ou compartilhados
        items = list_files(service, shared=show_shared)

        # Separar pastas e arquivos
        folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
        files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']

        # Mostrar pastas na sidebar (Se houver pastas)
        if folders:
            selected_folder_name = st.sidebar.selectbox("Escolha uma pasta", [folder['name'] for folder in folders])
            selected_folder = next((folder for folder in folders if folder['name'] == selected_folder_name), None)

            # Se uma pasta for selecionada, listar arquivos dentro dela
            if selected_folder:
                selected_folder_id = selected_folder['id']
                folder_files = list_files(service, folder_id=selected_folder_id, shared=show_shared)
                selected_file_name = st.sidebar.selectbox("Escolha um arquivo dentro da pasta", [file['name'] for file in folder_files])
            else:
                selected_file_name = None
        else:
            selected_folder = None
            selected_file_name = st.sidebar.selectbox("Escolha um arquivo na raiz", [file['name'] for file in files])

        # Fetch the selected file
        if selected_file_name:
            if selected_folder:
                selected_file = next(file for file in folder_files if file['name'] == selected_file_name)
            else:
                selected_file = next(file for file in files if file['name'] == selected_file_name)

            file_id = selected_file['id']
            st.sidebar.write(f"Você selecionou o arquivo: {selected_file['name']}")
            # Aqui você pode implementar a lógica de exibição do conteúdo do arquivo, como no código anterior.
            # Por exemplo, exibir o conteúdo do arquivo .docx ou outro tipo de arquivo conforme necessário.

# Footer with custom background color and fixed to the bottom of the page
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)

# Chama a função main() para exibir o conteúdo
main()
