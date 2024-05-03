import asyncio
from bleak import BleakScanner, BleakClient
import struct

data_points = []


def callback(sender: int, data: bytearray):
    print(f"Received data from {sender}: {data}")
    data_points.append(data)


async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

    device = "84:71:27:AC:20:D2"  # replace with your device's address
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")

        # replace with the UUID of the characteristic you want to read
        characteristic_uuid = "14181dce-eb95-46c5-8431-3b4fe0e0a12d"  
 
        ## imprimir dados primeiros recebidos 

        while client.is_connected:
            print("Connected: {client.is_connected}")
            services = await client.get_services()
            for service in services:
                for characteristic in service.characteristics:
                    if characteristic.uuid == characteristic_uuid:
                        print(characteristic.properties)

            data = await client.start_notify(characteristic_uuid, callback)
            print(data)


        # save the data in a file
            with open("dataTest.txt", "w") as f:
                for data in data_points:
                    f.write(str(data) + "\n")
            await asyncio.sleep(1)  # pause for a second before reading again

asyncio.run(main())