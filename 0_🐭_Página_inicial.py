import streamlit as st
import requests
import pytz
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Grupo Neuroscience",
    page_icon="🐭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para obter informações do DOI
def get_doi_info(doi):
    base_url = "https://api.crossref.org/works/"
    url = base_url + doi
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        title = data['message']['title'][0]
        
        authors = []
        for author in data['message'].get('author', []):
            given_name = author.get('given', '')
            family_name = author.get('family', '')
            if given_name or family_name:
                authors.append(f"{given_name} {family_name}".strip())
        authors = ", ".join(authors)
        
        published_year = data['message']['published']['date-parts'][0][0]
        url = data['message'].get('URL', '')
        pdf_link = data['message'].get('link', [{}])[0].get('URL', '')
        
        return title, authors, published_year, url, pdf_link
    else:
        return None, None, None, None, None

# Definição de categorias e artigos
themes = {
    "Publicações": ["10.22289/2446-922X.V10N1A23"],
    "Introdução ao modelo DT": [
        "10.1080/09168451.2016.1224639",
        "10.54038/ms.v1i1.2",
        "10.54038/ms.v2i2.20",
        "10.30574/gscarr.2023.15.3.0167"
    ],
    "Artigos de métodos - Biureto / Bradford e BCA": [
        "10.1016/0003-2697(76)90527-3",
        "10.1590/S0100-40421998000600020",
        "10.1016/0003-2697(85)90442-7",
        "10.1016/S0021-9258(18)57021-6"
    ]
}

# Estilização com CSS
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .main-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            color: #FF4081;
        }
        .article-card {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(255, 64, 129, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown('<p class="main-title">🧠 Neuroscience Interest Group</p>', unsafe_allow_html=True)

# Exibição dos artigos
for theme, dois in themes.items():
    st.subheader(theme)
    col1, col2 = st.columns(2)
    
    for i, doi in enumerate(dois):
        title, authors, published_year, url, pdf_link = get_doi_info(doi)
        
        if title:
            with (col1 if i % 2 == 0 else col2):
                with st.container():
                    st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
                    st.markdown(f"**{title}**")
                    st.markdown(f"*Autores:* {authors}")
                    st.markdown(f"*Publicado em:* {published_year}")
                    st.markdown(f"[Leia o artigo completo]({url})")
                    
                    if pdf_link:
                        st.markdown(f"[Baixar PDF]({pdf_link})")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Não foi possível recuperar informações para o DOI: {doi}")

if __name__ == "__main__":
    main()
