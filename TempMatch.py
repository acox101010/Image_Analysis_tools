# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:10:34 2019
@author: A8DPDZZ
updated 4/9/2019 for data analysis
"""
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

#Load Template and draw boundary
template = cv2.imread(r"M:\tempMatchTest\temp.jpg",0) #directory of template
w, h = template.shape[::-1] #finds shape of template
detectedObjects = 0 #variable for counting image iteration
#plt.imshow(template) #shows template

#Writing initial row to csv for data processing purposes
ofile  = open('match_results.csv', "w")
writer = csv.writer(ofile, delimiter=' ')
writer.writerow(["Data"])
ofile.close()

for fil in glob.glob("*.jpeg"):
    image = cv2.imread(fil) #read image global image files in directory
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    res = cv2.matchTemplate(gray_image,template,cv2.TM_CCOEFF_NORMED) #performs template matching
    threshold = 0.9 #set matching threshold. To be tuned further !!!
    loc = np.where(res >= threshold) #checks if template matches
    try:
        if np.any(loc[0]) > 0: 
            a = np.asarray(loc[0])[np.newaxis] #Transposes location matching coordinates
            detectedObjects = detectedObjects+1
            print(detectedObjects,"Template located in:",fil)
            
            for pt in zip(*loc[::-1]): #used for locating the matched template in the image
                cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
                plt.imshow(image)
                
            with open("match_results.csv",'a',newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ')
                spamwriter.writerow(["Located"])
        else:
            detectedObjects = detectedObjects+1
            print(detectedObjects,"Template not located in:",fil)
            
            with open("match_results.csv",'a',newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ')
                spamwriter.writerow(["NotLocated"])
            continue
    except KeyboardInterrupt:

        cv2.destroyAllWindows()
        cv2.waitKey(0)

#Execute Data Analysis with results
df = pd.read_csv('match_results.csv')
missdat = df.isnull()
missdat.head() #Count any missing rows?

#search for any missing data and count values
for column in missdat.columns.values.tolist():
    print(column)
    print (missdat[column].value_counts())
    print("")
    
#generate count statistics
for column in df.columns.values.tolist():
    print(column)
    print (df[column].value_counts())
    print("")

    