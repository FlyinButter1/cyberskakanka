#include <Wire.h>

#define NUMBER_OF_WEIGHTS 4
#define I2C_ADDRESS       0x10

float values[NUMBER_OF_WEIGHTS];

void setup() {
  Wire.begin(I2C_ADDRESS);

  Wire.onRequest(requestEvent);

  Serial.begin(9600);
  Serial.println("Cyber!123");

}
void requestEvent() {
  Wire.write((uint8_t*)values, NUMBER_OF_WEIGHTS * sizeof(values[0]));
}

void loop() {
  for (int i = 0; i < NUMBER_OF_WEIGHTS; i++) {
    values[i] = analogRead(i);
  }
}




 
