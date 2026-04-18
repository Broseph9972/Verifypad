#include Serial.h

const int SDA_PIN = D5;
const int SCL_PIN = D6;

int currentDisplay = 0; // 0=home screen, 1=loading, 2=success, 3=failure, 4=disconnect

void updateDisplay() {

}

void otpPressed() {
  Serial.print("paste-otp");
  currentDisplay = 1
}

void linkPressed() {
  Serial.print("paste-link");
  currentDisplay = 1
}

void setup() {
  pinMode(SDA_PIN, OUTPUT);
  digitalWrite(SDA_PIN, HIGH);
}

void loop() {
  
}