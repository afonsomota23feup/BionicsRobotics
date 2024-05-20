import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
available_ports = [port.name for port in ports]
print(available_ports)