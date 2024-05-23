import asyncio
import math
import struct
from bleak import BleakClient, BleakScanner
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import imufusion
import numpy as np
from collections import deque

CHARACTERISTIC_UUID = "14181dce-eb95-46c5-8431-3b4fe0e0a12d"
CONNECTION_RETRIES = 3
CONNECTION_TIMEOUT = 30.0

# Lists to store the data
acceleration_x = []
acceleration_y = []
acceleration_z = []

gyroscope_x = []
gyroscope_y = []
gyroscope_z = []

magnetometer_x = []
magnetometer_y = []
magnetometer_z = []

raw_acceleration_x = []
raw_acceleration_y = []
raw_acceleration_z = []

raw_gyroscope_x = []
raw_gyroscope_y = []
raw_gyroscope_z = []

raw_magnetometer_x = []
raw_magnetometer_y = []
raw_magnetometer_z = []

force1 = []
force2 = []

notification_count = 0

# # Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# # Initialize data buffer
max_points = 1000  # Maximum number of data points to display
x_data = deque(maxlen=max_points)
y_data = deque(maxlen=max_points)
z_data = deque(maxlen=max_points)
sc = None  # Placeholder for scatter plot

# # To keep track of the number of received notifications
notification_count = 0


# Function to update the scatter plot
def update_plot(new_x, new_y, new_z):
    global sc
    x_data.append(new_x)
    y_data.append(new_y)
    z_data.append(new_z)
    if sc:
        sc.remove()  # Remove previous scatter plot
    sc = ax.scatter(x_data, y_data, z_data, c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Real-time 3D Scatter Plot')
    fig.canvas.draw()
    fig.canvas.flush_events()


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


async def notification_handler(sender, data):
    global notification_count

    # Assuming unpackedData is parsed from data, replace this with your actual parsing
    unpackedData = struct.unpack('55f', data)
    
    # # Parse data as described in the provided organization
    # ax1, ay1, az1 = unpackedData[0], unpackedData[1], unpackedData[2]
    # ax2, ay2, az2 = unpackedData[11], unpackedData[12], unpackedData[13]
    # ax3, ay3, az3 = unpackedData[22], unpackedData[23], unpackedData[24]
    # ax4, ay4, az4 = unpackedData[33], unpackedData[34], unpackedData[35]
    # ax5, ay5, az5 = unpackedData[44], unpackedData[45], unpackedData[46]

    # raw_acceleration_x.append([ax1, ax2, ax3, ax4, ax5])
    # raw_acceleration_y.append([ay1, ay2, ay3, ay4, ay5])
    # raw_acceleration_z.append([az1, az2, az3, az4, az5])
    
    # # Parse data as described in the provided organization
    # gx1, gy1, gz1 = unpackedData[3], unpackedData[4], unpackedData[5]
    # gx2, gy2, gz2 = unpackedData[14], unpackedData[15], unpackedData[16]
    # gx3, gy3, gz3 = unpackedData[25], unpackedData[26], unpackedData[27]
    # gx4, gy4, gz4 = unpackedData[36], unpackedData[37], unpackedData[38]
    # gx5, gy5, gz5 = unpackedData[47], unpackedData[48], unpackedData[49]

    # # Append data to lists
    # raw_gyroscope_x.append([gx1, gx2, gx3, gx4, gx5])
    # raw_gyroscope_y.append([gy1, gy2, gy3, gy4, gy5])
    # raw_gyroscope_z.append([gz1, gz2, gz3, gz4, gz5])

    # mx1, my1, mz1 = unpackedData[6], unpackedData[7], unpackedData[8]
    # mx2, my2, mz2 = unpackedData[17], unpackedData[18], unpackedData[19]
    # mx3, my3, mz3 = unpackedData[28], unpackedData[29], unpackedData[30]
    # mx4, my4, mz4 = unpackedData[39], unpackedData[40], unpackedData[41]
    # mx5, my5, mz5 = unpackedData[50], unpackedData[51], unpackedData[52]

    # raw_magnetometer_x.append([mx1, mx2, mx3, mx4, mx5])
    # raw_magnetometer_y.append([my1, my2, my3, my4, my5])
    # raw_magnetometer_z.append([mz1, mz2, mz3, mz4, mz5])

    # f11, f12 = unpackedData[9], unpackedData[10]
    # f21, f22 = unpackedData[20], unpackedData[21]
    # f31, f32 = unpackedData[31], unpackedData[32]
    # f41, f42 = unpackedData[42], unpackedData[43]
    # f51, f52 = unpackedData[53], unpackedData[54]

    # force1.append([f11, f21, f31, f41, f51])
    # force2.append([f12, f22, f32, f42, f52])

    # # Define time vector based on the number of samples and sampling frequency
    # num_samples = notification_count*5
    # sampling_frequency = 50  # Hz
    # time_stamps = np.linspace(0, (num_samples - 1) / sampling_frequency, num_samples)


    # sample_rate = 50  # 100 Hz

    # # Convert lists to numpy arrays
    # timestamp = np.array(time_stamps)
    # accelerometer = np.column_stack((raw_acceleration_x, raw_acceleration_y, raw_acceleration_z))
    # gyroscope = np.column_stack((raw_gyroscope_x, raw_gyroscope_y, raw_gyroscope_z))
    # magnetometer = np.column_stack((raw_magnetometer_x, raw_magnetometer_y, raw_magnetometer_z))

    # # Instantiate algorithms
    # offset = imufusion.Offset(sample_rate)
    # ahrs = imufusion.Ahrs()

    # ahrs.settings = imufusion.Settings(imufusion.CONVENTION_NWU,  # convention
    #                                 0.5,  # gain
    #                                 2000,  # gyroscope range
    #                                 10,  # acceleration rejection
    #                                 10,  # magnetic rejection
    #                                 5 * sample_rate)  # recovery trigger period = 5 seconds

    # # Process sensor data
    # delta_time = np.diff(timestamp, prepend=timestamp[0])

    # euler = np.empty((len(timestamp), 3))
    # internal_states = np.empty((len(timestamp), 6))
    # flags = np.empty((len(timestamp), 4))

    # for index in range(len(timestamp)):
    #     gyroscope[index] = offset.update(gyroscope[index])

    #     ahrs.update(gyroscope[index], accelerometer[index], magnetometer[index], delta_time[index])

    #     euler[index] = ahrs.quaternion.to_euler()

    #     ahrs_internal_states = ahrs.internal_states
    #     internal_states[index] = np.array([ahrs_internal_states.acceleration_error,
    #                                         ahrs_internal_states.accelerometer_ignored,
    #                                         ahrs_internal_states.acceleration_recovery_trigger,
    #                                         ahrs_internal_states.magnetic_error,
    #                                         ahrs_internal_states.magnetometer_ignored,
    #                                         ahrs_internal_states.magnetic_recovery_trigger])

    #     ahrs_flags = ahrs.flags
    #     flags[index] = np.array([ahrs_flags.initialising,
    #                                 ahrs_flags.angular_rate_recovery,
    #                                 ahrs_flags.acceleration_recovery,
    #                                 ahrs_flags.magnetic_recovery])
    
    # # Converter a lista para um array NumPy para facilitar a plotagem
    # transformed_positions = np.array(transformed_positions)

    # mov_x = transformed_positions[:, 0]
    # mov_y = transformed_positions[:, 1]
    # mov_z =  transformed_positions[:, 2]

    # Update the scatter plot
    #update_plot(mov_x, mov_y, mov_z)

    notification_count += 1
    print(f"Notification {notification_count}: {unpackedData}")

async def connect_and_interact_with_characteristic(device_id, characteristic_uuid):
    for attempt in range(CONNECTION_RETRIES):
        try:
            async with BleakClient(device_id, timeout=CONNECTION_TIMEOUT) as client:
                if not client.is_connected:
                    print(f"Failed to connect to device: {device_id}")
                    continue
                
                print(f"Connected to device: {device_id}")
                services = await client.get_services()

                characteristic_found = False
                for service in services:
                    for characteristic in service.characteristics:
                        if characteristic.uuid == characteristic_uuid:
                            characteristic_found = True
                            print(f"Found characteristic: {characteristic.uuid}")
                            if "notify" in characteristic.properties:
                                try:
                                    await client.start_notify(characteristic, notification_handler)
                                    print("Started notification...")
                                    await asyncio.sleep(10)  # Listen for notifications for 30 seconds
                                    await client.stop_notify(characteristic)
                                    print("Stopped notification.")
                                except Exception as e:
                                    print(f"Failed to start/stop notify: {e}")
                            else:
                                print(f"Characteristic does not support notify.")
                            break
                
                if not characteristic_found:
                    print(f"Characteristic {characteristic_uuid} not found")
                break  # Exit the retry loop if connected successfully
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < CONNECTION_RETRIES - 1:
                print("Retrying...")
            await asyncio.sleep(5)  # Wait a bit before retrying
    else:
        print("Failed to connect after several attempts.")

async def main():
    device_id = "84:71:27:AC:20:D2"
    
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
    
    print(f"\nConnecting to device: {device_id}")
    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Initialize data buffer
    max_points = 1000  # Maximum number of data points to display
    x_data = deque(maxlen=max_points)
    y_data = deque(maxlen=max_points)
    z_data = deque(maxlen=max_points)
    sc = None  # Placeholder for scatter plot

    # To keep track of the number of received notifications

    # Function to update the scatter plot
    def update_plot(new_x, new_y, new_z):
        global sc
        x_data.append(new_x)
        y_data.append(new_y)
        z_data.append(new_z)
        if sc:
            sc.remove()  # Remove previous scatter plot
        sc = ax.scatter(x_data, y_data, z_data, c='r', marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Real-time 3D Scatter Plot')
        fig.canvas.draw()
        fig.canvas.flush_events()

    await connect_and_interact_with_characteristic(device_id, CHARACTERISTIC_UUID)

# Run the main function
asyncio.run(main())
