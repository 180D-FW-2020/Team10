import sys
import time
import math
import IMU
import datetime
import os
#My import
import RPi.GPIO as GPIO
import socket


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
#G_GAIN = 0.070          # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40              # Complementary filter constant
ACC_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
ACC_MEDIANTABLESIZE = 9         # Median filter table size for accelerometer. Higher = smoother but a longer delay
MyVar = -1
relVar = 0
Tvar = 0

def button_callback_SD(channel):
    #print("Start Drawing")
    client.send(str.encode("w"))
    
def button_callback_RA(channel):
    #print("Released Arrow\n\n")
    client.send(str.encode("s"))
    

###############Set up button reads##############################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #use physical pin number
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#set pin 8 to be an input pin and set inital value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#set pin 10 to be an input pin and set inital value to be pulled low (off)
GPIO.add_event_detect(8, GPIO.FALLING, callback=button_callback_SD) 
#set up event for pin 8, falling edge.
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback_RA)

oldXAccRawValue = 0
oldYAccRawValue = 0
oldZAccRawValue = 0

a = datetime.datetime.now()

#Setup the tables for the mdeian filter. Fill them all with '1' so we dont get devide by zero error
acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Z = [1] * ACC_MEDIANTABLESIZE

###############start IMU################

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

################Start communication with the computer###############
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.0.197'
port = 8080

print('waiting for connection')
try:
    client.connect((host,port))
except socket.error as e:
    print('much sad')

Response = client.recv(1024)
print(Response.decode("utf-8"))

while True:

    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()


    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    outputString = "Loop Time %5.2f " % ( LP )



    ###############################################
    #### Apply low pass filter ####
    ###############################################
    ACCx =  ACCx  * ACC_LPF_FACTOR + oldXAccRawValue*(1 - ACC_LPF_FACTOR);
    ACCy =  ACCy  * ACC_LPF_FACTOR + oldYAccRawValue*(1 - ACC_LPF_FACTOR);
    ACCz =  ACCz  * ACC_LPF_FACTOR + oldZAccRawValue*(1 - ACC_LPF_FACTOR);

    oldXAccRawValue = ACCx
    oldYAccRawValue = ACCy
    oldZAccRawValue = ACCz

    #########################################
    #### Median filter for accelerometer ####
    #########################################
    # cycle the table
    for x in range (ACC_MEDIANTABLESIZE-1,0,-1 ):
        acc_medianTable1X[x] = acc_medianTable1X[x-1]
        acc_medianTable1Y[x] = acc_medianTable1Y[x-1]
        acc_medianTable1Z[x] = acc_medianTable1Z[x-1]

    # Insert the lates values
    acc_medianTable1X[0] = ACCx
    acc_medianTable1Y[0] = ACCy
    acc_medianTable1Z[0] = ACCz

    # Copy the tables
    acc_medianTable2X = acc_medianTable1X[:]
    acc_medianTable2Y = acc_medianTable1Y[:]
    acc_medianTable2Z = acc_medianTable1Z[:]

    # Sort table 2
    acc_medianTable2X.sort()
    acc_medianTable2Y.sort()
    acc_medianTable2Z.sort()

    # The middle value is the value we are interested in
    ACCx = acc_medianTable2X[int(ACC_MEDIANTABLESIZE/2)];
    ACCy = acc_medianTable2Y[int(ACC_MEDIANTABLESIZE/2)];
    ACCz = acc_medianTable2Z[int(ACC_MEDIANTABLESIZE/2)];

    #Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG


    #Change the rotation value of the accelerometer to -/+ 180 and
    #move the Y axis '0' point to up.  This makes it easier to read.
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0


    ##################### END Tilt Compensation ########################

    #ME#

    if(MyVar < 5):
        MyVar+=1
        #print('did made it in')
        continue

    if(abs(AccYangle)<69):
        if(relVar == 0):
            time.sleep(1.5)
            #print('you reload')
            client.send(str.encode("r"))
            
            relVar = 1
            continue

        if(relVar == 1 and Tvar < 4):
            Tvar = Tvar+1
            #print('tvar<4')
            continue

        else:
            relVar = 0 
            Tvar = 0
            #print('else statement')
            continue
    #ME#

    #client.send(b'0')
    #slow program down a bit, makes the output more readable
    time.sleep(0.03)

client.close()
GPIO.cleanup() #cleanup

