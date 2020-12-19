import numpy as np
import cv2
import socket
import random
from time import sleep

#set up camera:
#to use the computer camera
cap = cv2.VideoCapture(0)
#somethings to do to the video image
#width
cap.set(3,640)
#height
cap.set(4,480)
#brightness
cap.set(10,150)

#set server variable
#serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Assigns a port for the server tha listens to clients connecting to this port
#serv.bind(('0.0.0.0',8080))
#serv.listen(5)

#client code
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.0.127'
#host = '127.0.0.1'
#port = 8080
port = 9999

print('waiting for connection')
try:
    client.connect((host,port))
except IOError:
    print ("fuck cant fuck opencv")


Response = client.recv(1024)
print(Response.decode("utf-8"))
#END of client code

myColors = [[57,76,0,100,255,255]] #green

myColorValues = [[0,255,0]] #color of countour?

area_int = 0
area_int_near = 0
power = 0
angle = 0
cy = 0
cy_near = 0
cy_i = 0

#function that finds the color on the screen
def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y,ai,yi=getContours(mask)
        #cv2.circle(frameResult, (x,y),10,myColorValues[count],cv2.FILLED)
        if(x!=0 and y!=0):
            newPoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]),mask)
    return newPoints, ai, yi

#function that takes care of contour 
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,dely,delx = 0,0,0,0
    area_i=0
    cy_i=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if area>500:
            area_i = area
            cy_i = int(M['m01']/M['m00'])
            #print(cy_i)
            cv2.drawContours(rec, cnt, -1,(255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, delx, dely = cv2.boundingRect(approx)
            #cv2.rectangle(frameResult, (x,y),(x+delx,y+dely),(0,255,0),2)
    return x+delx//2,y,area_i,cy_i

#function that communicates with UNITY
def BowLocation(angle):
    s = socket.socket()
    #connect to server on local computer
    s.connect(('192.168.0.197', 1755))
    s.send(("0"+","+"0"+","+str(angle)).encode())
    s.close()

while True:

	#capture frame-by-frame
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	
	if frame is None:
		print("FUCK")
		break
    
	frameResult = frame.copy()

	rec = frameResult
	#not sure what is the purpose of this
	colRec = rec.reshape((-1,3))
    #convert to np.float32 so we can do some cool stuff with what's in the box
	colRec = np.float32(colRec)
    #end of purposeless statement

	#now analyze what's in the box only
	_,area_int, y_int = findColor(rec, myColors, myColorValues)
	
	cv2.imshow('ACTUAL', frameResult) #this is what you actually see
	#client.send(str.encode(x))
	x = str(area_int)+','+str(y_int)
	client.send(str.encode(x))
	#x = str(area_int)+','+str(y_int)
    

	pressedKey = cv2.waitKey(1) & 0xFF

	if(pressedKey == ord('q')):
            break
	elif(pressedKey == ord('w')):
        	area_int_near = area_int
        	cy_near = y_int
        	print("area near:", area_int_near, "and cy near: ", cy_near)
            #print("Total score for", name, "is", score)
	elif(pressedKey == ord('s')):
			power = area_int_near/area_int
			angle = cy_near - y_int
			#BowLocation(angle)
			print("power: ", power, "angle: ", angle)
	elif(pressedKey == ord('r')):
		print('reload')

cap.release()
cv2.destroyAllWindows()
#conn.close()
#print('client disconnected')
