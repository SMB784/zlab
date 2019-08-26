#include <stepmoto.h>


//#include <Encoder.h>

/* *******Defination of Pins*******/
/*
#define XEncPin1 2
#define XEncPin2 4
#define YEncPin1 3
#define YEncPin2 5
#define ZEncPin1 3
#define ZEncPin2 5
*/
#define XDirPin 3
#define XPulPin 2
#define XEnaPin 4 
#define YDirPin 6
#define YPulPin 5
#define YEnaPin 7
#define ZDirPin 9
#define ZPulPin 8
#define ZEnaPin 10 


//Encoder XEnc(XEncPin1,XEncPin2);
//Encoder YEnc(YEncPin1,YEncPin2);
//Encoder ZEnc(ZEncPin1,ZEncPin2);
// Change these two numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
StepMoto XMoto(XDirPin,XPulPin,XEnaPin,true);
StepMoto YMoto(YDirPin,YPulPin,YEnaPin,true);
StepMoto ZMoto(ZDirPin,ZPulPin,ZEnaPin,0);

String inputString = "";
bool stringComplete = false;
long XAimPosition, YAimPosition, ZAimPosition;
long XCurrentPosition = 0,YCurrentPosition = 0, ZCurrentPosition = 0;


void setup() {
  Serial.begin(9600);
    // reserve 200 bytes for the inputString:
  pinMode(XDirPin,OUTPUT);
  pinMode(XPulPin,OUTPUT);
  pinMode(XEnaPin,OUTPUT);
  pinMode(YDirPin,OUTPUT);
  pinMode(YPulPin,OUTPUT);
  pinMode(YEnaPin,OUTPUT);
  pinMode(ZDirPin,OUTPUT);
  pinMode(ZPulPin,OUTPUT);
  pinMode(ZEnaPin,OUTPUT);
  inputString.reserve(200);
}

void loop() {
	if(stringComplete){
		//new position available
	
	/*	Serial.print(" y ");
		Serial.print(YAimPosition);
		Serial.print(" z ");
		Serial.print(ZAimPosition);
	  */
	  stringComplete = false;
  // long XDiff = XAimPosition - XCurrentPosition;
	  if(XAimPosition >0) XMoto.Dir(1);
    else XMoto.Dir(-1);
	  for (int i = 0; i <abs(XAimPosition);i++)
    {
      XMoto.PulUp();
      delayMicroseconds(1000);
      XMoto.PulDown();
      delayMicroseconds(1000);
    }
    if(YAimPosition >0) YMoto.Dir(1);
    else YMoto.Dir(-1);
    for (int i = 0; i <abs(YAimPosition);i++)
    {
      YMoto.PulUp();
      delayMicroseconds(1000);
      YMoto.PulDown();
      delayMicroseconds(1000);
    }
    if(ZAimPosition >0) ZMoto.Dir(1);
    else ZMoto.Dir(-1);
    for (int i = 0; i <abs(ZAimPosition);i++)
    {
      ZMoto.PulUp();
      delayMicroseconds(1000);
      ZMoto.PulDown();
      delayMicroseconds(1000);
    }
    XCurrentPosition =XCurrentPosition+ XAimPosition;
    YCurrentPosition =YCurrentPosition+ YAimPosition;
    ZCurrentPosition =ZCurrentPosition+ ZAimPosition;
    XAimPosition = 0;
    YAimPosition = 0;
    ZAimPosition = 0;
    Serial.print("x ");
    Serial.print(XCurrentPosition); 
    Serial.print("   y ");
    Serial.print(YCurrentPosition); 
    Serial.print("   z ");
    Serial.println(ZCurrentPosition); 
	}
		
}
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    if(isDigit(inChar)|| inChar == '-') inputString += inChar;
    else if(inChar == 'x' || inChar == 'X'){
      XAimPosition = inputString.toInt();
      inputString = "";
    }
    else if(inChar == 'y' || inChar == 'Y'){
      YAimPosition = inputString.toInt();
  	  inputString = "";      
    }
    else if(inChar == 'z' || inChar == 'Z'){
      ZAimPosition = inputString.toInt();
	  inputString = "";     
    }
    // if the incoming character is a num, add it to string
    // do something about it:
    if (inChar == '\n') {
  //    XAimPosition = inputString.toInt();
      inputString = "";
      stringComplete = true;
    }
  }
}
