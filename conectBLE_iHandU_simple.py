import asyncio
import struct
from bleak import BleakClient, BleakScanner
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

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

force1 = []
force2 = []

# To keep track of the number of received notifications
notification_count = 0

async def notification_handler(sender, data):
    global notification_count

    # Assuming unpackedData is parsed from data, replace this with your actual parsing
    unpackedData = struct.unpack('55f', data)
    
    # Parse data as described in the provided organization
    ax1, ay1, az1 = unpackedData[0], unpackedData[1], unpackedData[2]
    ax2, ay2, az2 = unpackedData[11], unpackedData[12], unpackedData[13]
    ax3, ay3, az3 = unpackedData[22], unpackedData[23], unpackedData[24]
    ax4, ay4, az4 = unpackedData[33], unpackedData[34], unpackedData[35]
    ax5, ay5, az5 = unpackedData[44], unpackedData[45], unpackedData[46]

    # Append data to lists
    acceleration_x.extend([ax1, ax2, ax3, ax4, ax5])
    acceleration_y.extend([ay1, ay2, ay3, ay4, ay5])
    acceleration_z.extend([az1, az2, az3, az4, az5])
    
    # Parse data as described in the provided organization
    gx1, gy1, gz1 = unpackedData[3], unpackedData[4], unpackedData[5]
    gx2, gy2, gz2 = unpackedData[14], unpackedData[15], unpackedData[16]
    gx3, gy3, gz3 = unpackedData[25], unpackedData[26], unpackedData[27]
    gx4, gy4, gz4 = unpackedData[36], unpackedData[37], unpackedData[38]
    gx5, gy5, gz5 = unpackedData[47], unpackedData[48], unpackedData[49]

    # Append data to lists
    gyroscope_x.extend([gx1, gx2, gx3, gx4, gx5])
    gyroscope_y.extend([gy1, gy2, gy3, gy4, gy5])
    gyroscope_z.extend([gz1, gz2, gz3, gz4, gz5])


    mx1, my1, mz1 = unpackedData[6], unpackedData[7], unpackedData[8]
    mx2, my2, mz2 = unpackedData[17], unpackedData[18], unpackedData[19]
    mx3, my3, mz3 = unpackedData[28], unpackedData[29], unpackedData[30]
    mx4, my4, mz4 = unpackedData[39], unpackedData[40], unpackedData[41]
    mx5, my5, mz5 = unpackedData[50], unpackedData[51], unpackedData[52]

    magnetometer_x.extend([mx1, mx2, mx3, mx4, mx5])
    magnetometer_y.extend([my1, my2, my3, my4, my5])
    magnetometer_z.extend([mz1, mz2, mz3, mz4, mz5])

    
    f11, f12 = unpackedData[9], unpackedData[10]
    f21, f22 = unpackedData[20], unpackedData[21]
    f31, f32 = unpackedData[31], unpackedData[32]
    f41, f42 = unpackedData[42], unpackedData[43]
    f51, f52 = unpackedData[53], unpackedData[54]

    force1.extend([f11, f21, f31, f41, f51])
    force2.extend([f12, f22, f32, f42, f52])


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
                                    await asyncio.sleep(45)  # Listen for notifications for 30 seconds
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
    await connect_and_interact_with_characteristic(device_id, CHARACTERISTIC_UUID)

    # Set up the live plot
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

    def update_plot(frame):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        
        ax1.plot(acceleration_x, label='Acceleration X')
        ax2.plot(acceleration_y, label='Acceleration Y')
        ax3.plot(acceleration_z, label='Acceleration Z')
        
        ax1.legend(loc='upper right')
        ax2.legend(loc='upper right')
        ax3.legend(loc='upper right')

        # Define the file path
        csv_file = 'data.csv'

        # Combine the acceleration data into a list of tuples
        acceleration_data = list(zip(acceleration_x, acceleration_y, acceleration_z))
        gyroscope_data = list(zip(gyroscope_x, gyroscope_y, gyroscope_z))
        magnetometer_data = list(zip(magnetometer_x, magnetometer_y, magnetometer_z))
        force_data = list(zip(force1, force2))

        # Write the data to the CSV file
        with open("sim_acele.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Acceleration X', 'Acceleration Y', 'Acceleration Z'])  # Write the header
            writer.writerows(acceleration_data)  # Write the data rows

        # Write the data to the CSV file
        with open("sim_gyro.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Gyroscope X', 'Gyroscope Y', 'Gyroscope Z'])  # Write the header
            writer.writerows(gyroscope_data)  # Write the data rows

        with open("sim_magn.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Magnetometer X', 'Magnetometer Y', 'Magnetometer Z'])  # Write the header
            writer.writerows(magnetometer_data)  # Write the data rows

        with open("sim_force.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Force 1', 'Force 2'])  # Write the header
            writer.writerows(force_data)  # Write the data rows

    ani = FuncAnimation(fig, update_plot, interval=1000)
    plt.show()

# Run the main function
asyncio.run(main())
