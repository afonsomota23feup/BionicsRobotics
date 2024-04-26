import asyncio
from bleak import BleakScanner, BleakClient
import struct

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

    device = "60658457-ED22-63A5-86C6-0A3297A1D188"  # replace with your device's address
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")

        # replace with the UUID of the characteristic you want to read
        characteristic_uuid = "d9c7628ae98d-413db1a8-9e0fcb24b7e8"  
 
        ## imprimir dados primeiros recebidos 

        while client.is_connected:
            data = await client.read_gatt_char(characteristic_uuid)
            print(data)

            # # Parse accelerometer data
            # ax1, ay1, az1 = struct.unpack_from('fff', data, 0)
            # ax2, ay2, az2 = struct.unpack_from('fff', data, 44)
            # ax3, ay3, az3 = struct.unpack_from('fff', data, 88)
            # ax4, ay4, az4 = struct.unpack_from('fff', data, 132)
            # ax5, ay5, az5 = struct.unpack_from('fff', data, 176)

            # print(f"Accelerometer Data: {ax1}, {ay1}, {az1}, {ax2}, {ay2}, {az2}, {ax3}, {ay3}, {az3}, {ax4}, {ay4}, {az4}, {ax5}, {ay5}, {az5}")

            await asyncio.sleep(1)  # pause for a second before reading again

asyncio.run(main())