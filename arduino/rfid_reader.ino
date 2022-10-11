#include "SPI.h"
#include "MFRC522.h"
#define SS_PIN 10
#define RST_PIN 9

#include <Servo.h>
Servo gapy;

int button_state = 0;
int buttonPin = 7;
int ledIndicator = 2;
int doorDelay = 800;
int buzzer = 4;

MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

int qtyOfCards = 1;
String registeredCards[] = {
  "8A:4B:81:7F"
};


void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();

  pinMode (buttonPin,INPUT_PULLUP);
  pinMode (ledIndicator,OUTPUT);
  digitalWrite(ledIndicator, 0);
  gapy.attach(2);
}


void loop() {
  buttonModule();
  rfidModule();
}


void openDoor(){
  //Serial.println("door open called");
  digitalWrite(ledIndicator, 1);
  gapy.write(170);
  delay(doorDelay);
  digitalWrite(ledIndicator, 0);
  delay(500); // for electrical security
  gapy.write(0);
}


void validateCard(String ID_key){
  for (int i = 0; i < qtyOfCards; i++){
    if (ID_key.indexOf(registeredCards[i]) >= 0){
      openDoor();
      //Serial.println(registeredCards[i]);
    }
  }
}


void buttonModule(){
  button_state = digitalRead(buttonPin);
  if (button_state == 0){
    openDoor();
  }
}


void rfidModule(){
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial())
    return;

  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }

  String ID_key = "";
  for (byte i = 0; i < 4; i++) {
    ID_key +=
    (rfid.uid.uidByte[i] < 0x10 ? "0" : "") +
    String(rfid.uid.uidByte[i], HEX) +
    (i!=3 ? ":" : "");
  }
  ID_key.toUpperCase();

  Serial.print("card_");
  Serial.println(ID_key);

  validateCard(ID_key);

  tone(buzzer, 800);
  delay(300);
  noTone(buzzer);
  delay(300);
  tone(buzzer, 800);
  delay(300);
  noTone(buzzer);

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}