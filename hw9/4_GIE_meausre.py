import cv2
import os
import re
import csv
from scipy.stats import entropy

with open('statis/GIE_res.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['GIE', '', 'Plain', '', '', 'Cipher'])
    writer.writerow(['Image', 'Type', 'Red', 'Green', 'Blue', 'Red', 'Green', 'Blue'])


def gie(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    histogram = hist / (image.shape[0] * image.shape[1])

    return entropy(histogram, base=2)


for filename in os.listdir(r"source"):
    cipher_img = cv2.imread("encryp/" + re.sub(".png", "", filename) + "_enc.png")
    plain_img = cv2.imread("source/" + filename)

    with open('statis/GIE_res.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([re.sub(".png", "", filename), 'grey',
                         gie(plain_img)[0], '', '', gie(cipher_img)[0]])
