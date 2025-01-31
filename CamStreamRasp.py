#Dit is de code dat op de Raspberry pi staat om de camera beelden te streamen over wifi
import cv2
import time
from mjpeg_streamer import MjpegServer, Stream


time.sleep(12)
cap = cv2.VideoCapture(0)
stream = Stream("project_oi", size=(640,480), quality=30, fps=30)

server = MjpegServer("10.38.4.211", 8080)
server.add_stream(stream)
server.start()

while True:
    _, frame = cap.read()
    #cv2.imshow(stream.name, frame)
    key =  cv2.waitKey(1)
    if key == 27:
        break
    
    stream.set_frame(frame)
    
server.stop()
cap.release()
cv2.destroyAllWindows()