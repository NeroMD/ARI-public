import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import date
from datetime import datetime
import time

credential = credentials.Certificate('A-R-Ifirebase.json')

firebase_admin.initialize_app(credential, {

    'databaseURL': '-'

})
def alarm():

    ref = db.reference('Alarm')
    # usrRef = ref.child('USR1')
    ref.update({

        'Notification': True

    })
    print("alarm")
while True:
    ref = db.reference('/')
    dic = dict(ref.get())
    remB = 0
    remT= 0.0
    bee = 0
    count = 0
    heat = 0.0
    avgBee=0
    avgHeat=0.0
    for x in dic['Hives']:
        count+=1
        print(dic['Hives'][x]['beeCount'])
        bee+=dic['Hives'][x]['beeCount']
        remB=dic['Hives'][x]['beeCount']
        #  timm = datetime(dic['Hives'][x]['time'])
        heat+=dic['Hives'][x]['temp']
        remT = dic['Hives'][x]['temp']
    avgHeat = heat/count
    avgBee = bee/count




    ref = db.reference('Avarage')
    # usrRef = ref.child('USR1')
    ref.update({

        'beeCount': avgBee,

        'temp': avgHeat

    })
    if remT < 10 or remT>30 or remB < 150 or avgHeat<10 or avgBee<150:
        alarm()
    time.sleep(3600)