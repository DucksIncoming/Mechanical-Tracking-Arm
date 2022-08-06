import serial
import time
import re

COM = "COM9"
BAUD = 115200

buffer = serial.Serial(COM, BAUD)
buffer.timeout = 1


while True:
    buffer.flushInput()
    data = buffer.readline().decode('ascii')
    if (data.__contains__('ypr')):
        print("\n\n\n")
        print("=== GYROSCOPE DATA ===")
        gyroData = re.split(r'\t+', data)
        yaw = float(gyroData[1])
        pitch = float(gyroData[2])
        roll = float(gyroData[3])
        print("Yaw: " + str(yaw))
        print("Pitch: " + str(pitch))
        print("Roll: " + str(roll))
        print("======================")