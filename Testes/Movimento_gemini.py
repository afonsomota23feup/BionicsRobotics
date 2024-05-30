import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
import serial
#from scipy.integrate import trap

# Load data from CSV
data = pd.read_csv('15_05_1.csv')

time = data['Time (s)'].to_numpy()
acceleration_y = data['Linear Acceleration y (m/s^2)'].to_numpy()


# Calculate time differences
time_diff = time[1:] - time[:-1]

# Aplicar o filtro de Savitzky-Golay para suavizar os dados
window_length = 51  # Deve ser um número ímpar e maior que polyorder
polyorder = 3
acc_smoothed_y = savgol_filter(acceleration_y, window_length, polyorder)

# Detectar os picos nos dados originais
peaks, _ = find_peaks(acceleration_y, height=2)

# Definir a largura da janela ao redor dos picos para preservação
peak_window = 5

# Restaurar os valores dos picos significativos e seus arredores nos dados suavizados
acc_smoothed_y_with_peaks = acc_smoothed_y.copy()
for peak in peaks:
    start = max(0, peak - peak_window)
    end = min(len(acceleration_y), peak + peak_window + 1)
    acc_smoothed_y_with_peaks[start:end] = acceleration_y[start:end]

# Calculate velocity
velocity = acc_smoothed_y_with_peaks[:-1] * time_diff




# Aplicar o filtro de Savitzky-Golay para suavizar os dados
window_length = 51  # Deve ser um número ímpar e maior que polyorder
polyorder = 3
v_smoothed = savgol_filter(velocity, window_length, polyorder)

# Detectar os picos nos dados originais
v_peaks = find_peaks(velocity, height=2)

# Definir a largura da janela ao redor dos picos para preservação
peak_window = 5

# Restaurar os valores dos picos significativos e seus arredores nos dados suavizados
v_smoothed_with_peaks = v_smoothed.copy()
for peak in peaks:
    start = max(0, peak - peak_window)
    end = min(len(velocity), peak + peak_window + 1)
    v_smoothed_with_peaks[start:end] = velocity[start:end]


# Calculate position
position = np.cumsum(v_smoothed_with_peaks * time_diff)

# Visualize results
# plt.plot(time, acceleration_x, label='Aceleração')
# plt.plot(time, velocity, label='Velocidade')
# plt.plot(time, position, label='Posição')
plt.subplot(3, 1, 1)
plt.plot(time[:-1], acc_smoothed_y_with_peaks[:-1], label='Aceleração')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s^2)')
plt.subplot(3, 1, 2)
plt.plot(time[:-1], v_smoothed_with_peaks, label='Velocidade')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.subplot(3, 1, 3)
plt.plot(time[:-1], position, label='Posição')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.legend()
plt.show()


