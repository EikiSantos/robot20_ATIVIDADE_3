import cv2
import numpy as np
import math
import auxiliar as aux

video1 = cv2.VideoCapture("video1.mp4")
coef_angular = 0
coef_angular_anterior = 0
x_1 = 0
x_2 = 0
y_1 = 0
y_2 = 0


while(True):

    ret, frame = video1.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    white = "#ffffff"
    white_1, white_2 = aux.ranges(white)
    mask_white = cv2.inRange(hsv, white_1, white_2)
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 
    lines = cv2.HoughLines(edges,1,np.pi/180, 200) 
    
    for r,theta in lines[0]: 

        a = np.cos(theta) 

        b = np.sin(theta) 

        x0 = a*r 

        y0 = b*r 

        x1 = int(x0 + 1000*(-b)) 

        y1 = int(y0 + 1000*(a)) 
      
        x2 = int(x0 - 1000*(-b)) 

        y2 = int(y0 - 1000*(a)) 
        
        delta_x = x1-x2
        delta_y = y1-y2
        print("DELTA X: ", delta_x)
        print("DELTA Y: ", delta_y)
        coef_angular = delta_y/delta_x
        modulo_coef = ((coef_angular - coef_angular_anterior)**2)**0.5
        if modulo_coef > 0.3:
            coef_angular_anterior = coef_angular
            print("TESTEEEEE")
        print("COEF ANGULAR: ", coef_angular)
        print("MODULO COEF: ", modulo_coef)
        if modulo_coef > 0.5:
            x_1 = x1
            x_2 = x2
            y_1 = y1
            y_2 = y2

        cv2.line(gray,(x1,y1), (x2,y2), (0,0,255),2) 

    cv2.imshow('hsv', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video1.release()
cv2.destroyAllWindows()

