import serial
from pyfirmata import Arduino, SERVO
import time
import re

SERVO_COM = "COM8"
SENSOR_COM = "COM9"
BAUD = 115200

# Servo Pins (Digital)
ShoulderYaw = 4

try:
    board = Arduino(SERVO_COM)
    buffer = serial.Serial(SENSOR_COM, BAUD)
    board.exit()
    buffer.close()
    board = Arduino(SERVO_COM)
    buffer = serial.Serial(SENSOR_COM, BAUD)
    buffer.timeout = 1

    board.digital[ShoulderYaw].mode = SERVO
    board.digital[ShoulderYaw].write(90)
except:
    print("Arduino board not plugged in! (Or not accessible on specified port)")
    time.sleep(5)
    quit()

def clamp(val, minimum, maximum):
    return max(minimum, min(val, maximum))

def shoulderServos(yaw, pitch, roll): 
    pitch = clamp(pitch, 0, 180)
    board.digital[ShoulderYaw].mode = SERVO
    board.digital[ShoulderYaw].write(clamp((90 + yaw), 0, 200))

while True:
    buffer.flushInput()
    data = buffer.readline().decode('ascii')
    if (data.__contains__('>')):
        print("\n\n\n")
        print("=== GYROSCOPE DATA ===")
        gyroData = data.split(",")

        yaw = float(gyroData[1])
        pitch = float(gyroData[2])
        roll = float(gyroData[3])

        if (gyroData[0] == ">0<"):
            print("Yaw: " + str(yaw))
            print("Pitch: " + str(pitch))
            print("Roll: " + str(roll))
            print("======================")
            shoulderServos(int(yaw), int(pitch), int(roll))
    else:
        print(data)