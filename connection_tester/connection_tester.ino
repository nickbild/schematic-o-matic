uint8_t bottom_row[31];
uint8_t top_row[31];
uint8_t vcc;
uint8_t gnd;

bool found;

void setup() {
  Serial.begin(115200);

  // Pin definitions. X_row[breadboardColumn] = pin
  bottom_row[30] = 22;
  bottom_row[29] = 24;
  bottom_row[28] = 26;
  bottom_row[27] = 28;
  bottom_row[26] = 30;
  bottom_row[25] = 32;
  bottom_row[24] = 34;
  bottom_row[23] = 36;
  bottom_row[22] = 38;
  bottom_row[21] = 40;
  bottom_row[20] = 42;
  bottom_row[19] = 44;
  bottom_row[18] = 46;
  bottom_row[17] = 48;
  bottom_row[16] = 50;
  bottom_row[15] = 52;
  bottom_row[14] = A11;
  bottom_row[13] = A10;

  top_row[30] = 23;
  top_row[29] = 25;
  top_row[28] = 27;
  top_row[27] = 29;
  top_row[26] = 31;
  top_row[25] = 33;
  top_row[24] = 35;
  top_row[23] = 37;
  top_row[22] = 39;
  top_row[21] = 41;
  top_row[20] = 43;
  top_row[19] = 45;
  top_row[18] = 47;
  top_row[17] = 49;
  top_row[16] = 51;
  top_row[15] = 53;
  top_row[14] = 21;
  top_row[13] = 20;

  vcc = 14;
  gnd = 16;
  
//  pinMode(22, OUTPUT);
//  pinMode(20, INPUT_PULLUP);
//
//  digitalWrite(22, LOW);

}

void loop() {
  // Check top columns of breadboard.
  Serial.println("TOP");
  // Loop through each column as an originating point.
  for (uint8_t test_c=30; test_c>=13; test_c--) {
    clearAllPins();
    
    Serial.print(test_c);
    Serial.print(":");
    
    pinMode(top_row[test_c], OUTPUT);
    digitalWrite(top_row[test_c], LOW);

    // Is it connected to VCC or GND?
    pinMode(vcc, INPUT_PULLUP);
    if (digitalRead(vcc) == LOW) {
      Serial.println("P;");
      continue;
    }
    
    pinMode(gnd, INPUT_PULLUP);
    if (digitalRead(gnd) == LOW) {
      Serial.println("G;");
      continue;
    }
    
    // Check originating point against all other columns on top (except itself).
    found = false;
    for (uint8_t top_c=30; top_c>=13; top_c--) {
      if (test_c == top_c) { continue; }

      pinMode(top_row[top_c], INPUT_PULLUP);
      // Electrical continuity detected.
      if (digitalRead(top_row[top_c]) == LOW) {
        if (found) { Serial.print(","); }
        Serial.print(top_c);
        found = true;
      }

    }

    Serial.print(";");
    
    // Check originating point against all other columns on bottom.
    found = false;
    for (uint8_t bottom_c=30; bottom_c>=13; bottom_c--) {
      // Electrical continuity detected.
      pinMode(bottom_row[bottom_c], INPUT_PULLUP);
      if (digitalRead(bottom_row[bottom_c]) == LOW) {
        if (found) { Serial.print(","); }
        Serial.print(bottom_c);
        found = true;
      }
    }

    Serial.println("");
  }




  // Check bottom columns of breadboard.
  Serial.println("BOTTOM");
  // Loop through each column as an originating point.
  for (uint8_t test_c=30; test_c>=13; test_c--) {
    clearAllPins();
    
    Serial.print(test_c);
    Serial.print(":");
    
    pinMode(bottom_row[test_c], OUTPUT);
    digitalWrite(bottom_row[test_c], LOW);

    // Is it connected to VCC or GND?
    pinMode(vcc, INPUT_PULLUP);
    if (digitalRead(vcc) == LOW) {
      Serial.println("P;");
      continue;
    }
    
    pinMode(gnd, INPUT_PULLUP);
    if (digitalRead(gnd) == LOW) {
      Serial.println("G;");
      continue;
    }
    
    // Check originating point against all other columns on top (except itself).
    found = false;
    for (uint8_t top_c=30; top_c>=13; top_c--) {
      if (test_c == top_c) { continue; }

      pinMode(top_row[top_c], INPUT_PULLUP);
      // Electrical continuity detected.
      if (digitalRead(top_row[top_c]) == LOW) {
        if (found) { Serial.print(","); }
        Serial.print(top_c);
        found = true;
      }

    }

    Serial.print(";");
    
    // Check originating point against all other columns on bottom.
    found = false;
    for (uint8_t bottom_c=30; bottom_c>=13; bottom_c--) {
      // Electrical continuity detected.
      pinMode(bottom_row[bottom_c], INPUT_PULLUP);
      if (digitalRead(bottom_row[bottom_c]) == LOW) {
        if (found) { Serial.print(","); }
        Serial.print(bottom_c);
        found = true;
      }
    }

    Serial.println("");
  }


  

  while(true){}
}

void clearAllPins() {
  for (uint8_t test_c=30; test_c>=13; test_c--) {
    pinMode(top_row[test_c], INPUT_PULLUP);
    pinMode(bottom_row[test_c], INPUT_PULLUP);
  }

  pinMode(vcc, INPUT_PULLUP);
  pinMode(gnd, INPUT_PULLUP);
}
