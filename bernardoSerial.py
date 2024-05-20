import serial
import time

# Configure the serial connection to the Arduino
ser = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

if ser.is_open:
    print("Serial connection established.")
    

def move_shoulder(distance):
    if -100 <= distance <= 100:
        ser.write(f"{distance}\n".encode())
        time.sleep(0.1)  # Give the Arduino time to process the command
        if ser.in_waiting > 0:
            new_angle = ser.readline().decode().strip()
            print(f"New shoulder angle: {new_angle}")
    else:
        print("Distance must be between -100 and 100")

# Example usage
while True:
    try:
        distance = int(input("Enter distance (-100 to 100): "))
        move_shoulder(distance)
    except ValueError:
        print("Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\nExiting program.")
        break

ser.close()