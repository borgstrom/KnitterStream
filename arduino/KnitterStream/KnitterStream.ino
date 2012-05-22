//
// KnitterStream Arduino Code
// Author: Evan Borgstrom <evan@fatbox.ca>
//

// map our button pins & commands
// most are straight forward, here are the special cases
// N = NO
// E = ENT
// B = blank
// > = >>> (three arrows, start)
// A = ABC
//
// G = GO/STOP motor control
// C = Colour motor control
// S = Switch direction motor contorl
// O = One time motor control
//
// T = toggle switch (this is a special case)

// first handle the buttons that are hooked up to a cd4067b multiplexer
// mio == multiplexed I/O

#define MIO_PIN 12
const int mio_channels[] = { 8, 9, 10, 11 };

#define MIO_BUTTONS 13
const int mio_pins[MIO_BUTTONS]           = {  0,   1,   2,    3,   4,   5,   6,   7,   8,   9,  10,  11,  12 };
const unsigned char mio_cmds[MIO_BUTTONS] = { 'N', 'E', 'B', '-', '0', '3', '1', '5', '4', '9', '8', '>', 'A' };

#define ANALOG_BUTTONS 4
const int analog_pins[ANALOG_BUTTONS]          = {  14,  15,  16,  17 };
const unsigned char analog_cmds[ANALOG_BUTTONS] = { 'G', 'C', 'S', 'O' };

// motor control pins
#define M1_PWM 5
#define M1_DIR 4

void setup() {
  // set the pin mode
  int i;

  // the io pins on the cd4067b
  for (i = 8; i <= 12; i++) {
    pinMode(i, OUTPUT);
  }

  // the analog pins
  for (i = 14; i <= 17; i++) {
    pinMode(i, OUTPUT);
  }
  
  // motor pins
  pinMode(M1_PWM, OUTPUT);
  pinMode(M1_DIR, OUTPUT);
  
  // setup our serial port
  Serial.begin(9600);
}

int toggle_dir = 2;

void toggle_switch() {
  Serial.print("Toggling switch: ");
  if (toggle_dir == 1) {
    Serial.println("Forward");
    digitalWrite(M1_DIR, LOW);
    analogWrite(M1_PWM, 254);
    delay(3750);
    toggle_dir = 2;
  } else {
    Serial.println("Reverse");
    digitalWrite(M1_DIR, HIGH);
    analogWrite(M1_PWM, 1);
    delay(3750);
    toggle_dir = 1;
  }
  
  digitalWrite(M1_PWM, LOW);
  digitalWrite(M1_DIR, LOW);
  
  Serial.println("Done!");
}

void loop() {
  // do we have data available?
  if (Serial.available() > 0) {
    // read the byte
    int incomingByte = Serial.read();

    // handle our special case
    // toggling the switch
    if (incomingByte == 'T') {
        toggle_switch();
        return;
    }
    
    // try to find the matching command and pin
    int found = -1;
    int i;
    
    // first check the multiplexed IO
    for (i = 0; i < MIO_BUTTONS; i++) {
      if (mio_cmds[i] == incomingByte) {
        Serial.print("MIO Channel #");
        Serial.print(mio_pins[i]);
        Serial.print(" - ");
        
        // now set the correct output channel
        digitalWrite(8, mio_pins[i] & 1);
        digitalWrite(9, (mio_pins[i] >> 1) & 1);
        digitalWrite(10, (mio_pins[i] >> 2) & 1);
        digitalWrite(11, (mio_pins[i] >> 3) & 1);

        // and set found to the common io pin
        found = MIO_PIN;
        break;
      }
    }
    
    if (found == -1) {
      // now try analog
      for (i = 0; i < ANALOG_BUTTONS; i++) {
        if (analog_cmds[i] == incomingByte) {
          found = analog_pins[i];
          Serial.print("Analog Pin #");
          Serial.print(analog_pins[i]);
          Serial.print(" - ");
          break;
        }
      }
    }
    
    if (found == -1) {
      Serial.println("FAIL");
    } else {
      // press the button for 250ms
      digitalWrite(found, HIGH);
      delay(250);
      digitalWrite(found, LOW);
      Serial.println("OK");
    }
  }
}

// vim: set ft=c :
