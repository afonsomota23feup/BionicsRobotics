import datetime
import math
import numpy as np
import pandas as pd
import imufusion
import matplotlib.pyplot as pyplot
import matplotlib.pyplot as plt
import numpy
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Load accelerometer data
data_acel = pd.read_csv('sim_acele1.csv')
raw_acceleration_x = data_acel['Acceleration X'].values
raw_acceleration_y = data_acel['Acceleration Y'].values
raw_acceleration_z = data_acel['Acceleration Z'].values

# Load gyroscope data
data_gyro = pd.read_csv('sim_gyro1.csv')
raw_gyroscope_x = data_gyro['Gyroscope X'].values
raw_gyroscope_y = data_gyro['Gyroscope Y'].values
raw_gyroscope_z = data_gyro['Gyroscope Z'].values

# Load magnetometer data
data_magn = pd.read_csv('sim_magn1.csv')
raw_magnetometer_x = data_magn['Magnetometer X'].values
raw_magnetometer_y = data_magn['Magnetometer Y'].values
raw_magnetometer_z = data_magn['Magnetometer Z'].values

# Load force data (not used in this script but loaded as per original code)
data_force = pd.read_csv('sim_force.csv')
raw_force1 = data_force['Force 1'].values
raw_force2 = data_force['Force 2'].values

# Define time vector based on the number of samples and sampling frequency
num_samples = raw_acceleration_x.size
sampling_frequency = 50  # Hz
time_stamps = np.linspace(0, (num_samples - 1) / sampling_frequency, num_samples)


sample_rate = 50  # 100 Hz

# Convert lists to numpy arrays
timestamp = np.array(time_stamps)
accelerometer = np.column_stack((raw_acceleration_x, raw_acceleration_y, raw_acceleration_z))
accelerometer = accelerometer*9.81  # Convert from g to m/s^2
gyroscope = np.column_stack((raw_gyroscope_x, raw_gyroscope_y, raw_gyroscope_z))
magnetometer = np.column_stack((raw_magnetometer_x, raw_magnetometer_y, raw_magnetometer_z))

# Instantiate algorithms
offset = imufusion.Offset(sample_rate)
ahrs = imufusion.Ahrs()

ahrs.settings = imufusion.Settings(imufusion.CONVENTION_NWU,  # convention
                                   0.5,  # gain
                                   2000,  # gyroscope range
                                   10,  # acceleration rejection
                                   10,  # magnetic rejection
                                   5 * sample_rate)  # recovery trigger period = 5 seconds

# Process sensor data
delta_time = numpy.diff(timestamp, prepend=timestamp[0])

euler = numpy.empty((len(timestamp), 3))
internal_states = numpy.empty((len(timestamp), 6))
flags = numpy.empty((len(timestamp), 4))

for index in range(len(timestamp)):
    gyroscope[index] = offset.update(gyroscope[index])

    ahrs.update(gyroscope[index], accelerometer[index], magnetometer[index], delta_time[index])

    euler[index] = ahrs.quaternion.to_euler()

    ahrs_internal_states = ahrs.internal_states
    internal_states[index] = numpy.array([ahrs_internal_states.acceleration_error,
                                          ahrs_internal_states.accelerometer_ignored,
                                          ahrs_internal_states.acceleration_recovery_trigger,
                                          ahrs_internal_states.magnetic_error,
                                          ahrs_internal_states.magnetometer_ignored,
                                          ahrs_internal_states.magnetic_recovery_trigger])

    ahrs_flags = ahrs.flags
    flags[index] = numpy.array([ahrs_flags.initialising,
                                ahrs_flags.angular_rate_recovery,
                                ahrs_flags.acceleration_recovery,
                                ahrs_flags.magnetic_recovery])


def plot_bool(axis, x, y, label):
    axis.plot(x, y, "tab:cyan", label=label)
    pyplot.sca(axis)
    pyplot.yticks([0, 1], ["False", "True"])
    axis.grid()
    axis.legend()


# Plot Euler angles
figure, axes = pyplot.subplots(nrows=11, sharex=True, gridspec_kw={"height_ratios": [6, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1]})

figure.suptitle("Euler angles, internal states, and flags")

axes[0].plot(timestamp, euler[:, 0], "tab:red", label="Roll")
axes[0].plot(timestamp, euler[:, 1], "tab:green", label="Pitch")
axes[0].plot(timestamp, euler[:, 2], "tab:blue", label="Yaw")
axes[0].set_ylabel("Degrees")
axes[0].grid()
axes[0].legend()

# Plot initialising flag
plot_bool(axes[1], timestamp, flags[:, 0], "Initialising")

