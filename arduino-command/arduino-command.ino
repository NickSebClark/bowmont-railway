#include <Adafruit_PWMServoDriver.h>

#include <TimerThree.h>

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define NBR_POINTS 15

#define Control_switch 44


// min = 200
// max = 300 

// the counter number for each servo
// look at the diagram on Python. The buttons are labelled
#define servo_0 14   // Button 0
#define servo_1 6   // Button 1
#define servo_2 8   // Button 2
#define servo_3 2  // Button 3
#define servo_4 1  // Button 3
#define servo_5 15   // Button 4 #TESTTEST
#define servo_6 4  // Button 5
#define servo_7 5  // Button 5
#define servo_8 10  // Button 6
#define servo_9 9   // Button 6
#define servo_10 7  // Button 7 INCREMENT TEST
#define servo_11 3  // Button 8
#define servo_12 11 // Button 9
#define servo_13 12 // Button 10
#define servo_14 13 // Button 11

#define servo_0_pos0 326
#define servo_1_pos0 275
#define servo_2_pos0 340
#define servo_3_pos0 350
#define servo_4_pos0 200
#define servo_5_pos0 275
#define servo_6_pos0 350
#define servo_7_pos0 362
#define servo_8_pos0 279
#define servo_9_pos0 324
#define servo_10_pos0 395
#define servo_11_pos0 350
#define servo_12_pos0 276
#define servo_13_pos0 275
#define servo_14_pos0 290

#define servo_0_pos1 276
#define servo_1_pos1 376
#define servo_2_pos1 278
#define servo_3_pos1 200
#define servo_4_pos1 275
#define servo_5_pos1 358
#define servo_6_pos1 285
#define servo_7_pos1 299
#define servo_8_pos1 324
#define servo_9_pos1 276
#define servo_10_pos1 275
#define servo_11_pos1 283
#define servo_12_pos1 340
#define servo_13_pos1 350
#define servo_14_pos1 340

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

char inCmd[6];
int cmdPos = 0;

int pointStatus[NBR_POINTS];
int pointServo[NBR_POINTS] = {servo_0, servo_1, servo_2, servo_3, servo_4, servo_5, servo_6, servo_7, servo_8, servo_9, servo_10, servo_11, servo_12, servo_13, servo_14};
int pointPos0[NBR_POINTS] = {servo_0_pos0, servo_1_pos0, servo_2_pos0, servo_3_pos0, servo_4_pos0, servo_5_pos0, servo_6_pos0, servo_7_pos0, servo_8_pos0, servo_9_pos0, servo_10_pos0, servo_11_pos0, servo_12_pos0, servo_13_pos0, servo_14_pos0};
int pointPos1[NBR_POINTS] = {servo_0_pos1, servo_1_pos1, servo_2_pos1, servo_3_pos1, servo_4_pos1, servo_5_pos1, servo_6_pos1, servo_7_pos1, servo_8_pos1, servo_9_pos1, servo_10_pos1, servo_11_pos1, servo_12_pos1, servo_13_pos1, servo_14_pos1};
int point_pair[NBR_POINTS] = {0, 0, 0, 1, -1, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0}; // shows the offset, if any, to a partner in a point pair.
int pointPos[NBR_POINTS];

boolean stringRecieved = false;

String syncString;

void incrementPosition(int point)
{
  pointPos[point]++;

  pwm.setPWM(pointServo[point], 0, pointPos[point]);

  Serial.print("<Increment point in Arduino, Point: ");
  Serial.print(point);
  Serial.print(" Val: ");
  Serial.print(pointPos[point]);
  Serial.print(">\n");
}

void decrementPosition(int point)
{
  pointPos[point]--;

  pwm.setPWM(pointServo[point], 0, pointPos[point]);

  Serial.print("<Decrement point in Arduino, Point: ");
  Serial.print(point);
  Serial.print(" Val: ");
  Serial.print(pointPos[point]);
  Serial.print(">\n");
}

