# -*- coding: UTF-8 -*-
# client.py

import cv2
import time
import socket
from PIL import Image
from io import BytesIO

#get camera
cap = cv2.VideoCapture(0)
#change picture size 640*480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

HOST, PORT = '192.168.0.108', 8000
#connect to host
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
  ret, img = cap.read()  #get one frame picture
  if ret is False:       #if get nothing exit
    print("can not get this frame")
    continue
  
  
  pi = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  #replace opencv picture format with PIL format
  buf = BytesIO()             #store in buffer
  pi.save(buf, format = 'JPEG')         #compress PIL picture to jpeg format and write to buffer
  jpeg = buf.getvalue()                 #read jpeg from buffer
  buf.close()
  sock.sendall(jpeg)         #transmit jpeg to server

'''
cap.release()                           #close camera
cv2.destroyAllWindows()                 #close window
'''
sock.close()                            #close socket
