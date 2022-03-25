#define NBR_SERVOS 16
#define NBR_POINT_BUTTONS 12

int ledpins[][2] = { {10,11},
                    {46,45},
                    {33,34},
                    {52,53},
                    {8,23},
                    {-1,-1},
                    {31,30},
                    {24,25},
                    {36,41},
                    {27,29},
                    {49,39},
                    {44,50} };                    

int ledpins_tri[] = {35,43,51};

int button_pins[] = {9,48,42,7,22,40,32,26,37,28,47,6,38};

const int NBR_POINT_BUTTONS = 12;
const int flash_wait = 50;

int servo_point = [0,1,2,3,3,4,5,5,5,6,6,7,8,9,10,11]; //defines which point a particular servo is changing.
int point_state[NBR_POINT_BUTTONS];
int servo_state[NBR_SERVOS]; //either 1 or 0

int i = 0;

int buttonState[NBR_POINT_BUTTONS+1];        // the current reading from the input pin
int lastButtonState[NBR_POINT_BUTTONS+1];   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime[NBR_POINT_BUTTONS+1];  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers
unsigned long previousMillis = 0;        // will store last time LED was updated

String inputString = "";

void setup() {
 
  // set the digital pin as output:
  for(i=0; i<NBR_POINT_BUTTONS; i++){
    pinMode(ledpins[i][0], OUTPUT);
    digitalWrite(ledpins[i][0], LOW);

    pinMode(ledpins[i][1], OUTPUT);
    digitalWrite(ledpins[i][1], LOW);

    pinMode(ledpins_tri[0], OUTPUT);
    digitalWrite(ledpins_tri[0], LOW);
    pinMode(ledpins_tri[1], OUTPUT);
    digitalWrite(ledpins_tri[1], LOW);
    pinMode(ledpins_tri[2], OUTPUT);
    digitalWrite(ledpins_tri[2], LOW);
    

    pinMode(button_pins[i],INPUT_PULLUP);
  }
    
    pinMode(button_pins[NBR_POINT_BUTTONS],INPUT_PULLUP);

    circleLights();

    flashLights(250);
    flashLights(250);
    flashLights(250);

    //set all the button states to true
    memset(lastButtonState,1,sizeof(lastButtonState));

    // initialize serial:
    Serial1.begin(9600);
    // reserve 200 bytes for the inputString:
    inputString.reserve(200);

    requestSync();
}

void requestSync(){ //send a message to the points controller to request a synchronisation 
  Serial1.write("r\n");
}

void flashLights(int wait){
  for(i=0; i<NBR_POINT_BUTTONS; i++){
      digitalWrite(ledpins[i][0], HIGH);
      digitalWrite(ledpins[i][1], HIGH);
      if(i == 5){
        digitalWrite(ledpins_tri[0], HIGH);
        digitalWrite(ledpins_tri[1], HIGH);
        digitalWrite(ledpins_tri[2], HIGH);
      }
    }

    delay(wait);

    for(i=0; i<NBR_POINT_BUTTONS; i++){
      digitalWrite(ledpins[i][0], LOW);
      digitalWrite(ledpins[i][1], LOW);
      if(i == 5){
        digitalWrite(ledpins_tri[0], LOW);
        digitalWrite(ledpins_tri[1], LOW);
        digitalWrite(ledpins_tri[2], LOW);
      }
    }

    delay(wait);
}

void circleLights(){
  for(i=0; i<NBR_POINT_BUTTONS; i++){ //circle around all the lights
      if(i == 5){
        digitalWrite(ledpins_tri[0], HIGH);
        delay(flash_wait);
        digitalWrite(ledpins_tri[0], LOW);
        digitalWrite(ledpins_tri[1], HIGH);
        delay(flash_wait);
        digitalWrite(ledpins_tri[1], LOW);
        digitalWrite(ledpins_tri[2], HIGH);
        delay(flash_wait);
        digitalWrite(ledpins_tri[2], LOW);
      }
      else{
        digitalWrite(ledpins[i][0], HIGH);
        delay(flash_wait);
        digitalWrite(ledpins[i][0], LOW);
        digitalWrite(ledpins[i][1], HIGH);
        delay(flash_wait);
        digitalWrite(ledpins[i][1], LOW);
      }
    }
}

void setPointLight(int button_index, int state){
  if(button_index == 5){
    switch(state){
      case 0:
        digitalWrite(ledpins_tri[0], HIGH);
        digitalWrite(ledpins_tri[1], LOW);
        digitalWrite(ledpins_tri[2], LOW);
        break;
       case 1:
        digitalWrite(ledpins_tri[0], LOW);
        digitalWrite(ledpins_tri[1], HIGH);
        digitalWrite(ledpins_tri[2], LOW);
        break;
       case 2:
        digitalWrite(ledpins_tri[0], LOW);
        digitalWrite(ledpins_tri[1], LOW);
        digitalWrite(ledpins_tri[2], HIGH);
        break;
    }
  }
  else{
  digitalWrite(ledpins[button_index][0], state);
  digitalWrite(ledpins[button_index][1], !state);
  }
  
}

void updatePointState(int servo_index, int state){
  //map from the servo to the point state
  int point_index;
  
  if(point_index == 5){ //if it is 5 wrap around 0 -> 3
    point_state[point_index]++;
    if(point_state[point_index] > 2){
      point_state[point_index] = 0;
    }
  }
  else{
    point_index = servo_point[servo_index];
    point_state[point_index] = state;
  }

  

  setPointLight(point_index, point_state[point_index]);
}

void requestPointChange(int button_index){
  //map from the button to the servo_index
  Serial1.println("p" + String(index));
}

void readButtons(){ //reads each button
  for(i=0; i<NBR_POINT_BUTTONS+1; i++){ //each point button plus the lights button

    //read if any buttons have been pushed
  
    // read the state of the switch into a local variable:
    int reading = digitalRead(button_pins[i]);
  
    // check to see if you just pressed the button
    // (i.e. the input went from LOW to HIGH), and you've waited long enough
    // since the last press to ignore any noise:
  
    // If the switch changed, due to noise or pressing:
    if (reading != lastButtonState[i]) {
      // reset the debouncing timer
      lastDebounceTime[i] = millis();
    }
  
    if ((millis() - lastDebounceTime[i]) > debounceDelay) {
      // whatever the reading is at, it's been there for longer than the debounce
      // delay, so take it as the actual current state:
  
      // if the button state has changed:
      if (reading != buttonState[i]) {
        buttonState[i] = reading;
        if (reading && i<NBR_POINT_BUTTONS){ //if it is positive (so only on button up), toggle the point state
          requestPointChange(i); //change to send point change request
        }
        else if(reading){ //this is trigged when the LIGHTS button is pressed.
          flashLights(200);
          flashLights(200);
          flashLights(200);
          circleLights();
          requestSync();
        }
      }
      }

     // save the reading. Next time through the loop, it'll be the lastButtonState:
    lastButtonState[i] = reading;
    }
  
}


void loop() {

  readButtons();
  
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') { // a complete string has been recieved so parse it.
      //read all the sync string. Update servo status then call update point status
      //reset input string now it has been parsed.
      inputString = ""; 
    }
    else{
      inputString += inChar; //just add the character to the string
    }
  }
}
