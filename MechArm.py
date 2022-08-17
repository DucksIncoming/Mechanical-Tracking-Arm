import serial
from pyfirmata import Arduino, SERVO
import time
import re

SERVO_COM = "COM8"
SENSOR_COM = "COM9"
BAUD = 115200

# Servo Pins (Digital)
ShoulderYaw = 4
ShoulderPitch = 5
ElbowPitch = 6
WristRoll = 7
ServoIDRef = [ShoulderYaw, ShoulderPitch, ElbowPitch, WristRoll]

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

def alignServo(id, reading): 
    reading = clamp(reading + 90, 0, 180)
    board.digital[ServoIDRef[id]].mode = SERVO
    board.digital[ServoIDRef[id]].write(reading)

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

        print("Yaw: " + str(yaw))
        print("Pitch: " + str(pitch))
        print("Roll: " + str(roll))
        print("======================")
        #shoulderServos(int(yaw), int(pitch), int(roll))

        if (gyroData[0] == ">0<"):
            alignServo(0, yaw)
            alignServo(1, pitch)
        elif (gyroData[0] == ">1<"):
            alignServo(2, yaw)
        elif (gyroData[0] == ">2<"):
            alignServo(3, roll)
            
    else:
        print(data)