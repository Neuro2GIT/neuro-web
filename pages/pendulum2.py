import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit as st
from io import BytesIO
import base64
from matplotlib.animation import PillowWriter  # Usando PillowWriter

# Parâmetros do pêndulo
g = 9.81  # aceleração devido à gravidade (m/s^2)
L = 1.0   # comprimento do pêndulo (m)
theta_0 = np.pi / 4  # ângulo inicial (rad)

# Função para calcular a posição do pêndulo ao longo do tempo
def pendulum(t, theta_0):
    return theta_0 * np.cos(np.sqrt(g / L) * t)

# Função para criar a animação e retornar como imagem codificada em base64
def create_pendulum_animation():
    # Criar o gráfico
    fig, ax = plt.subplots()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    line, = ax.plot([], [], 'o-', lw=2)

    def init():
        line.set_data([], [])
        return line,

    def animate(t):
        x = L * np.sin(pendulum(t, theta_0))
        y = -L * np.cos(pendulum(t, theta_0))
        line.set_data([0, x], [0, y])
        return line,

    # Animação
    ani = FuncAnimation(fig, animate, frames=np.linspace(0, 10, 200),
                        init_func=init, blit=True)

    # Salvar a animação como um arquivo temporário em memória usando PillowWriter
    buf = BytesIO()
    writer = PillowWriter(fps=30)  # Usando o escritor Pillow
    ani.save(buf, writer=writer)
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
