/*
  Movement-Tracking Mech Arm by DucksIncoming
  v1.0
  https://github.com/DucksIncoming/Mechanical-Tracking-Arm
  https://www.youtube.com/channel/UCwgpVWzXKdMB-kHblUzMsLg
 */

#include <Wire.h>
#include <MPU6050.h>

/* ============= ! PLEASE NOTE ! ====================
  This program uses a modified version of the
  Arduino-MPU6050 library, originally obtained
  from https://github.com/jarzebski/Arduino-MPU6050.
  This was just the easiest way to do this, just
  make sure you either download the modified library
  from my GitHub repo or change the MPU6050_ADDRESS
  variable to 0x70 instead of 0x68, or whatever the
  I2C address of your TCA9548A or equivalent is.
===================================================== */

MPU6050 mpu;

unsigned long timer = 0;
float timeStep = 0.01;

// Pitch, Roll and Yaw values
float pitch = 0;
float roll = 0;
float yaw = 0;

void TCA9548A(uint8_t bus){
  Wire.beginTransmission(0x70);
  Wire.write(1 << bus);
  Wire.endTransmission();
  Serial.print(bus);
}

void setup() 
{
  TCA9548A(1);
  Serial.begin(115200);
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  mpu.calibrateGyro();
  mpu.setThreshold(3);
}

void loop()
{
  TCA9548A(1);
  timer = millis();
  Vector norm = mpu.readNormalizeGyro();
  pitch = pitch + norm.YAxis * timeStep;
  roll = roll + norm.XAxis * timeStep;
  yaw = yaw + norm.ZAxis * timeStep;

  Serial.print(" Pitch = ");
  Serial.print(pitch);
  Serial.print(" Roll = ");
  Serial.print(roll);  
  Serial.print(" Yaw = ");
  Serial.println(yaw);

  delay((timeStep*1000) - (millis() - timer));
}
