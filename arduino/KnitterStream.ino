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
#define NUM_BUTTONS 13
int button_pins[NUM_BUTTONS]  = {  13,  12,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   0 };
unsigned char button_cmds[NUM_BUTTONS] = { 'N', 'E', 'B', '-', '0', '3', '1', '5', '4', '9', '8', '>', 'A' };

void setup() {
  // set the pin mode
  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(button_pins[i], OUTPUT);
  }
  
  // setup our serial port
  Serial.begin(9600);
}

void loop(){
  // do we have data available?
  if (Serial.available() > 0) {
    // read the byte
    int incomingByte = Serial.read();
    
    // try to find the matching command and pin
    int found = -1;
    for (int i = 0; i < NUM_BUTTONS; i++) {
      if (button_cmds[i] == incomingByte) {
        // found it!
        found = button_pins[i];
        break;
      }
    }
    if (found == -1) {
      Serial.println("FAIL");
    } else {
      // press the button for 250ms
      digitalWrite(found, HIGH);
      delay(250);
      digitalWrite(found, LOW);
      Serial.print("OK: ");
      Serial.println(found);
    }
  }
}

// vim: set ft=c :
