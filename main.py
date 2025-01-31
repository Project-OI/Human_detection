import cv2
from ultralytics import YOLO
import numpy as np
import time


model = YOLO("yolov8m.pt")

while True:
    #//////// voor cam stream van raspberry \\\\\\\\\\\\\
    url = "http://10.38.4.211:8080/project_oi"
    cap = cv2.VideoCapture(url)
    
    #////// live CAM \\\\\\\
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("piCam", frame)

    results = model(frame, device="mps") #mps is alleen mac en cpu voor andere pc's
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    aantal_personen = 0
    for cls, bbox in zip(classes, bboxes):
        (x, y, x2, y2) = bbox
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 225, 20), 2)
        cv2.putText(frame, result.names[cls], (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
        #print("x", x, "y", y)
        if result.names[cls] == "person":  # Controle of persoon in beeld zit
            print("Persoon gevonden")  # Print "persoon gevonden"
            aantal_personen += 1
    #print(bboxes) voor de coordinaten
    if aantal_personen > 0:
        print(f"Aantal personen gevonden: {aantal_personen}")


    cv2.imshow("Detection", frame)
    key = cv2.waitKey(1)
    if key == 27:           #met esc stop window
        break
    
    time.sleep(1/3)
    
    
cap.release()
cv2.destroyAllWindows()