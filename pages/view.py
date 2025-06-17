import streamlit as st
import matplotlib.pyplot as plt

# Função para simular a visão dicromática de um camundongo
def simulate_mouse_vision(rgb_color):
    r, g, b = rgb_color
    simulated_r = 0  # camundongos não veem vermelho
    simulated_g = g  # veem verde
    simulated_b = b * 0.5  # azul é parcialmente percebido
    return (simulated_r, simulated_g, simulated_b)

# Cores em RGB normalizado (valores entre 0 e 1)
colors_human = {
    "Branco": (1, 1, 1),
    "Azul Claro": (0.6, 0.8, 1),
    "Azul Escuro": (0.1, 0.1, 0.6),
    "Vermelho": (1, 0, 0)
}

colors_mouse = {name: simulate_mouse_vision(rgb) for name, rgb in colors_human.items()}

# Título da página
st.title("Simulação de Visão de Camundongos (Mus musculus - Swiss)")
st.write("Comparação entre a percepção de cores por humanos e camundongos.")

# Criar gráfico comparativo
fig, axs = plt.subplots(2, len(colors_human), figsize=(12, 3))

for idx, (name, rgb) in enumerate(colors_human.items()):
    axs[0, idx].imshow([[rgb]])
    axs[0, idx].set_title(name, fontsize=10)
    axs[0, idx].axis('off')
    axs[1, idx].imshow([[colors_mouse[name]]])
    axs[1, idx].axis('off')

axs[0, 0].set_ylabel("Humano", fontsize=10)
axs[1, 0].set_ylabel("Camundongo", fontsize=10)
fig.suptitle("Visão Humana vs Visão de Camundongo", fontsize=14)

st.pyplot(fig)

# Explicação
with st.expander("ℹ️ Explicação técnica"):
    st.markdown("""
    - Camundongos são dicromatas, com cones sensíveis ao ultravioleta (~360 nm) e ao verde (~510 nm).
    - Eles não percebem o vermelho e têm visão limitada do azul.
    - Nesta simulação, o canal vermelho foi removido, e o azul atenuado para representar sua baixa percepção.
    - Isso é útil para entender como eles percebem estímulos visuais em laboratório ou natureza.
    """)
