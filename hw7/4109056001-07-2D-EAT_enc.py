import numpy as np
import cv2
import os
import re
G=120 #times
a=1
b=1
def matrix(a, b):
    """
    :param a: a
    :param b: b
    :return: matrix [[a*b+1, a], [b, 1]]
    """
    return np.array([[a * b + 1, a], [b, 1]])

def eta(position, m, N):
    """
    :param position: (i, j)
    :param m: matrix
    :param N: N
    :return: eta(i, j)
    """
    return np.dot(m, position) % N

for filename in os.listdir(r"source"):
    #print(filename)
    img = cv2.imread("source/" + filename,cv2.IMREAD_GRAYSCALE)
    N = img.shape[0]
    #print(N)
    m = matrix(a,b)
    new_img = np.zeros_like(img)  # create a new array with the same shape as img

    for (i, j), pixel_value in np.ndenumerate(img):
        # print(f"Encrypting {i}, {j}")
        new_position = np.array([i, j])
        for g in range(G):
            new_position = eta(new_position, m, N)
        new_img[new_position[0], new_position[1]] = pixel_value
    img=new_img
    cv2.imwrite("encryp/"+re.sub(".png","",filename)+"_enc.png", img)
    #
        


