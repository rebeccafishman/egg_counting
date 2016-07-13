# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 16:03:33 2016

@author: Greencomp
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import color
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.measure import regionprops
from skimage.draw import circle_perimeter,circle_perimeter_aa
import time
#import os
import cv2
import scipy
import sys
from os import rename,listdir,path 
directory = '../Data/individualPics/07-12-2016/'#'../Data/19-May-2016/'
directory = '../Data/stitched/07-12-16/'

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
#counter = 0
refPt =[]

def click_and_count(event,x,y, flags, param):
	# grab references to the global variables
	global counter, refPt
  
	# check to see if the left mouse button was released
	if event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		#refPt.append((x, y))
		refPt = [(x,y)] #print "ya clicked!" #cropping = False
		counter = counter+1
		#print "counter = ",counter
 
		#small = cv2.resize(image, (0,0), fx=0.5, fy=0.5)#small = scipy.misc.imresize(image,0.5)#image2 = cv2.resize(image, (25, 50))  #cv2.putText(image, 'X',refPt[0],1,(255,0,255))#draw a rectangle around the region of interest
		cv2.circle(small, refPt[0],19, (255, 0, 0), 2)
		cv2.imshow("image", small)
	if event == cv2.EVENT_RBUTTONUP:
           refPt = [(x,y)]
           counter = counter-1
           #cv2.circle(small,refPt[0],1,(255,255,255),2)
           cv2.putText(small,'X',refPt[0], 1, 5, (0,0,255), 5)#, cv2.LINE_AA)
           cv2.imshow('image',small)


for names in range(int(len(listdir(directory)))):
    
    filename = directory+listdir(directory)[names]
    first_file =  directory+listdir(directory)[0]
    date = first_file.split('/')[3]
    t = filename.split('/')[4].split('png')[0].split('_')[2].split('.')[0]
    #loc = filename.split('/')[4].split('png')[0].split('_')[0]+'_'+filename.split('/')[4].split('png')[0].split('_')[1]
    loc = filename.split('/')[4].split('png')[0].split('_')[1]
    
    im = Image.open(filename)
    image = np.asarray(im)
    #io.imshow(image)
    #io.show()
    
    start = time.time()
    
    global_thresh = 1.5*threshold_otsu(image)#.82
    binary_global = image < global_thresh
    
    #block_size = 40
    #binary_adaptive = threshold_adaptive(image, block_size, offset=10)
    
    	
    labeled_array, num_features = ndimage.measurements.label(binary_global)
    #plt.imshow(binary_global,cmap = plt.gray())
    #plt.show()
    
    eggs = []
    
    properties = regionprops(labeled_array)
    
    
    for i in range(len(properties)):
        area = properties[i].filled_area #(140)
        if area < 2000 and area>100 and properties[i].eccentricity<0.95:# and properties[i].minor_axis_length>10 and properties[i].major_axis_length<65:
            coord = properties[i].centroid
            eggs.append(coord)        
            if area>360:
                coord2 = (properties[i].centroid[0]+4,properties[i].centroid[1]+4)
                eggs.append(coord2)
                if area>600:
                    coord3 = (properties[i].centroid[0]+10,properties[i].centroid[1]-10)
                    eggs.append(coord3)
                    if area>900:
                        coord4 = (properties[i].centroid[0]-10,properties[i].centroid[1]+10)
                        eggs.append(coord4)
            
    
    counter = len(eggs)
    #print eggs
    print '%i eggs' %counter
    
    radius = 22
    image.flags.writeable = True
    for i in range(len(eggs)):
        center_y, center_x = eggs[i]
        cx, cy,val = circle_perimeter_aa(int(center_x),int(center_y), radius)#,shape = image.shape)
        #image[cy,cx] = 255 
        try:        
            image[cy, cx] = 255# (220, 20, 20)# 0
        except IndexError:
            break
    
    ax = plt.axis()
    #plt.imshow(image, cmap=plt.cm.gray)
    #plt.imshow(image,cmap = plt.gray())
    #plt.show()
#plan: use area (or filled_area) to find the eggs, centroid? or coords to get the location of them



          
    # load the image, clone it, and setup the mouse callback function
    #image = cv2.imread(im)
    #small = cv2.resize(image,(0,0),fx=0.25,fy=0.25)
    #clone = image.copy()
    cv2.namedWindow("image",flags = cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", click_and_count)
    small = image
    #small = cv2.pyrDown( image, image, ( image.shape[0]/2, image.shape[1]/2 ))
    # keep looping until the 'q' key is pressed
    datafile = '../Data/egg_count/%s.txt'%date
    text= '#location    time    egg_count#\n'

    while True:
    	# display the image and wait for a keypress
    	#smaller = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    	cv2.imshow("image",small)#, small)
    	key = cv2.waitKey(1) & 0xFF
     
     
    	# if the 'c' key is pressed, break from the loop
    	if key == ord("n"):
             print 'total count = ',counter
             if not path.exists(datafile):
                 with open(datafile,"w") as f:
                     f.write(text)
                     f.close()    
             g=open(datafile,"a")
             text2='%s        %s     %s\n' %(loc, t, counter)
             g.write(text2)
             g.close()
             if counter != 0:
                 #newName = im.split('.png')[0]+'_eggs_%i.png'%counter
                 #rename(im, newName)
                 counter = 0
             break
    	if key == ord("q"):
             sys.exit()
                
             break

     

    # close all open windows
cv2.destroyAllWindows()
    