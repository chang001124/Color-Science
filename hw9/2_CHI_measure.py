import cv2
import os
import re
import csv
import numpy as np
from scipy.stats import chi2

alpha = 0.05
chi_aquare_value = 293.248
with open('statis/CHI_res.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['CHI', '', 'Cipher', '', '', '', '', 'Results'])
    writer.writerow(['Image', 'Type', 'Red', 'Green', 'Blue', 'alpha', 'chi value', 'Red', 'Green', 'Blue'])


def chi(cipher_img):
    cipher_hist = cv2.calcHist([cipher_img], [0], None, [256], (0, 256))
    # print(cipher_hist[0])

    """expected_frequency = np.sum(hist) / len(hist)
    chi2_value = np.sum((hist - expected_frequency) ** 2 / expected_frequency)
    degrees_of_freedom = len(hist) - 1
    p_value = 1 - chi2.cdf(chi2_value, degrees_of_freedom)
    print(chi2_value)
    print(p_value)
    return chi2_value"""
    # print(sum(hist))
    # expect=np.mean(hist)
    # print(expect)
    # print(hist[0])
    expect = 0
    for i in range(256):
        expect += (cipher_hist[i] * i)
    expect = expect / (len(cipher_hist))
    total = 0
    for i in range(256):
        total += ((cipher_hist[i] - expect) ** 2) / (expect)

    """for i in range(1,256):
        expect=(cipher_hist[i]*i)/(len(cipher_hist))
        if(expect!=0):
            total+=((plain_hist[i]-expect)**2)/(expect)"""
    # total=np.sum(((plain_hist-cipher_hist)**2)/(cipher_hist+1e-10))

    # print(total)

    if (total <= chi_aquare_value):
        return 'Pass'
    return 'Fail'


for filename in os.listdir(r"source"):
    cipher_img = cv2.imread("encryp/" + re.sub(".png", "", filename) + "_enc.png")

    with open('statis/CHI_res.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([re.sub(".png", "", filename), 'grey',
                         '', '', '', alpha, chi_aquare_value, chi(cipher_img)])
