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

# Footer with custom background color and fixed to the bottom of the page
    st.markdown("""
        <footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)

# Chama a função main() para exibir o conteúdo
main()
