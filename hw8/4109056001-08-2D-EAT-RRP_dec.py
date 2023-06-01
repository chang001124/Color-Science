import numpy as np
import cv2
import os
import re
import random
G=120 #times
a=1
b=1
random.seed(100)
def matrix(a, b):
    """
    :param a: a
    :param b: b
    :return: matrix [[a*b+1, a], [b, 1]]
    """
    return np.array([[1 , a], [b, a*b+1]])

def eta(position, m, N):
    """
    :param position: (i, j)
    :param m: matrix
    :param N: N
    :return: eta(i, j)
    """
    return np.dot(m, position) % N

def binary_array_to_decimal(binary_array):
    decimal = 0
    power = len(binary_array) - 1
    for digit in binary_array:
        decimal += digit * (2 ** power)
        power -= 1
    return decimal

def ran_per(pixel_value):
    #print(pixel_value)
    binary = bin(pixel_value)[2:]
    arr= []
    rev=[]
    count=7
    for i in range (8):
        arr.append(0)
    for i in range (len(binary)-1,-1,-1):
        arr[count]=int(binary[i])
        count-=1
    #random.seed(100)
    for i in range(8,1,-1):
        rev.insert(0, random.randint(0, 100) % i)
    #print(rev)
    for i in range(1,8):
        temp=arr[i]
        arr[i]=arr[rev[i-1]]
        arr[rev[i-1]]=temp
        
    #print(arr)
    #print(binary_array_to_decimal(arr))

    return binary_array_to_decimal(arr);

for filename in os.listdir(r"encryp"):
    #print(filename)
    img = cv2.imread("encryp/" + filename,cv2.IMREAD_GRAYSCALE)
    N = img.shape[0]
    #print(N)
    m = matrix(a,b)
    m=np.linalg.inv(m).astype(int)
    new_img = np.zeros_like(img)  # create a new array with the same shape as img

    for (i, j), pixel_value in np.ndenumerate(img):
        # print(f"Encrypting {i}, {j}")
        new_position = np.array([i, j])
        for g in range(G):
            new_position = eta(new_position, m, N)
        new_img[new_position[0], new_position[1]] = pixel_value
    img=new_img
    
    for (i, j), pixel_value in np.ndenumerate(img):
        # print(f"Encrypting {i}, {j}")
        new_position = np.array([i, j])
        new_img[new_position[0], new_position[1]] = ran_per(pixel_value)
    img=new_img
    cv2.imwrite("decryp/"+re.sub("enc.png","",filename)+"dec.png", img)
    #
     


