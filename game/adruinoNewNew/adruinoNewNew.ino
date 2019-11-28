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

int lastStateB = 0, lastStateA = 0, lastStateUp = 0, lastStateDown = 0, lastStateRight = 0, lastStateLeft = 0;
int lastStateB2 = 0, lastStateA2 = 0, lastStateUp2 = 0, lastStateDown2 = 0, lastStateRight2 = 0, lastStateLeft2 = 0;

int time = 0;

void action(int buttonPin, int onOff) {
  Serial.println(String(buttonPin) + "," + String(onOff));
  Serial.flush();
}
int checkState(int state, int buttonPin, int lastState) {
  state = digitalRead(buttonPin);
  //Serial.println("Data: " + String(state) +" " + String(lastState) + " " +String(buttonPin));

  if(lastState!=state){
    if (state == HIGH) {
      action(buttonPin, 1);
    }
    else{
      action(buttonPin, 0);
    }
    delay(50);
  }
  return state;


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

  delay(50);
  time += 1;



  Serial.flush();

  lastStateA = checkState(stateA, buttonPinA, lastStateA);
  lastStateB = checkState(stateB, buttonPinB, lastStateB);
  lastStateUp = checkState(stateUp, buttonPinUp, lastStateUp);
  lastStateDown = checkState(stateDown, buttonPinDown, lastStateDown);
  lastStateLeft = checkState(stateLeft, buttonPinLeft, lastStateLeft);
  lastStateRight = checkState(stateRight, buttonPinRight, lastStateRight);


  lastStateA2 = checkState(stateA2, buttonPinA2, lastStateA2);
  lastStateB2 = checkState(stateB2, buttonPinB2, lastStateB2);
  lastStateUp2 = checkState(stateUp2, buttonPinUp2, lastStateUp2);
  lastStateDown2 = checkState(stateDown2, buttonPinDown2, lastStateDown2);
  lastStateLeft2 = checkState(stateLeft2, buttonPinLeft2, lastStateLeft2);
  lastStateRight2 = checkState(stateRight2, buttonPinRight2, lastStateRight2);
}
