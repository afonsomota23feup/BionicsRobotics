import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks

# Carregar os dados do arquivo CSV
data = pd.read_csv('15_05_1.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
#acceleration_x = data['Linear Acceleration x (m/s^2)'].values
acceleration_y = data['Linear Acceleration y (m/s^2)'].values
#acceleration_z = data['Linear Acceleration z (m/s^2)'].values

# Initialize filter
filter_window = 5
filter_coeff = np.ones(filter_window) / filter_window

# Filter the data
#filtered_x = np.convolve(acceleration_x, filter_coeff, mode='same')
filtered_y = np.convolve(acceleration_y, filter_coeff, mode='same')
#filtered_z = np.convolve(acceleration_z, filter_coeff, mode='same')

# Detectar os picos em cada série temporal
#peaks_x, _ = find_peaks(filtered_x)
peaks_y, _ = find_peaks(filtered_y)
#peaks_z, _ = find_peaks(filtered_z)

# Filtrar os picos para considerar apenas valores superiores a 2 ou inferiores a -2
#peaks_acceleration_x = [peak for peak in peaks_x if filtered_x[peak] > 2 or filtered_x[peak] < -2]
peaks_acceleration_y = [peak for peak in peaks_y if filtered_y[peak] > 2 or filtered_y[peak] < -2]
#peaks_acceleration_z = [peak for peak in peaks_z if filtered_z[peak] > 2 or filtered_z[peak] < -2]

# Substituir valores entre -1 e 1 por zero
#filtered_x[(filtered_x >= -1) & (filtered_x <= 1)] = 0
filtered_y[(filtered_y >= -1) & (filtered_y <= 1)] = 0
#filtered_z[(filtered_z >= -1) & (filtered_z <= 1)] = 0

# Criar a figura e o subplot 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Definir os limites fixos dos eixos
#max_range = max(max(filtered_x) - min(filtered_x), max(filtered_y) - min(filtered_y), max(filtered_z) - min(filtered_z))
max_range = max( max(filtered_y) - min(filtered_y))
#xlim = (min(filtered_x), min(filtered_x) + max_range)
ylim = (min(filtered_y), min(filtered_y) + max_range)
#zlim = (min(filtered_z), min(filtered_z) + max_range)

# Inicialização da animação (função vazia)
def init():
    #ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    #ax.set_zlim(zlim)
    # Adicionar a bolinha no centro do referencial
    ax.scatter(0, 0, 0, color='purple', s=50)
    return [ax]

# Função para determinar a cor com base na direção da aceleração
def get_color(dx, dy, dz):
    if dx != 0 and dy == 0 and dz == 0:
        return 'r'  # Aceleração apenas no eixo x
    elif dx == 0 and dy != 0 and dz == 0:
        return 'g'  # Aceleração apenas no eixo y
    elif dx == 0 and dy == 0 and dz != 0:
        return 'b'  # Aceleração apenas no eixo z
    elif dx != 0 and dy != 0 and dz == 0:
        return 'm'  # Aceleração nos eixos x e y
    elif dx != 0 and dy == 0 and dz != 0:
        return 'y'  # Aceleração nos eixos x e z
    elif dx == 0 and dy != 0 and dz != 0:
        return 'c'  # Aceleração nos eixos y e z
    else:
        return 'k'  # Aceleração nos eixos x, y e z simultaneamente

# Função de animação
def update(frame):
    ax.cla()
    #ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    #ax.set_zlim(zlim)
    for i in range(1, frame):
        #color = get_color(filtered_x[i] - filtered_x[i-1], filtered_y[i] - filtered_y[i-1], filtered_z[i] - filtered_z[i-1])
        #ax.plot(filtered_x[i-1:i+1], filtered_y[i-1:i+1], filtered_z[i-1:i+1], color=color)
        color = get_color(filtered_y[i] - filtered_y[i-1])
        ax.plot(filtered_y[i-1:i+1], color=color)
    
    # Adicionar a bolinha na posição atual
    #ax.scatter(filtered_x[frame-1], filtered_y[frame-1], filtered_z[frame-1], color='purple', s=50)
    ax.scatter( filtered_y[frame-1], color='purple', s=50)
    
    #ax.set_xlabel('Aceleração eixo x (m/s^2)')
    ax.set_ylabel('Aceleração eixo y (m/s^2)')
    #ax.set_zlabel('Aceleração eixo z (m/s^2)')
    return [ax]

# Criar animação
ani = FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True)

plt.show()

