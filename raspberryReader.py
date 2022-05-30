import serial
import time
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import date
from datetime import datetime

credential = credentials.Certificate('A-R-Ifirebase.json')

firebase_admin.initialize_app(credential, {

    'databaseURL': '-'

})

heat=0.0
beeCounter = 0
s1Checker = False
s2Checker = False
#allowed = False
# eger diger fonksiyon calismiyosa calisirlar
# calisirsa 5 saniye icinde diger sensor yanmali
 
def cPlus():
    global beeCounter
    global t3
    global t1
    global s1Checker
    global s2Checker
    cont = True
    t3.start()
    while t3.is_alive() and cont:
        #print("2sartlar saglandi ",s1Checker)
        if s1Checker:
            s1Checker = False
            beeCounter+=1
            print("it should increase")
            cont=False
    s2Checker = False
    print(beeCounter)
    t3 = threading.Thread(target=timer)
    t1 = threading.Thread(target=cPlus)

def cMinus():
    global beeCounter
    global s1Checker
    global s2Checker
    global t4
    global t2
    cont = True
    t4.start()
    while t4.is_alive() and cont:
        #print("1 sartlar saglandi")
        if s2Checker:
            beeCounter-=1
            print("it should decrease")
            s2Checker = False
            cont = False

    s1Checker = False
    print(beeCounter)
    t4 = threading.Thread(target=timer)
    t2 = threading.Thread(target=cMinus)


# threadler icin ayri zaman sayaci
def timer():
    global allowed
    allowed = True
    time.sleep(5)
    allowed=False
def clock():
    global beeCounter
    global heat
    time.sleep(300)
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    Hive_ref = db.reference('Hives')


    hive_ref = Hive_ref.push({

        'beeCount': beeCounter,
        'time': now,
        'temp': heat

    })
    ref = db.reference('Current')
    # usrRef = ref.child('USR1')
    ref.update({

        'beeCount': beeCounter,
        'time': now,
        'temp': heat

    })


#thredler
t1 = threading.Thread(target=cPlus)
t2 = threading.Thread(target=cMinus)
t3 = threading.Thread(target=timer)
t4 = threading.Thread(target=timer)
t5 = threading.Thread(target=clock)

#dogru isim kontrol
if __name__ == '__main__':
    ser = serial.Serial('/dev/rfcomm0',9600,timeout=1)
    ser.flush()
    s1Record = 0
    s2Record = 0
    v = 0

# sonsuz loop, veri alimi ve yonetimi
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            sensors = str(line).split('-')
            sensors
            #print(line)
            if v <= 3 :
                v+=1
                print(sensors[0]+'\n'+sensors[1])
            if s1Record - int(sensors[0]) >= 250:
                print('1 doldu')
            if s2Record - int(sensors[1]) >= 250:
                print('2 doldu')

            if s2Record - int(sensors[1]) <= -250 and s2Record != 0:
                print('2 bosa gecti')
                if t1.is_alive() == True:
                    s1Checker = True
                    print("s1trueOldu")
                else:
                    if (t2.is_alive() == False):
                        t2.start()
                        print(s2Record)
                        print(sensors[1])
                    else:
                        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            if s1Record - int(sensors[0]) <= -250 and s1Record != 0:
                print('1 bosa gecti')
                if t2.is_alive() == True:
                    print('s2 true oldu')
                    s2Checker = True
                else:
                    if (t1.is_alive() == False):
                        print("t1 basliyo")
                        t1.start()
                        print("t1 basladi")

            s1Record = int(sensors[0])
            s2Record = int(sensors[1])
            heat = float(sensors[2])
            if t5.is_alive() == False:
                t5 = threading.Thread(target=clock)
                t5.start()
