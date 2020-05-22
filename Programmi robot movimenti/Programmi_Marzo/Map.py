'''
9/3 AD  10/2 AS    11/1 PD    12/0 PS
AS=26
AD=6
PS=19
PD=13
avanti=1
indietro=0
destra=3
sinistra=2
'''
import time
from time import sleep
import RPi.GPIO as GPIO
import threading
from random import randrange
import serial
from Adafruit_BNO055 import BNO055
import board
import busio
import adafruit_vl6180x
import numpy as np
from sys import getsizeof

lato=15
EAS=26
EAD=6
EPD=13
EPS=19
windup=150000
kp=50
ki=0.01
kd=100
prop=0.07
direzione=0
cm=968
avanti=1
indietro=0
destra=3
sinistra=2
voluto=7000
a=np.zeros((lato,lato))

for k in range(lato):
    for j in range(lato):
        a[k,j]=randrange(0,5)
    a[k,j]=randrange(0,5)
for k in range(lato):
    for j in range(lato):
        if(a[k,j]!=1):
            a[k,j]=0
    for j in range(lato):
        if(a[k,j]!=1):
            a[k,j]=0
a[int(lato/2),int(lato/2)]=57

print(getsizeof(a))
bno = BNO055.BNO055()
#i2c = busio.I2C(board.SCL, board.SDA)
#sensor = adafruit_vl6180x.VL6180X(i2c)
ser = serial.Serial('/dev/ttyUSB0',115200)

def setta(voluto,direzione):
    AD.voluto=voluto
    PD.voluto=voluto
    AS.voluto=voluto-50
    PS.voluto=voluto-50
    AS.direzione=direzione
    if(voluto==0):
        PS.voluto=0
        AS.voluto=0

def SAS(variabile):
    AS.counter+=1
    AS.enc=(time.time()-AS.time)*1000000
    AS.time=time.time()
    if (abs((AS.old-AS.enc))>100):
        AS.enc=(AS.old+AS.enc)/2
    AS.old=AS.enc

def SAD(variabile):
    AD.enc=(time.time()-AD.time)*1000000
    AD.time=time.time()
    if (abs((AD.old-AD.enc))>100):
        AD.enc=(AD.old+AD.enc)/2
    AD.old=AD.enc

def SPD(variabile):
    PD.enc=(time.time()-PD.time)*1000000
    PD.time=time.time()
    if (abs((PD.old-PD.enc))>100):
        PD.enc=(PD.old+PD.enc)/2
    PD.old=PD.enc

def SPS(variabile):
    PS.enc=(time.time()-PS.time)*1000000
    PS.time=time.time()
    if (abs((PS.old-PS.enc))>100):
        PS.enc=(PS.old+PS.enc)/2
    PS.old=PS.enc

class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        global voluto,direzione
        sel=0
        NPD=2
        NAD=0
        NPS=3
        NAS=1
        while((1) and not self.event.is_set()):
            if(sel==0):
                if(AS.voluto==0):
                    serial(0,2,AS.direzione)
                    integrale=0
                else:
                    AS.errore=AS.voluto-AS.enc
                    AS.derivata=AS.errore-AS.derivata
                    AS.integrale=AS.integrale+AS.errore
                    if(AS.integrale<-windup):
                        AS.integrale=-windup
                    if(AS.integrale>windup):
                        AS.integrale=windup
                    AS.valore=(prop*voluto)-(kp*AS.errore)-(ki*AS.integrale)-(kd*AS.derivata)
                    AS.derivata=AS.errore
                    if(AS.valore<0):
                       AS.valore=0
                    if(AS.valore>255):
                        AS.valore=255
                    AS.valore=int(AS.valore)
                    serial(AS.valore,NAS,AS.direzione)
                    #print(AS.valore)
            if(sel==1):
                if(AD.voluto==0):
                    serial(0,3,AS.direzione)
                    integrale=0
                else:
                    AD.errore=AD.voluto-AD.enc
                    AD.derivata=AD.errore-AD.derivata
                    AD.integrale=AD.integrale+AD.errore
                    if(AD.integrale<-windup):
                        AD.integrale=-windup
                    if(AD.integrale>windup):
                        AD.integrale=windup
                    AD.valore=(prop*voluto)-(kp*AD.errore)-(ki*AD.integrale)-(kd*AD.derivata)
                    AD.derivata=AD.errore
                    if(AD.valore<0):
                       AD.valore=0
                    if(AD.valore>255):
                        AD.valore=255
                    AD.valore=int(AD.valore)
                    serial(AD.valore,NAD,AS.direzione)
            if(sel==2):
                if(PS.voluto==0):
                    serial(0,0,AS.direzione)
                    integrale=0
                else:
                    PS.errore=PS.voluto-PS.enc
                    PS.derivata=PS.errore-PS.derivata
                    PS.integrale=PS.integrale+PS.errore
                    if(PS.integrale<-windup):
                        PS.integrale=-windup
                    if(PS.integrale>windup):
                        PS.integrale=windup
                    PS.valore=(prop*voluto)-(kp*PS.errore)-(ki*PS.integrale)-(kd*PS.derivata)
                    PS.derivata=PS.errore
                    if(PS.valore<0):
                       PS.valore=0
                    if(PS.valore>255):
                        PS.valore=255
                    PS.valore=int(PS.valore)
                    serial(PS.valore,NPS,AS.direzione)
                    #print(PS.valore)
            if(sel==3):
                if(PD.voluto==0):
                    serial(0,1,AS.direzione)
                    integrale=0
                else:
                    PD.errore=PD.voluto-PD.enc
                    PD.derivata=PD.errore-PD.derivata
                    PD.integrale=PD.integrale+PD.errore
                    if(PD.integrale<-windup):
                        PD.integrale=-windup
                    if(PD.integrale>windup):
                        PD.integrale=windup
                    PD.valore=(prop*voluto)-(kp*PD.errore)-(ki*PD.integrale)-(kd*PD.derivata)
                    PD.derivata=PD.errore
                    if(PD.valore<0):
                       PD.valore=0
                    if(PD.valore>255):
                        PD.valore=255
                    PD.valore=int(PD.valore)
                    serial(PD.valore,NPD,AS.direzione)
                    #print(PD.valore)
            time.sleep(0.001)
            sel+=1
            sel=sel%4

    def stop(self):
        self.event.set()

