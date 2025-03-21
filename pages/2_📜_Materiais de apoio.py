import streamlit as st
import pandas as pd
from io import StringIO
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from docx import Document
import io

st.set_page_config(
    page_title="Métodos e técnicas",
    page_icon="🐭",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={})
st.set_option('client.showErrorDetails', True)

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

def download_file_from_drive(file_id, service):
    try:
        # Tenta obter o arquivo como mídia binária
        request = service.files().get_media(fileId=file_id)
        
        # Caso seja um arquivo do Google Docs, exporta para o formato adequado
        file = service.files().get(fileId=file_id).execute()
        mime_type = file['mimeType']
        
        # Se for um arquivo do Google Docs, exporta para .docx
        if mime_type == 'application/vnd.google-apps.document':
            request = service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        
        # Baixa o arquivo
        fh = io.FileIO('modo_de_preparo.docx', 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        return 'modo_de_preparo.docx'
    except Exception as e:
        st.error(f"Erro ao baixar o arquivo: {e}")
        return None

# Função para ler o conteúdo do arquivo .docx
def read_docx_file(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

import streamlit as st

# Função principal
def main():
    # Sidebar para navegação e autenticação
    with st.sidebar:
        # Opção de seleção da técnica
        tecnica_selecionada = st.radio(
            "Índice",
            ("Preparo de ração", "Dosagem de proteínas", "Dosagem de cálcio")
        )

    # Criar um container para a técnica selecionada com três expanders
    if tecnica_selecionada == "Preparo de ração":
        
        st.title("Preparo de ração")
        url = "https://repositorio.ufmg.br/bitstream/1843/33624/1/Tese%20vers%c3%a3o%20FINAL.pdf"
        st.markdown("Fonte f"[dissertação de doutorado]({url})")

        st.markdown("---")
        
        with st.container(border=True):
            
            # Expander para "Ingredientes ração"
            with st.expander("Ingredientes"):
                st.write("Inserir a figura de ingredientes da ração CT")

            # Expander para "Ingredientes ração DT"
            with st.expander("Ingredientes - ração DT"):
                st.write("Inserir a figura de ingredientes da ração DT")

            # Expander para "Modo de preparo"
            with st.expander("Modo de preparo"):
                st.write("""
                1. **Preparação da massa base:**
                Misture bem o amido, o polvilho e a caseína em um recipiente.  
                Acrescente a água e mexa até dissolver completamente os ingredientes secos.

                2. **Cozimento da massa:**
                Unte a panela com uma parte do óleo.  
                Despeje a mistura e mexa constantemente.  
                Conforme a massa começar a ganhar firmeza, mexa com mais vigor.  
                Continue o processo até que ela comece a desgrudar completamente da panela e adquirir uma coloração levemente dourada. Reserve até atingir uma temperatura morna ao toque.

                3. **Adição dos complementos:**
                Assim que a massa atingir a temperatura adequada, acrescente os sais minerais, as vitaminas, a celulose e a sacarose.  
                Acrescente mais uma parte do óleo para ajudar na incorporação e misture.

                4. **Modelagem e finalização:**
                Faça a sova na massa até homogeneizar bem a mistura.  
                Modele a massa, em partes, em forma de bastão e corte em pequenos pellets, semelhantes à ração comercial.
                """)

    elif tecnica_selecionada == "Dosagem de proteínas":
        st.write("Conteúdo sobre dosagem de proteínas")

    elif tecnica_selecionada == "Dosagem de cálcio":
        st.write("Conteúdo sobre dosagem de cálcio")

# Chamada da função principal
if __name__ == "__main__":
    main()
      
             # Aqui você pode colocar o código para baixar e exibir o arquivo .docx no placeholder
            #placeholder = st.empty()  # Criando um Placeholder

            # Acessando o file_id de forma segura a partir do secrets.toml
            #file_id = st.secrets["google_drive"]["file_id_preparo_racao_ct"]  # Obtendo o file_id da configuração

            # Serviço da API do Google Drive (já autenticado)
            #service = authenticate_google_drive()  # Obtém o serviço autenticado

            # Baixar o arquivo e ler o conteúdo
            #file_path = download_file_from_drive(file_id, service)
            #if file_path:
                #docx_content = read_docx_file(file_path)
                #with placeholder:
                    #st.markdown(docx_content)

    # Footer com estilo customizado
    #st.markdown("""
        #<footer style='text-align: center; position: fixed; left: 0; background-color: #2C3E50; color: white; padding: 10px; bottom: 0; width: 100%; '>
            #LABIBIO 2025 - Biotério & Neuroscience
        #</footer>
    #""", unsafe_allow_html=True)

# Chama a função main() para exibir o conteúdo
#main()
