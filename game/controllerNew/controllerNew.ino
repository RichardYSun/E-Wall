// Create a controller

// SEND TO SERIAL
// SEND PRESS AND RELEASE NUMBERS

// Declaring pin states, Change to whatever connections are used
const int buttonPinUp = 2;
const int buttonPinRight = 3;
const int buttonPinDown = 4;
const int buttonPinLeft = 5;
const int buttonPinA = 6; // Bottom
const int buttonPinB = 7; // Right
const int buttonPinX = 8; // Left
const int buttonPinY = 9; // Up

int stateX = 0, stateY = 0, stateB = 0, stateA = 0, stateUp = 0, stateDown = 0, stateRight = 0, stateLeft = 0;

int time = 0;

void action(int buttonPin, int onOff) {
  Serial.println(String(buttonPin) + "," + String(onOff));
  Serial.flush();
}
void checkState(int state, int buttonPin) {
  state = digitalRead(buttonPin);

  if (state == HIGH) {
    action(buttonPin, 1);
  }
  else{
    action(buttonPin, 0);
  }
}
void setup() {
  // Setting everything as input.
  Serial.begin(9600);
  pinMode(buttonPinUp, INPUT);
  pinMode(buttonPinDown, INPUT);
  pinMode(buttonPinLeft, INPUT);
  pinMode(buttonPinRight, INPUT);
  pinMode(buttonPinA, INPUT);
  pinMode(buttonPinB, INPUT);
  pinMode(buttonPinX, INPUT);
  pinMode(buttonPinY, INPUT);

}


// Loops for each of the buttons
void loop() {
  // Sends the state to a function,  Makes it more readable

  delay(1000);
  time += 1;



  Serial.flush();
  //checkState(stateX, buttonPinX);
  //checkState(stateY, buttonPinY);
  //checkState(stateA, buttonPinA);
  //checkState(stateB, buttonPinB);
   checkState(stateUp, buttonPinUp);
  //checkState(stateDown, buttonPinDown);
  //checkState(stateLeft, buttonPinLeft);
  //checkState(stateRight, buttonPinRight);

}
