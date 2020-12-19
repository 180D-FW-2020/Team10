import socket
import random
import threading
#from _thread import *
from time import sleep
import paho.mqtt.client as mqtt

########END OF SETTING MQTT CONNECTION########################

def send_data():
    global sendDat
    while sendDat:
        def on_connect(client, userdata, flags, rc):
            client.subscribe("MRDMarcher/rotate")
            client.subscribe("MRDMarcher/fire")
        def on_disconnect(client, userdata, rc):
            if rc != 0:
                print('Unexpected Disconnect')
        mqtt_server = "broker.hivemq.com"
        mqtt_port = 1883
        #1 create a client instance
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        #client.on_message = on_message
        #2 connect to a broker
        client.connect_async(mqtt_server)
        client.loop_start()
        #5 publish shit
        #str_send = coordinates+","+area+","+bigArea+",0"
        z = -1*(float(zpos)-float(offset))
        coordinates = "0,0,"+str(z)
        force = float(bigArea)/float(area)
        f = str(force)
        client.publish('MRDMarcher/rotate',str.encode(coordinates), qos=1)
        client.publish('MRDMarcher/fire',str.encode(f), qos=1)
        #6 use disconnect() to disconnect from broker
        client.loop_stop()
        client.disconnect()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '192.168.0.127'
#HOST = '127.0.0.1'
#PORT = 1883
PORT = 9999
#to keep track of the threads
threadCount = 0

angleVal = 0
offset = 'n/a'
zpos = 'n/a'
coordinates = 'n/a'
area = '1'
bigArea = '1'
sendDat = True
c1 = 'n/a'
Fsocket = 0
bFromO = False
rpiIn = False

#bind host and port, if successful we will start waiting for client
try:
    serversocket.bind((HOST,PORT))
#except socket.error as e:
except IOError:
    print ("fuck cant fuck fuck")

print("Waiting for Connection")
serversocket.listen(5)

def client_thread(connection):
    #this one connects to openCV, client is who sends data.
    #so client thread is client send me data
    connection.send(str.encode("welcome to the server, you OpenCV")) 
    while True:
        global area
        global zpos
        global coordinates
        data=connection.recv(2048)
        srtData = data.decode("utf-8");
        chunks = srtData.split(',')
        if(chunks[0]=="0"):
            area = "1"
        else:
            area = chunks[0]
        zpos = chunks[1]
        coordinates = "0,0,"+chunks[1]
        if not data:
            bFromO = True
            break
        connection.sendall(str.encode(str(coordinates)))
    connection.close()

def client_thread_PI(connection):
    #this one connects to openCV, client is who sends data.
    #so client thread is client send me data
    connection.send(str.encode("welcome to the server, you RPi")) 
    pressed = False
    #pc = print_PA()
    while True:
        global area
        global coordinates
        global bigArea
        global offset
        global sendDat
        global rpiIn
        power=0
        data=connection.recv(2048)
        action = data.decode("utf-8")
        if not data:
            break
        if(action == 'r'):
            #print("you reload")
            def on_connect(client, userdata, flags, rc):
                client.subscribe("MRDMarcher/reload")
            def on_disconnect(client, userdata, rc):
                if rc != 0:
                    print('Unexpected Disconnect')
            mqtt_server = "broker.hivemq.com"
            mqtt_port = 1883
            #1 create a client instance
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.connect_async(mqtt_server)
            client.loop_start()
            #str_send = coordinates+","+area+","+bigArea+",1"
            str_send = "1"
            client.publish('MRDMarcher/reload',str.encode(str_send), qos=1)
            client.loop_stop()
            client.disconnect()

        elif(not(pressed) and action == 'w'):
            sendDat = True
            pressed = True
            bigArea = area
            offset = zpos
            rpiIn = True
            #print("this was pressed")
            threading.Thread(target=send_data, args=()).start()
            #pt = threading.Thread(target=pc.run, args=())
            #pt.start()
        elif(pressed and (action == 's')):
            sendDat = False
            #print("this was released")
            rpiIn = False
            pressed = False
    connection.close()

while True:
    #global Fsocket
    client,address = serversocket.accept()
    print('connected to: '+address[0]+' socket: '+str(address[1]))
    #if(address[0]=='192.168.0.197'):
    if(address[0]==HOST):
        threading.Thread(target=client_thread, args=(client,)).start()      
    else:
        print("else here")
        threading.Thread(target=client_thread_PI, args=(client,)).start()
    threadCount+=1
    print("the threadcount is: " + str(threadCount))

serversocket.close()
