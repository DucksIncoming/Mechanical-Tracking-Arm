#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

const int TCA_ADDRESS = 0x70;

Adafruit_MPU6050 mpu;
float yaw, pitch, roll;
float curTime, prevTime, deltaTime;

float GyroXError0 = 0;
float GyroYError0 = 0;
float GyroZError0 = 0;

float GyroXError1 = 0;
float GyroYError1 = 0;
float GyroZError1 = 0;

float GyroXError2 = 0;
float GyroYError2 = 0;
float GyroZError2 = 0;

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
    delay(5);
  }
  Serial.print(".");

  // Y Calibration
  for (int i = 0; i < depth; i++){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Yreadings += g.gyro.y;
    delay(5);
  }
  Serial.print(".");

  // Z Calibration
  for (int i = 0; i < depth; i++){
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Zreadings += g.gyro.z;
    delay(5);
  }
  Serial.println(".");

  switch (gyroIndex) {
    case 0: {
      GyroXError0 = Xreadings / depth;
      GyroYError0 = Yreadings / depth;
      GyroZError0 = Zreadings / depth;
      break;
    }
    case 1: {
      GyroXError1 = Xreadings / depth;
      GyroYError1 = Yreadings / depth;
      GyroZError1 = Zreadings / depth;
      break;
    }
    case 2: {
      GyroXError2 = Xreadings / depth;
      GyroYError2 = Yreadings / depth;
      GyroZError2 = Zreadings / depth;
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
  TCA9548A(0);
  prevTime = curTime;
  curTime = millis();
  deltaTime = (curTime - prevTime) / 1000;
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  roll += ((g.gyro.x - GyroXError0) * deltaTime) * (180/PI);
  pitch += ((g.gyro.y - GyroYError0) * deltaTime) * (180/PI);
  yaw += ((g.gyro.z - GyroZError0) * deltaTime) * (180/PI);

  Serial.print("Yaw: ");
  Serial.print(yaw);
  Serial.print(", Pitch: ");
  Serial.print(pitch);
  Serial.print(", Roll: ");
  Serial.print(roll);
  Serial.println(" deg");

  Serial.println("");
  delay(50);
}
