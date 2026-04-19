#include "DEV_Config.h"
#include "OLED_0in49.h"
#include "GUI_Paint.h"
#include "fonts.h"
#include <string.h>

static UBYTE displayBuffer[OLED_0in49_WIDTH * OLED_0in49_HEIGHT / 8];
static char serialBuffer[24];
static uint8_t serialBufferLength = 0;

const String possibleMessages[] = {"pasted-otp", "pasted-link", "otp-paste-failed", "link-paste-failed"};
const int possibleMessagesCount = sizeof(possibleMessages) / sizeof(possibleMessages[0]);
int currentDisplay = 0; // 0=home screen, 1=loading, 2=success, 3=failure, 4=disconnect

void displayUpdater() {
  switch (currentDisplay) {
    case 0:
      displayUpdater("HOME");
      break;
    case 1:
      displayUpdater("LOADING");
      break;
    case 2:
      displayUpdater("SUCCESS");
      break;
    case 3:
      displayUpdater("FAILED");
      break;
    case 4:
      displayUpdater("OFFLINE");
      break;
    default:
      currentDisplay = 0;
      displayUpdater("HOME");
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

  return false;
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
  OLED_0in49_Init();
  Paint_NewImage(displayBuffer, OLED_0in49_WIDTH, OLED_0in49_HEIGHT, 0, WHITE);
  Paint_SelectImage(displayBuffer);
  displayUpdater(0);
}

void loop() {
  while (Serial.available() > 0) {
    char incoming = (char)Serial.read();

    if (serialBufferLength < sizeof(serialBuffer) - 1) {
      serialBuffer[serialBufferLength++] = incoming;
      serialBuffer[serialBufferLength] = '\0';
    } else {
      serialBufferLength = 0;
      serialBuffer[0] = '\0';
    }

    if (processIncomingMessage(serialBuffer)) {
      serialBufferLength = 0;
      serialBuffer[0] = '\0';
    }
  }
}