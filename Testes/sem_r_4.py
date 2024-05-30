import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks, savgol_filter

# Carregar os dados do arquivo CSV
data = pd.read_csv('RawData.csv')

# Extrair os valores de tempo e acelerações
time = data['Time (s)'].values
acceleration_x = data['Linear Acceleration x (m/s^2)'].values

# Aplicar o filtro de Savitzky-Golay para suavizar os dados
window_length = 51  # Deve ser um número ímpar e maior que polyorder
polyorder = 3
smoothed_x = savgol_filter(acceleration_x, window_length, polyorder)

# Detectar os picos nos dados originais
peaks, _ = find_peaks(acceleration_x, height=2)

# Definir a largura da janela ao redor dos picos para preservação
peak_window = 5

# Restaurar os valores dos picos significativos e seus arredores nos dados suavizados
smoothed_x_with_peaks = smoothed_x.copy()
for peak in peaks:
    start = max(0, peak - peak_window)
    end = min(len(acceleration_x), peak + peak_window + 1)
    smoothed_x_with_peaks[start:end] = acceleration_x[start:end]

# Plotar os gráficos
plt.figure(figsize=(15, 5))

# Primeiro subplot
plt.subplot(1, 1, 1)
plt.plot(time, acceleration_x, linestyle='--', color='b', label='Original')
plt.plot(time, smoothed_x, linestyle='-', color='g', label='Suavizado (Savitzky-Golay)')
plt.plot(time, smoothed_x_with_peaks, linestyle='-', color='r', label='Suavizado com Picos Restaurados')
plt.title('Aceleração 1')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')
plt.legend()

plt.show()
