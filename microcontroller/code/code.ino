#include "DEV_Config.h"
#include "OLED_0in49.h"
#include "GUI_Paint.h"
#include "fonts.h"
#include "ImageData.h"
#include <avr/pgmspace.h>
#include <string.h>

static UBYTE displayBuffer[OLED_0in49_WIDTH * OLED_0in49_HEIGHT / 8];
static UBYTE imageBuffer[OLED_0in49_WIDTH * OLED_0in49_HEIGHT / 8];
const String possibleMessages[] = {"pasted-otp", "pasted-link", "otp-paste-failed", "link-paste-failed"};
const int possibleMessagesCount = sizeof(possibleMessages) / sizeof(possibleMessages[0]);
int currentDisplay = 0; // 0=home screen, 1=loading, 2=success, 3=failure, 4=disconnect

const int otpPin = D9;
const int linkPin = D8;

void writeText(const char *text) {
  Paint_Clear(WHITE);
  Paint_DrawString_EN(0, 0, text, &Font12, BLACK, WHITE);
  OLED_0in49_Display(displayBuffer);
}

void writeImage(const unsigned char *image) {
  memcpy_P(imageBuffer, image, sizeof(imageBuffer));
  Paint_Clear(WHITE);
  Paint_DrawBitMap(imageBuffer);
  OLED_0in49_Display(displayBuffer);
}

void drawLoadingDots() {
  Paint_Clear(WHITE);

  const int centerX = OLED_0in49_WIDTH / 2;
  const int centerY = (OLED_0in49_HEIGHT / 2) - 6;
  const int dotSpacing = 8;
  const int startX = centerX - dotSpacing;

  unsigned long frame = (millis() / 250) % 6;
  int dotsOn = (frame < 3) ? (frame + 1) : (5 - frame);

  for (int i = 0; i < 3; i++) {
    Paint_DrawString_EN(startX + (i * dotSpacing), centerY, (i < dotsOn) ? "." : " ", &Font12, BLACK, WHITE);
  }

  OLED_0in49_Display(displayBuffer);
}

void displayUpdater() {
  switch (currentDisplay) {
    case 0:
      writeImage(bitmap_home);
      break;
    case 1:
      drawLoadingDots();
      break;
    case 2:
      writeImage(bitmap_success);
      break;
    case 3:
      writeImage(bitmap_error);
      break;
    case 4:
      writeText("DISCONNECTED");
      break;
    default:
      currentDisplay = 0;
      writeImage(bitmap_home);
      break;
  }
}

void waitForMessage() {
  const unsigned long responseTimeoutMs = 25000;
  unsigned long startTime = millis();
  unsigned long lastAnimUpdate = 0;

  while (true) {
    String serialBuffer = "";
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

    if (currentDisplay == 1 && millis() - lastAnimUpdate >= 250) {
      displayUpdater();
      lastAnimUpdate = millis();
    }

    delay(10);
  }
}

void otpPressed() {
  Serial.print("paste-otp");
  currentDisplay = 1;
  displayUpdater();
  waitForMessage();
  if (currentDisplay == 4) {
    return;
  }
  delay(5000);
  currentDisplay = 0;
  displayUpdater();
}

void linkPressed() {
  Serial.print("paste-link");
  currentDisplay = 1;
  displayUpdater();
  waitForMessage();
  if (currentDisplay == 4) {
    return;
  }
  delay(5000);
  currentDisplay = 0;
  displayUpdater();
}

void setup() {
  pinMode(linkPin, INPUT);
  pinMode(otpPin, INPUT);
  OLED_0in49_Init();
  Paint_NewImage(displayBuffer, OLED_0in49_WIDTH, OLED_0in49_HEIGHT, 0, WHITE);
  Paint_SelectImage(displayBuffer);
  Serial.begin(9600);
  displayUpdater();
}

void loop() {
  if(digitalRead(otpPin) == HIGH) {
    while(digitalRead(otpPin) == HIGH) {
      delay(50);
    }
    otpPressed();
  }
  if(digitalRead(linkPin) == HIGH) {
    while(digitalRead(linkPin) == HIGH) {
      delay(50);
    }
    linkPressed();
  }
}