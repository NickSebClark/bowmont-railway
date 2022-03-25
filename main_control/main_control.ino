#include <TimerThree.h>

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define NBR_POINTS 16

#define Control_switch 44

//the counter number for each servo
#define servo_0 0 //Button 0
#define servo_1 -1 //Button 1
#define servo_2 -1 //Button 2
#define servo_3 -1 //Button 3
#define servo_4 -1 //Button 3
#define servo_5 1 //Button 4
#define servo_6 -1 //Button 5
#define servo_7 -1 //Button 5
#define servo_8 -1 //Button 5
#define servo_9 -1 //Button 6
#define servo_10 -1 //Button 6
#define servo_11 2 //Button 7
#define servo_12 -1 //Button 8
#define servo_13 -1 //Button 9
#define servo_14 -1 //Button 10
#define servo_15 -1 //Button 11

#define servo_0_pos0 450
#define servo_1_pos0 -1
#define servo_2_pos0 -1
#define servo_3_pos0 -1
#define servo_4_pos0 -1
#define servo_5_pos0 475
#define servo_6_pos0 -1
#define servo_7_pos0 -1
#define servo_8_pos0 -1
#define servo_9_pos0 -1
#define servo_10_pos0 -1
#define servo_11_pos0 450
#define servo_12_pos0 -1
#define servo_13_pos0 -1
#define servo_14_pos0 -1
#define servo_15_pos0 -1

#define servo_0_pos1 600
#define servo_1_pos1 -1
#define servo_2_pos1 -1
#define servo_3_pos1 -1
#define servo_4_pos1 -1
#define servo_5_pos1 580
#define servo_6_pos1 -1
#define servo_7_pos1 -1
#define servo_8_pos1 -1
#define servo_9_pos1 -1
#define servo_10_pos1 -1
#define servo_11_pos1 600
#define servo_12_pos1 -1
#define servo_13_pos1 -1
#define servo_14_pos1 -1
#define servo_15_pos1 -1

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

char inCmd[6];
int cmdPos = 0;

int pointStatus[NBR_POINTS];
int pointServo[NBR_POINTS] = {servo_0,servo_1,servo_2,servo_3,servo_4,servo_5,servo_6,servo_7,servo_8,servo_9,servo_10,servo_11,servo_12,servo_13,servo_14,servo_15};
int pointPos0[NBR_POINTS] = {servo_0_pos0,servo_1_pos0,servo_2_pos0,servo_3_pos0,servo_4_pos0,servo_5_pos0,servo_6_pos0,servo_7_pos0,servo_8_pos0,servo_9_pos0,servo_10_pos0,servo_11_pos0,servo_12_pos0,servo_13_pos0,servo_14_pos0,servo_15_pos0};
int pointPos1[NBR_POINTS] = {servo_0_pos1,servo_1_pos1,servo_2_pos1,servo_3_pos1,servo_4_pos1,servo_5_pos1,servo_6_pos1,servo_7_pos1,servo_8_pos1,servo_9_pos1,servo_10_pos1,servo_11_pos1,servo_12_pos1,servo_13_pos1,servo_14_pos1,servo_15_pos1};

boolean stringRecieved = false;

String syncString;

void setup(){
  Serial.begin(9600);//init comms
  Serial1.begin(9600);
  
  pwm.begin();
  pwm.setPWMFreq(60);
  
  for(int i=0; i<NBR_POINTS; i++){
    pointStatus[i] = 0;
    setPoint(i);
  }
    
  Timer3.initialize(20000000);
  Timer3.attachInterrupt(sendHeartBeat);

}

void loop(){
  
}

void parseString(){
  Serial.print("<Parsing Input String>\n");
  String s;

  switch(inCmd[0]){
    case 'p':
      if(cmdPos > 2){//two character number
        s = String(inCmd[1]) + String(inCmd[2]);
        setPoint(s.toInt());
      }
      else
        setPoint((int)inCmd[1] - 48);
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
    default:
      Serial.println("<Command not found>");
      break;
  }
}

void serialEvent1() {
  while(Serial1.available()){
    
    char inChar = (char)Serial1.read(); 
    
    // add it to the inputString:
    inCmd[cmdPos] = inChar;
    cmdPos++;
    
    // if the incoming character is a newline, we have a whole command. Do something.
    if (inChar == '\n') {
      parseString();
      cmdPos = 0;      
    } 
  }
}

void serialEvent(){ //reads from the serial port
  while(Serial.available()){
    
    char inChar = (char)Serial.read(); 
    
    // add it to the inputString:
    inCmd[cmdPos] = inChar;
    cmdPos++;
    
    // if the incoming character is a newline, we have a whole command. Do something.
    if (inChar == '\n') {
      parseString();
      cmdPos = 0;      
    } 
  }
}

void sendHeartBeat(){
   Serial.print("<ID: 24/03/22 V2>\n");
}

void setPoint(int point){ //toggles status of point

  if(pointServo[point] > -1){
    if(pointStatus[point]){
      Serial.print("<Setting point in Arduino, Point: ");
      Serial.print(point);
      Serial.print(" Val: ");
      Serial.print(pointPos0[point]);
      Serial.print(">\n");
      pwm.setPWM(pointServo[point], 0, pointPos0[point]);
      pointStatus[point] = 0;
    }
    else{
      Serial.print("<Setting point in Arduino, Point: ");
      Serial.print(point);
      Serial.print(" Val: ");
      Serial.print(pointPos1[point]);
      Serial.print(">\n");
      pwm.setPWM(pointServo[point], 0, pointPos1[point]);
      pointStatus[point] = 1;
    }
  }   
  syncData();
}

void syncData(){
  syncString = "<Sync:";
  for(int k=0; k<NBR_POINTS; k++){
    syncString = syncString + String(pointStatus[k]);
  }
  syncString = syncString  + ">";
  //send to both serial ports so PC/controller swap is seamless.
  //Serial.println(syncString);
  //Serial1.println(syncString);
}

void setSignal(int sig){
  Serial.println("<Signals...>");
  syncData();
}

void toggleLights(){
  Serial.println("<Lights Toggled>");
  syncData();
}
