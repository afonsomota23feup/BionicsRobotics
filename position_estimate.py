import numpy as np
import pandas as pd
import imufusion
import matplotlib.pyplot as pyplot
import numpy
import sys

# Load accelerometer data
data_acel = pd.read_csv('sim_acele.csv')
raw_acceleration_x = data_acel['Acceleration X'].values
raw_acceleration_y = data_acel['Acceleration Y'].values
raw_acceleration_z = data_acel['Acceleration Z'].values

# Load gyroscope data
data_gyro = pd.read_csv('sim_gyro.csv')
raw_gyroscope_x = data_gyro['Gyroscope X'].values
raw_gyroscope_y = data_gyro['Gyroscope Y'].values
raw_gyroscope_z = data_gyro['Gyroscope Z'].values

# Load magnetometer data
data_magn = pd.read_csv('sim_magn.csv')
raw_magnetometer_x = data_magn['Magnetometer X'].values
raw_magnetometer_y = data_magn['Magnetometer Y'].values
raw_magnetometer_z = data_magn['Magnetometer Z'].values

# Load force data (not used in this script but loaded as per original code)
data_force = pd.read_csv('sim_force.csv')
raw_force1 = data_force['Force 1'].values
raw_force2 = data_force['Force 2'].values

# Combine the data into arrays of shape (num_samples, 3)
acc_data = np.vstack((raw_acceleration_x, raw_acceleration_y, raw_acceleration_z)).T
gyro_data = np.vstack((raw_gyroscope_x, raw_gyroscope_y, raw_gyroscope_z)).T
mag_data = np.vstack((raw_magnetometer_x, raw_magnetometer_y, raw_magnetometer_z)).T

# Define time vector based on the number of samples and sampling frequency
num_samples = raw_acceleration_x.size
sampling_frequency = 50  # Hz
time_stamps = np.linspace(0, (num_samples - 1) / sampling_frequency, num_samples)


sample_rate = 50  # 100 Hz

# Convert lists to numpy arrays
timestamp = np.array(time_stamps)
accelerometer = np.column_stack((raw_acceleration_x, raw_acceleration_y, raw_acceleration_z))
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