void setup()
{
  Serial.begin(9600); // init comm
  Serial1.begin(9600);

  pwm.begin();
  pwm.setPWMFreq(50);

  memcpy(pointPos, pointPos0, sizeof(pointPos0));

  for (int i = 0; i < NBR_POINTS; i++)
  {
    pointStatus[i] = 0;
    setPoint(i, false);
  }
  syncData();

  Timer3.initialize(20000000);
  Timer3.attachInterrupt(sendHeartBeat);
}

void loop()
{
}

void parseString()
{
  Serial.print("<Parsing Input String>\n");
  
  int point_index;

  switch (inCmd[0])
  {
  case 'p':

    point_index = indexFromString();

    // set the point pair too if it exists. We only update on the seconf of the pair
    if (point_pair[point_index] != 0){ 
      setPoint(point_index, false);
      setPoint(point_index + point_pair[point_index], true);
    }
    else
      setPoint(point_index, true);

    break;
  case 's':
    setSignal(inCmd[2]);
    break;
  case 'l':
    toggleLights();
    break;
  case 'c':
    sendHeartBeat();
    break;
  case 'r':
    syncData();
    break;
  case 'i':
    incrementPosition(indexFromString());
    break;
  case 'd':
    decrementPosition(indexFromString());
    break;
  default:
    Serial.println("<Command not found>");
    break;
  }
}

int indexFromString()
{
  String s;
  if (cmdPos > 2)
  { // two character number
    s = String(inCmd[1]) + String(inCmd[2]);
    return s.toInt();
  }
  else
    return (int)inCmd[1] - 48;
}



void serialEvent1()
{
  while (Serial1.available())
  {
    int i;

    char inChar = (char)Serial1.read();

    // add it to the inputString:
    inCmd[cmdPos] = inChar;
    cmdPos++;

    // if the incoming character is a newline, we have a whole command. Do something.
    if (inChar == '\n')
    {
      Serial.println("<Serial-1 Recieved>");
      for (i = 0; i < cmdPos; i++)
      {
        Serial.print(inCmd[i]);
      }
      parseString();
      cmdPos = 0;
    }
  }
}

void serialEvent()
{ // reads from the serial port
  while (Serial.available())
  {
    int i;
    char inChar = (char)Serial.read();

    // add it to the inputString:
    inCmd[cmdPos] = inChar;
    cmdPos++;

    // if the incoming character is a newline, we have a whole command. Do something.
    if (inChar == '\n')
    {
      Serial.println("<Serial Recieved>");
      for (i = 0; i < cmdPos; i++)
      {
        Serial.print(inCmd[i]);
      }
      parseString();
      cmdPos = 0;
    }
  }
}

void sendHeartBeat()
{
  Serial.print("<ID: 18/01/25 v2.3>\n");
}

void setPoint(int point, bool sync)
{ // toggles status of point

  if (pointServo[point] > -2)
  {
    if (pointStatus[point])
    {
      Serial.print("<Setting point in Arduino, Point: ");
      Serial.print(point);
      Serial.print(" Val: ");
      Serial.print(pointPos0[point]);
      Serial.print(">\n");
      pwm.setPWM(pointServo[point], 0, pointPos0[point]);
      pointStatus[point] = 0;
      pointPos[point] = pointPos0[point];
    }
    else
    {
      Serial.print("<Setting point in Arduino, Point: ");
      Serial.print(point);
      Serial.print(" Val: ");
      Serial.print(pointPos1[point]);
      Serial.print(">\n");
      pwm.setPWM(pointServo[point], 0, pointPos1[point]);
      pointStatus[point] = 1;
      pointPos[point] = pointPos1[point];
    }
  }
  delay(1000);
  pwm.setPWM(pointServo[point], 0, 0);

  if (sync){
    syncData();
  }
}

void syncData()
{
  syncString = "S";
  for (int k = 0; k < NBR_POINTS; k++)
  {
    syncString = syncString + String(pointStatus[k]);
  }
  // send to both serial ports so PC/controller swap is seamless.
  Serial.println(syncString);
  Serial1.println(syncString);
}

void setSignal(int sig)
{
  Serial.println("<Signals...>");
  syncData();
}

void toggleLights()
{
  Serial.println("<Lights Toggled>");
  syncData();
}
