import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

# Carregar os dados do arquivo CSV
data = pd.read_csv('RawData.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values

# Aplicar um filtro de média móvel para suavizar os dados
window_size = 5
moving_avg_x = np.convolve(acceleration_x, np.ones(window_size)/window_size, mode='same')

# Detectar os picos nos dados originais
peaks, _ = find_peaks(acceleration_x, height=2)

# Restaurar os valores dos picos significativos nos dados suavizados
smoothed_x_with_peaks = moving_avg_x.copy()
smoothed_x_with_peaks[peaks] = acceleration_x[peaks]

# Plotar os gráficos
plt.figure(figsize=(15, 5))

# Primeiro subplot
plt.subplot(1, 1, 1)
plt.plot(time, acceleration_x, linestyle='--', color='b', label='Original')
plt.plot(time, moving_avg_x, linestyle='-', color='g', label='Suavizado (Média Móvel)')
plt.plot(time, smoothed_x_with_peaks, linestyle='-', color='r', label='Suavizado com Picos Restaurados')
plt.title('Aceleração 1')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')
plt.legend()

plt.show()
