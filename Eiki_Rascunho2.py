import cv2
import numpy as np
import math
import auxiliar as aux

n = input("Qual numero do video gostaria de rodar? (1/2/3)")
while n!="1" and n!="2" and n!="3":
    n = input("Digite 1, 2 ou 3, por favor!")
#n = "2"
video = "video{0}.mp4".format(n)
video1 = cv2.VideoCapture(video)
coef_angular = 0
coef_angular_anterior = 0
x_1 = 0
x_2 = 0
y_1 = 0
y_2 = 0
x_r1 = 0
x_r2 = 0
y_r1 = 0
y_r2 = 0
x_l1 = 0
x_l2 = 0
y_l1 = 0
y_l2 = 0
h_l = 1.0
h_r = 2.0
m_l = 2.0
m_r = 1.0
rx_mean = []
ry_mean = []
rx = 0
ry = 0
i = 0
while(True):

    ret, frame = video1.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    white = "#eb4034"
    white_1, white_2 = aux.ranges(white)
    branco_1 = np.array([0, 0, 210], dtype=np.uint8)
    branco_2 = np.array([255, 40, 255], dtype=np.uint8)
    mask_white = cv2.inRange(hsv, branco_1, branco_2)
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 
    lines = cv2.HoughLines(mask_white,1,np.pi/180, 200) 
    
    for i in range(0, len(lines)): 
        r = lines[i][0][0]
        theta = lines[i][0][1]
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
        if delta_x == 0:
            coef_angular = 0
            print("PULEI")
        else:
            coef_angular = delta_y/delta_x
        modulo_coef = ((coef_angular - coef_angular_anterior)**2)**0.5
        if modulo_coef > 0.3:
            coef_angular_anterior = coef_angular
        coef_angular = float(coef_angular)
        print(' ')
        print(' ')
        print("COEF ANGULAR: ", coef_angular)
        print(' ')
        if n == "1":
            if coef_angular > 0.6 and coef_angular < 3.84:
                x_r1 = x1
                x_r2 = x2
                y_r1 = y1
                y_r2 = y2
                m_r = coef_angular
                h_r = y_r1 - m_r*x_r1
                
                print("------------------------RIGHT----------------------")
            elif coef_angular > -2.2 and coef_angular < -0.6:
                x_l1 = x1
                x_l2 = x2
                y_l1 = y1
                y_l2 = y2
                m_l = coef_angular
                h_l = y_l1 - m_l*x_l1
                print("------------------------LEFT----------------------")
        elif n == "2":
            if coef_angular > 3 and coef_angular < 4:
                x_r1 = x1
                x_r2 = x2
                y_r1 = y1
                y_r2 = y2
                m_r = coef_angular
                h_r = y_r1 - m_r*x_r1
                
                print("------------------------RIGHT----------------------")
            elif coef_angular > -1.1 and coef_angular < -0.67:
                x_l1 = x1
                x_l2 = x2
                y_l1 = y1
                y_l2 = y2
                m_l = coef_angular
                h_l = y_l1 - m_l*x_l1
                print("------------------------LEFT----------------------")
        elif n == "3":
            if coef_angular > 0.9 and coef_angular < 3.84:
                x_r1 = x1
                x_r2 = x2
                y_r1 = y1
                y_r2 = y2
                m_r = coef_angular
                h_r = y_r1 - m_r*x_r1
                
                print("------------------------RIGHT----------------------")
            elif coef_angular > -2.2 and coef_angular < -0.5:
                x_l1 = x1
                x_l2 = x2
                y_l1 = y1
                y_l2 = y2
                m_l = coef_angular
                h_l = y_l1 - m_l*x_l1
                print("------------------------LEFT----------------------")
        #cv2.line(mask_white,(x1,y1), (x2,y2), (50,0,255),2)
    cv2.line(mask_white,(x_l1, y_l1), (x_l2,y_l2), (50,0,255),2) 
    cv2.line(mask_white,(x_r1,y_r1), (x_r2,y_r2), (50,0,255),2)
    xi = (h_r-h_l)/(m_l-m_r)
    yi = (m_l*xi + h_l)
    xii = int(xi)
    yii = int(yi)
    #while i < 20:
#        rx_mean.append(xii)
#        ry_mean.append(yii)
#        rx = np.mean(rx_mean)
#        ry = np.mean(ry_mean)
#        rx = int(rx)
    #if i < 20:
        #i += 1
    #if i >= 20:
    #    i = 0
    #    rx_mean = []
    #    ry_mean = []
    #ry = int(ry)
    #print(type(rx))
    #print(type(ry))
    cv2.circle(mask_white, (xii, yii), 2, (255,255,255), 2)
    cv2.circle(mask_white, (xii, yii), 10, (255,255,255), 2)
    #cv2.circle(mask_white, (rx, ry), 50, (255,255,255), 2)
#    font = cv2.FONT_HERSHEY_SIMPLEX
#    cv2.putText(mask_white,'Coeficiente Angular: {0}'.format(m_r),(0,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('mask_white', mask_white)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video1.release()
cv2.destroyAllWindows()