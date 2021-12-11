
import numpy as np
import cv2
from math import sqrt
import os

def solution(obs):
    image = cv2.cvtColor(obs, cv2.COLOR_BGR2HSV)
    Y,X, _ = image.shape
    centrX = int(X/2)
    centrY = int(Y/2)
    angle = 0
    vel = 0.45
    xRazmetkaYpred = -int(centrX/2)
    xWhitelinepred = centrX-100
    loop = 0
    xRazmetkaY = 0
    y_min = np.array((63, 142, 165), np.uint8)
    y_max = np.array((137, 184, 233), np.uint8)
    l_min = np.array((130, 121, 139), np.uint8)
    l_max = np.array((186, 189, 186), np.uint8)
    razmetka = cv2.inRange(image, y_min, y_max)
    whiteline = cv2.inRange(image, l_min, l_max)
    cntRazmetkaY, _ =  cv2.findContours(razmetka,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cntRazmetkaY = sorted(cntRazmetkaY, key = cv2.contourArea,reverse = True)
    cntWhiteline, _ =  cv2.findContours(whiteline,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cntWhiteline = sorted(cntWhiteline, key = cv2.contourArea,reverse = True)
    x2 = 0
    count = 0
    if len(cntRazmetkaY)>=2:
        rect = cv2.minAreaRect(cntRazmetkaY[0])
        cord,_,_ = rect
        x0,y0 = cord
        x0 = int(x0)
        y0 = int(y0)
        index0 = 0
        index1 = 0
        for i in range (len(cntRazmetkaY)):
            if cv2.contourArea (cntRazmetkaY[i]) > 30:
                rect = cv2.minAreaRect(cntRazmetkaY[i])
                cord,_,_ = rect
                x,y = cord
                x = int(x)
                y = int(y)
                if y > centrY:
                    if abs(x0-x)<70 and int(sqrt(np.power((x-x0), 2)+np.power((y-y0),2)))<70:
                        if count == 0:
                            index0 = i
                        index1 = i
                        count +=1
                x0 = x
                y0 = y       
        if count>0:
            rect = cv2.minAreaRect(cntRazmetkaY[index0])
            cord,_,_ = rect
            x1,_ = cord
            x1 = int(x1)
            rect = cv2.minAreaRect(cntRazmetkaY[index1])
            cord,_,_ = rect
            x2,_ = cord
            x2 = int(x2)
            if x2>0 and x1>0:
                xRazmetkaYpred = int((x2+x1)/1.5)
        if xRazmetkaYpred>int(centrX+(int(centrX/3))):
            xRazmetkaYpred = int(centrX-(int(centrX/2)))
        raschet = 1
    k = 0.042
    if xRazmetkaY == xRazmetkaYpred and loop == 1:
        k = 0.064
    xRazmetkaY = xRazmetkaYpred
    poloz = int((int(X-(X/16)) + xRazmetkaY)/2)
    razn = centrX - poloz
    if razn >= 1:
        angle = k*razn
    if razn < -1:
        angle = k*razn
    loop =1
    return[vel,angle]



