import streamlit as st
import requests

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
        title = data['message'].get('title', [''])[0]
        authors = []
        for author in data['message'].get('author', []):
            given_name = author.get('given', '')
            family_name = author.get('family', '')
            if given_name or family_name:
                authors.append(f"{given_name} {family_name}".strip())
        authors = ", ".join(authors)
        published_year = data['message'].get('published', {}).get('date-parts', [[None]])[0][0]
        url = data['message'].get('URL', '')
        pdf_link = next((link.get('URL', '') for link in data['message'].get('link', []) if link.get('content-type') == 'application/pdf'), '')
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
            background-color: #f5f5f5;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .article-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .article-title {
            font-size: 1.5em;
            color: #2980b9;
            margin-bottom: 10px;
        }
        .article-authors, .article-year {
            font-size: 1em;
            color: #7f8c8d;
        }
        .article-link {
            font-size: 1em;
            color: #27ae60;
            text-decoration: none;
        }
        .article-link:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown('<div class="main-title">🧠 Neuroscience Interest Group</div>', unsafe_allow_html=True)

# Exibição dos artigos
for theme, dois in themes.items():
    st.subheader(theme)
    for doi in dois:
        title, authors, published_year, url, pdf_link = get_doi_info(doi)
        if title:
            st.markdown(f'''
                <div class="article-card">
                    <div class="article-title">{title}</div>
                    <div class="article-authors"><strong>Autores:</strong> {authors}</div>
                    <div class="article-year"><strong>Publicado em:</strong> {published_year}</div>
                    <a class="article-link" href="{url}" target="_blank">Leia o artigo completo</a>
                    {' | <a class="article-link" href="' + pdf_link + '" target="_blank">Baixar PDF</a>' if pdf_link else ''}
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.warning(f"Não foi possível recuperar informações para o DOI: {doi}")
