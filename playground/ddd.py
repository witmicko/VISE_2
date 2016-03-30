import numpy as np
import cv2

cap = cv2.VideoCapture('Video 3.mp4')
face_cascade = cv2.CascadeClassifier('C:/opencv/build/install/etc/haarcascades/cascade.xml')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3, 6)
    # faces = face_cascade.detectMultiScale(image=gray,
    #                                       scaleFactor=1.0,
    #                                       minNeighbors=1)
                                          # minSize=,
                                          # maxSize=)
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = gray[y:y + h, x:x + w]
        print(x, y, w, h)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()