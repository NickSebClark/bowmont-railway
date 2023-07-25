#define NBR_SERVOS 15
#define NBR_POINT_BUTTONS 12

// led pins for each point
int ledpins[][2] = {{10, 11},
                    {46, 45},
                    {33, 34},
                    {52, 53},
                    {8, 23},
                    {-1, -1},
                    {31, 30},
                    {24, 25},
                    {36, 41},
                    {27, 29},
                    {49, 39},
                    {44, 50}};

// LED pins for the tristate button
int ledpins_tri[] = {35, 43, 51};
int button_pins[] = {9, 48, 42, 7, 22, 40, 32, 26, 37, 28, 47, 6, 38};

const int flash_wait = 50;

int servo_point[] = {0, 1, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11}; // defines which point a particular servo is changing. I.e. when a servo changes which light should we change.
int point_servo[] = {0, 1, 2, 3, 5, 6, 8, 10, 11, 12, 13, 14};       // what servo to switch for a particular point, the controller handles point pairs)
int servo_6_set;
int servo_7_set;

int i = 0;

int buttonState[NBR_POINT_BUTTONS + 1];     // the current reading from the input pin
int lastButtonState[NBR_POINT_BUTTONS + 1]; // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime[NBR_POINT_BUTTONS + 1]; // the last time the output pin was toggled
unsigned long debounceDelay = 100;                     // the debounce time; increase if the output flickers
unsigned long previousMillis = 0;                      // will store last time LED was updated

char inCmd[25];
int cmdPos = 0;

void setup()
{

  // set the digital pin as output:
  for (i = 0; i < NBR_POINT_BUTTONS; i++)
  {
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

    pinMode(button_pins[i], INPUT_PULLUP);
  }

  pinMode(button_pins[NBR_POINT_BUTTONS], INPUT_PULLUP);

  circleLights();

  flashLights(250);

  // set all the button states to false
  memset(lastButtonState, 0, sizeof(lastButtonState));

  // initialize serial:
  Serial1.begin(9600);
  Serial.begin(9600);

  requestSync();
}

void requestSync()
{ // send a message to the points controller to request a synchronisation
  Serial1.write("r\n");
}

void flashLights(int wait)
{
  for (i = 0; i < NBR_POINT_BUTTONS; i++)
  {
    digitalWrite(ledpins[i][0], HIGH);
    digitalWrite(ledpins[i][1], HIGH);
    if (i == 5)
    {
      digitalWrite(ledpins_tri[0], HIGH);
      digitalWrite(ledpins_tri[1], HIGH);
      digitalWrite(ledpins_tri[2], HIGH);
    }
  }

  delay(wait);

  for (i = 0; i < NBR_POINT_BUTTONS; i++)
  {
    digitalWrite(ledpins[i][0], LOW);
    digitalWrite(ledpins[i][1], LOW);
    if (i == 5)
    {
      digitalWrite(ledpins_tri[0], LOW);
      digitalWrite(ledpins_tri[1], LOW);
      digitalWrite(ledpins_tri[2], LOW);
    }
  }

  delay(wait);
}

void circleLights()
{
  for (i = 0; i < NBR_POINT_BUTTONS; i++)
  { // circle around all the lights
    if (i == 5)
    {
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
    else
    {
      digitalWrite(ledpins[i][0], HIGH);
      delay(flash_wait);
      digitalWrite(ledpins[i][0], LOW);
      digitalWrite(ledpins[i][1], HIGH);
      delay(flash_wait);
      digitalWrite(ledpins[i][1], LOW);
    }
  }
}

void setPointLight(int button_index, int state)
{
  if (button_index == 5)
  {
    switch (state)
    {
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
  else
  {
    digitalWrite(ledpins[button_index][0], state);
    digitalWrite(ledpins[button_index][1], !state);
  }
}

void updatePointState(int servo_index, int state)
{
  // map from the servo to the point state
  int point_index;
  Serial.println("Update State: " + String(servo_index) + " State =" + String(state));

  point_index = servo_point[servo_index]; // find which point to change for this servo.

  if (servo_index == 6)
  {
    servo_6_set = state; // save this as servo 7 state is irrelevant if this is set.
    if (state)
    {
      state = 2; // set the bottom siding
    }
  }
  else if (servo_index == 7)
  {
    servo_7_set = state;
    if (servo_6_set)
    {
      state = 2; // set the bottom siding in the 3 if servo 6 is set,o therwise servo 7 indicates middle siding
    }
  }

  setPointLight(point_index, state);
}

void requestPointChange(int button_index)
{
  // map from the button to the servo_index
  int index = point_servo[button_index];

  Serial.println("Request change button index: " + String(button_index) + " Servo Index: " + String(index));

  if (button_index == 5)
  { // some special code for the tristate point as we need to control p6 and p7
    if (servo_6_set)
    { // state is 2 so change to state 0
      Serial1.println("p6");
      if (!servo_7_set)
      {
        Serial1.println("p7");
      }
    }
    else if (servo_7_set)
    { // state 0 so change to state 1
      Serial1.println("p7");
    }
    else
    { // state 1 so change to state 2
      Serial1.println("p6");
    }
  }
  else
  {
    Serial1.println("p" + String(index)); // point pairs are handled by the points controller
  }
}

void readButtons()
{ // reads each button
  for (i = 0; i < NBR_POINT_BUTTONS + 1; i++)
  { // each point button plus the lights button

    // read if any buttons have been pushed

    // read the state of the switch into a local variable:
    int reading = digitalRead(button_pins[i]);

    // check to see if you just pressed the button
    // (i.e. the input went from LOW to HIGH), and you've waited long enough
    // since the last press to ignore any noise:

    // If the switch changed, due to noise or pressing:
    if (reading != lastButtonState[i])
    {
      // reset the debouncing timer
      lastDebounceTime[i] = millis();
    }

    if ((millis() - lastDebounceTime[i]) > debounceDelay)
    {
      // whatever the reading is at, it's been there for longer than the debounce
      // delay, so take it as the actual current state:

      // if the button state has changed:
      if (reading != buttonState[i])
      {
        buttonState[i] = reading;
        if (reading && i < NBR_POINT_BUTTONS)
        {                        // if it is positive (so only on button up), toggle the point state
          requestPointChange(i); // change to send point change request
        }
        else if (reading)
        { // this is trigged when the LIGHTS button is pressed.
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

void loop()
{

  readButtons();
}

void serialEvent1()
{
  while (Serial1.available())
  {
    // get the new byte:
    char inChar = (char)Serial1.read();
    inCmd[cmdPos] = inChar;
    cmdPos++;

    if (inChar == '\n')
    { // a complete string has been recieved so parse it.
      if (inCmd[0] == 'S')
      { // Sync command recieved
        for (i = 0; i < NBR_SERVOS; i++)
        {
          updatePointState(i, String(inCmd[i + 1]).toInt());
        }
      }
      // reset input string now it has been parsed.
      cmdPos = 0;
    }
  }
}
