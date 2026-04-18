#include "DEV_Config.h"
#include "OLED_0in49.h"
#include "GUI_Paint.h"
#include "fonts.h"
#include <string.h>

static UBYTE displayBuffer[OLED_0in49_WIDTH * OLED_0in49_HEIGHT / 8];
static char serialBuffer[24];
static uint8_t serialBufferLength = 0;

int currentDisplay = 0; // 0=home screen, 1=loading, 2=success, 3=failure, 4=disconnect

void displayUpdater(const char *message) {
  Paint_SelectImage(displayBuffer);
  Paint_Clear(WHITE);

  int messageWidth = strlen(message) * Font8.Width;
  int x = 0;
  if (messageWidth < OLED_0in49_WIDTH) {
    x = (OLED_0in49_WIDTH - messageWidth) / 2;
  }

  int y = (OLED_0in49_HEIGHT - Font8.Height) / 2;
  Paint_DrawString_EN(x, y, message, &Font8, BLACK, WHITE);
  OLED_0in49_Display_RAM(displayBuffer);
}

void displayUpdater(int displayToShow) {
  currentDisplay = displayToShow;

  switch (displayToShow) {
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

bool processIncomingMessage(const char *message) {
  if (strcmp(message, "pasted-otp") == 0 || strcmp(message, "pasted-link") == 0) {
    displayUpdater(2);
    return true;
  } else if (strcmp(message, "otp-paste-failed") == 0 || strcmp(message, "link-paste-failed") == 0) {
    displayUpdater(3);
    return true;
  } else if (strcmp(message, "disconnect") == 0) {
    displayUpdater(4);
    return true;
  }

  return false;
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