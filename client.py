# -*- coding: UTF-8 -*-
# src_camera.py

import cv2
import time
import socket
from PIL import Image
from io import BytesIO

#获取摄像头
cap = cv2.VideoCapture(0)
#调整采集图像大小为640*480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

HOST, PORT = '192.168.0.108', 8000
#连接服务器
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
  ret, img = cap.read()  #获取一帧图像
  if ret is False:       #未获取图像时，退出循环
    print("can not get this frame")
    continue
  
  
  pi = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  #将OpenCV下的图像转换成PIL支持的格式
  buf = BytesIO()             #缓存对象
  pi.save(buf, format = 'JPEG')         #将PIL下的图像压缩成jpeg格式，存入内存中的字符串
  jpeg = buf.getvalue()                 #从buf中读出jpeg格式的图像
  buf.close()
  transfer = jpeg
  print(len(transfer))
  print(transfer[-1])
  sock.sendall(transfer)         #通过socket传到服务器

'''
cap.release()                           #释放摄像头
cv2.destroyAllWindows()                 #关闭所有窗口
'''
sock.close()                            #关闭socket