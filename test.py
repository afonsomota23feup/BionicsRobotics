import asyncio
from bleak import BleakClient
import matplotlib.pyplot as plt

data_points = []

def callback(sender, data):
     # Convert the data to bytes if it's not already
    if isinstance(data, str):
        data = bytes.fromhex(data)

    # Convert each bytearray to a decimal number
    decimal_data = int.from_bytes(data, 'big')

    # Append the values to data_points
    data_points.append(decimal_data)


async def connect_to_device(device_id, device_uuid):
    client = BleakClient(device_id)
    try:
        await client.connect()
        print(f"Connected to device: {device_id}")

        await client.start_notify(device_uuid, callback)

        # Collect data for 60 seconds
        for _ in range(60):
            if not client.is_connected:
                break
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Failed to connect to device: {device_uuid}, Error: {e}")
    finally:
        await client.stop_notify(device_uuid)
        await client.disconnect()

async def main():
    device_id = "C9:4B:17:0B:28:09"
    device_uuid = "00002A37-0000-1000-8000-00805F9B34FB"
    
    await connect_to_device(device_id, device_uuid)

    print(data_points); #print the data collected

    # save the data in a file
    with open("data.txt", "w") as f:
        for data in data_points:
            f.write(str(data) + "\n")

asyncio.run(main())