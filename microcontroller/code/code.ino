const int SDA_PIN = D5;
const int SCL_PIN = D6;

int currentDisplay = 0; // 0=home screen, 1=loading, 2=success, 3=failure, 4=disconnect

void displayUpdater(int displayToShow) {
  currentDisplay = displayToShow;

  switch (displayToShow) {
    case 0:
      Serial.println("home");
      break;
    case 1:
      Serial.println("loading");
      break;
    case 2:
      Serial.println("success");
      break;
    case 3:
      Serial.println("failure");
      break;
    case 4:
      Serial.println("disconnect");
      break;
    default:
      Serial.println("home");
      currentDisplay = 0;
      break;
  }
}

void otpPressed() {
  Serial.print("paste-otp");
  displayUpdater(1);
}

void linkPressed() {
  Serial.print("paste-link");
  displayUpdater(1);
}

void setup() {
  pinMode(SDA_PIN, OUTPUT);
  digitalWrite(SDA_PIN, HIGH);
  displayUpdater(0);
}

void loop() {
  
}