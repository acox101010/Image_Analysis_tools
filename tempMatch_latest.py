import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

#fp_img = (r'C:\Users\Reaper124\Documents\Python Scripts\testimages') #filepath for all images
#fp_img_gry = (r'C:\Users\Reaper124\Documents\Python Scripts\testimages\grey')
#temp_cl = cv2.imread(r'C:\Users\Reaper124\Documents\Python Scripts\temp.png',0) #directory of image template
#mydir = (r'M:\ETR Testing Files\ETR-X380N-4935')  # Replace mydir with the directory you want

template = cv2.imread(r"C:\Users\A8DPDZZ\TestScripts\testfiles\temp2.jpg",0) #directory of template
w, h = template.shape[::-1] #finds shape of template
detectedObjects = 0 #variable for counting image iteration
plt.imshow(template) #shows template

for fil in glob.glob("*.jpg"):
    image = cv2.imread(fil) #read image global image files in directory
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    res = cv2.matchTemplate(gray_image,template,cv2.TM_CCOEFF_NORMED) #performs template matching
    threshold = 0.8 #set matching threshold. To be tuned further !!!
    loc = np.where(res >= threshold) #checks if template matches
    try:
        if np.any(loc[0]) > 0: 
            a = np.asarray(loc[0])[np.newaxis] #Transposes location matching coordinates
            detectedObjects = detectedObjects+1
            print(detectedObjects,"Template is a match in file:",fil)
            #for pt in zip(*loc[::-1]): #used for locating the matched template in the image
                #cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
                #cv2.imshow("Image",image)
                #cv2.waitKey(25)
            with open("foo.csv",'a',newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ')
                spamwriter.writerow([fil, "_TempMatch"])
        else:
            detectedObjects = detectedObjects+1
            print(detectedObjects,"Template not located in image:",fil)
            with open("foo.csv",'a',newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ')
                spamwriter.writerow([fil, "_NoMatch"])
            continue
    except KeyboardInterrupt:
        
        cv2.destroyAllWindows()
        cv2.waitKey(0)
