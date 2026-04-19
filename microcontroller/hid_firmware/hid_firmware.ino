#include <Keyboard.h>

// Hardware mapping from the PCB:
// SW2 -> D8 (active low to GND)
// SW1 -> D9 (active low to GND)
const int BUTTON_1_PIN = D8;
const int BUTTON_2_PIN = D9;

const unsigned long DEBOUNCE_MS = 5;

struct Button {
  int pin;
  bool stablePressed;
  bool lastRawPressed;
  unsigned long lastChangeMs;
};

Button button1 = {BUTTON_1_PIN, false, false, 0};
Button button2 = {BUTTON_2_PIN, false, false, 0};

void sendMacro1() {
  Keyboard.write(KEY_UP_ARROW);
}

void sendMacro2() {
  Keyboard.write(KEY_UP_ARROW);
}

void handleButton(Button &button, void (*onPressed)()) {
  bool rawPressed = (digitalRead(button.pin) == LOW);
  unsigned long now = millis();

  if (rawPressed != button.lastRawPressed) {
    button.lastRawPressed = rawPressed;
    button.lastChangeMs = now;
  }

  if ((now - button.lastChangeMs) >= DEBOUNCE_MS && rawPressed != button.stablePressed) {
    button.stablePressed = rawPressed;

    // Fire only once on press edge (not continuously while held).
    if (button.stablePressed) {
      onPressed();
    }
  }
}

void setup() {
  pinMode(BUTTON_1_PIN, INPUT_PULLUP);
  pinMode(BUTTON_2_PIN, INPUT_PULLUP);

  Keyboard.begin();
}

void loop() {
  handleButton(button1, sendMacro1);
  handleButton(button2, sendMacro2);
}