# Plot angular rate recovery flag
plot_bool(axes[2], timestamp, flags[:, 1], "Angular rate recovery")

# Plot acceleration rejection internal states and flag
axes[3].plot(timestamp, internal_states[:, 0], "tab:olive", label="Acceleration error")
axes[3].set_ylabel("Degrees")
axes[3].grid()
axes[3].legend()

plot_bool(axes[4], timestamp, internal_states[:, 1], "Accelerometer ignored")

axes[5].plot(timestamp, internal_states[:, 2], "tab:orange", label="Acceleration recovery trigger")
axes[5].grid()
axes[5].legend()

plot_bool(axes[6], timestamp, flags[:, 2], "Acceleration recovery")

# Plot magnetic rejection internal states and flag
axes[7].plot(timestamp, internal_states[:, 3], "tab:olive", label="Magnetic error")
axes[7].set_ylabel("Degrees")
axes[7].grid()
axes[7].legend()

plot_bool(axes[8], timestamp, internal_states[:, 4], "Magnetometer ignored")

axes[9].plot(timestamp, internal_states[:, 5], "tab:orange", label="Magnetic recovery trigger")
axes[9].grid()
axes[9].legend()

plot_bool(axes[10], timestamp, flags[:, 3], "Magnetic recovery")

pyplot.show(block="no_block" not in sys.argv)  # don't block when script run by CI

# Funções de rotação
def euler_to_rotation_matrix(roll, pitch, yaw):
    """ Converte ângulos de Euler em uma matriz de rotação 3x3. """
    R_x = np.array([[1, 0, 0],
                    [0, math.cos(roll), -math.sin(roll)],
                    [0, math.sin(roll), math.cos(roll)]])
    
    R_y = np.array([[math.cos(pitch), 0, math.sin(pitch)],
                    [0, 1, 0],
                    [-math.sin(pitch), 0, math.cos(pitch)]])
    
    R_z = np.array([[math.cos(yaw), -math.sin(yaw), 0],
                    [math.sin(yaw), math.cos(yaw), 0],
                    [0, 0, 1]])
    
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R

def apply_rotation_matrix(R, position):
    """ Aplica uma matriz de rotação a um vetor de posição. """
    return np.dot(R, position)


# Inicializa a posição inicial e a lista para armazenar as posições transformadas
initial_position = np.array([-1, 0, 0])
transformed_positions = []

# Calcular e armazenar as posições transformadas ao longo do tempo
for i in range(num_samples):
    roll = euler[i, 0] * math.pi / 180.0  # Convertendo para radianos
    pitch = euler[i, 1] * math.pi / 180.0
    yaw = euler[i, 2] * math.pi / 180.0

    R = euler_to_rotation_matrix(roll, pitch, yaw)
    transformed_position = apply_rotation_matrix(R, initial_position)
    transformed_positions.append(transformed_position)

# Converter a lista para um array NumPy para facilitar a plotagem
transformed_positions = np.array(transformed_positions)

mov_x = transformed_positions[:, 0]
mov_y = transformed_positions[:, 1]
mov_z =  transformed_positions[:, 2]


# mov_x = 10*mov_x
# mov_y = 10*mov_y
# mov_z = 10*mov_z

# Create a figure and a 3D axis with a larger size
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Frequency and time calculations
frequency = 50  # Hz
time_increment = 1 / frequency  # seconds

# Function to update the scatter plot
def update(frame):
    ax.clear()  # Clear the previous points
    start = max(0, frame - 30)  # Ensure we don't go below zero
    
    # Get the current segment of data
    x_data = mov_x[start:frame]
    y_data = mov_y[start:frame]
    z_data = mov_z[start:frame]


    # Create a color gradient
    colors = plt.cm.viridis(np.linspace(0, 1, len(x_data)))
    
    ax.scatter(x_data, y_data, z_data, c=colors, marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Calculate the current timestamp
    ax.set_title(f'Frame {frame}')
    
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    ax.set_zlim(-1, 2)


# Create the animation with a shorter interval
ani = FuncAnimation(fig, update, frames=len(mov_x), interval=0.01)  # Interval in milliseconds

# Save the animation as a GIF
save_gif = input("Do you want to save the animation as a GIF? (y/n): ")

if save_gif.lower() == "y":
    ani.save('animation_v1.gif', writer='imagemagick')
    print("Animation saved as animation_v1.gif")
else:
    print("Animation not saved.")

# Display the animation
plt.show()

# # Crie um gráfico 3D para visualizar as posições transformadas ao longo do tempo
# fig = pyplot.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(mov_x, mov_y, mov_z, c='r', marker='o')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# pyplot.title('Posições Transformadas ao Longo do Tempo')
# pyplot.show()
