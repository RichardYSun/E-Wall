// Create a controller

// SEND TO SERIAL
// SEND PRESS AND RELEASE NUMBERS

// Declaring pin states, Change to whatever connections are used
const int buttonPinUp = 2;
const int buttonPinRight = 3;
const int buttonPinDown = 4;
const int buttonPinLeft = 5;
const int buttonPinA = 6; // 
const int buttonPinB = 7; // 

const int buttonPinUp2 = 8;
const int buttonPinRight2 = 9;
const int buttonPinDown2 = 10;
const int buttonPinLeft2 = 11;
const int buttonPinA2 = 12; // 
const int buttonPinB2 = 13; // 



int stateB = 0, stateA = 0, stateUp = 0, stateDown = 0, stateRight = 0, stateLeft = 0;
int stateB2 = 0, stateA2 = 0, stateUp2 = 0, stateDown2 = 0, stateRight2 = 0, stateLeft2 = 0;

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

  pinMode(buttonPinUp2, INPUT);
  pinMode(buttonPinDown2, INPUT);
  pinMode(buttonPinLeft2, INPUT);
  pinMode(buttonPinRight2, INPUT);
  pinMode(buttonPinA2, INPUT);
  pinMode(buttonPinB2, INPUT);
}


// Loops for each of the buttons
void loop() {
  // Sends the state to a function,  Makes it more readable

  delay(0);
  time += 1;



  Serial.flush();

  checkState(stateA, buttonPinA);
  checkState(stateB, buttonPinB);
  checkState(stateUp, buttonPinUp);
  checkState(stateDown, buttonPinDown);
  checkState(stateLeft, buttonPinLeft);
  checkState(stateRight, buttonPinRight);


  checkState(stateA2, buttonPinA2);
  checkState(stateB2, buttonPinB2);
  checkState(stateUp2, buttonPinUp2);
  checkState(stateDown2, buttonPinDown2);
  checkState(stateLeft2, buttonPinLeft2);
  checkState(stateRight2, buttonPinRight2);
}
