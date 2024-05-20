import asyncio
from bleak import BleakClient, BleakScanner

async def scan_and_print_services(device_id):
    async with BleakClient(device_id) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}")

async def main():
    device_id = "84:71:27:AC:20:D2"
    
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
    
    print(f"\nConnecting to device: {device_id}")
    await scan_and_print_services(device_id)

# Run the main function
asyncio.run(main())
