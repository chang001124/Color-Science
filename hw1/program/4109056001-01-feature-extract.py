import numpy as np
import cv2 as cv
import os
import csv
import re

def cal_features(img,filename):
    (B, G, R) = cv.split(img)
    with open('../feature/'+filename+'_dec.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([round(np.mean(R),2)])
        writer.writerow([round(np.std(R),2)])
        writer.writerow([round(np.mean(G),2)])
        writer.writerow([round(np.std(G),2)])
        writer.writerow([round(np.mean(B),2)])
        writer.writerow([round(np.std(B),2)])

def read_directory(directory_name):
    for filename in os.listdir(r"../"+directory_name):
        img = cv.imread('../'+directory_name + "/" + filename)
        cal_features(img,re.sub(".png","",filename))
       
read_directory("source")
read_directory("target")