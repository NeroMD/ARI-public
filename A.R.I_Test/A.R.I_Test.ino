#define irSensor1 A0
#define irSensor2 A4

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int ir1Value = analogRead(irSensor1);
  int ir2Value = analogRead(irSensor2);
  Serial.print(ir1Value);
  Serial.print("-");
  Serial.print(ir2Value);
  Serial.println();
  delay(500);
}
