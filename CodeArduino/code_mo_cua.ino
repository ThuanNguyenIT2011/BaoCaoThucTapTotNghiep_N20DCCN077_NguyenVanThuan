#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <ESP32Servo.h>
static const int servoPin = 13;

Servo servo1;

const char* ssid = "nvt";
const char* pass  = "12345678";
FirebaseAuth auth;
FirebaseConfig firebaseConfig;
FirebaseData fbdo;
#include "DHT.h"

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, pass);
  WiFi.setSleep(false);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  Serial.println("Wifi connected");
  firebaseConfig.api_key = "AIzaSyAI-PPSS1T77n-pnP00Vy-60HL2t5IuaqU";
  firebaseConfig.host = "https://nhanthongminh-9fb6f-default-rtdb.asia-southeast1.firebasedatabase.app";
  auth.user.email = "nguyenvanthuan20112002@gmail.com";
  auth.user.password = "thuanbeo2k2@";

  Firebase.begin(&firebaseConfig, &auth);

  if(Firebase.ready()) {
    Serial.println("Connected to Firebase");
  } else {
    Serial.println("Failed to connect to Firebase");
  }
  servo1.attach(servoPin);
}

void loop() {
  if(Firebase.RTDB.getBool(&fbdo, "/predict_door")) {
    if (fbdo.boolData() == true) {
      for(int posDegrees = 0; posDegrees <= 90; posDegrees++) {
        servo1.write(posDegrees);
        Serial.println(posDegrees);
        delay(20);
      }
      delay(5000);
      for(int posDegrees = 90; posDegrees >= 0; posDegrees--) {
        servo1.write(posDegrees);
        Serial.println(posDegrees);
        delay(20);
      }
    } else {
      servo1.write(0);
    }
    delay(1000);
  }
}