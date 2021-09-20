
import base64
import cv2
import zmq
import numpy as np
import time

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://127.0.0.10:5555')

camera = cv2.VideoCapture('rtsp://admin:LIRROY@196.221.205.130:554/H.264')  # init the camera

while True:
        try:
                grabbed, frame = camera.read()  # grab the current frame
                frame = cv2.resize(frame, (640, 480))  # resize the frame
                encoded, buffer = cv2.imencode('.jpg', frame)
                footage_socket.send(buffer)


        except KeyboardInterrupt:
                camera.release()
                cv2.destroyAllWindows()
                break
