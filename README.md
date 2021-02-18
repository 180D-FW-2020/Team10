# Team10

Game Description

	It is an interactive and competitive archery game
	Single and multiplayer mode
	Use of Keyboard and Mouse
	Use of simulator controller
	Test your accuracy with the controller and a camera
	Challenge yourself in accuracy and speed or compete with your friends

Parts list and where to purchase 

	RaspberryPi Zero W (Amazon)
	IMU - https://ozzmaker.com/product/berryimu-accelerometer-gyroscope-magnetometer-barometricaltitude-sensor/
	Custom PCB or similar breadboard layout
	Micro USB charging cable w/external battery (Amazon)
	Micro SD card (Amazon)
	Green Ball (up to you)

Programs Download and Setup 
No controller setup

	1.	you will need to install unity on your computer   https://unity3d.com/get-unity/download
	2.	Create an account on unity https://id.unity.com/en/conversations/5c9cca53-07d6-4b2a-bcf4-00fe928cc4cc019f
	3.	Email Mathew Rodriguez at thfdevien@g.ucla.edu to get access to the game
	4.	Follow the game instruction below to play it
	5.	Start the game and enjoy!!

Controller Setup

	1.	To set up the Raspberry Pi, please refer to the file named “Setup_Raspberri_Pi” for detailed instructions into how to set up the Raspberry Pi and connect it to your local network (i.e. the same your computer will be connected to)
	2.	To set up BerryIMU, please refer to the file named “” (instructions from tutorial)
	3.      Download “2piToMac.py” from github (link: ). You will need to add the file into the right folder. In the raspberryPi “cd BerryIMU>cd python”. 
		a. I would recommend use cyberDuck or WinSCP to do this because it gives a very friendly user interface 

Programs Description (github files)

	Python: It is the code for the controller for reading the data from Raspberry Pi Zero W/ Ozzmaker Berry IMU. For more info refer to the Image and gesture Recognition section.
	Rotation Codes: This is the code that controls the rotations using the BerryIMU. It was designed to detect the movements of the user and know when the “reload” action was performed.
	Unity: This is all the custom scripts made to run the game logic and physics. When downloading the executable all scripts will be included. 
	C_sharp/Server: it includes the game logic as well as the communication code files for Raspberry Pi Zero W and the Ozzmaker Berry IMU and unity
	OpenCV: it is python code uses OpenCV for image recognition using a green ball to determine the angle and the force of the launch of the arrow
	Sockets: These files connect the raspberry pi to the local computer through local socket connections. The Raspberrypi transmits shoot and IMU data to the user's computer.

Game Design and Features 

- Image and gesture Recognition 

		Using an IMU with two buttons which are connected to the Raspberry Pi Zero W/Ozzmaker Berry IMU; this gives a signal to the animated character to start imitating the player’s movements.  To determine the force of the arrow, a ball is attached to the controller and the player pulls back from the original position and the farther the position, the more force is being applied to the arrow. To determine the angle of trajectory for the arrow, the player moves the controller (Raspberry Pi Zero W/ Ozzmaker Berry IMU) in a vertical motion until the desired angle is achieved. When the buttons are released the arrow is fired at the target.

- Communication

		The game is designed using Unity where the scenes of the game and the animated characters are built. The communication between the hardwares (see Game Design below) and Unity is done through an MQTT broker at “broker.hivemq.com”. The process of data transmission is as follows, the data is transferred from the Raspberry Pi Zero W/Ozzmaker Berry IMU to the local computer using sockets where the Raspberry Pi Zero W/Ozzmaker Berry IMU are the clients and the local computer is the server that receives this data. To transfer the data to Unity, we used a HiveMQ broker to send the values needed to Unity in order to use it in the game.
- Game Design and Logic

		The design of the game is split into two parts, the first is the hardware, and the second is the software. The software is mainly used in communication. The hardware has multiple parts including the Raspberry Pi Zero W and the Ozzmaker Berry IMU. These two parts work together to calculate the force using the area of a ball that utilizes another hardware part which is the camera. They also find the angle of the trajectory which is determined by the motion of the Ozzmaker Berry IMU after pressing the buttons attached. The microphone is being used for speech recognition. The use of the microphone is being implemented directly into the game.

- Game Instructions

		1. Game starts from the scene called Mikes Main Menu in Unity
			a. If using the controller please make sure that you are running the Mac.py, opencvToMac.py files are running on your terminal windows. Also turn on the controller and ssh into your rpi files and run (sudo python 2piToMac.py)
			b. If using keyboard and mouse just press play and follow next steps
		2. After hitting the play button at the top of Unity the player will be directed to a screen to enter their username or alias.
		3. The player will then be sent to a menu that gives them the following options
			a. Single player (currently uses the controller only)
				i. Currently has three stages to win
				ii. Upon winning player will be sent to final scene where they can choose to restart the game or go back to the main menu
			b. Multiplayer MK (this is the mouse and keyboard multiplayer mode)
			c. Multiplayer (this is the controller multiplayer mode)
			d. Join Game MK (this is used to join existing Multiplayer MK games)
			e. Join Game (this is used to join existing Multiplayer games)
		4. When creating a multiplayer game the user must put in a lobby name that future players will use to join their game.
		5. Players will be selected in the order that they join the lobby.
		6. Multiplayer game modes are a race to a specific score. 
Stay Updated  

	1. Once logged into the Unity Collab System you will receive an email every time there is an update in the game 
	2. You will be able to download any updates by
		a. Clicking on the collab button in unity 
		b. Then click collab to add all the updates to the game  
