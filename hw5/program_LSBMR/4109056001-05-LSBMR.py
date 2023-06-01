import numpy as np
import cv2
import random
import os
import re
import math
ratio=0.5
def f(x1,x2):
    if(math.floor(x1/2)+x2)%2==0:
        return 0
    return 1
def lsb(x1,x2,m1,m2):
    if(m1==x1%2):

        if(m2!=f(x1,x2)):
            random.seed(200)
            if(random.randint(0, 1)==0):
                if(x2-1<0):
                    y2=x2+1
                y2=x2-1
            else:
                if(x2+1>255):
                    y2=x2-1
                y2=x2+1
        else:
            y2=x2
        y1=x1
    else:
        if(m2 == f(x1-1,x2)):
            y1=x1-1
            if(x1-1<0):
                y1=x1+1
        else:
            if(x1+1>255):
                y1=x1-1
            y1=x1+1
        y2=x2
    m1=m1%2
    m2=f(y1,y2)
    return y1,y2,m1,m2
def read_directory(directory_name):
    for filename in os.listdir(r"../"+directory_name):
        img = cv2.imread('../'+directory_name + "/" + filename,cv2.IMREAD_GRAYSCALE)
        height,width = img.shape
        pixel_cnt = height*width
        msg_cnt = round(pixel_cnt * ratio)
        random.seed(100)
        secret_message = [random.randint(0, 1) for i in range(msg_cnt)]
        num=math.floor(len(secret_message)/2)
        stego=img.flatten()[:]
        check=[]
        #print(secret_message[0])
        #print(secret_message[1])
        a=0
        count=0
        for i in range(0,num): #0 1
            #print(img.flatten()[a],img.flatten()[a+1],secret_message[a],secret_message[a+1])
            #print(secret_message[a],secret_message[a+1])
            x1,x2,m1,m2=lsb(img.flatten()[a],img.flatten()[a+1],secret_message[a],secret_message[a+1])
            #print(x1,x2)
            check.append(m1)
            check.append(m2)
            stego[count]=x1
            count+=1
            stego[count]=x2
            count+=1
            #print(check[0])
            #print(check[1])
            #break
            a+=2
        #print("stego",stego[0])
        stego_img = np.array(stego, dtype = np.uint8)
        stego_img = np.reshape(stego_img,(height,width))
        stego_img = cv2.cvtColor(stego_img,cv2.COLOR_GRAY2BGR )
        cv2.imwrite('../stego/'+re.sub(".png","",filename)+'_stego_'+str(ratio)+'.png', stego_img)
        if(len(secret_message)%2!=0):
            check.append(secret_message[len(secret_message)-1])
        print(np.array_equal(secret_message,check))

            
read_directory("cover")