tmr = TimerClass()
class PID:
    def __init__(self,errore,tempo,voluto,valore,counter):
        self.errore=errore
        self.time=tempo
        self.enc=voluto
        self.old=voluto
        self.valore=valore
        self.voluto=voluto
        self.counter=counter
        self.derivata=0
        self.integrale=0
        self.direzione=avanti

class DATI:
    def __init__(self,HEADM):
        self.HEADM=HEADM
        self.riga=int(lato/2)
        self.colonna=int(lato/2)
        self.counter=0

AS = PID(0, time.time(),voluto,0,0)
AD = PID(0, time.time(),voluto,0,0)
PS = PID(0, time.time(),voluto,0,0)
PD = PID(0, time.time(),voluto,0,0)
dati=DATI(0)

def initialize():
    setta(0,avanti)
    direzione=0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EAS,GPIO.IN,GPIO.PUD_DOWN)
    GPIO.add_event_detect(EAS, GPIO.FALLING, callback=SAS) 
    GPIO.setup(EAD,GPIO.IN,GPIO.PUD_DOWN)
    GPIO.add_event_detect(EAD, GPIO.FALLING, callback=SAD)
    GPIO.setup(EPD,GPIO.IN,GPIO.PUD_DOWN)
    GPIO.add_event_detect(EPD, GPIO.FALLING, callback=SPD) 
    GPIO.setup(EPS,GPIO.IN,GPIO.PUD_DOWN)
    GPIO.add_event_detect(EPS, GPIO.FALLING, callback=SPS) 
    temp=time.time()
    tmr.start()
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
    head, roll, pitch = bno.read_euler()
    dati.HEADM=head
    a[dati.riga,dati.colonna]=1

def serial(valore,puntatore,movimento):
    temp=str(chr((valore>>4) | (puntatore<<4)))
    ser.write(temp.encode())
    temp=str(chr((valore&0b1111) | (movimento<<4)))
    ser.write(temp.encode())

def raddrizza():
    temp, roll, pitch = bno.read_euler()
    #print(abs(HEADM-temp))
    print(dati.HEADM)
    if((abs(dati.HEADM-temp))<180):
        setta(3700,3)
    if((abs(dati.HEADM-temp))>180):
           setta(3700,2)      #destra, ma chissà come mai non me lo accetta come input
    if(abs(dati.HEADM-temp)>2):
        while(abs(dati.HEADM-temp)>0.5):
            temp, roll, pitch = bno.read_euler()
            time.sleep(0.005)
            #print(abs(dati.HEADM-temp))
    setta(0,avanti)

def ruota_destra():
    dati.counter+=1
    dati.counter=dati.counter%4

def ruota_sinistra():
    dati.counter-=1
    dati.counter=dati.counter%4

def movimento_30(direzione):
    a[dati.riga,dati.colonna]=96
    if(direzione==avanti) :
        if((dati.counter==0) and (a[dati.riga,dati.colonna+1]!=1)): dati.colonna+=1
        if((dati.counter==1) and (a[dati.riga+1,dati.colonna]!=1)): dati.riga+=1
        if((dati.counter==2) and (a[dati.riga,dati.colonna-1]!=1)): dati.colonna-=1
        if((dati.counter==3) and (a[dati.riga-1,dati.colonna+1]!=1)): dati.riga-=1
    if(direzione==indietro):
        if(dati.counter==0): dati.colonna-=1
        if(dati.counter==1): dati.riga-=1
        if(dati.counter==2): dati.colonna+=1
        if(dati.counter==3): dati.riga+=1
    a[dati.riga,dati.colonna]=57

