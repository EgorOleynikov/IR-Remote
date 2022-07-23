#include <Arduino.h>
#line 1 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
/* rawR&cv.ino Example sketch for IRLib2
 *  Illustrate how to capture raw timing values for an unknow protocol.
 *  You will capture a signal using this sketch. It will output data the 
 *  serial monitor that you can cut and paste into the "rawSend.ino"
 *  sketch.
 */
// Recommend only use IRLibRecvPCI or IRLibRecvLoop for best results
// #include "IRLibAll.h"
#include <IRLibRecvPCI.h>
#include <IRLibDecodeBase.h>
#include <IRLib_P01_NEC.h>
#include <IRLibCombo.h>

IRrecvPCI myReceiver(3);//pin number for the receiver
IRdecode myDecoder;   //create decoder

#line 17 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
void setup();
#line 22 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
void loop();
#line 17 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
void setup() {
  Serial.begin(9600);
  Serial.println(F("Ready"));
}

void loop() {
  if (Serial.available() > 0){
    int incomingByte = Serial.read();
    if (incomingByte == '1'){
      myReceiver.enableIRIn(); // Start the receiver
      Serial.println("Listen");
    } else if (incomingByte == '0') {
      myReceiver.disableIRIn();
    }
  }
  //Continue looping until you get a complete signal received
  if (myReceiver.getResults()) {
    myDecoder.decode();           //Decode it
    myDecoder.dumpResults(false);  //Now print results. Use false for less detail
    Serial.print("uint16_t rawData[");
    Serial.print(recvGlobal.recvLength,DEC);
    Serial.print("]={");
    for(bufIndex_t i=1;i<recvGlobal.recvLength;i++) {
      Serial.print(recvGlobal.recvBuffer[i],DEC);
      Serial.print(F(", "));
    }
    Serial.println(F("1000};"));//Add arbitrary trailing space
    myReceiver.enableIRIn();      //Restart receiver
  }
}

