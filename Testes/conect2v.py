import asyncio
import struct
from bleak import BleakClient, BleakScanner

DATA_LENGTH = 220  # 4 bytes for each of the 54 values
data_points = []

async def callback(sender, data):
    data_points.append(data)

def process_data(data):
    return struct.unpack('<' + 'f' * 54, data)

async def connect_to_device(device_id, device_uuid):
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        
    async with BleakClient(device_id) as client:
        try:
            await client.connect()
            print(f"Connected to device: {device_id}")

            await client.start_notify(device_uuid, callback)
            print(f"Start notify for device: {device_uuid}")

            await asyncio.sleep(60)
            await client.stop_notify(device_uuid)
            print(f"Stop notify for device: {device_uuid}")

        except Exception as e:
            print(f"Failed to connect to device: {device_uuid}, Error: {e}")

async def main():
    device_id = "84:71:27:AC:20:D2"
    device_uuid = "14181dce-eb95-46c5-8431-3b4fe0e0a12d"
    
    await connect_to_device(device_id, device_uuid)

    with open("data.txt", "w") as f:
        for data in data_points:
            f.write(str(data) + "\n")

if __name__ == "__main__":
    for i in range(5):  # Adjust the range as needed
        asyncio.run(main())
