import serial
from pyfirmata import Arduino, SERVO
import time
import asyncio

# Arduino variables
SERVO_COM = "COM8"
SENSOR_COM = "COM9"
BAUD = 115200

# Gyro Data Storage
RECENT_0 = []
RECENT_1 = []
RECENT_2 = []

# Servo Pins (Digital)
ShoulderYaw = 2
ShoulderPitch = 4
ElbowPitch = 6
WristRoll = 8
ServoIDRef = [ShoulderYaw, ShoulderPitch, ElbowPitch, WristRoll]
ServoPosRef = [90, 90, 90, 90]

# =========================== FUNCTIONS =================================

def millis(seconds):
    return seconds / 1000

def clamp(val, minimum, maximum):
    return max(minimum, min(val, maximum))

def correctRelativeOrientation(mpuId, reading): # 0 - Yaw, 1 - Pitch, 2 - Roll
    global RECENT_0
    global RECENT_1
    global RECENT_2
    
    relSwitch = {
        0: reading,
        1: reading - RECENT_0[1],
        2: reading - RECENT_0[2]
    }

    return relSwitch.get(mpuId)

def resetServos():
    for i in range (len(ServoIDRef)):
        board.digital[ServoIDRef[i]].mode = SERVO
        board.digital[ServoIDRef[i]].write(90)

def alignServos():
    global RECENT_0
    global RECENT_1
    global RECENT_2
    global ServoPosRef

    for id in range (len(ServoIDRef)):
        mpuId = clamp(id - 1, 0, 2)

        readingSwitch = {
            0: RECENT_0[0],
            1: RECENT_0[1],
            2: RECENT_1[1],
            3: RECENT_2[2]
        }
        reading = readingSwitch.get(id)
        reading = correctRelativeOrientation(mpuId, reading)
        reading = clamp(reading+90, 0, 180)

        board.digital[ServoIDRef[id]].mode = SERVO
        board.digital[ServoIDRef[id]].write((reading - ServoPosRef[id]) / 2)
        ServoPosRef[id] = ((reading - ServoPosRef[id]) / 2)
    
    time.sleep(millis(15))

# =======================================================================

# God this is so poorly formatted i'm so sorry to anyone trying to read this

# ============================= MAIN ====================================

try:
    board = Arduino(SERVO_COM)
    buffer = serial.Serial(SENSOR_COM, BAUD)
    board.exit()
    buffer.close()
    board = Arduino(SERVO_COM)
    buffer = serial.Serial(SENSOR_COM, BAUD)
    buffer.timeout = 1

    resetServos()
except:
    print("Arduino board not plugged in! (Or not accessible on specified port)")
    time.sleep(5)
    quit()

def main():
    global RECENT_0
    global RECENT_1
    global RECENT_2

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

            if (gyroData[0] == ">0<"):
                RECENT_0 = [yaw, pitch, roll]
            elif (gyroData[0] == ">1<"):
                RECENT_1 = [yaw, pitch, roll]
            elif (gyroData[0] == ">2<"):
                RECENT_2 = [yaw, pitch, roll]
            
            try:
                alignServos()
            except Exception as e:
                print("WARNING: Exception raised in 'alignServos()' >>> " + str(e))
                
        else:
            print(data)

main()

# ==================================================================================