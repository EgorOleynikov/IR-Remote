# 1 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
/* rawR&cv.ino Example sketch for IRLib2

 *  Illustrate how to capture raw timing values for an unknow protocol.

 *  You will capture a signal using this sketch. It will output data the 

 *  serial monitor that you can cut and paste into the "rawSend.ino"

 *  sketch.

 */
# 7 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
// Recommend only use IRLibRecvPCI or IRLibRecvLoop for best results
// #include "IRLibAll.h"
# 10 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 2
# 11 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 2
# 12 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 2
# 13 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 2

IRrecvPCI myReceiver(3);//pin number for the receiver
IRdecode myDecoder; //create decoder

void setup() {
  Serial.begin(9600);
  Serial.println((reinterpret_cast<const __FlashStringHelper *>(
# 19 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 3
                (__extension__({static const char __c[] __attribute__((__progmem__)) = (
# 19 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
                "Ready"
# 19 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 3
                ); &__c[0];}))
# 19 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
                )));
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
    myDecoder.decode(); //Decode it
    myDecoder.dumpResults(false); //Now print results. Use false for less detail
    Serial.print("uint16_t rawData[");
    Serial.print(recvGlobal.recvLength,10);
    Serial.print("]={");
    for(bufIndex_t i=1;i<recvGlobal.recvLength;i++) {
      Serial.print(recvGlobal.recvBuffer[i],10);
      Serial.print((reinterpret_cast<const __FlashStringHelper *>(
# 41 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 3
                  (__extension__({static const char __c[] __attribute__((__progmem__)) = (
# 41 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
                  ", "
# 41 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 3
                  ); &__c[0];}))
# 41 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
                  )));
    }
    Serial.println((reinterpret_cast<const __FlashStringHelper *>(
# 43 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 3
                  (__extension__({static const char __c[] __attribute__((__progmem__)) = (
# 43 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
                  "1000};"
# 43 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino" 3
                  ); &__c[0];}))
# 43 "c:\\Users\\Andrew\\Desktop\\Remote\\Remote.ino"
                  )));//Add arbitrary trailing space
    myReceiver.enableIRIn(); //Restart receiver
  }
}
