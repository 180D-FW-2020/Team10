There are 3 Windows executable python code documents in this folder; "2piToMac.py", "Mac_MR.py" and "opencvToWin.py". The rest are just supporting files.
"2piToMac.py" sends IMU data from the raspberry pi to the local computer using HiveMQ IOT transmission
"opencvToWin.py" processes the images on the computer's camera, detecting the ball and sending the Y-axis center of the ball and the area of the ball to the MQTT channel.
"Mac_MR.py" sets up the local computer connection that recieves all of the above mentioned data.
