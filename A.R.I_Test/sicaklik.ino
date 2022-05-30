#include <SoftwareSerial.h>
SoftwareSerial BTSerial(10,11);
#define irSensor1 A1
#define irSensor2 A4
int lm35Pin = A0;

int zaman = 50;
int okunan_deger = 0;
float sicaklik_gerilim = 0;
float sicaklik = 0;
void setup()
{

Serial.begin(9600);

}
void loop()
{
okunan_deger = analogRead(lm35Pin);
sicaklik_gerilim = (okunan_deger / 1023.0)*5000;
sicaklik = sicaklik_gerilim /10.0;
int ir1Value = analogRead(irSensor1);
int ir2Value = analogRead(irSensor2);
Serial.print(ir1Value);
Serial.print("-");
Serial.print(ir2Value);
Serial.print("-");
Serial.print(sicaklik);
Serial.println();

  


delay(500);
}
