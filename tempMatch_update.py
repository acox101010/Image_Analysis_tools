# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:10:34 2019

@author: A8DPDZZ
"""
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
#fp_img = (r'C:\Users\Reaper124\Documents\Python Scripts\testimages') #filepath for all images
#fp_img_gry = (r'C:\Users\Reaper124\Documents\Python Scripts\testimages\grey')
#temp_cl = cv2.imread(r'C:\Users\Reaper124\Documents\Python Scripts\temp.png',0) #directory of image template

mydir = (r'C:\Users\A8DPDZZ\TestScripts\testfiles')  # Replace mydir with the directory you want
template = cv2.imread(r"C:\Users\A8DPDZZ\TestScripts\temp1.jpg",0) #directory of template
w, h = template.shape[::-1] #finds shape of template
detectedObjects = 0 #list for storing detected object location in image
plt.imshow(template) #shows template

for fil in glob.glob("*.jpg"):
    image = cv2.imread(fil) 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    res = cv2.matchTemplate(gray_image,template,cv2.TM_CCOEFF_NORMED) #performs template matching
    threshold = 0.3 #set matching threshold. To be tuned further !!!
    loc = np.where(res >= threshold) #checks if template matches
    try:
        if np.any(loc[0]) > 0: 
            print(loc[0])
            a = np.asarray(loc[0])
            detectedObjects = detectedObjects+1
            print(detectedObjects,"Filename is:",fil)
            np.savetxt("foo.csv", a, delimiter="")
        else:
            print("Template not located in image:",fil)
            continue
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        cv2.waitKey(1)
