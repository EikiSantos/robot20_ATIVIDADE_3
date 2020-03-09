# -*- coding: utf-8 -*-
import sys
import math
import cv2
import numpy as np
import math
import auxiliar as aux

video1 = cv2.VideoCapture("video1.mp4")
#video1 =cv2.rotate(video1, cv2.ROTATE_90_CLOCKWISE)
x_1 = 0
x_2 = 0
y_1 = 0
y_2 = 0
x_1r = 1
x_2r = 1
y_1r = 1
y_2r = 1
x_1l = 1
x_2l = 1
y_1l = 1
y_2l = 1
h_r=1.0
h_l=2.0
m_l=2.0
m_r=1.0


while(True):
    # Capture frame-by-frame
    ret, frame = video1.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    # Our operations on the frame come her
    #frame=cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    #cv2.Flip(frame, flipMode=-1)
    #cv.ShowImage('180_rotation', orig)
    #frame = rotateImage(frame, 180)
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
    
    if lines is not None:
        for i in range(0, len(lines)):
            r = lines[i][0][0]
            theta = lines[i][0][1]
     
            # Stores the value of cos(theta) in a 
            a = np.cos(theta) 
          
            # Stores the value of sin(theta) in b 
            b = np.sin(theta) 
              
            # x0 stores the value rcos(theta) 
            x0 = a*r 
              
            # y0 stores the value rsin(theta) 
            y0 = b*r 
              
            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
            x1 = int(x0 + 1000*(-b)) 
              
            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
            y1 = int(y0 + 1000*(a)) 
          
            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
            x2 = int(x0 - 1000*(-b))
            
            y2 = int(y0 - 1000*(a)) 
                
            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
            y2 = int(y0 - 1000*(a)) 
            deltay = y2 - y1
            deltax = x2 - x1
            m_inicial = float(deltay/deltax)
            lista_coef_ang = [-1.06,-2.71]
            if m_inicial >-5 and m_inicial <-1:
                m_r = m_inicial
                x_1r = x1
                x_2r = x2
                y_1r = y1
                y_2r = y2
                h_r = y_1r - m_r*x_1r
            elif m_inicial >0.5 and m_inicial < 1.61:
                m_l = m_inicial
                x_1l = x1
                x_2l = x2
                y_1l = y1
                y_2l = y2
                h_l = y_1l - m_l*x_1l
        #cv2.line draws a line in img from the point(x_1r,y_1r) to (x_2r,y_2r). 
        #cv2.line draws a line in img from the point(x_1l,y_1l) to (x_2r,y_2l).
        cv2.line(mask_white,(x_1r,y_1r), (x_2r,y_2r), (100,0,255),2)
        cv2.line(mask_white,(x_1l,y_1l), (x_2l,y_2l), (100,0,255),2)
        # (0,0,255) denotes the colour of the line to be  
        
        # Encontrando o intercepto
        xi = (h_r - h_l) / (m_l - m_r)
        yi = m_l*xi + h_l
        xii = int(xi)
        yii = int(yi)
        cv2.circle(mask_white,(xii,yii),20,(255,255,255),2)
        
        #drawn. In this case, it is red.  
        #cv2.line(mask_white,(x1,y1), (x2,y2), (100,0,255),2) 
          
    
    # Display the resulting frame
    # cv2.imshow('frame',frame)
    cv2.imshow('hsv', mask_white)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
video1.release()
cv2.destroyAllWindows()

#
#    if lines is not None:
#        for i in range(0, len(lines)):
#            rho = lines[i][0][0]
#            theta = lines[i][0][1]
#            a = math.cos(theta)
#            b = math.sin(theta)
#            x0 = a * rho
#            y0 = b * rho
#            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
#            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
#            cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
#    
#    
#    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
#    
#    if linesP is not None:
#        for i in range(0, len(linesP)):
#            l = linesP[i][0]
#            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
#    
#    cv.imshow("Source", src)
#    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
#    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
#    
#    cv.waitKey()
#    return 0
#
#if __name__ == "__main__":
#    main(sys.argv[1:])
