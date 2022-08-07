import serial
from pyfirmata import Arduino, SERVO
import time
import re

SERVO_COM = "COM8"
SENSOR_COM = "COM9"
BAUD = 115200

# Servo Pins (Digital)
ShoulderPitch = 2
ShoulderYaw = 3
ElbowPitch = 4
WristRoll = 5

try:
    board = Arduino(SERVO_COM)
    buffer = serial.Serial(SENSOR_COM, BAUD)

    board.exit()
    buffer.close()

    board = Arduino(SERVO_COM)
    buffer = serial.Serial(SENSOR_COM, BAUD)

    buffer.timeout = 1
except:
    print("Arduino board not plugged in! (Or not accessible on specified port)")
    time.sleep(5)
    quit()

memory = 0

def clamp(val, minimum, maximum):
    return max(minimum, min(val, maximum))

def shoulderServos(yaw, pitch, roll):
    global memory
    
    yaw = clamp(yaw, 0, 180)
    pitch = clamp(pitch, 0, 180)
    roll = clamp(roll, 0, 180)

    print(memory)
    print(pitch)
    memory = pitch

    board.digital[ShoulderYaw].mode = SERVO
    board.digital[ShoulderPitch].mode = SERVO

    board.digital[ShoulderPitch].write(pitch)

    time.sleep(0.1)

def elbowServos(yaw, pitch, roll):
    board.digital[ElbowPitch].mode = SERVO

def wristServos(yaw, pitch, roll):
    board.digital[WristRoll].mode = SERVO

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

        shoulderServos(int(yaw), int(pitch), int(roll))