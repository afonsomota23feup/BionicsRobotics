import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define Kalman filter parameters
Q = 0.01  # Process noise covariance
R = 0.2   # Measurement noise covariance
P = 1     # Estimation error covariance


# time = data['Time (s)'].values
time = []
force = []
velocity_x = []
position_x = []


raw_data_points = []
converted_data_points = []
instants_data = []
unpackedData = []

filtered_position = []

# 'gyro_data' is your gyroscope data, and 'dt' is the time step

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def KalmanFilter(data, Q, R, P=1):
    filtered_position = data
<<<<<<< HEAD
    # x = 0     # Initial position estimate
=======
    x = 0     # Initial position estimate
>>>>>>> 7b44716932c548243f27e4b33a1fcc817b92cb28
    # v = 0     # Initial velocity estimate
    # for i in range(len(data)):
    #     # Prediction step
    #     x += v
    #     P += Q
        
    #     # Correction step (measurement update)
    #     K = P / (P + R)
    #     x += K * (data[i] - x)
    #     v = x
        
    #     # Store filtered position estimates
    #     filtered_position.append(x)
    return filtered_position



<<<<<<< HEAD

# Carregar os dados do arquivo CSV
data_acel = pd.read_csv('sim_acele.csv')
=======
# Carregar os dados do arquivo CSV
data_acel = pd.read_csv('Accelerometer_v3.csv')
# Extrair os valores de tempo e acelerações
time = data_acel['Time (s)'].values
raw_acceleration_x = data_acel['Acceleration x (m/s^2)'].values
raw_acceleration_y = data_acel['Acceleration y (m/s^2)'].values
raw_acceleration_z= data_acel['Acceleration z (m/s^2)'].values


# Carregar os dados do arquivo CSV
data_gy = pd.read_csv('Gyroscope_v3.csv')
>>>>>>> 7b44716932c548243f27e4b33a1fcc817b92cb28
# Extrair os valores de tempo e acelerações

raw_acceleration_x = data_acel['Acceleration X'].values
raw_acceleration_y = data_acel['Acceleration Y'].values
raw_acceleration_z= data_acel['Acceleration Z'].values

# Número de amostras
num_amostras = raw_acceleration_x.size
# Frequência de amostragem (em Hz)
frequencia_amostragem = 50
# Calcula o intervalo de tempo entre cada amostra
intervalo_tempo = 1 / frequencia_amostragem
# Cria o vetor de tempo
time = [i * intervalo_tempo for i in range(num_amostras)]

# Carregar os dados do arquivo CSV
data_gy = pd.read_csv('sim_gyro.csv')
# Extrair os valores de tempo e acelerações
raw_gyro_x = data_gy['Gyroscope X'].values
raw_gyro_y = data_gy['Gyroscope Y'].values
raw_gyro_z = data_gy['Gyroscope Z'].values

# Carregar os dados do arquivo CSV
data_gy = pd.read_csv('sim_magn.csv')
# Extrair os valores de tempo e acelerações
raw_gyro_x = data_gy['Magnetometer X'].values
raw_gyro_y = data_gy['Magnetometer Y'].values
raw_gyro_z = data_gy['Magnetometer Z'].values



time
acceleration_x = raw_acceleration_x
acceleration_y = raw_acceleration_y
acceleration_z = raw_acceleration_z

gyro_x = raw_gyro_x
gyro_y = raw_gyro_y
gyro_z = raw_gyro_z

magno_x = raw_gyro_x
magno_y = raw_gyro_y
magno_z = raw_gyro_z


<<<<<<< HEAD

alpha = 0.1 # This is the weight for the gyroscope data. You might need to adjust this.
dt = 1/50

alphaz = 0.9
=======
alpha = 0.01 # This is the weight for the gyroscope data. You might need to adjust this.
dt= 1

alphaz = 0.75
>>>>>>> 7b44716932c548243f27e4b33a1fcc817b92cb28

#Calculate the velocity and position in the x-axis
velocity_x = alpha * (np.cumsum(gyro_x) * dt) + (1 - alpha) * np.array(acceleration_x)
# velocity_x = KalmanFilter(velocity_x, Q, R, P)

position_x = np.cumsum(velocity_x) * dt
position_x = KalmanFilter(position_x, Q, R, P)

#Calculate the velocity and position in the y-axis
velocity_y = 10* (alpha * (np.cumsum(gyro_y) * dt) + (1 - alpha) * np.array(acceleration_y))
position_y = (np.cumsum(velocity_y) * dt)*0.1

#calculate the velocity and position in the z-axis
velocity_z = 10*(alphaz * (np.cumsum(gyro_z) * dt) + (1 - alphaz) * np.array(acceleration_z))
position_z = (np.cumsum(velocity_z) * dt)*0.1

# Create subplots with 3 rows and 1 column
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# Plot acceleration, velocity, and position for x-axis
axes[0].plot(acceleration_x, label='Aceleração em X')
axes[0].plot(velocity_x, label='Velocidade em X')
axes[0].plot(position_x, label='Posição em X')
axes[0].set_xlabel('Amostra')
axes[0].set_title('Aceleração, Velocidade e Posição vs Tempo em X')
axes[0].legend()

# Plot acceleration, velocity, and position for y-axis
axes[1].plot(acceleration_y, label='Aceleração em Y')
axes[1].plot(velocity_y, label='Velocidade em Y')
axes[1].plot(position_y, label='Posição em Y')
axes[1].set_xlabel('Amostra')
axes[1].set_title('Aceleração, Velocidade e Posição vs Tempo em Y')
axes[1].legend()

# Plot acceleration, velocity, and position for z-axis
axes[2].plot(acceleration_z, label='Aceleração em Z')
axes[2].plot(velocity_z, label='Velocidade em Z')
axes[2].plot(position_z, label='Posição em Z')
axes[2].set_xlabel('Amostra')
axes[2].set_title('Aceleração, Velocidade e Posição vs Tempo em Z')
axes[2].legend()

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

