import cv2
import os
import re
import csv
from scipy.stats import kendalltau
import random

K = 8000
with open('statis/COR_res.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['COR', '', 'Plain', '', '', '', '', '', '', '', '', 'Cipher'])
    writer.writerow(
        ['Sample', '8000', 'red', '', '', 'green', '', '', 'blue', '', '', 'red', '', '', 'green', '', '', 'blue'])
    writer.writerow(
        ['Image', 'Type', 'horizontal', 'vertical', 'diagonal', 'horizontal', 'vertical', 'diagonal', 'horizontal',
         'vertical', 'diagonal', 'horizontal', 'vertical', 'diagonal', 'horizontal', 'vertical', 'diagonal',
         'horizontal', 'vertical', 'diagonal'])


def tran(s, N):
    x = s // N
    y = s % N
    return x, y


def cor(img):
    N = img.shape[0]
    num_range = ((img.shape[0] - 1) * (img.shape[1] - 1)) // K
    src = []
    hor = []
    ver = []
    dia = []
    for i in range(K):
        x, y = tran(random.randint(i * num_range, (i + 1) * num_range), N - 1)
        src.append(img[x][y])
        hor.append(img[x][y + 1])
        ver.append(img[x + 1][y])
        dia.append(img[x + 1][y + 1])
    h, _ = kendalltau(src, hor)
    v, _ = kendalltau(src, ver)
    d, _ = kendalltau(src, dia)
    return h, v, d


for filename in os.listdir(r"source"):
    cipher_img = cv2.imread("encryp/" + re.sub(".png", "", filename) + "_enc.png")
    plain_img = cv2.imread("source/" + filename)
    plain = cor(plain_img)
    cipher = cor(cipher_img)
    with open('statis/COR_res.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([re.sub(".png", "", filename), 'grey',
                         plain[0], plain[1], plain[2], '', '', '', '', '', '', cipher[0], cipher[1], cipher[2]])
