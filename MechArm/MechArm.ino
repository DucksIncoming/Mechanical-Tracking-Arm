#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

const int TCA_ADDRESS = 0x70;

Adafruit_MPU6050 mpu;
float yaw, pitch, roll;
float curTime, prevTime, deltaTime;

float GyroXError[3];
float GyroYError[3];
float GyroZError[3];

void TCA9548A(uint8_t bus){
  Wire.beginTransmission(TCA_ADDRESS);
  Wire.write(1 << bus);
  Wire.endTransmission();
  //Serial.print(bus);
}

void calibrateGyro(int gyroIndex, int depth) {
  Serial.println("Calibrating gyros...");
  Serial.println("WARNING: Moving the MPU6050 device while calibrating will result in incorrect behavior.");

  float Xreadings, Yreadings, Zreadings;

  // X Calibration
  for (int i = 0; i < depth; i++){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Xreadings += g.gyro.x;
    delay(3);
  }
  Serial.print(".");

  // Y Calibration
  for (int i = 0; i < depth; i++){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Yreadings += g.gyro.y;
    delay(3);
  }
  Serial.print(".");

  // Z Calibration
  for (int i = 0; i < depth; i++){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Zreadings += g.gyro.z;
    delay(3);
  }
  Serial.println(".");

  switch (gyroIndex) {
    case 0: {
      GyroXError[0] = Xreadings / depth;
      GyroYError[0] = Yreadings / depth;
      GyroZError[0] = Zreadings / depth;
      break;
    }
    case 1: {
      GyroXError[1] = Xreadings / depth;
      GyroYError[1] = Yreadings / depth;
      GyroZError[1] = Zreadings / depth;
      break;
    }
    case 2: {
      GyroXError[2] = Xreadings / depth;
      GyroYError[2] = Yreadings / depth;
      GyroZError[2] = Zreadings / depth;
      break;
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  for (int i = 0; i < 3; i++){
    TCA9548A(i);
    
    while (!mpu.begin()){
      Serial.println("No MPU6050 connected, or wiring is incorrect.");
      delay(10);
    }
    Serial.println("MPU6050 Found (" + String(i + 1) + "/3): Starting...");
  
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    calibrateGyro(i, 200); // Second argument is depth, keep high for accuracy.
    delay(100);
  }

  roll = 0;
  pitch = 0;
  yaw = 0;
  curTime = millis();
}

void loop() {
  for (int i = 0; i < 3; i++){
    TCA9548A(i);
    prevTime = curTime;
    curTime = millis();
    deltaTime = (curTime - prevTime) / 1000;
    
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
  
    roll += ((g.gyro.x - GyroXError[i]) * deltaTime) * (180/PI);
    pitch += ((g.gyro.y - GyroYError[i]) * deltaTime) * (180/PI);
    yaw += ((g.gyro.z - GyroZError[i]) * deltaTime) * (180/PI);

    Serial.print(">" + String(i) + "<");
    Serial.print(",");
    Serial.print(yaw);
    Serial.print(",");
    Serial.print(pitch);
    Serial.print(",");
    Serial.println(roll);
  
    delay(3);
  }
}
