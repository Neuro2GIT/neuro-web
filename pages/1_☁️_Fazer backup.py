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

def list_files(service, folder_id=None, shared=False):
    """Lista arquivos e pastas do Google Drive, incluindo arquivos compartilhados"""
    try:
        # Se shared=True, vamos listar arquivos compartilhados com o usuário
        if shared:
            query = "sharedWithMe = true"
        else:
            # Caso contrário, listamos arquivos dentro de uma pasta específica ou todos os arquivos não excluídos
            query = f"'{folder_id}' in parents and trashed = false" if folder_id else "trashed = false"

        # Realiza a busca usando a API
        results = service.files().list(q=query, pageSize=10, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])
        return items

    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
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

    # Upload de novo arquivo
    st.title("Faça upload para o drive")
    uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])

    # Verifique se um arquivo foi carregado antes de tentar fazer upload
    #if uploaded_file is not None:
        #upload_to_drive(uploaded_file.name, uploaded_file, folder_id=selected_folder_id)
    #else:
        #st.warning("Nenhum arquivo carregado.")

    # Rodapé estilizado para fixar na parte inferior sem sobrepor o conteúdo
    st.markdown("""
        <style>
            body {
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                margin: 0;
            }
            main {
                flex: 1;
            }
            footer {
                text-align: center;
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                width: 100%;
                bottom: 0;
                left: 0;
                position: fixed;
            }
        </style>
        <footer>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>
    """, unsafe_allow_html=True)

# Chama a função main() para exibir o conteúdo
main()
