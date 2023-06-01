import numpy as np
import cv2 as cv

def check(factor):
    if(factor > 255):
        factor = 255
    elif(factor < 0):
        factor = 0
    return factor

for i in range(1,7):
    s_img = cv.imread('../bctresult/' + 'sou-0'+str(i)+'.png')
    (SB, SG, SR) = cv.split(s_img)
    t_img = cv.imread('../bctresult/' + 'tar-0'+str(i)+'.png')
    (TB, TG, TR) = cv.split(t_img)
    #print(round(np.mean(SR),2),round(np.std(SR),2),round(np.mean(TR),2),round(np.std(TR),2))
    R= check(np.std(TR) / np.std(SR)) * (SR-np.mean(SR)) + np.mean(TR)
    G= check(np.std(TG) / np.std(SG)) * (SG-np.mean(SG)) + np.mean(TG)
    B= check(np.std(TB) / np.std(SB)) * (SB-np.mean(SB)) + np.mean(TB)
    img = cv.merge([B, G, R])
    cv.imwrite('../bctresult/res-0'+str(i)+'.png', img)