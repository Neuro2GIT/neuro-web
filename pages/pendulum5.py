import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import streamlit as st
from PIL import Image

# Parâmetros do pêndulo
g = 9.81  # aceleração devido à gravidade (m/s^2)
L = 1.0   # comprimento do pêndulo (m)
theta_0 = np.pi / 4  # ângulo inicial (rad)

# Função para calcular a posição do pêndulo ao longo do tempo
def pendulum(t, theta_0):
    return theta_0 * np.cos(np.sqrt(g / L) * t)

# Função para criar a animação e retornar como imagem codificada em base64
def create_pendulum_animation():
    # Configurar o gráfico
    fig, ax = plt.subplots()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    line, = ax.plot([], [], 'o-', lw=2)

    # Lista para armazenar os quadros da animação
    frames = []

    # Gerar os quadros da animação
    for t in np.linspace(0, 10, 200):
        x = L * np.sin(pendulum(t, theta_0))
        y = -L * np.cos(pendulum(t, theta_0))
        line.set_data([0, x], [0, y])

        # Salvar o quadro como imagem e adicionar à lista de frames
        fig.canvas.draw()

        # Usando print_to_buffer() para capturar a imagem
        buf = fig.canvas.print_to_buffer()
        img = np.frombuffer(buf[0], dtype=np.uint8).reshape(buf[1][::-1] + (4,))
        pil_img = Image.fromarray(img)
        frames.append(pil_img)

    # Salvar os quadros como um GIF em memória
    buf = BytesIO()
    frames[0].save(buf, save_all=True, append_images=frames[1:], optimize=True, duration=100, loop=0)
    buf.seek(0)

    # Codificar a animação em base64 para exibir no Streamlit
    gif_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return gif_data

# Título da página Streamlit
st.title('Animação do Pêndulo')

# Gerar a animação
gif_data = create_pendulum_animation()

# Exibir a animação na página
st.image(f"data:image/gif;base64,{gif_data}", use_column_width=True)
