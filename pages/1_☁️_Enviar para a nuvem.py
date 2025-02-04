import streamlit as st

# Página protegida
if st.session_state.get("password_correct", False):
    # Conteúdo da página protegida
    st.title("Página Protegida")
    st.write("Conteúdo visível apenas para usuários autenticados.")
else:
    # Se o usuário não estiver autenticado, exibe a mensagem de login
    st.warning("Por favor, faça login para acessar esta página.")
    st.stop()

def main():
    st.title("🐁Grupo neuroscience")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