initialize()
distAV=0
h=0
while(1):
    while(1):
        if((dati.counter==0) and (a[dati.riga,dati.colonna+1]==0)): 
            movimento_30(avanti)
            break
        elif((dati.counter==1) and (a[dati.riga+1,dati.colonna]==0)): 
            movimento_30(avanti)
            break
        elif((dati.counter==2) and (a[dati.riga,dati.colonna-1]==0)): 
            movimento_30(avanti)
            break
        elif((dati.counter==3) and (a[dati.riga-1,dati.colonna]==0)): 
            movimento_30(avanti)
            break
        '''
        elif((dati.counter==0) and (a[dati.riga,dati.colonna+1]==1)): ruota_destra()
        elif((dati.counter==1) and (a[dati.riga+1,dati.colonna]==1)): ruota_destra()
        elif((dati.counter==2) and (a[dati.riga,dati.colonna-1]==1)): ruota_destra()
        elif((dati.counter==3) and (a[dati.riga-1,dati.colonna]==1)): ruota_destra()
        '''
        if(dati.counter==0):
            if(a[dati.riga,dati.colonna+1]==1):
                if((a[dati.riga+1,dati.colonna]==0) or ((a[dati.riga+1,dati.colonna]==0) and (a[dati.riga-1,dati.colonna]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga-1,dati.colonna]==0) and (a[dati.riga+1,dati.colonna]>0)):
                    ruota_sinistra()
                    break
        if(dati.counter==1):
            if(a[dati.riga+1,dati.colonna]==1):
                if((a[dati.riga,dati.colonna-1]==0) or ((a[dati.riga,dati.colonna-1]==0) and (a[dati.riga,dati.colonna+1]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga,dati.colonna+1]==0) and (a[dati.riga,dati.colonna-1]>0)):
                    ruota_sinistra()
                    break
        if(dati.counter==2):
            if(a[dati.riga,dati.colonna-1]==1):
                if((a[dati.riga-1,dati.colonna]==0) or ((a[dati.riga-1,dati.colonna]==0) and (a[dati.riga+1,dati.colonna]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga+1,dati.colonna]==0) and (a[dati.riga-1,dati.colonna]>0)):
                    ruota_sinistra()
                    break
        if(dati.counter==0):
            if(a[dati.riga,dati.colonna+1]==96):
                if((a[dati.riga+1,dati.colonna]==0) or ((a[dati.riga+1,dati.colonna]==0) and (a[dati.riga-1,dati.colonna]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga-1,dati.colonna]==0) and (a[dati.riga+1,dati.colonna]>0)):
                    ruota_sinistra()
                    break
        if(dati.counter==1):
            if(a[dati.riga+1,dati.colonna]==96):
                if((a[dati.riga,dati.colonna-1]==0) or ((a[dati.riga,dati.colonna-1]==0) and (a[dati.riga,dati.colonna+1]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga,dati.colonna+1]==0) and (a[dati.riga,dati.colonna-1]>0)):
                    ruota_sinistra()
                    break
        if(dati.counter==2):
            if(a[dati.riga,dati.colonna-1]==96):
                if((a[dati.riga-1,dati.colonna]==0) or ((a[dati.riga-1,dati.colonna]==0) and (a[dati.riga+1,dati.colonna]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga+1,dati.colonna]==0) and (a[dati.riga-1,dati.colonna]>0)):
                    ruota_sinistra()
                    break
        if(dati.counter==3):
            if(a[dati.riga-1,dati.colonna]==96):
                if((a[dati.riga,dati.colonna+1]==0) or ((a[dati.riga,dati.colonna+1]==0) and (a[dati.riga,dati.colonna-1]>1))):
                    ruota_destra()
                    break
                elif((a[dati.riga,dati.colonna-1]==0) and (a[dati.riga,dati.colonna+1]>0)):
                    ruota_sinistra()
                    break
    if((dati.counter==0) and ((dati.colonna+1)==(lato-1))): 
        ruota_destra()
        print("Lato destro")
    if((dati.counter==1) and ((dati.riga+1)==(lato-1))): 
        ruota_destra()
        print("Lato sotto")
    if((dati.counter==2) and ((dati.colonna-1)==0)): 
        ruota_destra()
        print("Lato sinistro")
    if((dati.counter==3) and ((dati.riga-1)==0)): 
        ruota_destra()
        print("Lato sopra")
    if(dati.counter==0): print("Guardo destra")
    elif(dati.counter==1): print("Guardo basso")
    elif(dati.counter==2): print("Guardo sinistra")
    else: print("Guardo alto")
    print(a)
    time.sleep(1)
    '''
    elif((dati.counter==0) and (a[dati.riga,dati.colonna+1]!=1)): ruota_destra()
    elif((dati.counter==1) and (a[dati.riga+1,dati.colonna]!=1)): ruota_destra()
    elif((dati.counter==2) and (a[dati.riga,dati.colonna-1]!=1)): ruota_destra()
    elif((dati.counter==3) and (a[dati.riga-1,dati.colonna]!=1)): ruota_destra()
    '''
