import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks

# Carregar os dados do arquivo CSV
data = pd.read_csv('RawData.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values
acceleration_y = data['Linear Acceleration y (m/s^2)'].values
acceleration_z= data['Linear Acceleration z (m/s^2)'].values

# Initialize filter
filter_window = 5
filter_coeff = np.ones(filter_window)/filter_window
calibration_offset = 0
calibration_gain = 1
    
# Filter the data
filtered_x = np.convolve(acceleration_x, filter_coeff, mode='same')
filtered_y = np.convolve(acceleration_y, filter_coeff, mode='same')
filtered_z = np.convolve(acceleration_z, filter_coeff, mode='same')

# Detectar os picos em cada série temporal
peaks_acceleration_x, _ = find_peaks(filtered_x)
peaks_acceleration_y, _ = find_peaks(filtered_y)
peaks_acceleration_z, _ = find_peaks(filtered_z)

# Definir os valores seguintes aos picos como zero
for peak in peaks_acceleration_x:
    acceleration_x[peak + 1] = 0
for peak in peaks_acceleration_y:
    acceleration_y[peak + 1] = 0
for peak in peaks_acceleration_z:
    acceleration_z[peak + 1] = 0

# Plotar os gráficos
# plt.figure(figsize=(15, 5)) é das imagens 2D
# Criar a figura e o subplot 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Primeiro subplot
# plt.subplot(1, 3, 1)
# plt.plot(time, acceleration1, linestyle='--', color='b')
# plt.title('Aceleração 1')
# plt.xlabel('Tempo (s)')
# plt.ylabel('Aceleração (m/s^2)')

# Segundo subplot
# plt.subplot(1, 3, 2)
# plt.plot(time, acceleration2, linestyle='--', color='r')
# plt.title('Aceleração 2')
# plt.xlabel('Tempo (s)')
# plt.ylabel('Aceleração (m/s^2)')

# Terceiro subplot
# plt.subplot(1, 3, 3)
#plt.plot(time, acceleration3, linestyle='--', color='g')
#plt.title('Aceleração 3')
#plt.xlabel('Tempo (s)')
#plt.ylabel('Aceleração (m/s^2)')

#plt.tight_layout()

# Plotar os dados
# ax.plot(time, acceleration1, acceleration2, linestyle='--', color='b', label='Aceleração 1')
# ax.plot(time, acceleration2, acceleration3, linestyle='--', color='r', label='Aceleração 2')
# ax.plot(time, acceleration3, acceleration1, linestyle='--', color='g', label='Aceleração 3')

# Plotar os picos
# ax.plot(time[peaks_acceleration1], acceleration1[peaks_acceleration1], acceleration2[peaks_acceleration1], linestyle='--', color='b', label='Picos Aceleração 1')
# ax.plot(time[peaks_acceleration2], acceleration1[peaks_acceleration2], acceleration2[peaks_acceleration2], linestyle='--', color='r', label='Picos Aceleração 2')
# ax.plot(time[peaks_acceleration3], acceleration1[peaks_acceleration3], acceleration2[peaks_acceleration3], linestyle='--', color='g', label='Picos Aceleração 3')

# Inicialização da animação (função vazia)
def init():
    ax.set_xlim(min(peaks_acceleration_x), max(acceleration_x))
    ax.set_ylim(min(peaks_acceleration_y), max(acceleration_y))
    ax.set_zlim(min(peaks_acceleration_z), max(acceleration_z))
    return []

# Função de animação
def update(frame):
    ax.cla()
    ax.plot(peaks_acceleration_x[:frame], peaks_acceleration_y[:frame], peaks_acceleration_z[:frame], color='b')
    # Definir rótulos dos eixos
    #ax.set_xlabel('Tempo (s)')
    ax.set_xlabel('Aceleração eixo x (m/s^2)')
    ax.set_ylabel('Aceleração eixo y (m/s^2)')
    ax.set_zlabel('Aceleração eixo z (m/s^2)')
    return [ax]

# Plotar o movimento 3D
#ax.plot (acceleration1, acceleration2, acceleration3, linestyle='--', color='r')

# Criar animação
ani = FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True)

# Adicionar legenda
#ax.legend()
plt.show()