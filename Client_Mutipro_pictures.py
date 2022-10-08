# -*- coding: UTF-8 -*-
# server

import cv2
import numpy as np
import time
import os
import socket
from multiprocessing import Process, Queue

# This function will process picture from Raspberry pi
# Input: Image savepath, queue to receive image, queue to receive command
def drawcircle(folder,q,c):
    num = 0
    while True: 
        num+=1
        frame = cv2.circle(q.get(),(280,280),8,(255,0,0),0,cv2.LINE_8)
        time.sleep(0.2)
        
        cv2.imwrite(folder + "/Image" + str(num) +'.jpg', frame)
        cv2.imshow('capturing', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    c.get()
    quit()

# This function will accept data from raspberry pi by socket
# Input: serve socket, image savepath, queue to receive image, queue to receive command
def VideoStreamingTest(server_socket,folder,q,c): 
    num = 0
    while True:
        connection, client_address = server_socket.accept() 
        connection = connection.makefile('rb')
        stream_bytes = b' '
        
        while True:
            num+=1
            stream_bytes += connection.read(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imwrite(folder + "/Image" + str(num) +'.jpg', image)
                if q.empty() ==1:
                    q.put(image)
                if c.empty() == 1:
                    break
        connection.close()
        break
    server_socket.close()
    quit()

# This function will create the folder to save image, the path is the same as this .py file
# Input: folder name
def mkfolder(name):
    
    folder = os.getcwd() + name
    if not os.path.exists(folder):
        os.makedirs(folder) 
    return folder
    

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 8000))
    server_socket.listen()
    
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Host: ", host_name + ' ' + host_ip)
    print("Streaming...")
    print("Press 'q' to exit")
    
    folder1 = mkfolder('\\Raspi_Picature')   # make folder to save image from Raspberry pi
    folder2 = mkfolder('\\Processed_Picature')  # make folder to save processed image
    
    q = Queue()  # create a queue to transmit image between two processes
    c = Queue()  # creat a queue to control two processes
    c.put('start')
    
    p1 = Process(target=VideoStreamingTest, args=(server_socket,folder1,q,c,))  # set p1 process to receive picture 
    p2 = Process(target=drawcircle, args=(folder2,q,c,))   # set p2 process to deal with these pictures
    p1.start()
    p2.start()
    
    if q.empty() ==1 and c.empty()==1:  # when no picture and no command stop two processes 
        p1.join()
        p2.join()
        
        
if __name__ == '__main__':
    main()