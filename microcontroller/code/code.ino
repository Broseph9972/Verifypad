#include Serial.h

const int SDA_PIN = D5;
const int SCL_PIN = D6;

const String possibleMessages[] = {"pasted-otp", "pasted-link", "otp-paste-failed", "link-paste-failed"};
const int possibleMessagesCount = sizeof(possibleMessages) / sizeof(possibleMessages[0]);
int currentDisplay = 0; // 0=home screen, 1=loading, 2=success, 3=failure, 4=disconnect

void displayUpdater() {
  switch (currentDisplay) {
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

void waitForMessage() {
  const unsigned long responseTimeoutMs = 25000;
  unsigned long startTime = millis();

  while (true) {
    String serialBuffer = ""
    if (Serial.available() > 0) {
      serialBuffer = Serial.readStringUntil('\n');
      serialBuffer.trim();

      for (int i = 0; i < possibleMessagesCount; i++) {
        if (serialBuffer == possibleMessages[i]) {
          if (serialBuffer == "pasted-otp" || serialBuffer == "pasted-link") {
            currentDisplay = 2;
          } else {
            currentDisplay = 3;
          }
          return;
        }
      }
    }

    if (millis() - startTime > responseTimeoutMs) {
      currentDisplay = 4;
      return;
    }

    delay(10);
  }
}

void otpPressed() {
  Serial.print("paste-otp");
  currentDisplay = 1
  waitForMessage()
  if(currentDisplay == 4) {
    return;
  }
  delay(5000)
  currentDisplay = 0
}

void linkPressed() {
  Serial.print("paste-link");
  currentDisplay = 1
  waitForMessage()
  if(currentDisplay == 4) {
    return;
  }
  delay(5000)
  currentDisplay = 0
}

void setup() {
  pinMode(SDA_PIN, OUTPUT);
  digitalWrite(SDA_PIN, HIGH);
  displayUpdater(0);
}

void loop() {
  
}