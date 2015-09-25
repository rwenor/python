import cv2
import time

cap = cv2.VideoCapture(0)
i = 0
b,frame = cap.read()  # Les forste bilde

print "Start"
t0 = time.time()
while True:
    b,frame = cap.read()
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
    i += 1
    #print i
    t = time.time() - t0
    #print t
    
    if t >  30:
        break

print "Bilder i sekundet: ", i / t

cap.release()
cv2.destroyAllWindows()
