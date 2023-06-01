import cv2
import os
import re
import csv
import numpy as np

with open('statis/VOH_res.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['VOH', '', 'Plain', '', '', 'Cipher'])
    writer.writerow(['Image', 'Type', 'Red', 'Green', 'Blue', 'Red', 'Green', 'Blue'])


def voh(img):
    hist = cv2.calcHist([img], [0], None, [256], (0, 256))
    return np.var(hist)


for filename in os.listdir(r"source"):
    # print(filename)
    plain_img = cv2.imread("source/" + filename)
    cipher_img = cv2.imread("encryp/" + re.sub(".png", "", filename) + "_enc.png")
    with open('statis/VOH_res.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([re.sub(".png", "", filename), 'grey',
                         voh(plain_img), '', '', voh(cipher_img), '', ''])
