# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:26:23 2019

@author: A8DPDZZ
"""
#Load libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

#load image
img_loc = (r"C:\Users\A8DPDZZ\Documents\Test Development\ImgAnalysis\samplePix.jpg")
img = cv2.imread(img_loc)
print("ImgSize and Type:", img.size, img.dtype) #check image information

#Image Prep
img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blr = cv2.GaussianBlur(img_gry,(5,5),0)
f, ax = plt.subplots(2,2,figsize=(10,7))
plt.subplot(121),plt.imshow(img),plt.title('Original')
#plt.xticks([]), plt.yticks([]) #remove ticks if necessary
plt.subplot(122),plt.imshow(img_blr),plt.title('Processed')
#plt.xticks([]), plt.yticks([]) #remove ticks if necessary
plt.show()

#Crop Image to remove icons
cr_roi = img_blr[0:775, 375:1300]
f, ax = plt.subplots(1,1,figsize=(10,7))
plt.title('Cropped Image', fontdict=None, loc='center', pad=None, fontsize = 20)
plt.imshow(cr_roi) #plot last image with all points

#Draw rectangle to determine crosshair area
cv2.rectangle(cr_roi, (475, 385), (560, 475), (50, 50, 50), 2) #Draw bounding area for crosshair extraction
f, ax = plt.subplots(1,1,figsize=(10,7))
plt.title('Crosshair Removal Area', fontdict=None, loc='center', pad=None, fontsize = 20)
plt.imshow(cr_roi) #plot last image with all points

#Set determined crosshair area to 0 
cr_roi[385:475,475:560] = 0
f, ax = plt.subplots(1,1,figsize=(10,7))
plt.title('Cropped Image', fontdict=None, loc='center', pad=None, fontsize = 20)
plt.imshow(cr_roi) #plot last image with all points

#Checks image for max and min pixel values
print("Greatest pixel value:",np.ndarray.max(cr_roi),"Least pixel value:",np.ndarray.min(cr_roi))

ret,imgO = cv2.threshold(cr_roi,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
f, ax = plt.subplots(1,1,figsize=(10,7))
plt.title('Otsu Thresh Image', fontdict=None, loc='center', pad=None, fontsize = 20)
plt.imshow(imgO) #plot last image with all points

#Select the whether min or max for dead pixels depending on the thermal target
thresh = np.ndarray.max(imgO)
locat = np.where(imgO >= thresh)
print(locat, np.count_nonzero(locat))

#Locates NR pixel on image
rad = 10
for pt in zip(*locat[::-1]): 
    cv2.circle(imgO, pt, rad, (255,255,255),2)
f, ax = plt.subplots(1,1,figsize=(10,7))
plt.title('Identified Pixels', fontdict=None, loc='center', pad=None, fontsize = 20)
plt.imshow(imgO) #plot last image with all points

#Plot histogram of greyscale and thresholded image
f, ax = plt.subplots(2,2,figsize=(15,5))
plt.subplot(121),plt.hist(cr_roi.ravel(),256,[0,256]),plt.title('Histogram of Greyscale Values',
                                                               fontdict=None,
                                                               loc='center',
                                                               pad=None,
                                                               fontsize=20)
plt.subplot(122),plt.hist(imgO.ravel(),256,[0,256]),plt.title('Histogram of Thesh Values',
                                                               fontdict=None,
                                                               loc='center',
                                                               pad=None,
                                                               fontsize=20)
plt.show()
