import streamlit as st
import pandas as pd
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io

# Função para autenticar e obter o serviço do Google Drive
def authenticate_google_drive():
    """Verifica se já existe um serviço de autenticação com o Google Drive no session_state"""
    if "google_drive_service" not in st.session_state:
        st.error("Erro: Usuário não autenticado com o Google Drive. Por favor, faça login na página inicial.")
        st.stop()
        
    return st.session_state["google_drive_service"]

# Função para listar arquivos no Google Drive
def list_files(service, folder_id=None, include_shared=False):
    """Lista arquivos e pastas do Google Drive, incluindo arquivos compartilhados"""
    try:
        query = "trashed = false"
        
        # Se houver um folder_id, filtra por essa pasta
        if folder_id:
            query += f" and '{folder_id}' in parents"

        # Se include_shared for True, buscamos também pastas compartilhadas como 'Neuroscience'
        if include_shared:
            query += " or sharedWithMe = true"

        # Realiza a busca usando a API
        results = service.files().list(q=query, pageSize=50, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])
        return items

    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
        return []

from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload

def upload_to_drive(file_name, file_data, folder_id=None):
    """Faz o upload de qualquer tipo de arquivo para o Google Drive sem salvar localmente"""
    try:
        # Conectar à API do Google Drive
        service = authenticate_google_drive()
        
        # Determinar o tipo MIME do arquivo baseado na extensão
        if file_name.endswith('.csv'):
            mime_type = 'text/csv'
        elif file_name.endswith('.xlsx'):
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_name.endswith('.txt'):
            mime_type = 'text/plain'
        else:
            mime_type = 'application/octet-stream'  # Tipo genérico para outros arquivos
        
        # Cria o arquivo no Google Drive
        file_metadata = {'name': file_name}
        
        # Se uma pasta foi escolhida, o arquivo será enviado para essa pasta
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Lê o arquivo carregado diretamente como um fluxo de bytes
        file_data_bytes = BytesIO(file_data.read())
        
        # Cria o MediaIoBaseUpload com os dados binários e o tipo MIME correto
        media = MediaIoBaseUpload(file_data_bytes, mimetype=mime_type)
        
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
        
        # Autenticação para o Google Drive
        service = authenticate_google_drive()

        # Listar arquivos e pastas, incluindo compartilhados, por padrão
        items = list_files(service, include_shared=True)

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
                folder_files = list_files(service, folder_id=selected_folder_id, include_shared=True)
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

    # Upload de novo arquivo
    st.title("Faça upload para o drive")
    uploaded_file = st.file_uploader("Escolha um arquivo para enviar", type=["csv", "txt", "xlsx"])

    # Verifique se um arquivo foi carregado antes de tentar fazer upload
    if uploaded_file is not None:
        upload_to_drive(uploaded_file.name, uploaded_file, folder_id=selected_folder_id)
    
    # Footer com custom background color e fixado no fundo da página
    st.markdown("""<footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            LABIBIO 2025 - Biotério & Neuroscience
        </footer>""", unsafe_allow_html=True)
    
# Chama a função main() para exibir o conteúdo
if __name__ == "__main__":
    main()
