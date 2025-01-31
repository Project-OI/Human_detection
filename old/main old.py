#Dit is een test code. Bedoelt voor het testen van alleen de mens herkenning via webcam of een videobestand.
import cv2
from ultralytics import YOLO
import numpy as np


#test videos cap = cv2.VideoCapture("dags.mp4")
#//////// voor live cam \\\\\\\\\\\\\
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


model = YOLO("yolov8m.pt")

while True:
    #// test video \\\\\\
    #ret, frame = cap.read() #haalt frames op
    #if not ret:
    #    break              #stopt als de video klaar is
    
    #////// live CAM \\\\\\\
    ret, frame= cap.read()
    cv2.imshow('webcam', frame)
    
    
    results = model(frame, device="mps") #mps is alleen mac
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    for cls, bbox in zip(classes, bboxes):
        (x, y, x2, y2) = bbox
        
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 225, 20), 2)
        cv2.putText(frame, result.names[cls], (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
        #print("x", x, "y", y)
        
        if result.names[cls] == "person":  # Controle of persoon in beeld zit
            print("Persoon gevonden")  # Print "persoon gevonden"
    
    #print(bboxes)  #voor de cordinaten

    cv2.imshow("img", frame)
    key = cv2.waitKey(1)
    if key == 27:           #met esc stop window
        break
    
cap.release()
cv2.destroyAllWindows()