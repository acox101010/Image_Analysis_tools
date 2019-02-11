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
#fp_img = (r'C:\Users\Reaper124\Documents\Python Scripts\testimages') #filepath for all images
#fp_img_gry = (r'C:\Users\Reaper124\Documents\Python Scripts\testimages\grey')
#temp_cl = cv2.imread(r'C:\Users\Reaper124\Documents\Python Scripts\temp.png',0) #directory of image template

#for roots, dirs, files in os.walk(fp_img):
mydir = (r'C:\Users\A8DPDZZ\TestScripts\testfiles')  # Replace mydir with the directory you want
template = cv2.imread(r"C:\Users\A8DPDZZ\TestScripts\temp1.jpg",0) #directory of template
w, h = template.shape[::-1] #finds shape of template
detectedObjects = 0 #list for storing detected object location in image

for fil in glob.glob("*.jpg"):
    image = cv2.imread(fil) 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    res = cv2.matchTemplate(gray_image,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.2
    loc = np.where(res >= threshold)
    np.asarray(loc)
    try:
        if loc[0:] != None:
            print(loc[0])
            detectedObjects = detectedObjects+1
            print(detectedObjects)
        else:
            continue
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    #cv2.imwrite(os.path.join(mydir,fil),gray_image) # write to location with same name
    #for fil in zip(*loc[::-1]):
     #   cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
      #  cv2.imshow('Detected',image)
       # cv2.waitKey(25)
    
